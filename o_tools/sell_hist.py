"""Actual per-unit sales of both players by (product, day, hour) with the realised price, recorded by hooking the engine's
_commit_unit during pinned games (our planner vs the tape, both seats). Prints, per product, the tape's hour-of-day sales
profile vs ours, the tape's daily dump windows, and a first-order estimate of the timing slack: for each product and day,
units we sold in the 6 hours after the tape's main dump hour and the price drop the dump caused.
Usage: python o_tools/sell_hist.py [--seeds 7000-7015] [--workers 16] [--knobs ...] [--a agent/o227_stealth_drop.py]
Output: o_results/proxy/sell_hist_<label>.json + table."""
import argparse, collections, json, os, statistics, sys
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')


def play(args):
    seed, seat_b, knobs, a_path, b_path = args
    os.environ['PROXY_KNOBS'] = knobs; os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    from proxy_eval import load_agent
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    shops = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))[str(seed)]
    A = load_agent(a_path, 'agA'); B = load_agent(b_path, 'agB')
    orig_eod = engine._end_of_day; orig_commit = engine._commit_unit
    cur = {'step': 0}; sales = []   # (step, who, item, price) who: 'B' ours, 'A' tape

    def pinned(state, env, day):
        orig_eod(state, env, day); town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want
    farms_ref = {}

    def commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = orig_commit(op, item, price, farm, private, market, shed_capacity)
        if ok and op == 'SELL':
            who = 'B' if farm is farms_ref.get('B') else 'A'
            sales.append((cur['step'], who, item, int(price)))
        return ok
    engine._end_of_day = pinned; engine._commit_unit = commit

    def pre_hook(env, step):
        cur['step'] = step
        fs = env.state[0].observation['farms']; farms_ref['B'] = fs[seat_b]
    env = make('kaggriculture', configuration={'seed': seed}, debug=False)
    fastgame.play(env, [A, B] if seat_b == 1 else [B, A], deep=True, pre_hook=pre_hook)
    engine._end_of_day = orig_eod; engine._commit_unit = orig_commit
    return seed, seat_b, sales


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--seeds', default='7000-7015'); ap.add_argument('--workers', type=int, default=16); ap.add_argument('--knobs', default='')
    ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py'); ap.add_argument('--label', default='base')
    a = ap.parse_args()
    lo, hi = a.seeds.split('-'); seeds = list(range(int(lo), int(hi) + 1))
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(play, [(s, seat, a.knobs, a.a, a.b) for s in seeds for seat in (0, 1)], chunksize=2))
    n = len(res)
    json.dump([dict(seed=r[0], seat_b=r[1], sales=r[2]) for r in res], open(os.path.join(ROOT, 'o_results', 'proxy', f'sell_hist_{a.label}.json'), 'w'))
    # hour-of-day profile per product (units per game)
    prof = {w: {p: [0.0] * 24 for p in PRODUCTS} for w in 'AB'}; rev = {w: collections.Counter() for w in 'AB'}; units = {w: collections.Counter() for w in 'AB'}
    for _, _, sales in res:
        for step, who, item, price in sales:
            prof[who][item][step % 24] += 1.0 / n; rev[who][item] += price / n; units[who][item] += 1.0 / n
    print(f'{n} games. Units sold per game by hour of day (tape A / ours B), with mean price:')
    for p in PRODUCTS:
        if units['A'][p] + units['B'][p] < 5:
            continue
        top_a = sorted(range(24), key=lambda h: -prof['A'][p][h])[:4]
        print(f"{p:11s} A {units['A'][p]:5.0f}u @{rev['A'][p] / max(1e-9, units['A'][p]):4.0f} peak hours {top_a} | B {units['B'][p]:5.0f}u @{rev['B'][p] / max(1e-9, units['B'][p]):4.0f}")
        print('   A: ' + ' '.join(f"{prof['A'][p][h]:4.1f}" for h in range(24)))
        print('   B: ' + ' '.join(f"{prof['B'][p][h]:4.1f}" for h in range(24)))
    # timing slack: per product, per game-day, the tape's dump (first hour where it sells >= 25% of its daily units) and our units sold in the 6 hours after it,
    # priced against the pre-dump price (mean price of the tape's first units that day)
    print('\nTiming slack estimate per product: our units sold within 6h after the tape dump start, x (pre-dump price - our realised price)')
    for p in PRODUCTS:
        tot_units = 0.0; tot_slack = 0.0; days_with_dump = 0
        for _, _, sales in res:
            by_day = collections.defaultdict(lambda: {'A': [], 'B': []})
            for step, who, item, price in sales:
                if item == p:
                    by_day[step // 24][who].append((step % 24, price))
            for d, s in by_day.items():
                a_s = sorted(s['A']); b_s = sorted(s['B'])
                if len(a_s) < 4:
                    continue
                # dump start = first hour by which >= 25% of the tape's daily units are sold
                cum = 0; start = None
                for h, pr in a_s:
                    cum += 1
                    if cum >= 0.25 * len(a_s):
                        start = h; break
                pre_price = statistics.mean(pr for h, pr in a_s[:max(1, len(a_s) // 4)])
                after = [(h, pr) for h, pr in b_s if start <= h <= start + 6]
                if after:
                    days_with_dump += 1; tot_units += len(after); tot_slack += sum(max(0, pre_price - pr) for h, pr in after)
        if days_with_dump:
            print(f"  {p:11s} game-days with a tape dump {days_with_dump / n:4.1f}/game | our units in the 6h after {tot_units / n:5.1f}/game | slack {tot_slack / n:6.0f} $/game")


if __name__ == '__main__':
    main()
