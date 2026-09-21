"""p002 (one conditional extra cow) readout from EXISTING result files - no games are run.
(a) mx_eval pairs:  python o_tools/p002_report.py --mx base19 p002_cow1 [--mx p001_mx2 p002_cow1_mx2]
    per opponent and pooled: attempts (telemetry p002_bought = order emitted) vs CONFIRMED purchases (candidate bought >= parent + 1 cow;
    the frozen p002 sets cow1_done on emission, so a silently failed BUY would still read as an attempt), buy days, first block reasons, and the
    paired deltas the owner asked for: own cash, rival cash, paired margin, W->L / L->W, biggest losses, and the ledger split into
    milk / fertiliser sales, cow purchase, feed spend (the candidate's WHOLE feed bill, not the cow's direct feed), hires, other products, other
    buys, rival revenue. Everything is also split into confirmed-purchase / attempted-unconfirmed / no-attempt games; no-attempt games must be
    identical to the parent - any nonzero delta there is listed as a behaviour difference to explain before crediting "the cow".
    Development cases (the two smoke worlds analysed in reports/o-p002-smoke-audit-2026-09-18.ko.md) are flagged and totals are also given without them.
(b) canonical campaign: python o_tools/p002_report.py --campaign state/agent_experiments/<out> --parent base19-planner --cand p002-cow1
    same statistics from jobs/*/result.json (candidate_telemetry + checkpoint COW counts for confirmation).
Gates are set-mean based (family-weighted CI, pooled own delta); single-game losses are reported, not gated."""
import argparse, collections, glob, json, os, statistics as st
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MX = os.path.join(ROOT, 'o_results', 'mx')
DEV_CASES = {('v46', '7000', 0), ('v46', '7001', 1)}   # smoke worlds already used for the ledger audit: development evidence, not confirmation


def mean(v):
    return st.mean(v) if v else 0.0


def se(v):
    return st.stdev(v) / len(v) ** 0.5 if len(v) > 1 else 0.0


def cows_bought(r):
    return int(round((r.get('buy') or {}).get('ANIMAL:COW', 0.0) / 400.0))


def ledger(B, C, ks, title):
    """Paired deltas (cand - base) over keys ks: performance first, then the ledger."""
    if not ks:
        print(f'{title}: no games'); return
    g = lambda r, f, k: (r.get(f) or {}).get(k, 0.0)
    d = lambda f, k: mean([g(C[x], f, k) - g(B[x], f, k) for x in ks])
    own = [C[x]['our_cash'] - B[x]['our_cash'] for x in ks]; opp = [C[x]['their_cash'] - B[x]['their_cash'] for x in ks]; dm = [a - b for a, b in zip(own, opp)]
    w0 = [B[x]['our_cash'] > B[x]['their_cash'] for x in ks]; w1 = [C[x]['our_cash'] > C[x]['their_cash'] for x in ks]
    print(f"{title:44s} n={len(ks):3d} | own {mean(own):+6.0f} (se {se(own):3.0f}) rival {mean(opp):+6.0f} margin {mean(dm):+6.0f} (se {se(dm):3.0f}) | wins {sum(w0)}->{sum(w1)} W->L {sum(1 for a, b in zip(w0, w1) if a and not b)} L->W {sum(1 for a, b in zip(w0, w1) if b and not a)} | games own<-500 {sum(1 for x in own if x < -500)} margin<-500 {sum(1 for x in dm if x < -500)}")
    milk = d('rev', 'MILK'); fert = d('rev', 'FERTILIZER'); cow = d('buy', 'ANIMAL:COW'); feed = d('buy', 'PRODUCT:WHEAT'); hire = mean([C[x]['other_spend'] - B[x]['other_spend'] for x in ks])
    other_rev = mean([sum(v for k, v in C[x]['rev'].items() if k not in ('MILK', 'FERTILIZER')) - sum(v for k, v in B[x]['rev'].items() if k not in ('MILK', 'FERTILIZER')) for x in ks])
    other_buy = mean([sum(v for k, v in C[x]['buy'].items() if k not in ('ANIMAL:COW', 'PRODUCT:WHEAT')) - sum(v for k, v in B[x]['buy'].items() if k not in ('ANIMAL:COW', 'PRODUCT:WHEAT')) for x in ks])
    print(f"{'':44s}   ledger: milk sales ${milk:+5.0f} ({d('units', 'MILK'):+4.1f}u, ${(sum(g(C[x],'rev','MILK') for x in ks)/max(1,sum(g(C[x],'units','MILK') for x in ks))):.0f}/u cand vs ${(sum(g(B[x],'rev','MILK') for x in ks)/max(1,sum(g(B[x],'units','MILK') for x in ks))):.0f}/u base) fert sales ${fert:+5.0f} ({d('units', 'FERTILIZER'):+4.1f}u) fert bought ${d('buy', 'PRODUCT:FERTILIZER'):+4.0f} | cow purchases ${cow:+4.0f} whole feed bill ${feed:+5.0f} hire+land ${hire:+4.0f} | other products ${other_rev:+5.0f} other buys ${other_buy:+4.0f} | rival revenue {mean([sum(C[x]['opp_rev'].values()) - sum(B[x]['opp_rev'].values()) for x in ks]):+5.0f}")
    prods = collections.Counter()
    for x in ks:
        for k in set(C[x]['rev']) | set(B[x]['rev']):
            prods[k] += g(C[x], 'rev', k) - g(B[x], 'rev', k)
    print(f"{'':44s}   per-product $ delta: " + ' '.join(f"{k[:5]} {v / len(ks):+5.0f}" for k, v in sorted(prods.items(), key=lambda kv: kv[0])))


def mx(base, cand):
    load = lambda l: {(x['opp'], str(x['seed_or_episode']), x['seat_b']): x for x in json.load(open(os.path.join(MX, f'eval_{l}.json')))}
    B, C = load(base), load(cand); keys = sorted(k for k in B if k in C)
    print(f'=== {cand} vs {base} (mx_eval, paired n={len(keys)}; development cases in the set: {sorted(k for k in keys if k in DEV_CASES)})')
    tel = {k: (C[k].get('telemetry') or {}) for k in keys}
    attempt = [k for k in keys if tel[k].get('p002_bought')]
    confirmed = [k for k in attempt if cows_bought(C[k]) >= cows_bought(B[k]) + 1]
    unconfirmed = [k for k in attempt if k not in set(confirmed)]
    none = [k for k in keys if k not in set(attempt)]
    print(f"attempts (order emitted) {len(attempt)}/{len(keys)} = {100 * len(attempt) / max(1, len(keys)):.0f}% | CONFIRMED (cand bought >= parent+1 cow) {len(confirmed)} | attempted but not confirmed (failed BUY or the plan bought one fewer later) {len(unconfirmed)} | no attempt {len(none)}")
    print(f"buy day histogram {dict(sorted(collections.Counter(int(tel[k]['p002_buy_day']) for k in attempt).items()))}  buy hour median {st.median([tel[k]['p002_buy_hour'] for k in attempt]) if attempt else '-'}")
    blocks = collections.Counter()
    for k in keys:
        for kk, v in tel[k].items():
            if kk.startswith('p002_block_'):
                blocks[kk[11:]] += v
    checks = sum(tel[k].get('p002_checks', 0) for k in keys)
    print(f"evaluations {checks} (per game {checks / max(1, len(keys)):.0f}); first-block reasons: " + ', '.join(f"{k} {100 * v / max(1, checks):.0f}%" for k, v in blocks.most_common()))
    if attempt:
        print(f"attempt games: estimated value mean {mean([tel[k]['p002_value'] for k in attempt]):.0f}, p_final mean {mean([tel[k]['p002_p_final'] for k in attempt]):.0f}, cash after {mean([tel[k]['p002_cash_after'] for k in attempt]):.0f}")
    for o in dict.fromkeys(k[0] for k in keys):
        ks = [k for k in keys if k[0] == o]
        print(f"  {o:14s} attempts {sum(1 for k in ks if k in set(attempt)):2d} confirmed {sum(1 for k in ks if k in set(confirmed)):2d} / {len(ks):2d}  buy days {sorted(int(tel[k]['p002_buy_day']) for k in ks if k in set(attempt))[:12]}")
    print()
    ledger(B, C, keys, 'ALL games (main verdict basis)')
    ledger(B, C, [k for k in keys if k not in DEV_CASES], 'ALL games minus development cases')
    ledger(B, C, confirmed, 'confirmed purchase (mechanism analysis)')
    ledger(B, C, unconfirmed, 'attempted, not confirmed')
    ledger(B, C, none, 'no attempt (must equal the parent)')
    diff = [k for k in none if abs(C[k]['our_cash'] - B[k]['our_cash']) > 0.5 or abs(C[k]['their_cash'] - B[k]['their_cash']) > 0.5]
    print(f"   no-attempt games whose finals differ from the parent: {len(diff)}" + (f" -> explain before crediting the cow: {diff[:8]}" if diff else ' (behaviour identical, as required)'))
    print()
    for o in dict.fromkeys(k[0] for k in keys):
        ledger(B, C, [k for k in keys if k[0] == o], f'  opponent {o}')
    print()
    worst = sorted(keys, key=lambda k: (C[k]['our_cash'] - C[k]['their_cash']) - (B[k]['our_cash'] - B[k]['their_cash']))[:6]
    print('biggest paired-margin losses (opp, seed, seat): ' + '; '.join(f"{k[0]}/{k[1]}/s{k[2]} margin {((C[k]['our_cash'] - C[k]['their_cash']) - (B[k]['our_cash'] - B[k]['their_cash'])):+.0f} own {C[k]['our_cash'] - B[k]['our_cash']:+.0f} {'attempt' if k in set(attempt) else 'no-attempt'}{' DEV' if k in DEV_CASES else ''}" for k in worst))
    worst_own = sorted(keys, key=lambda k: C[k]['our_cash'] - B[k]['our_cash'])[:6]
    print('biggest own-cash losses: ' + '; '.join(f"{k[0]}/{k[1]}/s{k[2]} own {C[k]['our_cash'] - B[k]['our_cash']:+.0f} margin {((C[k]['our_cash'] - C[k]['their_cash']) - (B[k]['our_cash'] - B[k]['their_cash'])):+.0f}" for k in worst_own))
    print('note: own/margin gates are set means; single-game losses above are context, not gate failures. Feed/fertiliser deltas are whole-farm ledger changes, not the cow\'s direct costs.')
    print()


def campaign(out, parent, cand):
    rows = []
    for p in glob.glob(os.path.join(out, 'jobs', '*', 'result.json')):
        rows.append(json.load(open(p, encoding='utf-8')))
    idx = {(r['model'], r['seed'], r['opponent_name'], r['candidate_seat']): r for r in rows}
    pairs = [(idx[(parent,) + k[1:]], r) for k, r in idx.items() if k[0] == cand and (parent,) + k[1:] in idx]
    print(f'=== campaign {out}: {cand} vs {parent}, paired rows {len(pairs)} (of {sum(1 for k in idx if k[0] == cand)} candidate rows)')
    tel = [c.get('candidate_telemetry') or {} for _, c in pairs]

    def cows_at_end(r):
        cps = r.get('checkpoints') or []
        return (cps[-1].get('tiles') or {}).get('COW', 0) if cps else None
    attempt = [i for i, t in enumerate(tel) if t.get('p002_bought')]
    confirmed = [i for i in attempt if cows_at_end(pairs[i][1]) is not None and cows_at_end(pairs[i][0]) is not None and cows_at_end(pairs[i][1]) >= cows_at_end(pairs[i][0]) + 1]
    print(f"attempts {len(attempt)}/{len(pairs)}; confirmed (final-checkpoint COW tiles >= parent+1) {len(confirmed)}; buy days {dict(sorted(collections.Counter(int(t['p002_buy_day']) for t in tel if t.get('p002_bought')).items()))}")
    blocks = collections.Counter()
    for t in tel:
        for k, v in t.items():
            if k.startswith('p002_block_') and isinstance(v, (int, float)):
                blocks[k[11:]] += v
    print('first-block reasons (evaluations):', dict(blocks.most_common()))
    none = [i for i in range(len(pairs)) if i not in set(attempt)]
    for name, sel in (('all', range(len(pairs))), ('confirmed', confirmed), ('attempt-unconf', [i for i in attempt if i not in set(confirmed)]), ('no attempt', none)):
        sel = list(sel)
        if not sel:
            continue
        dm = [pairs[i][1]['margin'] - pairs[i][0]['margin'] for i in sel]; own = [pairs[i][1]['rewards'][pairs[i][1]['candidate_seat']] - pairs[i][0]['rewards'][pairs[i][0]['candidate_seat']] for i in sel]
        riv = [pairs[i][1]['rewards'][1 - pairs[i][1]['candidate_seat']] - pairs[i][0]['rewards'][1 - pairs[i][0]['candidate_seat']] for i in sel]
        w2l = sum(1 for i in sel if pairs[i][0]['outcome'] == 'win' and pairs[i][1]['outcome'] == 'loss'); l2w = sum(1 for i in sel if pairs[i][0]['outcome'] == 'loss' and pairs[i][1]['outcome'] == 'win')
        print(f"  {name:14s} n={len(sel):3d} own d {mean(own):+6.0f} (se {se(own):3.0f}) rival d {mean(riv):+6.0f} margin d {mean(dm):+6.0f} (se {se(dm):3.0f}) W->L {w2l} L->W {l2w} own<-500 {sum(1 for x in own if x < -500)}")
    same = sum(1 for i in none if pairs[i][1]['action_hashes'][pairs[i][1]['candidate_seat']] == pairs[i][0]['action_hashes'][pairs[i][0]['candidate_seat']])
    print(f"  no-attempt games with IDENTICAL candidate action stream to the parent: {same}/{len(none)}" + ('' if same == len(none) else '  -> differences to explain before crediting the cow'))
    byo = collections.defaultdict(list)
    for i, (b, c) in enumerate(pairs):
        byo[(c['opponent_family'], c['opponent_name'])].append(i)
    print('per opponent: attempts/confirmed / n | own d | rival d | margin d | W->L L->W | worst margin game')
    for (fam, o), sel in sorted(byo.items()):
        dm = [pairs[i][1]['margin'] - pairs[i][0]['margin'] for i in sel]; own = [pairs[i][1]['rewards'][pairs[i][1]['candidate_seat']] - pairs[i][0]['rewards'][pairs[i][0]['candidate_seat']] for i in sel]
        riv = [pairs[i][1]['rewards'][1 - pairs[i][1]['candidate_seat']] - pairs[i][0]['rewards'][1 - pairs[i][0]['candidate_seat']] for i in sel]
        wi = min(sel, key=lambda i: pairs[i][1]['margin'] - pairs[i][0]['margin'])
        print(f"  {fam[:18]:18s} {o:28s} {sum(1 for i in sel if i in set(attempt)):2d}/{sum(1 for i in sel if i in set(confirmed)):2d} / {len(sel):<2d} | {mean(own):+6.0f} | {mean(riv):+6.0f} | {mean(dm):+6.0f} | {sum(1 for i in sel if pairs[i][0]['outcome'] == 'win' and pairs[i][1]['outcome'] == 'loss')} {sum(1 for i in sel if pairs[i][0]['outcome'] == 'loss' and pairs[i][1]['outcome'] == 'win')} | seed {pairs[wi][1]['seed']} s{pairs[wi][1]['candidate_seat']} {pairs[wi][1]['margin'] - pairs[wi][0]['margin']:+.0f}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--mx', nargs=2, action='append', metavar=('BASE', 'CAND')); ap.add_argument('--campaign'); ap.add_argument('--parent', default='base19-planner'); ap.add_argument('--cand', default='p002-cow1')
    a = ap.parse_args()
    for base, cand in a.mx or []:
        mx(base, cand)
    if a.campaign:
        campaign(a.campaign, a.parent, a.cand)


if __name__ == '__main__':
    main()
