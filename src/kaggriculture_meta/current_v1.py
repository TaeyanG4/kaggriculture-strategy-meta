from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

from .expanded_pilot import download_selected
from .pilot import extract_seat, write_csv
from .release_schema import build_v1_candidate
from .targeted_validation import select_quantile_grid


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()


def csv_row_count(path: Path) -> int:
    with path.open(encoding="utf-8", newline="") as f:
        return sum(1 for _ in csv.DictReader(f))


def daily_summary(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row["source_date"])].append(row)
    out = []
    for day, members in sorted(grouped.items()):
        families = Counter(r["strategy_family_pilot"] for r in members)
        cow = families["cow+strawberry"]
        out.append(
            {
                "source_date": day,
                "episodes": len({r["episode_id"] for r in members}),
                "seats": len(members),
                "cow_strawberry_seats": cow,
                "cow_strawberry_share": round(cow / len(members), 4) if members else None,
                "distinct_families": len(families),
                "distinct_openings_t24": len({r["opening_hash_t24"] for r in members}),
                "distinct_openings_t48": len({r["opening_hash_t48"] for r in members}),
                "mean_cash_t24": round(sum(float(r["cash_t24"]) for r in members) / len(members), 3),
                "mean_cash_t168": round(sum(float(r["cash_t168"]) for r in members) / len(members), 3),
                "mean_cash_t360": round(sum(float(r["cash_t360"]) for r in members) / len(members), 3),
                "mean_crop_strawberry_share": round(
                    sum(float(r["crop_strawberry_share"]) for r in members) / len(members), 6
                ),
                "mean_crop_tomato_share": round(
                    sum(float(r["crop_tomato_share"]) for r in members) / len(members), 6
                ),
                "mean_animal_cow_share": round(
                    sum(float(r["animal_cow_share"]) for r in members) / len(members), 6
                ),
                "mean_animal_goose_share": round(
                    sum(float(r["animal_goose_share"]) for r in members) / len(members), 6
                ),
                "mean_animal_sheep_share": round(
                    sum(float(r["animal_sheep_share"]) for r in members) / len(members), 6
                ),
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest-root", type=Path, default=Path("state/expanded_pilot/manifests"))
    ap.add_argument("--raw-root", type=Path, default=Path("state/expanded_pilot/raw"))
    ap.add_argument("--work-dir", type=Path, default=Path("state/expanded_pilot/current_v1"))
    ap.add_argument(
        "--release-csv",
        type=Path,
        default=Path("state/expanded_pilot/release_candidate/strategy_meta.csv"),
    )
    ap.add_argument("--report-dir", type=Path, default=Path("reports"))
    ap.add_argument("--samples-per-day", type=int, default=24)
    ap.add_argument("--days", nargs="+", required=True)
    args = ap.parse_args()

    started = time.time()
    builder_sha = git_head()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    args.report_dir.mkdir(parents=True, exist_ok=True)

    selection: list[dict] = []
    manifest_snapshots = []
    for day in args.days:
        manifest = args.manifest_root / day / "manifest.csv"
        if not manifest.exists():
            raise FileNotFoundError(manifest)
        chosen = select_quantile_grid(day, manifest, args.samples_per_day)
        selection.extend(chosen)
        manifest_snapshots.append(
            {
                "source_date": day,
                "source_dataset": f"kaggle/kaggriculture-episodes-{day}",
                "source_license": "CC0-1.0",
                "manifest_rows": csv_row_count(manifest),
                "manifest_sha256": sha256_file(manifest),
            }
        )
        print(f"select {day}: {len(chosen)} episodes", flush=True)
    write_csv(args.work_dir / "selection.csv", selection)
    print(f"current V1 selection: {len(selection)} episodes", flush=True)

    feature_rows: list[dict] = []
    failures = []
    source_bytes = 0
    engine_versions = Counter()
    rewards_checked = 0
    rewards_matched = 0
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
            for seat in (0, 1):
                row = extract_seat(eid, replay, seat, meta)
                row["source_date"] = meta["source_date"]
                row["score_band"] = meta["score_band"]
                row["sample_quantile"] = meta["sample_quantile"]
                row["manifest_avg_score"] = float(meta["avg_score"])
                row["manifest_min_score"] = float(meta["min_score"])
                row["source_dataset"] = meta["source_dataset"]
                row["source_license"] = meta["source_license"]
                if row.get("final_reward") is not None and row.get("ending_cash_observed") is not None:
                    rewards_checked += 1
                    if float(row["final_reward"]) == float(row["ending_cash_observed"]):
                        rewards_matched += 1
                feature_rows.append(row)
            print(
                f"parse {i}/{len(selection)} episode={eid} day={meta['source_date']} "
                f"q={meta['sample_quantile']:.3f} engine={engine}",
                flush=True,
            )
        except Exception as exc:
            failures.append({"episode_id": eid, "source_date": meta.get("source_date"), "error": str(exc)})
            print(f"parse {i}/{len(selection)} episode={eid} FAILED: {exc}", flush=True)

    feature_path = args.work_dir / "features.csv"
    write_csv(feature_path, feature_rows)
    qa = build_v1_candidate(feature_path, args.release_csv, args.report_dir / "current_v1_qa.json")
    daily = daily_summary(feature_rows)
    write_csv(args.report_dir / "current_v1_daily_summary.csv", daily)

    families = Counter(r["strategy_family_pilot"] for r in feature_rows)
    summary = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "builder_git_sha": builder_sha,
        "source_days": args.days,
        "samples_per_day": args.samples_per_day,
        "selected_episodes": len(selection),
        "parsed_episodes": len({r["episode_id"] for r in feature_rows}),
        "player_seats": len(feature_rows),
        "source_bytes": source_bytes,
        "parsing_failures": failures,
        "engine_versions": dict(engine_versions),
        "reward_cash_exact_matches": rewards_matched,
        "reward_cash_checked_seats": rewards_checked,
        "strategy_family_counts": dict(families),
        "distinct_openings_t24": len({r["opening_hash_t24"] for r in feature_rows}),
        "distinct_openings_t48": len({r["opening_hash_t48"] for r in feature_rows}),
        "release_rows": qa["row_count"],
        "release_columns": qa["column_count"],
        "release_bytes": qa["candidate_bytes"],
        "release_sha256": sha256_file(args.release_csv),
        "passes_core_qa": qa["passes_core_qa"],
        "runtime_seconds": round(time.time() - started, 3),
        "scope_note": (
            "Bounded current-meta V1 only. Each daily official CC0 manifest is sampled at 24 equally "
            "spaced quantile midpoints after sorting by avg_score. This is not a full-ladder population sample."
        ),
    }
    (args.report_dir / "current_v1_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    provenance = {
        "builder_git_sha": builder_sha,
        "build_timestamp_utc": summary["generated_at_utc"],
        "selection_rule": {
            "sort_key": "avg_score ascending within each official daily manifest",
            "samples_per_day": args.samples_per_day,
            "quantile_formula": "q=(i+0.5)/samples_per_day for i=0..samples_per_day-1",
        },
        "source_manifests": manifest_snapshots,
        "release_artifact": {
            "filename": "strategy_meta.csv",
            "rows": qa["row_count"],
            "columns": qa["column_count"],
            "bytes": qa["candidate_bytes"],
            "sha256": summary["release_sha256"],
        },
        "rights": {
            "source_license_expected": "CC0-1.0",
            "raw_replays_in_release": False,
            "raw_replays_in_git": False,
        },
        "qa": {
            "passes_core_qa": qa["passes_core_qa"],
            "duplicate_episode_seat_keys": qa["duplicate_episode_seat_keys"],
            "core_required_missing": qa["core_required_missing"],
            "invalid_share_values": qa["invalid_share_values"],
            "unicode_replacement_character_cells": qa["unicode_replacement_character_cells"],
        },
    }
    (args.report_dir / "current_v1_provenance.json").write_text(
        json.dumps(provenance, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
