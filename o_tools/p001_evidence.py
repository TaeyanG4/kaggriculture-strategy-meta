"""Consolidate the EXISTING MX2 (p001) evidence into one promotion-review table. No games are run.
Sources: o_results/proxy/eval_<label>.json (pinned reacting games: seed, seat_b, a, b), o_results/mx/eval_<label>.json
(mx_eval: per-product revenue/units, both seats), o_results/elite_pool/eval_<label>.json (frozen replays: team, episode).
Usage: python o_tools/p001_evidence.py [--md reports/o-p001-mx2-evidence-2026-09-18.ko.md]"""
import argparse, collections, json, os, statistics as st
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(rel):
    p = os.path.join(ROOT, rel)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None


def se(v):
    return st.stdev(v) / len(v) ** 0.5 if len(v) > 1 else 0.0


def pair_proxy(base_lab, cand_lab):
    """Pinned reacting eval: b = our cash, a = opponent cash; paired on (seed, seat_b)."""
    B = load(f'o_results/proxy/eval_{base_lab}.json'); C = load(f'o_results/proxy/eval_{cand_lab}.json')
    if not B or not C:
        return None
    b = {(x['seed'], x['seat_b']): x for x in B}; c = {(x['seed'], x['seat_b']): x for x in C}
    keys = sorted(k for k in b if k in c)
    do = [c[k]['b'] - b[k]['b'] for k in keys]; dopp = [c[k]['a'] - b[k]['a'] for k in keys]; dm = [x - y for x, y in zip(do, dopp)]
    wb = [b[k]['b'] > b[k]['a'] for k in keys]; wc = [c[k]['b'] > c[k]['a'] for k in keys]
    return dict(n=len(keys), seeds=f"{min(k[0] for k in keys)}-{max(k[0] for k in keys)}", seats=sorted({k[1] for k in keys}), own=st.mean(do), opp=st.mean(dopp), margin=st.mean(dm), se=se(dm),
                wins_base=sum(wb), wins_cand=sum(wc), w2l=sum(1 for x, y in zip(wb, wc) if x and not y), l2w=sum(1 for x, y in zip(wb, wc) if (not x) and y), worse=sum(1 for x in dm if x < -500), better=sum(1 for x in dm if x > 500))


def pair_mx(base_lab, cand_lab):
    B = load(f'o_results/mx/eval_{base_lab}.json'); C = load(f'o_results/mx/eval_{cand_lab}.json')
    if not B or not C:
        return None
    b = {(x['opp'], x['seed_or_episode'], x['seat_b']): x for x in B}; c = {(x['opp'], x['seed_or_episode'], x['seat_b']): x for x in C}
    out = {}
    for opp in sorted({k[0] for k in b}):
        keys = sorted(k for k in b if k in c and k[0] == opp)
        if not keys:
            continue
        do = [c[k]['our_cash'] - b[k]['our_cash'] for k in keys]; dopp = [c[k]['their_cash'] - b[k]['their_cash'] for k in keys]; dm = [x - y for x, y in zip(do, dopp)]
        wb = [b[k]['our_cash'] > b[k]['their_cash'] for k in keys]; wc = [c[k]['our_cash'] > c[k]['their_cash'] for k in keys]
        prod = {}
        for it in ('STRAWBERRY', 'MILK', 'WOOL'):
            ub = st.mean(b[k]['units'].get(it, 0) for k in keys); uc = st.mean(c[k]['units'].get(it, 0) for k in keys)
            pb = sum(b[k]['rev'].get(it, 0) for k in keys) / max(1e-9, sum(b[k]['units'].get(it, 0) for k in keys)); pc = sum(c[k]['rev'].get(it, 0) for k in keys) / max(1e-9, sum(c[k]['units'].get(it, 0) for k in keys))
            ob = sum(b[k]['opp_rev'].get(it, 0) for k in keys) / max(1e-9, sum(b[k]['opp_units'].get(it, 0) for k in keys)); oc = sum(c[k]['opp_rev'].get(it, 0) for k in keys) / max(1e-9, sum(c[k]['opp_units'].get(it, 0) for k in keys))
            prod[it] = dict(units=(ub, uc), price=(pb, pc), opp_price=(ob, oc))
        out[opp] = dict(n=len(keys), kind='frozen' if opp in ('Unknown_Mother-Goose', 'Majkel1337') else 'reacting', own=st.mean(do), opp=st.mean(dopp), margin=st.mean(dm), se=se(dm), wins_base=sum(wb), wins_cand=sum(wc),
                        w2l=sum(1 for x, y in zip(wb, wc) if x and not y), l2w=sum(1 for x, y in zip(wb, wc) if (not x) and y), worse=sum(1 for x in dm if x < -500), better=sum(1 for x in dm if x > 500), prod=prod)
    return out


def pair_elite(base_lab, cand_lab, cluster_fn=None):
    B = load(f'o_results/elite_pool/eval_{base_lab}.json'); C = load(f'o_results/elite_pool/eval_{cand_lab}.json')
    if not B or not C:
        return None
    b = {(x['team'], x['episode']): x for x in B}; c = {(x['team'], x['episode']): x for x in C}
    keys = sorted(k for k in b if k in c)
    do = [c[k]['our_cash'] - b[k]['our_cash'] for k in keys]; dopp = [c[k]['their_cash'] - b[k]['their_cash'] for k in keys]; dm = [x - y for x, y in zip(do, dopp)]
    wb = [b[k]['our_cash'] > b[k]['their_cash'] for k in keys]; wc = [c[k]['our_cash'] > c[k]['their_cash'] for k in keys]
    res = dict(n=len(keys), own=st.mean(do), opp=st.mean(dopp), margin=st.mean(dm), se=se(dm), wins_base=sum(wb), wins_cand=sum(wc), w2l=sum(1 for x, y in zip(wb, wc) if x and not y), l2w=sum(1 for x, y in zip(wb, wc) if (not x) and y), worse=sum(1 for x in dm if x < -500), better=sum(1 for x in dm if x > 500))
    if cluster_fn:
        groups = collections.defaultdict(list)
        for k, d in zip(keys, dm):
            groups[cluster_fn(k)].append(d)
        means = [st.mean(v) for v in groups.values()]
        res.update(clusters=len(groups), cluster_mean=st.mean(means), cluster_se=se(means), cluster_sizes=sorted(collections.Counter(len(v) for v in groups.values()).items()))
    return res


def live_pool_meta():
    """Rival identity for the frozen current-live pool: team name per episode and the sub-id map from the live episode lists."""
    meta = {}
    for sub in ('56312878', '56319267'):
        d = load(f'o_results/live_episodes_{sub}.json')
        if not d:
            continue
        for e in d['episodes']:
            if e.get('state') != 'COMPLETED':
                continue
            ag = e['agents']; op = [a for a in ag if a.get('submissionId') != int(sub)]
            if op:
                meta[str(e['id'])] = dict(our_sub=sub, opp_sub=op[0].get('submissionId'), opp_team=op[0].get('teamId'), opp_rating=op[0].get('initialScore'))
    return meta


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--md', default='')
    a = ap.parse_args()
    L = []
    P = L.append
    P('# p001_mx2 (MX2) promotion-review evidence - existing results only (2026-09-18)')
    P('')
    P('Candidate: `agent/p001_mx2.py` = base19 body + `mx2` default-on (manifest `state/o_dev/p001_mx2.manifest.json`). Champion stays base19.')
    P('Two parameter states appear below: **cur** = the frozen parameters (mx2_tc 1, mx2_same 0.5, mx2_decouple 0); **v0d** = predecessor (tc 0, same 0, decouple 0) used for the o227/V46/K0006 3-set runs (16:48-16:54). On the sel screen `mx2g_v0d` reproduced v0d exactly and `mx2g_nodec` (= cur) differed by <= 0.2k own; the cur parameters were NOT re-run on hold/fresh in this task.')
    P('')
    P('## A. Reacting opponents, pinned worlds (proxy_eval; 16 seeds x 2 seats per set; sel 7000-7015 = MX2 tuning set, hold 7016-7031, fresh 7032-7047)')
    P('| opponent | set | params | n | own d | opp d | paired margin d (se) | wins base->cand | W->L / L->W | worse/better (>500) |')
    P('|---|---|---|---|---|---|---|---|---|---|')
    rows = [('o227 tape', 'sel', 'v0d', 'base19_sel', 'mx2d_all_sel'), ('o227 tape', 'hold', 'v0d', 'base19_hold', 'mx2d_all_hold'), ('o227 tape', 'fresh', 'v0d', 'base19_fresh', 'mx2d_all_fresh'), ('o227 tape', 'sel', 'cur', 'base19_sel', 'mx2g_nodec_sel'),
            ('V46', 'sel', 'v0d', 'base19_vs_v46_sel', 'mx2d_all_vs_v46_sel'), ('V46', 'hold', 'v0d', 'base19_vs_v46_hold', 'mx2d_all_vs_v46_hold'), ('V46', 'fresh', 'v0d', 'base19_vs_v46_fresh', 'mx2d_all_vs_v46_fresh'), ('V46', 'sel', 'cur', 'base19_vs_v46_sel', 'mx2g_nodec_vs_v46_sel'),
            ('K0006', 'sel', 'v0d', 'base19_vs_k0006_sel', 'mx2d_all_vs_k0006_sel'), ('K0006', 'hold', 'v0d', 'base19_vs_k0006_hold', 'mx2d_all_vs_k0006_hold'), ('K0006', 'fresh', 'v0d', 'base19_vs_k0006_fresh', 'mx2d_all_vs_k0006_fresh'), ('K0006', 'sel', 'cur', 'base19_vs_k0006_sel', 'mx2g_nodec_vs_k0006_sel'),
            ('v37 (exact0)', 'sel', 'v0d', 'base19_vs_public_v37_mor_sel', 'mx2d_all_vs_v37_sel'), ('v37 (exact0)', 'sel', 'cur', 'base19_vs_public_v37_mor_sel', 'mx2g_nodec_vs_v37_sel')]
    pooled = collections.defaultdict(list)
    for opp, s_, par, bl, cl in rows:
        r = pair_proxy(bl, cl)
        if not r:
            P(f'| {opp} | {s_} | {par} | - | missing {cl} | | | | | |'); continue
        P(f"| {opp} | {s_} | {par} | {r['n']} | {r['own']:+.0f} | {r['opp']:+.0f} | {r['margin']:+.0f} ({r['se']:.0f}) | {r['wins_base']}->{r['wins_cand']} | {r['w2l']} / {r['l2w']} | {r['worse']}/{r['better']} |")
        if par == 'v0d':
            pooled[opp].append(r)
    P('')
    for opp, rs in pooled.items():
        n = sum(r['n'] for r in rs)
        P(f"- {opp} pooled (v0d, {n} games): own {sum(r['own'] * r['n'] for r in rs) / n:+.0f}, margin {sum(r['margin'] * r['n'] for r in rs) / n:+.0f}, wins {sum(r['wins_base'] for r in rs)}->{sum(r['wins_cand'] for r in rs)}, W->L {sum(r['w2l'] for r in rs)}, L->W {sum(r['l2w'] for r in rs)}")
    P('')
    P('## B. mx_eval panel (cur params, 17:24-17:26): v46/k0006/v48 reacting (32 = 16 seeds x 2 seats) + frozen MG/Majkel (40 replays each, ONE recorded submission per team)')
    mx = pair_mx('base19', 'mx2_all')
    P('| opponent | kind | n | our rev d | opp rev d | paired margin d (se) | wins base->cand | W->L / L->W | worse/better |')
    P('|---|---|---|---|---|---|---|---|---|')
    for opp, r in (mx or {}).items():
        P(f"| {opp} | {r['kind']} | {r['n']} | {r['own']:+.0f} | {r['opp']:+.0f} | {r['margin']:+.0f} ({r['se']:.0f}) | {r['wins_base']}->{r['wins_cand']} | {r['w2l']} / {r['l2w']} | {r['worse']}/{r['better']} |")
    P('')
    P('Per-product realised $/unit (base -> cand), our units per game and the rival\'s $/unit:')
    P('| opponent | STRAWBERRY ours $/u | units | rival $/u | MILK ours $/u | units | rival $/u | WOOL ours $/u | units | rival $/u |')
    P('|---|---|---|---|---|---|---|---|---|---|')
    for opp, r in (mx or {}).items():
        cells = []
        for it in ('STRAWBERRY', 'MILK', 'WOOL'):
            p = r['prod'][it]; cells += [f"{p['price'][0]:.1f}->{p['price'][1]:.1f}", f"{p['units'][0]:.0f}->{p['units'][1]:.0f}", f"{p['opp_price'][0]:.1f}->{p['opp_price'][1]:.1f}"]
        P(f"| {opp} | " + ' | '.join(cells) + ' |')
    P('')
    P('## C. Frozen elite replays (elite_pool, v0d params, 40 replays each of one recorded submission; rivals do not react)')
    r = pair_elite('base19', 'mx2d_all', cluster_fn=lambda k: k[0])
    if r:
        P(f"- MG+Majkel pooled n={r['n']}: own {r['own']:+.0f}, opp {r['opp']:+.0f}, margin {r['margin']:+.0f} (game se {r['se']:.0f}); by team (n_teams={r['clusters']}): mean of team means {r['cluster_mean']:+.0f} (se over 2 teams {r['cluster_se']:.0f}); wins {r['wins_base']}->{r['wins_cand']}, W->L {r['w2l']}, L->W {r['l2w']}, worse/better {r['worse']}/{r['better']}")
    B = load('o_results/elite_pool/eval_base19.json'); C = load('o_results/elite_pool/eval_mx2d_all.json')
    if B and C:
        for team in ('Unknown_Mother-Goose', 'Majkel1337'):
            b = {x['episode']: x for x in B if x['team'] == team}; c = {x['episode']: x for x in C if x['team'] == team}
            ks = [k for k in b if k in c]; dm = [(c[k]['our_cash'] - c[k]['their_cash']) - (b[k]['our_cash'] - b[k]['their_cash']) for k in ks]; do = [c[k]['our_cash'] - b[k]['our_cash'] for k in ks]
            P(f"  - {team}: n={len(ks)} own {st.mean(do):+.0f} margin {st.mean(dm):+.0f} (se {se(dm):.0f}) wins {sum(b[k]['our_cash'] > b[k]['their_cash'] for k in ks)}->{sum(c[k]['our_cash'] > c[k]['their_cash'] for k in ks)}")
    P('')
    P('## D. Frozen current-live pool (elite_pool --us Taeyang, cur params, 18:57-18:58): the rivals of our own live games, recorded actions replayed in their worlds')
    meta = live_pool_meta()
    r = pair_elite('lb_base19', 'lb_mx2', cluster_fn=lambda k: str((meta.get(k[1]) or {}).get('opp_team') or ('self' if k[1] == '110284146' else 'unknown')))
    if r:
        P(f"- all games n={r['n']}: own {r['own']:+.0f}, opp {r['opp']:+.0f}, margin {r['margin']:+.0f} (game se {r['se']:.0f}); by rival team n_teams={r['clusters']}: mean of team means {r['cluster_mean']:+.0f} (team-cluster se {r['cluster_se']:.0f}); wins {r['wins_base']}->{r['wins_cand']}, W->L {r['w2l']}, L->W {r['l2w']}, worse/better {r['worse']}/{r['better']}; team sizes {r['cluster_sizes']}")
        B = load('o_results/elite_pool/eval_lb_base19.json'); C = load('o_results/elite_pool/eval_lb_mx2.json')
        b = {x['episode']: x for x in B}; c = {x['episode']: x for x in C}
        ks = [k for k in b if k in c and k != '110284146']
        dm = [(c[k]['our_cash'] - c[k]['their_cash']) - (b[k]['our_cash'] - b[k]['their_cash']) for k in ks]
        P(f"- excluding the self-match 110284146 (both seats Taeyang; the frozen side is our other submission): n={len(ks)} margin {st.mean(dm):+.0f} (se {se(dm):.0f}), wins {sum(b[k]['our_cash'] > b[k]['their_cash'] for k in ks)}->{sum(c[k]['our_cash'] > c[k]['their_cash'] for k in ks)}")
        subs = collections.Counter((meta.get(k) or {}).get('our_sub', 'unknown') for k in b)
        P(f"- composition by OUR submission: {dict(subs)} (base17 = 56312878, base19 = 56319267); live episode lists: base17 59 completed (55 replays present, 4 never downloaded), base19 62 completed (62 replays) -> 117 of 121 listed; live win record of the same lists: base17 37/58, base19 35/61 (games with both rewards).")
        opp_subs = collections.Counter((meta.get(k) or {}).get('opp_sub') for k in b)
        P(f"- distinct rival submissions in the pool: {len(opp_subs)}; most repeated: {opp_subs.most_common(5)}")
        rt = [(meta.get(k) or {}).get('opp_rating') for k in b if (meta.get(k) or {}).get('opp_rating')]
        P(f"- rival rating at match time: median {st.median(rt):.0f}, IQR {sorted(rt)[len(rt) // 4]:.0f}-{sorted(rt)[3 * len(rt) // 4]:.0f} (new submissions; the same builds also sit at 2400-2700 in the tape-era live_all sample)")
    P('')
    P('## E. Scope of the conclusions (recorded as agreed)')
    P('- Replay audit: in the 62 audited base19 (56319267) live games, local actions and final cash matched the server record step by step. Nothing is claimed about other submissions.')
    P('- Historical comparison: on the checked V46/K0006 (pinned sel worlds) the tapes o227/o239 showed no economic advantage (12/32, 10/32; base19 14/32, 14/32); against v37 the tape has a large tactical advantage (32/32). The population-wide statement "all of the tape\'s live edge is exact0" is NOT asserted.')
    P('- Frozen pools fix the rival\'s recorded actions; a frozen mean close to the live mean does not establish that the rival is non-reacting. Frozen deltas measure our change against fixed rival behaviour only.')
    P('- The correlation between rival herd size and our margin (-0.47 over 117 live games) is a structural lead, not a causal conclusion about herd size or labour throughput.')
    P('')
    P('## Appendix F. Mirror overlay and MX2+mirror (kept apart from the MX2 body evidence)')
    P('| candidate | pool | n | own d | opp d | paired margin d (se) | wins base->cand | W->L / L->W | worse/better |')
    P('|---|---|---|---|---|---|---|---|---|')
    for name, args in (('mirror (tA_m6r)', ('base19_sel', 'tA_m6r_sel')), ('mirror', ('base19_hold', 'tA_m6r_hold')), ('mirror', ('base19_fresh', 'tA_m6r_fresh')),
                       ('mirror', ('base19_vs_v46_sel', 'tA_m6r_vs_v46_sel')), ('mirror', ('base19_vs_v46_hold', 'tA_m6r_vs_v46_hold')), ('mirror', ('base19_vs_v46_fresh', 'tA_m6r_vs_v46_fresh')),
                       ('mirror', ('base19_vs_k0006_sel', 'tA_m6r_vs_k0006_sel')), ('mirror', ('base19_vs_k0006_hold', 'tA_m6r_vs_k0006_hold')), ('mirror', ('base19_vs_k0006_fresh', 'tA_m6r_vs_k0006_fresh')),
                       ('mirror', ('base19_vs_public_v37_mor_sel', 'tA_m6r_vs_v37_sel')), ('mirror', ('base19_vs_public_v37_mor_hold', 'tA_m6r_vs_v37_hold')), ('mirror', ('base19_vs_public_v37_mor_fresh', 'tA_m6r_vs_v37_fresh')),
                       ('mirror (sw_mirror=1)', ('base19_vs_public_v37_mor_sel', 'mirror1_vs_v37_sel'))):
        r = pair_proxy(*args)
        if r:
            P(f"| {name} | {args[1]} | {r['n']} | {r['own']:+.0f} | {r['opp']:+.0f} | {r['margin']:+.0f} ({r['se']:.0f}) | {r['wins_base']}->{r['wins_cand']} | {r['w2l']} / {r['l2w']} | {r['worse']}/{r['better']} |")
    for name, lab in (('mirror', 'tA_m6r'), ('mirror', 'lb_mirror'), ('mirror+MX2', 'lb_both')):
        base = 'lb_base19' if lab.startswith('lb_') else 'base19'
        r = pair_elite(base, lab)
        if r:
            P(f"| {name} | elite_pool {lab} vs {base} | {r['n']} | {r['own']:+.0f} | {r['opp']:+.0f} | {r['margin']:+.0f} ({r['se']:.0f}) | {r['wins_base']}->{r['wins_cand']} | {r['w2l']} / {r['l2w']} | {r['worse']}/{r['better']} |")
    pool = load('o_tools/diverse_pool.json') or {}
    rows49 = [(name, pair_proxy(f'base19_dp_vs_{name}', f'tA_m6r_vs_{name}')) for name in pool]
    rows49 = [(n_, r) for n_, r in rows49 if r]
    if rows49:
        P(f"- mirror vs the 49-agent diverse pool (4 seeds x 2 seats, 8 games per agent): agents {len(rows49)}, own {st.mean(r['own'] for _, r in rows49):+.0f}, margin {st.mean(r['margin'] for _, r in rows49):+.0f} (agent-cluster se {se([r['margin'] for _, r in rows49]):.0f}), wins {sum(r['wins_base'] for _, r in rows49)}->{sum(r['wins_cand'] for _, r in rows49)}, W->L {sum(r['w2l'] for _, r in rows49)}, L->W {sum(r['l2w'] for _, r in rows49)}, agents margin < -1k: {sum(1 for _, r in rows49 if r['margin'] < -1000)}, > +1k: {sum(1 for _, r in rows49 if r['margin'] > 1000)}")
    if a.md:
        open(os.path.join(ROOT, a.md), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
