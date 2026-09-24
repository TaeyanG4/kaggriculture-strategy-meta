"""Fixed-world evaluation harness for the planner proxy: runs agent A vs agent B on given seeds with the SHOP
SEQUENCE PINNED per seed (the engine draws shops from an RNG shared with weed spawns, so different agents see
different worlds on the same seed; pinning makes A/B comparisons exact). Sequences are cached in
o_results/proxy/shop_seq.json (recorded once from a c150-vs-c150 game per seed).
Usage: python o_tools/proxy_eval.py --a agent/c150.py --b agent/opp_planner_proxy.py --seeds 7000-7007 [--flags nostock] [--workers 8]
Prints B's cash mean/median/min/max, A's mean, B wins, and per-bucket means.
Oracle diagnostics (o401): PROXY_ENGINE_CFG='{"farmHandCostMult": 0}' merges into the engine configuration; PROXY_ENGINE_PATCH=path applies
that file's apply(engine) in every worker (both enter the cache key only when set)."""
import argparse, json, os, sys, importlib.util, statistics, collections, hashlib
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


_SHA = {}


def file_sha(path):
    if path not in _SHA:
        _SHA[path] = hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]
    return _SHA[path]


def game_key(a_path, b_path, seed, seat_b, shops, flags):
    """Content-addressed cache key: both agent files, knobs/flags, engine file, pinned shops, seed, seat."""
    import kaggle_environments.envs.kaggriculture.kaggriculture as eng_mod
    parts = [file_sha(os.path.abspath(a_path)), file_sha(os.path.abspath(b_path)), os.environ.get('PROXY_KNOBS', ''), flags or os.environ.get('PROXY_FLAGS', ''),
             file_sha(eng_mod.__file__), str(seed), str(seat_b), json.dumps(shops)]
    for var in ('PROXY_ENGINE_CFG', 'PROXY_ENGINE_PATCH'):   # o401 oracles: extra engine configuration / engine patch file (key unchanged when unset)
        if os.environ.get(var):
            parts.append(var + '=' + (file_sha(os.environ[var]) if var == 'PROXY_ENGINE_PATCH' else os.environ[var]))
    return hashlib.sha256('|'.join(parts).encode()).hexdigest()


def run_game(args):
    a_path, b_path, seed, seat_b, shops, flags = args
    if flags:
        os.environ['PROXY_FLAGS'] = flags
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    key = game_key(a_path, b_path, seed, seat_b, shops, flags) if shops and not os.environ.get('PROXY_NOCACHE') else None
    cpath = os.path.join(ROOT, 'o_results', 'proxy', 'cache', key[:2], key + '.json') if key else None
    if cpath and os.path.exists(cpath):
        try:
            r = json.load(open(cpath)); r['cached'] = True
            return r
        except Exception:
            pass
    A = load_agent(a_path, 'agA'); B = load_agent(b_path, 'agB')
    if os.environ.get('PROXY_ENGINE_PATCH'):   # o401: apply(engine) from the given file, e.g. state/o401/engine_patch.py (TELEPORT command)
        spec = importlib.util.spec_from_file_location('proxy_engine_patch', os.path.abspath(os.environ['PROXY_ENGINE_PATCH'])); pm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pm)
        try:
            pm.apply(engine, seat_b=seat_b)   # patches that need to know B's seat (o401 perfect-sales oracle)
        except TypeError:
            pm.apply(engine)
    original = engine._end_of_day
    if shops:
        def pinned(state, env, day):
            original(state, env, day)
            want = shops[:len(state[0].observation.town['unlocked_shops'])]
            if len(want) == len(state[0].observation.town['unlocked_shops']):
                state[0].observation.town['unlocked_shops'][:] = want
        engine._end_of_day = pinned
    try:
        cfg = {'seed': seed}
        if os.environ.get('PROXY_ENGINE_CFG'):   # o401: e.g. {"farmHandCostMult": 0} (free labour oracle)
            cfg.update(json.loads(os.environ['PROXY_ENGINE_CFG']))
        env = make('kaggriculture', configuration=cfg, debug=False)
        agents = [A, B] if seat_b == 1 else [B, A]
        if os.environ.get('PROXY_SLOW'):
            env.run(agents)
        else:
            sys.path.insert(0, os.path.join(ROOT, 'o_tools')); import fastgame
            fastgame.play(env, agents, deep=True)   # bit-identical to env.run (o_tools/fastgame_check.py), ~3.7x faster
    finally:
        engine._end_of_day = original
    rw = [s.reward for s in env.state]; final_shops = list(env.state[0].observation['town']['unlocked_shops'])
    b = rw[seat_b]; a = rw[1 - seat_b]
    out = dict(seed=seed, seat_b=seat_b, a=a, b=b, shops=final_shops)
    if cpath:
        os.makedirs(os.path.dirname(cpath), exist_ok=True)
        json.dump(out, open(cpath, 'w'))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--a', default='agent/c150.py'); ap.add_argument('--b', default='agent/opp_planner_proxy.py')
    ap.add_argument('--seeds', default='7000-7007'); ap.add_argument('--flags', default=''); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--label', default=''); ap.add_argument('--seats', default='0,1'); ap.add_argument('--seed-list', default='')
    args = ap.parse_args()
    lo, hi = (args.seeds.split('-') + [args.seeds])[:2]; seeds = [int(x) for x in args.seed_list.split(',')] if args.seed_list else list(range(int(lo), int(hi) + 1))
    cache_path = os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json'); os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    missing = [s for s in seeds if str(s) not in cache]
    if missing:
        with ProcessPoolExecutor(args.workers) as ex:
            for r in ex.map(run_game, [(args.a, args.a, s, 1, None, '') for s in missing]):
                cache[str(r['seed'])] = r['shops']
        json.dump(cache, open(cache_path, 'w'), indent=0)
    jobs = [(args.a, args.b, s, seat, cache[str(s)], args.flags) for s in seeds for seat in [int(x) for x in args.seats.split(',')]]
    with ProcessPoolExecutor(args.workers) as ex:
        res = list(ex.map(run_game, jobs))
    hits = sum(1 for r in res if r.get('cached'))
    for r in res:
        r.pop('cached', None)
    b = [r['b'] for r in res]; a = [r['a'] for r in res]
    byb = collections.defaultdict(list)
    for r in res:
        byb[bucket(cache[str(r['seed'])])].append(r['b'])
    print(f"[{args.label or args.flags or 'base'}] B cash mean {statistics.mean(b):.0f} median {statistics.median(b):.0f} min {min(b):.0f} max {max(b):.0f} | A mean {statistics.mean(a):.0f} | B wins {sum(r['b'] > r['a'] for r in res)}/{len(res)} | cache {hits}/{len(res)} | by bucket " + ' '.join(f"{k}:{statistics.mean(v)/1000:.0f}k(n{len(v)})" for k, v in sorted(byb.items())))
    out = os.path.join(ROOT, 'o_results', 'proxy', f"eval_{(args.label or args.flags or 'base').replace(',', '_')}.json")
    json.dump(res, open(out, 'w'))


if __name__ == '__main__':
    main()
