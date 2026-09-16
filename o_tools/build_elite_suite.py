"""Build the live elite-loss regression suite: every completed live episode our submissions LOST
to an opponent rated >= RATING_MIN, downloaded as <episode>-replay.json for replay_lab.
Usage: python o_tools/build_elite_suite.py 56209242 56219458 56219450 --min-rating 2750 --out o_replays/elite_losses"""
import argparse, json, os, time, requests
REPLAY_URL="https://www.kaggleusercontent.com/episodes/{id}.json"
ap=argparse.ArgumentParser(); ap.add_argument("subs",nargs="+"); ap.add_argument("--min-rating",type=float,default=2750)
ap.add_argument("--out",default="o_replays/elite_losses"); ap.add_argument("--wins",action="store_true",help="also include wins (for calibration)")
a=ap.parse_args(); os.makedirs(a.out,exist_ok=True)
s=requests.Session(); s.headers["User-Agent"]="kaggriculture-strategy-meta live audit"
index=[]
for sid in a.subs:
    d=json.load(open(f"o_results/live_episodes_{sid}.json",encoding="utf-8"))
    for e in d["episodes"]:
        if e.get("state")!="COMPLETED": continue
        ag=e["agents"]; me=next((x for x in ag if str(x.get("submissionId"))==sid),None); op=next((x for x in ag if str(x.get("submissionId"))!=sid),None)
        if not me or not op or me.get("reward") is None or op.get("reward") is None: continue
        if (op.get("updatedScore") or 0) < a.min_rating: continue
        lost = me["reward"] < op["reward"]
        if not lost and not a.wins: continue
        eid=e["id"]; p=os.path.join(a.out,f"{eid}-replay.json")
        if not os.path.exists(p):
            r=s.get(REPLAY_URL.format(id=eid),timeout=120)
            if r.status_code!=200: print("skip",eid,r.status_code); continue
            open(p,"wb").write(r.content); time.sleep(0.8)
        index.append(dict(episode=eid,sub=sid,lost=lost,margin=me["reward"]-op["reward"],opp_sub=op.get("submissionId"),opp_team=op.get("teamId"),opp_rating=op.get("updatedScore"),my_seat=[i for i,x in enumerate(ag) if str(x.get("submissionId"))==sid][0]))
        print(f"{eid} sub {sid} {'L' if lost else 'W'} margin {me['reward']-op['reward']:+.0f} opp {op.get('teamId')} rating {op.get('updatedScore'):.0f}")
json.dump(index,open(os.path.join(a.out,"_index.json"),"w"),indent=1)
print(len(index),"episodes ->",a.out)
