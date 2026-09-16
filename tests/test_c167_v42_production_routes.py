import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o182_combo_overflow.py"
TARGET = ROOT / "agent/c167_v42_production_routes.py"
OVERLAY = ROOT / "agent/overlays/c167_v42_production_routes.py"
MANIFEST = ROOT / "agent/c167_v42_production_routes.manifest.json"
BUILDER_PATH = ROOT / "tools/build_c167_v42_production_routes.py"

spec = importlib.util.spec_from_file_location("c167_builder", BUILDER_PATH)
builder = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(builder)


def load(path):
    return runpy.run_path(str(path), run_name=path.stem + "_test")


def observation(step, shops, player=0):
    return {"step": step, "player": player, "town": {"unlocked_shops": list(shops)}}


def test_manifest_and_all_frozen_source_hashes_match():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert hashlib.sha256(PARENT.read_bytes()).hexdigest() == manifest["parent"]["sha256"]
    assert hashlib.sha256(OVERLAY.read_bytes()).hexdigest() == manifest["overlay"]["sha256"]
    assert hashlib.sha256(TARGET.read_bytes()).hexdigest() == manifest["output"]["sha256"]
    for key in ("notebook", "extracted", "metadata", "comparison"):
        row = manifest["source"][key]
        path = ROOT / row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
    assert manifest["status"] == "implemented_unvalidated"
    assert manifest["promotion"] is False


def test_legacy_routes_are_byte_equivalent_and_new_routes_match_v42():
    parent = load(PARENT)
    candidate = load(TARGET)
    source_tree = ast.parse(builder.SOURCE.read_text(encoding="utf-8"))
    v42_routes, _ = builder.reconstruct_v42_routes(source_tree)

    assert set(candidate["_ROUTES"]) == set(range(13)) | set(builder.NEW_ROUTE_IDS)
    for route in range(13):
        assert candidate["_ROUTES"][route] == parent["_ROUTES"][route]
    for route in builder.NEW_ROUTE_IDS:
        expected = copy.deepcopy(v42_routes[route])
        expected[0] = copy.deepcopy(parent["_ROUTES"][0][0])
        assert candidate["_ROUTES"][route] == expected
        assert candidate["_IMPL"].chassis.routes[route] == expected


def test_every_route_has_719_schema_valid_actions_and_same_opening():
    candidate = load(TARGET)
    opening = candidate["_ROUTES"][0][0]
    for route, tape in candidate["_ROUTES"].items():
        assert len(tape) == 719, route
        assert tape[0] == opening
        for action in tape:
            assert isinstance(action, dict)
            assert set(action) <= {"farmer", "hands", "market"}
            assert isinstance(action.get("farmer"), list)
            assert isinstance(action.get("hands"), list)
            assert isinstance(action.get("market"), list)
            assert all(isinstance(command, list) for command in action["hands"] + action["market"])


def test_shop_router_changes_exactly_the_49_no_yarn_pairs():
    parent = load(PARENT)
    candidate = load(TARGET)
    source_tree = ast.parse(builder.SOURCE.read_text(encoding="utf-8"))
    _, mapping = builder.reconstruct_v42_routes(source_tree)
    no_yarn = {shops: route for shops, route in mapping.items() if "YARN_STORE" not in shops}
    assert candidate["_C167_ROUTE_MAP"] == no_yarn
    assert len(no_yarn) == 49

    for shops in sorted(mapping):
        obs = observation(144, shops)
        parent_state = {}
        candidate_state = {}
        old_route = parent["_router"](obs, 144, parent_state)
        new_route = candidate["_c167_router"](obs, 144, candidate_state)
        if "YARN_STORE" in shops:
            assert new_route == old_route
            assert candidate_state["c167_expert"] == "o182"
        else:
            assert old_route == 0
            assert new_route == no_yarn[shops]
            assert candidate_state["c167_expert"] == "V42"


def test_router_keeps_route_zero_before_day6_and_route_two_after_day27():
    candidate = load(TARGET)
    router = candidate["_c167_router"]
    state = {}
    shops = ("BAKERY", "BAKERY")
    assert router(observation(143, shops), 143, state) == 0
    assert router(observation(144, shops), 144, state) == 101
    assert router(observation(647, shops), 647, state) == 101
    assert router(observation(648, shops), 648, state) == 2
    assert router(observation(700, shops), 700, state) == 2


def test_router_states_are_independent_objects():
    candidate = load(TARGET)
    router = candidate["_c167_router"]
    state0 = {}
    state1 = {}
    assert router(observation(144, ("BAKERY", "BAKERY"), 0), 144, state0) == 101
    assert router(observation(144, ("PIZZA_SHOP", "PIZZA_SHOP"), 1), 144, state1) == 123
    assert state0["route"] == 101
    assert state1["route"] == 123


def test_new_routes_do_not_change_v219_global_obligation_predicate():
    candidate = load(TARGET)

    def disqualifying(tape):
        for action in tape[432:719]:
            if any(order and order[0] == "BUY_LAND" for order in action.get("market", [])):
                return True
            commands = [action.get("farmer"), *action.get("hands", [])]
            if any(command == ["PLANT", "TOMATO"] for command in commands):
                return True
        return False

    legacy = [disqualifying(candidate["_ROUTES"][route]) for route in range(13)]
    added = [disqualifying(candidate["_ROUTES"][route]) for route in builder.NEW_ROUTE_IDS]
    assert not any(legacy)
    assert not any(added)


def test_o171_and_o170_are_bypassed_only_for_new_route_windows():
    candidate = load(TARGET)
    gate171 = candidate["_c167_gate_o171"]
    globals171 = gate171.__globals__
    calls = {"before171": 0, "original171": 0}

    def before171(obs, config=None):
        calls["before171"] += 1
        return {"source": "before171"}

    def original171(obs, config=None):
        calls["original171"] += 1
        return {"source": "original171"}

    globals171["_C167_BEFORE_O171"] = before171
    globals171["_C167_ORIGINAL_O171"] = original171
    globals171["_IMPL"].chassis.players[0] = {"route": 101}
    assert gate171(observation(150, ("BAKERY", "BAKERY")))["source"] == "before171"
    globals171["_IMPL"].chassis.players[0] = {"route": 0}
    assert gate171(observation(150, ("BAKERY", "BAKERY")))["source"] == "original171"
    assert calls == {"before171": 1, "original171": 1}

    gate170 = candidate["_c167_gate_o170"]
    globals170 = gate170.__globals__
    calls = {"before170": 0, "original170": 0}

    def before170(obs, config=None):
        calls["before170"] += 1
        return {"source": "before170"}

    def original170(obs, config=None):
        calls["original170"] += 1
        return {"source": "original170"}

    globals170["_O170_PARENT"] = before170
    globals170["_C167_ORIGINAL_O170"] = original170
    globals170["_IMPL"].chassis.players[0] = {"route": 101}
    assert gate170(observation(241, ("BAKERY", "BAKERY")))["source"] == "before170"
    globals170["_IMPL"].chassis.players[0] = {"route": 0}
    assert gate170(observation(241, ("BAKERY", "BAKERY")))["source"] == "original170"
    assert calls == {"before170": 1, "original170": 1}


def test_final_wrapper_calls_parent_once_and_agent_is_last_callable():
    candidate = load(TARGET)
    final_agent = candidate["agent"]
    scope = final_agent.__globals__
    calls = {"count": 0}
    expected = {"farmer": ["PASS"], "hands": [], "market": []}

    def parent(obs, config=None):
        calls["count"] += 1
        return expected

    scope["_C167_PARENT"] = parent
    scope["_IMPL"].chassis.players[0] = {"route": 101}
    assert final_agent(observation(200, ("BAKERY", "BAKERY"))) is expected
    assert calls["count"] == 1
    callables = [name for name, value in candidate.items() if callable(value) and not name.startswith("__")]
    assert callables[-1] == "agent"


def test_overlay_imports_only_standard_library_modules():
    tree = ast.parse(OVERLAY.read_text(encoding="utf-8"))
    roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    assert roots <= {"base64", "json", "zlib"}
