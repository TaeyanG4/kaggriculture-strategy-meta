import json, glob, os, sys, collections
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
F=collections.defaultdict(lambda:[0,0]); C=collections.defaultdict(lambda:[0,0]); n=0
animals=collections.defaultdict(lambda:[0,0])
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; r=json.load(open(p,encoding="utf-8")); me=idx[eid]["my_seat"]; op=1-me; steps=r["steps"]; n+=1
    for t in range(1,len(steps)):
        day=(t-1)//24
        for k,s in ((0,me),(1,op)):
            a=steps[t][s].get("action") or {}
            cmds=[a.get("farmer") or ["PASS"]]+list(a.get("hands") or [])
            F[day][k]+=sum(1 for c in cmds if c and c[0]=="FEED"); C[day][k]+=sum(1 for c in cmds if c and c[0]=="CARE")
        if (t-1)%24==0:
            for k,s in ((0,me),(1,op)):
                farm=steps[t-1][0]["observation"]["farms"][s]
                animals[day][k]+=sum(1 for row in farm["tiles"] for x in row if isinstance(x,dict) and x.get("animal"))
print(f"{n} games: per-game FEED / CARE actions and animal count by day (ours | rival)")
for d in range(30):
    print(f"day {d:2d}: animals {animals[d][0]/n:4.1f}|{animals[d][1]/n:4.1f}  FEED {F[d][0]/n:5.1f}|{F[d][1]/n:5.1f}  CARE {C[d][0]/n:5.1f}|{C[d][1]/n:5.1f}")
print("total FEED", sum(v[0] for v in F.values())/n, sum(v[1] for v in F.values())/n, " CARE", sum(v[0] for v in C.values())/n, sum(v[1] for v in C.values())/n)
