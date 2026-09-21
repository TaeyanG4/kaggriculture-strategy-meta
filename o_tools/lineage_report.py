"""Frozen live-pool diagnostic by rival LINEAGE (development data, not a promotion gate): reads elite_pool results
o_results/elite_pool/eval_<label>.json for a base label and candidate labels (same 117 recorded rivals of o_replays/live_frozen/live_b19,
`elite_pool.py --us Taeyang --dir o_replays/live_frozen/live_b19 --teams live_b19 --label <L>`), groups the games by the lineage map
o_results/live_pool_groups.json (from o_tools/rival_source_trace.py) and prints per-lineage wins / mean margin / paired deltas plus the
live-frequency-weighted total (= the pool itself: every recorded rival counts once).
Usage: python o_tools/lineage_report.py --base lb_base19 --cands lb_mx2 lb_cow1 lb_cow1_mx2 [--groups o_results/live_pool_groups.json]"""
import argparse, collections, json, os, statistics as st
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(label):
    return {g['episode']: g for g in json.load(open(os.path.join(ROOT, 'o_results', 'elite_pool', f'eval_{label}.json'), encoding='utf-8'))}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--base', required=True); ap.add_argument('--cands', nargs='+', required=True); ap.add_argument('--groups', default='o_results/live_pool_groups.json')
    a = ap.parse_args()
    groups = json.load(open(os.path.join(ROOT, a.groups), encoding='utf-8')); B = load(a.base); C = {c: load(c) for c in a.cands}
    eps = [e for e in B if all(e in C[c] for c in a.cands)]
    by = collections.defaultdict(list)
    for e in eps:
        by[groups.get(e, 'O  other')].append(e)
    m = lambda D, e: D[e]['our_cash'] - D[e]['their_cash']
    print(f"frozen live pool: {len(eps)} games paired across {a.base} and {a.cands} (lineage = first 6 market turns + replay verification; see reports/o-live-source-trace-2026-09-18.ko.md)")
    print(f"{'lineage':66s} n  | {a.base[:12]:>12s} W  margin | " + ' | '.join(f"{c[:12]:>12s} W  margin (d)  W->L L->W" for c in a.cands))
    tot = collections.defaultdict(list)
    for gname in sorted(by):
        es = by[gname]
        wb = sum(1 for e in es if m(B, e) > 0); mb = st.mean(m(B, e) for e in es)
        cells = []
        for c in a.cands:
            D = C[c]; wc = sum(1 for e in es if m(D, e) > 0); mc = st.mean(m(D, e) for e in es)
            w2l = sum(1 for e in es if m(B, e) > 0 and m(D, e) <= 0); l2w = sum(1 for e in es if m(B, e) <= 0 and m(D, e) > 0)
            cells.append(f"{wc:2d}/{len(es):<3d} {mc:+7.0f} ({mc - mb:+6.0f}) {w2l:3d} {l2w:4d}")
            tot[c] += [m(D, e) - m(B, e) for e in es]
        print(f"{gname[:66]:66s} {len(es):3d} | {wb:2d}/{len(es):<3d} {mb:+7.0f} | " + ' | '.join(cells))
    print()
    for c in a.cands:
        d = tot[c]; wb = sum(1 for e in eps if m(B, e) > 0); wc = sum(1 for e in eps if m(C[c], e) > 0)
        print(f"live-frequency-weighted (all {len(eps)} recorded rivals once): {c:14s} margin delta {st.mean(d):+6.0f} (se {st.stdev(d) / len(d) ** 0.5:4.0f}), wins {wb}->{wc}, W->L {sum(1 for e in eps if m(B, e) > 0 and m(C[c], e) <= 0)}, L->W {sum(1 for e in eps if m(B, e) <= 0 and m(C[c], e) > 0)}, worse(<-500) {sum(1 for x in d if x < -500)}")
    print('caveat: frozen rivals replay recorded actions; routers that branch on prices at fixed turns may have chosen differently against the candidate (frozen = mechanism-level evidence only).')


if __name__ == '__main__':
    main()
