"""Aggregate replay_lab results across chunks: python o_tools/suite_summary.py o_results/elite_suite/<tag> [baseline_tag]"""
import json, glob, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def load(tag):
    out={}
    for f in glob.glob(f"o_results/{SUITE}/{tag}/c*/results.json"):
        for r in json.load(open(f,encoding="utf-8")): out[str(r["episode"])]=r
    return out
SUITE=sys.argv[3] if len(sys.argv)>3 else "elite_suite"   # optional 3rd arg: results root (elite_suite | elite2_suite holdout)
cand=load(sys.argv[1]); base=load(sys.argv[2]) if len(sys.argv)>2 and sys.argv[2]!="-" else None
idx={}
for _f in ("o_replays/elite_losses/_index.json","o_replays/elite_losses_new/_index.json"):   # frozen 88 + holdout 40
    try: idx.update({str(r["episode"]):r for r in json.load(open(_f))})
    except Exception: pass
ms=[r["margin"] for r in cand.values()]; valid=sum(r["valid"] for r in cand.values())
wins=sum(1 for r in cand.values() if r["margin"]>0)
print(f"{sys.argv[1]}: {len(cand)} games, valid {valid}, mean margin {sum(ms)/len(ms):+.0f}, wins {wins}/{len(ms)}, worst {min(ms):+.0f} best {max(ms):+.0f}")
orig=[idx[e]["margin"] for e in cand if e in idx]
if orig: print(f"  live original mean margin {sum(orig)/len(orig):+.0f}")
if base:
    common=[e for e in cand if e in base]; d=[cand[e]["margin"]-base[e]["margin"] for e in common]
    better=sum(1 for x in d if x>0); worse=sum(1 for x in d if x<0)
    print(f"  vs {sys.argv[2]} on {len(common)} common: mean delta {sum(d)/len(d):+.0f}, better {better} worse {worse} same {len(d)-better-worse}, flips L->W {sum(1 for e in common if base[e]['margin']<=0<cand[e]['margin'])}, W->L {sum(1 for e in common if cand[e]['margin']<=0<base[e]['margin'])}")
    import random, statistics
    random.seed(0); n=len(d); boots=[]
    for _ in range(4000):
        sm=[d[random.randrange(n)] for _ in range(n)]; boots.append(sum(sm)/n)
    boots.sort(); lo, hi = boots[int(0.025*len(boots))], boots[int(0.975*len(boots))]
    sd=statistics.pstdev(d); med=statistics.median(d)
    verdict = "SIGNIFICANT (+)" if lo>0 else ("SIGNIFICANT (-)" if hi<0 else "not significant (CI includes 0)")
    print(f"  paired delta: median {med:+.0f}, sd {sd:.0f}, SE {sd/max(1,n)**0.5:.0f}, bootstrap 95% CI [{lo:+.0f}, {hi:+.0f}] -> {verdict}")
    tel={}
    for r in cand.values():
        for k,v in (r.get("candidate_telemetry") or {}).items():
            if k.startswith("o1") and isinstance(v,(int,float)): tel[k]=tel.get(k,0)+v
    if tel: print("  telemetry per game:", {k:round(v/len(cand),1) for k,v in tel.items()})
    worst=sorted(common,key=lambda e:cand[e]["margin"]-base[e]["margin"])[:5]
    print("  worst deltas:", [(e, round(cand[e]["margin"]-base[e]["margin"])) for e in worst])
