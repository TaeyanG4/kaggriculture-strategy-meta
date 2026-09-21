"""Throughput audit of recorded games: replay each live episode locally with BOTH players' recorded actions (deterministic,
pinned shops) and instrument the engine to count, per player and day, what the labour actually did: unit actions by type
(attempted / executed / failed no-ops / idle PASS), moves, harvest units, atomic PLANT blocks, day-end farm state (hands, owned,
empty, weeds, plants, animals, unwatered, unfed, ready-unharvested units), losses (plants -> weed, decayed plants, escapes) and the
cash ledger from the market (sell revenue and units per product, seed/animal/feed/fertilizer/hire/land spend).
Usage: python o_tools/throughput_audit.py --dir o_replays/live_frozen/live_b19 --us Taeyang [--episodes id,id] [--workers 8] [--out o_results/throughput_live_b19.json]
Aggregate afterwards with --report <json> [--groups o_results/live_pool_groups.json]."""
import argparse, collections, copy, glob, json, os, statistics as st, sys
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
MOVES = ('NORTH', 'SOUTH', 'EAST', 'WEST')
TILE_OPS = ('PLANT', 'WATER', 'HARVEST', 'FERTILIZE', 'DIG', 'BUILD_COOP', 'BUILD_PASTURE', 'FEED', 'COLLECT_FERTILIZER', 'CARE')
INV_OPS = ('DROP', 'PICKUP', 'PLACE')


def new_day():
    return dict(att=collections.Counter(), ok=collections.Counter(), harvest_units=collections.Counter(), plant_blocked=0,
                sell_rev=collections.Counter(), sell_units=collections.Counter(), spend=collections.Counter(), end={}, loss=collections.Counter(),
                hour_idle=[0] * 24, hour_units=[0] * 24, hour_feed=[0] * 24, hour_harv=[0] * 24, buys=collections.Counter())


def play(args):
    path, us = args
    os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as eng
    r = json.load(open(path, encoding='utf-8')); names = r['info']['TeamNames']; steps = r['steps']
    shops = list(steps[-1][0]['observation']['town']['unlocked_shops'])
    stats = {0: {}, 1: {}}; owner = {}; cur = {'day': 0, 'hour': 0}

    def frozen(i):
        def ag(observation, configuration=None):
            k = int(observation['step']) + 1
            return copy.deepcopy(steps[k][i]['action']) if k < len(steps) else {}
        return ag

    def D(farm):
        return stats[owner[id(farm)]].setdefault(cur['day'], new_day())
    o_unit, o_commit, o_hire, o_land, o_eod, o_decay = eng._apply_unit_action, eng._commit_unit, eng._do_hire, eng._do_buy_land, eng._end_of_day, eng._decay_plants

    def unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
        d = D(farm); op = action[0] if isinstance(action, list) and action else 'NONE'
        d['att'][op] += 1; h = cur['hour']; d['hour_units'][h] += 1
        if op in ('PASS', 'NONE'):
            d['hour_idle'][h] += 1
        pos = eng._farmer_position(farm, idx)
        if pos is None:
            return o_unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
        inv = eng._farmer_inventory(private, idx); inv0 = dict(inv); shed0 = sum(private['shed'].values())
        tile0 = json.dumps(farm['tiles'][pos[1]][pos[0]], sort_keys=True, default=str) if op in TILE_OPS else None
        pos0 = tuple(pos)
        o_unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
        if op in MOVES:
            ok = tuple(eng._farmer_position(farm, idx)) != pos0
        elif op in TILE_OPS:
            ok = json.dumps(farm['tiles'][pos0[1]][pos0[0]], sort_keys=True, default=str) != tile0 or dict(inv) != inv0
        elif op in INV_OPS:
            ok = dict(inv) != inv0 or sum(private['shed'].values()) != shed0
        else:
            ok = False
        if ok:
            d['ok'][op] += 1
            if op == 'FEED':
                d['hour_feed'][h] += 1
            if op == 'HARVEST':
                d['hour_harv'][h] += 1
                for k, v in inv.items():
                    if v > inv0.get(k, 0):
                        d['harvest_units'][k] += v - inv0.get(k, 0)

    def commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = o_commit(op, item, price, farm, private, market, shed_capacity)
        if ok:
            d = D(farm)
            if op == 'SELL':
                d['sell_rev'][item] += price; d['sell_units'][item] += 1
            elif op == 'BUY_PRODUCT':
                d['spend']['feed_wheat' if item == 'WHEAT' else 'fertilizer_buy'] += price
            elif op == 'BUY_SEED':
                d['spend']['seeds'] += price
            elif op == 'BUY_ANIMAL':
                d['spend']['animals'] += price; d['buys'][item + '@' + str(cur['hour'])] += 1
        return ok

    def hire(farm, private, board_size, mult=eng.FARM_HAND_COST_MULT):
        m0 = farm['money']; o_hire(farm, private, board_size, mult); D(farm)['spend']['hire'] += m0 - farm['money']

    def land(farm, board_size):
        m0 = farm['money']; o_land(farm, board_size); D(farm)['spend']['land'] += m0 - farm['money']

    def decay(farm, step):
        before = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('kind') == 'PLANT')
        o_decay(farm, step)
        after = sum(1 for row in farm['tiles'] for t in row if isinstance(t, dict) and t.get('kind') == 'PLANT')
        if before > after:
            D(farm)['loss']['decayed_plants'] += before - after

    def eod(state, env, day):
        farms = state[0].observation.farms
        for p, farm in enumerate(farms):
            d = stats[p].setdefault(day, new_day()); tiles = [t for row in farm['tiles'] for t in row]
            plants = [t for t in tiles if isinstance(t, dict) and t.get('kind') == 'PLANT']; animals = [t for t in tiles if isinstance(t, dict) and 'animal' in t]
            d['end'] = dict(hands=len(farm['hands']), owned=sum(1 for t in tiles if t != 'LOCKED'), empty=sum(1 for t in tiles if t is None),
                            weeds=sum(1 for t in tiles if isinstance(t, dict) and t.get('kind') == 'WEED'), plants=len(plants), animals=len(animals),
                            unwatered=sum(1 for t in plants if not t['watered_today']), unfed=sum(1 for t in animals if not t['fed_today']),
                            ready_units=sum(t.get('yield_units', 0) for t in plants) + sum(t.get('yield_units', 0) for t in animals),
                            money=farm['money'], shed=sum(state[p].observation.private['shed'].values()), shed_wheat=state[p].observation.private['shed'].get('WHEAT', 0),
                            seeds=dict(state[p].observation.private.get('seeds', {})), market={k: state[0].observation.market['inventory'].get(k, 0) for k in ('MILK', 'WOOL', 'FERTILIZER', 'WHEAT', 'STRAWBERRY', 'EGG')},
                            shops=list(state[0].observation.town['unlocked_shops']),
                            crops=dict(collections.Counter(t['crop'] for t in plants)), herd=dict(collections.Counter(t['animal'] for t in animals)))
            d['loss']['will_weed'] = sum(1 for t in plants if not t['watered_today'] and t['consecutive_unwatered'] >= 1)
            d['loss']['will_escape'] = sum(1 for t in animals if not t['fed_today'] and t['consecutive_unfed'] >= 1)
        o_eod(state, env, day)
        town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want

    def pre(env, step):
        cur['day'] = step // 24; cur['hour'] = step % 24
        for i, f in enumerate(env.state[0].observation.farms):
            owner[id(f)] = i
        for i in (0, 1):   # atomic PLANT blocks: requested PLANTs that the interpreter turns into PASS
            a = steps[step + 1][i].get('action') if step + 1 < len(steps) else None
            if isinstance(a, dict):
                seeds = env.state[i].observation.private.get('seeds', {}); dem = collections.Counter()
                for u in [a.get('farmer') or ['PASS']] + list(a.get('hands') or []):
                    if isinstance(u, list) and len(u) >= 2 and u[0] == 'PLANT':
                        dem[u[1]] += 1
                stats[i].setdefault(cur['day'], new_day())['plant_blocked'] += sum(n for c, n in dem.items() if n > seeds.get(c, 0))
    eng._apply_unit_action, eng._commit_unit, eng._do_hire, eng._do_buy_land, eng._end_of_day, eng._decay_plants = unit, commit, hire, land, eod, decay
    try:
        env = make('kaggriculture', configuration={'seed': int(r['info'].get('seed') or 0) % (2 ** 31)}, debug=False)
        fastgame.play(env, [frozen(0), frozen(1)], deep=True, pre_hook=pre)
    finally:
        eng._apply_unit_action, eng._commit_unit, eng._do_hire, eng._do_buy_land, eng._end_of_day, eng._decay_plants = o_unit, o_commit, o_hire, o_land, o_eod, o_decay
    out = dict(episode=os.path.basename(path).split('-')[0], names=names, us=names.index(us) if us in names else None,
               final=[float(env.state[i].reward or 0) for i in (0, 1)], recorded=[float(steps[-1][i].get('reward') or 0) for i in (0, 1)], days={})
    for p in (0, 1):
        out['days'][p] = {d: {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in x.items()} for d, x in sorted(stats[p].items())}
    return out


def agg(games, side):
    """side(g) -> player index to aggregate (or None to skip). Returns per-day metric lists and per-game totals."""
    per_day = collections.defaultdict(lambda: collections.defaultdict(list)); totals = collections.defaultdict(list)
    for g in games:
        p = side(g)
        if p is None:
            continue
        days = g['days'][str(p)]
        T = collections.Counter()
        for d, x in days.items():
            d = int(d); att = sum(x['att'].values()); mv = sum(x['ok'].get(m, 0) for m in MOVES); idle = x['att'].get('PASS', 0) + x['att'].get('NONE', 0)
            ok = sum(x['ok'].values()); fail = att - ok - idle; hu = sum(x['harvest_units'].values())
            e = x['end'] or {}
            row = dict(units=e.get('hands', 0) + 1, att=att, ok=ok, idle=idle, fail=fail, moves=mv, harv=x['ok'].get('HARVEST', 0), harv_units=hu,
                       plant=x['ok'].get('PLANT', 0), water=x['ok'].get('WATER', 0), feed=x['ok'].get('FEED', 0), drop=x['ok'].get('DROP', 0) + x['ok'].get('PLACE', 0), pickup=x['ok'].get('PICKUP', 0),
                       plant_blocked=x['plant_blocked'], empty=e.get('empty', 0), owned=e.get('owned', 0), weeds=e.get('weeds', 0), unwatered=e.get('unwatered', 0), unfed=e.get('unfed', 0),
                       ready=e.get('ready_units', 0), rev=sum(x['sell_rev'].values()), spend=sum(x['spend'].values()))
            for k, v in row.items():
                per_day[d][k].append(v)
            for k in ('rev', 'spend', 'moves', 'harv', 'harv_units', 'fail', 'idle', 'att', 'ok', 'plant_blocked'):
                T[k] += row[k]
            T['unit_days'] += row['units']; T['decayed'] += x['loss'].get('decayed_plants', 0); T['weeded'] += x['loss'].get('will_weed', 0); T['escaped'] += x['loss'].get('will_escape', 0)
            for k, v in x['spend'].items():
                T['spend_' + k] += v
            for k, v in x['sell_rev'].items():
                T['rev_' + k] += v
            for k, v in x['sell_units'].items():
                T['units_' + k] += v
        T['final'] = g['final'][p]
        for k, v in T.items():
            totals[k].append(v)
    return per_day, totals


def report(path, groups_path):
    games = json.load(open(path, encoding='utf-8')); groups = json.load(open(groups_path, encoding='utf-8')) if groups_path else {}
    sides = [('OURS (all games)', lambda g: g['us']), ('RIVAL (all games)', lambda g: 1 - g['us'])]
    for gname in sorted(set(groups.values())):
        eps = {e for e, gg in groups.items() if gg == gname}
        sides.append((f'RIVAL {gname[:40]}', (lambda eps: lambda g: (1 - g['us']) if g['episode'] in eps else None)(eps)))
        sides.append((f'OURS vs {gname[:2].strip()}', (lambda eps: lambda g: g['us'] if g['episode'] in eps else None)(eps)))
    keys = ['final', 'rev', 'spend', 'spend_seeds', 'spend_animals', 'spend_feed_wheat', 'spend_fertilizer_buy', 'spend_hire', 'spend_land', 'unit_days', 'att', 'ok', 'idle', 'fail', 'moves', 'harv', 'harv_units', 'plant_blocked', 'decayed', 'weeded', 'escaped']
    print('side                                        n | ' + ' '.join(f'{k[:9]:>9s}' for k in keys))
    for name, side in sides:
        per_day, T = agg(games, side)
        n = len(T.get('final', []))
        if not n:
            continue
        print(f"{name:43s} {n:3d} | " + ' '.join(f"{st.mean(T.get(k, [0])):9.0f}" for k in keys))
    print('\nper-day profile (OURS all vs RIVAL all): units, actions ok/att, idle, fail, moves, harvest units, empty tiles, unwatered, unfed, ready-unharvested')
    pd_o, _ = agg(games, lambda g: g['us']); pd_r, _ = agg(games, lambda g: 1 - g['us'])
    print('day | units  ok/att   idle fail moves harvU | empty unwat unfed ready || RIVAL units  ok/att   idle fail moves harvU | empty unwat unfed ready')
    f = lambda x, k: st.mean(x[k]) if x.get(k) else 0
    for d in sorted(pd_o):
        o, r_ = pd_o[d], pd_r.get(d, {})
        print(f"{d:3d} | {f(o,'units'):5.1f} {f(o,'ok'):5.0f}/{f(o,'att'):<5.0f} {f(o,'idle'):4.0f} {f(o,'fail'):4.0f} {f(o,'moves'):5.0f} {f(o,'harv_units'):5.0f} | {f(o,'empty'):5.1f} {f(o,'unwatered'):5.1f} {f(o,'unfed'):5.1f} {f(o,'ready'):5.0f} ||"
              f" {f(r_,'units'):5.1f} {f(r_,'ok'):5.0f}/{f(r_,'att'):<5.0f} {f(r_,'idle'):4.0f} {f(r_,'fail'):4.0f} {f(r_,'moves'):5.0f} {f(r_,'harv_units'):5.0f} | {f(r_,'empty'):5.1f} {f(r_,'unwatered'):5.1f} {f(r_,'unfed'):5.1f} {f(r_,'ready'):5.0f}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dir'); ap.add_argument('--us', default='Taeyang'); ap.add_argument('--episodes', default=''); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--out', default=''); ap.add_argument('--report', default=''); ap.add_argument('--groups', default='')
    a = ap.parse_args()
    if a.report:
        return report(a.report, a.groups)
    files = sorted(glob.glob(os.path.join(ROOT, a.dir, '*-replay.json')))
    if a.episodes:
        keep = set(a.episodes.split(',')); files = [f for f in files if os.path.basename(f).split('-')[0] in keep]
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(play, [(f, a.us) for f in files]))
    out = a.out or os.path.join(ROOT, 'o_results', f"throughput_{os.path.basename(a.dir.rstrip('/'))}.json")
    json.dump(res, open(out, 'w'), indent=0)
    bad = [g for g in res if any(abs(x - y) > 1 for x, y in zip(g['final'], g['recorded']))]
    print(f'{len(res)} games -> {out}; reproduction mismatches (final cash != recorded): {len(bad)}')


if __name__ == '__main__':
    main()
