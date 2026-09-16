"""When do rivals buy/sell WHEAT vs price? per-game day-level ledger of executed wheat buys/sells and price."""
import json, glob, os, sys, collections
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
minr=float(sys.argv[2]) if len(sys.argv)>2 else 0
buy=collections.defaultdict(lambda:[0,0.0]); sell=collections.defaultdict(lambda:[0,0.0]); n=0
pricehist=collections.defaultdict(list)
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]
    if idx[eid]["opp_rating"]<minr: continue
    r=json.load(open(p,encoding="utf-8")); me=idx[eid]["my_seat"]; op=1-me; steps=r["steps"]; n+=1
    for t in range(1,len(steps)):
        prev=steps[t-1]; now=steps[t]; day=(t-1)//24; hour=(t-1)%24
        price=prev[0]["observation"]["market"]["prices"]["WHEAT"]; pricehist[day].append(price)
        for side,s in (("ours",me),("rival",op)):
            sb=prev[s]["observation"]["private"]["shed"].get("WHEAT",0); sa=now[s]["observation"]["private"]["shed"].get("WHEAT",0)
            a=now[s].get("action") or {}; mk=a.get("market") or []
            b=sum(int(o[2]) for o in mk if o and o[0]=="BUY_PRODUCT" and len(o)==3 and o[1]=="WHEAT")
            sl=sum(int(o[2]) for o in mk if o and o[0]=="SELL" and len(o)==3 and o[1]=="WHEAT")
            if b: buy[(side,day)][0]+=b; buy[(side,day)][1]+=b*price
            if sl: sell[(side,day)][0]+=sl; sell[(side,day)][1]+=sl*price
print(f"{n} games (opp rating>={minr}). per-game avg WHEAT orders by day: buy units@price / sell units@price ; market price mean")
print(f"{'day':>3} {'price':>6} | {'ours buy':>12} {'ours sell':>12} | {'rival buy':>12} {'rival sell':>12}")
for day in range(30):
    pr=sum(pricehist[day])/max(1,len(pricehist[day]))
    def f(d,k):
        u,v=d[(k,day)]; return f"{u/n:5.1f}@{v/max(1,u):3.0f}"
    print(f"{day:>3} {pr:6.1f} | {f(buy,'ours'):>12} {f(sell,'ours'):>12} | {f(buy,'rival'):>12} {f(sell,'rival'):>12}")
