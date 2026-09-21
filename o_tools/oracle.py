"""Macro Oracle: at each branch day (6/9/12/15/18) force K strategy branches on the planner (day-gated knobs) and greedily keep the
branch with the best final margin (own - rival cash) = ex-post full-information upper bound. A matched-null family runs the same
procedure with K meaningless perturbations (one worker idles one step at hour h of the branch day) to measure how much of the
oracle's gain is chaos harvesting. Per-day cash of both seats is recorded so 1-/2-day lookahead selectors can be scored offline.
Usage: python o_tools/oracle.py --seeds 7000-7015 --workers 12 --label orc_sel [--family both|strat|null] [--knobs base_knobs]"""
import argparse, json, os, sys, time
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['MPLBACKEND'] = 'Agg'
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
STAGES = [6, 9, 12, 15, 18]
# strategy branches per stage: (name, knob string gated at the stage day); KEEP = no change
OPTIONS = {
    6: [('COW+2', 'plus_cow=2'), ('SHEEP+2', 'plus_sheep=2'), ('GOOSE+2', 'plus_goose=2'), ('STRAW+8', 'straw_plus=8'), ('SAVE', 'save_day=6')],
    9: [('COW+2', 'plus_cow=2'), ('SHEEP+2', 'plus_sheep=2'), ('GOOSE+2', 'plus_goose=2'), ('STRAW+8', 'straw_plus=8'), ('LAND3+2d', 'land3=11')],
    12: [('COW+2', 'plus_cow=2'), ('GOOSE+2', 'plus_goose=2'), ('STRAW+6', 'straw_plus=6'), ('TOM+4', 'tom_per=12'), ('CAR+8', 'car_plus=8')],
    15: [('TOM+4', 'tom_per=12'), ('CAR+8', 'car_plus=8'), ('GOOSE+2', 'plus_goose=2'), ('LAND4', 'sw_land4=1,land4=15,land4_last=16'), ('HERDSTOP', 'herd_stop=15')],
    18: [('CAR+8', 'car_plus=8'), ('TOM_D20', 'tom_d1=20,tom_per=12'), ('SEED27', 'seed_last=27'), ('HERDSTOP', 'herd_stop=18'), ('NOWFERT', 'nwf_d=99')],
}
OPTIONS2 = {   # round 2: reduce / retime / stop branches
    6: [('STRAW-8', 'straw_plus=-8'), ('HERDSTOP', 'herd_stop=6'), ('GOOSE+2', 'plus_goose=2'), ('LAND3NEV', 'land3=99'), ('SAVE', 'save_day=6')],
    9: [('STRAW-8', 'straw_plus=-8'), ('HERDSTOP', 'herd_stop=9'), ('NOSTRAW', 'straw_plus=-40'), ('LAND3NEV', 'land3=99'), ('FEEDCUT', 'worth_d=9')],
    12: [('HERDSTOP', 'herd_stop=12'), ('NOSTRAW', 'straw_plus=-40'), ('TOM0', 'tom_per=0'), ('CAR0', 'car_pet=0,car_plus=-8'), ('FEEDCUT', 'worth_d=12')],
    15: [('FEEDCUT', 'worth_d=15'), ('TOM0', 'tom_per=0'), ('CAR0', 'car_pet=0,car_plus=-8'), ('SEED24', 'seed_last=24'), ('NOWFERT', 'nwf_d=99')],
    18: [('FEEDCUT', 'worth_d=18'), ('FEEDCUT2', 'worth_d=18,worth_f=2.0'), ('SEED24', 'seed_last=24'), ('CAR+8', 'car_plus=8'), ('TOM_D20', 'tom_d1=20,tom_per=12')],
}
OPTIONS3 = {   # round 3: market-timing / portfolio branches
    6: [('HOLD_ON', 'sw_price_hold=1'), ('DUMP', 'buf=0'), ('STRAW+12', 'straw_plus=12'), ('CARROT2OFF', 'sw_carrot2=0'), ('EGGOFF', 'sw_egg=0')],
    9: [('HOLD_ON', 'sw_price_hold=1'), ('DUMP', 'buf=0'), ('STRAW+8', 'straw_plus=8'), ('OPP1.3', 'opp_f=1.3'), ('OPP0.7', 'opp_f=0.7')],
    12: [('HOLD_ON', 'sw_price_hold=1'), ('TOMSELL20', 'tom_sell=20'), ('TOMRATE3', 'tom_rate=3.0'), ('CARHOLDOFF', 'sw_carrot_hold=0'), ('OPP1.3', 'opp_f=1.3')],
    15: [('HOLD_ON', 'sw_price_hold=1'), ('TOMSELL22', 'tom_sell=22'), ('CARHOLDOFF', 'sw_carrot_hold=0'), ('WFERT', 'nwf_d=0'), ('CAPM3', 'cap_m=3,cap_m23=12')],
    18: [('HOLD_ON', 'sw_price_hold=1'), ('TOMSELL24', 'tom_sell=24'), ('TOMRATE1', 'tom_rate=1.0'), ('SEED28', 'seed_last=28'), ('TERM29', 'term_d=29')],
}
K = 5   # branches per family per stage (plus KEEP)


def gated(day, knobs):
    return ','.join(f'@{day}:{kv}' for kv in knobs.split(','))


def play(a_path, b_path, seed, seat_b, shops, knobs):
    """One pinned-world game; returns final cash of both seats, cash at every day end and stage-day state features."""
    os.environ['PROXY_KNOBS'] = knobs
    from proxy_eval import load_agent
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    A = load_agent(a_path, 'agA'); B = load_agent(b_path, 'agB')
    orig = engine._end_of_day

    def pinned(state, env, day):
        orig(state, env, day)
        want = shops[:len(state[0].observation.town['unlocked_shops'])]
        if len(want) == len(state[0].observation.town['unlocked_shops']):
            state[0].observation.town['unlocked_shops'][:] = want
    engine._end_of_day = pinned
    import fastgame
    money = {0: [], 1: []}; feats = {}

    def day_hook(e, d):
        for s_ in (0, 1):
            money[s_].append(e.state[0].observation['farms'][s_]['money'])

    def step_hook(e, step_before):
        d = (step_before + 1) // 24
        if (step_before + 1) % 24 == 0 and d in STAGES:   # state at day d h0 (= env.run's steps[d*24])
            ob = e.state[0].observation; f = ob['farms'][seat_b]
            an = {}
            for row in f['tiles']:
                for t in row:
                    if isinstance(t, dict) and t.get('animal'):
                        an[t['animal']] = an.get(t['animal'], 0) + 1
            feats[d] = dict(cash=f['money'], animals=an, shops=list(ob['town'].get('unlocked_shops', [])),
                            free=sum(1 for row in f['tiles'] for t in row if t is None), quads=len(f['unlocked_quadrants']),
                            prices={k: ob['market']['prices'][k] for k in ('MILK', 'WOOL', 'STRAWBERRY', 'EGG', 'FERTILIZER')})
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        fastgame.play(env, [A, B] if seat_b == 1 else [B, A], deep=True, day_hook=day_hook, step_hook=step_hook)
    finally:
        engine._end_of_day = orig
    rw = [x.reward for x in env.state]
    for s_ in (0, 1):
        money[s_] = (money[s_] + [money[s_][-1]] * 30)[:30]
    return dict(b=rw[seat_b], a=rw[1 - seat_b], money_b=money[seat_b], money_a=money[1 - seat_b], feats=feats)


def add_knobs(cur, k, family):
    if family == 'null':
        prev = [kv for kv in cur.split(',') if kv.startswith('null_days=')]
        merged = ('null_days=' + prev[0].split('=', 1)[1] + '/' + k.split('=', 1)[1]) if prev else k
        return ','.join([kv for kv in cur.split(',') if kv and not kv.startswith('null_days=')] + [merged])
    return ','.join([kv for kv in cur.split(',') if kv] + [k])


def chain(args):
    """Greedy oracle chain for one world and one family; returns every branch result per stage."""
    a_path, b_path, seed, seat_b, shops, base_knobs, family = args
    cur = base_knobs; cur_res = play(a_path, b_path, seed, seat_b, shops, cur)
    out = dict(seed=seed, seat_b=seat_b, family=family, base=dict(b=cur_res['b'], a=cur_res['a']), stages=[])
    for D in STAGES:
        table = {'r2': OPTIONS2, 'r3': OPTIONS3}.get(os.environ.get('ORACLE_OPTS', ''), OPTIONS)
        opts = [(n, gated(D, k)) for n, k in table[D][:K]] if family == 'strat' else [(f'NULL_h{h}', f'null_days={D}:{h}') for h in range(K)]
        branches = [dict(name='KEEP', knobs=cur, b=cur_res['b'], a=cur_res['a'], money_b=cur_res['money_b'], money_a=cur_res['money_a'], feats=cur_res['feats'][D])]
        for name, k in opts:
            knobs = add_knobs(cur, k, family)
            r = play(a_path, b_path, seed, seat_b, shops, knobs)
            branches.append(dict(name=name, knobs=knobs, b=r['b'], a=r['a'], money_b=r['money_b'], money_a=r['money_a'], feats=r['feats'][D], feats_all=r['feats']))
        best = max(branches, key=lambda x: x['b'] - x['a'])
        out['stages'].append(dict(day=D, best=best['name'], branches=[{k: v for k, v in br.items() if k != 'feats_all'} for br in branches]))
        cur = best['knobs']
        cur_res = dict(b=best['b'], a=best['a'], money_b=best['money_b'], money_a=best['money_a'], feats=best.get('feats_all', cur_res['feats']))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--a', default='agent/o227_stealth_drop.py'); ap.add_argument('--b', default='agent/p000_planner.py')
    ap.add_argument('--seeds', default='7000-7015'); ap.add_argument('--seats', default='0,1'); ap.add_argument('--workers', type=int, default=12)
    ap.add_argument('--label', required=True); ap.add_argument('--family', default='both'); ap.add_argument('--knobs', default='')
    a = ap.parse_args()
    lo, hi = (a.seeds.split('-') + [a.seeds])[:2]; seeds = list(range(int(lo), int(hi) + 1))
    cache = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    fams = ['strat', 'null'] if a.family == 'both' else [a.family]
    jobs = [(a.a, a.b, s, int(seat), cache[str(s)], a.knobs, fam) for s in seeds for seat in a.seats.split(',') for fam in fams]
    t0 = time.time()
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(chain, jobs))
    os.makedirs(os.path.join(ROOT, 'o_results', 'oracle'), exist_ok=True)
    json.dump(res, open(os.path.join(ROOT, 'o_results', 'oracle', f'{a.label}.json'), 'w'))
    print(f'{len(res)} chains in {(time.time() - t0) / 60:.1f} min -> o_results/oracle/{a.label}.json')


if __name__ == '__main__':
    main()
