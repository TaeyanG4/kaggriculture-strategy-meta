"""USER-RUN phase 1: replay accounting, baseline controls, selection comparison.

No upload or holdout execution. A single command resumes only identical inputs.
Each engine job runs in a fresh process. Root results.json is authoritative.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import statistics
import subprocess
import sys

from .league import ROOT, digest, engine_identity, prepare, run_jobs, write_json

DEFAULT = ROOT / 'state/agent_experiments/championship_phase1_20260913'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def require_valid(rows, expected):
    if len(rows) != expected or any(not r.get('valid') for r in rows):
        raise ValueError('Incomplete or invalid evaluation; do not select a candidate')
    for row in rows:
        counts = row.get('candidate_telemetry', {})
        if any('error' in k.lower() and isinstance(v, (int, float)) and v > 0 for k, v in counts.items()):
            raise ValueError('Internal candidate error: ' + str(row.get('match_id', row.get('episode'))))
        if row.get('candidate_timing', {}).get('over_1s', 0):
            raise ValueError('Candidate exceeded 1 second; review before continuing')


def paired_comparison(control, candidate):
    def key(r):
        return r['seed'], r['candidate_seat'], r['opponent_sha256']
    left, right = {key(r): r for r in control}, {key(r): r for r in candidate}
    if len(left) != len(control) or len(right) != len(candidate) or set(left) != set(right):
        raise ValueError('Panels do not match or contain duplicate games')
    pairs = []
    for k in sorted(left):
        a, b = left[k], right[k]
        score = lambda m: 1.0 if m > 0 else 0.5 if m == 0 else 0.0
        pairs.append({'seed': k[0], 'seat': k[1], 'opponent': a['opponent_name'],
                      'family': a['opponent_family'], 'control_margin': a['margin'],
                      'candidate_margin': b['margin'], 'margin_delta': b['margin']-a['margin'],
                      'score_delta': score(b['margin'])-score(a['margin'])})
    blocks = [statistics.mean(r['score_delta'] for r in pairs if r['seed'] == seed)
              for seed in sorted({r['seed'] for r in pairs})]
    interval = None
    if len(blocks) > 1 and len(set(blocks)) > 1:
        rng = random.Random(813091)
        samples = sorted(statistics.mean(rng.choices(blocks, k=len(blocks))) for _ in range(5000))
        interval = [samples[124], samples[4874]]
    return {'games': len(pairs), 'score_rate_delta': statistics.mean(blocks),
            'seed_block_bootstrap_95': interval,
            'interval_note': 'Conditional on these related opponents; unavailable for degenerate seed blocks.',
            'mean_margin_delta': statistics.mean(r['margin_delta'] for r in pairs),
            'wins_to_losses': sum(r['control_margin'] > 0 and r['candidate_margin'] < 0 for r in pairs),
            'losses_to_wins': sum(r['control_margin'] < 0 and r['candidate_margin'] > 0 for r in pairs),
            'pairs': pairs}


def worker(path):
    job = read(path)
    if job['kind'] == 'accounting':
        from .replay_accounting import execute
        execute(job)
    else:
        from .replay_lab import evaluate
        result = evaluate(job)
        require_valid([result], 1)
        if job['kind'] == 'c111_reproduction':
            if result['rewards'] != result['original_rewards'] or not result['same_shop_sequence']:
                raise ValueError('Submitted c111 does not reproduce live game')
        write_json(Path(job['output']), result)


def launch(job, path):
    result_path = Path(job['output'])
    if path.exists() and read(path) != job:
        raise ValueError('Job changed; use a new directory')
    write_json(path, job)
    if not result_path.exists():
        with path.with_suffix('.log').open('w', encoding='utf-8') as log:
            subprocess.run([sys.executable, '-m', 'src.kaggriculture_meta.championship_phase1',
                            '--job', str(path)], cwd=ROOT, stdout=log, stderr=log,
                           check=True, timeout=120)
    result = read(result_path)
    if not result.get('valid'):
        raise ValueError('Invalid job: ' + str(path))
    if job['kind'] == 'c111_reproduction':
        if result['rewards'] != result['original_rewards'] or not result['same_shop_sequence']:
            raise ValueError('Cached c111 result does not reproduce live game')
    return result


def run(out, workers):
    manifest = read(out / 'manifest.json')
    if engine_identity() != manifest['engine']:
        raise ValueError('Pinned engine changed; do not mix engines')
    for asset in manifest['assets']:
        path = ROOT / asset['path']
        if digest(path.read_bytes()) != asset['sha256']:
            raise ValueError('Pinned input changed: ' + asset['path'])
        if path.suffix == '.py':
            compile(path.read_bytes(), str(path), 'exec')
    lock = out / 'run.lock'
    try:
        with lock.open('x', encoding='utf-8') as stream:
            stream.write('One phase-1 coordinator owns this study.\n')
    except FileExistsError:
        raise SystemExit('Run lock exists. Do not start a second coordinator; report it.')
    result_path = out / 'results.json'
    previous = read(result_path) if result_path.exists() else {}
    report = {'status': 'running', 'manifest_sha256': digest((out/'manifest.json').read_bytes()),
              'stage': 'recorded_accounting', 'holdout_run': False, 'submission_performed': False,
              'selection_run': False,
              'planned_native_games': 416, 'completed_diagnostic_jobs': 0, 'native': {}, 'diagnostics': []}
    if previous.get('manifest_sha256') not in (None, report['manifest_sha256']):
        lock.unlink()
        raise ValueError('Study identity changed')
    try:
        write_json(result_path, report)
        print('Preflight: run phase-1 accounting and paired-comparison contract tests.', flush=True)
        subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests',
                        '-p', 'test_championship_phase1.py', '-v'],
                       cwd=ROOT, check=True)
        report['contract_tests'] = 'passed'
        write_json(result_path, report)
        sources = {a['name']: {'path': str((ROOT/a['path']).resolve()), 'sha256': a['sha256'],
                               'source': a['path']} for a in manifest['candidates']}
        replay_manifest = read(out/'replay_manifest.json')
        print('Phase 1/3: 5 exact accounting replays, 5 c111 reproductions, 5 c110 diagnostics.', flush=True)
        for kind in ('accounting', 'c111_reproduction', 'c110_diagnostic'):
            for item in replay_manifest['records']:
                tag = f"{kind}_{item['episode']}"
                job_path = out/'diagnostics'/f'{tag}.json'
                job = {'kind': kind, 'engine': manifest['engine'], 'episode': item['episode'],
                       'replay': str((ROOT/item['path']).resolve()), 'replay_sha256': item['sha256'],
                       'output': str(job_path.with_suffix('.result.json')),
                       'accounting_sha256': manifest['accounting_sha256'],
                       'mode': 'native_frozen_opponent', 'candidate_seat': item['seat']}
                if kind != 'accounting':
                    replay = read(ROOT/item['path'])
                    job.update(candidate=sources['c111' if kind == 'c111_reproduction' else 'c110'],
                               opponent_name=replay['info']['TeamNames'][1-item['seat']],
                               evidence_type='recorded_diagnostic_not_reacting_policy')
                value = launch(job, job_path)
                if kind != 'accounting':
                    require_valid([value], 1)
                report['diagnostics'].append({'kind': kind, 'episode': item['episode'], 'valid': True,
                                              'margin': value.get('margin'), 'path': str(Path(job['output']).relative_to(ROOT))})
                report['completed_diagnostic_jobs'] += 1
                write_json(result_path, report)
                print(f"Diagnostic {report['completed_diagnostic_jobs']}/15: {tag} valid", flush=True)
        plan = read(out/'selection_plan.json')
        for name in ('c110', 'c111'):
            report['stage'] = 'selection_' + name
            report['selection_run'] = True
            write_json(result_path, report)
            print(f'Phase 2/3: {name}, 192 selection games, 16 seeds x 2 seats x 6 related opponents.', flush=True)
            location = out/'selection'/name
            identity, jobs = prepare(plan, ROOT/manifest['candidate_paths'][name], 'selection', location)
            if len(jobs) != 192:
                raise ValueError('Unexpected opponent deduplication')
            summary = run_jobs(identity, jobs, location, workers=workers)
            rows = [json.loads(line) for line in (location/'matches.jsonl').read_text(encoding='utf-8').splitlines()]
            require_valid(rows, 192)
            report['native'][name] = summary
            write_json(result_path, report)
        report['stage'] = 'direct_head_to_head'
        write_json(result_path, report)
        print('Phase 3/3: c111 vs c110, 32 paired selection games. No holdout.', flush=True)
        direct = read(out/'direct_plan.json')
        location = out/'direct'
        identity, jobs = prepare(direct, ROOT/manifest['candidate_paths']['c111'], 'selection', location)
        if len(jobs) != 32:
            raise ValueError('Unexpected direct panel')
        report['direct'] = run_jobs(identity, jobs, location, workers=workers)
        rows = [json.loads(line) for line in (location/'matches.jsonl').read_text(encoding='utf-8').splitlines()]
        require_valid(rows, 32)
        controls = [json.loads(line) for line in (out/'selection/c110/matches.jsonl').read_text(encoding='utf-8').splitlines()]
        candidates = [json.loads(line) for line in (out/'selection/c111/matches.jsonl').read_text(encoding='utf-8').splitlines()]
        report['paired_comparison'] = paired_comparison(controls, candidates)
        report.update(status='complete', stage='complete', selection_run=True,
                      note='Selection seeds are observed after this run. No automatic winner promotion. Holdout48 untouched.')
        write_json(result_path, report)
        print('DONE: ' + str(result_path), flush=True)
    except BaseException as exc:
        report.update(status='failed', error_type=type(exc).__name__, error=str(exc)[:500])
        write_json(result_path, report)
        raise
    finally:
        lock.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, default=DEFAULT)
    ap.add_argument('--workers', type=int, choices=range(1, 9), default=4)
    ap.add_argument('--job', type=Path)
    args = ap.parse_args()
    if args.job:
        worker(args.job)
    else:
        run(args.out.resolve(), args.workers)


if __name__ == '__main__':
    main()
