"""Compact wheat-flow audit for planner candidates on pinned proxy worlds.

Counts actual WHEAT seed buys/plants and end-of-day wheat/free-tile state. This is
diagnostic only; it never edits an agent or submission artifact.
"""
import argparse
import importlib.util
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLBACKEND'] = 'Agg'


def load_agent(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return [v for k, v in vars(mod).items() if callable(v) and not k.startswith('__')][-1]


def run(path, opp, seed, seat, shops):
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine

    cand = load_agent(path, f'cand_{seed}_{seat}')
    rival = load_agent(opp, f'opp_{seed}_{seat}')
    original = engine._end_of_day

    def pinned(state, env, day):
        original(state, env, day)
        want = shops[:len(state[0].observation.town['unlocked_shops'])]
        if len(want) == len(state[0].observation.town['unlocked_shops']):
            state[0].observation.town['unlocked_shops'][:] = want

    engine._end_of_day = pinned
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        env.run([cand, rival] if seat == 0 else [rival, cand])
    finally:
        engine._end_of_day = original

    plants = [0] * 30
    buys = [0] * 30
    crop_plants = {c: 0 for c in ('WHEAT', 'STRAWBERRY', 'MELON', 'CARROT', 'TOMATO')}
    sells = {p: 0 for p in ('WHEAT', 'STRAWBERRY', 'MELON', 'CARROT', 'TOMATO', 'MILK', 'WOOL', 'EGG', 'FERTILIZER')}
    crop_ops = {c: {'WATER': 0, 'HARVEST': 0, 'FERTILIZE': 0} for c in crop_plants}
    moves = works = passes = 0
    for k, frame in enumerate(env.steps):
        action = frame[seat].action or {}
        day = min(29, k // 24)
        actor_cmds = [action.get('farmer')] + (action.get('hands') or [])
        obs_now = frame[seat].observation
        farm_now = obs_now['farms'][seat]
        actor_pos = [tuple(farm_now['farmer'])] + [tuple(p) for p in farm_now.get('hands', [])]
        for ai, cmd in enumerate(actor_cmds):
            if not cmd or cmd[0] == 'PASS':
                passes += 1
            elif cmd[0] in ('NORTH', 'SOUTH', 'EAST', 'WEST'):
                moves += 1
            else:
                works += 1
            if cmd and len(cmd) >= 2 and cmd[0] == 'PLANT' and cmd[1] == 'WHEAT':
                plants[day] += 1
            if cmd and len(cmd) >= 2 and cmd[0] == 'PLANT' and cmd[1] in crop_plants:
                crop_plants[cmd[1]] += 1
            if cmd and cmd[0] in ('WATER', 'HARVEST', 'FERTILIZE') and ai < len(actor_pos):
                x, y = actor_pos[ai]
                tile = farm_now['tiles'][y][x]
                if isinstance(tile, dict) and tile.get('crop') in crop_ops:
                    crop_ops[tile['crop']][cmd[0]] += 1
        for order in action.get('market') or []:
            if order and len(order) >= 3 and order[0] == 'BUY_SEED' and order[1] == 'WHEAT':
                buys[day] += int(order[2])
            if order and len(order) >= 3 and order[0] == 'SELL' and order[1] in sells:
                sells[order[1]] += max(0, int(order[2]))

    daily = []
    fed_sum = cared_sum = animal_sum = 0
    for day in range(30):
        k = min(len(env.steps) - 1, day * 24 + 23)
        obs = env.steps[k][seat].observation
        farm = obs['farms'][seat]
        tiles = [t for row in farm['tiles'] for t in row]
        wheat = sum(1 for t in tiles if isinstance(t, dict) and t.get('crop') == 'WHEAT')
        free = sum(1 for t in tiles if t is None)
        seeds = int(obs['private']['seeds'].get('WHEAT', 0))
        animals = [t for t in tiles if isinstance(t, dict) and t.get('animal')]
        fed = sum(1 for t in animals if t.get('fed_today'))
        cared = sum(1 for t in animals if t.get('cared_today'))
        fed_sum += fed; cared_sum += cared; animal_sum += len(animals)
        daily.append((wheat, free, seeds, fed, cared, len(animals)))

    return {
        'reward': env.steps[-1][seat].reward,
        'plants': plants,
        'buys': buys,
        'daily': daily,
        'moves': moves,
        'works': works,
        'passes': passes,
        'fed_sum': fed_sum,
        'cared_sum': cared_sum,
        'animal_sum': animal_sum,
        'crop_plants': crop_plants,
        'sells': sells,
        'crop_ops': crop_ops,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--candidate', default='agent/opp_planner_proxy.py')
    ap.add_argument('--opponent', default='agent/o227_stealth_drop.py')
    ap.add_argument('--seeds', default='7000-7003')
    args = ap.parse_args()
    lo, hi = map(int, args.seeds.split('-'))
    cache = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    rows = []
    for seed in range(lo, hi + 1):
        for seat in (0, 1):
            rows.append(run(args.candidate, args.opponent, seed, seat, cache[str(seed)]))

    print(f"candidate={args.candidate} games={len(rows)} cash_mean={statistics.mean(r['reward'] for r in rows):.0f}")
    print('day plant buy | wheat free seed(end)')
    for day in range(30):
        pl = statistics.mean(r['plants'][day] for r in rows)
        bu = statistics.mean(r['buys'][day] for r in rows)
        wh = statistics.mean(r['daily'][day][0] for r in rows)
        fr = statistics.mean(r['daily'][day][1] for r in rows)
        sd = statistics.mean(r['daily'][day][2] for r in rows)
        if pl or bu or day in (0, 6, 9, 12, 15, 18, 21, 24, 27, 29):
            print(f"d{day:02d} {pl:5.1f} {bu:5.1f} | {wh:5.1f} {fr:5.1f} {sd:5.1f}")
    print(f"TOTAL wheat plants={statistics.mean(sum(r['plants']) for r in rows):.1f} buys={statistics.mean(sum(r['buys']) for r in rows):.1f}")
    mv = statistics.mean(r['moves'] for r in rows)
    wk = statistics.mean(r['works'] for r in rows)
    ps = statistics.mean(r['passes'] for r in rows)
    print(f"ACTIONS move={mv:.0f} work={wk:.0f} pass={ps:.0f} move_share={mv/max(1,mv+wk+ps):.3f}")
    fed = sum(r['fed_sum'] for r in rows); cared = sum(r['cared_sum'] for r in rows); animals = sum(r['animal_sum'] for r in rows)
    print(f"ANIMAL_DAY feed={fed/max(1,animals):.3f} care={cared/max(1,animals):.3f} observations={animals}")
    for key in ('WHEAT', 'STRAWBERRY', 'MELON', 'CARROT', 'TOMATO'):
        water = statistics.mean(r['crop_ops'][key]['WATER'] for r in rows)
        harvest = statistics.mean(r['crop_ops'][key]['HARVEST'] for r in rows)
        fert = statistics.mean(r['crop_ops'][key]['FERTILIZE'] for r in rows)
        print(f"CROP {key:10s} plants={statistics.mean(r['crop_plants'][key] for r in rows):6.1f} water={water:6.1f} harvest={harvest:6.1f} fert={fert:6.1f} sell_orders={statistics.mean(r['sells'][key] for r in rows):7.1f}")
    for key in ('MILK', 'WOOL', 'EGG', 'FERTILIZER'):
        print(f"PRODUCT {key:10s} sell_orders={statistics.mean(r['sells'][key] for r in rows):7.1f}")


if __name__ == '__main__':
    main()
