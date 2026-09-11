from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def f(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in {"", None} else 0.0


def mean(rows: list[dict[str, str]], key: str) -> float:
    return sum(f(r, key) for r in rows) / len(rows) if rows else 0.0


def summarize_day(rows: list[dict[str, str]]) -> dict:
    families = Counter(r.get("strategy_family_pilot", "unknown") for r in rows)
    return {
        "seats": len(rows),
        "episodes": len({r["episode_id"] for r in rows}),
        "distinct_t24": len({r["opening_hash_t24"] for r in rows}),
        "distinct_t48": len({r["opening_hash_t48"] for r in rows}),
        "distinct_lineages": len({(r["opening_hash_t24"], r["opening_hash_t48"]) for r in rows}),
        "cow_strawberry_share": families.get("cow+strawberry", 0) / len(rows) if rows else 0.0,
        "mean_first_land_turn": mean(rows, "first_land_turn"),
        "mean_first_hire_turn": mean(rows, "first_hire_turn"),
        "mean_first_sell_turn": mean(rows, "first_sell_turn"),
        "mean_strawberry_share": mean(rows, "crop_strawberry_share"),
        "mean_tomato_share": mean(rows, "crop_tomato_share"),
        "mean_cow_share": mean(rows, "animal_cow_share"),
        "mean_goose_share": mean(rows, "animal_goose_share"),
        "mean_sheep_share": mean(rows, "animal_sheep_share"),
        "mean_market_sell_orders": mean(rows, "market_sell_orders"),
        "mean_market_sell_units": mean(rows, "market_sell_units"),
        "mean_total_hires": mean(rows, "total_hires_actual"),
    }


def lineage_table(rows: list[dict[str, str]]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["opening_hash_t24"], row["opening_hash_t48"])].append(row)
    out = []
    for (h24, h48), members in grouped.items():
        days = sorted({r["source_date"] for r in members})
        fam = Counter(r.get("strategy_family_pilot", "unknown") for r in members)
        out.append(
            {
                "opening_hash_t24": h24,
                "opening_hash_t48": h48,
                "first_seen": days[0],
                "last_seen": days[-1],
                "seat_count": len(members),
                "day_count": len(days),
                "dominant_family": fam.most_common(1)[0][0],
                "dominant_family_share": round(fam.most_common(1)[0][1] / len(members), 4),
            }
        )
    return sorted(out, key=lambda r: (r["first_seen"], -r["seat_count"], r["opening_hash_t24"], r["opening_hash_t48"]))


def build(features_csv: Path, out_dir: Path, report_date: str, source_status: str) -> None:
    rows = read_rows(features_csv)
    if not rows:
        raise ValueError("features csv has no rows")
    out_dir.mkdir(parents=True, exist_ok=True)
    days = sorted({r["source_date"] for r in rows})
    latest = days[-1]
    previous = days[-2] if len(days) >= 2 else latest
    by_day = {d: [r for r in rows if r["source_date"] == d] for d in days}
    prev_summary = summarize_day(by_day[previous])
    latest_summary = summarize_day(by_day[latest])
    lineages = lineage_table(rows)

    new = [r for r in lineages if r["first_seen"] == latest]
    disappearing = [r for r in lineages if r["seat_count"] >= 2 and r["last_seen"] <= previous]
    latest_lineage_keys = {(r["opening_hash_t24"], r["opening_hash_t48"]) for r in by_day[latest]}
    disappearing = [r for r in disappearing if (r["opening_hash_t24"], r["opening_hash_t48"]) not in latest_lineage_keys]

    fields = [
        "opening_hash_t24", "opening_hash_t48", "first_seen", "last_seen",
        "seat_count", "day_count", "dominant_family", "dominant_family_share",
    ]
    csv_path = out_dir / f"new-fingerprints-{report_date}.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fobj:
        w = csv.DictWriter(fobj, fieldnames=fields)
        w.writeheader()
        w.writerows(new)

    changes = {
        key: round(latest_summary[key] - prev_summary[key], 6)
        for key in [
            "cow_strawberry_share", "mean_first_land_turn", "mean_first_hire_turn",
            "mean_first_sell_turn", "mean_strawberry_share", "mean_tomato_share",
            "mean_cow_share", "mean_goose_share", "mean_sheep_share",
            "mean_market_sell_orders", "mean_market_sell_units", "mean_total_hires",
        ]
    }
    summary = {
        "report_date": report_date,
        "source_status": source_status,
        "window_start": days[0],
        "window_end": latest,
        "window_days": len(days),
        "episodes": len({r["episode_id"] for r in rows}),
        "seats": len(rows),
        "comparison_day": previous,
        "latest_day": latest,
        "previous_summary": prev_summary,
        "latest_summary": latest_summary,
        "latest_minus_previous": changes,
        "new_lineage_count": len(new),
        "disappearing_lineage_count": len(disappearing),
        "new_lineages": new[:25],
        "disappearing_lineages": sorted(disappearing, key=lambda r: (-r["seat_count"], r["last_seen"]))[:25],
        "identity_caveat": "Opening hashes are behavior fingerprints, not submission or agent identities.",
    }
    (out_dir / f"meta-refresh-{report_date}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    def pp_delta(key: str, scale: float = 100.0) -> str:
        return f"{changes[key] * scale:+.2f} pp"

    lines = [
        f"# Kaggriculture Daily Meta Refresh — {report_date}",
        "",
        "## Source status",
        "",
        f"- {source_status}",
        f"- Reconstructed bounded window: {days[0]} through {latest}; {len(days)} days, {summary['episodes']} episodes, {summary['seats']} seats.",
        "- Sampling remains the Core-approved 24 deterministic manifest-score quantile midpoints per day.",
        "- Raw replay payloads are not copied into the shared handoff.",
        "- Opening hashes below are behavioral fingerprints only; they are not guaranteed submission identities.",
        "",
        f"## What changed from {previous} to {latest}",
        "",
        f"- cow+strawberry share: {prev_summary['cow_strawberry_share']:.1%} -> {latest_summary['cow_strawberry_share']:.1%} ({pp_delta('cow_strawberry_share')})",
        f"- strawberry tile-turn share: {prev_summary['mean_strawberry_share']:.1%} -> {latest_summary['mean_strawberry_share']:.1%} ({pp_delta('mean_strawberry_share')})",
        f"- goose tile-turn share: {prev_summary['mean_goose_share']:.1%} -> {latest_summary['mean_goose_share']:.1%} ({pp_delta('mean_goose_share')})",
        f"- sheep tile-turn share: {prev_summary['mean_sheep_share']:.1%} -> {latest_summary['mean_sheep_share']:.1%} ({pp_delta('mean_sheep_share')})",
        f"- mean first land turn: {prev_summary['mean_first_land_turn']:.1f} -> {latest_summary['mean_first_land_turn']:.1f} ({changes['mean_first_land_turn']:+.1f})",
        f"- mean first hire turn: {prev_summary['mean_first_hire_turn']:.1f} -> {latest_summary['mean_first_hire_turn']:.1f} ({changes['mean_first_hire_turn']:+.1f})",
        f"- mean first sell turn: {prev_summary['mean_first_sell_turn']:.1f} -> {latest_summary['mean_first_sell_turn']:.1f} ({changes['mean_first_sell_turn']:+.1f})",
        f"- mean sell orders: {prev_summary['mean_market_sell_orders']:.1f} -> {latest_summary['mean_market_sell_orders']:.1f} ({changes['mean_market_sell_orders']:+.1f})",
        f"- distinct t24/t48 lineage pairs: {prev_summary['distinct_lineages']} -> {latest_summary['distinct_lineages']}",
        "",
        "## Freshness / lineage read",
        "",
        f"- New lineage fingerprints first seen on {latest}: {len(new)}.",
        f"- Repeated lineage fingerprints absent on {latest}: {len(disappearing)} (requires >=2 historical seats).",
        "- This is evidence of opening-behavior churn, not proof that one named agent replaced another.",
        "- No robust early standalone winner predictor was established by prior V1 analysis; this refresh does not reinterpret fingerprint freshness as causal strength.",
        "",
        "## New-generation vs old-generation evidence",
        "",
        "The bounded sample can show that newer fingerprints appear and older repeated fingerprints disappear, but it does not yet establish that a newer generation beats an older generation. A defensible superiority claim would require repeated cross-lineage matchups with seat balance or controlled local benchmarks.",
        "",
        "## NEW STRATEGIES:",
        f"{len(new)} opening-hash lineage candidates first appeared on {latest}. See `new-fingerprints-{report_date}.csv`. Treat these as candidate behaviors, not identities.",
        "",
        "## DISAPPEARING / STALE STRATEGIES:",
        f"{len(disappearing)} repeated historical lineage candidates were absent on {latest}. Absence in one 24-episode daily quantile sample is a staleness signal only, not proof of retirement.",
        "",
        "## MEANINGFUL RESOURCE/OPENING SHIFTS:",
        f"The clearest day-over-day movement is goose allocation {pp_delta('mean_goose_share')}, sheep {pp_delta('mean_sheep_share')}, strawberry {pp_delta('mean_strawberry_share')}, with lineage-pair diversity {prev_summary['distinct_lineages']} -> {latest_summary['distinct_lineages']}.",
        "",
        "## NEW OPPONENTS CORE SHOULD BENCHMARK:",
        "Prioritize reproducible public agents whose observed behavior matches the newest high-frequency lineage candidates. The current official daily slice alone does not expose a defensible executable agent identity, so no new named opponent is promoted from this refresh.",
        "",
        "## POSSIBLE AGENT ADAPTATION IMPLICATION:",
        "Core should keep benchmarks robust to increasing goose allocation and opening-fingerprint churn, but should not retune solely from this descriptive daily sample. Promote a meta shift into agent changes only after controlled benchmark evidence.",
    ]
    (out_dir / f"meta-refresh-{report_date}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--features-csv", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--report-date", required=True)
    ap.add_argument("--source-status", required=True)
    args = ap.parse_args()
    build(args.features_csv, args.out_dir, args.report_date, args.source_status)


if __name__ == "__main__":
    main()
