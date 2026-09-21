"""Paired margin report: for each set, delta of (own - rival) cash per game vs the base label, with se and worse/better counts.
Usage: python o_tools/margin_pair.py --base base13 --cand b14_t62 [--sets sel,hold,fresh]"""
import argparse, json, os, statistics
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(label):
    return {(r['seed'], r['seat_b']): r for r in json.load(open(os.path.join(ROOT, 'o_results', 'proxy', f'eval_{label}.json')))}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--base', required=True); ap.add_argument('--cand', required=True); ap.add_argument('--sets', default='sel,hold,fresh')
    a = ap.parse_args(); pooled = []
    for s in a.sets.split(','):
        try:
            base = load(f'{a.base}_{s}'); cand = load(f'{a.cand}_{s}')
        except FileNotFoundError:
            continue
        d = [(cand[k]['b'] - cand[k]['a']) - (base[k]['b'] - base[k]['a']) for k in sorted(set(base) & set(cand))]
        own = [cand[k]['b'] - base[k]['b'] for k in sorted(set(base) & set(cand))]
        wins = sum(cand[k]['b'] > cand[k]['a'] for k in cand); wins0 = sum(base[k]['b'] > base[k]['a'] for k in base)
        se = statistics.stdev(d) / len(d) ** 0.5
        print(f"{a.cand}_{s:5s} margin {statistics.mean(d):+6.0f} (se {se:4.0f}, worse {sum(x < -500 for x in d):2d}, better {sum(x > 500 for x in d):2d}) | own {statistics.mean(own):+6.0f} | wins {wins0}->{wins}")
        pooled += d
    if pooled and len(pooled) > 1 and statistics.stdev(pooled) > 0:
        se = statistics.stdev(pooled) / len(pooled) ** 0.5
        print(f"pooled n={len(pooled)} margin {statistics.mean(pooled):+6.0f} (se {se:4.0f}, {statistics.mean(pooled) / se:.1f} se, worse {sum(x < -500 for x in pooled)})")


if __name__ == '__main__':
    main()
