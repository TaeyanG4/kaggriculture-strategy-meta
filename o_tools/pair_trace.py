"""Same-game, same-date economic trace of a LIVE pair (our agent file vs an executing opponent file) on pinned worlds: per player and
day - end-of-day state (cash, herd, crops, empty tiles, hands, quadrants, shed, seeds, milk/berry/wheat market inventory), sales per
product (units, $) with the hour-level records for the small markets, spend by category, harvest units per crop, unit actions
(executed / idle), hires and land; plus the opponent's exported telemetry at the end (V4x report counters = its branch triggers).
Development analysis tool (reuses fastgame + the throughput_audit hooks); results o_results/trace/<label>.json.
Usage: python o_tools/pair_trace.py --label b19_v46 --b state/o_dev/p000_base19.py --a state/o_dev/v46_public.py --seeds 7000-7031 --workers 12"""
import argparse, collections, json, os, sys, io, contextlib
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
MOVES = ('NORTH', 'SOUTH', 'EAST', 'WEST')
HOURLY = ('MILK', 'STRAWBERRY', 'WOOL', 'MELON', 'WHEAT', 'FERTILIZER', 'TOMATO', 'CARROT', 'EGG')


def new_day():
    return dict(rev=collections.Counter(), units=collections.Counter(), sales=[], spend=collections.Counter(), buys=[], harvest=collections.Counter(),
                ok=collections.Counter(), idle=0, att=0, hires=0, end={})


def play(job):
    b_path, a_path, seed, seat_b, shops, knobs = job
    os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    if knobs:
        os.environ['PROXY_KNOBS'] = knobs
    else:
        os.environ.pop('PROXY_KNOBS', None)
    from proxy_eval import load_agent
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as eng
    B = load_agent(b_path, 'agB'); A = load_agent(a_path, 'agA')
    stats = {0: {}, 1: {}}; owner = {}; cur = {'day': 0, 'hour': 0}
    o = dict(unit=eng._apply_unit_action, commit=eng._commit_unit, hire=eng._do_hire, land=eng._do_buy_land, eod=eng._end_of_day)

    def D(farm):
        return stats[owner[id(farm)]].setdefault(cur['day'], new_day())

    def unit(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
        d = D(farm); op = action[0] if isinstance(action, list) and action else 'NONE'; d['att'] += 1
        if op in ('PASS', 'NONE'):
            d['idle'] += 1
        pos = eng._farmer_position(farm, idx)
        inv = eng._farmer_inventory(private, idx) if pos is not None else {}; inv0 = dict(inv)
        tile0 = json.dumps(farm['tiles'][pos[1]][pos[0]], sort_keys=True, default=str) if pos is not None and op not in MOVES and op not in ('PASS', 'NONE') else None
        pos0 = tuple(pos) if pos is not None else None
        o['unit'](farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)
        if pos0 is None:
            return
        if op in MOVES:
            ok = tuple(eng._farmer_position(farm, idx)) != pos0
        elif op in ('PASS', 'NONE'):
            ok = False
        else:
            ok = json.dumps(farm['tiles'][pos0[1]][pos0[0]], sort_keys=True, default=str) != tile0 or dict(inv) != inv0
        if ok:
            d['ok'][op] += 1
            if op == 'HARVEST':
                for k, v in inv.items():
                    if v > inv0.get(k, 0):
                        d['harvest'][k] += v - inv0.get(k, 0)

    def commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = o['commit'](op, item, price, farm, private, market, shed_capacity)
        if ok:
            d = D(farm)
            if op == 'SELL':
                d['rev'][item] += price; d['units'][item] += 1
                if item in HOURLY:
                    d['sales'].append((cur['hour'], item, price))
            else:
                cat = {'BUY_PRODUCT': 'feed_wheat' if item == 'WHEAT' else 'fert_buy', 'BUY_SEED': 'seed_' + item, 'BUY_ANIMAL': 'animal_' + item}[op]; d['spend'][cat] += price
                if op != 'BUY_PRODUCT':
                    d['buys'].append((cur['hour'], op[4:], item))
        return ok

    def hire(farm, private, board_size, mult=eng.FARM_HAND_COST_MULT):
        m0 = farm['money']; o['hire'](farm, private, board_size, mult); d = D(farm); d['spend']['hire'] += m0 - farm['money']; d['hires'] += int(farm['money'] != m0)

    def land(farm, board_size):
        m0 = farm['money']; o['land'](farm, board_size); D(farm)['spend']['land'] += m0 - farm['money']

    def eod(state, env, day):
        farms = state[0].observation.farms; mk = state[0].observation.market
        for p, farm in enumerate(farms):
            tiles = [t for row in farm['tiles'] for t in row]; plants = [t for t in tiles if isinstance(t, dict) and t.get('kind') == 'PLANT']; animals = [t for t in tiles if isinstance(t, dict) and 'animal' in t]
            priv = state[p].observation.private
            stats[p].setdefault(day, new_day())['end'] = dict(money=farm['money'], herd=dict(collections.Counter(t['animal'] for t in animals)), crops=dict(collections.Counter(t['crop'] for t in plants)),
                empty=sum(1 for t in tiles if t is None), owned=sum(1 for t in tiles if t != 'LOCKED'), quadrants=len(farm['unlocked_quadrants']), hands=len(farm['hands']),
                shed=dict(priv['shed']), seeds=dict(priv.get('seeds', {})), unfed=sum(1 for t in animals if not t['fed_today']), unwatered=sum(1 for t in plants if not t['watered_today']),
                market={k: mk['inventory'].get(k, 0) for k in HOURLY}, prices={k: mk['prices'].get(k, 0) for k in HOURLY})
        o['eod'](state, env, day)
        if shops:   # pinned world (proxy shop sequence); [] = natural shops as in the canonical runner
            town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
            if len(want) == len(town):
                town[:] = want

    def pre(env, step):
        cur['day'] = step // 24; cur['hour'] = step % 24
        for i, f in enumerate(env.state[0].observation.farms):
            owner[id(f)] = i
    eng._apply_unit_action, eng._commit_unit, eng._do_hire, eng._do_buy_land, eng._end_of_day = unit, commit, hire, land, eod
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        with contextlib.redirect_stdout(io.StringIO()):
            fastgame.play(env, [A, B] if seat_b == 1 else [B, A], deep=True, pre_hook=pre)
    finally:
        eng._apply_unit_action, eng._commit_unit, eng._do_hire, eng._do_buy_land, eng._end_of_day = o['unit'], o['commit'], o['hire'], o['land'], o['eod']
    modA = sys.modules.get('agA'); telA = {}
    for name in dir(modA):
        v = getattr(modA, name)
        if isinstance(v, dict) and name.endswith('_REPORT') and v:
            telA[name] = {k: x for k, x in v.items() if isinstance(x, (int, float, str, bool))}
    modB = sys.modules.get('agB'); telB = {k: v for k, v in dict(getattr(modB, '_TEL', {}) or {}).items() if isinstance(v, (int, float))}
    out = dict(seed=seed, seat_b=seat_b, shops=(shops or list(env.state[0].observation.town['unlocked_shops']))[:10], final=[float(s.reward or 0) for s in env.state], b=b_path, a=a_path, knobs=knobs, opp_telemetry=telA, our_telemetry=telB, days={})
    for p in (0, 1):
        out['days'][p] = {d: {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in x.items()} for d, x in sorted(stats[p].items())}
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--label', required=True); ap.add_argument('--b', required=True); ap.add_argument('--a', required=True)
    ap.add_argument('--seeds', default='7000-7015'); ap.add_argument('--seats', default='0,1'); ap.add_argument('--workers', type=int, default=12); ap.add_argument('--knobs', default='', help='PROXY_KNOBS for the B agent (development only)'); ap.add_argument('--nopin', action='store_true', help='natural shop sequence (canonical-runner worlds)')
    a = ap.parse_args()
    seeds = [int(x) for x in a.seeds.split(',')] if ',' in a.seeds or '-' not in a.seeds else list(range(int(a.seeds.split('-')[0]), int(a.seeds.split('-')[1]) + 1))
    shop_seq = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    if not a.nopin:
        for s in seeds:
            if str(s) not in shop_seq:
                sys.exit(f'seed {s} has no pinned shop sequence (run proxy_eval on it first, or pass --nopin for natural shops)')
    jobs = [(a.b, a.a, s, seat, ([] if a.nopin else shop_seq[str(s)]), a.knobs) for s in seeds for seat in [int(x) for x in a.seats.split(',')]]
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(play, jobs))
    os.makedirs(os.path.join(ROOT, 'o_results', 'trace'), exist_ok=True)
    out = os.path.join(ROOT, 'o_results', 'trace', f'{a.label}.json'); json.dump(res, open(out, 'w'), indent=0)
    m = [r['final'][r['seat_b']] - r['final'][1 - r['seat_b']] for r in res]
    print(f"{a.label}: {len(res)} games, margin mean {sum(m)/len(m):+.0f}, wins {sum(1 for x in m if x > 0)}/{len(m)} -> {out}")


if __name__ == '__main__':
    main()
