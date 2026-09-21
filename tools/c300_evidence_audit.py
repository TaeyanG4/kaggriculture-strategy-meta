"""Read-only independent campaign recount and timestamped public episode snapshots."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(obj):
    raw = obj if isinstance(obj, bytes) else json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def campaign(folder):
    m = read(folder / "manifest.json")
    previous = read(folder / "results.json")
    failures = []
    by_model = defaultdict(list)
    physical = defaultdict(list)
    for role in ("models", "opponents"):
        for label, ref in m[role].items():
            if digest(Path(ref["path"]).read_bytes()) != ref["sha256"]:
                failures.append("source drift: " + label)
    for j in m["jobs"]:
        path = folder / "jobs" / j["match_id"] / "result.json"
        if not path.exists():
            failures.append("missing: " + j["match_id"])
            continue
        r = read(path)
        seat = j["candidate_seat"]
        margin = r["rewards"][seat] - r["rewards"][1-seat]
        outcome = "win" if margin > 0 else "loss" if margin < 0 else "tie"
        checks = (r["job_sha256"] == digest(j), r["candidate_sha256"] == j["candidate"]["sha256"],
                  r["opponent_sha256"] == j["opponent"]["sha256"], r["seed"] == j["seed"],
                  r["resolved_seed"] == j["seed"], r["candidate_seat"] == seat,
                  r["margin"] == margin, r["outcome"] == outcome, r["valid"],
                  r["statuses"] == ["DONE", "DONE"], r["states"] == 720,
                  not any(r["errors"]), not r.get("health_failures"))
        if not all(checks):
            failures.append("row mismatch: " + j["match_id"])
        by_model[j["candidate"]["name"]].append(r)
        hashes = [None, None]
        hashes[seat], hashes[1-seat] = j["candidate"]["sha256"], j["opponent"]["sha256"]
        physical[(j["seed"], *hashes)].append(r)
    model_stats = {}
    for label, rows in by_model.items():
        counts = Counter(r["outcome"] for r in rows)
        for field, wanted in (("games", len(rows)), ("wins", counts["win"]), ("losses", counts["loss"]), ("ties", counts["tie"])):
            if previous["by_candidate"][label][field] != wanted:
                failures.append(f"aggregate mismatch: {label}/{field}")
        other = [r for r in rows if r["candidate_sha256"] != r["opponent_sha256"]]
        model_stats[label] = dict(games=len(rows), outcomes=dict(counts),
            excluding_self_games=len(other), excluding_self_point_rate=statistics.mean(
                1 if r["margin"] > 0 else .5 if r["margin"] == 0 else 0 for r in other))
    duplicate_groups = [rs for rs in physical.values() if len(rs) > 1]
    disagreement = sum(any((r["rewards"], r["action_hashes"]) != (rs[0]["rewards"], rs[0]["action_hashes"])
                           for r in rs[1:]) for rs in duplicate_groups)
    return dict(campaign=folder.name, expected=m["expected_jobs"], rows=sum(map(len, by_model.values())),
                failures=failures, models=model_stats, unique_physical_conditions=len(physical),
                repeated_physical_conditions=len(duplicate_groups), repeated_condition_disagreements=disagreement,
                qualification="Recount of recorded rows, not replay or proof of current ladder strength")


def episodes(data, sid):
    rows = []
    for e in data.get("episodes", []):
        if e.get("state") != "COMPLETED":
            continue
        agents = e.get("agents", [])
        ours = [a for a in agents if a.get("submissionId") == sid]
        if len(ours) != 1 or len(agents) != 2:
            continue
        me = ours[0]
        rival = next(a for a in agents if a is not me)
        if me.get("reward") is None or rival.get("reward") is None:
            continue
        margin = me["reward"] - rival["reward"]
        rows.append(dict(id=e["id"], at=e.get("endTime") or e.get("createTime"),
                         outcome="W" if margin > 0 else "L" if margin < 0 else "T",
                         opponent_submission=rival.get("submissionId"),
                         opponent_score_after=rival.get("updatedScore"), score_after=me.get("updatedScore")))
    rows.sort(key=lambda r: r["at"])
    return dict(submission=sid, games=len(rows), outcomes=dict(Counter(r["outcome"] for r in rows)),
                latest=rows[-1] if rows else None,
                latest_30_outcomes=dict(Counter(r["outcome"] for r in rows[-30:])),
                peak_observed_score=max((r["score_after"] for r in rows if r["score_after"] is not None), default=None),
                limitation="Last observed post-match score, not current leaderboard or resubmission prediction",
                rows=rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--fetch", nargs="*", type=int, default=[])
    args = ap.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    audits = [campaign(ROOT / "state/agent_experiments" / name)
              for name in ("policy_compare_final", "policy_h2h_v2_screen", "policy_h2h_v2_confirm")]
    write(out / "campaigns.json", audits)
    for a in audits:
        print(json.dumps({k: v for k, v in a.items() if k not in ("models", "qualification")}), flush=True)
    if args.fetch:
        import requests
        for sid in args.fetch:
            stamp = datetime.now(timezone.utc).isoformat()
            r = requests.post("https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes",
                              json={"submissionId": sid}, timeout=30)
            write(out / f"episodes_{sid}_request.json", dict(fetched_at=stamp, status=r.status_code,
                  response_date=r.headers.get("Date"), sha256=digest(r.content), bytes=len(r.content)))
            r.raise_for_status()
            data = r.json()
            write(out / f"episodes_{sid}.json", data)
            summary = episodes(data, sid)
            write(out / f"episodes_{sid}_summary.json", summary)
            print(json.dumps({k: v for k, v in summary.items() if k != "rows"}), flush=True)


if __name__ == "__main__":
    main()
