"""Learn the rival's feed-skip rule empirically: for each rival animal-day, was it fed? vs features."""
import json, glob, os, sys, collections
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
SPEC={'GOOSE':(4,1),'COW':(8,2),'SHEEP':(6,3)}; PROD={'GOOSE':'EGG','COW':'MILK','SHEEP':'WOOL'}
rows=[]
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; me=idx[eid]["my_seat"]; r=json.load(open(p,encoding="utf-8")); steps=r["steps"]
    for side,s in (("ours",me),("rival",1-me)):
        for day in range(10,29):
            t0=day*24; t1=(day+1)*24-1
            f0=steps[t0][0]["observation"]["farms"][s]["tiles"]; f1=steps[t1][0]["observation"]["farms"][s]["tiles"]
            pr0=steps[t0][0]["observation"]["market"]["prices"]
            # avg product price over the day
            for y in range(10):
                for x in range(10):
                    a=f0[y][x]; b=f1[y][x]
                    if not(isinstance(a,dict) and a.get("animal")): continue
                    kind=a["animal"]; fed=isinstance(b,dict) and b.get("animal")==kind and bool(b.get("fed_today"))
                    first,interval=SPEC[kind]; ds=(day+1)-a["placed_day"]-first; prod=ds>=0 and ds%interval==0
                    pav=sum(steps[t][0]["observation"]["market"]["prices"][PROD[kind]] for t in range(t0,t1+1))/24
                    rows.append(dict(side=side,kind=kind,day=day,fed=fed,unfed0=a.get("consecutive_unfed",0),prod=prod,pending=a.get("pending_care_bonus",0) or 0,price0=pr0[PROD[kind]],pav=pav,wheat=pr0["WHEAT"],held=a.get("yield_units",0)))
import statistics
def bucket(v): return "<20" if v<20 else ("20-42" if v<42 else ("42-80" if v<80 else "80+"))
for side in ("ours","rival"):
    print(f"\n== {side}: feed rate by (kind, day-avg product price bucket) ==")
    c=collections.defaultdict(lambda:[0,0])
    for r in rows:
        if r["side"]!=side: continue
        k=(r["kind"],bucket(r["pav"])); c[k][0]+=r["fed"]; c[k][1]+=1
    for k in sorted(c): print(f"  {str(k):22s} fed {c[k][0]}/{c[k][1]} = {c[k][0]/c[k][1]:.0%}")
    c=collections.defaultdict(lambda:[0,0])
    for r in rows:
        if r["side"]!=side: continue
        k=(r["kind"],"prod" if r["prod"] else "nonprod","unfed1" if r["unfed0"] else "unfed0"); c[k][0]+=r["fed"]; c[k][1]+=1
    print("  by prod/unfed:", {str(k):f"{v[0]}/{v[1]}={v[0]/v[1]:.0%}" for k,v in sorted(c.items())})
    c=collections.defaultdict(lambda:[0,0])
    for r in rows:
        if r["side"]!=side: continue
        c[r["day"]][0]+=r["fed"]; c[r["day"]][1]+=1
    print("  by day:", " ".join(f"{d}:{v[0]/v[1]:.0%}" for d,v in sorted(c.items())))
json.dump(rows,open(os.path.join(D,"_feed_rows.json"),"w"))
