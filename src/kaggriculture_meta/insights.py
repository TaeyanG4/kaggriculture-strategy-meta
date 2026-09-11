from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

from .pilot import write_csv


FEATURES = {
    "cash_t24": "opening_economy",
    "cash_t72": "early_economy",
    "cash_t168": "mid_economy",
    "cash_t360": "late_economy",
    "first_land_turn": "timing",
    "first_hire_turn": "timing",
    "first_plant_turn": "timing",
    "first_sell_turn": "timing",
    "first_animal_turn": "timing",
    "total_hires_actual": "labor",
    "early_hires_actual": "opening_labor",
    "early_plant_actions": "opening_behavior",
    "early_seed_units": "opening_behavior",
    "early_animal_units": "opening_behavior",
    "early_sell_units": "opening_behavior",
    "early_dominant_crop_share": "opening_crop_mix",
    "crop_carrot_share": "resource_mix",
    "crop_melon_share": "resource_mix",
    "crop_strawberry_share": "resource_mix",
    "crop_tomato_share": "resource_mix",
    "crop_wheat_share": "resource_mix",
    "animal_cow_share": "resource_mix",
    "animal_goose_share": "resource_mix",
    "animal_sheep_share": "resource_mix",
    "total_market_orders": "full_game_behavior",
    "total_unit_actions": "full_game_behavior",
    "market_buy_seed_units": "full_game_behavior",
    "market_buy_animal_units": "full_game_behavior",
    "market_sell_units": "full_game_behavior",
}


def sign_test_two_sided(positive: int, negative: int) -> float | None:
    n = positive + negative
    if n == 0:
        return None
    k = min(positive, negative)
    cdf = sum(math.comb(n, i) for i in range(k + 1)) / (2**n)
    return min(1.0, 2.0 * cdf)


def benjamini_hochberg(p_values: list[float | None]) -> list[float | None]:
    indexed = [(i, p) for i, p in enumerate(p_values) if p is not None]
    m = len(indexed)
    if not m:
        return [None] * len(p_values)
    indexed.sort(key=lambda pair: pair[1])
    adjusted = [None] * len(p_values)
    running = 1.0
    for rank_from_end in range(m - 1, -1, -1):
        idx, p = indexed[rank_from_end]
        rank = rank_from_end + 1
        running = min(running, p * m / rank)
        adjusted[idx] = min(1.0, running)
    return adjusted


def paired_rows(rows: list[dict]) -> list[tuple[dict, dict]]:
    by_episode: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_episode[str(row["episode_id"])].append(row)
    pairs = []
    for episode_id, members in sorted(by_episode.items()):
        winners = [r for r in members if r.get("outcome") == "win"]
        losers = [r for r in members if r.get("outcome") == "loss"]
        if len(winners) == 1 and len(losers) == 1:
            pairs.append((winners[0], losers[0]))
    return pairs


def feature_summary(pairs: list[tuple[dict, dict]]) -> list[dict]:
    results = []
    for feature, group in FEATURES.items():
        winner_values = []
        loser_values = []
        diffs = []
        seat0_winner_diffs = []
        seat1_winner_diffs = []
        positive = negative = ties = 0
        for winner, loser in pairs:
            w = winner.get(feature)
            l = loser.get(feature)
            if w in {None, ""} or l in {None, ""}:
                continue
            w_n = float(w)
            l_n = float(l)
            diff = w_n - l_n
            winner_values.append(w_n)
            loser_values.append(l_n)
            diffs.append(diff)
            if diff > 0:
                positive += 1
            elif diff < 0:
                negative += 1
            else:
                ties += 1
            if str(winner.get("seat")) == "0":
                seat0_winner_diffs.append(diff)
            else:
                seat1_winner_diffs.append(diff)

        mean_diff = statistics.fmean(diffs) if diffs else None
        sd_diff = statistics.stdev(diffs) if len(diffs) > 1 else None
        standardized = mean_diff / sd_diff if mean_diff is not None and sd_diff not in {None, 0} else None
        seat0_mean = statistics.fmean(seat0_winner_diffs) if seat0_winner_diffs else None
        seat1_mean = statistics.fmean(seat1_winner_diffs) if seat1_winner_diffs else None
        direction_consistent = (
            seat0_mean is not None
            and seat1_mean is not None
            and seat0_mean != 0
            and seat1_mean != 0
            and (seat0_mean > 0) == (seat1_mean > 0)
        )
        results.append(
            {
                "feature": feature,
                "feature_group": group,
                "paired_games": len(diffs),
                "mean_winner": round(statistics.fmean(winner_values), 6) if winner_values else None,
                "mean_loser": round(statistics.fmean(loser_values), 6) if loser_values else None,
                "mean_winner_minus_loser": round(mean_diff, 6) if mean_diff is not None else None,
                "median_winner_minus_loser": round(statistics.median(diffs), 6) if diffs else None,
                "paired_standardized_effect": round(standardized, 6) if standardized is not None else None,
                "winner_higher_games": positive,
                "winner_lower_games": negative,
                "ties": ties,
                "winner_higher_share_decided": round(positive / (positive + negative), 4)
                if positive + negative else None,
                "sign_test_p": sign_test_two_sided(positive, negative),
                "winner_seat0_games": len(seat0_winner_diffs),
                "winner_seat1_games": len(seat1_winner_diffs),
                "mean_diff_when_winner_seat0": round(seat0_mean, 6) if seat0_mean is not None else None,
                "mean_diff_when_winner_seat1": round(seat1_mean, 6) if seat1_mean is not None else None,
                "direction_consistent_across_winner_seats": direction_consistent,
            }
        )

    q_values = benjamini_hochberg([r["sign_test_p"] for r in results])
    for row, q in zip(results, q_values):
        row["sign_test_bh_q"] = round(q, 8) if q is not None else None
        effect = row["paired_standardized_effect"]
        row["robust_exploratory_signal"] = bool(
            q is not None
            and q <= 0.05
            and row["direction_consistent_across_winner_seats"]
            and effect is not None
            and abs(float(effect)) >= 0.2
        )
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        type=Path,
        default=Path("state/expanded_pilot/release_candidate/strategy_meta.csv"),
    )
    ap.add_argument("--out-dir", type=Path, default=Path("reports"))
    args = ap.parse_args()

    with args.input.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    pairs = paired_rows(rows)
    summaries = feature_summary(pairs)
    write_csv(args.out_dir / "current_v1_winner_loser_features.csv", summaries)

    robust = sorted(
        [r for r in summaries if r["robust_exploratory_signal"]],
        key=lambda r: abs(float(r["paired_standardized_effect"])),
        reverse=True,
    )
    opening_or_early = [
        r for r in robust
        if r["feature_group"]
        in {"opening_economy", "early_economy", "timing", "opening_labor", "opening_behavior", "opening_crop_mix"}
    ]
    summary = {
        "input_rows": len(rows),
        "paired_games": len(pairs),
        "features_tested": len(summaries),
        "multiple_test_correction": "Benjamini-Hochberg over exact paired sign tests",
        "robust_exploratory_signal_count": len(robust),
        "robust_opening_or_early_signal_count": len(opening_or_early),
        "robust_exploratory_features": [r["feature"] for r in robust],
        "robust_opening_or_early_features": [r["feature"] for r in opening_or_early],
        "interpretation_note": (
            "Exploratory association only. A robust flag requires BH q<=0.05, paired standardized "
            "effect |d|>=0.2, and the mean winner-loser direction to agree when the winner is in seat 0 "
            "and when the winner is in seat 1. It does not establish causality."
        ),
    }
    (args.out_dir / "current_v1_insight_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
