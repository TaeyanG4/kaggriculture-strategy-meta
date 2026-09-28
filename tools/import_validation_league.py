"""Bulk-import complete native validation campaigns into Public League ratings.

check is read-only. apply is transactional and idempotent; it never registers
agents or runs games. Incomplete campaigns and unknown identities are refused.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tools'))
from src.kaggriculture_meta import public_league as league


class ImportRejected(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ImportRejected(message)


def read(path):
    return json.loads(Path(path).read_text('utf-8-sig'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), 'utf8')
    temporary.replace(path)


def checked_campaign(path):
    """Reuse the frozen runner's identity, coverage, and row checks, without games."""
    if (Path(path) / 'bounded-import.json').exists():
        from bounded_validation_import import checked_bounded
        return checked_bounded(path)
    import validation_v2 as validation
    import validation_v3
    path = Path(path).resolve()
    require((path / 'results.json').exists(), f'Campaign unfinished: {path}')
    result = read(path / 'results.json')
    require(result.get('status') == 'complete', f'Campaign unfinished: {path}')
    preliminary = read(path / 'manifest.json')
    previous = (validation.__file__, validation.SUPPORT[:], validation.L.health_failures)
    try:
        if preliminary['plan'].get('arena_meta', {}).get('validation_health_policy') == 'official_overage_v3':
            validation_v3.install()
        manifest = validation.check(path)
        rows = validation.load_rows(path, manifest)
    finally:
        validation.__file__, validation.SUPPORT, validation.L.health_failures = previous
    require(manifest['stage'] in ('screen', 'confirm', 'final'), 'Unsupported validation stage')
    require(manifest['plan']['configuration'] == league.ENGINE_CONFIG, 'League configuration differs')
    require(len(rows) == result.get('completed_jobs') == manifest['expected_jobs'], 'Incomplete result coverage')
    require(result.get('contract_sha256') == manifest['contract_sha256'], 'Saved result contract differs')
    jobs = {job['match_id']: job for job in manifest['jobs']}
    require(len(jobs) == len(rows) == len({row['match_id'] for row in rows}), 'Duplicate/missing jobs')
    return manifest, rows


def path_key(path):
    return os.path.normcase(str(Path(path).resolve()))


class AgentResolver:
    def __init__(self, db, explicit=None):
        self.agents = [dict(row) for row in db.execute('SELECT * FROM agents')]
        self.registered = {r[0] for r in db.execute('''SELECT DISTINCT a.id FROM agents a
            JOIN aliases x ON x.agent_id=a.id JOIN notebook_versions v ON v.id=x.version_id
            JOIN notebooks n ON n.id=v.notebook_id''')}
        self.cache = {}
        self.explicit = explicit or {}
        self.missing = {}

    def resolve(self, ref, original):
        source_sha = ref['sha256']
        key = (source_sha, path_key(original['path']))
        if key in self.cache:
            return self.cache[key]
        candidates = [a for a in self.agents if (a['source_sha256'] or a['sha256']) == source_sha]
        normalization = None
        if not candidates:
            original_path = Path(original['path'])
            if not original_path.is_absolute():
                original_path = ROOT / original_path
            raw = original_path.read_bytes()
            require(hashlib.sha256(raw).hexdigest() == source_sha, 'Original validation source drift')
            normalized = raw.replace(b'\r\n', b'\n')
            normalized_sha = hashlib.sha256(normalized).hexdigest()
            # League canonicalizes Python newlines on upload. Permit precisely
            # that transform; do not merge AST-similar or otherwise edited code.
            if raw != normalized and b'\r' not in normalized:
                candidates = [a for a in self.agents if (a['source_sha256'] or a['sha256']) == normalized_sha]
                if candidates:
                    # Marshal's reference/intern flags can differ for equal code
                    # objects in large modules. Compare compiled code directly;
                    # exact CRLF-only bytes are still required below.
                    require(compile(raw, '<newline-identity>', 'exec') ==
                            compile(normalized, '<newline-identity>', 'exec'),
                            'CRLF conversion changed compiled Python')
                    normalization = dict(transform='CRLF_to_LF_only', validation_sha256=source_sha,
                                         league_sha256=normalized_sha, compiled_code_equal=True)
        if source_sha in self.explicit:
            candidates = [a for a in candidates if a['id'] == int(self.explicit[source_sha])]
            require(len(candidates) == 1, f'Explicit agent map does not match {source_sha}')
        else:
            exact = [a for a in candidates if path_key(a['source_path']) == key[1]]
            if exact:
                candidates = exact
        if not candidates:
            self.missing[source_sha] = str(original['path'])
            self.cache[key] = None
            return None
        require(len(candidates) == 1, f'Ambiguous source {source_sha}; supply --agent-map source SHA to local ID')
        agent = dict(candidates[0])
        require(agent['id'] in self.registered, f'Agent {agent["id"]} has no registered League alias')
        require(agent['qa_status'] == 'pass' and agent['execution_platform'] == 'host', f'Agent {agent["id"]} is not QA-passing host Python')
        registered_sha = agent['source_sha256'] or agent['sha256']
        require(digest(agent['source_path']) == registered_sha, f'Local agent {agent["id"]} source drift')
        if normalization:
            require(Path(agent['source_path']).read_bytes() == normalized, 'Registered newline conversion differs')
            agent['_validation_source_identity'] = normalization
        members = set(json.loads(agent['artifact_files_json'] or '["main.py"]'))
        documentation = {name for name in members if re.fullmatch(r'README(?:[_-][A-Za-z0-9_-]+)?\.(?:md|txt|rst)', name, re.I)}
        require('main.py' in members and members <= {'main.py', 'LICENSE.txt', 'NOTICE.txt'} | documentation,
                f'Runtime sidecars not present in validation snapshot: agent {agent["id"]}')
        payload = {'main.py': Path(agent['source_path']).read_bytes()}
        for member in members - {'main.py'}:
            payload[member] = Path(agent['source_path']).with_name(member).read_bytes()
        require(league.artifact_digest(payload) == agent['sha256'], f'Agent {agent["id"]} artifact drift')
        self.cache[key] = agent
        return agent


def validate_result(row):
    result = league.normalize_public_league_result(copy.deepcopy(row))
    require(result.get('mode') == 'native_reacting', 'Frozen/replay games cannot affect League ratings')
    require(result.get('valid') is True and result.get('statuses') == ['DONE', 'DONE'] and result.get('states') == 720,
            'Invalid or incomplete game')
    require(result.get('errors') == [[], []] and not result.get('health_failures'), 'Execution failure')
    require(result.get('seed') == result.get('resolved_seed'), 'Resolved seed differs')
    require(result.get('candidate_seat') in (0, 1), 'Invalid seat')
    require(all(result.get(role + '_timing', {}).get('calls') == 719 for role in ('candidate', 'opponent')), 'Missing actions')
    rewards = result.get('rewards', [])
    require(len(rewards) == 2 and all(type(x) in (int, float) and math.isfinite(x) for x in rewards), 'Invalid rewards')
    seat = result['candidate_seat']
    margin = rewards[seat] - rewards[1 - seat]
    require(result.get('margin') == margin, 'Reward/margin mismatch')
    require(result.get('outcome') == ('win' if margin > 0 else 'loss' if margin < 0 else 'tie'), 'Outcome mismatch')
    require(len(result.get('action_hashes', [])) == 2 and all(isinstance(h, str) and re.fullmatch('[a-f0-9]{64}', h) for h in result['action_hashes']), 'Missing action identity')
    require(type(result.get('seconds')) in (int, float) and math.isfinite(result['seconds']) and result['seconds'] >= 0,
            'Invalid runtime')
    return result


def converted(row, candidate, opponent, eng, provenance):
    result = validate_result(row)
    for role, agent in (('candidate', candidate), ('opponent', opponent)):
        identity = agent.get('_validation_source_identity')
        if identity:
            require(result[role + '_sha256'] == identity['validation_sha256'], 'Normalization source mismatch')
            provenance.setdefault('source_identity_transforms', {})[role] = dict(identity)
            result[role + '_sha256'] = identity['league_sha256']
    a, b = sorted((candidate, opponent), key=lambda item: item['sha256'])
    seat = result['candidate_seat'] if a['id'] == candidate['id'] else 1 - result['candidate_seat']
    if a['id'] != candidate['id']:
        for one, two in (('candidate_sha256', 'opponent_sha256'), ('candidate_timing', 'opponent_timing'),
                         ('candidate_telemetry', 'opponent_telemetry')):
            result[one], result[two] = result.get(two), result.get(one)
        provenance['original_candidate_checkpoints'] = result.pop('checkpoints', [])
        result['checkpoints'] = []
        for name in ('public_league_warnings', 'timing_warnings'):
            result[name] = [x.replace('candidate_', 'opponent_', 1) if x.startswith('candidate_') else
                            x.replace('opponent_', 'candidate_', 1) if x.startswith('opponent_') else x
                            for x in result.get(name, [])]
    require(result['candidate_sha256'] == (a['source_sha256'] or a['sha256']) and
            result['opponent_sha256'] == (b['source_sha256'] or b['sha256']), 'Canonical source orientation mismatch')
    key = league.match_key(eng, a['sha256'], b['sha256'], row['seed'], seat)
    ra, rb = result['rewards'][seat], result['rewards'][1 - seat]
    result.update(candidate_seat=seat, margin=ra-rb, outcome='win' if ra>rb else 'loss' if ra<rb else 'tie',
                  opponent_name=b['sha256'][:12], opponent_family='public_notebook',
                  stage='public_league_imported_validation', match_id=key[:24], import_provenance=provenance)
    return dict(key=key, engine_sha=eng, a=a['id'], b=b['id'], seed=row['seed'], seat_a=seat,
                ra=ra, rb=rb, margin=ra-rb, score=1.0 if ra>rb else 0.0 if ra<rb else .5, result=result)


def same_record(existing, planned):
    require(existing['status'] == 'complete', f'Existing match is not complete: {planned["key"]}')
    for column, value in [('engine_sha', planned['engine_sha']), ('agent_a', planned['a']), ('agent_b', planned['b']),
                          ('seed', planned['seed']), ('seat_a', planned['seat_a']), ('reward_a', planned['ra']),
                          ('reward_b', planned['rb']), ('margin_a', planned['margin']), ('outcome_a', planned['score'])]:
        require(existing[column] == value, f'Existing match conflict: {column} / {planned["key"]}')
    result = validate_result(json.loads(existing['result_json']))
    for key in ('candidate_sha256', 'opponent_sha256', 'action_hashes', 'rewards', 'candidate_seat'):
        require(result[key] == planned['result'][key], f'Existing result conflict: {key} / {planned["key"]}')


def prepare(db, campaigns, explicit=None, loader=checked_campaign):
    resolver = AgentResolver(db, explicit)
    eng = league.engine_sha()
    has_refs = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='validation_import_refs'").fetchone()
    planned, stages = {}, []
    self_games = duplicate_inputs = pending = total = 0
    for path in sorted({Path(p).resolve() for p in campaigns}):
        manifest, rows = loader(path)
        metadata = dict(path=str(path), stage=manifest['stage'], contract_sha256=manifest['contract_sha256'],
                        manifest_sha256=digest(path/manifest.get('_manifest_file', 'manifest.json')),
                        results_sha256=digest(path/manifest.get('_results_file', 'results.json')), games=len(rows))
        stages.append(metadata)
        jobs = {j['match_id']: j for j in manifest['jobs']}
        for row in rows:
            total += 1
            validate_result(row)
            job = jobs[row['match_id']]
            c = resolver.resolve(job['candidate'], manifest['plan']['models'][job['candidate']['name']])
            o = resolver.resolve(job['opponent'], manifest['plan']['opponents'][job['opponent']['name']])
            if c is None or o is None:
                pending += 1
                continue
            if c['id'] == o['id'] or row['candidate_sha256'] == row['opponent_sha256']:
                self_games += 1
                continue
            provenance = dict(source='native_validation', campaign=str(path), contract_sha256=manifest['contract_sha256'],
                original_match_id=row['match_id'], original_stage=row['stage'], original_model=job['candidate']['name'],
                original_opponent=job['opponent']['name'], original_candidate_seat=row['candidate_seat'],
                result_sha256=digest(manifest.get('_result_files', {}).get(row['match_id'], path/'jobs'/row['match_id']/'result.json')),
                workers=manifest['plan']['workers'], selection='All valid scheduled results, including losses; fixed validation panel, not random League matchmaking')
            provenance.update(manifest.get('_row_provenance', {}).get(row['match_id'], {}))
            item = converted(row, c, o, eng, provenance)
            ref = dict(contract=provenance['contract_sha256'], match_id=row['match_id'],
                       result_sha256=provenance['result_sha256'])
            item['refs'] = [ref]
            if has_refs:
                imported = db.execute('''SELECT r.result_sha256,m.* FROM validation_import_refs r
                    JOIN matches m ON m.match_key=r.match_key
                    WHERE r.contract_sha256=? AND r.original_match_id=?''',
                    (ref['contract'],ref['match_id'])).fetchone()
                if imported:
                    require(imported['result_sha256'] == ref['result_sha256'], 'Previously imported result changed')
                    # Tool/League wrapper changes must not turn the same historical
                    # outcome into a second rating observation.
                    item.update(key=imported['match_key'], engine_sha=imported['engine_sha'])
                    item['result']['match_id'] = imported['match_key'][:24]
            if item['key'] in planned:
                other = planned[item['key']]
                require(other['result']['rewards'] == item['result']['rewards'] and
                        other['result']['action_hashes'] == item['result']['action_hashes'], 'Duplicate input has conflicting results')
                duplicate_inputs += 1
                other['refs'].append(ref)
            else:
                planned[item['key']] = item
    existing = 0
    for item in planned.values():
        prior = db.execute('SELECT * FROM matches WHERE match_key=?', (item['key'],)).fetchone()
        if prior:
            same_record(prior, item)
            item['existing_id'] = prior['id']
            existing += 1
    summary = dict(engine_sha=eng, stages=stages, input_games=total, self_games_excluded=self_games,
        duplicate_inputs=duplicate_inputs, eligible_games=len(planned), already_present=existing,
        new_games=len(planned)-existing, pending_unregistered_games=pending, missing_agents=resolver.missing,
        ready=not resolver.missing, policy='No automatic registration, source replacement, games, or retirement changes.')
    return list(planned.values()), summary


def receipt_id(summary):
    data = dict(contracts=sorted(x['contract_sha256'] for x in summary['stages']))
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()[:24]


def apply_batch(store, planned, summary, receipt_path):
    require(summary['ready'], 'Unregistered sources: register a qualified candidate first, then retry the same command')
    timestamp = league.utcnow()
    ids = sorted({x for p in planned for x in (p['a'], p['b'])})
    snapshot = lambda: {str(i): dict(store.db.execute('SELECT id,games,wins,losses,ties,rating,status FROM agents WHERE id=?', (i,)).fetchone()) for i in ids}
    before = snapshot()
    prior_receipt = read(receipt_path) if Path(receipt_path).exists() else None
    if prior_receipt:
        require(prior_receipt['keys'] == sorted(p['key'] for p in planned), 'Receipt input differs')
    # One transaction for all outcomes. A restart after this commit can recheck
    # identities and finish the ranking pass without duplicating any games.
    with store.db:
        store.db.execute('''CREATE TABLE IF NOT EXISTS validation_import_refs(
            contract_sha256 TEXT NOT NULL, original_match_id TEXT NOT NULL,
            result_sha256 TEXT NOT NULL, match_key TEXT NOT NULL,
            PRIMARY KEY(contract_sha256,original_match_id))''')
        for p in planned:
            if 'existing_id' not in p:
                store.db.execute('''INSERT INTO matches(match_key,engine_sha,agent_a,agent_b,seed,seat_a,
                    status,outcome_a,reward_a,reward_b,margin_a,runtime,error,result_json,created_at,completed_at)
                    VALUES(?,?,?,?,?,?,'complete',?,?,?,?,?,NULL,?,?,?)''',
                    (p['key'],p['engine_sha'],p['a'],p['b'],p['seed'],p['seat_a'],p['score'],p['ra'],p['rb'],p['margin'],
                     p['result']['seconds'],json.dumps(p['result'],ensure_ascii=False),timestamp,timestamp))
            for ref in p['refs']:
                store.db.execute('''INSERT OR IGNORE INTO validation_import_refs
                    (contract_sha256,original_match_id,result_sha256,match_key) VALUES(?,?,?,?)''',
                    (ref['contract'],ref['match_id'],ref['result_sha256'],p['key']))
    if summary['new_games'] or not prior_receipt or not prior_receipt.get('ratings_updated'):
        league.update_rankings(store)
    for p in planned:
        same_record(store.db.execute('SELECT * FROM matches WHERE match_key=?', (p['key'],)).fetchone(), p)
    after = snapshot()
    for i in ids:
        # Agent stats may be stale if a previous process stopped between the
        # transaction commit and the rating pass. Verify against durable rows.
        expected = store.db.execute('''SELECT
            (SELECT COUNT(*) FROM matches WHERE status='complete' AND agent_a=?) +
            (SELECT COUNT(*) FROM matches WHERE status='complete' AND agent_b=?)''', (i, i)).fetchone()[0]
        require(after[str(i)]['games'] == expected, f'Agent {i} game-count readback differs')
    record = dict(imported_at=timestamp,summary=summary,keys=sorted(p['key'] for p in planned),
                  before=before,after=after,ratings_updated=True)
    if not prior_receipt or summary['new_games']:
        atomic_json(receipt_path, record)
    if summary['new_games']:
        store.event('league_import', f'Validation batch: {summary["new_games"]} games imported',
                    dict(receipt=str(receipt_path), contracts=[x['contract_sha256'] for x in summary['stages']]))
    return dict(imported_new=summary['new_games'], verified_total=len(planned), ratings_updated=True,
                receipt=str(receipt_path), agents=after)


def prepare_readonly(state, campaigns, explicit=None):
    db = sqlite3.connect((state/'league.sqlite3').as_uri()+'?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    try:
        return prepare(db, campaigns, explicit)
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('check','apply','verify','seal-bounded'))
    parser.add_argument('campaigns', nargs='+', type=Path)
    parser.add_argument('--state', type=Path, default=league.DEFAULT_STATE)
    parser.add_argument('--agent-map', type=Path, help='Optional JSON mapping source SHA256 to an existing local ID')
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    if args.mode == 'seal-bounded':
        from bounded_validation_import import seal_bounded
        for path in args.campaigns:
            print(json.dumps(seal_bounded(path), ensure_ascii=False))
        return
    explicit = read(args.agent_map) if args.agent_map else None
    state = args.state.resolve()
    if args.mode != 'apply':
        planned, summary = prepare_readonly(state, args.campaigns, explicit)
        if args.mode == 'verify':
            require(summary['ready'] and summary['new_games'] == 0, 'Batch is not completely imported')
        print(json.dumps(summary, ensure_ascii=False))
        return
    with league.process_lock(state/'league.lock') as acquired:
        require(acquired, 'League cycle or another import is active; retry after it stops')
        planned, summary = prepare_readonly(state, args.campaigns, explicit)
        require(summary['ready'], 'Unregistered sources: register a qualified candidate first, then retry the same command')
        store = league.Store(state)
        try:
            receipt = args.receipt or state/'validation-imports'/(receipt_id(summary)+'.json')
            print(json.dumps(apply_batch(store, planned, summary, receipt), ensure_ascii=False))
        finally:
            store.close()


if __name__ == '__main__':
    try:
        # Library startup messages are not per-game progress output.
        main()
    except (ImportRejected, ValueError) as error:
        print(json.dumps(dict(status='not_imported', error=str(error)), ensure_ascii=False))
        raise SystemExit(2)
