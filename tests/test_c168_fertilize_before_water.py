import copy
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "agent/overlays/c168_fertilize_before_water.py"


def action(farmer=None, hands=None, market=None):
    return {"farmer": farmer or ["PASS"], "hands": hands or [], "market": market or []}


def obs(step=378, crop="WHEAT", held=3, fertilized=-1, watered=False,
        positions=None, inventories=None):
    positions = positions or [[0,0],[0,0]]
    tiles = [[None for _ in range(10)] for _ in range(10)]
    tiles[0][0] = {"kind": "PLANT", "crop": crop, "planted_day": 13,
                   "yield_units": held, "watered_today": watered,
                   "consecutive_unwatered": 0, "fertilized_until_day": fertilized,
                   "max_lifespan_step": 999}
    farm = {"farmer": list(positions[0]), "hands": [list(p) for p in positions[1:]],
            "tiles": tiles, "money": 10000, "hires_today": 0,
            "unlocked_quadrants": ["NW"]}
    return {"step": step, "player": 0, "farms": [farm, copy.deepcopy(farm)],
            "private": {"shed": {}, "seeds": {},
                        "inventories": inventories or [{"FERTILIZER": 1},{"FERTILIZER": 1}]},
            "market": {"prices": {}}, "town": {"unlocked_shops": []}}


def load(actions, future=None):
    calls = {"n": 0}
    def parent(observation, configuration=None):
        calls["n"] += 1
        return copy.deepcopy(actions.get(observation["step"], action()))
    tape = [action() for _ in range(720)]
    for step, value in (future or {}).items():
        tape[step] = value
    ns = {"agent": parent,
          "_IMPL": SimpleNamespace(chassis=SimpleNamespace(players={0:{"route":0}},
                                                             routes={0:tape})),
          "__name__": "c168_test"}
    exec(compile(OVERLAY.read_bytes(), str(OVERLAY), "exec"), ns)
    return ns["agent"], calls


def test_same_turn_water_then_fertilize_is_atomically_reordered():
    candidate, calls = load({378: action(farmer=["WATER"], hands=[["FERTILIZE"]])})
    result = candidate(obs(), None)
    assert result["farmer"] == ["FERTILIZE"]
    assert result["hands"] == [["WATER"]]
    assert calls["n"] == 1
    assert candidate.telemetry["c168_same_turn_swaps"] == 1
    assert candidate.telemetry["c168_requested_extra_yield"] == 1


def test_adjacent_native_pair_starts_then_completes_exact_contract():
    now = action(farmer=["WATER"], hands=[["PASS"]])
    nxt = action(farmer=["PASS"], hands=[["FERTILIZE"]])
    candidate, _ = load({378: now, 379: nxt}, {379: nxt})
    first = candidate(obs(), None)
    assert first["farmer"] == ["FERTILIZE"]
    fertilized = obs(step=379, fertilized=17)
    second = candidate(fertilized, None)
    assert second["hands"] == [["WATER"]]
    assert candidate.telemetry["c168_fertilizer_confirmations"] == 1
    assert candidate.telemetry["c168_next_turn_completions"] == 1


def test_start_requires_fertilizer_on_both_workers():
    now = action(farmer=["WATER"], hands=[["PASS"]])
    nxt = action(farmer=["PASS"], hands=[["FERTILIZE"]])
    candidate, _ = load({378: now}, {379: nxt})
    result = candidate(obs(inventories=[{"FERTILIZER":1},{}]), None)
    assert result["farmer"] == ["WATER"]
    assert candidate.telemetry["c168_declined_inventory"] == 1


def test_same_turn_requires_native_fertilizer_worker_inventory():
    parent = action(farmer=["WATER"], hands=[["FERTILIZE"]])
    candidate, _ = load({378: parent})
    result = candidate(obs(inventories=[{"FERTILIZER": 1}, {}]), None)
    assert result == parent
    assert candidate.telemetry["c168_declined_inventory"] == 1


def test_same_turn_preserves_water_workers_later_fertilizer_commitment():
    parent = action(farmer=["WATER"], hands=[["FERTILIZE"]])
    later = action(farmer=["FERTILIZE"], hands=[["PASS"]])
    candidate, _ = load({378: parent}, {379: later})
    result = candidate(obs(inventories=[{"FERTILIZER": 1}, {"FERTILIZER": 1}]), None)
    assert result == parent
    assert candidate.telemetry["c168_declined_future_commitment"] == 1


def test_same_turn_allows_spare_inventory_after_future_commitment():
    parent = action(farmer=["WATER"], hands=[["FERTILIZE"]])
    later = action(farmer=["FERTILIZE"], hands=[["PASS"]])
    candidate, _ = load({378: parent}, {379: later})
    result = candidate(obs(inventories=[{"FERTILIZER": 2}, {"FERTILIZER": 1}]), None)
    assert result["farmer"] == ["FERTILIZE"]
    assert result["hands"] == [["WATER"]]


def test_failed_first_fertilize_preserves_next_native_fertilize():
    now = action(farmer=["WATER"], hands=[["PASS"]])
    nxt = action(farmer=["PASS"], hands=[["FERTILIZE"]])
    candidate, _ = load({378: now, 379: nxt}, {379: nxt})
    assert candidate(obs(), None)["farmer"] == ["FERTILIZE"]
    second = candidate(obs(step=379, fertilized=-1), None)
    assert second == nxt
    assert candidate.telemetry["c168_next_turn_completions"] == 0
    assert candidate.telemetry["c168_contract_errors"] == 1


def test_completed_pending_target_cannot_start_another_exchange_same_callback():
    now = action(farmer=["WATER"], hands=[["PASS"]])
    nxt = action(farmer=["PASS"], hands=[["FERTILIZE"]])
    later = action(farmer=["FERTILIZE"], hands=[["PASS"]])
    candidate, _ = load({378: now, 379: nxt}, {379: nxt, 380: later})
    candidate(obs(inventories=[{"FERTILIZER": 2}, {"FERTILIZER": 1}]), None)
    second = candidate(obs(step=379, fertilized=17), None)
    assert second["hands"] == [["WATER"]]
    assert candidate.telemetry["c168_next_turn_starts"] == 1
    assert candidate.telemetry["c168_next_turn_completions"] == 1


def test_external_water_replaces_due_native_fertilize_with_pass():
    now = action(farmer=["WATER"], hands=[["PASS"]])
    nxt = action(farmer=["WATER"], hands=[["FERTILIZE"]])
    candidate, _ = load({378: now, 379: nxt}, {379: action(farmer=["PASS"], hands=[["FERTILIZE"]])})
    candidate(obs(), None)
    second = candidate(obs(step=379, fertilized=17), None)
    assert second["farmer"] == ["WATER"]
    assert second["hands"] == [["PASS"]]
    commands = [second["farmer"], *second["hands"]]
    assert commands.count(["WATER"]) == 1
    assert candidate.telemetry["c168_next_turn_completions"] == 1


def test_due_exchange_preserves_parent_when_third_action_conflicts_on_tile():
    now = action(farmer=["WATER"], hands=[["PASS"]])
    native_next = action(farmer=["PASS"], hands=[["FERTILIZE"]])
    reactive_next = action(farmer=["HARVEST"], hands=[["FERTILIZE"]])
    candidate, _ = load({378: now, 379: reactive_next}, {379: native_next})
    candidate(obs(), None)
    second = candidate(obs(step=379, fertilized=17), None)
    assert second == reactive_next
    assert candidate.telemetry["c168_next_turn_completions"] == 0
    assert candidate.telemetry["c168_contract_errors"] == 1


def test_same_turn_third_conflicting_action_blocks_exchange():
    parent = action(farmer=["WATER"], hands=[["FERTILIZE"], ["HARVEST"]])
    candidate, _ = load({378: parent})
    observation = obs(positions=[[0, 0], [0, 0], [0, 0]],
                      inventories=[{"FERTILIZER": 2}, {"FERTILIZER": 1}, {}])
    assert candidate(observation, None) == parent


def test_no_increment_at_crop_cap_preserves_parent():
    parent = action(farmer=["WATER"], hands=[["FERTILIZE"]])
    candidate, _ = load({378: parent})
    result = candidate(obs(held=5), None)
    assert result == parent
    assert candidate.telemetry["c168_declined_no_gain"] == 1


def test_fertilize_already_before_water_is_unchanged():
    parent = action(farmer=["FERTILIZE"], hands=[["WATER"]])
    candidate, _ = load({378: parent})
    assert candidate(obs(), None) == parent


def test_nonstandard_configuration_preserves_parent():
    parent = action(farmer=["WATER"], hands=[["FERTILIZE"]])
    candidate, _ = load({378: parent})
    assert candidate(obs(), {"turnsPerDay": 12}) == parent
