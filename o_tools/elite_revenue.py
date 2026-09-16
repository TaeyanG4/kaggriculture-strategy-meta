import json, glob, os, sys, io, contextlib, collections
sys.path.insert(0,"tools"); from o_revenue import analyze
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
agg={"ours":collections.defaultdict(float),"rival":collections.defaultdict(float)}
qty={"ours":collections.Counter(),"rival":collections.Counter()}
cost={"ours":collections.defaultdict(float),"rival":collections.defaultdict(float)}
n=0
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; me=idx[eid]["my_seat"]
    with contextlib.redirect_stdout(io.StringIO()):
        out=analyze(p)
    n+=1
    for side,s in (("ours",me),("rival",1-me)):
        for k,v in out[s]["revenue"].items(): agg[side][k]+=v
        for k,v in out[s]["qty"].items(): qty[side][k]+=v
        for k,v in out[s]["cost"].items(): cost[side][k]+=v
print(f"{n} games. per-game averages: revenue (units, avg price)")
items=sorted(set(agg["ours"])|set(agg["rival"]), key=lambda k:-agg["rival"][k])
print(f"{'item':12s} {'ours$':>8s} {'units':>6s} {'$/u':>5s} | {'rival$':>8s} {'units':>6s} {'$/u':>5s} | d$")
for k in items:
    o,r=agg["ours"][k]/n,agg["rival"][k]/n; qo,qr=qty["ours"][k]/n,qty["rival"][k]/n
    print(f"{k:12s} {o:8.0f} {qo:6.1f} {o/max(1,qo):5.0f} | {r:8.0f} {qr:6.1f} {r/max(1,qr):5.0f} | {o-r:+6.0f}")
print("\ncosts per game")
for k in sorted(set(cost["ours"])|set(cost["rival"]), key=lambda k:-cost["rival"][k]):
    print(f"{k:16s} ours {cost['ours'][k]/n:8.0f}  rival {cost['rival'][k]/n:8.0f}  d {cost['ours'][k]/n-cost['rival'][k]/n:+7.0f}")
print(f"\nTOTAL revenue ours {sum(agg['ours'].values())/n:.0f} rival {sum(agg['rival'].values())/n:.0f}; cost ours {sum(cost['ours'].values())/n:.0f} rival {sum(cost['rival'].values())/n:.0f}")
