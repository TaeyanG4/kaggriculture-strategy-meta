"""Market Impact Oracle & Counterfactual Attribution Audit Tool
Analyzes base19 vs reactive and frozen opponents across products and time phases.
Computes:
1. Product x Phase (d0-9, d10-18, d19-29, total) revenue, units, avg prices for both sides.
2. Paired margin contribution (our revenue - opponent revenue).
3. Hourly sales profiles and timing divergences.
4. Theoretical margin ceiling for 1, 4, 8, 16 unit pre-emption (own gain + opponent suppression).
Usage:
    python o_tools/market_impact_audit.py --opp v37 [--seeds 7000-7015] [--workers 8]
    python o_tools/market_impact_audit.py --opp v46
    python o_tools/market_impact_audit.py --opp v48
    python o_tools/market_impact_audit.py --opp k0006
    python o_tools/market_impact_audit.py --opp frozen_mg
    python o_tools/market_impact_audit.py --opp frozen_majkel
    python o_tools/market_impact_audit.py --all-opps
"""
import argparse, collections, copy, glob, json, os, sys, time, statistics
from concurrent.futures import ProcessPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_ROOT = r'H:\dev\kaggle-data\kaggriculture-strategy-meta'
os.environ['MPLBACKEND'] = 'Agg'
for p in [os.path.join(ROOT, 'o_tools'), os.path.join(MAIN_ROOT, 'o_tools'), ROOT, MAIN_ROOT]:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

def resolve_path(rel_path):
    p = os.path.join(ROOT, rel_path)
    if not os.path.exists(p):
        main_p = os.path.join(MAIN_ROOT, rel_path)
        if os.path.exists(main_p):
            return main_p
    return p

PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
PHASES = ('d0_9', 'd10_18', 'd19_29')

OPPONENTS = {
    'v37': {'type': 'agent', 'rel_path': os.path.join('agent', 'public_v37_more_yield.py')},
    'v46': {'type': 'agent', 'rel_path': os.path.join('state', 'o_dev', 'v46_public.py')},
    'v48': {'type': 'agent', 'rel_path': os.path.join('state', 'o_dev', 'v48_public.py')},
    'k0006': {'type': 'agent', 'rel_path': os.path.join('state', 'o_dev', 'jaxa_k0006.py')},
    'frozen_mg': {'type': 'frozen', 'team': 'Unknown_Mother-Goose', 'dir': 'Unknown_Mother-Goose'},
    'frozen_majkel': {'type': 'frozen', 'team': 'Majkel1337', 'dir': 'Majkel1337'},
    'frozen_boey': {'type': 'frozen', 'team': 'Boey', 'dir': 'Boey'},
    'frozen_spataro': {'type': 'frozen', 'team': 'SpaTaro', 'dir': 'SpaTaro'},
    'frozen_dsm': {'type': 'frozen', 'team': 'DSM', 'dir': 'DSM'},
}

def get_phase(step):
    day = step // 24
    if day <= 9:
        return 'd0_9'
    elif day <= 18:
        return 'd10_18'
    else:
        return 'd19_29'

def run_single_match(args):
    """Run one match, logging every market transaction with exact price, step, seat, item."""
    opp_spec, seed, seat_b, shops, b_path, replay_path = args
    for p in [os.path.join(ROOT, 'o_tools'), os.path.join(MAIN_ROOT, 'o_tools'), ROOT, MAIN_ROOT]:
        if os.path.isdir(p) and p not in sys.path:
            sys.path.insert(0, p)
    from proxy_eval import load_agent
    import fastgame
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine

    B = load_agent(b_path, 'agB')
    if opp_spec['type'] == 'agent':
        A = load_agent(opp_spec['path'], 'agA')
    else:
        # Frozen opponent from replay
        r = json.load(open(replay_path, encoding='utf-8'))
        names = r['info']['TeamNames']
        tn = opp_spec['team'].replace('_', ' ')
        seat = names.index(tn) if tn in names else names.index(opp_spec['team'])
        steps = r['steps']
        def frozen(observation, configuration=None):
            k = int(observation['step']) + 1
            return copy.deepcopy(steps[k][seat]['action']) if k < len(steps) else {}
        A = frozen

    orig_eod = engine._end_of_day
    orig_commit = engine._commit_unit
    orig_pm = engine._process_market

    cur = {'step': 0}
    tx_log = []  # (step, seat, op, item, price)
    inv_log = {}  # step -> dict(market['inventory'])

    def pinned(state, env, day):
        orig_eod(state, env, day)
        town = state[0].observation.town['unlocked_shops']
        want = shops[:len(town)]
        if len(want) == len(town):
            town[:] = want

    seat_of = {}
    def process_market(state, env):
        seat_of.clear()
        for i, f in enumerate(state[0].observation.farms):
            seat_of[id(f)] = i
        cur['step'] = int(state[0].observation.step)
        inv_log[cur['step']] = dict(state[0].observation.market['inventory'])
        return orig_pm(state, env)

    def commit(op, item, price, farm, private, market, shed_capacity=100):
        ok = orig_commit(op, item, price, farm, private, market, shed_capacity)
        if ok:
            tx_log.append((cur['step'], seat_of.get(id(farm)), op, item, int(price)))
        return ok

    engine._end_of_day = pinned
    engine._commit_unit = commit
    engine._process_market = process_market

    try:
        env = make('kaggriculture', configuration={'seed': seed}, debug=False)
        agents = [A, B] if seat_b == 1 else [B, A]
        fastgame.play(env, agents, deep=True)
    finally:
        engine._end_of_day = orig_eod
        engine._commit_unit = orig_commit
        engine._process_market = orig_pm

    # Rewards
    ours_cash = float(env.state[seat_b].reward or 0)
    opp_cash = float(env.state[1 - seat_b].reward or 0)

    # Compile transaction aggregates
    # rev[who][phase][item], units[who][phase][item], spend[who][phase][item], hourly_sales[who][item][hour]
    rev = {'our': collections.defaultdict(lambda: collections.Counter()),
           'opp': collections.defaultdict(lambda: collections.Counter())}
    units = {'our': collections.defaultdict(lambda: collections.Counter()),
             'opp': collections.defaultdict(lambda: collections.Counter())}
    hourly = {'our': collections.defaultdict(lambda: collections.Counter()),
              'opp': collections.defaultdict(lambda: collections.Counter())}
    spend = {'our': collections.defaultdict(lambda: collections.Counter()),
             'opp': collections.defaultdict(lambda: collections.Counter())}

    sales_stream = []  # chronological list of sales for pre-emption ceiling analysis
    for step, seat, op, item, price in tx_log:
        if seat is None:
            continue
        who = 'our' if seat == seat_b else 'opp'
        phase = get_phase(step)
        hour = step % 24
        if op == 'SELL':
            rev[who][phase][item] += price
            units[who][phase][item] += 1
            hourly[who][item][hour] += 1
            sales_stream.append((step, who, item, price))
        elif op.startswith('BUY_') or op in ('HIRE', 'BUY_LAND'):
            spend[who][phase][op + '_' + item] += price

    return {
        'seed': seed,
        'seat_b': seat_b,
        'our_cash': ours_cash,
        'opp_cash': opp_cash,
        'margin': ours_cash - opp_cash,
        'rev': {w: {ph: dict(rev[w][ph]) for ph in PHASES} for w in ('our', 'opp')},
        'units': {w: {ph: dict(units[w][ph]) for ph in PHASES} for w in ('our', 'opp')},
        'hourly': {w: {it: dict(hourly[w][it]) for it in PRODUCTS} for w in ('our', 'opp')},
        'spend': {w: {ph: dict(spend[w][ph]) for ph in PHASES} for w in ('our', 'opp')},
        'sales_stream': sales_stream,
        'inv_log': inv_log,
    }


def compute_preemption_ceiling(match_results):
    """Computes the theoretical margin gain from 1, 4, 8, 16 unit priority pre-emption.
    For each product and phase, measures:
    1. Own Price Advantage: If we sold our units before opponent's dumps instead of after.
    2. Opponent Suppression: If our units were injected Delta-U units earlier into the market,
       how much opponent revenue would be suppressed by the engine's price degradation formula.
    """
    from kaggle_environments.envs.kaggriculture import kaggriculture as engine

    ceilings = collections.defaultdict(lambda: collections.defaultdict(lambda: {1: 0.0, 4: 0.0, 8: 0.0, 16: 0.0}))
    n_games = len(match_results)

    for r in match_results:
        # Group sales by (day, product)
        day_sales = collections.defaultdict(lambda: collections.defaultdict(list))
        for step, who, item, price in r['sales_stream']:
            d = step // 24
            day_sales[d][item].append((step, who, price))

        for d, prod_map in day_sales.items():
            phase = 'd0_9' if d <= 9 else ('d10_18' if d <= 18 else 'd19_29')
            for item, sales in prod_map.items():
                our_sales = [s for s in sales if s[1] == 'our']
                opp_sales = [s for s in sales if s[1] == 'opp']
                if not our_sales or not opp_sales:
                    continue

                # Check if opponent sold before us or after us
                # If opponent sold first and we sold later, our price was depressed by opponent units
                first_opp_step = min(s[0] for s in opp_sales)
                first_our_step = min(s[0] for s in our_sales)

                # For Delta in [1, 4, 8, 16]:
                # If we supply Delta units FIRST at day start (or pre-empt opponent):
                # How much does the market price drop for opponent's units?
                opp_units_count = len(opp_sales)
                for delta in (1, 4, 8, 16):
                    # Theoretical price impact on opponent:
                    # Under the engine formula, selling delta units increases inventory by delta.
                    # Price drop per unit = market_price(inv) - market_price(inv + delta)
                    # We evaluate this drop across the opponent's actual sales
                    suppression = 0.0
                    for step, who, actual_price in opp_sales:
                        inv = r['inv_log'].get(step, {}).get(item, 10000)
                        p_base = engine.market_price(item, inv)
                        p_suppressed = engine.market_price(item, inv + delta)
                        suppression += max(0, p_base - p_suppressed)

                    # Own gain if our units that sold after opponent were sold before opponent:
                    own_advantage = 0.0
                    for step, who, actual_price in our_sales:
                        if step >= first_opp_step:
                            # Our price was subject to opponent's inventory
                            # At best, we could have gotten the pre-opponent price
                            inv_before_opp = r['inv_log'].get(first_opp_step, {}).get(item, 10000)
                            p_ideal = engine.market_price(item, inv_before_opp)
                            own_advantage += max(0, p_ideal - actual_price)

                    # Cap own_advantage to delta units
                    own_advantage_capped = min(own_advantage, delta * engine.MARKET_PARAMS[item]['base'])
                    total_ceiling = suppression + own_advantage_capped
                    ceilings[item][phase][delta] += total_ceiling / n_games

    return ceilings


def audit_opponent(opp_key, seeds=None, workers=8, b_path='agent/p000_planner.py', per_team=32):
    """Run audit for one opponent specification."""
    opp_spec = copy.deepcopy(OPPONENTS[opp_key])
    b_path_resolved = resolve_path(b_path)

    if opp_spec['type'] == 'agent':
        opp_spec['path'] = resolve_path(opp_spec.get('rel_path', opp_spec.get('path', '')))
        if seeds is None:
            seeds = list(range(7000, 7016))
        cache = json.load(open(resolve_path(os.path.join('o_results', 'proxy', 'shop_seq.json'))))
        jobs = [(opp_spec, s, seat, cache[str(s)], b_path_resolved, None) for s in seeds for seat in (0, 1)]
    else:
        # Frozen opponent: load from replays
        replays_dir = resolve_path(os.path.join('o_replays', 'elite_current', opp_spec['dir']))
        replays = sorted(glob.glob(os.path.join(replays_dir, '*-replay.json')))[:per_team]
        jobs = []
        for f in replays:
            r = json.load(open(f, encoding='utf-8'))
            names = r['info']['TeamNames']
            tn = opp_spec['team'].replace('_', ' ')
            seat = names.index(tn) if tn in names else names.index(opp_spec['team'])
            shops = list(r['steps'][-1][0]['observation']['town']['unlocked_shops'])
            seed = int(r['info'].get('seed') or 0) % (2 ** 31)
            jobs.append((opp_spec, seed, 1 - seat, shops, b_path_resolved, f))

    print(f"\n========================================================")
    print(f"AUDITING base19 vs {opp_key.upper()} (n={len(jobs)} games, workers={workers})")
    print(f"========================================================")
    t0 = time.time()
    with ProcessPoolExecutor(workers) as ex:
        results = list(ex.map(run_single_match, jobs))
    elapsed = time.time() - t0
    print(f"Completed in {elapsed:.1f}s ({len(results)/elapsed:.2f} games/s)")

    # Aggregate summaries
    n = len(results)
    mean_our_cash = statistics.mean(r['our_cash'] for r in results)
    mean_opp_cash = statistics.mean(r['opp_cash'] for r in results)
    mean_margin = statistics.mean(r['margin'] for r in results)
    wins = sum(r['margin'] > 0 for r in results)
    print(f"Summary: Ours {mean_our_cash:.0f} | Opp {mean_opp_cash:.0f} | Margin {mean_margin:+.0f} | Wins {wins}/{n} ({wins/n*100:.1f}%)")

    # Aggregate revenue, units, spend, hourly by product and phase
    agg_rev = {'our': collections.defaultdict(lambda: collections.Counter()),
               'opp': collections.defaultdict(lambda: collections.Counter())}
    agg_units = {'our': collections.defaultdict(lambda: collections.Counter()),
                 'opp': collections.defaultdict(lambda: collections.Counter())}
    agg_spend = {'our': collections.defaultdict(lambda: collections.Counter()),
                 'opp': collections.defaultdict(lambda: collections.Counter())}
    agg_hourly = {'our': collections.defaultdict(lambda: collections.Counter()),
                  'opp': collections.defaultdict(lambda: collections.Counter())}

    for r in results:
        for w in ('our', 'opp'):
            for ph in PHASES:
                agg_rev[w][ph].update(r['rev'][w][ph])
                agg_units[w][ph].update(r['units'][w][ph])
                agg_spend[w][ph].update(r['spend'][w][ph])
            for p in PRODUCTS:
                agg_hourly[w][p].update(r['hourly'][w][p])

    # Print Product x Phase table
    print(f"\n--- PRODUCT x PHASE REVENUE & MARGIN TABLE (Per Game Average) ---")
    header = f"{'Product':11s} | {'d0-9 (Our/Opp/Δ)':20s} | {'d10-18 (Our/Opp/Δ)':22s} | {'d19-29 (Our/Opp/Δ)':22s} | {'TOTAL (Our/Opp/Δ)':22s} | {'Our u / Opp u':15s}"
    print(header)
    print("-" * len(header))

    prod_totals = {}
    for p in PRODUCTS:
        row_str = f"{p:11s} | "
        p_our_tot = 0.0
        p_opp_tot = 0.0
        p_our_u_tot = 0.0
        p_opp_u_tot = 0.0
        for ph in PHASES:
            our_r = agg_rev['our'][ph][p] / n
            opp_r = agg_rev['opp'][ph][p] / n
            delta_r = our_r - opp_r
            p_our_tot += our_r
            p_opp_tot += opp_r
            p_our_u_tot += agg_units['our'][ph][p] / n
            p_opp_u_tot += agg_units['opp'][ph][p] / n
            row_str += f"{our_r:6.0f}/{opp_r:6.0f}/{delta_r:+6.0f} | "
        tot_delta = p_our_tot - p_opp_tot
        row_str += f"{p_our_tot:6.0f}/{p_opp_tot:6.0f}/{tot_delta:+6.0f} | {p_our_u_tot:6.1f} / {p_opp_u_tot:6.1f}"
        prod_totals[p] = {'our': p_our_tot, 'opp': p_opp_tot, 'delta': tot_delta}
        print(row_str)

    # Print Hourly Sales Breakdown table
    print(f"\n--- HOURLY SALES BREAKDOWN (Per Game Average Units Sold by Time of Day) ---")
    h_header = f"{'Product':11s} | {'Dawn (h0-5) Our/Opp':20s} | {'Morning (h6-11) Our/Opp':24s} | {'Aftn (h12-17) Our/Opp':22s} | {'Eve (h18-23) Our/Opp':21s} | {'Peak Hour (Our vs Opp)':22s}"
    print(h_header)
    print("-" * len(h_header))
    for p in ('STRAWBERRY', 'MILK', 'WOOL', 'FERTILIZER', 'WHEAT', 'TOMATO', 'MELON'):
        our_dawn = sum(agg_hourly['our'][p][h] for h in range(0, 6)) / n
        opp_dawn = sum(agg_hourly['opp'][p][h] for h in range(0, 6)) / n
        our_morn = sum(agg_hourly['our'][p][h] for h in range(6, 12)) / n
        opp_morn = sum(agg_hourly['opp'][p][h] for h in range(6, 12)) / n
        our_aftn = sum(agg_hourly['our'][p][h] for h in range(12, 18)) / n
        opp_aftn = sum(agg_hourly['opp'][p][h] for h in range(12, 18)) / n
        our_eve = sum(agg_hourly['our'][p][h] for h in range(18, 24)) / n
        opp_eve = sum(agg_hourly['opp'][p][h] for h in range(18, 24)) / n
        our_tot = sum(agg_hourly['our'][p].values())
        opp_tot = sum(agg_hourly['opp'][p].values())
        our_peak = max(range(24), key=lambda h: agg_hourly['our'][p][h]) if our_tot > 0 else -1
        opp_peak = max(range(24), key=lambda h: agg_hourly['opp'][p][h]) if opp_tot > 0 else -1
        peak_str = f"h{our_peak} vs h{opp_peak}" if our_peak >= 0 or opp_peak >= 0 else "none"
        print(f"{p:11s} | {our_dawn:6.1f} / {opp_dawn:6.1f}       | {our_morn:7.1f} / {opp_morn:7.1f}         | {our_aftn:6.1f} / {opp_aftn:6.1f}       | {our_eve:6.1f} / {opp_eve:6.1f}      | {peak_str:22s}")

    # Compute preemption ceilings
    ceilings = compute_preemption_ceiling(results)
    print(f"\n--- THEORETICAL PRE-EMPTION MARGIN CEILING (Own Gain + Opp Suppression) ---")
    c_header = f"{'Product':11s} | {'Phase':7s} | {'Δ=1 unit':10s} | {'Δ=4 units':10s} | {'Δ=8 units':10s} | {'Δ=16 units':11s} | {'Potential >= +5k?':18s}"
    print(c_header)
    print("-" * len(c_header))
    for p in PRODUCTS:
        for ph in PHASES:
            c1 = ceilings[p][ph][1]
            c4 = ceilings[p][ph][4]
            c8 = ceilings[p][ph][8]
            c16 = ceilings[p][ph][16]
            has_5k = "YES (+5k candidate)" if c16 >= 5000 or c8 >= 5000 else "NO (<5k ceiling)"
            if c16 >= 500 or c8 >= 300:
                print(f"{p:11s} | {ph:7s} | {c1:+9.0f} | {c4:+9.0f} | {c8:+9.0f} | {c16:+10.0f} | {has_5k}")

    # Save structured audit file
    os.makedirs(os.path.join(ROOT, 'o_results', 'market_impact'), exist_ok=True)
    out_path = os.path.join(ROOT, 'o_results', 'market_impact', f'audit_{opp_key}.json')
    hourly_sales = {
        w: {
            p: {h: agg_hourly[w][p][h] / n for h in range(24)}
            for p in PRODUCTS
        }
        for w in ('our', 'opp')
    }
    summary_data = {
        'opponent': opp_key,
        'n_games': n,
        'mean_our_cash': mean_our_cash,
        'mean_opp_cash': mean_opp_cash,
        'mean_margin': mean_margin,
        'win_rate': wins / n,
        'product_totals': prod_totals,
        'phase_rev': {w: {ph: {p: agg_rev[w][ph][p] / n for p in PRODUCTS} for ph in PHASES} for w in ('our', 'opp')},
        'phase_units': {w: {ph: {p: agg_units[w][ph][p] / n for p in PRODUCTS} for ph in PHASES} for w in ('our', 'opp')},
        'hourly_sales': hourly_sales,
        'preemption_ceilings': {p: {ph: ceilings[p][ph] for ph in PHASES} for p in PRODUCTS},
    }
    json.dump(summary_data, open(out_path, 'w'), indent=2)
    print(f"\nSaved structured audit to {out_path}")
    return summary_data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--opp', default='v37', choices=list(OPPONENTS.keys()) + ['all'])
    ap.add_argument('--seeds', default='7000-7015')
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--b', default='agent/p000_planner.py')
    ap.add_argument('--per-team', type=int, default=32)
    a = ap.parse_args()

    lo, hi = a.seeds.split('-')
    seeds = list(range(int(lo), int(hi) + 1))

    if a.opp == 'all':
        target_opps = ['v37', 'v46', 'v48', 'k0006', 'frozen_mg', 'frozen_majkel', 'frozen_boey', 'frozen_spataro', 'frozen_dsm']
    else:
        target_opps = [a.opp]

    all_summaries = {}
    for opp_key in target_opps:
        summary = audit_opponent(opp_key, seeds=seeds, workers=a.workers, b_path=a.b, per_team=a.per_team)
        all_summaries[opp_key] = summary

    if len(target_opps) > 1:
        # Cross-opponent synthesis table
        print(f"\n========================================================")
        print(f"CROSS-OPPONENT MARGIN CONTRIBUTION SYNTHESIS")
        print(f"========================================================")
        print(f"{'Product':11s} | " + " | ".join(f"{op[:8]:>8s}" for op in target_opps) + " | {'Mean Delta':10s}")
        print("-" * (14 + 11 * len(target_opps) + 13))
        for p in PRODUCTS:
            deltas = [all_summaries[op]['product_totals'][p]['delta'] for op in target_opps]
            mean_d = statistics.mean(deltas)
            print(f"{p:11s} | " + " | ".join(f"{d:+8.0f}" for d in deltas) + f" | {mean_d:+10.0f}")

        # Summary of final cash margins
        print("-" * (14 + 11 * len(target_opps) + 13))
        tot_deltas = [all_summaries[op]['mean_margin'] for op in target_opps]
        print(f"{'NET MARGIN':11s} | " + " | ".join(f"{d:+8.0f}" for d in tot_deltas) + f" | {statistics.mean(tot_deltas):+10.0f}")

        # Save cross-opponent synthesis
        json.dump(all_summaries, open(os.path.join(ROOT, 'o_results', 'market_impact', 'cross_opponent_synthesis.json'), 'w'), indent=2)


if __name__ == '__main__':
    main()
