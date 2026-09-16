"""Executed sells (units) per 6-step bucket over the last 96 steps, ours vs rival, plus mean price path."""
import json, glob, os, sys, collections
D=sys.argv[1]; item=sys.argv[2]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
B=6; start=624
sold={"ours":collections.Counter(),"rival":collections.Counter()}; price=collections.defaultdict(list); n=0
held_at={"ours":collections.Counter(),"rival":collections.Counter()}
def held(st,s):
    priv=st[s]["observation"]["private"]; t=priv.get("shed",{}).get(item,0)+sum(i.get(item,0) for i in priv.get("inventories",[]) or [])
    return t
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; me=idx[eid]["my_seat"]; r=json.load(open(p,encoding="utf-8")); steps=r["steps"]; n+=1
    for t in range(start,720):
        price[(t-start)//B].append(steps[t-1][0]["observation"]["market"]["prices"][item])
        for side,s in (("ours",me),("rival",1-me)):
            d=held(steps[t-1],s)-held(steps[t],s)
            mk=[o for o in ((steps[t][s].get("action") or {}).get("market") or []) if o and o[0]=="SELL" and o[1]==item]
            if d>0 and mk: sold[side][(t-start)//B]+=d
            if t%24==0: held_at[side][t]+=held(steps[t],s)
print(f"{n} games, {item}: units sold per game per {B}-step bucket (ours | rival), mean price")
for b in range((720-start)//B):
    print(f"  steps {start+b*B:3d}-{start+b*B+B-1:3d} day{(start+b*B)//24} h{(start+b*B)%24:2d}: {sold['ours'][b]/n:5.1f} | {sold['rival'][b]/n:5.1f}   price {sum(price[b])/len(price[b]):6.1f}")
print("held (shed+carried) at day starts:", {t:(round(held_at['ours'][t]/n,1),round(held_at['rival'][t]/n,1)) for t in sorted(held_at['ours'])})
