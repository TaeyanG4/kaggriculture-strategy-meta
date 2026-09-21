"""Strawberry production audit on pinned worlds: per production event (plant ages 9/11/13/15) whether the tile was
watered, fertilized, or already at the 4-unit hold cap, plus plants lost to weeds and decay.
Usage: python o_tools/straw_audit.py --b agent/p000_planner.py --seeds 7000-7003 [--knobs ...] [--a agent/o227_stealth_drop.py]"""
import argparse, json, os, sys, collections
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLBACKEND'] = 'Agg'
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))


def run(args):
    a_path, b_path, seed, seat_b, shops, knobs = args
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
    c = collections.Counter(); planted_days = collections.Counter()
    seen = {}
    for d in range(30):
        k = d * 24 + 23
        f = st[k][0].observation['farms'][seat_b]
        for y, row in enumerate(f['tiles']):
            for x, t in enumerate(row):
                key = (x, y)
                if isinstance(t, dict) and t.get('crop') == 'STRAWBERRY':
                    pd = t['planted_day']
                    if seen.get(key) != pd:
                        seen[key] = pd; c['plants'] += 1; planted_days[pd] += 1
                    age = d - pd
                    if age in (9, 11, 13, 15):
                        c['prod'] += 1
                        w = t.get('watered_today'); fz = t.get('fertilized_until_day', -1) >= d
                        c['prod_watered'] += bool(w); c['prod_fert'] += bool(w and fz)
                        if t.get('yield_units', 0) >= 3:
                            c['prod_capped'] += 1   # room for <2 units: part of this production is lost
                        if t.get('yield_units', 0) >= 4:
                            c['prod_full'] += 1
                    if age > 16:
                        c['tile_days_after_last'] += 1
                elif key in seen and not (isinstance(t, dict) and t.get('crop') == 'STRAWBERRY'):
                    if isinstance(t, dict) and t.get('kind') == 'WEED':
                        c['to_weed'] += 1
                    del seen[key]
    rw = [s.reward for s in st[-1]]
    return dict(seed=seed, seat_b=seat_b, b=rw[seat_b], c=dict(c), planted=dict(planted_days))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py')
    ap.add_argument('--seeds', default='7000-7003'); ap.add_argument('--knobs', default=''); ap.add_argument('--workers', type=int, default=8); ap.add_argument('--seats', default='0,1')
    args = ap.parse_args()
    lo, hi = (args.seeds.split('-') + [args.seeds])[:2]; seeds = list(range(int(lo), int(hi) + 1))
    cache = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    seats = [int(s) for s in args.seats.split(',')]
    jobs = [(args.a, args.b, s, seat, cache[str(s)], args.knobs) for s in seeds for seat in seats]
    with ProcessPoolExecutor(args.workers) as ex:
        res = list(ex.map(run, jobs))
    n = len(res); c = collections.Counter(); pdays = collections.Counter()
    for r in res:
        c.update(r['c']); pdays.update({int(k): v for k, v in r['planted'].items()})
    print(f"[{args.knobs or 'base'}] {args.b} n={n} cash {sum(r['b'] for r in res) / n:.0f}")
    print(f"plants/game {c['plants'] / n:.1f}  productions/game {c['prod'] / n:.1f} (per plant {c['prod'] / max(1, c['plants']):.2f})  watered {100 * c['prod_watered'] / max(1, c['prod']):.0f}%  fertilized {100 * c['prod_fert'] / max(1, c['prod']):.0f}%  capped(yield>=3) {100 * c['prod_capped'] / max(1, c['prod']):.0f}%  full(4) {100 * c['prod_full'] / max(1, c['prod']):.0f}%  to_weed/game {c['to_weed'] / n:.1f}  tile-days after last prod/game {c['tile_days_after_last'] / n:.1f}")
    print('planted by day: ' + ' '.join(f"d{d}:{v / n:.1f}" for d, v in sorted(pdays.items())))


if __name__ == '__main__':
    main()
