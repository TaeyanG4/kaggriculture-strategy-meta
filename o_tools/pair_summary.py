"""Paired summary of two o_arena result files (same seeds/seats): wins, our/opp money, flips, telemetry sums.
Usage: python o_tools/pair_summary.py base.json cand.json [tel_prefix]"""
import json, sys


def load(f):
    R = [r for r in json.load(open(f, encoding='utf-8'))['results'] if r.get('outcome') in ('win', 'loss', 'tie')]
    M = {}
    for r in R:
        r0, r1 = r['rewards']
        me, op = (r0, r1) if abs((r0 - r1) - r['margin']) < 1e-6 else (r1, r0)
        M[(r['seed'], r['seat'])] = (r['margin'], me, op, r.get('telemetry') or {})
    return M


def main():
    a, b = load(sys.argv[1]), load(sys.argv[2]); pre = sys.argv[3] if len(sys.argv) > 3 else None
    ks = [k for k in a if k in b]
    for name, M in (('base', a), ('cand', b)):
        W = sum(M[k][0] > 0 for k in ks)
        print(f"  {name}: {W}W {len(ks)-W}L mean {sum(M[k][0] for k in ks)/len(ks):+.0f} money {sum(M[k][1] for k in ks)/len(ks):.0f}/{sum(M[k][2] for k in ks)/len(ks):.0f}")
    print(f"  paired delta {sum(b[k][0]-a[k][0] for k in ks)/len(ks):+.0f} | flips L->W {sum(a[k][0]<=0<b[k][0] for k in ks)} W->L {sum(b[k][0]<=0<a[k][0] for k in ks)} | changed {sum(abs(b[k][0]-a[k][0])>0.5 for k in ks)}")
    if pre:
        keys = sorted({x for k in ks for x in b[k][3] if x.startswith(pre)})
        print('  telemetry/game:', {x: round(sum(b[k][3].get(x, 0) or 0 for k in ks) / len(ks), 1) for x in keys})


if __name__ == '__main__':
    main()
