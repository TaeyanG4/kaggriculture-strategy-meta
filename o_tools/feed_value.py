"""Per game: FEED actions by animal kind, ours vs rival, split by whether the product has demand
(shop present) — and the product price at feed time. Identifies wasted feeds on worthless animals."""
import json, glob, os, sys, collections
D=sys.argv[1]; idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
SHOPS={"SHEEP":("YARN_STORE",),"COW":("PIZZA_SHOP","SMOOTHIE_SHOP","ICE_CREAM_SHOP"),"GOOSE":("BRUNCH_SPOT","PET_CAFE","BAKERY")}
PROD={"SHEEP":"WOOL","COW":"MILK","GOOSE":"EGG"}
agg=collections.defaultdict(lambda:[0,0,0.0,0.0]); n=0  # (kind, demand?) -> [ours feeds, rival feeds, ours wheat$ , rival wheat$]
lowp=collections.defaultdict(lambda:[0,0])  # feeds while product price < 20
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; me=idx[eid]["my_seat"]; op=1-me; r=json.load(open(p,encoding="utf-8")); steps=r["steps"]; n+=1
    for t in range(1,len(steps)):
        obs=steps[t-1][0]["observation"]; shops=obs["town"]["unlocked_shops"]; prices=obs["market"]["prices"]
        for k,s in ((0,me),(1,op)):
            farm=obs["farms"][s]; pos=[farm["farmer"]]+farm["hands"]
            a=steps[t][s].get("action") or {}; cmds=[a.get("farmer") or ["PASS"]]+list(a.get("hands") or [])
            for i,c in enumerate(cmds[:len(pos)]):
                if not(c and c[0]=="FEED"): continue
                x,y=pos[i]; tile=farm["tiles"][y][x]
                if not(isinstance(tile,dict) and tile.get("animal")): continue
                kind=tile["animal"]; demand=any(sh in shops for sh in SHOPS[kind])
                agg[(kind,demand)][k]+=1; agg[(kind,demand)][2+k]+=prices["WHEAT"]
                if prices[PROD[kind]]<20: lowp[kind][k]+=1
print(f"{n} games. FEED actions per game by (animal, product-demand): ours | rival  (wheat $ spent)")
for key in sorted(agg):
    o,rv,oc,rc=agg[key]; print(f"  {str(key):22s} {o/n:6.1f} | {rv/n:6.1f}   ${oc/n:6.0f} | ${rc/n:6.0f}")
print("feeds while product price < $20 (ours | rival):", {k:(v[0]/n,v[1]/n) for k,v in lowp.items()})
