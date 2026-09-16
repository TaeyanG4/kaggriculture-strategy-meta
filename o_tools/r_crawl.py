"""Incremental crawler + analysis for the reverse-engineering track (r series).

Runs unattended (Task Scheduler / manual). Everything is incremental and idempotent; state in
o_results/r_crawl/state.json. Output for humans/LLMs is ONE compact file:
o_results/r_crawl/latest_summary.md (read that instead of re-running analyses).

Stages (each skippable with --skip-<stage>):
  archive : new shards of ashok205/kaggriculture-top10-replay-archive -> replays of tracked
            teams into o_replays/archive_by_team/<team>/ (+_index.json per team)
  live    : our submissions' live episodes (public ListEpisodes API) -> rating-bucket win rates,
            new losses vs >= --elite-min into o_replays/elite_losses_new/ (the frozen 88-game
            suite in o_replays/elite_chunks is never modified)
  analyze : policy probe + phase ledger + divergence + terminal timing on the leader dir and the
            elite dirs -> compact summary
Usage: .venv/Scripts/python.exe o_tools/r_crawl.py [--teams Majkel1337,...] [--top 10]
"""
import argparse, collections, contextlib, glob, io, json, os, subprocess, sys, time, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
OUT = "o_results/r_crawl"; os.makedirs(OUT, exist_ok=True)
STATE = os.path.join(OUT, "state.json")
DATASET = "ashok205/kaggriculture-top10-replay-archive"
ARCHIVE_DIR = "state/o_dev/datasets/top10_archive"
LIST_URL = "https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes"
REPLAY_URL = "https://www.kaggleusercontent.com/episodes/{id}.json"
PY = sys.executable
log_lines = []


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"; print(line, flush=True); log_lines.append(line)


def load_state():
    return json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {"shards_done": [], "live_seen": {}, "runs": []}


def save_state(st):
    json.dump(st, open(STATE, "w", encoding="utf-8"), indent=1)


def kaggle(*args):
    return subprocess.run(["kaggle", *args], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout


# ---------------------------------------------------------------- archive
def crawl_archive(st, teams, top):
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    listing = kaggle("datasets", "files", DATASET)
    shards = sorted(l.split()[0] for l in listing.splitlines() if l.startswith("replays_") and l.split()[0].endswith(".parquet"))
    new = [s for s in shards if s not in st["shards_done"]]
    log(f"archive: {len(shards)} shards listed, {len(new)} new")
    if not new:
        return
    # refresh index
    kaggle("datasets", "download", DATASET, "-f", "episodes.parquet", "-p", ARCHIVE_DIR, "--force")
    for z in glob.glob(ARCHIVE_DIR + "/*.zip"):
        zipfile.ZipFile(z).extractall(ARCHIVE_DIR); os.remove(z)
    import pandas as pd
    ep = pd.read_parquet(ARCHIVE_DIR + "/episodes.parquet")
    if top:
        latest = ep[ep.date == ep.date.max()]
        top_teams = latest.sort_values("daily_rank").drop_duplicates("team_name").head(top).team_name.tolist()
        teams = sorted(set(teams) | set(top_teams))
    log(f"archive: tracking teams {teams}")
    for shard in new:
        need = ep[(ep.replay_shard == shard) & (ep.team_name.isin(teams))]
        if need.empty:
            st["shards_done"].append(shard); continue
        kaggle("datasets", "download", DATASET, "-f", shard, "-p", ARCHIVE_DIR)
        for z in glob.glob(ARCHIVE_DIR + "/*.zip"):
            zipfile.ZipFile(z).extractall(ARCHIVE_DIR); os.remove(z)
        path = os.path.join(ARCHIVE_DIR, shard)
        if not os.path.exists(path):
            log(f"archive: download failed {shard}"); continue
        r = pd.read_parquet(path); got = collections.Counter()
        for eid, js in zip(r.episode_id, r.replay_json):
            rep = json.loads(js); names = rep["info"]["TeamNames"]
            for team in names:
                if team not in teams: continue
                d = f"o_replays/archive_by_team/{team.replace('/', '_')}"; os.makedirs(d, exist_ok=True)
                p = f"{d}/{eid}-replay.json"
                if not os.path.exists(p):
                    open(p, "w", encoding="utf-8").write(js); got[team] += 1
                idxp = f"{d}/_index.json"; idx = json.load(open(idxp)) if os.path.exists(idxp) else []
                if not any(x["episode"] == int(eid) for x in idx):
                    seat = names.index(team); rw = [s["reward"] for s in rep["steps"][-1]]
                    idx.append(dict(episode=int(eid), my_seat=seat, margin=rw[seat] - rw[1 - seat], opp_team=names[1 - seat], opp_rating=0, lost=rw[seat] < rw[1 - seat], bank=rw[seat], shard=shard))
                    json.dump(idx, open(idxp, "w"), indent=0)
        os.remove(path)  # keep disk small; replays are now per-team files
        st["shards_done"].append(shard); save_state(st)
        log(f"archive: {shard} -> {dict(got)}")


# ---------------------------------------------------------------- live
def crawl_live(st, elite_min, max_new):
    import requests
    subs = kaggle("competitions", "submissions", "-c", "kaggriculture")
    ids = [l.split()[0] for l in subs.splitlines() if l.strip() and l.split()[0].isdigit() and "COMPLETE" in l][:6]
    s = requests.Session(); s.headers["User-Agent"] = "kaggriculture-strategy-meta r_crawl"
    summary = {}
    os.makedirs("o_replays/elite_losses_new", exist_ok=True)
    seen_eids = {os.path.basename(p).split("-")[0] for p in glob.glob("o_replays/elite_losses*/**/*-replay.json", recursive=True)}
    newidx_p = "o_replays/elite_losses_new/_index.json"; newidx = json.load(open(newidx_p)) if os.path.exists(newidx_p) else []
    got = 0
    for sid in ids:
        for attempt in range(3):
            r = s.post(LIST_URL, json={"submissionId": int(sid)}, timeout=30)
            if r.status_code == 429: time.sleep(8); continue
            break
        if r.status_code != 200:
            log(f"live: {sid} http {r.status_code}"); continue
        data = r.json(); json.dump(data, open(f"o_results/live_episodes_{sid}.json", "w", encoding="utf-8"))
        buckets = collections.defaultdict(lambda: [0, 0]); n = 0
        for e in data.get("episodes", []):
            if e.get("state") != "COMPLETED": continue
            ag = e.get("agents", []); me = next((a for a in ag if str(a.get("submissionId")) == sid), None); op = next((a for a in ag if str(a.get("submissionId")) != sid), None)
            if not me or not op or me.get("reward") is None or op.get("reward") is None: continue
            n += 1; rt = op.get("updatedScore") or 0
            b = "<2400" if rt < 2400 else ("2400-2749" if rt < 2750 else "2750+")
            buckets[b][0] += me["reward"] > op["reward"]; buckets[b][1] += 1
            eid = str(e["id"])
            if me["reward"] < op["reward"] and rt >= elite_min and eid not in seen_eids and got < max_new:
                rr = s.get(REPLAY_URL.format(id=eid), timeout=120)
                if rr.status_code == 200:
                    open(f"o_replays/elite_losses_new/{eid}-replay.json", "wb").write(rr.content); seen_eids.add(eid); got += 1
                    newidx.append(dict(episode=int(eid), sub=sid, lost=True, margin=me["reward"] - op["reward"], opp_team=op.get("teamId"), opp_rating=rt, my_seat=[i for i, x in enumerate(ag) if str(x.get("submissionId")) == sid][0]))
                    time.sleep(0.8)
        summary[sid] = {"episodes": n, **{b: f"{w}/{t}" for b, (w, t) in sorted(buckets.items())}}
        time.sleep(1.5)
    json.dump(newidx, open(newidx_p, "w"), indent=1)
    log(f"live: {summary}; new elite losses downloaded {got} (total new-dir {len(newidx)})")
    return summary


# ---------------------------------------------------------------- analyze
def run_capture(args):
    p = subprocess.run([PY, *args], capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return (p.stdout or "") + (("\nSTDERR: " + p.stderr[-800:]) if p.returncode else "")


def analyze(teams, live_summary):
    parts = [f"# r_crawl latest summary ({time.strftime('%Y-%m-%d %H:%M')})\n"]
    if live_summary:
        parts.append("## Live rating-bucket win rates (our submissions)\n```\n" + json.dumps(live_summary, indent=1) + "\n```\n")
    for team in teams:
        d = f"o_replays/archive_by_team/{team.replace('/', '_')}"
        if not os.path.exists(d + "/_index.json"): continue
        idx = json.load(open(d + "/_index.json")); n = len(idx); w = sum(1 for x in idx if not x["lost"])
        byo = collections.defaultdict(list)
        for x in idx: byo[x["opp_team"]].append(x["margin"])
        opp = sorted(byo.items(), key=lambda kv: -len(kv[1]))[:8]
        parts.append(f"## {team}: {n} games, W/L {w}/{n-w}, mean margin {sum(x['margin'] for x in idx)/max(1,n):+.0f}\n")
        parts.append("opponents: " + "; ".join(f"{o[:20]} n={len(m)} W={sum(1 for v in m if v>0)} mean {sum(m)/len(m):+.0f}" for o, m in opp) + "\n")
        for tool, tail in (("o_tools/r000_policy_probe.py", 22), ("o_tools/phase_ledger.py", 40)):
            out = run_capture([tool, d]).strip().splitlines()
            parts.append(f"### {os.path.basename(tool)}\n```\n" + "\n".join(out[-tail:]) + "\n```\n")
    for d in ("o_replays/elite_losses", "o_replays/elite_losses_new"):
        if os.path.exists(d + "/_index.json") and glob.glob(d + "/*-replay.json"):
            out = run_capture(["o_tools/elite_revenue.py", d]).strip().splitlines()
            parts.append(f"## {d}: executed revenue ours vs rival\n```\n" + "\n".join(out[-24:]) + "\n```\n")
    parts.append("## crawl log\n```\n" + "\n".join(log_lines) + "\n```\n")
    open(os.path.join(OUT, "latest_summary.md"), "w", encoding="utf-8").write("\n".join(parts))
    log("analyze: wrote " + os.path.join(OUT, "latest_summary.md"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--teams", default="Majkel1337"); ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--elite-min", type=float, default=2750); ap.add_argument("--max-new", type=int, default=40)
    ap.add_argument("--skip-archive", action="store_true"); ap.add_argument("--skip-live", action="store_true"); ap.add_argument("--skip-analyze", action="store_true")
    a = ap.parse_args()
    st = load_state(); teams = a.teams.split(",")
    live = None
    if not a.skip_archive:
        try: crawl_archive(st, teams, a.top)
        except Exception as e: log(f"archive failed: {e!r}")
    if not a.skip_live:
        try: live = crawl_live(st, a.elite_min, a.max_new)
        except Exception as e: log(f"live failed: {e!r}")
    if not a.skip_analyze:
        try: analyze(teams, live)
        except Exception as e: log(f"analyze failed: {e!r}")
    st["runs"].append({"t": time.strftime("%Y-%m-%d %H:%M"), "log": log_lines[-12:]}); st["runs"] = st["runs"][-30:]; save_state(st)


if __name__ == "__main__":
    main()
