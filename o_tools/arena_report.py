"""Cluster-level readout of a canonical validation campaign (tools/validation_v1.py results.json) against its config:
per-opponent win rates of parent and candidate, paired margin / own-cash deltas, W->L and L->W counts, cluster-weighted score
(arena_meta.cluster_weights, descriptive) and the DECLARED rules, fixed in the plan documents before any game:
  --rules arena  (default; reports/o-p001-mx2-arena-plan-2026-09-18.ko.md, v1 clusters 1-5, rules R1-R5)
  --rules panel  (reports/o-p002-panel-plan-2026-09-18.ko.md, live-lineage panel, rules L1-L4 incl. the p002 trigger rate)
  --rules policy (reports/o-policy-compare-plan-2026-09-19.ko.md, whole-policy comparison, rules P1-P5 + worlds/big losses/detection flags)
Read-only: no games are run and no rule is derived from the result.
Usage: python o_tools/arena_report.py <campaign_out_dir> <config.json> [--rules arena|panel]"""
import argparse, json, os, statistics as st


def comparison_block(res, cfg, key, C):
    cand, par = key.split('_vs_'); det = C['conditions']; cluster_of = {n: r.get('cluster', r['family']) for n, r in cfg['opponents'].items()}
    weights = cfg.get('arena_meta', {}).get('cluster_weights', {})
    print(f"--- {key}  ({'PRIMARY' if C.get('primary') else 'descriptive'})")
    print(f"family-weighted point delta {C['family_weighted_point_delta']:+.3f}  bootstrap CI {C['approximate_bootstrap_ci']}  signal {C['signal']}  (seed clusters {C['seed_clusters']})")
    print(f"pooled: mean margin delta {C['mean_margin_delta']:+.0f}  own cash delta {C['mean_own_cash_delta']:+.0f}  point delta {C['mean_point_delta']:+.3f}  W->L {C['win_to_loss']}  conditions {len(det)}")
    print('opponent                    cluster            n | parent WR  cand WR | margin d (se) | own d | W->L L->W')
    by_c = {}
    for opp in cfg['opponents']:
        d = [x for x in det if x['opponent'] == opp]
        if not d:
            continue
        pw = res['by_candidate'][par]['subgroups']['opponent_name'][opp]; cw = res['by_candidate'][cand]['subgroups']['opponent_name'][opp]
        dm = [x['margin_delta'] for x in d]; do = [x['own_cash_delta'] for x in d]
        w2l = sum(1 for x in d if x['win_to_loss']); l2w = sum(1 for x in d if x['point_delta'] > 0.5)
        print(f"{opp:27s} {cluster_of[opp][:18]:18s} {len(d):2d} | {pw['point_rate']:8.2f}  {cw['point_rate']:7.2f} | {st.mean(dm):+7.0f} ({st.stdev(dm) / len(dm) ** 0.5 if len(dm) > 1 else 0:4.0f}) | {st.mean(do):+6.0f} | {w2l:3d}  {l2w:3d}")
        by_c.setdefault(cluster_of[opp], []).extend(d)
    print('cluster                          weight | margin d | own d | point d | W->L L->W')
    wsum_m = wsum_p = wtot = 0.0
    for cl, d in by_c.items():
        w = weights.get(cl, 0.0); dm = st.mean(x['margin_delta'] for x in d); do = st.mean(x['own_cash_delta'] for x in d); dp = st.mean(x['point_delta'] for x in d)
        print(f"{cl:32s} {w:6.3f} | {dm:+8.0f} | {do:+6.0f} | {dp:+.3f} | {sum(1 for x in d if x['win_to_loss']):3d}  {sum(1 for x in d if x['point_delta'] > 0.5):3d}")
        wsum_m += w * dm; wsum_p += w * dp; wtot += w
    if wtot:
        print(f"cluster-weighted (arena_meta weights, descriptive): margin delta {wsum_m / wtot:+.0f}, point delta {wsum_p / wtot:+.3f}")
    print()
    return by_c


def rules_arena(res, cfg, by):
    key = [k for k, c in res['comparisons'].items() if c.get('primary')][0]; C = res['comparisons'][key]; det = C['conditions']; by_c = by[key]
    cluster_of = {n: r['cluster'] for n, r in cfg['opponents'].items()}
    r1 = C['signal'] != 'negative'
    c23 = by_c.get('cluster2_hard_reacting_forks', []) + by_c.get('cluster3_modern_fast_climbers', [])
    r2 = all(sum(1 for x in det if x['opponent'] == o and x['win_to_loss']) <= sum(1 for x in det if x['opponent'] == o and x['point_delta'] > 0.5) for o in cfg['opponents'] if cluster_of[o] in ('cluster2_hard_reacting_forks', 'cluster3_modern_fast_climbers')) and (st.mean(x['margin_delta'] for x in c23) >= 0 if c23 else True)
    c1 = by_c.get('cluster1_elite_planners', []); r3 = (st.mean(x['margin_delta'] for x in c1) >= 0 and st.mean(x['own_cash_delta'] for x in c1) >= 0) if c1 else True
    c5 = by_c.get('cluster5_historical_anchors', []); r4 = (st.mean(x['margin_delta'] for x in c5) >= -1000) if c5 else True
    print(f"R1 primary signal not negative: {'PASS' if r1 else 'FAIL'} ({C['signal']})")
    print(f"R2 clusters 2+3: per-opponent W->L <= L->W and pooled margin delta >= 0: {'PASS' if r2 else 'FAIL'}")
    print(f"R3 cluster 1: margin delta >= 0 and own cash delta >= 0: {'PASS' if r3 else 'FAIL'}")
    print(f"R4 cluster 5 anchors: margin delta >= -1000: {'PASS' if r4 else 'FAIL'}")
    print('R5 cluster 4 fragile tapes: descriptive only for the body candidate (mirror overlay judged separately)')
    print('OVERALL (body rules R1-R4):', 'PASS' if (r1 and r2 and r3 and r4) else 'FAIL', "- promotion itself remains the owner's decision; blind 7240-7255 untouched")


def rules_panel(res, cfg, by):
    prim = {k: c for k, c in res['comparisons'].items() if c.get('primary')}
    cluster_of = {n: r.get('cluster', r['family']) for n, r in cfg['opponents'].items()}
    ok1 = all(c['signal'] != 'negative' for c in prim.values())
    print('L1 both primary comparisons (p002 on base19, p002 on MX2) not negative: ' + ('PASS' if ok1 else 'FAIL') + ' ' + str({k: c['signal'] for k, c in prim.items()}))
    ok2 = True; ok3 = True
    for k, c in prim.items():
        det = c['conditions']; rt = [o for o in cfg['opponents'] if cluster_of[o] == 'router_tschinkel']
        w = all(sum(1 for x in det if x['opponent'] == o and x['win_to_loss']) <= sum(1 for x in det if x['opponent'] == o and x['point_delta'] > 0.5) for o in rt); ok2 &= w
        own_all = c['mean_own_cash_delta']; own_rt = st.mean(x['own_cash_delta'] for x in det if x['opponent'] in rt) if rt else 0.0; ok3 &= own_all >= 0 and own_rt >= 0
        print(f"   {k}: router_tschinkel W->L<=L->W {w}; own cash delta pooled {own_all:+.0f}, router_tschinkel {own_rt:+.0f}")
    print('L2 router_tschinkel (the verified live build): per-opponent W->L <= L->W in both primaries: ' + ('PASS' if ok2 else 'FAIL'))
    print('L3 own cash delta >= 0 pooled and in router_tschinkel for both primaries (the cow must not cost cash): ' + ('PASS' if ok3 else 'FAIL'))
    for m in ('p002-cow1', 'p002-cow1-mx2'):
        if m in res['by_candidate']:
            t = res['by_candidate'][m].get('telemetry', {}); n = res['by_candidate'][m]['games']; b = t.get('p002_bought', 0)
            print(f"L4 trigger rate {m}: bought {b}/{n} = {100 * b / max(1, n):.0f}% (evaluations {t.get('p002_checks', 0)}, blocks cash {t.get('p002_block_cash', 0)} queue {t.get('p002_block_queue', 0)} tile {t.get('p002_block_tile', 0)} room {t.get('p002_block_room', 0)} payback {t.get('p002_block_payback', 0)})" + ('  -> condition rarely met: result inconclusive by design' if b < 0.2 * n else ''))
    print('OVERALL (L1-L3):', 'PASS' if (ok1 and ok2 and ok3) else 'FAIL', '- fieldbook lineage judged by the frozen diagnostic (lineage_report.py); expansion beyond one cow only after a favourable condition is confirmed; owner decides')


WORLD_FLAGS = {'yarn2': lambda s: s.count('YARN_STORE') >= 2, 'milk3': lambda s: sum(x in ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP') for x in s) >= 3,
               'berry3': lambda s: sum(x in ('BRUNCH_SPOT', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP', 'FARMERS_MARKET') for x in s) >= 3,
               'tomato3': lambda s: sum(x in ('PIZZA_SHOP', 'FARMERS_MARKET') for x in s) >= 3, 'pet2': lambda s: s.count('PET_CAFE') >= 2}
DETECT_KEYS = ('race_mirror', 'race_clone_turns', 'race_horizon_turns', 'race_lost_races', 'race_escalations', 'probe_matches', 'three_turn_calls', 'probe_four_turn_calls')


def load_jobs(out, man):
    rows = {}
    for j in man['jobs']:
        f = os.path.join(out, 'jobs', j['match_id'], 'result.json')
        if os.path.exists(f):
            r = json.load(open(f, encoding='utf-8')); rows[(r['model'], r['seed'], r['opponent_name'], r['candidate_seat'])] = r
    return rows


def rules_policy(res, cfg, by, out, man):
    """reports/o-policy-compare-plan-2026-09-19.ko.md: P1 primary positive, P2 breadth (>=6/8 families >= 0, none <= -0.25), P3 net flips > 0,
    P4 health + both seats >= 0, P5 cash reported only; plus worlds, big losses, detection flags and the relatives sensitivity."""
    rows = load_jobs(out, man); fams = sorted({o['family'] for o in cfg['opponents'].values()})
    rel_fam = {o['family'] for n, o in cfg['opponents'].items() if o.get('candidate_relation')}
    print('=== per-policy overview: games / point rate / wins-losses-ties / mean margin / bottom10% / worst / seat point rates / max decision s / invalid')
    for m, B in res['by_candidate'].items():
        seats = B['subgroups']['candidate_seat']; mx = max((r['candidate_timing']['max'] for r in rows.values() if r['model'] == m), default=0)
        inv = sum(1 for r in rows.values() if r['model'] == m and not r['valid'])
        print(f"{m:22s} {B['games']:4d}  {B['point_rate']:.3f}  {B['wins']}-{B['losses']}-{B['ties']}  {B['mean_margin']:+7.0f}  {B['bottom_10pct_mean']:+7.0f}  {B['worst_margin']:+7.0f}  s0 {seats['0']['point_rate']:.3f} s1 {seats['1']['point_rate']:.3f}  {mx:.3f}s  invalid {inv}")
    print('\n=== per-family point rate (policy rows) | paired point delta vs parent per primary')
    prim = {k: c for k, c in res['comparisons'].items() if c.get('primary')}
    hdr = 'family               ' + ' '.join(f'{m[:14]:>14s}' for m in res['by_candidate']) + ' | ' + ' '.join(f'{k.split("_vs_")[0][:14]:>14s}' for k in prim)
    print(hdr)
    for f in fams:
        cells = ' '.join(f"{res['by_candidate'][m]['subgroups']['opponent_family'][f]['point_rate']:14.3f}" for m in res['by_candidate'])
        deltas = ' '.join(f"{prim[k]['subgroups']['family'][f]['mean_point_delta']:+14.3f}" for k in prim)
        print(f"{f:20s}{'*' if f in rel_fam else ' '} {cells} | {deltas}")
    print('(* = family containing a same-author relative of one candidate)')
    verdicts = {}
    for k, C in prim.items():
        cand = k.split('_vs_')[0]; det = C['conditions']
        fam_d = {f: C['subgroups']['family'][f]['mean_point_delta'] for f in fams}
        p1 = C['signal'] == 'positive'
        p2 = sum(1 for v in fam_d.values() if v >= 0) >= 6 and min(fam_d.values()) > -0.25
        l2w = sum(1 for x in det if x['point_delta'] > 0.5); w2l = C['win_to_loss']; p3 = l2w - w2l > 0
        seat_d = {s: C['subgroups']['seat'][s]['mean_point_delta'] for s in ('0', '1')}
        inv = sum(1 for r in rows.values() if r['model'] == cand and (not r['valid'] or r['health_failures']))
        p4 = inv == 0 and all(v >= 0 for v in seat_d.values())
        nonrel = [x for x in det if x['family'] not in rel_fam]
        print(f"\n--- {k}: P1 primary positive: {'PASS' if p1 else 'FAIL'} ({C['signal']}, family-weighted point delta {C['family_weighted_point_delta']:+.3f}, CI {C['approximate_bootstrap_ci']})")
        print(f"    P2 breadth: families >= 0: {sum(1 for v in fam_d.values() if v >= 0)}/8, min family delta {min(fam_d.values()):+.3f} ({min(fam_d, key=fam_d.get)}) -> {'PASS' if p2 else 'FAIL'}")
        print(f"    P3 flips: L->W {l2w} - W->L {w2l} = {l2w - w2l:+d} -> {'PASS' if p3 else 'FAIL'}")
        print(f"    P4 health/seats: invalid {inv}, seat deltas {seat_d} -> {'PASS' if p4 else 'FAIL'}")
        print(f"    P5 (reported only): own cash delta {C['mean_own_cash_delta']:+.0f}, margin delta {C['mean_margin_delta']:+.0f}")
        print(f"    sensitivity without relative families {sorted(rel_fam)}: point delta {st.mean(x['point_delta'] for x in nonrel):+.3f}, margin delta {st.mean(x['margin_delta'] for x in nonrel):+.0f} (n={len(nonrel)})")
        verdicts[cand] = p1 and p2 and p3 and p4
    parent = [c for c in cfg['comparisons'] if c['primary']][0]['parent']
    print(f'\n=== worlds (flags from the final shop list of the PARENT game of each cell, {parent}; shops are world-RNG + action dependent, so a seed is not one world): flag n_cells | per-policy point rate | paired point delta per primary')
    shops_of = {(sd, o, t): r['shops'] for (m, sd, o, t), r in rows.items() if m == parent}
    for flag, fn in list(WORLD_FLAGS.items()) + [('none_of_above', lambda s: not any(g(s) for g in WORLD_FLAGS.values()))]:
        sel = {c for c, sh in shops_of.items() if fn(sh)}
        if not sel:
            print(f"{flag:14s} 0"); continue
        pr = ' '.join(f"{m[:14]:>10s} {st.mean(1.0 if r['outcome'] == 'win' else .5 if r['outcome'] == 'tie' else 0.0 for (mm, sd, o, t), r in rows.items() if mm == m and (sd, o, t) in sel):.3f}" for m in res['by_candidate'])
        pd = ' '.join(f"{k.split('_vs_')[0][:14]:>14s} {st.mean(x['point_delta'] for x in prim[k]['conditions'] if (x['seed'], x['opponent'], x['seat']) in sel):+.3f}" for k in prim)
        print(f"{flag:14s} {len(sel):3d} | {pr} | {pd}")
    print('\n=== big losses (margin < -10000) per policy: count, by family')
    for m in res['by_candidate']:
        big = [r for r in rows.values() if r['model'] == m and r['margin'] < -10000]
        byf = {}
        for r in big: byf[r['opponent_family']] = byf.get(r['opponent_family'], 0) + 1
        print(f"{m:22s} {len(big):3d}  {dict(sorted(byf.items()))}")
    print('\n=== clone/mirror detection flags (candidate or opponent telemetry key > 0): games per policy x opponent')
    flags = {}
    for r in rows.values():
        hit = [k for role in ('candidate_telemetry', 'opponent_telemetry') for k, v in r.get(role, {}).items() if k in DETECT_KEYS and isinstance(v, (int, float)) and v > 0]
        if hit: flags.setdefault((r['model'], r['opponent_name']), []).append(sorted(set(hit)))
    for (m, o), lst in sorted(flags.items()): print(f"{m:22s} {o:27s} {len(lst):3d} games  keys {sorted({k for h in lst for k in h})}")
    if not flags: print('none')
    dec = [c for c, ok in verdicts.items() if ok]
    print('\nDECISION (plan 4): ' + ('(a) broadly superior on development: ' + ', '.join(dec) + ' -> run confirm' if dec else '(b)/(c): no policy passes P1-P4 -> check the split condition (family/world delta >= +0.25 and <= -0.25) before keeping base19'))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('config'); ap.add_argument('--rules', choices=['arena', 'panel', 'policy'], default='arena')
    a = ap.parse_args(); out, cfg_path = a.out, a.config
    cfg = json.load(open(cfg_path, encoding='utf-8-sig')); res = json.load(open(os.path.join(out, 'results.json'), encoding='utf-8')); man = json.load(open(os.path.join(out, 'manifest.json'), encoding='utf-8'))
    print(f"campaign {out}  stage {res['stage']}  completed {res['completed_jobs']}/{man['expected_jobs']}  status {res['status']}  contract {res.get('contract_sha256', '')[:12]}  alpha {cfg['stages'][res['stage']]['alpha']}")
    by = {k: comparison_block(res, cfg, k, C) for k, C in res['comparisons'].items()}
    if a.rules == 'policy': rules_policy(res, cfg, by, out, man)
    else: (rules_arena if a.rules == 'arena' else rules_panel)(res, cfg, by)


if __name__ == '__main__':
    main()
