"""Sequential knob sweep of the planner proxy vs a fixed opponent on pinned worlds (o_tools/proxy_eval.py per variant).
Each variant runs as its own subprocess with PROXY_KNOBS set; results append to o_results/proxy/sweep.txt.
Usage: python o_tools/proxy_sweep.py [--a agent/o227_stealth_drop.py] [--seeds 7000-7015] [--workers 8]"""
import argparse, os, subprocess, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARIANTS = ['', 'feed=3.0', 'feed=4.5', 'straw=20', 'straw=32', 'wheat_units=3', 'land3=9', 'buf=2', 'buf=6', 'feed=3.0,wheat_units=3', 'straw=32,land3=9']
ap = argparse.ArgumentParser(); ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--seeds', default='7000-7015'); ap.add_argument('--workers', default='8')
args = ap.parse_args(); out = os.path.join(ROOT, 'o_results', 'proxy', 'sweep.txt')
for v in VARIANTS:
    env = dict(os.environ, PROXY_KNOBS=v, PYTHONIOENCODING='utf-8'); tag = 'sweep_' + (v.replace('=', '').replace(',', '_') or 'base'); t0 = time.time()
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'o_tools', 'proxy_eval.py'), '--a', args.a, '--b', 'agent/opp_planner_proxy.py', '--seeds', args.seeds, '--workers', args.workers, '--label', tag], env=env, capture_output=True, text=True, cwd=ROOT)
    line = [l for l in r.stdout.splitlines() if l.startswith('[')]
    with open(out, 'a', encoding='utf-8') as f:
        f.write(f"{time.strftime('%m-%d %H:%M')} knobs={v or 'base'} {int(time.time()-t0)}s {line[0] if line else 'ERROR ' + r.stderr[-200:]}\n")
