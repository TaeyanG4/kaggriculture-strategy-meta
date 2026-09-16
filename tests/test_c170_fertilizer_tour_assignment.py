import copy
import hashlib
import json
from pathlib import Path
import runpy
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o182_combo_overflow.py"
OVERLAY = ROOT / "agent/overlays/c170_fertilizer_tour_assignment.py"
TARGET = ROOT / "agent/c170_fertilizer_tour_assignment.py"
MANIFEST = ROOT / "agent/c170_fertilizer_tour_assignment.manifest.json"


def action(farmer=None, hands=None, market=None):
    return {"farmer": farmer or ["PASS"], "hands": hands or [], "market": market or []}


def target(x, y, crop, birth, deadline, gain=1):
    return {"crop": crop, "birth": birth, "deadline": deadline, "gain": gain,
            "harvest": 400, "water": [], "until": -1, "yield": 0,
            "first": 2, "last": 6, "cap": 6}


def observation(step=288, farmer=(9, 9), hands=None):
    tiles = [[None for _ in range(10)] for _ in range(10)]
    farm = {"farmer": list(farmer), "hands": [list(pos) for pos in (hands or [])],
            "tiles": tiles, "money": 10000, "hires_today": 0,
            "unlocked_quadrants": ["NW"]}
    return {"step": step, "player": 0, "farms": [farm, copy.deepcopy(farm)],
            "private": {"shed": {"FERTILIZER": 0}, "seeds": {},
                        "inventories": [{} for _ in range(1 + len(hands or []))]},
            "market": {"prices": {"WHEAT": 20, "CARROT": 30}},
            "town": {"unlocked_shops": []}}


def pending(paths):
    return {index + 1: {"path": list(path), "quantity": len(path), "loaded": False}
            for index, path in enumerate(paths)}


def fake_gain(row, arrival, day):
    return row["gain"] if arrival <= row["deadline"] else 0


def load(parent_action, parent_pending, forecast, parent_hook=None):
    calls = {"count": 0}
    input_states = {0: {"step": 288, "pending": copy.deepcopy(parent_pending)}}

    def parent(obs, configuration=None):
        calls["count"] += 1
        if parent_hook:
            parent_hook(obs, input_states)
        return copy.deepcopy(parent_action)

    parent.telemetry = {"parent_marker": 9}
    chassis = SimpleNamespace(players={0: {"route": 0}}, routes={0: [action()] * 719})
    namespace = {
        "agent": parent,
        "_R51_INPUT_STATES": input_states,
        "_IMPL": SimpleNamespace(chassis=chassis),
        "_v219_native_day": lambda native, day: [action() for _ in range(24)],
        "_r51_input_forecast": lambda obs, route, expected: copy.deepcopy(forecast),
        "_r51_input_gain": fake_gain,
        "__name__": "c170_overlay_test",
    }
    exec(compile(OVERLAY.read_bytes(), str(OVERLAY), "exec"), namespace)
    return namespace, calls, input_states


def test_exact_spawn_uses_current_moves_and_nwse_tie_break():
    market = [["BUY_PRODUCT", "FERTILIZER", 2], ["HIRE"], ["HIRE"]]
    namespace, _, _ = load(action(farmer=["EAST"], market=market), {}, {})
    starts = namespace["_c170_spawn_starts"](
        observation(farmer=(4, 4)), action(farmer=["EAST"], market=market), 2)
    assert starts == [(290, (4, 4)), (290, (4, 5))]


def test_two_worker_crossed_paths_are_atomically_reassigned_with_fixed_economics():
    a = (4, 4, "WHEAT", 1)
    b = (4, 5, "WHEAT", 1)
    c = (5, 4, "CARROT", 1)
    d = (5, 5, "CARROT", 1)
    original = pending([[c, d], [a, b]])
    forecast = {(4, 4): target(4, 4, "WHEAT", 1, 290),
                (4, 5): target(4, 5, "WHEAT", 1, 292),
                (5, 4): target(5, 4, "CARROT", 1, 290),
                (5, 5): target(5, 5, "CARROT", 1, 292)}
    parent_action = action(market=[
        ["BUY_PRODUCT", "FERTILIZER", 4], ["HIRE"], ["HIRE"]])
    namespace, calls, input_states = load(parent_action, original, forecast)

    result = namespace["agent"](observation())
    rewritten = input_states[0]["pending"]
    assert result == parent_action
    assert calls["count"] == 1
    assert [rewritten[i]["quantity"] for i in (1, 2)] == [2, 2]
    assert [rewritten[i]["loaded"] for i in (1, 2)] == [False, False]
    assert {row for plan in rewritten.values() for row in plan["path"]} == {a, b, c, d}
    assert rewritten != original
    assert namespace["agent"].telemetry["c170_reassignments"] == 1
    assert namespace["agent"].telemetry["c170_forecast_extra_units"] == 4
    assert namespace["agent"].telemetry["parent_marker"] == 9


def test_one_worker_value_gain_with_any_target_regression_is_rejected():
    a = (4, 4, "WHEAT", 1)
    b = (5, 4, "CARROT", 1)
    original = pending([[a, b]])
    forecast = {(4, 4): target(4, 4, "WHEAT", 1, 290, 1),
                (5, 4): target(5, 4, "CARROT", 1, 291, 3)}
    parent_action = action(market=[
        ["BUY_PRODUCT", "FERTILIZER", 2], ["HIRE"]])
    namespace, _, input_states = load(parent_action, original, forecast)
    namespace["_c170_search"] = lambda *args: ([[b, a]], 2)

    assert namespace["agent"](observation()) == parent_action
    assert input_states[0]["pending"] == original
    assert namespace["agent"].telemetry["c170_no_gain_declines"] == 1


def test_equal_gain_and_shorter_path_does_not_change_parent_plan():
    a = (4, 4, "WHEAT", 1)
    b = (5, 4, "WHEAT", 1)
    original = pending([[b, a]])
    forecast = {(4, 4): target(4, 4, "WHEAT", 1, 310),
                (5, 4): target(5, 4, "WHEAT", 1, 310)}
    parent_action = action(market=[
        ["BUY_PRODUCT", "FERTILIZER", 2], ["HIRE"]])
    namespace, _, input_states = load(parent_action, original, forecast)
    namespace["_c170_search"] = lambda *args: ([[a, b]], 2)

    namespace["agent"](observation())
    assert input_states[0]["pending"] == original
    assert namespace["agent"].telemetry["c170_no_gain_declines"] == 1


def test_market_suffix_duplicate_and_forecast_drift_fail_closed():
    a = (4, 4, "WHEAT", 1)
    original = pending([[a]])
    forecast = {(4, 4): target(4, 4, "WHEAT", 1, 300)}
    bad_market = action(market=[
        ["BUY_PRODUCT", "FERTILIZER", 1], ["HIRE"], ["SELL", "WHEAT", 1]])
    namespace, _, input_states = load(bad_market, original, forecast)
    assert namespace["agent"](observation()) == bad_market
    assert input_states[0]["pending"] == original
    assert namespace["agent"].telemetry["c170_contract_declines"] == 1

    duplicate = {1: {"path": [a, a], "quantity": 2, "loaded": False}}
    good_market = action(market=[
        ["BUY_PRODUCT", "FERTILIZER", 2], ["HIRE"]])
    namespace, _, input_states = load(good_market, duplicate, forecast)
    namespace["agent"](observation())
    assert input_states[0]["pending"] == duplicate
    assert namespace["agent"].telemetry["c170_contract_declines"] == 1

    drifted = {(4, 4): target(4, 4, "WHEAT", 2, 300)}
    namespace, _, input_states = load(good_market, original, drifted)
    namespace["agent"](observation())
    assert input_states[0]["pending"] == original
    assert namespace["agent"].telemetry["c170_contract_declines"] == 1


def test_search_exception_and_nonstandard_configuration_preserve_everything():
    a = (4, 4, "WHEAT", 1)
    original = pending([[a]])
    forecast = {(4, 4): target(4, 4, "WHEAT", 1, 300)}
    parent_action = action(market=[
        ["BUY_PRODUCT", "FERTILIZER", 1], ["HIRE"]])
    namespace, _, input_states = load(parent_action, original, forecast)

    def fail(*args):
        raise RuntimeError("synthetic search failure")

    namespace["_c170_search"] = fail
    assert namespace["agent"](observation()) == parent_action
    assert input_states[0]["pending"] == original
    assert namespace["agent"].telemetry["c170_errors"] == 1

    namespace, _, input_states = load(parent_action, original, forecast)
    assert namespace["agent"](observation(), {"turnsPerDay": 12}) == parent_action
    assert input_states[0]["pending"] == original
    assert namespace["agent"].telemetry["c170_searches"] == 0


def test_search_rejects_any_route_reaching_hour23():
    a = (9, 9, "WHEAT", 1)
    forecast = {(9, 9): target(9, 9, "WHEAT", 1, 999)}
    parent_action = action(market=[
        ["BUY_PRODUCT", "FERTILIZER", 1], ["HIRE"]])
    namespace, _, _ = load(parent_action, pending([[a]]), forecast)
    paths, _ = namespace["_c170_search"](
        (a,), (1,), [(310, (4, 4))], {a: forecast[(9, 9)]},
        {"WHEAT": 18, "CARROT": 28}, 12, {a: 0})
    assert paths is None


def test_beam_selects_best_safe_route_instead_of_rejecting_unsafe_global_maximum():
    rows = ((3, 6, "CARROT", 0), (3, 3, "CARROT", 1),
            (4, 4, "WHEAT", 2), (7, 7, "CARROT", 3))
    targets = {
        rows[0]: {"gain": 1, "deadline": 293},
        rows[1]: {"gain": 3, "deadline": 298},
        rows[2]: {"gain": 2, "deadline": 296},
        rows[3]: {"gain": 3, "deadline": 295},
    }
    starts = [(290, (4, 4)), (290, (5, 4))]
    prices = {"WHEAT": 18, "CARROT": 28}
    baseline_paths = [[rows[0], rows[2]], [rows[3], rows[1]]]
    parent_action = action(market=[
        ["BUY_PRODUCT", "FERTILIZER", 4], ["HIRE"], ["HIRE"]])
    namespace, _, _ = load(parent_action, pending(baseline_paths), {})
    baseline = namespace["_c170_evaluate"](
        baseline_paths, starts, targets, prices, 12)
    safe_paths, _ = namespace["_c170_search"](
        tuple(sorted(rows)), (2, 2), starts, targets, prices, 12, baseline["gains"])
    assert safe_paths is not None
    selected = namespace["_c170_evaluate"](safe_paths, starts, targets, prices, 12)
    assert all(selected["gains"][row] >= baseline["gains"][row] for row in rows)
    assert any(selected["gains"][row] > baseline["gains"][row] for row in rows)
    assert selected["value"] == 196


def test_built_manifest_hashes_and_last_callable_contract():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert hashlib.sha256(PARENT.read_bytes()).hexdigest() == manifest["parent"]["sha256"]
    assert hashlib.sha256(OVERLAY.read_bytes()).hexdigest() == manifest["overlay"]["sha256"]
    assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == manifest["output"]["sha256"]
    assert manifest["status"] == "implemented_unvalidated"
    assert manifest["promotion"] is False
    namespace = runpy.run_path(str(TARGET), run_name="c170_candidate_test")
    callables = [name for name, value in namespace.items()
                 if callable(value) and not name.startswith("__")]
    assert callables[-1] == "agent"
