from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

from .pilot import build_matchups, extract_seat, write_csv


QUANTILE_POINTS = {
    "daily_low": (0.10, 0.20),
    "daily_mid": (0.45, 0.55),
    "daily_high": (0.80, 0.90),
}


def read_manifest(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def select_day(day: str, manifest_path: Path) -> list[dict]:
    rows = read_manifest(manifest_path)
    if not rows:
        return []
    rows.sort(key=lambda r: float(r["avg_score"]))
    n = len(rows)
    selected: list[dict] = []
    used: set[str] = set()
    for band, points in QUANTILE_POINTS.items():
        for q in points:
            idx = round((n - 1) * q)
            row = dict(rows[idx])
            eid = row["episode_id"]
            if eid in used:
                continue
            used.add(eid)
            row.update(
                source_date=day,
                score_band=band,
                source_dataset=f"kaggle/kaggriculture-episodes-{day}",
                source_license="CC0-1.0",
                source_class="official_kaggle_daily_cc0",
                rating_band=band,
                end_time=row.get("create_time"),
            )
            selected.append(row)
    return selected


def download_selected(row: dict, raw_root: Path) -> Path:
    day = row["source_date"]
    eid = row["episode_id"]
    out_dir = raw_root / day
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{eid}.json"
    if out_path.exists() and out_path.stat().st_size > 0:
        return out_path
    cmd = [
        "kaggle",
        "datasets",
        "download",
        row["source_dataset"],
        "-f",
        f"{eid}.json",
        "-p",
        str(out_dir),
    ]
    subprocess.run(cmd, check=True)
    if not out_path.exists() or out_path.stat().st_size == 0:
        raise RuntimeError(f"expected replay not found after Kaggle CLI download: {out_path}")
    return out_path


def family_distribution(rows: list[dict], key: str) -> list[dict]:
    groups: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        groups[str(row.get(key) or "unknown")][row["strategy_family_pilot"]] += 1
    out = []
    for group, counts in sorted(groups.items()):
        total = sum(counts.values())
        for family, count in counts.most_common():
            out.append(
                {
                    key: group,
                    "strategy_family": family,
                    "seats": count,
                    "share": round(count / total, 4) if total else 0.0,
                    "group_seats": total,
                }
            )
    return out


def repeated_agent_stability(rows: list[dict]) -> dict:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        agent = str(row.get("agent_name") or "").strip()
        if agent:
            groups[agent].append(row["strategy_family_pilot"])
    repeated = {agent: families for agent, families in groups.items() if len(families) >= 2}
    majority_shares = []
    perfect = 0
    for families in repeated.values():
        counts = Counter(families)
        share = max(counts.values()) / len(families)
        majority_shares.append(share)
        if share == 1.0:
            perfect += 1
    return {
        "named_agents": len(groups),
        "repeated_agents": len(repeated),
        "repeated_agent_seats": sum(len(v) for v in repeated.values()),
        "perfect_family_stability_agents": perfect,
        "perfect_family_stability_share": round(perfect / len(repeated), 4) if repeated else None,
        "mean_majority_family_share": round(sum(majority_shares) / len(majority_shares), 4) if majority_shares else None,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest-root", type=Path, default=Path("state/expanded_pilot/manifests"))
    ap.add_argument("--raw-root", type=Path, default=Path("state/expanded_pilot/raw"))
    ap.add_argument("--out-dir", type=Path, default=Path("reports"))
    ap.add_argument("--days", nargs="+", required=True)
    args = ap.parse_args()

    started = time.time()
    selection: list[dict] = []
    for day in args.days:
        manifest = args.manifest_root / day / "manifest.csv"
        if not manifest.exists():
            raise FileNotFoundError(manifest)
        chosen = select_day(day, manifest)
        print(f"select {day}: {len(chosen)} episodes", flush=True)
        selection.extend(chosen)

    write_csv(args.out_dir / "expanded_pilot_selection.csv", selection)
    print(f"expanded pilot selection: {len(selection)} episodes", flush=True)

    features: list[dict] = []
    failures: list[dict] = []
    source_bytes = 0
    engine_versions = Counter()
    for i, meta in enumerate(selection, 1):
        eid = meta["episode_id"]
        try:
            path = download_selected(meta, args.raw_root)
            source_bytes += path.stat().st_size
            with path.open(encoding="utf-8") as f:
                replay = json.load(f)
            steps = replay.get("steps") or []
            if not steps:
                raise ValueError("no replay steps")
            engine = str(replay.get("module_version"))
            engine_versions[engine] += 1
            agents = (replay.get("info") or {}).get("Agents") or []
            for seat in (0, 1):
                row = extract_seat(eid, replay, seat, meta)
                row["agent_name"] = agents[seat] if seat < len(agents) else None
                row["source_date"] = meta["source_date"]
                row["score_band"] = meta["score_band"]
                row["manifest_avg_score"] = float(meta["avg_score"])
                row["manifest_min_score"] = float(meta["min_score"])
                row["source_dataset"] = meta["source_dataset"]
                row["source_license"] = meta["source_license"]
                features.append(row)
            print(
                f"parse {i}/{len(selection)} episode={eid} day={meta['source_date']} "
                f"band={meta['score_band']} turns={len(steps)} engine={engine}",
                flush=True,
            )
        except Exception as exc:
            failures.append({"episode_id": eid, "source_date": meta.get("source_date"), "error": str(exc)})
            print(f"parse {i}/{len(selection)} episode={eid} FAILED: {exc}", flush=True)

    feature_path = args.out_dir / "expanded_pilot_features.csv"
    write_csv(feature_path, features)
    episode_matchups, matchup_summary = build_matchups(features)
    write_csv(args.out_dir / "expanded_pilot_episode_matchups.csv", episode_matchups)
    write_csv(args.out_dir / "expanded_pilot_matchup_summary.csv", matchup_summary)
    write_csv(args.out_dir / "expanded_pilot_family_by_day.csv", family_distribution(features, "source_date"))
    write_csv(args.out_dir / "expanded_pilot_family_by_score_band.csv", family_distribution(features, "score_band"))

    family_counts = Counter(r["strategy_family_pilot"] for r in features)
    opening24 = Counter(r["opening_hash_t24"] for r in features)
    opening48 = Counter(r["opening_hash_t48"] for r in features)
    supported_matchups = [r for r in matchup_summary if int(r["games"]) >= 5]
    decided = [r for r in episode_matchups if r["winner"] in {"seat0", "seat1"}]
    same_family_decided = [r for r in decided if r["family_0"] == r["family_1"]]
    reward_cash_matches = sum(
        1
        for r in features
        if r.get("final_reward") is not None
        and r.get("ending_cash_observed") is not None
        and float(r["final_reward"]) == float(r["ending_cash_observed"])
    )
    summary = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_days": args.days,
        "selected_episodes": len(selection),
        "parsed_episodes": len({r["episode_id"] for r in features}),
        "player_seats": len(features),
        "source_bytes": source_bytes,
        "parsing_failures": failures,
        "engine_versions": dict(engine_versions),
        "strategy_family_counts": dict(family_counts),
        "distinct_strategy_families": len(family_counts),
        "distinct_openings_t24": len(opening24),
        "distinct_openings_t48": len(opening48),
        "largest_opening_t24_share": round(max(opening24.values()) / len(features), 4) if features else None,
        "largest_opening_t48_share": round(max(opening48.values()) / len(features), 4) if features else None,
        "matchup_pairs": len(matchup_summary),
        "matchup_pairs_with_5plus_games": len(supported_matchups),
        "seat0_win_rate": round(sum(r["winner"] == "seat0" for r in decided) / len(decided), 4) if decided else None,
        "same_family_seat0_win_rate": round(
            sum(r["winner"] == "seat0" for r in same_family_decided) / len(same_family_decided), 4
        ) if same_family_decided else None,
        "reward_cash_exact_matches": reward_cash_matches,
        "reward_cash_checked_seats": sum(
            r.get("final_reward") is not None and r.get("ending_cash_observed") is not None for r in features
        ),
        "repeated_agent_family_stability": repeated_agent_stability(features),
        "derived_feature_bytes": feature_path.stat().st_size if feature_path.exists() else 0,
        "runtime_seconds": round(time.time() - started, 3),
        "sampling_note": (
            "Each official daily CC0 manifest is sorted by avg_score and sampled at fixed 10/20, "
            "45/55, and 80/90 percentiles. Bands are relative to Kaggle's published daily elite slice, "
            "not the full competition ladder."
        ),
        "rights_note": (
            "All expanded-pilot replay payloads are downloaded through Kaggle CLI from official "
            "kaggle/kaggriculture-episodes-YYYY-MM-DD datasets reporting CC0-1.0. Raw replays remain local."
        ),
    }
    (args.out_dir / "expanded_pilot_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
