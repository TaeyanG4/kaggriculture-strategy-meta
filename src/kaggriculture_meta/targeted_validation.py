from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path

from .expanded_pilot import download_selected, read_manifest
from .pilot import build_matchups, extract_seat, write_csv


RESOURCE_SHARE_FIELDS = [
    "crop_carrot_share",
    "crop_melon_share",
    "crop_strawberry_share",
    "crop_tomato_share",
    "crop_wheat_share",
    "animal_cow_share",
    "animal_goose_share",
    "animal_sheep_share",
]

CONTINUOUS_FIELDS = [
    "cash_t24",
    "cash_t72",
    "cash_t168",
    "cash_t360",
    "peak_cash",
    "total_hires_actual",
    "early_hires_actual",
    "early_plant_actions",
    "early_seed_units",
    "early_animal_units",
    "early_sell_units",
    *RESOURCE_SHARE_FIELDS,
]


def score_band_for_quantile(q: float) -> str:
    if q < 1 / 3:
        return "daily_low"
    if q < 2 / 3:
        return "daily_mid"
    return "daily_high"


def select_quantile_grid(day: str, manifest_path: Path, samples: int = 24) -> list[dict]:
    rows = read_manifest(manifest_path)
    if not rows:
        return []
    if samples < 3:
        raise ValueError("samples must be at least 3")
    rows.sort(key=lambda r: float(r["avg_score"]))
    n = len(rows)
    selected: list[dict] = []
    used: set[str] = set()
    for i in range(samples):
        q = (i + 0.5) / samples
        idx = round((n - 1) * q)
        row = dict(rows[idx])
        eid = row["episode_id"]
        if eid in used:
            continue
        used.add(eid)
        band = score_band_for_quantile(q)
        row.update(
            source_date=day,
            score_band=band,
            rating_band=band,
            sample_quantile=round(q, 6),
            source_dataset=f"kaggle/kaggriculture-episodes-{day}",
            source_license="CC0-1.0",
            source_class="official_kaggle_daily_cc0",
            end_time=row.get("create_time"),
        )
        selected.append(row)
    return selected


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> float:
    n1 = a + b
    n2 = c + d
    successes = a + c
    total = n1 + n2
    denominator = math.comb(total, n1)

    def prob(x: int) -> float:
        return math.comb(successes, x) * math.comb(total - successes, n1 - x) / denominator

    lo = max(0, n1 - (total - successes))
    hi = min(n1, successes)
    observed = prob(a)
    return min(1.0, sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= observed + 1e-15))


def aggregate_means(rows: list[dict], key: str, fields: list[str]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key) or "unknown")].append(row)
    out = []
    for group, members in sorted(grouped.items()):
        result = {key: group, "seats": len(members)}
        for field in fields:
            vals = [float(r[field]) for r in members if r.get(field) not in {None, ""}]
            result[f"mean_{field}"] = round(sum(vals) / len(vals), 6) if vals else None
        out.append(result)
    return out


def family_by_day(rows: list[dict]) -> list[dict]:
    grouped: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        grouped[str(row["source_date"])][str(row["strategy_family_pilot"])] += 1
    out = []
    for day, counts in sorted(grouped.items()):
        total = sum(counts.values())
        for family, seats in counts.most_common():
            out.append(
                {
                    "source_date": day,
                    "strategy_family": family,
                    "seats": seats,
                    "share": round(seats / total, 4),
                    "group_seats": total,
                }
            )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest-root", type=Path, default=Path("state/expanded_pilot/manifests"))
    ap.add_argument("--raw-root", type=Path, default=Path("state/expanded_pilot/raw"))
    ap.add_argument("--out-dir", type=Path, default=Path("reports"))
    ap.add_argument("--samples-per-day", type=int, default=24)
    ap.add_argument("--days", nargs="+", required=True)
    args = ap.parse_args()

    started = time.time()
    selection: list[dict] = []
    for day in args.days:
        manifest = args.manifest_root / day / "manifest.csv"
        chosen = select_quantile_grid(day, manifest, args.samples_per_day)
        print(f"select {day}: {len(chosen)} episodes", flush=True)
        selection.extend(chosen)
    write_csv(args.out_dir / "targeted_validation_selection.csv", selection)

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
            for seat in (0, 1):
                row = extract_seat(eid, replay, seat, meta)
                row["source_date"] = meta["source_date"]
                row["score_band"] = meta["score_band"]
                row["sample_quantile"] = meta["sample_quantile"]
                row["manifest_avg_score"] = float(meta["avg_score"])
                row["manifest_min_score"] = float(meta["min_score"])
                row["source_dataset"] = meta["source_dataset"]
                row["source_license"] = meta["source_license"]
                features.append(row)
            print(
                f"parse {i}/{len(selection)} episode={eid} day={meta['source_date']} "
                f"q={meta['sample_quantile']:.3f} engine={engine}",
                flush=True,
            )
        except Exception as exc:
            failures.append({"episode_id": eid, "source_date": meta.get("source_date"), "error": str(exc)})
            print(f"parse {i}/{len(selection)} episode={eid} FAILED: {exc}", flush=True)

    write_csv(args.out_dir / "targeted_validation_features.csv", features)
    episode_matchups, matchup_summary = build_matchups(features)
    write_csv(args.out_dir / "targeted_validation_episode_matchups.csv", episode_matchups)
    write_csv(args.out_dir / "targeted_validation_matchup_summary.csv", matchup_summary)
    write_csv(args.out_dir / "targeted_validation_family_by_day.csv", family_by_day(features))
    continuous = aggregate_means(features, "source_date", CONTINUOUS_FIELDS)
    write_csv(args.out_dir / "targeted_validation_continuous_by_day.csv", continuous)

    days = sorted({str(r["source_date"]) for r in features})
    cow = "cow+strawberry"
    family_counts = {
        day: Counter(r["strategy_family_pilot"] for r in features if r["source_date"] == day)
        for day in days
    }
    seats_by_day = {day: sum(family_counts[day].values()) for day in days}
    cow_shift = None
    resource_shift = {}
    if len(days) >= 2:
        first, last = days[0], days[-1]
        first_cow = family_counts[first][cow]
        last_cow = family_counts[last][cow]
        first_other = seats_by_day[first] - first_cow
        last_other = seats_by_day[last] - last_cow
        cow_shift = {
            "first_day": first,
            "last_day": last,
            "first_cow_strawberry_seats": first_cow,
            "first_total_seats": seats_by_day[first],
            "first_share": round(first_cow / seats_by_day[first], 4),
            "last_cow_strawberry_seats": last_cow,
            "last_total_seats": seats_by_day[last],
            "last_share": round(last_cow / seats_by_day[last], 4),
            "share_change_last_minus_first": round(
                last_cow / seats_by_day[last] - first_cow / seats_by_day[first], 4
            ),
            "fisher_two_sided_p": round(
                fisher_exact_two_sided(last_cow, last_other, first_cow, first_other), 6
            ),
        }
        by_day_means = {row["source_date"]: row for row in continuous}
        for field in RESOURCE_SHARE_FIELDS:
            first_mean = by_day_means[first].get(f"mean_{field}")
            last_mean = by_day_means[last].get(f"mean_{field}")
            if first_mean is not None and last_mean is not None:
                resource_shift[field] = round(float(last_mean) - float(first_mean), 6)

    opening_by_day = {}
    seat_win_by_day = {}
    for day in days:
        members = [r for r in features if r["source_date"] == day]
        opening_by_day[day] = {
            "seats": len(members),
            "distinct_t24": len({r["opening_hash_t24"] for r in members}),
            "distinct_t48": len({r["opening_hash_t48"] for r in members}),
        }
        games = [r for r in episode_matchups if r.get("source_date") == day]
        decided = [r for r in games if r["winner"] in {"seat0", "seat1"}]
        seat_win_by_day[day] = {
            "decided_games": len(decided),
            "seat0_win_rate": round(sum(r["winner"] == "seat0" for r in decided) / len(decided), 4)
            if decided else None,
        }

    summary = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source_days": days,
        "samples_per_day": args.samples_per_day,
        "selected_episodes": len(selection),
        "parsed_episodes": len({r["episode_id"] for r in features}),
        "player_seats": len(features),
        "source_bytes": source_bytes,
        "parsing_failures": failures,
        "engine_versions": dict(engine_versions),
        "family_counts_by_day": {day: dict(family_counts[day]) for day in days},
        "cow_strawberry_shift": cow_shift,
        "resource_share_mean_shift_last_minus_first": resource_shift,
        "opening_diversity_by_day": opening_by_day,
        "seat0_win_rate_by_day": seat_win_by_day,
        "matchup_pairs": len(matchup_summary),
        "cross_family_pairs_with_5plus_games_and_both_seats": sum(
            1
            for row in matchup_summary
            if row["strategy_family_A"] != row["strategy_family_B"]
            and int(row["games"]) >= 5
            and row.get("both_seat_orientations_observed") is True
        ),
        "runtime_seconds": round(time.time() - started, 3),
        "sampling_note": (
            "Each source day is sampled at equally spaced quantile midpoints across the official daily "
            "manifest sorted by avg_score. This validates change within the published daily elite slice; "
            "it is not a random estimate of the full ladder population."
        ),
        "rights_note": (
            "All replay payloads come from official Kaggle daily datasets reporting CC0-1.0. Raw and "
            "row-level targeted validation files remain local/ignored."
        ),
    }
    (args.out_dir / "targeted_validation_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
