"""Stratified world-bank evaluation: candidate vs a few opponents on the seeds of each world bucket.
Results are cached per (tag, bucket, opponent) so a baseline is played once and every later candidate
is compared paired (same seed, same seat, same opponent) with a bootstrap 95% CI per bucket.
Usage:
  python o_tools/stratified_pool.py run  <tag> <agent.py> [--workers 8]
  python o_tools/stratified_pool.py compare <tag> <base_tag>
Opponents: c150 (lineage mirror), V43, Farming Score V4, Market-Smart (edit OPPONENTS to change).
"""
import argparse, json, os, random, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
OPPONENTS = {
    'c150': 'agent/c150.py',
    'v43': 'state/o_dev/public_pull/kaggriculture-v43-recovering-lost-harvests/extracted_main.py',
    'fsv4': 'state/o_dev/public_pull/farming-score-v4-a-better-shop-20260915/extracted_main.py',
    'msf': 'state/o_dev/public_pull/market-smart-farming-kaggriculture-20260915/extracted_main.py',
}


def bank():
    return json.load(open(os.path.join(ROOT, 'o_tools', 'world_bank.json')))


def run(tag, agent, workers, only=None):
    b = bank(); b = {k: v for k, v in b.items() if not only or k in only}; out = os.path.join(ROOT, 'o_results', 'strat', tag); os.makedirs(out, exist_ok=True)
    jobs = [(bk, op) for bk in b for op in OPPONENTS]
    for i, (bk, op) in enumerate(jobs):
        jf = os.path.join(out, f'{bk}__{op}.json')
        if os.path.exists(jf):
            continue
        seeds = ','.join(map(str, b[bk]))
        print(f'[{i+1}/{len(jobs)}] {tag} {bk} vs {op} ({len(b[bk])} seeds x 2 seats)', flush=True)
        subprocess.run([PY, os.path.join(ROOT, 'tools', 'o_arena.py'), os.path.join(ROOT, agent), os.path.join(ROOT, OPPONENTS[op]),
                        '--seed-list', seeds, '--workers', str(workers), '--json-out', jf],
                       cwd=ROOT, env=dict(os.environ, MPLBACKEND='Agg'), capture_output=True, text=True, timeout=7200)
    print('done', tag)


def load(tag):
    d = {}
    for f in os.listdir(os.path.join(ROOT, 'o_results', 'strat', tag)):
        bk, op = f[:-5].split('__')
        for r in json.load(open(os.path.join(ROOT, 'o_results', 'strat', tag, f)))['results']:
            if r['outcome'] in ('win', 'loss', 'tie'):
                d[(bk, op, r['seed'], r['seat'])] = r['margin']
    return d


def ci(d):
    random.seed(0); n = len(d); ms = []
    for _ in range(2000):
        s = [d[random.randrange(n)] for _ in range(n)]; ms.append(sum(s) / n)
    ms.sort(); return ms[50], ms[1949]


def compare(tag, base):
    a = load(tag); b = load(base); buckets = sorted({k[0] for k in a})
    print(f'{tag} vs {base}: paired margin delta per world bucket (candidate - base, same seed/seat/opponent)')
    for bk in buckets:
        keys = [k for k in a if k[0] == bk and k in b]
        if not keys:
            continue
        d = [a[k] - b[k] for k in keys]; mean = sum(d) / len(d); lo, hi = ci(d)
        wins = sum(a[k] > 0 for k in keys); bwins = sum(b[k] > 0 for k in keys)
        by_op = {op: round(sum(a[k] - b[k] for k in keys if k[1] == op) / max(1, sum(1 for k in keys if k[1] == op))) for op in OPPONENTS}
        flag = 'SIG+' if lo > 0 else ('SIG-' if hi < 0 else 'n.s.')
        print(f'  {bk:9s} n={len(d):3d} delta {mean:+6.0f} CI[{lo:+.0f},{hi:+.0f}] {flag:4s} | wins {wins}/{len(keys)} (base {bwins}) | by opp {by_op}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['run', 'compare']); ap.add_argument('tag'); ap.add_argument('arg2')
    ap.add_argument('--workers', type=int, default=8); ap.add_argument('--buckets', default=None, help='comma list to restrict run'); a = ap.parse_args()
    run(a.tag, a.arg2, a.workers, a.buckets.split(',') if a.buckets else None) if a.cmd == 'run' else compare(a.tag, a.arg2)
