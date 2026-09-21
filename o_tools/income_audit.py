"""Exact income/spend ledger for two agents on pinned proxy worlds (hooks the engine's per-unit market commit).
Usage: python o_tools/income_audit.py --a agent/o227_stealth_drop.py --b agent/p000_planner.py --seeds 7000-7003 [--knobs ...]
Prints per-product revenue/units/avg price for B and A, revenue by 5-day window, and spend by category."""
import argparse, json, os, sys, collections, statistics
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLBACKEND'] = 'Agg'
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
LOG = []


def run(args):
    a_path, b_path, seed, seat_b, shops, knobs = args
    if knobs:
        os.environ['PROXY_KNOBS'] = knobs
    from proxy_eval import load_agent
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    A = load_agent(a_path, 'agA'); B = load_agent(b_path, 'agB')
    original = engine._end_of_day; commit0 = engine._commit_unit
    step_box = [0]

    def pinned(state, env, day):
        original(state, env, day)
        want = shops[:len(state[0].observation.town['unlocked_shops'])]
        if len(want) == len(state[0].observation.town['unlocked_shops']):
            state[0].observation.town['unlocked_shops'][:] = want

    seat_of = {}; pm0 = engine._process_market

    def process_market(state, env):
        seat_of.clear()
        for i, f in enumerate(state[0].observation.farms):
            seat_of[id(f)] = i
        step_box[0] = int(state[0].observation.step)
        return pm0(state, env)

    drop0 = engine._drop_inventories_to_shed; priv_seat = {}

    def drop(private, capacity):
        seat = priv_seat.get(id(private))
        before = {}
        for inv in private['inventories']:
            for item, n in inv.items():
                before[item] = before.get(item, 0) + n
        shed_before = dict(private['shed'])
        drop0(private, capacity)
        for item, n in before.items():
            kept = private['shed'].get(item, 0) - shed_before.get(item, 0)
            if n - kept > 0:
                LOG.append((seat, step_box[0], 'DISCARD', item, n - kept))

    def end_of_day(state, env, day):
        for i, s_ in enumerate(state):
            priv_seat[id(s_.observation.private)] = i
        return pinned(state, env, day)

    def commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = commit0(op, item, price, farm, private, market, shed_capacity)
        if ok:
            LOG.append((seat_of.get(id(farm)), step_box[0], op, item, price))
        return ok
    engine._end_of_day = end_of_day; engine._commit_unit = commit; engine._process_market = process_market; engine._drop_inventories_to_shed = drop
    del LOG[:]
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        env.run([A, B] if seat_b == 1 else [B, A])
    finally:
        engine._end_of_day = original; engine._commit_unit = commit0; engine._process_market = pm0; engine._drop_inventories_to_shed = drop0
    st = env.steps
    rev = collections.defaultdict(lambda: collections.Counter()); units = collections.defaultdict(lambda: collections.Counter())
    spend = collections.defaultdict(lambda: collections.Counter()); win = collections.defaultdict(lambda: collections.Counter())
    for seat, step, op, item, price in LOG:
        if seat is None:
            continue
        if op == 'DISCARD':
            spend[seat]['DISCARD_' + item] += price   # units lost to the 100-unit shed cap at the day-end inventory drop
        elif op == 'SELL':
            rev[seat][item] += price; units[seat][item] += 1; win[seat][(item, min(5, step // 120))] += price
        elif op == 'BUY_PRODUCT':
            spend[seat]['PRODUCT_' + item] += price
        elif op == 'BUY_SEED':
            spend[seat]['SEED_' + item] += price
        elif op == 'BUY_ANIMAL':
            spend[seat]['ANIMAL_' + item] += price
    # money by window (cash at day ends)
    money = {seat: [st[min(len(st) - 1, d * 24 + 23)][0].observation['farms'][seat]['money'] for d in range(30)] for seat in (0, 1)}
    rw = [s.reward for s in st[-1]]
    return dict(seed=seed, seat_b=seat_b, b=rw[seat_b], a=rw[1 - seat_b], rev={s: dict(rev[s]) for s in (0, 1)}, units={s: dict(units[s]) for s in (0, 1)},
                spend={s: dict(spend[s]) for s in (0, 1)}, money=money, win={s: {f"{k[0]}|{k[1]}": v for k, v in win[s].items()} for s in (0, 1)})


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py')
    ap.add_argument('--seeds', default='7000-7003'); ap.add_argument('--knobs', default=''); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--item', default='', help='print per-game revenue/units of this product (B side) with the world shops')
    args = ap.parse_args()
    if ',' in args.seeds:
        seeds = [int(x) for x in args.seeds.split(',')]   # explicit list
    else:
        lo, hi = (args.seeds.split('-') + [args.seeds])[:2]; seeds = list(range(int(lo), int(hi) + 1))
    cache = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    jobs = [(args.a, args.b, s, seat, cache[str(s)], args.knobs) for s in seeds for seat in (0, 1)]
    with ProcessPoolExecutor(args.workers) as ex:
        res = list(ex.map(run, jobs))
    n = len(res)
    print(f"[{args.knobs or 'base'}] B cash mean {statistics.mean(r['b'] for r in res):.0f} | A mean {statistics.mean(r['a'] for r in res):.0f} | n {n}")
    agg = {'B': (collections.Counter(), collections.Counter(), collections.Counter()), 'A': (collections.Counter(), collections.Counter(), collections.Counter())}
    for r in res:
        for tag, seat in (('B', r['seat_b']), ('A', 1 - r['seat_b'])):
            agg[tag][0].update(r['rev'][seat]); agg[tag][1].update(r['units'][seat]); agg[tag][2].update(r['spend'][seat])
    items = sorted(set(agg['B'][0]) | set(agg['A'][0]))
    print('product      B rev   B units  B avg |   A rev   A units  A avg |  diff')
    for it in items:
        br, bu = agg['B'][0][it] / n, agg['B'][1][it] / n; ar, au = agg['A'][0][it] / n, agg['A'][1][it] / n
        print(f"{it:11s} {br:7.0f} {bu:8.1f} {br / max(1e-9, bu):6.0f} | {ar:7.0f} {au:8.1f} {ar / max(1e-9, au):6.0f} | {br - ar:+7.0f}")
    print(f"TOTAL       {sum(agg['B'][0].values()) / n:7.0f}                 | {sum(agg['A'][0].values()) / n:7.0f}                 | {(sum(agg['B'][0].values()) - sum(agg['A'][0].values())) / n:+7.0f}")
    cats = sorted(set(agg['B'][2]) | set(agg['A'][2]))
    print('spend        B       A     diff')
    for c in cats:
        print(f"{c:14s} {agg['B'][2][c] / n:6.0f} {agg['A'][2][c] / n:6.0f} {(agg['B'][2][c] - agg['A'][2][c]) / n:+6.0f}")
    print(f"TOTAL spend    {sum(agg['B'][2].values()) / n:6.0f} {sum(agg['A'][2].values()) / n:6.0f}")
    wagg = {'B': collections.Counter(), 'A': collections.Counter()}
    for r in res:
        for tag, seat in (('B', r['seat_b']), ('A', 1 - r['seat_b'])):
            wagg[tag].update(r['win'][seat])
    print('revenue by 5-day window (B | A):   d0-4    d5-9   d10-14  d15-19  d20-24  d25-29')
    for it in items:
        print(f"  {it:11s} " + ' '.join(f"{wagg['B'][f'{it}|{w}'] / n:6.0f}|{wagg['A'][f'{it}|{w}'] / n:6.0f}" for w in range(6)))
    if args.item:
        for r in res:
            sb = r['seat_b']; sh = cache[str(r['seed'])]
            print(f"  seed {r['seed']} seat {sb}: {args.item} rev {r['rev'][sb].get(args.item, 0):6.0f} units {r['units'][sb].get(args.item, 0):3d} | A rev {r['rev'][1 - sb].get(args.item, 0):6.0f} units {r['units'][1 - sb].get(args.item, 0):3d} | shops {sh}")
    print('cash at day end (B | A):')
    for d in range(0, 30, 3):
        mb = statistics.mean(r['money'][r['seat_b']][d] for r in res); ma = statistics.mean(r['money'][1 - r['seat_b']][d] for r in res)
        print(f"  d{d:2d} {mb:7.0f} | {ma:7.0f} | {mb - ma:+7.0f}")


if __name__ == '__main__':
    main()
