"""Fixed-world evaluation harness for the planner proxy: runs agent A vs agent B on given seeds with the SHOP
SEQUENCE PINNED per seed (the engine draws shops from an RNG shared with weed spawns, so different agents see
different worlds on the same seed; pinning makes A/B comparisons exact). Sequences are cached in
o_results/proxy/shop_seq.json (recorded once from a c150-vs-c150 game per seed).
Usage: python o_tools/proxy_eval.py --a agent/c150.py --b agent/opp_planner_proxy.py --seeds 7000-7007 [--flags nostock] [--workers 8]
Prints B's cash mean/median/min/max, A's mean, B wins, and per-bucket means."""
import argparse, json, os, sys, importlib.util, statistics, collections
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLBACKEND'] = 'Agg'
MILK = {'PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP'}


def bucket(sh):
    return 'yarn' if 'YARN_STORE' in sh[:2] else 'milk%d' % min(3, sum(s in MILK for s in sh[:3]))


def load_agent(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path)); m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m; spec.loader.exec_module(m)
    return [v for k, v in vars(m).items() if callable(v) and not k.startswith('__')][-1]


def run_game(args):
    a_path, b_path, seed, seat_b, shops, flags = args
    if flags:
        os.environ['PROXY_FLAGS'] = flags
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    A = load_agent(a_path, 'agA'); B = load_agent(b_path, 'agB')
    original = engine._end_of_day
    if shops:
        def pinned(state, env, day):
            original(state, env, day)
            want = shops[:len(state[0].observation.town['unlocked_shops'])]
            if len(want) == len(state[0].observation.town['unlocked_shops']):
                state[0].observation.town['unlocked_shops'][:] = want
        engine._end_of_day = pinned
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        agents = [A, B] if seat_b == 1 else [B, A]
        env.run(agents)
    finally:
        engine._end_of_day = original
    rw = [s.reward for s in env.steps[-1]]; final_shops = list(env.steps[-1][0].observation['town']['unlocked_shops'])
    b = rw[seat_b]; a = rw[1 - seat_b]
    return dict(seed=seed, seat_b=seat_b, a=a, b=b, shops=final_shops)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--a', default='agent/c150.py'); ap.add_argument('--b', default='agent/opp_planner_proxy.py')
    ap.add_argument('--seeds', default='7000-7007'); ap.add_argument('--flags', default=''); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--label', default='')
    args = ap.parse_args()
    lo, hi = (args.seeds.split('-') + [args.seeds])[:2]; seeds = list(range(int(lo), int(hi) + 1))
    cache_path = os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json'); os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    missing = [s for s in seeds if str(s) not in cache]
    if missing:
        with ProcessPoolExecutor(args.workers) as ex:
            for r in ex.map(run_game, [(args.a, args.a, s, 1, None, '') for s in missing]):
                cache[str(r['seed'])] = r['shops']
        json.dump(cache, open(cache_path, 'w'), indent=0)
    jobs = [(args.a, args.b, s, seat, cache[str(s)], args.flags) for s in seeds for seat in (0, 1)]
    with ProcessPoolExecutor(args.workers) as ex:
        res = list(ex.map(run_game, jobs))
    b = [r['b'] for r in res]; a = [r['a'] for r in res]
    byb = collections.defaultdict(list)
    for r in res:
        byb[bucket(cache[str(r['seed'])])].append(r['b'])
    print(f"[{args.label or args.flags or 'base'}] B cash mean {statistics.mean(b):.0f} median {statistics.median(b):.0f} min {min(b):.0f} max {max(b):.0f} | A mean {statistics.mean(a):.0f} | B wins {sum(r['b'] > r['a'] for r in res)}/{len(res)} | by bucket " + ' '.join(f"{k}:{statistics.mean(v)/1000:.0f}k(n{len(v)})" for k, v in sorted(byb.items())))
    out = os.path.join(ROOT, 'o_results', 'proxy', f"eval_{(args.label or args.flags or 'base').replace(',', '_')}.json")
    json.dump(res, open(out, 'w'))


if __name__ == '__main__':
    main()
