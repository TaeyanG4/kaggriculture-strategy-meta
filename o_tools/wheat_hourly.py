import json, glob, os, sys, collections
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
lo,hi=int(sys.argv[2]),int(sys.argv[3])  # day range
H=collections.defaultdict(lambda:[0,0,0,0]); n=0  # hour -> [rival buy, rival sell, ours buy, ours sell]
ph=collections.defaultdict(list)
seq=collections.Counter()
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; r=json.load(open(p,encoding="utf-8")); me=idx[eid]["my_seat"]; op=1-me; steps=r["steps"]; n+=1
    for t in range(1,len(steps)):
        day=(t-1)//24; hour=(t-1)%24
        if not (lo<=day<=hi): continue
        price=steps[t-1][0]["observation"]["market"]["prices"]["WHEAT"]; ph[hour].append(price)
        for k,s in ((0,op),(2,me)):
            sb=steps[t-1][s]["observation"]["private"]["shed"].get("WHEAT",0); sa=steps[t][s]["observation"]["private"]["shed"].get("WHEAT",0)
            mk=(steps[t][s].get("action") or {}).get("market") or []
            b=sum(int(o[2]) for o in mk if o and o[0]=="BUY_PRODUCT" and len(o)==3 and o[1]=="WHEAT")
            sl=sum(int(o[2]) for o in mk if o and o[0]=="SELL" and len(o)==3 and o[1]=="WHEAT")
            H[hour][k]+=b; H[hour][k+1]+=sl
            if s==op and b and sl: seq["rival same-step buy+sell"]+=1
            if s==op and b: seq["rival buy steps"]+=1
            if s==op and sl: seq["rival sell steps"]+=1
print(f"{n} games, days {lo}-{hi}: per-game avg WHEAT units by hour of day")
print(f"{'hr':>2} {'price':>6} | {'rival buy':>9} {'rival sell':>10} | {'ours buy':>8} {'ours sell':>9}")
for h in range(24):
    b,s,ob,os_=H[h]; print(f"{h:>2} {sum(ph[h])/max(1,len(ph[h])):6.1f} | {b/n:9.2f} {s/n:10.2f} | {ob/n:8.2f} {os_/n:9.2f}")
print(dict(seq))
