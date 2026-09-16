import json, os, sys, gzip, requests, time, collections
OUT="o_results"; REPLAY_URL="https://www.kaggleusercontent.com/episodes/{id}.json"
s=requests.Session(); s.headers["User-Agent"]="kaggriculture-strategy-meta live audit"
NAMES={"56232526":"c153","56231047":"c152","56219458":"c146","56219450":"c147","56209242":"c129"}
# 1) top-cluster loss rate per submission
for sid,name in NAMES.items():
    d=json.load(open(f"{OUT}/live_episodes_{sid}.json",encoding="utf-8"))
    buckets=collections.defaultdict(lambda:[0,0])
    for e in d.get("episodes",[]):
        if e.get("state")!="COMPLETED": continue
        ag=e.get("agents",[]); me=next((a for a in ag if str(a.get("submissionId"))==sid),None); op=next((a for a in ag if str(a.get("submissionId"))!=sid),None)
        if not me or not op or me.get("reward") is None or op.get("reward") is None: continue
        r=op.get("updatedScore") or 0
        b="<2400" if r<2400 else ("2400-2749" if r<2750 else "2750+")
        buckets[b][0]+= me["reward"]>op["reward"]; buckets[b][1]+=1
    print(name, {b:f"{w}/{n} ({w/n:.0%})" for b,(w,n) in sorted(buckets.items())})
# 2) download anomalous c153 losses (to opponents rated < 2300) and check for errors/timeouts
sid="56232526"; d=json.load(open(f"{OUT}/live_episodes_{sid}.json",encoding="utf-8"))
os.makedirs(f"{OUT}/live_replays_c153",exist_ok=True)
for e in d["episodes"]:
    if e.get("state")!="COMPLETED": continue
    ag=e["agents"]; me=next((a for a in ag if str(a.get("submissionId"))==sid),None); op=next((a for a in ag if str(a.get("submissionId"))!=sid),None)
    if not me or not op or me.get("reward") is None: continue
    if me["reward"]<op["reward"] and (op.get("updatedScore") or 0)<2300:
        eid=e["id"]; p=f"{OUT}/live_replays_c153/episode-{eid}.json"
        if not os.path.exists(p):
            r=s.get(REPLAY_URL.format(id=eid),timeout=120); open(p,"wb").write(r.content); time.sleep(1)
        rep=json.load(open(p,encoding="utf-8"))
        my_idx=[i for i,a in enumerate(ag) if str(a.get("submissionId"))==sid][0]
        steps=rep["steps"]; last=steps[-1]
        statuses=[x.get("status") for x in last]
        # count our PASS-only / error steps and timing
        errs=sum(1 for st in steps if st[my_idx].get("status") not in ("ACTIVE","DONE"))
        passes=sum(1 for st in steps if (st[my_idx].get("action") or {}).get("farmer")==["PASS"] and not (st[my_idx].get("action") or {}).get("hands"))
        money=[st[0]["observation"]["farms"][my_idx]["money"] for st in steps]
        print(f"ep {eid} seat{my_idx} vs {op.get('teamId')} rating {op.get('updatedScore'):.0f}: final statuses {statuses}, non-active steps {errs}, pass-only steps {passes}, money@0/240/480/719 {[round(money[i]) for i in (0,240,480,-1)]}, rewards {[a.get('reward') for a in ag]}")
