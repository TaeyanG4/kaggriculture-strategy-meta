"""Read-only compact research receipts. Never prints replays or source blobs.

Usage: python tools/research_brief.py c686 [--economics] [--limit 12]
All player totals are selected by their explicit seat, not list position.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    with Path(path).open(encoding="utf-8-sig") as stream:
        return json.load(stream)


def selected(value, keys):
    return {key: value[key] for key in keys if key in value}


def delta(left, right):
    return {key: right.get(key, 0) - left.get(key, 0)
            for key in sorted(left.keys() | right.keys())
            if right.get(key, 0) != left.get(key, 0)}


def total_for_seat(document, seat):
    matches = [item for item in document["totals"] if item["seat"] == seat]
    if len(matches) != 1:
        raise ValueError(f"Expected one total for seat {seat}")
    return matches[0]


def resolve(path):
    result = Path(path)
    return result if result.is_absolute() else ROOT / result


def economics(row):
    job = row["job"]
    document = read(resolve(row["ledger"]))
    own = total_for_seat(document, job["seat"])
    rival = total_for_seat(document, 1 - job["seat"])
    return dict(
        own_seat=job["seat"], margin=own["final_cash"] - rival["final_cash"],
        own_cash=own["final_cash"], rival_cash=rival["final_cash"],
        own_minus_rival_operations=delta(rival["cash_delta_by_operation"], own["cash_delta_by_operation"]),
        own_minus_rival_production=delta(rival["harvested_and_collected"], own["harvested_and_collected"]),
        own_minus_rival_consumption=delta(rival["feed_and_fertilizer_consumed"], own["feed_and_fertilizer_consumed"]),
        cash_residuals=[own["cash_residual"], rival["cash_residual"]],
    )


def brief(campaign, include_economics=False, limit=12):
    folder = (ROOT / "state" / campaign).resolve()
    if folder.parent != (ROOT / "state").resolve() or not folder.is_dir():
        raise ValueError("Use an existing direct campaign directory, e.g. c686")
    output = {"campaign": campaign}
    for name in ["review-decision", "completion-ready", "adoption-complete", "submission-receipt"]:
        path = folder / (name + ".json")
        if path.exists():
            obj = read(path)
            output[name] = selected(obj, [
                "at", "decision", "status", "baseline", "source_sha256", "submission_id",
                "cases", "exact_actions", "exact", "new_native", "new_matches", "new_games",
                "total", "cached_games", "overall", "combined", "own_mean", "margin_mean",
                "gained_wins", "lost_wins", "new_ineffective", "execution_pass", "cycle_execution_pass",
                "allvalid_import_verified", "unique_games", "qa_pass", "adopted", "submitted",
                "stage1_supported", "precommitted_stage2_not_launched",
            ])
    errors = sorted(folder.glob("*error*.json"))
    output["error_receipts"] = [p.name for p in errors]
    output["completed_files"] = {
        name: sum(1 for _ in (folder / name).glob("*.json"))
        for name in ["games", "audits", "comparisons"] if (folder / name).is_dir()
    }
    diagnostic = folder / "diagnostic-summary.json"
    development = folder / "development-summary.json"
    if diagnostic.exists():
        data = read(diagnostic)
        rows = data.get("rows", [])
        output["rows_total"] = len(rows)
        output["rows"] = []
        for row in rows[:limit]:
            item = selected(row, [
                "episode", "first_difference", "own_delta", "margin_delta", "actual_margin",
                "alternative_margin", "reference_margin", "current_margin", "exact_actions",
                "exact_current_actions", "cycle_execution_pass", "new_native",
            ])
            if "new_ineffective" in row:
                item["new_ineffective_count"] = len(row["new_ineffective"])
            item["service_event_counts"] = {
                name: {key: len(value) if isinstance(value, list) else value
                       for key, value in service.items() if isinstance(value, (int, float, bool, list))}
                for name, service in row.get("service", {}).items() if isinstance(service, dict)
            }
            captured = row.get("current_row", row.get("row"))
            if include_economics and captured:
                item["economics"] = economics(captured)
            output["rows"].append(item)
    elif development.exists():
        rows = read(development).get("conditions", [])
        output["rows_total"] = len(rows)
        output["rows"] = [selected(row, [
            "seed", "seat", "episode", "opponent", "own", "margin", "parent_margin",
            "candidate_margin", "win_lost", "win_gained"
        ]) for row in rows[:limit]]
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign")
    parser.add_argument("--economics", action="store_true")
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()
    if not 0 <= args.limit <= 24:
        parser.error("--limit must be between 0 and 24")
    print(json.dumps(brief(args.campaign, args.economics, args.limit), ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
