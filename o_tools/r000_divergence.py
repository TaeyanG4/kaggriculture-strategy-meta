"""Divergence detector between the two seats of a replay (same-family pairs): first step where
field commands or market orders differ, the observable state there, and money/value gap after.
Usage: python o_tools/r000_divergence.py <replay_dir> [opponent_substring]"""
import json, glob, os, sys, collections
D=sys.argv[1]; want=sys.argv[2] if len(sys.argv)>2 else None
idx={str(r["episode"]):r for r in json.load(open(os.path.join(D,"_index.json")))}
def norm(a): return (json.dumps(a.get("farmer") or ["PASS"]), json.dumps(a.get("hands") or []), json.dumps(a.get("market") or []))
out=[]
for p in sorted(glob.glob(os.path.join(D,"*-replay.json"))):
    eid=os.path.basename(p).split("-")[0]; me=idx[eid]["my_seat"]
    if want and want not in idx[eid]["opp_team"]: continue
    r=json.load(open(p,encoding="utf-8")); steps=r["steps"]; op=1-me
    div=None; kind=None
    for t in range(1,720):
        a=norm(steps[t][me].get("action") or {}); b=norm(steps[t][op].get("action") or {})
        if a!=b:
            div=t-1; kind="market" if a[2]!=b[2] and a[:2]==b[:2] else ("field" if a[2]==b[2] else "both"); break
    if div is None: out.append(dict(ep=eid,div=None)); continue
    obs=steps[div][0]["observation"]; fm=obs["farms"][me]; fr=obs["farms"][op]
    a=steps[div+1][me].get("action") or {}; b=steps[div+1][op].get("action") or {}
    money=lambda t,s: steps[min(719,t)][0]["observation"]["farms"][s]["money"]
    gaps={t:round(money(t,me)-money(t,op)) for t in (div, div+24, div+72, div+144, 719)}
    out.append(dict(ep=eid,div=div,day=div//24,hour=div%24,kind=kind,margin=idx[eid]["margin"],me_cash=round(fm["money"]),op_cash=round(fr["money"]),
                    prices={k:obs["market"]["prices"][k] for k in ("WHEAT","MILK","STRAWBERRY","TOMATO")},shops=obs["town"]["unlocked_shops"],
                    me_action=(a.get("farmer"),a.get("hands"),a.get("market")),op_action=(b.get("farmer"),b.get("hands"),b.get("market")),gaps=gaps))
for o in out:
    if o["div"] is None: print(o["ep"],"identical whole game"); continue
    print(f"ep {o['ep']} div step {o['div']} (day {o['day']} h{o['hour']}) {o['kind']}: cash me {o['me_cash']} op {o['op_cash']} prices {o['prices']} shops {o['shops']}")
    print(f"   me : {o['me_action']}\n   op : {o['op_action']}\n   money gap after: {o['gaps']}  final margin {o['margin']:+.0f}")
json.dump(out,open(os.path.join(D,"_divergence.json"),"w"),indent=1)
