"""Paired comparison of two proxy_eval runs (same seeds/seats): candidate's own cash (a) minus baseline's, per game.
Usage: python o_tools/proxy_pair.py BASE_LABEL CAND_LABEL [...]   (compares A-side cash; add --side b to compare the proxy/B side)"""
import json, os, statistics, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(label):
    return {(r['seed'], r['seat_b']): r for r in json.load(open(os.path.join(ROOT, 'o_results', 'proxy', f'eval_{label}.json')))}
side = 'b' if '--side' in sys.argv and sys.argv[sys.argv.index('--side') + 1] == 'b' else 'a'
labels = [x for i, x in enumerate(sys.argv[1:]) if x != '--side' and sys.argv[1:][i - 1] != '--side']
base = load(labels[0])
for lab in labels[1:]:
    cand = load(lab); keys = sorted(set(base) & set(cand))
    o = 'b' if side == 'a' else 'a'
    d = [cand[k][side] - base[k][side] for k in keys]; dp = [cand[k][o] - base[k][o] for k in keys]
    wins_b = sum(base[k]['a'] > base[k]['b'] for k in keys); wins_c = sum(cand[k]['a'] > cand[k]['b'] for k in keys)
    sd = statistics.stdev(d) if len(d) > 1 else 0.0; se = sd / max(1, len(d)) ** 0.5
    print(f"{lab:32s} n={len(d)} {'own' if side == 'a' else 'proxy'} cash {statistics.mean(d):+7.0f} (se {se:5.0f}, min {min(d):+6.0f}, max {max(d):+6.0f}) | other side {statistics.mean(dp):+7.0f} | wins {wins_b}->{wins_c} | worse games {sum(x < -500 for x in d)} better {sum(x > 500 for x in d)}")
