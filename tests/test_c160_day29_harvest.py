import copy
import hashlib
import json
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o182_combo_overflow.py"
OVERLAY = ROOT / "agent/overlays/c160_day29_harvest.py"
TARGET = ROOT / "agent/c160_day29_harvest.py"
MANIFEST = ROOT / "agent/c160_day29_harvest.manifest.json"


def action(farmer=None, hands=None, market=None):
    return {"farmer": farmer or ["PASS"], "hands": hands or [], "market": market or []}


def observation(step=696, crop="TOMATO", units=3, positions=None):
    positions = positions or [(0, 0)]
    tiles = [[None for _ in range(10)] for _ in range(10)]
    tiles[0][0] = {"kind": "PLANT", "crop": crop, "yield_units": units,
                   "planted_day": 20, "watered_today": False,
                   "consecutive_unwatered": 0, "fertilized_until_day": -1}
    farm = {"farmer": list(positions[0]),
            "hands": [list(position) for position in positions[1:]],
            "tiles": tiles, "money": 10000, "hires_today": 0,
            "unlocked_quadrants": ["NW"]}
    return {"step": step, "player": 0, "farms": [farm, copy.deepcopy(farm)],
            "private": {"shed": {}, "seeds": {},
                        "inventories": [{} for _ in positions]},
            "market": {"prices": {}}, "town": {"unlocked_shops": []}}


def load(parent_action):
    calls = {"count": 0}

    def parent(obs, configuration=None):
        calls["count"] += 1
        return copy.deepcopy(parent_action)

    parent.telemetry = {"parent_marker": 4}
    namespace = {"agent": parent, "__name__": "c160_overlay_test"}
    exec(compile(OVERLAY.read_bytes(), str(OVERLAY), "exec"), namespace)
    return namespace["agent"], calls


def test_water_on_existing_tomato_yield_becomes_harvest_only_in_window():
    parent = action(farmer=["WATER"], market=[["SELL", "MILK", 2]])
    candidate, calls = load(parent)
    result = candidate(observation(step=696), None)
    assert result == action(farmer=["HARVEST"], market=[["SELL", "MILK", 2]])
    assert calls["count"] == 1
    assert candidate.telemetry["day29_harvest_harvest_replacements"] == 1
    assert candidate.telemetry["day29_harvest_yield_units_requested"] == 3
    assert candidate.telemetry["parent_marker"] == 4

    candidate, _ = load(parent)
    assert candidate(observation(step=695), None) == parent
    candidate, _ = load(parent)
    assert candidate(observation(step=712), None) == parent


def test_fertilize_hand_on_strawberry_changes_without_touching_other_commands():
    parent = action(farmer=["EAST"], hands=[["FERTILIZE"], ["NORTH"]],
                    market=[["BUY_PRODUCT", "WHEAT", 1]])
    candidate, _ = load(parent)
    obs = observation(crop="STRAWBERRY", units=5,
                      positions=[(9, 9), (0, 0), (8, 8)])
    result = candidate(obs, None)
    assert result["farmer"] == ["EAST"]
    assert result["hands"] == [["HARVEST"], ["NORTH"]]
    assert result["market"] == parent["market"]
    assert candidate.telemetry["day29_harvest_strawberry_replacements"] == 1


def test_zero_yield_one_time_crop_and_unrelated_commands_are_unchanged():
    parent = action(farmer=["WATER"])
    candidate, _ = load(parent)
    assert candidate(observation(units=0), None) == parent
    candidate, _ = load(parent)
    assert candidate(observation(crop="WHEAT", units=5), None) == parent
    parent_harvest = action(farmer=["HARVEST"])
    candidate, _ = load(parent_harvest)
    assert candidate(observation(), None) == parent_harvest


def test_nonstandard_or_malformed_observation_preserves_parent():
    parent = action(farmer=["WATER"])
    candidate, calls = load(parent)
    assert candidate(observation(), {"episodeSteps": 600}) == parent
    assert calls["count"] == 1


def test_manifest_hashes_and_last_callable_match_frozen_candidate():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert hashlib.sha256(PARENT.read_bytes()).hexdigest() == manifest["parent"]["sha256"]
    assert hashlib.sha256(OVERLAY.read_bytes()).hexdigest() == manifest["overlay"]["sha256"]
    assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == manifest["output"]["sha256"]
    assert manifest["validation"]["promotion"] is False
    namespace = runpy.run_path(str(TARGET), run_name="c160_candidate_test")
    callables = [name for name, value in namespace.items()
                 if callable(value) and not name.startswith("__")]
    assert callables[-1] == "agent"
