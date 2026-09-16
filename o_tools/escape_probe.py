"""For each elite loss, find our animals that escape (tile becomes bare structure) and report the
2 preceding days: fed_today per day, our shed WHEAT at day start, worker count, and what the FEED
actions looked like. Also aggregate escape-day histogram and yield lost."""
import json, glob, os, sys, collections
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
esc_day=collections.Counter(); lost_yield=0; n_esc=0; wheat_at_escape=[]; kinds=collections.Counter(); games_with=0
detail=[]
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; r=json.load(open(p,encoding="utf-8")); me=idx[eid]["my_seat"]; steps=r["steps"]
    had=False
    for t in range(24,len(steps),24):  # day boundaries: step t is start of day t//24
        fb=steps[t-1][0]["observation"]["farms"][me]["tiles"]; fa=steps[t][0]["observation"]["farms"][me]["tiles"]
        for y in range(10):
            for x in range(10):
                b=fb[y][x]; a=fa[y][x]
                if isinstance(b,dict) and b.get("animal") and isinstance(a,dict) and not a.get("animal"):
                    n_esc+=1; had=True; day=t//24-1; esc_day[day]+=1; lost_yield+=b.get("yield_units",0); kinds[b["animal"]]+=1
                    shedw=steps[t-24][me]["observation"]["private"]["shed"].get("WHEAT",0)
                    shedw2=steps[t-1][me]["observation"]["private"]["shed"].get("WHEAT",0)
                    # was it fed on day-1 and day?
                    fed_prev=steps[t-24][0]["observation"]["farms"][me]["tiles"][y][x].get("consecutive_unfed") if isinstance(steps[t-24][0]["observation"]["farms"][me]["tiles"][y][x],dict) else None
                    hands=len(steps[t-1][0]["observation"]["farms"][me]["hands"])
                    detail.append((eid,day,b["animal"],(x,y),b.get("yield_units",0),shedw,shedw2,fed_prev,hands))
    games_with+=had
print(f"escapes: {n_esc} in {games_with}/{len(idx)} games; kinds {dict(kinds)}; yield units lost on tile {lost_yield} (avg {lost_yield/max(1,n_esc):.1f}/escape)")
print("escape end-of-day histogram:", dict(sorted(esc_day.items())))
print("\nsample details (episode, day, animal, pos, yield_on_tile, shedWHEAT@daystart, shedWHEAT@dayend, consecutive_unfed@daystart, hands):")
for d in detail[:25]: print(" ",d)
