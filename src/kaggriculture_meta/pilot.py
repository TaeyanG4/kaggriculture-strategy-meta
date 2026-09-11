from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

BANDS = {
    "low": (0.0, 1400.0),
    "mid": (1800.0, 2100.0),
    "high": (2700.0, float("inf")),
}
CROPS = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"}
ANIMALS = {"GOOSE", "COW", "SHEEP"}
REPLAY_URL = "https://www.kaggleusercontent.com/episodes/{episode_id}.json"


def fnum(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_index(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def select_recent(rows: list[dict], since: str, per_band: int) -> list[dict]:
    eligible = []
    for row in rows:
        if row.get("type") != "EPISODE_TYPE_PUBLIC" or row.get("state") != "COMPLETED":
            continue
        if (row.get("end_time") or "") < since:
            continue
        r0, r1 = fnum(row.get("rating_0")), fnum(row.get("rating_1"))
        if r0 is None or r1 is None:
            continue
        row = dict(row)
        row["avg_rating"] = (r0 + r1) / 2.0
        eligible.append(row)

    chosen = []
    for band, (lo, hi) in BANDS.items():
        candidates = [r for r in eligible if lo <= r["avg_rating"] < hi]
        candidates.sort(key=lambda r: r.get("end_time") or "", reverse=True)
        for row in candidates[:per_band]:
            row = dict(row)
            row["rating_band"] = band
            row["source_class"] = "public_episode_cdn_internal"
            chosen.append(row)
    return chosen


def download_episode(episode_id: str, out_path: Path) -> int:
    if out_path.exists() and out_path.stat().st_size > 0:
        return out_path.stat().st_size
    req = urllib.request.Request(
        REPLAY_URL.format(episode_id=episode_id),
        headers={"User-Agent": "kaggriculture-strategy-meta-pilot/0.1"},
    )
    last_error = None
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                blob = response.read()
            json.loads(blob)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = out_path.with_suffix(".json.tmp")
            tmp.write_bytes(blob)
            tmp.replace(out_path)
            return len(blob)
        except Exception as exc:  # bounded retry for pilot robustness
            last_error = exc
            if attempt == 0:
                time.sleep(2)
    raise RuntimeError(f"episode {episode_id} download failed: {last_error}")


def canonical_action(action) -> bytes:
    if not isinstance(action, dict):
        action = {}
    return json.dumps(action, sort_keys=True, separators=(",", ":")).encode("utf-8")


def prefix_hash(steps: list, seat: int, end_turn: int) -> str:
    h = hashlib.sha256()
    for turn, step in enumerate(steps):
        if turn == 0:
            continue
        action = step[seat].get("action") or {}
        h.update(canonical_action(action))
        h.update(b"\0")
        if turn >= end_turn:
            break
    return h.hexdigest()[:16]


def unit_commands(action: dict) -> list[list]:
    farmer = action.get("farmer") or []
    hands = action.get("hands") or []
    cmds = []
    if isinstance(farmer, list) and farmer:
        cmds.append(farmer)
    if isinstance(hands, list):
        cmds.extend(c for c in hands if isinstance(c, list) and c)
    return cmds


def classify_strategy(features: dict) -> str:
    """Coarse, deterministic resource-mix family for the pilot.

    Wheat is a near-universal staple in the observed sample, so the family uses the
    dominant livestock species plus the dominant *secondary* crop by actual tile-turn
    occupancy. Opening identity remains separate in opening_hash_t24/t48.
    """
    animals = {a: float(features.get(f"animal_{a}_share") or 0.0) for a in ("goose", "cow", "sheep")}
    secondary = {c: float(features.get(f"crop_{c}_share") or 0.0) for c in ("carrot", "melon", "strawberry", "tomato")}
    animal = max(animals, key=animals.get) if any(animals.values()) else "no_animal"
    crop = max(secondary, key=secondary.get) if any(secondary.values()) else "wheat_core"
    return f"{animal}+{crop}"


def extract_seat(episode_id: str, replay: dict, seat: int, meta: dict) -> dict:
    steps = replay["steps"]
    market_counts = Counter()
    market_units = Counter()
    market_item_units = Counter()
    early_market_item_units = Counter()
    unit_counts = Counter()
    crop_counts = Counter()
    early_crop_counts = Counter()
    early_market_units = Counter()
    early_unit_counts = Counter()
    hires_by_day = defaultdict(int)
    early_hires_by_day = defaultdict(int)
    cash = []
    peak_crop_tiles = Counter()
    peak_animal_tiles = Counter()
    crop_tile_turns = Counter()
    animal_tile_turns = Counter()
    first = {"land": None, "hire": None, "plant": None, "sell": None, "animal": None}

    for turn, step in enumerate(steps):
        obs = step[0].get("observation") or {}
        farms = obs.get("farms") or []
        if seat < len(farms):
            farm = farms[seat] or {}
            money = fnum(farm.get("money"))
            if money is not None:
                cash.append((turn, money))
            day = turn // 24
            hires = int(farm.get("hires_today") or 0)
            hires_by_day[day] = max(hires_by_day[day], hires)
            if turn < 48:
                early_hires_by_day[day] = max(early_hires_by_day[day], hires)
            quads = farm.get("unlocked_quadrants") or []
            if len(quads) > 1 and first["land"] is None:
                first["land"] = turn
            current_crops = Counter()
            current_animals = Counter()
            for tile_row in farm.get("tiles") or []:
                for tile in tile_row or []:
                    if not isinstance(tile, dict):
                        continue
                    if tile.get("kind") == "PLANT" and tile.get("crop") in CROPS:
                        current_crops[str(tile["crop"])] += 1
                    elif tile.get("kind") in {"COOP", "PASTURE"} and tile.get("animal") in ANIMALS:
                        current_animals[str(tile["animal"])] += 1
            for key, value in current_crops.items():
                peak_crop_tiles[key] = max(peak_crop_tiles[key], value)
                crop_tile_turns[key] += value
            for key, value in current_animals.items():
                peak_animal_tiles[key] = max(peak_animal_tiles[key], value)
                animal_tile_turns[key] += value

        action = step[seat].get("action") or {}
        if not isinstance(action, dict):
            action = {}
        for order in action.get("market") or []:
            if not isinstance(order, list) or not order:
                continue
            op = str(order[0])
            market_counts[op] += 1
            qty = 1
            if len(order) >= 3:
                try:
                    qty = int(order[2])
                except (TypeError, ValueError):
                    qty = 1
            market_units[op] += max(qty, 0)
            item = str(order[1]) if len(order) > 1 else ""
            if item:
                market_item_units[(op, item)] += max(qty, 0)
            if turn < 48:
                early_market_units[op] += max(qty, 0)
                if item:
                    early_market_item_units[(op, item)] += max(qty, 0)
            if op == "HIRE" and first["hire"] is None:
                first["hire"] = turn
            if op == "SELL" and first["sell"] is None:
                first["sell"] = turn
            if op == "BUY_ANIMAL" and first["animal"] is None:
                first["animal"] = turn

        for cmd in unit_commands(action):
            op = str(cmd[0])
            unit_counts[op] += 1
            if turn < 48:
                early_unit_counts[op] += 1
            if op == "PLANT" and len(cmd) > 1 and str(cmd[1]) in CROPS:
                crop = str(cmd[1])
                crop_counts[crop] += 1
                if turn < 48:
                    early_crop_counts[crop] += 1
                if first["plant"] is None:
                    first["plant"] = turn

    cash_values = [v for _, v in cash]
    early_total_plants = sum(early_crop_counts.values())
    if early_crop_counts:
        dominant_crop, dominant_n = early_crop_counts.most_common(1)[0]
        dominant_share = dominant_n / early_total_plants if early_total_plants else 0.0
    else:
        dominant_crop, dominant_share = "", 0.0
    total_plants = sum(crop_counts.values())
    if crop_counts:
        total_dominant_crop, total_dominant_n = crop_counts.most_common(1)[0]
        total_dominant_share = total_dominant_n / total_plants if total_plants else 0.0
    else:
        total_dominant_crop, total_dominant_share = "", 0.0

    def cash_at(turn_target: int):
        vals = [v for t, v in cash if t <= turn_target]
        return vals[-1] if vals else None

    row = {
        "episode_id": episode_id,
        "episode_date": meta.get("end_time"),
        "seat": seat,
        "team_id": meta.get(f"team_{seat}"),
        "submission_id": meta.get(f"sub_{seat}"),
        "rating_after": fnum(meta.get(f"rating_{seat}")),
        "rating_band": meta.get("rating_band", "sentinel"),
        "source_class": meta.get("source_class", "unknown"),
        "engine_version": replay.get("module_version"),
        "turns": len(steps),
        "final_money_index": fnum(meta.get(f"bank_{seat}")),
        "starting_cash": cash_values[0] if cash_values else None,
        "ending_cash_observed": cash_values[-1] if cash_values else None,
        "peak_cash": max(cash_values) if cash_values else None,
        "cash_t24": cash_at(24),
        "cash_t72": cash_at(72),
        "cash_t168": cash_at(168),
        "cash_t360": cash_at(360),
        "first_land_turn": first["land"],
        "first_hire_turn": first["hire"],
        "first_plant_turn": first["plant"],
        "first_sell_turn": first["sell"],
        "first_animal_turn": first["animal"],
        "total_hires_actual": sum(hires_by_day.values()),
        "early_hires_actual": sum(early_hires_by_day.values()),
        "early_plant_actions": early_unit_counts["PLANT"],
        "early_animal_units": early_market_units["BUY_ANIMAL"],
        "early_seed_units": early_market_units["BUY_SEED"],
        "early_sell_units": early_market_units["SELL"],
        "early_dominant_crop": dominant_crop,
        "early_dominant_crop_share": round(dominant_share, 4),
        "dominant_crop": total_dominant_crop,
        "dominant_crop_share": round(total_dominant_share, 4),
        "opening_hash_t24": prefix_hash(steps, seat, 24),
        "opening_hash_t48": prefix_hash(steps, seat, 48),
        "total_market_orders": sum(market_counts.values()),
        "total_unit_actions": sum(unit_counts.values()),
    }
    crop_tile_turn_total = sum(crop_tile_turns.values())
    animal_tile_turn_total = sum(animal_tile_turns.values())
    for crop in sorted(CROPS):
        row[f"plant_{crop.lower()}_actions"] = crop_counts[crop]
        row[f"peak_{crop.lower()}_tiles"] = peak_crop_tiles[crop]
        row[f"crop_{crop.lower()}_tile_turns"] = crop_tile_turns[crop]
        row[f"crop_{crop.lower()}_share"] = round(crop_tile_turns[crop] / crop_tile_turn_total, 4) if crop_tile_turn_total else 0.0
    for animal in sorted(ANIMALS):
        row[f"peak_{animal.lower()}_tiles"] = peak_animal_tiles[animal]
        row[f"animal_{animal.lower()}_tile_turns"] = animal_tile_turns[animal]
        row[f"animal_{animal.lower()}_share"] = round(animal_tile_turns[animal] / animal_tile_turn_total, 4) if animal_tile_turn_total else 0.0
    for (op, item), qty in sorted(market_item_units.items()):
        if op in {"BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "SELL"}:
            row[f"market_{op.lower()}_{item.lower()}_units"] = qty
    for (op, item), qty in sorted(early_market_item_units.items()):
        if op in {"BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "SELL"}:
            row[f"early_{op.lower()}_{item.lower()}_units"] = qty
    for op in ("BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "SELL", "HIRE", "BUY_LAND"):
        row[f"market_{op.lower()}_orders"] = market_counts[op]
        row[f"market_{op.lower()}_units"] = market_units[op]
    for op in ("MOVE", "HARVEST", "WATER", "CARE", "PLANT", "PLACE", "PICKUP", "FERTILIZE", "DIG", "PASS"):
        row[f"unit_{op.lower()}_actions"] = unit_counts[op]
    row["strategy_family_pilot"] = classify_strategy(row)
    return row


def write_csv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_matchups(feature_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    by_episode = defaultdict(dict)
    for row in feature_rows:
        by_episode[row["episode_id"]][int(row["seat"])] = row
    episodes = []
    grouped = defaultdict(lambda: {"games": 0, "wins_a": 0, "wins_b": 0, "ties": 0, "margins": []})
    for eid, seats in sorted(by_episode.items()):
        if 0 not in seats or 1 not in seats:
            continue
        a, b = seats[0], seats[1]
        bank_a, bank_b = a.get("final_money_index"), b.get("final_money_index")
        if bank_a is None or bank_b is None:
            winner = "unknown"
            margin = None
        elif bank_a > bank_b:
            winner = "seat0"
            margin = bank_a - bank_b
        elif bank_b > bank_a:
            winner = "seat1"
            margin = bank_a - bank_b
        else:
            winner = "tie"
            margin = 0.0
        episodes.append({
            "episode_id": eid,
            "rating_band": a.get("rating_band"),
            "engine_version": a.get("engine_version"),
            "family_0": a.get("strategy_family_pilot"),
            "family_1": b.get("strategy_family_pilot"),
            "bank_0": bank_a,
            "bank_1": bank_b,
            "winner": winner,
            "margin_0_minus_1": margin,
        })

        fam0, fam1 = a.get("strategy_family_pilot"), b.get("strategy_family_pilot")
        if fam0 <= fam1:
            fam_a, fam_b = fam0, fam1
            a_bank, b_bank = bank_a, bank_b
        else:
            fam_a, fam_b = fam1, fam0
            a_bank, b_bank = bank_b, bank_a
        g = grouped[(fam_a, fam_b)]
        g["games"] += 1
        if a_bank is not None and b_bank is not None:
            g["margins"].append(a_bank - b_bank)
            if a_bank > b_bank:
                g["wins_a"] += 1
            elif b_bank > a_bank:
                g["wins_b"] += 1
            else:
                g["ties"] += 1

    summary = []
    for (fam_a, fam_b), g in sorted(grouped.items()):
        games = g["games"]
        decided = g["wins_a"] + g["wins_b"]
        summary.append({
            "strategy_family_A": fam_a,
            "strategy_family_B": fam_b,
            "games": games,
            "wins_A": g["wins_a"],
            "wins_B": g["wins_b"],
            "ties": g["ties"],
            "win_rate_A_decided": round(g["wins_a"] / decided, 4) if decided else None,
            "mean_margin_A": round(sum(g["margins"]) / len(g["margins"]), 2) if g["margins"] else None,
            "evidence": "pilot_only" if games < 5 else "small_sample",
        })
    return episodes, summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", type=Path, default=Path("state/pilot/source_index/episodes.csv"))
    ap.add_argument("--raw-dir", type=Path, default=Path("state/pilot/downloads"))
    ap.add_argument("--out-dir", type=Path, default=Path("reports"))
    ap.add_argument("--since", default="2026-09-09")
    ap.add_argument("--per-band", type=int, default=4)
    ap.add_argument("--official-sentinel", type=Path, default=Path("state/pilot/raw/107289135.json"))
    args = ap.parse_args()

    started = time.time()
    index_rows = load_index(args.index)
    by_id = {r["episode_id"]: r for r in index_rows}
    selection = select_recent(index_rows, args.since, args.per_band)

    if args.official_sentinel.exists():
        sid = args.official_sentinel.stem
        meta = dict(by_id.get(sid, {"episode_id": sid}))
        meta["rating_band"] = "official_sentinel"
        meta["source_class"] = "official_kaggle_daily_cc0"
        if not any(r["episode_id"] == sid for r in selection):
            selection.append(meta)

    print(f"pilot selection: {len(selection)} episodes", flush=True)
    write_csv(args.out_dir / "pilot_selection.csv", selection)

    feature_rows = []
    failures = []
    source_bytes = 0
    engine_versions = Counter()
    for i, meta in enumerate(selection, 1):
        eid = meta["episode_id"]
        if meta.get("source_class") == "official_kaggle_daily_cc0" and args.official_sentinel.exists():
            path = args.official_sentinel
        else:
            path = args.raw_dir / f"{eid}.json"
            try:
                nbytes = download_episode(eid, path)
                print(f"download {i}/{len(selection)} episode={eid} bytes={nbytes}", flush=True)
            except Exception as exc:
                failures.append({"episode_id": eid, "stage": "download", "error": str(exc)})
                print(f"download {i}/{len(selection)} episode={eid} FAILED", flush=True)
                continue
        source_bytes += path.stat().st_size
        try:
            with path.open(encoding="utf-8") as f:
                replay = json.load(f)
            engine_versions[str(replay.get("module_version"))] += 1
            if len(replay.get("steps") or []) == 0:
                raise ValueError("no steps")
            for seat in (0, 1):
                feature_rows.append(extract_seat(eid, replay, seat, meta))
            print(f"parse {i}/{len(selection)} episode={eid} turns={len(replay['steps'])} engine={replay.get('module_version')}", flush=True)
        except Exception as exc:
            failures.append({"episode_id": eid, "stage": "parse", "error": str(exc)})
            print(f"parse {i}/{len(selection)} episode={eid} FAILED", flush=True)

    feature_path = args.out_dir / "pilot_features.csv"
    write_csv(feature_path, feature_rows)
    episode_matchups, matchup_summary = build_matchups(feature_rows)
    write_csv(args.out_dir / "pilot_episode_matchups.csv", episode_matchups)
    write_csv(args.out_dir / "pilot_matchup_summary.csv", matchup_summary)

    families = Counter(r["strategy_family_pilot"] for r in feature_rows)
    ratings = [r["rating_after"] for r in feature_rows if r.get("rating_after") is not None]
    summary = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "selection_episodes": len(selection),
        "parsed_episodes": len({r["episode_id"] for r in feature_rows}),
        "player_seats": len(feature_rows),
        "source_bytes": source_bytes,
        "parsing_failures": failures,
        "engine_versions": dict(engine_versions),
        "rating_min": min(ratings) if ratings else None,
        "rating_max": max(ratings) if ratings else None,
        "strategy_family_counts": dict(families),
        "episode_matchups": len(episode_matchups),
        "matchup_pairs": len(matchup_summary),
        "derived_feature_bytes": feature_path.stat().st_size if feature_path.exists() else 0,
        "runtime_seconds": round(time.time() - started, 3),
        "rights_note": "Raw replays remain local. Public release provenance must be source-scoped; official Kaggle daily episode datasets are CC0-1.0.",
        "interpretation": "Pilot strategy labels are deterministic hypotheses only; matchup rows below five games are not strong evidence.",
    }
    (args.out_dir / "pilot_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()