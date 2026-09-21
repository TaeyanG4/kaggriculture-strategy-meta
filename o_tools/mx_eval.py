"""Market-executor evaluation: per-product revenue/units for BOTH seats, recorded from every executed unit sale (engine._commit_unit hook),
over pinned public-fork worlds (proxy_eval shop sequences, seeds 7000-7015, both seats) and frozen elite replays (elite_pool style).
Usage: python o_tools/mx_eval.py --label <L> [--knobs "k=v,..."] [--seeds 7000-7015] [--opps v46,k0006,v48] [--elite Unknown_Mother-Goose,Majkel1337 --per-team 40] [--workers 16] [--b agent/p000_planner.py]
       python o_tools/mx_eval.py --compare base19 <L>       (paired per opponent: revenue / margin deltas, win flips, per-product units and $/unit)
Output: o_results/mx/eval_<L>.json = [{opp, seed_or_episode, seat_b, our_cash, their_cash, rev, units, opp_rev, opp_units, buy, opp_buy, feed_spend, other_spend}]
Frozen elites do not react, so use them paired only (candidate vs base on the same episode)."""
import argparse, collections, copy, glob, json, os, statistics, sys
from concurrent.futures import ProcessPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'o_tools'))
OUT = os.path.join(ROOT, 'o_results', 'mx')
OPPS = {'v46': 'state/o_dev/v46_public.py', 'k0006': 'state/o_dev/jaxa_k0006.py', 'v48': 'state/o_dev/v48_public.py',
        'v37': 'agent/public_v37_more_yield.py', 'o227': 'agent/o227_stealth_drop.py',
        # live-population lineages (reports/o-live-source-trace-2026-09-18.ko.md): executing public sources, router_v5 reproduced a live game 720/720
        'router_v5': 'state/o_dev/datasets/donor_agents/agents/tschinkel-router-v5.py', 'router_v31': 'state/o_dev/datasets/donor_agents/agents/tschinkel-state-router.py',
        'boatlee_v29': 'state/o_dev/datasets/donor_agents/agents/boatlee-v29-market-hysteresis.py', 'prvsiyan_q45': 'state/o_dev/datasets/donor_agents/agents/prvsiyan-wheat-q45.py',
        'fieldbook': 'state/o_dev/datasets/donor_agents/agents/flexonafft-fieldbook-closeout.py',
        'shop_router_v5': 'state/parallel-handoffs/collaboration-20260914/public-latest-live/shop-router-v5/extracted_main.py'}
ITEMS = ['STRAWBERRY', 'MILK', 'WOOL', 'EGG', 'MELON', 'WHEAT', 'FERTILIZER']


def play(job):
    """One game in a worker process. job = (kind, opp, seed_or_path, seat_b, shops, knobs, b_path); kind 'script' (pinned seed) or 'elite' (frozen replay)."""
    kind, opp, src, seat_b, shops, knobs, b_path = job
    os.environ['PROXY_KNOBS'] = knobs; os.environ['MPLBACKEND'] = 'Agg'; os.chdir(ROOT)
    from proxy_eval import load_agent
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine
    B = load_agent(b_path, 'agB')
    if kind == 'elite':
        r = json.load(open(src, encoding='utf-8')); names = r['info']['TeamNames']; tn = opp.replace('_', ' ')
        seat = names.index(tn) if tn in names else names.index(opp); steps = r['steps']; seat_b = 1 - seat
        shops = list(steps[-1][0]['observation']['town']['unlocked_shops']); seed = int(r['info'].get('seed') or 0) % (2 ** 31)
        key = os.path.basename(src).split('-')[0]

        def A(observation, configuration=None):
            k = int(observation['step']) + 1
            return copy.deepcopy(steps[k][seat]['action']) if k < len(steps) else {}
    else:
        A = load_agent(OPPS.get(opp, opp), 'agA'); seed = int(src); key = seed
    orig_eod = engine._end_of_day; orig_commit = engine._commit_unit; orig_hire = engine._do_hire; orig_land = engine._do_buy_land
    seat_of = {}; rev = [collections.Counter(), collections.Counter()]; units = [collections.Counter(), collections.Counter()]
    buy = [collections.Counter(), collections.Counter()]; other = [0.0, 0.0]

    def pinned(state, env, day):
        orig_eod(state, env, day); town = state[0].observation.town['unlocked_shops']; want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want

    def pre_hook(env, step):   # farm object -> seat, refreshed every step (dict and attribute paths both mapped)
        obs = env.state[0].observation
        for s, f in enumerate(obs['farms']):
            seat_of[id(f)] = s
        for s, f in enumerate(getattr(obs, 'farms', [])):
            seat_of[id(f)] = s

    def commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = orig_commit(op, item, price, farm, private, market, shed_capacity)
        if ok:
            s = seat_of[id(farm)]
            if op == 'SELL':
                rev[s][item] += float(price); units[s][item] += 1
            else:
                buy[s][op[4:] + ':' + item] += float(price)
        return ok

    def hire(farm, private, board_size, mult=engine.FARM_HAND_COST_MULT):
        m0 = farm['money']; orig_hire(farm, private, board_size, mult); other[seat_of[id(farm)]] += m0 - farm['money']

    def land(farm, board_size):
        m0 = farm['money']; orig_land(farm, board_size); other[seat_of[id(farm)]] += m0 - farm['money']
    engine._end_of_day = pinned; engine._commit_unit = commit; engine._do_hire = hire; engine._do_buy_land = land
    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        fastgame.play(env, [A, B] if seat_b == 1 else [B, A], deep=True, pre_hook=pre_hook)
    finally:
        engine._end_of_day = orig_eod; engine._commit_unit = orig_commit; engine._do_hire = orig_hire; engine._do_buy_land = orig_land
    o = seat_b; t = 1 - seat_b
    tel = {k: v for k, v in dict(getattr(sys.modules.get('agB'), '_TEL', {}) or {}).items() if isinstance(v, (int, float))}   # p002-style flat telemetry of the candidate module (empty for other agents)
    return dict(opp=opp, seed_or_episode=key, seat_b=seat_b, our_cash=float(env.state[o].reward or 0), their_cash=float(env.state[t].reward or 0), telemetry=tel,
                rev=dict(rev[o]), units=dict(units[o]), opp_rev=dict(rev[t]), opp_units=dict(units[t]), buy=dict(buy[o]), opp_buy=dict(buy[t]),
                feed_spend=buy[o].get('PRODUCT:WHEAT', 0.0), other_spend=other[o], opp_other_spend=other[t])


def compare(base, cand):
    load = lambda l: {(x['opp'], str(x['seed_or_episode']), x['seat_b']): x for x in json.load(open(os.path.join(OUT, f'eval_{l}.json')))}
    B = load(base); C = load(cand); keys = sorted(k for k in B if k in C)
    se = lambda v: statistics.stdev(v) / len(v) ** 0.5 if len(v) > 1 else 0.0
    tot = lambda d: sum(d.values())
    ppu = lambda r, u: r / u if u else 0.0

    def block(name, ks):
        d_our = [tot(C[k]['rev']) - tot(B[k]['rev']) for k in ks]; d_opp = [tot(C[k]['opp_rev']) - tot(B[k]['opp_rev']) for k in ks]
        dm = [(C[k]['our_cash'] - C[k]['their_cash']) - (B[k]['our_cash'] - B[k]['their_cash']) for k in ks]
        w0 = [B[k]['our_cash'] > B[k]['their_cash'] for k in ks]; w1 = [C[k]['our_cash'] > C[k]['their_cash'] for k in ks]
        flips = [f"{k[1]}{'ab'[k[2]]}{'+' if b else '-'}" for k, a, b in zip(ks, w0, w1) if a != b]
        print(f"{name:22s} n={len(ks):3d} | our rev {statistics.mean(d_our):+6.0f} opp rev {statistics.mean(d_opp):+6.0f} | margin {statistics.mean(dm):+6.0f} (se {se(dm):4.0f}) worse/better(>500) {sum(x < -500 for x in dm)}/{sum(x > 500 for x in dm)} | wins {sum(w0)}->{sum(w1)} flips {' '.join(flips) or '-'}")
        row = ['   product    | our units  $/unit           | opp units  $/unit']
        for it in ITEMS:
            u0 = sum(B[k]['units'].get(it, 0) for k in ks) / len(ks); u1 = sum(C[k]['units'].get(it, 0) for k in ks) / len(ks)
            p0 = ppu(sum(B[k]['rev'].get(it, 0) for k in ks), u0 * len(ks)); p1 = ppu(sum(C[k]['rev'].get(it, 0) for k in ks), u1 * len(ks))
            v0 = sum(B[k]['opp_units'].get(it, 0) for k in ks) / len(ks); v1 = sum(C[k]['opp_units'].get(it, 0) for k in ks) / len(ks)
            q0 = ppu(sum(B[k]['opp_rev'].get(it, 0) for k in ks), v0 * len(ks)); q1 = ppu(sum(C[k]['opp_rev'].get(it, 0) for k in ks), v1 * len(ks))
            if u0 or u1 or v0 or v1:
                row.append(f"   {it:11s}| {u0:5.1f}->{u1:5.1f} {p0:5.1f}->{p1:5.1f} | {v0:5.1f}->{v1:5.1f} {q0:5.1f}->{q1:5.1f}")
        print('\n'.join(row))
        return d_our, d_opp, dm, sum(w0), sum(w1), len(flips)
    print(f'{cand} vs {base} paired (n={len(keys)}); units and $/unit are per-game means, base -> cand')
    opps = [o for o in dict.fromkeys(k[0] for k in B) if any(k[0] == o for k in keys)]; acc = [[], [], [], 0, 0, 0]   # base file order: forks first, then elites
    for o in opps:
        r = block(o, [k for k in keys if k[0] == o])
        for i in range(3):
            acc[i] += r[i]
        for i in range(3, 6):
            acc[i] += r[i]
    d_our, d_opp, dm, w0, w1, nf = acc
    print(f"POOL n={len(dm)} our rev {statistics.mean(d_our):+.0f} opp rev {statistics.mean(d_opp):+.0f} margin {statistics.mean(dm):+.0f} (se {se(dm):.0f}, {statistics.mean(dm) / max(1e-9, se(dm)):.1f} se) worse {sum(x < -500 for x in dm)} better {sum(x > 500 for x in dm)} wins {w0}->{w1} flips {nf}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--label', default=''); ap.add_argument('--knobs', default=''); ap.add_argument('--seeds', default='7000-7015')
    ap.add_argument('--opps', default='v46,k0006,v48'); ap.add_argument('--elite', default=''); ap.add_argument('--per-team', type=int, default=40)
    ap.add_argument('--workers', type=int, default=16); ap.add_argument('--b', default='agent/p000_planner.py'); ap.add_argument('--dir', default='o_replays/elite_current')
    ap.add_argument('--compare', nargs=2, metavar=('BASE', 'CAND'))
    a = ap.parse_args(); os.makedirs(OUT, exist_ok=True)
    if a.compare:
        compare(*a.compare); return
    if not a.label:
        ap.error('--label required')
    lo, hi = (a.seeds.split('-') + [a.seeds])[:2]; seeds = list(range(int(lo), int(hi) + 1))
    shop_seq = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    jobs = []
    for opp in [o for o in a.opps.split(',') if o]:
        for s in seeds:
            if str(s) not in shop_seq:
                sys.exit(f'seed {s} has no pinned shop sequence in o_results/proxy/shop_seq.json (run proxy_eval on it first)')
            jobs += [('script', opp, s, seat, shop_seq[str(s)], a.knobs, a.b) for seat in (0, 1)]
    for team in [t for t in a.elite.split(',') if t]:
        files = sorted(glob.glob(os.path.join(ROOT, a.dir, team, '*-replay.json')))[:a.per_team]
        jobs += [('elite', team, f, None, None, a.knobs, a.b) for f in files]
    with ProcessPoolExecutor(a.workers) as ex:
        res = list(ex.map(play, jobs, chunksize=2))
    json.dump(res, open(os.path.join(OUT, f'eval_{a.label}.json'), 'w'), indent=0)
    for opp in dict.fromkeys(r['opp'] for r in res):
        rs = [r for r in res if r['opp'] == opp]
        print(f"[{a.label}] {opp:22s} n={len(rs):3d} ours {statistics.mean(r['our_cash'] for r in rs):7.0f} theirs {statistics.mean(r['their_cash'] for r in rs):7.0f} margin {statistics.mean(r['our_cash'] - r['their_cash'] for r in rs):+6.0f} wins {sum(r['our_cash'] > r['their_cash'] for r in rs)}/{len(rs)} | rev ours {statistics.mean(sum(r['rev'].values()) for r in rs):6.0f} theirs {statistics.mean(sum(r['opp_rev'].values()) for r in rs):6.0f}")


if __name__ == '__main__':
    main()
