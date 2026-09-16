"""Compile the o209 livestock policy table from engine rollouts (approach A-1).
For every non-yarn first-2 shop pair take K seeds from the world bank, play the o209 stack with each
slot forced to each kind (others on fallback) against the opponents, both seats, and pick per key the
kind with the best mean margin (must beat the fallback choice by MARGIN to replace it).
Usage: python o_tools/compile_policy.py [--seeds-per-pair 4] [--workers 12] [--opps c150,v43]
Writes o_tools/policy_table.json and rewrites agent/overlays/o209_policy.py's _O209_TABLE line.
"""
import argparse, collections, json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
OPP = {'c150': 'agent/c150.py', 'v43': 'state/o_dev/public_pull/kaggriculture-v43-recovering-lost-harvests/extracted_main.py',
       'fsv4': 'state/o_dev/public_pull/farming-score-v4-a-better-shop-20260915/extracted_main.py',
       'msf': 'state/o_dev/public_pull/market-smart-farming-kaggriculture-20260915/extracted_main.py'}
KINDS = ('GOOSE', 'COW', 'SHEEP')
MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
AGENT = 'agent/o209_policy.py'
OUT = os.path.join(ROOT, 'o_results', 'policy_rollouts')


def fallback(shops, slot):
    m2 = sum(s in MILK for s in shops[:2]); m3 = sum(s in MILK for s in shops[:3])
    if slot == 'd6': return 'GOOSE' if m2 == 0 else 'COW'
    if slot == 'd8': return 'SHEEP'
    if 'YARN_STORE' in shops[:3]: return 'SHEEP'
    return 'COW' if m3 == 3 else 'GOOSE'


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--seeds-per-pair', type=int, default=4); ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--opps', default='c150,v43'); ap.add_argument('--margin', type=float, default=200); a = ap.parse_args()
    allw = json.load(open(os.path.join(ROOT, 'o_tools', 'world_bank_all.json')))
    pairs = collections.defaultdict(list)
    for s, sh in sorted(allw.items(), key=lambda kv: int(kv[0])):
        if 'YARN_STORE' not in sh[:2] and len(pairs[tuple(sorted(sh[:2]))]) < a.seeds_per_pair:
            pairs[tuple(sorted(sh[:2]))].append(int(s))
    seeds = sorted(x for v in pairs.values() for x in v); seedlist = ','.join(map(str, seeds))
    variants = ['-,-,-'] + [','.join(k if i == j else '-' for j in range(3)) for i in range(3) for k in KINDS]
    os.makedirs(OUT, exist_ok=True)
    jobs = [(v, o) for v in variants for o in a.opps.split(',')]
    for i, (v, o) in enumerate(jobs):
        jf = os.path.join(OUT, f"{v.replace(',', '_')}__{o}.json")
        if os.path.exists(jf):
            continue
        print(f'[{i+1}/{len(jobs)}] force={v} vs {o} ({len(seeds)} seeds x 2)', flush=True)
        subprocess.run([PY, os.path.join(ROOT, 'tools', 'o_arena.py'), os.path.join(ROOT, AGENT), os.path.join(ROOT, OPP[o]),
                        '--seed-list', seedlist, '--workers', str(a.workers), '--json-out', jf],
                       cwd=ROOT, env=dict(os.environ, MPLBACKEND='Agg', KAGG_O209_FORCE=v), capture_output=True, text=True, timeout=14400)
    # aggregate: margin[(variant, opp, seed, seat)] and shops per game
    M = {}; shops_of = {}
    for v, o in jobs:
        for r in json.load(open(os.path.join(OUT, f"{v.replace(',', '_')}__{o}.json")))['results']:
            if r['outcome'] in ('win', 'loss', 'tie'):
                M[(v, o, r['seed'], r['seat'])] = r['margin']; shops_of[r['seed']] = r.get('shops') or []
    table = {'d6': {}, 'd8': {}, 'd10': {}}; report = []
    for si, slot in enumerate(('d6', 'd8', 'd10')):
        keyf = (lambda sh: '|'.join(sorted(sh[:2]))) if slot != 'd10' else (lambda sh: '|'.join(sorted(sh[:3])))
        groups = collections.defaultdict(set)
        for sd in seeds:
            if sd in shops_of: groups[keyf(shops_of[sd])].add(sd)
        for key, sds in sorted(groups.items()):
            fb = fallback(shops_of[next(iter(sds))], slot)
            means = {}; wins = {}
            for k in KINDS:
                v = ','.join(k if j == si else '-' for j in range(3))
                vals = [M[(v, o, sd, seat)] for o in a.opps.split(',') for sd in sds for seat in (0, 1) if (v, o, sd, seat) in M]
                if vals: means[k] = sum(vals) / len(vals); wins[k] = sum(x > 0 for x in vals)
            if not means or fb not in means:
                continue
            # wins decide rating (o203 lesson: higher mean margin but fewer wins is a regression); margin breaks ties
            best = max(means, key=lambda k: (wins[k], means[k]))
            choice = best if best != fb and wins[best] >= wins[fb] + 2 and means[best] >= means[fb] - a.margin else fb
            table[slot][key] = choice
            report.append((slot, key, len(sds), fb, choice, {k: (wins[k], round(means[k])) for k in means}))
    json.dump(table, open(os.path.join(ROOT, 'o_tools', 'policy_table.json'), 'w'), indent=1)
    p = os.path.join(ROOT, 'agent', 'overlays', 'o209_policy.py'); src = open(p, encoding='utf-8').read()
    src = re.sub(r'^_O209_TABLE = .*$', '_O209_TABLE = ' + json.dumps(table, separators=(',', ':')) + '   # compiled by o_tools/compile_policy.py', src, count=1, flags=re.M)
    open(p, 'w', encoding='utf-8').write(src)
    changed = [r for r in report if r[3] != r[4]]
    print(f'table keys: d6 {len(table["d6"])} d8 {len(table["d8"])} d10 {len(table["d10"])} | overrides vs fallback: {len(changed)}')
    for r in changed: print('  ', r)


if __name__ == '__main__':
    main()
