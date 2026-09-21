"""Build the world-profile tuning pool: pins the shop sequences of extra seeds, runs the base planner on all pool seeds (label
base<N>_pool) and writes o_results/proxy/pool_seeds.json = {tune: {bucket: [seeds]}, hold: {bucket: [seeds]}}.
Tune = 7000-7047 + 7300-7331, hold = 7332-7363 (blind blocks 7208+ stay untouched).
Usage: python o_tools/build_pool.py --base base17 --workers 12"""
import argparse, json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
from proxy_eval import bucket

TUNE = list(range(7000, 7048)) + list(range(7300, 7332))
HOLD = list(range(7332, 7364))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--base', default='base17'); ap.add_argument('--workers', type=int, default=12); ap.add_argument('--agent', default='agent/p000_planner.py')
    a = ap.parse_args()
    seeds = TUNE + HOLD
    env = dict(os.environ, PROXY_KNOBS='', PYTHONIOENCODING='utf-8', MPLBACKEND='Agg')
    subprocess.run([sys.executable, os.path.join(ROOT, 'o_tools', 'proxy_eval.py'), '--a', 'agent/o227_stealth_drop.py', '--b', a.agent,
                    '--seed-list', ','.join(map(str, seeds)), '--workers', str(a.workers), '--label', a.base + '_pool'], env=env, cwd=ROOT)
    shops = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    out = {'tune': {}, 'hold': {}}
    for name, lst in (('tune', TUNE), ('hold', HOLD)):
        for s in lst:
            out[name].setdefault(bucket(shops[str(s)]), []).append(s)
    json.dump(out, open(os.path.join(ROOT, 'o_results', 'proxy', 'pool_seeds.json'), 'w'), indent=1)
    for name in ('tune', 'hold'):
        print(name, {k: len(v) for k, v in sorted(out[name].items())})


if __name__ == '__main__':
    main()
