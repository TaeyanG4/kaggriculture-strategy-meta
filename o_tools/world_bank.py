"""World bank: classify seeds by the shop world they produce and keep N seeds per bucket.
Shops are drawn from seed + both farms' empty tiles; same-lineage pairs share the early layout, so the
first four shops are stable across our opponents. Games are run only to day 12 (4 shops).
Usage: python o_tools/world_bank.py --start 7000 --count 1500 --per-bucket 36 --workers 12
Output: o_tools/world_bank.json {bucket: [seeds]}, plus o_tools/world_bank_all.json {seed: shops[:4]}
"""
import argparse, json, os, sys, importlib.util
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
BUCKETS = ('goose', 'one_milk', 'two_milk', 'yarn')          # exclusive, by the first two shops
TAGS = ('carrot', 'tomato')                                   # overlapping, by the first four shops


def classify(shops):
    f2 = shops[:2]
    if 'YARN_STORE' in f2:
        b = 'yarn'
    else:
        m = sum(s in MILK for s in f2)
        b = ('goose', 'one_milk', 'two_milk')[m]
    tags = []
    if shops[:4].count('PET_CAFE') >= 2: tags.append('carrot')
    if sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET') for s in shops[:4]) >= 3: tags.append('tomato')
    return b, tags


def shops_for(seed):
    os.environ['MPLBACKEND'] = 'Agg'
    from kaggle_environments import make
    spec = importlib.util.spec_from_file_location('c150', os.path.join(ROOT, 'agent', 'c150.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=False)
    env.reset()
    a = m.agent
    while env.state[0].observation['step'] < 289:          # day 12 -> 4 shops known
        shared = dict(env.state[0].observation)
        acts = [a({**shared, **dict(env.state[i].observation)}, None) for i in range(2)]
        env.step(acts)
    return seed, list(env.state[0].observation['town']['unlocked_shops'][:4])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, default=7000); ap.add_argument('--count', type=int, default=1500)
    ap.add_argument('--per-bucket', type=int, default=36); ap.add_argument('--workers', type=int, default=12)
    a = ap.parse_args()
    allp = os.path.join(ROOT, 'o_tools', 'world_bank_all.json')
    known = json.load(open(allp)) if os.path.exists(allp) else {}
    todo = [s for s in range(a.start, a.start + a.count) if str(s) not in known]
    with ProcessPoolExecutor(a.workers) as ex:
        for i, (seed, shops) in enumerate(ex.map(shops_for, todo, chunksize=4)):
            known[str(seed)] = shops
            if i % 50 == 0:
                print(f'{i}/{len(todo)}', flush=True); json.dump(known, open(allp, 'w'), indent=0)
    json.dump(known, open(allp, 'w'), indent=0)
    bank = {b: [] for b in BUCKETS}; bank.update({t: [] for t in TAGS})
    for seed, shops in sorted(known.items(), key=lambda kv: int(kv[0])):
        b, tags = classify(shops)
        if len(bank[b]) < a.per_bucket: bank[b].append(int(seed))
        for t in tags:
            if len(bank[t]) < a.per_bucket: bank[t].append(int(seed))
    json.dump(bank, open(os.path.join(ROOT, 'o_tools', 'world_bank.json'), 'w'), indent=1)
    print({k: len(v) for k, v in bank.items()}, 'from', len(known), 'seeds')


if __name__ == '__main__':
    main()
