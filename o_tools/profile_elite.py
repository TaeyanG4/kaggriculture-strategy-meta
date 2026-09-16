"""Profile elite-loss replays: per game, ours vs rival portfolio at checkpoints, money curve, hires,
quadrants, sells by product. Aggregates what the 2750+ cluster does differently."""
import json, glob, os, sys, collections
D=sys.argv[1] if len(sys.argv)>1 else "o_replays/elite_losses"
idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
CK=(96,192,288,384,480,576,672,719)
def farm_mix(farm):
    c=collections.Counter()
    for row in farm["tiles"]:
        for t in row:
            if isinstance(t,dict):
                if t.get("animal"): c[t["animal"]]+=1
                elif t.get("crop"): c[t["crop"]]+=1
                elif t.get("kind") in("COOP","PASTURE"): c["empty_"+t["kind"]]+=1
                elif t.get("kind")=="WEED": c["WEED"]+=1
    return c
agg=collections.defaultdict(lambda: collections.Counter()); n=0; rows=[]
sells=collections.defaultdict(lambda: collections.Counter())
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    r=json.load(open(p,encoding="utf-8")); eid=os.path.basename(p).split("-")[0]
    me=idx[eid]["my_seat"]; op=1-me; steps=r["steps"]; n+=1
    row={"ep":eid,"opp":idx[eid]["opp_team"],"rating":round(idx[eid]["opp_rating"]),"margin":idx[eid]["margin"],"seat":me}
    for ck in CK:
        o=steps[ck][0]["observation"]; fm=o["farms"][me]; fr=o["farms"][op]
        row[f"m{ck}"]=(round(fm["money"]),round(fr["money"]))
        for side,f in (("ours",fm),("rival",fr)):
            mix=farm_mix(f); agg[(side,ck)].update(mix); agg[(side,ck)]["hands"]+=len(f["hands"]); agg[(side,ck)]["quads"]+=len(f["unlocked_quadrants"])
    # sells from actions
    for st in steps[1:]:
        for side,s in (("ours",me),("rival",op)):
            a=st[s].get("action") or {}
            for o in (a.get("market") or []):
                if o and o[0]=="SELL" and len(o)==3: sells[side][o[1]]+=int(o[2])
                if o and o[0]=="HIRE": sells[side]["HIRE"]+=1
                if o and o[0]=="BUY_LAND": sells[side]["BUY_LAND"]+=1
                if o and o[0]=="BUY_ANIMAL" and len(o)==3: sells[side]["BUY_"+o[1]]+=int(o[2])
                if o and o[0]=="BUY_PRODUCT" and len(o)==3 and o[1]=="FERTILIZER": sells[side]["BUY_FERT"]+=int(o[2])
                if o and o[0]=="BUY_PRODUCT" and len(o)==3 and o[1]=="WHEAT": sells[side]["BUY_WHEAT"]+=int(o[2])
    rows.append(row)
print(f"{n} elite games (mean margin {sum(r['margin'] for r in rows)/n:+.0f})")
print("\n== avg farm mix ours vs rival at checkpoints ==")
keys=["WHEAT","CARROT","TOMATO","STRAWBERRY","MELON","COW","SHEEP","GOOSE","empty_PASTURE","empty_COOP","WEED","hands","quads"]
print(f"{'ck':>4} "+" ".join(f"{k[:7]:>13}" for k in keys))
for ck in CK:
    print(f"{ck:>4} "+" ".join(f"{agg[('ours',ck)][k]/n:5.1f}/{agg[('rival',ck)][k]/n:<5.1f}" for k in keys))
print("\n== avg market orders per game ours vs rival ==")
for k in sorted(set(sells["ours"])|set(sells["rival"])):
    print(f"  {k:12s} {sells['ours'][k]/n:8.1f} {sells['rival'][k]/n:8.1f}")
print("\n== money curve ours-rival (mean gap) ==")
for ck in CK:
    print(f"  step {ck:3d}: {sum(r[f'm{ck}'][0]-r[f'm{ck}'][1] for r in rows)/n:+8.0f}   (ours {sum(r[f'm{ck}'][0] for r in rows)/n:7.0f} rival {sum(r[f'm{ck}'][1] for r in rows)/n:7.0f})")
json.dump(rows,open(os.path.join(D,"_profile.json"),"w"),indent=1)
