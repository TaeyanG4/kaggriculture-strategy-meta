"""Shadow value of cash: inject +X into our seat's money at (day, hour) and measure the final own cash and paired margin deltas
against the uninjected game, over the pinned selection worlds (both seats). A multiplier >> 1 marks a binding cash constraint
(the money brings a land/animal/seed purchase forward); ~1 means the cash just sits.
Usage: python o_tools/cash_shadow.py --points 0:2,1:2,2:2,...,9:2 --amount 100 [--seeds 7000-7015] [--workers 16] [--knobs ...]
Output: one line per point: day hour amount | own delta (se) | margin delta (se) | multiplier | worlds better/worse."""
import argparse, json, os, statistics, sys
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))


def play(args):
    seed, seat_b, inject_step, amount, knobs, a_path, b_path = args
    os.environ['PROXY_KNOBS'] = knobs; os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    from proxy_eval import load_agent
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    shops = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))[str(seed)]
    A = load_agent(a_path, 'agA'); B = load_agent(b_path, 'agB')
    orig = engine._end_of_day

    def pinned(state, env, day):
        orig(state, env, day); town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want
    engine._end_of_day = pinned

    def pre_hook(env, step):
        if step == inject_step:
            env.state[0].observation['farms'][seat_b]['money'] += amount   # synthetic cash (dict access: Struct attributes are stale copies), visible to the agent this step
    env = make('kaggriculture', configuration={'seed': seed}, debug=False)
    fastgame.play(env, [A, B] if seat_b == 1 else [B, A], deep=True, pre_hook=pre_hook if inject_step >= 0 else None)
    engine._end_of_day = orig
    return seed, seat_b, float(env.state[seat_b].reward or 0), float(env.state[1 - seat_b].reward or 0)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--points', default='0:2,1:2,2:2,3:2,4:2,5:2,6:2,7:2,8:2,9:2'); ap.add_argument('--amount', type=float, default=100)
    ap.add_argument('--seeds', default='7000-7015'); ap.add_argument('--workers', type=int, default=16); ap.add_argument('--knobs', default='')
    ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py')
    a = ap.parse_args()
    lo, hi = a.seeds.split('-'); seeds = list(range(int(lo), int(hi) + 1))
    points = [(int(p.split(':')[0]), int(p.split(':')[1])) for p in a.points.split(',')]
    jobs = [(s, seat, -1, 0.0, a.knobs, a.a, a.b) for s in seeds for seat in (0, 1)]
    for d, h in points:
        jobs += [(s, seat, d * 24 + h, a.amount, a.knobs, a.a, a.b) for s in seeds for seat in (0, 1)]
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(play, jobs, chunksize=2))
    n = len(seeds) * 2
    base = {(r[0], r[1]): (r[2], r[3]) for r in res[:n]}
    print(f"cash shadow value (+{a.amount:.0f} at day:hour), {n} games, base own {statistics.mean(v[0] for v in base.values()):.0f}")
    print('day hour | own delta (se) mult | margin delta (se) mult | better/worse (>500)')
    for i, (d, h) in enumerate(points):
        chunk = res[n * (i + 1):n * (i + 2)]
        do = [r[2] - base[(r[0], r[1])][0] for r in chunk]; dm = [(r[2] - r[3]) - (base[(r[0], r[1])][0] - base[(r[0], r[1])][1]) for r in chunk]
        se = lambda v: statistics.stdev(v) / len(v) ** 0.5 if len(v) > 1 else 0
        print(f"d{d:2d} h{h:2d} | {statistics.mean(do):+7.0f} ({se(do):4.0f}) x{statistics.mean(do) / a.amount:4.1f} | {statistics.mean(dm):+7.0f} ({se(dm):4.0f}) x{statistics.mean(dm) / a.amount:4.1f} | {sum(x > 500 for x in do)}/{sum(x < -500 for x in do)}")


if __name__ == '__main__':
    main()
