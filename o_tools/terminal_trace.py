"""Trace the last N steps of a replay: per step money delta for both seats and executed sells (via shed delta)."""
import json, sys, collections
p=sys.argv[1]; N=int(sys.argv[2]) if len(sys.argv)>2 else 48; who=sys.argv[3] if len(sys.argv)>3 else "Majkel1337"
r=json.load(open(p,encoding="utf-8")); steps=r["steps"]; names=r["info"]["TeamNames"]; me=names.index(who) if who in names else 0
PR=("WHEAT","CARROT","TOMATO","STRAWBERRY","MELON","EGG","MILK","WOOL","FERTILIZER")
print("names",names,"me",me)
tot=[collections.Counter(),collections.Counter()]
for t in range(720-N,720):
    prev=steps[t-1]; now=steps[t]; line=f"t{t:3d} h{(t-1)%24:2d}"
    prices=prev[0]["observation"]["market"]["prices"]
    for s in (me,1-me):
        dm=now[0]["observation"]["farms"][s]["money"]-prev[0]["observation"]["farms"][s]["money"]
        sb=prev[s]["observation"]["private"]["shed"]; sa=now[s]["observation"]["private"]["shed"]
        sold={k:sb.get(k,0)-sa.get(k,0) for k in PR if sb.get(k,0)-sa.get(k,0)>0}
        for k,v in sold.items(): tot[s][k]+=v
        mk=[o for o in ((now[s].get("action") or {}).get("market") or []) if o and o[0]=="SELL"]
        line+=f" | {'L' if s==me else 'R'} +{dm:6.0f} shed_sold {sold} orders {[(o[1][:4],o[2]) for o in mk][:5]}"
    if any(x for x in line.split("|")[1:] if "shed_sold {}" not in x) or t%6==0:
        print(line[:260])
print("prices at t672:", {k:steps[672][0]["observation"]["market"]["prices"][k] for k in PR})
print("prices at t719:", {k:steps[719][0]["observation"]["market"]["prices"][k] for k in PR})
print("total sold last N: L",dict(tot[me])," R",dict(tot[1-me]))
print("shed at t672 L",{k:v for k,v in steps[672][me]["observation"]["private"]["shed"].items() if v}," R",{k:v for k,v in steps[672][1-me]["observation"]["private"]["shed"].items() if v})
print("money 672->719 L",steps[672][0]["observation"]["farms"][me]["money"],"->",steps[719][0]["observation"]["farms"][me]["money"]," R",steps[672][0]["observation"]["farms"][1-me]["money"],"->",steps[719][0]["observation"]["farms"][1-me]["money"])
