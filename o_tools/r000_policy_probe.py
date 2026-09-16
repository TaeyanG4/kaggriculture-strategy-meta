"""Policy probe: per-game decision records for a team (Level-1 route reconstruction).
Usage: python o_tools/r000_policy_probe.py <replay_dir>   (uses <dir>/_index.json my_seat)"""
import json, glob, os, sys, collections
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
TOM=("PIZZA_SHOP","FARMERS_MARKET")
recs=[]
def cnt(tiles,pred): return sum(1 for row in tiles for t in row if isinstance(t,dict) and pred(t))
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; me=idx[eid]["my_seat"]; r=json.load(open(p,encoding="utf-8")); steps=r["steps"]
    rec=dict(ep=eid,margin=idx[eid]["margin"],opp=idx[eid]["opp_team"])
    first_tom=None; land=[]; quads=1; first_str=None; carrot_first=None
    for t in range(1,720):
        obs=steps[t-1][0]["observation"]; farm=obs["farms"][me]; shops=obs["town"]["unlocked_shops"]
        a=steps[t][me].get("action") or {}; cmds=[a.get("farmer") or ["PASS"]]+list(a.get("hands") or [])
        q=len(farm["unlocked_quadrants"])
        if q>quads: land.append((t-1,q,round(farm["money"]))); quads=q
        if first_tom is None and any(c and c[:2]==["PLANT","TOMATO"] for c in cmds):
            first_tom=dict(step=t-1,day=(t-1)//24,tom_shops=sum(s in TOM for s in shops),n_shops=len(shops),cash=round(farm["money"]),price=obs["market"]["prices"]["TOMATO"])
        if first_str is None and any(c and c[:2]==["PLANT","STRAWBERRY"] for c in cmds): first_str=(t-1)//24
        if carrot_first is None and any(c and c[:2]==["PLANT","CARROT"] for c in cmds): carrot_first=(t-1)//24
    tiles=lambda t: steps[t][0]["observation"]["farms"][me]["tiles"]
    rec.update(first_tomato=first_tom, land=land, straw_first_day=first_str, carrot_first_day=carrot_first,
               tom_max=max(cnt(tiles(t),lambda x:x.get("crop")=="TOMATO") for t in range(0,720,24)),
               straw_max=max(cnt(tiles(t),lambda x:x.get("crop")=="STRAWBERRY") for t in range(0,720,24)),
               geese_d12=cnt(tiles(288),lambda x:x.get("animal")=="GOOSE"), cows_d12=cnt(tiles(288),lambda x:x.get("animal")=="COW"), sheep_d12=cnt(tiles(288),lambda x:x.get("animal")=="SHEEP"),
               final_shops=steps[-1][0]["observation"]["town"]["unlocked_shops"], hands_d12=len(steps[288][0]["observation"]["farms"][me]["hands"]))
    # tomato shops at day 12 and at end
    rec["tom_shops_final"]=sum(s in TOM for s in rec["final_shops"]); rec["tom_shops_d12"]=sum(s in TOM for s in steps[288][0]["observation"]["town"]["unlocked_shops"])
    recs.append(rec)
json.dump(recs,open(os.path.join(D,"_policy.json"),"w"),indent=0)
n=len(recs); print(f"{n} games")
print("\n== TOMATO planting decision ==")
c=collections.Counter(); v=collections.defaultdict(list)
for r in recs:
    ft=r["first_tomato"]; k=(ft["tom_shops"] if ft else "never")
    c[k]+=1; 
    if ft: v[k].append((ft["day"], r["tom_max"], ft["cash"], ft["price"]))
print("first tomato plant by #tomato-shops-at-that-time:", dict(c))
for k in sorted(v, key=str):
    days=[x[0] for x in v[k]]; tiles=[x[1] for x in v[k]]; cash=[x[2] for x in v[k]]; pr=[x[3] for x in v[k]]
    print(f"  tom_shops={k}: n={len(v[k])} plant day median {sorted(days)[len(days)//2]} (min {min(days)} max {max(days)}), max tiles median {sorted(tiles)[len(tiles)//2]}, cash median {sorted(cash)[len(cash)//2]}, tomato price median {sorted(pr)[len(pr)//2]}")
print("never-planted games by final tomato shops:", collections.Counter(r["tom_shops_final"] for r in recs if not r["first_tomato"]))
print("planted games by final tomato shops:", collections.Counter(r["tom_shops_final"] for r in recs if r["first_tomato"]))
print("\n== LAND ==")
for k in (2,3,4):
    xs=[(l[0],l[2]) for r in recs for l in r["land"] if l[1]==k]
    if xs: print(f"  quadrant {k}: n={len(xs)}/{n} step median {sorted(x[0] for x in xs)[len(xs)//2]} (day {sorted(x[0] for x in xs)[len(xs)//2]//24}), cash-before median {sorted(x[1] for x in xs)[len(xs)//2]}")
print("\n== crops/animals ==")
print("strawberry first plant day:", collections.Counter(r["straw_first_day"] for r in recs).most_common(5), " max straw tiles median", sorted(r["straw_max"] for r in recs)[n//2])
print("carrot first plant day:", collections.Counter(r["carrot_first_day"] for r in recs).most_common(6))
print("day12 geese/cows/sheep/hands medians:", [sorted(r[k] for r in recs)[n//2] for k in ("geese_d12","cows_d12","sheep_d12","hands_d12")])
print("\n== margin by tomato decision ==")
for k in ("planted","never"):
    ms=[r["margin"] for r in recs if bool(r["first_tomato"])==(k=="planted")]
    if ms: print(f"  {k}: n={len(ms)} mean margin {sum(ms)/len(ms):+.0f}")
