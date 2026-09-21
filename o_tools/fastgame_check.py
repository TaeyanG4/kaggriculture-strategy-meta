"""Bit-identity check of o_tools/fastgame.play vs env.run on pinned worlds (rewards + per-day cash of both seats) and a timing comparison.
Usage: python o_tools/fastgame_check.py --seeds 7000,7001 --seats 0,1"""
import argparse, json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLBACKEND'] = 'Agg'
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
from proxy_eval import load_agent
import fastgame


def one(seed, seat_b, shops, fast):
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    A = load_agent('agent/o227_stealth_drop.py', 'agA'); B = load_agent('agent/p000_planner.py', 'agB')
    orig = engine._end_of_day

    def pinned(state, env, day):
        orig(state, env, day)
        want = shops[:len(state[0].observation.town['unlocked_shops'])]
        if len(want) == len(state[0].observation.town['unlocked_shops']):
            state[0].observation.town['unlocked_shops'][:] = want
    engine._end_of_day = pinned
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        agents = [A, B] if seat_b == 1 else [B, A]
        t = time.perf_counter()
        money = {0: [], 1: []}
        if fast == 2:
            fastgame.play(env, agents, deep=True, day_hook=lambda e, d: [money[s].append(e.state[0].observation['farms'][s]['money']) for s in (0, 1)])
        elif fast:
            fastgame.play(env, agents)
        else:
            env.run(agents)
        dt = time.perf_counter() - t
    finally:
        engine._end_of_day = orig
    rw = [s.reward for s in env.state]
    if fast == 2:
        return rw, [money[s][:30] for s in (0, 1)], dt
    return rw, [fastgame.money_by_day(env, s) for s in (0, 1)], dt


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--seeds', default='7000,7001'); ap.add_argument('--seats', default='0,1')
    a = ap.parse_args(); os.chdir(ROOT)
    cache = json.load(open('o_results/proxy/shop_seq.json'))
    ok = True; ts = []
    for seed in [int(x) for x in a.seeds.split(',')]:
        for seat in [int(x) for x in a.seats.split(',')]:
            r1, m1, t1 = one(seed, seat, cache[str(seed)], False)
            r2, m2, t2 = one(seed, seat, cache[str(seed)], True)
            r3, m3, t3 = one(seed, seat, cache[str(seed)], 2)
            same = (r1 == r2 and m1 == m2); same3 = (r1 == r3 and m1 == m3)
            ok &= same and same3; ts.append((t1, t2, t3))
            print(f"seed {seed} seat {seat}: run {r1} {t1:.1f}s | fast {r2} {t2:.1f}s {'IDENTICAL' if same else 'DIFF'} | deep {r3} {t3:.1f}s {'IDENTICAL' if same3 else 'DIFF'}")
    print('ALL IDENTICAL' if ok else 'MISMATCH', '| mean run %.1fs fast %.1fs deep %.1fs' % (sum(t[0] for t in ts) / len(ts), sum(t[1] for t in ts) / len(ts), sum(t[2] for t in ts) / len(ts)))


if __name__ == '__main__':
    main()
