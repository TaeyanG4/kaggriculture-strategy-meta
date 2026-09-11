from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


V1_FIELD_MAP = [
    ("source_dataset", "source_dataset"),
    ("source_license", "source_license"),
    ("source_date", "source_date"),
    ("episode_id", "episode_id"),
    ("episode_date", "episode_date"),
    ("seat", "seat"),
    ("engine_version", "engine_version"),
    ("turns", "turns"),
    ("final_reward", "final_reward"),
    ("manifest_avg_score", "manifest_avg_score"),
    ("manifest_min_score", "manifest_min_score"),
    ("source_score_quantile", "sample_quantile"),
    ("cash_t24", "cash_t24"),
    ("cash_t72", "cash_t72"),
    ("cash_t168", "cash_t168"),
    ("cash_t360", "cash_t360"),
    ("peak_cash", "peak_cash"),
    ("first_land_turn", "first_land_turn"),
    ("first_hire_turn", "first_hire_turn"),
    ("first_plant_turn", "first_plant_turn"),
    ("first_sell_turn", "first_sell_turn"),
    ("first_animal_turn", "first_animal_turn"),
    ("total_hires_actual", "total_hires_actual"),
    ("early_hires_actual", "early_hires_actual"),
    ("early_plant_actions", "early_plant_actions"),
    ("early_seed_units", "early_seed_units"),
    ("early_animal_units", "early_animal_units"),
    ("early_sell_units", "early_sell_units"),
    ("early_dominant_crop", "early_dominant_crop"),
    ("early_dominant_crop_share", "early_dominant_crop_share"),
    ("opening_hash_t24", "opening_hash_t24"),
    ("opening_hash_t48", "opening_hash_t48"),
    ("crop_carrot_share", "crop_carrot_share"),
    ("crop_melon_share", "crop_melon_share"),
    ("crop_strawberry_share", "crop_strawberry_share"),
    ("crop_tomato_share", "crop_tomato_share"),
    ("crop_wheat_share", "crop_wheat_share"),
    ("animal_cow_share", "animal_cow_share"),
    ("animal_goose_share", "animal_goose_share"),
    ("animal_sheep_share", "animal_sheep_share"),
    ("total_market_orders", "total_market_orders"),
    ("total_unit_actions", "total_unit_actions"),
    ("market_buy_seed_units", "market_buy_seed_units"),
    ("market_buy_animal_units", "market_buy_animal_units"),
    ("market_sell_units", "market_sell_units"),
    ("strategy_family_experimental", "strategy_family_pilot"),
]

V1_COLUMNS = [out for out, _ in V1_FIELD_MAP]

EXCLUDED_IDENTITY_FIELDS = {"team_id", "submission_id", "agent_name", "rating_after"}

CORE_REQUIRED_FIELDS = {
    "source_dataset",
    "source_license",
    "source_date",
    "episode_id",
    "seat",
    "engine_version",
    "turns",
    "final_reward",
    "manifest_avg_score",
    "manifest_min_score",
    "source_score_quantile",
}

SHARE_FIELDS = [
    "crop_carrot_share",
    "crop_melon_share",
    "crop_strawberry_share",
    "crop_tomato_share",
    "crop_wheat_share",
    "animal_cow_share",
    "animal_goose_share",
    "animal_sheep_share",
]

GEORGY_SEMANTIC_OVERLAP = {
    "final_reward": "final_money",
    "total_hires_actual": "total_hires",
    "first_land_turn": "first_land_day",
}


def project_v1(row: dict) -> dict:
    return {out: row.get(source) for out, source in V1_FIELD_MAP}


def read_header(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as f:
        return next(csv.reader(f))


def compare_with_georgy(candidate_columns: list[str], georgy_columns: list[str]) -> dict:
    exact = sorted(set(candidate_columns) & set(georgy_columns))
    semantic = {
        ours: theirs
        for ours, theirs in GEORGY_SEMANTIC_OVERLAP.items()
        if ours in candidate_columns and theirs in georgy_columns
    }
    fingerprint_specific = [
        c
        for c in candidate_columns
        if c.startswith(("cash_t", "first_", "crop_", "animal_", "early_", "market_"))
        or c in {"opening_hash_t24", "opening_hash_t48", "total_market_orders", "total_unit_actions"}
    ]
    return {
        "candidate_columns": len(candidate_columns),
        "closest_alternative_episode_feature_columns": len(georgy_columns),
        "exact_name_overlap": exact,
        "semantic_overlap": semantic,
        "candidate_fingerprint_columns": fingerprint_specific,
        "candidate_fingerprint_column_count": len(fingerprint_specific),
        "note": (
            "The alternative also publishes a separate stream_hashes table, so exact opening hashes are "
            "conceptually overlapping even though they are not columns of episode_features.csv. The V1 "
            "differentiator is the single-row combination of timing, cash checkpoints, actual tile-turn "
            "resource shares, semantic action totals, provenance, and opening fingerprints."
        ),
    }


def write_comparison(georgy_csv: Path, out_json: Path) -> dict:
    comparison = compare_with_georgy(V1_COLUMNS, read_header(georgy_csv))
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    return comparison


def build_v1_candidate(source_csv: Path, out_csv: Path, qa_json: Path) -> dict:
    with source_csv.open(encoding="utf-8", newline="") as f:
        source_rows = list(csv.DictReader(f))
    rows = [project_v1(row) for row in source_rows]

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=V1_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    key_counts = Counter((row["episode_id"], row["seat"]) for row in rows)
    duplicate_keys = sum(1 for count in key_counts.values() if count > 1)
    missing_counts = {
        field: sum(row.get(field) in {None, ""} for row in rows)
        for field in V1_COLUMNS
    }
    invalid_share_values = 0
    crop_sum_deviations = []
    animal_sum_deviations = []
    for row in rows:
        for field in SHARE_FIELDS:
            value = row.get(field)
            if value in {None, ""}:
                continue
            number = float(value)
            if number < 0.0 or number > 1.0:
                invalid_share_values += 1
        crop_values = [float(row[f]) for f in SHARE_FIELDS[:5] if row.get(f) not in {None, ""}]
        animal_values = [float(row[f]) for f in SHARE_FIELDS[5:] if row.get(f) not in {None, ""}]
        if crop_values and sum(crop_values) > 0:
            crop_sum_deviations.append(abs(sum(crop_values) - 1.0))
        if animal_values and sum(animal_values) > 0:
            animal_sum_deviations.append(abs(sum(animal_values) - 1.0))

    replacement_character_cells = sum(
        "\ufffd" in str(value)
        for row in rows
        for value in row.values()
        if value is not None
    )
    qa = {
        "row_count": len(rows),
        "column_count": len(V1_COLUMNS),
        "unique_episodes": len({row["episode_id"] for row in rows}),
        "duplicate_episode_seat_keys": duplicate_keys,
        "source_days": sorted({row["source_date"] for row in rows}),
        "source_license_counts": dict(Counter(row["source_license"] for row in rows)),
        "engine_version_counts": dict(Counter(row["engine_version"] for row in rows)),
        "core_required_missing": {
            field: missing_counts[field] for field in sorted(CORE_REQUIRED_FIELDS) if missing_counts[field]
        },
        "all_missing_counts": missing_counts,
        "invalid_share_values": invalid_share_values,
        "max_crop_share_sum_abs_error": round(max(crop_sum_deviations), 6) if crop_sum_deviations else None,
        "max_animal_share_sum_abs_error": round(max(animal_sum_deviations), 6) if animal_sum_deviations else None,
        "excluded_identity_fields_present": sorted(EXCLUDED_IDENTITY_FIELDS & set(V1_COLUMNS)),
        "unicode_replacement_character_cells": replacement_character_cells,
        "candidate_bytes": out_csv.stat().st_size,
    }
    qa["passes_core_qa"] = (
        qa["duplicate_episode_seat_keys"] == 0
        and not qa["core_required_missing"]
        and qa["source_license_counts"] == {"CC0-1.0": len(rows)}
        and qa["invalid_share_values"] == 0
        and (qa["max_crop_share_sum_abs_error"] is None or qa["max_crop_share_sum_abs_error"] <= 0.001)
        and (qa["max_animal_share_sum_abs_error"] is None or qa["max_animal_share_sum_abs_error"] <= 0.001)
        and not qa["excluded_identity_fields_present"]
        and qa["unicode_replacement_character_cells"] == 0
    )
    qa_json.parent.mkdir(parents=True, exist_ok=True)
    qa_json.write_text(json.dumps(qa, indent=2), encoding="utf-8")
    return qa
