"""Per-shop-pair evaluation of c171 (V42 production routes) vs o182 on the world bank, and a guard overlay
that removes the pairs where V42 loses. Reads o_results/strat/{c171,o182}/*.json (same seeds/opponents/seats).
Usage: python o_tools/c171_pair_guard.py            -> prints per-pair table, writes agent/overlays/o215_c171_guard.py
Guard rule (robust): keep V42 for a pair only if n >= 8, wins >= base wins, and worst game > -8000; else legacy.
"""
import collections, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(tag):
    d = {}
    for f in os.listdir(os.path.join(ROOT, 'o_results', 'strat', tag)):
        for r in json.load(open(os.path.join(ROOT, 'o_results', 'strat', tag, f)))['results']:
            if r['outcome'] in ('win', 'loss', 'tie'):
                d[(f, r['seed'], r['seat'])] = (r['margin'], tuple((r.get('shops') or [])[:2]))
    return d


def main():
    a = load('c171'); b = load('o199c')   # o182 has no bank run; o199c = o182 + carrot switch (differs only in PET-heavy worlds)
    per = collections.defaultdict(list)
    for k, (m, pair) in a.items():
        if k in b and len(pair) == 2:
            per[pair].append((m - b[k][0], m > 0, b[k][0] > 0))
    keep, drop = [], []
    print('pair (ordered first two shops) | n | delta | wins c171/o182 | worst')
    for pair, v in sorted(per.items(), key=lambda kv: sum(x[0] for x in kv[1]) / len(kv[1])):
        n = len(v); d = sum(x[0] for x in v) / n; w = sum(x[1] for x in v); wb = sum(x[2] for x in v); worst = min(x[0] for x in v)
        ok = n >= 8 and worst > -8000 and (w > wb or (w == wb and d >= -300))   # equal wins with a big margin loss is a tail risk
        (keep if ok else drop).append(pair)
        print(f"  {'KEEP' if ok else 'DROP'} {pair[0][:12]:12s}+{pair[1][:12]:12s} n={n:3d} delta {d:+6.0f} wins {w}/{wb} worst {worst:+.0f}")
    src = f'''# o215_c171_guard (Claude/o-series, 2026-09-15). Overlay for c171: drop the V42 routes for shop pairs where
# the world bank shows V42 losing to the legacy o182 route (n>=8 & wins>=base & worst>-8000 required to keep).
# Kept pairs: {len(keep)}, dropped pairs: {len(drop)}.
_O215_DROP = {json.dumps([list(p) for p in drop])}
for _p in _O215_DROP:
    _C171_ROUTE_MAP.pop(tuple(_p), None)
agent = globals().pop('agent')
'''
    open(os.path.join(ROOT, 'agent', 'overlays', 'o215_c171_guard.py'), 'w', encoding='utf-8').write(src)
    print(f'kept {len(keep)} pairs, dropped {len(drop)} -> agent/overlays/o215_c171_guard.py')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main()
