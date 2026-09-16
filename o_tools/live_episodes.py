"""Pull live Kaggle episode records for our submissions (read-only public API) and tabulate
W/L/T, tie rate, opponent teams/ratings. Usage: python o_tools/live_episodes.py 56232526 56231047 ...
Writes o_results/live_episodes_<sid>.json and prints a per-submission summary."""
import json, sys, time, os, collections
import requests
LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "o_results")
NAMES = {"56232526":"c153","56231047":"c152","56219458":"c146","56219450":"c147","56209242":"c129","56204514":"c125"}
s = requests.Session(); s.headers["User-Agent"] = "kaggriculture-strategy-meta live audit"
for sid in sys.argv[1:]:
    for attempt in range(3):
        r = s.post(LIST_URL, json={"submissionId": int(sid)}, timeout=30)
        if r.status_code == 429: time.sleep(6); continue
        break
    r.raise_for_status()
    data = r.json(); eps = data.get("episodes", [])
    teams = {t["id"]: t.get("teamName") for t in data.get("teams", [])} if isinstance(data.get("teams"), list) else {}
    json.dump(data, open(os.path.join(OUT, f"live_episodes_{sid}.json"), "w", encoding="utf-8"))
    w=l=t=0; rows=[]; opp_scores=[]
    for e in eps:
        if e.get("state") != "COMPLETED": continue
        ag = e.get("agents", [])
        me = next((a for a in ag if str(a.get("submissionId")) == sid), None)
        op = next((a for a in ag if str(a.get("submissionId")) != sid), None)
        if not me or not op: continue
        mr, orw = me.get("reward"), op.get("reward")
        if mr is None or orw is None: continue
        res = "W" if mr > orw else ("L" if mr < orw else "T")
        w += res=="W"; l += res=="L"; t += res=="T"
        rows.append((res, mr-orw, op.get("submissionId"), teams.get(op.get("teamId"), op.get("teamId")), op.get("updatedScore"), me.get("updatedScore")))
        if op.get("updatedScore") is not None: opp_scores.append(op["updatedScore"])
    name = NAMES.get(sid, sid)
    print(f"\n=== {name} ({sid}): {len(rows)} completed episodes  W/L/T = {w}/{l}/{t}  tie-rate {t/max(1,len(rows)):.0%}  mean opp rating {sum(opp_scores)/max(1,len(opp_scores)):.0f}")
    for res, m, osid, oteam, osc, msc in sorted(rows, key=lambda x: x[1])[:12]:
        print(f"  {res} margin {m:8.0f}  vs {str(oteam)[:28]:28s} sub {osid} opp_rating {osc}  my_rating_after {msc}")
    if len(rows) > 12: print("  ...")
    time.sleep(1.5)
