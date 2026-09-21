"""p002 smoke-game ledger tracer (kept for the record; see reports/o-p002-smoke-audit-2026-09-18.ko.md).
Deterministic re-execution of the two p002 smoke games (same seed / seat / pinned shops / opponent) for BOTH the frozen candidate and the
parent, with engine hooks: per-day herd, cash, feed stock, purchases by hour, per-tile animal events (place / first feed / first harvest), milk
sales and the full cash ledger. Not a new evaluation: reproduces the exact smoke games (finals must equal the smoke printout)."""
import os, sys, json, collections, io, contextlib
ROOT = 'H:/dev/kaggle-data/kaggriculture-strategy-meta'; os.chdir(ROOT); sys.path.insert(0, 'o_tools'); os.environ['MPLBACKEND'] = 'Agg'
os.environ.pop('PROXY_KNOBS', None)
from proxy_eval import load_agent
import fastgame
from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as eng


def run(agent_path, seed, seat, tag):
    B = load_agent(agent_path, 'cand_' + tag); A = load_agent('state/o_dev/v46_public.py', 'opp_' + tag)
    shops = json.load(open('o_results/proxy/shop_seq.json'))[str(seed)]
    o_eod, o_unit, o_commit, o_hire, o_land = eng._end_of_day, eng._apply_unit_action, eng._commit_unit, eng._do_hire, eng._do_buy_land
    cur = {'day': 0, 'hour': 0}; owner = {}
    L = dict(days={}, events=[], tiles={})   # tiles: (x,y) -> dict(kind, placed, first_feed, first_harvest, feeds, harvests, units)

    def D(p, d=None):
        return L['days'].setdefault(d if d is not None else cur['day'], {}).setdefault(p, dict(rev=collections.Counter(), units=collections.Counter(), spend=collections.Counter(), buys=[], hires=0, feeds=0, end={}))

    def pinned(state, env, day):
        farms = state[0].observation.farms
        for p, farm in enumerate(farms):
            tiles = [t for row in farm['tiles'] for t in row]; animals = [t for t in tiles if isinstance(t, dict) and 'animal' in t]
            priv = state[p].observation.private
            D(p, day)['end'] = dict(money=farm['money'], herd=dict(collections.Counter(t['animal'] for t in animals)), unfed=sum(1 for t in animals if not t['fed_today']),
                                    shed_wheat=priv['shed'].get('WHEAT', 0), shed_milk=priv['shed'].get('MILK', 0), shed_cow=priv['shed'].get('COW', 0), shed_total=sum(priv['shed'].values()),
                                    milk_inv=state[0].observation.market['inventory'].get('MILK', 0), milk_price=state[0].observation.market['prices'].get('MILK', 0),
                                    seeds=dict(priv.get('seeds', {})), hands=len(farm['hands']), plants=sum(1 for t in tiles if isinstance(t, dict) and t.get('kind') == 'PLANT'), empty=sum(1 for t in tiles if t is None))
        o_eod(state, env, day); town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want

    def unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
        p = owner[id(farm)]; op = action[0] if isinstance(action, list) and action else 'NONE'
        pos = eng._farmer_position(farm, idx)
        before = json.dumps(farm['tiles'][pos[1]][pos[0]], sort_keys=True, default=str) if pos is not None and op in ('PLACE', 'FEED', 'HARVEST', 'BUILD_PASTURE', 'COLLECT_FERTILIZER') else None
        inv = eng._farmer_inventory(private, idx) if pos is not None else {}; inv0 = dict(inv)
        o_unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
        if pos is None or p != seat:
            return
        after = json.dumps(farm['tiles'][pos[1]][pos[0]], sort_keys=True, default=str) if before is not None else None
        key = (pos[0], pos[1]); t = farm['tiles'][pos[1]][pos[0]]
        if op == 'PLACE' and after != before and isinstance(t, dict) and 'animal' in t:
            L['tiles'][key] = dict(kind=t['animal'], placed=(day, cur['hour']), first_feed=None, first_harvest=None, feeds=0, harvests=0, units=0)
            L['events'].append((day, cur['hour'], 'PLACE', t['animal'], key))
        if op == 'FEED' and after != before and key in L['tiles']:
            rec = L['tiles'][key]; rec['feeds'] += 1; D(p)['feeds'] += 1
            if rec['first_feed'] is None:
                rec['first_feed'] = (day, cur['hour'])
        if op == 'HARVEST' and key in L['tiles'] and dict(inv) != inv0:
            rec = L['tiles'][key]; got = sum(v - inv0.get(k, 0) for k, v in inv.items() if v > inv0.get(k, 0)); rec['harvests'] += 1; rec['units'] += got
            if rec['first_harvest'] is None:
                rec['first_harvest'] = (day, cur['hour'])

    def commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = o_commit(op, item, price, farm, private, market, shed_capacity); p = owner[id(farm)]
        if ok:
            d = D(p)
            if op == 'SELL':
                d['rev'][item] += price; d['units'][item] += 1
            else:
                cat = {'BUY_PRODUCT': 'feed_wheat' if item == 'WHEAT' else 'fertilizer_buy', 'BUY_SEED': 'seeds', 'BUY_ANIMAL': 'animals'}[op]; d['spend'][cat] += price
                if op != 'BUY_PRODUCT':
                    d['buys'].append((cur['hour'], op[4:], item, price))
        elif op == 'BUY_ANIMAL' and p == seat:
            L['events'].append((cur['day'], cur['hour'], 'BUY_ANIMAL_FAILED', item, dict(money=farm['money'], shed=sum(private['shed'].values()))))
        return ok

    def hire(farm, private, board_size, mult=eng.FARM_HAND_COST_MULT):
        m0 = farm['money']; o_hire(farm, private, board_size, mult); d = D(owner[id(farm)]); d['spend']['hire'] += m0 - farm['money']; d['hires'] += 1 if farm['money'] != m0 else 0

    def land(farm, board_size):
        m0 = farm['money']; o_land(farm, board_size); D(owner[id(farm)])['spend']['land'] += m0 - farm['money']

    def pre(env, step):
        cur['day'] = step // 24; cur['hour'] = step % 24
        for i, f in enumerate(env.state[0].observation.farms):
            owner[id(f)] = i
    eng._end_of_day, eng._apply_unit_action, eng._commit_unit, eng._do_hire, eng._do_buy_land = pinned, unit, commit, hire, land
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        with contextlib.redirect_stdout(io.StringIO()):
            fastgame.play(env, [B, A] if seat == 0 else [A, B], deep=True, pre_hook=pre)
    finally:
        eng._end_of_day, eng._apply_unit_action, eng._commit_unit, eng._do_hire, eng._do_buy_land = o_eod, o_unit, o_commit, o_hire, o_land
    mod = sys.modules['cand_' + tag]
    L['final'] = [float(s.reward) for s in env.state]; L['telemetry'] = {k: v for k, v in dict(getattr(mod, '_TEL', {})).items()}
    return L


def show(child, parent, seat, title):
    print(f'===== {title}: finals child {child["final"]} parent {parent["final"]}  (seat {seat})')
    print('child telemetry:', {k: v for k, v in child['telemetry'].items() if k != 'p002_log'}); print('child p002_log:', child['telemetry'].get('p002_log'))
    ev = [e for e in child['events'] if e[2] != 'PLACE' or e[3] == 'COW']
    print('child events (PLACE COW / failed buys):', ev[:20])
    print('parent COW placements:', [e for e in parent['events'] if e[2] == 'PLACE' and e[3] == 'COW'])
    # tiles: cows placed after the purchase
    for lab, L in (('child', child), ('parent', parent)):
        cows = sorted((v for v in L['tiles'].values() if v['kind'] == 'COW'), key=lambda v: v['placed'])
        print(f"{lab} cow tiles: " + ' | '.join(f"placed d{v['placed'][0]}h{v['placed'][1]} feed1 {v['first_feed']} harv1 {v['first_harvest']} feeds {v['feeds']} harv {v['harvests']}/{v['units']}u" for v in cows))
    print('day | cows c/p | animals c/p | money c/p | shed wheat c/p | unfed c/p | milk sold c/p ($) | milk price | buys child | buys parent | hires c/p | seeds$ c/p | plants c/p')
    for d in range(0, 30):
        c = child['days'].get(d, {}).get(seat); p = parent['days'].get(d, {}).get(seat)
        if not c or not p:
            continue
        ce, pe = c['end'], p['end']
        if not ce or not pe:
            continue
        cb = ','.join(f"h{h}{k[0]}{i[:3]}" for h, k, i, pr in c['buys'] if k != 'SEED') ; pb = ','.join(f"h{h}{k[0]}{i[:3]}" for h, k, i, pr in p['buys'] if k != 'SEED')
        print(f"d{d:2d} | {ce['herd'].get('COW', 0):2d}/{pe['herd'].get('COW', 0):<2d} | {sum(ce['herd'].values()):2d}/{sum(pe['herd'].values()):<2d} | {ce['money']:6.0f}/{pe['money']:<6.0f} | {ce['shed_wheat']:3d}/{pe['shed_wheat']:<3d} | {ce['unfed']}/{pe['unfed']} | {c['units'].get('MILK', 0):3d}/{p['units'].get('MILK', 0):<3d} ({c['rev'].get('MILK', 0):5.0f}/{p['rev'].get('MILK', 0):<5.0f}) | {ce['milk_price']:4.0f} | {cb:22s} | {pb:22s} | {c['hires']:2d}/{p['hires']:<2d} | {c['spend'].get('seeds', 0):4.0f}/{p['spend'].get('seeds', 0):<4.0f} | {ce['plants']:2d}/{pe['plants']:<2d}")
    tot = lambda L, f: sum(sum(x[seat][f].values()) for x in L['days'].values() if seat in x)
    keys_r = sorted(set(k for L in (child, parent) for x in L['days'].values() if seat in x for k in x[seat]['rev']))
    keys_s = sorted(set(k for L in (child, parent) for x in L['days'].values() if seat in x for k in x[seat]['spend']))
    sumk = lambda L, f, k: sum(x[seat][f].get(k, 0) for x in L['days'].values() if seat in x)
    print('ledger delta (child - parent): revenue ' + ' '.join(f"{k[:5]} {sumk(child,'rev',k)-sumk(parent,'rev',k):+6.0f} ({sumk(child,'units',k)-sumk(parent,'units',k):+3.0f}u)" for k in keys_r))
    print('                              spend   ' + ' '.join(f"{k} {sumk(child,'spend',k)-sumk(parent,'spend',k):+6.0f}" for k in keys_s))
    d_rev = tot(child, 'rev') - tot(parent, 'rev'); d_sp = tot(child, 'spend') - tot(parent, 'spend'); d_fin = child['final'][seat] - parent['final'][seat]
    print(f"own final delta {d_fin:+.0f} = revenue {d_rev:+.0f} - spend {d_sp:+.0f} -> residual {d_fin - (d_rev - d_sp):+.0f}; rival final delta {child['final'][1-seat]-parent['final'][1-seat]:+.0f}; margin delta {d_fin - (child['final'][1-seat]-parent['final'][1-seat]):+.0f}")
    opp_keys = sorted(set(k for L in (child, parent) for x in L['days'].values() if (1-seat) in x for k in x[1-seat]['rev']))
    sumo = lambda L, k: sum(x[1-seat]['rev'].get(k, 0) for x in L['days'].values() if (1-seat) in x)
    print('rival revenue delta by product: ' + ' '.join(f"{k[:5]} {sumo(child,k)-sumo(parent,k):+6.0f}" for k in opp_keys))
    print()


for seed, seat in ((7000, 0), (7001, 1)):
    child = run('agent/p002_cow1.py', seed, seat, f'c{seed}'); parent = run('state/o_dev/p000_base19.py', seed, seat, f'p{seed}')
    show(child, parent, seat, f'seed {seed} seat {seat} vs V46')
