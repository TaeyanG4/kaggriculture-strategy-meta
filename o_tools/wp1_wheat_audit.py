"""WP1 wheat-cycle audit on pinned worlds.

Reports the age-2 fertilize -> age-3 harvest transition, wheat harvest age/yield,
and wheat SELL timing. Diagnostic only; never edits an agent artifact.
"""
import argparse
import collections
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

    cand = load_agent(path, f'wp1_cand_{seed}_{seat}')
    rival = load_agent(opp, f'wp1_opp_{seed}_{seat}')
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

    fert_age = collections.Counter()
    harvest_age = collections.Counter()
    harvest_yield = collections.Counter()
    harvest_age_yield = collections.Counter()
    sell_hour_qty = collections.Counter()
    sell_hour_orders = collections.Counter()
    ferted = set()
    fert_harvest = {}
    water_age3 = 0
    water_age3_ferted = 0

    for k, frame in enumerate(env.steps):
        action = frame[seat].action or {}
        # env.steps[k].action was chosen from the preceding observation. This
        # matters for one-shot crops because HARVEST removes the tile before
        # frame k's observation is recorded.
        pre = env.steps[k - 1][seat] if k > 0 else frame[seat]
        obs = pre.observation
        farm = obs['farms'][seat]
        positions = [tuple(farm['farmer'])] + [tuple(p) for p in farm.get('hands', [])]
        cmds = [action.get('farmer')] + (action.get('hands') or [])
        step = int(obs.get('step', max(0, k - 1)))
        day = min(29, step // 24)
        hour = step % 24

        for ai, cmd in enumerate(cmds):
            if not cmd or ai >= len(positions):
                continue
            x, y = positions[ai]
            tile = farm['tiles'][y][x]
            if not isinstance(tile, dict) or tile.get('crop') != 'WHEAT':
                continue
            planted = int(tile.get('planted_day', day))
            age = day - planted
            key = (x, y, planted)
            if cmd[0] == 'FERTILIZE':
                fert_age[age] += 1
                if age == 2:
                    ferted.add(key)
            elif cmd[0] == 'WATER' and age == 3:
                water_age3 += 1
                if key in ferted:
                    water_age3_ferted += 1
            elif cmd[0] == 'HARVEST':
                yu = int(tile.get('yield_units', 0) or 0)
                harvest_age[age] += 1
                harvest_yield[yu] += 1
                harvest_age_yield[(age, yu)] += 1
                if key in ferted and key not in fert_harvest:
                    fert_harvest[key] = (age, yu)

        for order in action.get('market') or []:
            if order and len(order) >= 3 and order[0] == 'SELL' and order[1] == 'WHEAT':
                q = max(0, int(order[2]))
                sell_hour_qty[hour] += q
                sell_hour_orders[hour] += 1

    transitioned3 = sum(1 for age, _ in fert_harvest.values() if age == 3)
    transitioned4 = sum(1 for age, _ in fert_harvest.values() if age == 4)
    return {
        'reward': env.steps[-1][seat].reward,
        'fert_age': dict(fert_age),
        'harvest_age': dict(harvest_age),
        'harvest_yield': dict(harvest_yield),
        'harvest_age_yield': {f'{a}:{y}': n for (a, y), n in harvest_age_yield.items()},
        'fert2': len(ferted),
        'fert2_h3': transitioned3,
        'fert2_h4': transitioned4,
        'fert2_other': len(ferted) - len(fert_harvest),
        'water_age3': water_age3,
        'water_age3_ferted': water_age3_ferted,
        'sell_hour_qty': dict(sell_hour_qty),
        'sell_hour_orders': dict(sell_hour_orders),
    }


def merge_counter(rows, key):
    out = collections.Counter()
    for r in rows:
        for k, v in r[key].items():
            out[k] += v
    return out


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

    f2 = sum(r['fert2'] for r in rows)
    h3 = sum(r['fert2_h3'] for r in rows)
    h4 = sum(r['fert2_h4'] for r in rows)
    other = sum(r['fert2_other'] for r in rows)
    print(f"candidate={args.candidate} games={len(rows)} cash_mean={statistics.mean(r['reward'] for r in rows):.0f}")
    print(f"FERT2 instances={f2} -> harvest age3={h3} ({h3/max(1,f2):.1%}) age4={h4} ({h4/max(1,f2):.1%}) no/later={other} ({other/max(1,f2):.1%})")
    print('FERT age:', sorted(merge_counter(rows, 'fert_age').items(), key=lambda x: int(x[0])))
    print('HARVEST age:', sorted(merge_counter(rows, 'harvest_age').items(), key=lambda x: int(x[0])))
    print('HARVEST yield:', sorted(merge_counter(rows, 'harvest_yield').items(), key=lambda x: int(x[0])))
    print('HARVEST age:yield:', sorted(merge_counter(rows, 'harvest_age_yield').items()))
    wa3 = sum(r['water_age3'] for r in rows); wa3f = sum(r['water_age3_ferted'] for r in rows)
    print(f"WATER age3={wa3} fertilized_instances={wa3f}")
    qty = merge_counter(rows, 'sell_hour_qty'); orders = merge_counter(rows, 'sell_hour_orders')
    print('WHEAT sell hour qty:', ' '.join(f"h{int(h):02d}:{qty[h]}" for h in sorted(qty, key=int)))
    print('WHEAT sell hour orders:', ' '.join(f"h{int(h):02d}:{orders[h]}" for h in sorted(orders, key=int)))


if __name__ == '__main__':
    main()
