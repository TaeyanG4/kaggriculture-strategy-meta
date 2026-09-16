import copy
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "agent/overlays/c163_worthless_care_fertilizer.py"


def action(farmer=None, hands=None, market=None):
    return {"farmer": farmer or ["PASS"], "hands": hands or [], "market": market or []}


def obs(step=378, fed=False, cared=False, fertilizer=True, positions=None, inventories=None):
    positions = positions or [[0, 0]]
    tiles = [[None for _ in range(10)] for _ in range(10)]
    tiles[0][0] = {"kind": "PASTURE", "animal": "COW", "placed_day": 0,
                   "yield_units": 0, "consecutive_unfed": 0, "fed_today": fed,
                   "cared_today": cared, "fertilizer_available": fertilizer,
                   "pending_care_bonus": 0}
    farm = {"farmer": list(positions[0]), "hands": [list(p) for p in positions[1:]],
            "tiles": tiles, "money": 10000, "unlocked_quadrants": ["NW"],
            "hires_today": 0}
    return {"step": step, "player": 0, "farms": [farm, copy.deepcopy(farm)],
            "private": {"shed": {}, "seeds": {},
                        "inventories": inventories or [{} for _ in positions]},
            "market": {"prices": {"FERTILIZER": 100}}, "town": {"unlocked_shops": []}}


def load(parent_action, future=None):
    calls = {"n": 0}
    def parent(observation, configuration=None):
        calls["n"] += 1
        return copy.deepcopy(parent_action)
    tape = [action() for _ in range(720)]
    for step, value in (future or {}).items():
        tape[step] = value
    ns = {"agent": parent,
          "_IMPL": SimpleNamespace(chassis=SimpleNamespace(players={0: {"route": 0}},
                                                             routes={0: tape})),
          "__name__": "c163_test"}
    exec(compile(OVERLAY.read_bytes(), str(OVERLAY), "exec"), ns)
    return ns["agent"], calls


def test_unfed_worthless_care_collects_expiring_fertilizer():
    candidate, calls = load(action(farmer=["CARE"]))
    result = candidate(obs(), None)
    assert result["farmer"] == ["COLLECT_FERTILIZER"]
    assert calls["n"] == 1
    assert candidate.telemetry["c163_worthless_unfed"] == 1


def test_later_feed_with_future_production_preserves_care():
    candidate, _ = load(action(farmer=["CARE"]), {379: action(farmer=["FEED"])})
    result = candidate(obs(), None)
    assert result["farmer"] == ["CARE"]
    assert candidate.telemetry["c163_declined_future_feed_value"] == 1


def test_later_collect_vetoes_early_collection():
    candidate, _ = load(action(farmer=["CARE"]),
                        {379: action(farmer=["COLLECT_FERTILIZER"])})
    assert candidate(obs(), None)["farmer"] == ["CARE"]
    assert candidate.telemetry["c163_declined_future_collect"] == 1


def test_duplicate_care_preserves_one_and_collects_with_other():
    candidate, _ = load(action(farmer=["CARE"], hands=[["CARE"]]))
    result = candidate(obs(fed=True, positions=[[0,0],[0,0]], inventories=[{},{}]), None)
    assert result["farmer"] == ["CARE"]
    assert result["hands"] == [["COLLECT_FERTILIZER"]]
    assert candidate.telemetry["c163_care_preserved"] == 1


def test_missing_fertilizer_and_nonstandard_config_preserve_parent():
    candidate, _ = load(action(farmer=["CARE"]))
    assert candidate(obs(fertilizer=False), None)["farmer"] == ["CARE"]
    candidate, _ = load(action(farmer=["CARE"]))
    assert candidate(obs(), {"boardSize": 8})["farmer"] == ["CARE"]


def test_confirmation_observes_inventory_increase():
    candidate, _ = load(action(farmer=["CARE"]))
    assert candidate(obs(), None)["farmer"] == ["COLLECT_FERTILIZER"]
    candidate(obs(step=379, inventories=[{"FERTILIZER": 1}]), None)
    assert candidate.telemetry["c163_confirmed_fertilizer_units"] == 1
    assert candidate.telemetry["c163_confirmation_errors"] == 0
