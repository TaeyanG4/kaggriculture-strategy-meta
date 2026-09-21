"""Conditional-rule judgement: paired comparison over the three seed sets vs a baseline label, split into affected games
(cash differs from the baseline, i.e. the rule fired) and untouched games (bit-identical). Prints the affected-subset gain,
se, worse/better counts and a breakdown by the shop feature of the world.
Usage: python o_tools/cond_pair.py --base base8 --cand egg [--feature egg|yarn|pet|tomato]"""
import argparse, json, os, statistics, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEAT = {'egg': ('BAKERY', 'BRUNCH_SPOT'), 'yarn': ('YARN_STORE',), 'pet': ('PET_CAFE',), 'tomato': ('PIZZA_SHOP', 'FARMERS_MARKET'), 'milk': ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')}


def load(label):
    out = {}
    for s in ('sel', 'hold', 'fresh'):
        p = os.path.join(ROOT, 'o_results', 'proxy', f'eval_{label}_{s}.json')
        if os.path.exists(p):
            for r in json.load(open(p)):
                out[(r['seed'], r['seat_b'])] = r
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--base', default='base8'); ap.add_argument('--cand', required=True); ap.add_argument('--feature', default='')
    a = ap.parse_args()
    cache = json.load(open(os.path.join(ROOT, 'o_results', 'proxy', 'shop_seq.json')))
    base = load(a.base); cand = load(a.cand)
    keys = sorted(set(base) & set(cand))
    d = {k: cand[k]['b'] - base[k]['b'] for k in keys}
    aff = [k for k in keys if abs(d[k]) > 1e-6]; unt = [k for k in keys if abs(d[k]) <= 1e-6]
    def stats(ks):
        v = [d[k] for k in ks]
        if not v: return 'n=0'
        se = statistics.stdev(v) / len(v) ** 0.5 if len(v) > 1 else 0.0
        return f"n={len(v)} mean {statistics.mean(v):+6.0f} (se {se:4.0f}) worse {sum(x < -500 for x in v)} better {sum(x > 500 for x in v)} min {min(v):+.0f} max {max(v):+.0f}"
    print(f"{a.cand} vs {a.base}: all {stats(keys)} | affected {stats(aff)} | untouched {len(unt)} games")
    for s, lo, hi in (('sel', 7000, 7015), ('hold', 7016, 7031), ('fresh', 7032, 7047)):
        ks = [k for k in keys if lo <= k[0] <= hi]
        print(f"  {s:5s} all {stats(ks)} | affected {stats([k for k in ks if k in aff])}")
    if a.feature:
        by = collections.defaultdict(list)
        for k in keys:
            sh = cache[str(k[0])]
            n = sum(x in FEAT[a.feature] for x in sh[:6])   # shops unlocked by day 18
            by[n].append(k)
        for n in sorted(by):
            print(f"  {a.feature} shops by d18 = {n}: {stats(by[n])}")


if __name__ == '__main__':
    main()
