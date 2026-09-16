"""Field-Ledger style phase decomposition: executed sell revenue by product per phase window,
approximated as (shed+carried delta) x prev-step price, for 'ours' (index seat) vs 'rival'."""
import json, glob, os, sys, collections
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
PR=("WHEAT","CARROT","TOMATO","STRAWBERRY","MELON","EGG","MILK","WOOL","FERTILIZER")
WINDOWS=[(1,240),(240,480),(480,672),(672,720)]
rev={w:{"ours":collections.Counter(),"rival":collections.Counter()} for w in WINDOWS}
money={w:{"ours":0.0,"rival":0.0} for w in WINDOWS}; n=0
def held(st,s):
    priv=st[s]["observation"]["private"]; tot=collections.Counter(priv.get("shed",{}))
    for inv in priv.get("inventories",[]) or []:
        for k,v in inv.items(): tot[k]+=v
    return tot
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; me=idx[eid]["my_seat"]; r=json.load(open(p,encoding="utf-8")); steps=r["steps"]; n+=1
    for (a,b) in WINDOWS:
        for side,s in (("ours",me),("rival",1-me)):
            money[(a,b)][side]+=steps[min(719,b-1)][0]["observation"]["farms"][s]["money"]-steps[a-1 if a>1 else 0][0]["observation"]["farms"][s]["money"]
        for t in range(a,min(b,720)):
            prices=steps[t-1][0]["observation"]["market"]["prices"]
            for side,s in (("ours",me),("rival",1-me)):
                hb=held(steps[t-1],s); ha=held(steps[t],s)
                mk=[o for o in ((steps[t][s].get("action") or {}).get("market") or []) if o and o[0]=="SELL"]
                sold_items={o[1] for o in mk}
                for k in PR:
                    d=hb.get(k,0)-ha.get(k,0)
                    if d>0 and k in sold_items: rev[(a,b)][side][k]+=d*prices[k]
print(f"{n} games. Executed-sell revenue per game by phase (ours | rival), money delta per phase")
for w in WINDOWS:
    o=rev[w]["ours"]; rv=rev[w]["rival"]
    print(f"\nsteps {w[0]:3d}-{w[1]:3d}: money +{money[w]['ours']/n:7.0f} | +{money[w]['rival']/n:7.0f}   sell$ {sum(o.values())/n:7.0f} | {sum(rv.values())/n:7.0f}")
    for k in PR:
        if o[k] or rv[k]: print(f"    {k:11s} {o[k]/n:7.0f} | {rv[k]/n:7.0f}   d {o[k]/n-rv[k]/n:+6.0f}")
