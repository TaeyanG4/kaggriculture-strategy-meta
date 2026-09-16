import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o199c_carrot_price2.py"
OVERLAY = ROOT / "agent/overlays/c176_structural_tomato_tail.py"
TARGET = ROOT / "agent/c176_structural_tomato_tail.py"
MANIFEST = ROOT / "agent/c176_structural_tomato_tail.manifest.json"


def load_candidate():
    spec = importlib.util.spec_from_file_location("c176_test_module", TARGET)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def base_observation(step=432, shops=None, money=12000):
    shops = list(shops or ["PIZZA_SHOP", "PIZZA_SHOP"])
    empty = [[None for _ in range(10)] for _ in range(10)]
    for y in range(10):
        for x in range(10):
            if x >= 5 and y >= 5:
                empty[y][x] = "LOCKED"
    farms = [
        {
            "money": money,
            "tiles": empty,
            "farmer": [4, 4],
            "hands": [],
            "unlocked_quadrants": ["NW", "NE", "SW"],
            "hires_today": 0,
        },
        {
            "money": money,
            "tiles": [[None for _ in range(10)] for _ in range(10)],
            "farmer": [4, 4],
            "hands": [],
            "unlocked_quadrants": ["NW", "NE", "SW"],
            "hires_today": 0,
        },
    ]
    return {
        "step": step,
        "player": 0,
        "town": {"unlocked_shops": shops},
        "market": {
            "prices": {
                "WHEAT": 25, "CARROT": 35, "TOMATO": 90, "STRAWBERRY": 120,
                "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100,
            },
            "inventory": {k: 10000 for k in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")},
            "params": {},
        },
        "farms": farms,
        "private": {
            "shed": {},
            "seeds": {},
            "inventories": [{}],
        },
    }


def test_manifest_pins_frozen_o199c_and_candidate_hashes():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert hashlib.sha256(PARENT.read_bytes()).hexdigest() == manifest["parent"]["sha256"]
    assert hashlib.sha256(OVERLAY.read_bytes()).hexdigest() == manifest["overlay"]["sha256"]
    assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == manifest["output"]["sha256"]
    assert manifest["parent"]["path"] == "agent/o199c_carrot_price2.py"
    assert manifest["status"] == "implemented_unvalidated"
    assert manifest["promotion"] is False


def test_overlay_contains_no_buy_land_action_literal():
    text = OVERLAY.read_text(encoding="utf-8")
    executable_lines = [line for line in text.splitlines() if not line.lstrip().startswith("#")]
    assert not any("['BUY_LAND']" in line or '["BUY_LAND"]' in line for line in executable_lines)


def test_auto_decision_enters_reallocation_for_two_tomato_shops():
    module = load_candidate()
    state = module._c176_new_state()
    module._c176_decide(base_observation(), state)
    assert state["active"] is True
    assert state["regime"] == "REALLOC"
    assert state["target_count"] == 8


def test_v219_is_suppressed_only_for_active_c176_on_decision_step():
    module = load_candidate()
    state = module._c176_new_state()
    state["active"] = True
    module._C176_STATES[0] = state
    assert module._v219_qualifies(base_observation(), {}) is False
    assert state["counts"]["v219_suppressed"] == 1


def test_seed_pool_and_wheat_plant_swap_are_two_phase():
    module = load_candidate()
    observation = base_observation(step=432)
    state = module._c176_new_state()
    state.update(active=True, regime="REALLOC", target_count=8)
    action = {"farmer": ["PASS"], "hands": [], "market": []}
    funded = module._c176_seed_pool(observation, action, state)
    assert funded["market"][-1] == ["BUY_SEED", "TOMATO", 8]

    # Market orders execute after field actions, so same-turn planting must not
    # assume the just-requested seeds already exist.
    observation["farms"][0]["farmer"] = [1, 1]
    planting = {"farmer": ["PLANT", "WHEAT"], "hands": [], "market": []}
    assert module._c176_convert_plants(observation, planting, state) is planting

    # On the next callback the physically present seed enables the substitution.
    observation["step"] = 433
    observation["private"]["seeds"]["TOMATO"] = 8
    switched = module._c176_convert_plants(observation, planting, state)
    assert switched["farmer"] == ["PLANT", "TOMATO"]
    assert state["counts"]["plant_swaps"] == 1
    assert (1, 1) in state["pending_plants"]


def test_candidate_exports_agent_as_last_callable():
    module = load_candidate()
    callables = [name for name, value in vars(module).items() if callable(value) and not name.startswith("__")]
    assert callables[-1] == "agent"
    assert callable(module.agent)
