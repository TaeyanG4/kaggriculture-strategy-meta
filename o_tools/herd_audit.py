"""Herd audit for a planner candidate on pinned proxy worlds: animals placed, fed/cared rate by day, herd
layout compactness and wool/milk/egg income. Usage:
  python o_tools/herd_audit.py --b agent/p000_planner.py --seeds 7000-7003 [--knobs sw_herd_block=1] [--layout 12]"""
import argparse, json, os, sys, collections, statistics
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLBACKEND'] = 'Agg'
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
SHED = [(4, 4), (5, 4), (4, 5), (5, 5)]


def run(args):
    a_path, b_path, seed, seat_b, shops, knobs, layout_days = args
    if knobs:
        os.environ['PROXY_KNOBS'] = knobs
    from proxy_eval import load_agent
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    A = load_agent(a_path, 'agA'); B = load_agent(b_path, 'agB')
    original = engine._end_of_day

    def pinned(state, env, day):
        original(state, env, day)
        want = shops[:len(state[0].observation.town['unlocked_shops'])]
        if len(want) == len(state[0].observation.town['unlocked_shops']):
            state[0].observation.town['unlocked_shops'][:] = want
    engine._end_of_day = pinned
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        env.run([A, B] if seat_b == 1 else [B, A])
    finally:
        engine._end_of_day = original
    st = env.steps
    days = []
    for d in range(30):
        k = min(len(st) - 1, d * 24 + 23)
        f = st[k][0].observation['farms'][seat_b]
        an = [(x, y, t) for y, row in enumerate(f['tiles']) for x, t in enumerate(row) if isinstance(t, dict) and t.get('animal')]
        fed = sum(1 for _, _, t in an if t.get('fed_today')); cared = sum(1 for _, _, t in an if t.get('cared_today'))
        pos = [(x, y) for x, y, _ in an]
        spread = statistics.mean(min(abs(x - s[0]) + abs(y - s[1]) for s in SHED) for x, y in pos) if pos else 0
        days.append(dict(n=len(an), fed=fed, cared=cared, spread=spread, money=f['money']))
    sold = collections.Counter(); acts = collections.Counter(); uncollected = 0
    for k in range(1, len(st)):
        a = st[k][seat_b].action or {}
        for o in a.get('market') or []:
            if o and o[0] == 'SELL' and len(o) >= 3:
                sold[o[1]] += int(o[2])
        for c in [a.get('farmer')] + (a.get('hands') or []):
            if c and c[0] in ('COLLECT_FERTILIZER', 'FERTILIZE', 'FEED', 'CARE', 'HARVEST', 'WATER', 'PASS'):
                acts[c[0]] += 1
        if k % 24 == 23:
            f = st[k][0].observation['farms'][seat_b]
            uncollected += sum(1 for row in f['tiles'] for t in row if isinstance(t, dict) and t.get('animal') and t.get('fertilizer_available'))
    acts['uncollected_fert'] = uncollected
    layouts = {}
    sym = {'COW': 'C', 'SHEEP': 'S', 'GOOSE': 'G'}
    csym = {'WHEAT': 'w', 'MELON': 'm', 'STRAWBERRY': 's', 'CARROT': 'c', 'TOMATO': 't'}
    for d in layout_days:
        f = st[min(len(st) - 1, d * 24 + 23)][0].observation['farms'][seat_b]; rows = []
        for y, row in enumerate(f['tiles']):
            line = ''
            for x, t in enumerate(row):
                if (x, y) in SHED: line += '#'
                elif t == 'LOCKED': line += '?'
                elif t is None: line += '.'
                elif t.get('animal'): line += sym[t['animal']]
                elif t.get('kind') in ('PASTURE', 'COOP'): line += 'p'
                elif t.get('kind') == 'WEED': line += 'x'
                else: line += csym.get(t.get('crop'), '?')
            rows.append(line)
        layouts[d] = rows
    rw = [s.reward for s in st[-1]]
    return dict(seed=seed, seat_b=seat_b, b=rw[seat_b], a=rw[1 - seat_b], days=days, sold=dict(sold), layouts=layouts, acts=dict(acts))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py')
    ap.add_argument('--seeds', default='7000-7003'); ap.add_argument('--knobs', default=''); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--layout', default=''); ap.add_argument('--seats', default='0,1')
    args = ap.parse_args()
    lo, hi = (args.seeds.split('-') + [args.seeds])[:2]; seeds = list(range(int(lo), int(hi) + 1))
    cache = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    ldays = [int(v) for v in args.layout.split(',') if v]
    seats = [int(s) for s in args.seats.split(',')]
    jobs = [(args.a, args.b, s, seat, cache[str(s)], args.knobs, ldays) for s in seeds for seat in seats]
    with ProcessPoolExecutor(args.workers) as ex:
        res = list(ex.map(run, jobs))
    n = len(res)
    print(f"[{args.knobs or 'base'}] B cash mean {statistics.mean(r['b'] for r in res):.0f} | A mean {statistics.mean(r['a'] for r in res):.0f} | n {n}")
    print('day  animals  fed%  cared%  spread  money')
    for d in range(30):
        an = sum(r['days'][d]['n'] for r in res); fed = sum(r['days'][d]['fed'] for r in res); cared = sum(r['days'][d]['cared'] for r in res)
        sp = statistics.mean(r['days'][d]['spread'] for r in res); money = statistics.mean(r['days'][d]['money'] for r in res)
        print(f"d{d:2d}  {an / n:5.1f}  {100 * fed / max(1, an):5.1f}  {100 * cared / max(1, an):5.1f}  {sp:5.2f}  {money:7.0f}")
    tot_an = sum(r['days'][d]['n'] for r in res for d in range(6, 29)); tot_fed = sum(r['days'][d]['fed'] for r in res for d in range(6, 29))
    tot_cared = sum(r['days'][d]['cared'] for r in res for d in range(6, 29))
    print(f"d6-28 fed {100 * tot_fed / max(1, tot_an):.1f}% cared {100 * tot_cared / max(1, tot_an):.1f}%  animal-days/game {tot_an / n:.0f}")
    sold = collections.Counter()
    for r in res:
        sold.update(r['sold'])
    print('units sold/game: ' + ' '.join(f"{k}:{v / n:.0f}" for k, v in sorted(sold.items())))
    acts = collections.Counter()
    for r in res:
        acts.update(r['acts'])
    print('actions/game: ' + ' '.join(f"{k}:{v / n:.0f}" for k, v in sorted(acts.items())))
    for r in res:
        for d, rows in r['layouts'].items():
            print(f"seed {r['seed']} seat {r['seat_b']} day {d}: cash {r['b']:.0f}")
            for line in rows:
                print('   ' + line)


if __name__ == '__main__':
    main()
