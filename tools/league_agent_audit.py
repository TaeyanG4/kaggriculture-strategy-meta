"""Read-only, bounded League cohort audit using existing identity/statistics helpers.

Does not run games, refit ratings, register candidates, or modify League state.
Seat pairs are grouped as worlds; notebook aliases never become extra opponents.
"""
import argparse
import collections
import json
import sqlite3
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from kaggriculture_meta.public_league import artifact_digest, match_key, sha256
from kaggriculture_meta.insights import sign_test_two_sided


def audit(db_path, agent_id, since_id=0, through_id=None, expected=None, prefix=None):
    db = sqlite3.connect(db_path.resolve().as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    db.execute('BEGIN')
    agents = {r['id']: dict(r) for r in db.execute('SELECT * FROM agents')}
    agent = agents[agent_id]
    boundary = through_id or db.execute('SELECT MAX(id) FROM matches').fetchone()[0]
    rows = [dict(r) for r in db.execute(
        'SELECT * FROM matches WHERE (agent_a=? OR agent_b=?) AND id>? AND id<=? ORDER BY id',
        (agent_id, agent_id, since_id, boundary))]
    complete = [r for r in rows if r['status'] == 'complete']
    if expected is not None and len(complete) != expected:
        raise ValueError(f'Expected {expected} complete games, found {len(complete)}; no verdict written')
    if not complete:
        raise ValueError('No complete games')
    aliases = collections.defaultdict(list)
    for r in db.execute('''SELECT x.agent_id,x.notebook_title,x.notebook_url,x.is_current,n.origin
        FROM aliases x JOIN notebook_versions v ON v.id=x.version_id
        JOIN notebooks n ON n.id=v.notebook_id ORDER BY x.is_current DESC,x.id DESC'''):
        aliases[r['agent_id']].append(dict(r))
    used = {i for r in complete for i in (r['agent_a'], r['agent_b'])}
    identities, problems = {}, []
    for ident in used:
        a = agents[ident]
        path = Path(a['source_path'])
        names = json.loads(a['artifact_files_json'] or '["main.py"]')
        try:
            files = {n: (path if n == 'main.py' else path.parent / n).read_bytes() for n in names}
            ok = (sha256(files['main.py']) == (a['source_sha256'] or a['sha256'])
                  and artifact_digest(files) == a['sha256'])
            identities[ident] = {'verified': ok, 'sha256': a['sha256'], 'files': names}
        except (OSError, ValueError) as exc:
            identities[ident] = {'verified': False, 'error': str(exc)}
        if not identities[ident]['verified']:
            problems.append({'agent_id': ident, 'issue': 'current artifact identity mismatch'})
    groups, worlds = collections.defaultdict(list), collections.defaultdict(list)
    max_action, changes, settled = 0.0, 0, 0
    matches = []
    for row in complete:
        is_a = row['agent_a'] == agent_id
        opponent = row['agent_b'] if is_a else row['agent_a']
        seat = row['seat_a'] if is_a else 1 - row['seat_a']
        score = row['outcome_a'] if is_a else 1 - row['outcome_a']
        margin = row['margin_a'] if is_a else -row['margin_a']
        data = json.loads(row['result_json'])
        telemetry = data['candidate_telemetry'] if is_a else data['opponent_telemetry']
        timing = data['candidate_timing'] if is_a else data['opponent_timing']
        a, b = agents[row['agent_a']], agents[row['agent_b']]
        checks = {
            'engine_done': data['valid'] and data['statuses'] == ['DONE', 'DONE'] and data['states'] == 720,
            'health': not data.get('health_failures') and not any(data['errors']),
            'calls': timing['calls'] == 719,
            'seed_seat': data['seed'] == data['resolved_seed'] == row['seed'] and data['candidate_seat'] == row['seat_a'],
            'source': data['candidate_sha256'] == (a['source_sha256'] or a['sha256']) and data['opponent_sha256'] == (b['source_sha256'] or b['sha256']),
            'match_key': row['match_key'] == match_key(row['engine_sha'], a['sha256'], b['sha256'], row['seed'], row['seat_a']),
            'cash': data['rewards'][row['seat_a']] == row['reward_a'] and data['rewards'][1-row['seat_a']] == row['reward_b'],
        }
        if prefix:
            c, s = telemetry.get(prefix + '_changes'), telemetry.get(prefix + '_settled')
            checks['settlement_balance'] = c is not None and c == s
            changes += c or 0
            settled += s or 0
        bad = [k for k, v in checks.items() if not v]
        counters = {k: v for k, v in telemetry.items() if k.endswith('_errors') and isinstance(v, (int, float)) and v}
        if bad or counters:
            problems.append({'match_id': row['id'], 'failed_checks': bad, 'nonzero_error_counters': counters})
        max_action = max(max_action, timing['max'])
        item = dict(id=row['id'], opponent_id=opponent, seed=row['seed'], seat=seat,
                    score=score, margin=margin, own=row['reward_a'] if is_a else row['reward_b'])
        matches.append(item)
        groups[opponent].append(item)
        worlds[opponent, row['seed']].append(item)
    pairs_ok = all(len(v) == 2 and {r['seat'] for r in v} == {0, 1} for v in worlds.values())
    if not pairs_ok:
        problems.append({'issue': 'incomplete or repeated world-seat pairs'})
    opponents = []
    for ident, entries in groups.items():
        books = aliases[ident]
        scores = [statistics.mean(r['score'] for r in v) for (i, _), v in worlds.items() if i == ident]
        positive, negative = sum(s > .5 for s in scores), sum(s < .5 for s in scores)
        wins, losses, ties = (sum(r['score'] == v for r in entries) for v in (1, 0, .5))
        opponents.append(dict(id=ident, name=books[0]['notebook_title'] if books else str(ident),
            aliases=books, public=any(b['origin'] != 'local' for b in books),
            rating=agents[ident]['rating'], status=agents[ident]['status'], games=len(entries),
            wins=wins, losses=losses, ties=ties, score_rate=statistics.mean(r['score'] for r in entries),
            mean_margin=statistics.mean(r['margin'] for r in entries), worlds=len(scores),
            worlds_ahead=positive, worlds_behind=negative, worlds_tied=len(scores)-positive-negative,
            world_sign_p=sign_test_two_sided(positive, negative)))
    public_count = sum(o['public'] for o in opponents)
    for o in opponents:
        p = o['world_sign_p']
        o['public_world_sign_bonferroni'] = min(1, p * public_count) if o['public'] and p is not None else None
    opponents.sort(key=lambda x: (x['score_rate'], x['mean_margin'], -x['games']))
    result = dict(agent_id=agent_id, source_sha256=agent['source_sha256'], through_id=boundary,
        since_id=since_id, games=len(complete), status_counts=dict(collections.Counter(r['status'] for r in rows)),
        wins=sum(r['score'] == 1 for r in matches), losses=sum(r['score'] == 0 for r in matches),
        ties=sum(r['score'] == .5 for r in matches), worlds=len(worlds), opponent_count=len(opponents),
        public_source_count=public_count, current_rating=agent['rating'],
        valid_integrity=not problems, problems=problems, artifact_checks=identities,
        max_own_action_seconds=max_action, accelerated_trades=changes, debited_trades=settled,
        engine_contracts=dict(collections.Counter(r['engine_sha'] for r in complete)),
        opponents=opponents, matches=matches,
        limits='Descriptive adaptive League cohort; opponents have different seeds. Paired seats are one world. Exact world sign tests concern frequency of world-level advantage, not mean margin; ties excluded and public multiplicity corrected. Current rating includes other historical games. Runtime/accounting counters do not replace full field ledgers.')
    db.close()
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent-id', type=int, required=True)
    p.add_argument('--db', type=Path, default=ROOT / 'state/public_league/league.sqlite3')
    p.add_argument('--since-id', type=int, default=0)
    p.add_argument('--through-id', type=int)
    p.add_argument('--expected-games', type=int)
    p.add_argument('--telemetry-prefix')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    result = audit(args.db, args.agent_id, args.since_id, args.through_id, args.expected_games, args.telemetry_prefix)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), 'utf8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('opponents', 'matches', 'artifact_checks', 'limits')}, ensure_ascii=False))
    for o in result['opponents']:
        if o['public'] and o['score_rate'] <= .5:
            print(o['id'], o['name'], 'W-L-T', o['wins'], o['losses'], o['ties'], 'worlds', o['worlds'], 'margin', o['mean_margin'])
