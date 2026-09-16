import copy
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "agent/overlays/c156_production_cap_harvest.py"


def action(hands=None, farmer=None, market=None):
    return {"farmer": farmer or ["PASS"], "hands": hands or [], "market": market or []}


def animal(kind="COW", held=6, pending=3, fed=True, cared=False, placed=0):
    return {"kind": "COOP" if kind == "GOOSE" else "PASTURE", "animal": kind,
            "placed_day": placed, "yield_units": held, "consecutive_unfed": 0,
            "fed_today": fed, "cared_today": cared, "fertilizer_available": True,
            "pending_care_bonus": pending}


def observation(step=378, tile=None, positions=None, inventories=None, shed=None):
    positions = positions or [[0, 0]]
    tiles = [[None for _ in range(10)] for _ in range(10)]
    tiles[0][0] = tile or animal()
    farm = {"farmer": list(positions[0]), "hands": [list(p) for p in positions[1:]],
            "tiles": tiles, "money": 10000, "hires_today": 0,
            "unlocked_quadrants": ["NW"]}
    inventories = inventories or [{} for _ in positions]
    return {"step": step, "player": 0, "farms": [farm, copy.deepcopy(farm)],
            "private": {"shed": shed or {}, "seeds": {}, "inventories": inventories},
            "market": {"prices": {"EGG": 50, "MILK": 160, "WOOL": 200}},
            "town": {"unlocked_shops": []}}


def load(parent_action, future=None):
    calls = {"n": 0}
    def parent(obs, configuration=None):
        calls["n"] += 1
        return copy.deepcopy(parent_action)
    parent.telemetry = {"parent_calls": 7}
    tape = [action() for _ in range(720)]
    for step, value in (future or {}).items():
        tape[step] = value
    chassis = SimpleNamespace(players={0: {"route": 0}}, routes={0: tape})
    namespace = {"agent": parent, "_IMPL": SimpleNamespace(chassis=chassis),
                 "__name__": "c156_test"}
    exec(compile(OVERLAY.read_bytes(), str(OVERLAY), "exec"), namespace)
    return namespace["agent"], calls


def test_clipped_cow_swaps_when_net_units_increase_and_no_later_harvest():
    candidate, calls = load(action(farmer=["CARE"]))
    result = candidate(observation(), None)
    assert result["farmer"] == ["HARVEST"]
    assert calls["n"] == 1
    assert candidate.telemetry["c156_harvest_swaps"] == 1
    assert candidate.telemetry["c156_forecast_clipped_units"] == 4
    assert candidate.telemetry["parent_calls"] == 7


def test_future_native_harvest_vetoes_change():
    candidate, _ = load(action(farmer=["CARE"]), {379: action(farmer=["HARVEST"])})
    result = candidate(observation(), None)
    assert result["farmer"] == ["CARE"]
    assert candidate.telemetry["c156_declined_future_harvest"] == 1


def test_no_clip_and_unknown_feed_preserve_parent():
    candidate, _ = load(action(farmer=["CARE"]))
    result = candidate(observation(tile=animal(held=1, pending=0)), None)
    assert result["farmer"] == ["CARE"]
    candidate, _ = load(action(farmer=["CARE"]))
    result = candidate(observation(tile=animal(fed=False)), None)
    assert result["farmer"] == ["CARE"]
    assert candidate.telemetry["c156_declined_not_fed"] == 1


def test_last_duplicate_care_becomes_harvest_and_first_preserves_bonus():
    parent = action(farmer=["CARE"], hands=[["CARE"]])
    candidate, _ = load(parent)
    obs = observation(positions=[[0, 0], [0, 0]], inventories=[{}, {}])
    result = candidate(obs, None)
    assert result["farmer"] == ["CARE"]
    assert result["hands"] == [["HARVEST"]]
    assert candidate.telemetry["c156_care_preserved"] == 1


def test_parent_harvest_and_nonstandard_configuration_are_unchanged():
    candidate, calls = load(action(farmer=["HARVEST"]))
    result = candidate(observation(), None)
    assert result["farmer"] == ["HARVEST"]
    assert calls["n"] == 1
    candidate, _ = load(action(farmer=["CARE"]))
    result = candidate(observation(), {"boardSize": 8})
    assert result["farmer"] == ["CARE"]


def test_hour23_capacity_bound_declines_extra_harvest():
    candidate, _ = load(action(farmer=["CARE"]))
    obs = observation(step=383, shed={"WHEAT": 95})
    result = candidate(obs, None)
    assert result["farmer"] == ["CARE"]
    assert candidate.telemetry["c156_declined_eod_capacity"] == 1


def test_confirmation_counts_only_observed_actor_inventory_gain():
    candidate, _ = load(action(farmer=["CARE"]))
    first = observation()
    assert candidate(first, None)["farmer"] == ["HARVEST"]
    second = observation(step=379, inventories=[{"MILK": 6}])
    candidate(second, None)
    assert candidate.telemetry["c156_confirmed_harvest_units"] == 6
    assert candidate.telemetry["c156_confirmation_errors"] == 0
