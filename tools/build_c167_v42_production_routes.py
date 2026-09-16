"""Build immutable c167 from frozen o182 and V42 route literals.

The public notebook is parsed as Python source and its compressed literal is
decoded with the standard library.  It is never imported or executed.  The
generated candidate contains only the normalized route patches and shop map,
so Kaggle runtime does not read any repository or notebook file.
"""
from __future__ import annotations

import ast
import base64
import copy
import hashlib
import json
from pathlib import Path
import zlib


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "agent/o182_combo_overflow.py"
PARENT_SHA256 = "ef9d2aade50ce2ce400a64791288ffb179eee7a6e60ea0d06085ac12fe02900b"
NOTEBOOK = ROOT / "state/research/c156_rules_20260915/public_v42/kaggriculture-v42-production-that-fits-the-marke.ipynb"
NOTEBOOK_SHA256 = "d7ff530e896a855e514274a09d662fc9c905379754cb6fdfa349b6ed6cf271aa"
SOURCE = ROOT / "state/research/c156_rules_20260915/public_v42/main_extracted.py"
SOURCE_SHA256 = "728fdfb4405ba313f8b14ffb3e0f8eceaddcaa0de49e4835928d89aaf71467e9"
METADATA = ROOT / "state/research/c156_rules_20260915/public_v42/kernel-metadata.json"
METADATA_SHA256 = "22ae4b8341527a4d4899424d53f555159f0753135fbcf047c2ff025576682f23"
COMPARISON = ROOT / "state/research/c156_rules_20260915/v42_route_comparison.json"
COMPARISON_SHA256 = "adb0041eef134ebccbc67b327793e16aeb2cba4d5343ebf7a9d5154017285e85"

OVERLAY = ROOT / "agent/overlays/c167_v42_production_routes.py"
TARGET = ROOT / "agent/c167_v42_production_routes.py"
MANIFEST = ROOT / "agent/c167_v42_production_routes.manifest.json"

NEW_ROUTE_IDS = (100, 101, *range(103, 129))
LEGACY_ROUTE_IDS = tuple(range(13))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_write(path: Path, payload: bytes) -> None:
    if path.exists() and path.read_bytes() != payload:
        raise ValueError("Existing immutable c167 artifact differs: " + str(path))
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def assignment(tree: ast.Module, name: str) -> ast.Assign:
    matches = [
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one top-level assignment for {name}, got {len(matches)}")
    return matches[0]


def compressed_literal(tree: ast.Module, name: str) -> dict:
    node = assignment(tree, name)
    strings = [
        child.value for child in ast.walk(node.value)
        if isinstance(child, ast.Constant) and isinstance(child.value, str)
    ]
    if len(strings) != 1:
        raise ValueError(f"expected one compressed string for {name}, got {len(strings)}")
    return json.loads(zlib.decompress(base64.b85decode(strings[0])))


def literal(tree: ast.Module, name: str):
    return ast.literal_eval(assignment(tree, name).value)


def reconstruct_parent_routes(tree: ast.Module) -> dict[int, list[dict]]:
    payload = compressed_literal(tree, "_PAYLOAD")
    routes = {0: list(payload["base"])}
    for raw_id, patch in payload["patches"].items():
        tape = list(payload["base"])
        for raw_step, action in patch:
            tape[int(raw_step)] = action
        routes[int(raw_id)] = tape
    opening = literal(tree, "_R42_OPENING")
    for tape in routes.values():
        tape[0] = dict(tape[0], market=copy.deepcopy(opening))
    return routes


def reconstruct_v42_routes(tree: ast.Module) -> tuple[dict[int, list[dict]], dict[tuple[str, str], int]]:
    payload = compressed_literal(tree, "_R108_DATA")
    routes = {
        int(raw_id): [payload["actions"][index] for index in indices]
        for raw_id, indices in payload["routes"].items()
    }
    mapping = {tuple(row["shops"]): int(row["route"]) for row in payload["shops"]}
    return routes, mapping


def validate_action(action: object) -> None:
    if not isinstance(action, dict) or set(action) - {"farmer", "hands", "market"}:
        raise ValueError("invalid action dictionary")
    if not isinstance(action.get("farmer"), list):
        raise ValueError("invalid farmer command")
    if not isinstance(action.get("hands"), list) or not isinstance(action.get("market"), list):
        raise ValueError("invalid hands/market commands")
    if not all(isinstance(command, list) for command in action["hands"] + action["market"]):
        raise ValueError("invalid nested command")


def route_hash(tape: list[dict]) -> str:
    raw = json.dumps(tape, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def prepare_payload() -> tuple[str, dict[str, str], dict[tuple[str, str], int]]:
    parent_tree = ast.parse(PARENT.read_text(encoding="utf-8"), str(PARENT))
    source_tree = ast.parse(SOURCE.read_text(encoding="utf-8"), str(SOURCE))
    parent_routes = reconstruct_parent_routes(parent_tree)
    v42_routes, v42_mapping = reconstruct_v42_routes(source_tree)

    if tuple(sorted(parent_routes)) != LEGACY_ROUTE_IDS:
        raise ValueError("o182 legacy route set drift")
    if tuple(sorted(route for route in v42_routes if route >= 100)) != NEW_ROUTE_IDS:
        raise ValueError("V42 new route set drift")
    for route in LEGACY_ROUTE_IDS:
        if parent_routes[route][1:] != v42_routes[route][1:]:
            raise ValueError(f"V42 legacy route {route} differs after opening")

    opening = copy.deepcopy(parent_routes[0][0])
    patches: dict[str, list[list[object]]] = {}
    hashes: dict[str, str] = {}
    for route in NEW_ROUTE_IDS:
        tape = copy.deepcopy(v42_routes[route])
        tape[0] = copy.deepcopy(opening)
        if len(tape) != 719:
            raise ValueError(f"route {route} length is {len(tape)}")
        for action in tape:
            validate_action(action)
        patch = [[step, action] for step, action in enumerate(tape) if action != parent_routes[0][step]]
        rebuilt = list(parent_routes[0])
        for step, action in patch:
            rebuilt[int(step)] = action
        if rebuilt != tape:
            raise ValueError(f"route {route} patch reconstruction failed")
        patches[str(route)] = patch
        hashes[str(route)] = route_hash(tape)

    no_yarn = {
        shops: route for shops, route in v42_mapping.items()
        if "YARN_STORE" not in shops
    }
    if len(no_yarn) != 49 or set(no_yarn.values()) - set(NEW_ROUTE_IDS):
        raise ValueError("unexpected V42 no-YARN shop map")
    rows = [[shops[0], shops[1], route] for shops, route in sorted(no_yarn.items())]
    payload = {"patches": patches, "shops": rows}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    encoded = base64.b85encode(zlib.compress(raw, 9)).decode("ascii")
    return encoded, hashes, no_yarn


OVERLAY_TEMPLATE = r'''# SPDX-License-Identifier: Apache-2.0
"""Route non-YARN shop worlds through V42 production tapes.

The route actions and ordered shop-pair map are derived from the public
"Kaggriculture V42 - Production That Fits the Market" notebook and its
yhay81 shop-router lineage.  The notebook is Apache-2.0 and is parsed only by
the frozen build tool; this runtime block contains a compressed literal only.

The o182 opening, routes 0..12, day-27 route 2 closure, and all YARN worlds are
preserved.  Fixed o171/o170 livestock schedule substitutions are bypassed only
while their action windows overlap a newly selected V42 route.
"""
import base64 as _c167_base64
import json as _c167_json
import zlib as _c167_zlib


_C167_PAYLOAD = __C167_PAYLOAD_LITERAL__
_C167_DATA = _c167_json.loads(_c167_zlib.decompress(_c167_base64.b85decode(_C167_PAYLOAD)))
_C167_NEW_ROUTES = frozenset((100, 101, *range(103, 129)))
_C167_ROUTE_MAP = {tuple(row[:2]): int(row[2]) for row in _C167_DATA["shops"]}
if len(_C167_ROUTE_MAP) != 49 or any("YARN_STORE" in shops for shops in _C167_ROUTE_MAP):
    raise RuntimeError("c167 shop-map contract failed")
if _IMPL.chassis.players or _IMPL.chassis._future_sells:
    raise RuntimeError("c167 routes must be installed before the first observation")
if set(map(int, _C167_DATA["patches"])) != _C167_NEW_ROUTES:
    raise RuntimeError("c167 route-id contract failed")

for _c167_raw_id, _c167_patch in _C167_DATA["patches"].items():
    _c167_route_id = int(_c167_raw_id)
    _c167_tape = list(_ROUTES[0])
    for _c167_step, _c167_action in _c167_patch:
        _c167_tape[int(_c167_step)] = _c167_action
    _c167_tape[0] = dict(_c167_tape[0], market=[list(order) for order in _R42_OPENING])
    if len(_c167_tape) != 719:
        raise RuntimeError("c167 route-length contract failed")
    _ROUTES[_c167_route_id] = _c167_tape
    _IMPL.chassis.routes[_c167_route_id] = list(_c167_tape)

del _C167_DATA, _C167_PAYLOAD
del _c167_raw_id, _c167_patch, _c167_route_id, _c167_tape, _c167_step, _c167_action


_C167_LEGACY_ROUTER = _IMPL.chassis.router


def _c167_router(observation, step, state):
    first_day6 = step >= 144 and not state.get("day6")
    route = _C167_LEGACY_ROUTER(observation, step, state)
    if first_day6:
        shops = tuple((_get(_get(observation, "town", {}), "unlocked_shops", []) or [])[:2])
        if "YARN_STORE" not in shops:
            route = _C167_ROUTE_MAP.get(shops, 100)
            state["route"] = route
            state["c167_expert"] = "V42"
        else:
            state["c167_expert"] = "o182"
    return route


_IMPL.chassis.router = _c167_router


def _c167_selected_route(observation):
    step = int(_get(observation, "step", 0))
    if step >= 648:
        return 2
    seat = int(_get(observation, "player", 0))
    native = _IMPL.chassis.players.get(seat, {})
    route = native.get("route")
    if route is not None:
        return route
    if step >= 144:
        shops = tuple((_get(_get(observation, "town", {}), "unlocked_shops", []) or [])[:2])
        if "YARN_STORE" not in shops:
            return _C167_ROUTE_MAP.get(shops, 100)
    return 0


# o170 calls the o171 wrapper through _O170_PARENT.  The later r97 wrapper
# calls o170 through _R97_PARENT.  Rebind only these parent links so every
# earlier and later o182 layer remains in the original order.
_C167_BEFORE_O171 = _O171_PARENT
_C167_ORIGINAL_O171 = _O170_PARENT
_C167_ORIGINAL_O170 = _R97_PARENT
_C167_GUARD_STATES = {}


def _c167_guard_state(observation):
    seat = int(_get(observation, "player", 0))
    step = int(_get(observation, "step", 0))
    state = _C167_GUARD_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _C167_GUARD_STATES[seat] = {
            "last": -1, "o171_guarded": 0, "o170_guarded": 0, "errors": 0,
        }
    state["last"] = step
    return state


def _c167_gate_o171(observation, configuration=None):
    step = int(_get(observation, "step", 0))
    if _c167_selected_route(observation) in _C167_NEW_ROUTES and 150 <= step <= 182:
        state = _c167_guard_state(observation)
        if step == 150:
            state["o171_guarded"] += 1
        return _C167_BEFORE_O171(observation, configuration)
    return _C167_ORIGINAL_O171(observation, configuration)


_O170_PARENT = _c167_gate_o171


def _c167_gate_o170(observation, configuration=None):
    step = int(_get(observation, "step", 0))
    if _c167_selected_route(observation) in _C167_NEW_ROUTES and 241 <= step < 300:
        state = _c167_guard_state(observation)
        if step == 241:
            state["o170_guarded"] += 1
        return _O170_PARENT(observation, configuration)
    return _C167_ORIGINAL_O170(observation, configuration)


_R97_PARENT = _c167_gate_o170


_C167_PARENT = agent
_C167_REPORT = {}
del agent


def agent(observation, configuration=None):
    result = _C167_PARENT(observation, configuration)
    try:
        state = _c167_guard_state(observation)
        route = _c167_selected_route(observation)
        _C167_REPORT.clear()
        _C167_REPORT.update(getattr(_C167_PARENT, "telemetry", {}))
        _C167_REPORT.update({
            "c167_route": route,
            "c167_v42_selected": int(route in _C167_NEW_ROUTES),
            "c167_o171_guarded": state["o171_guarded"],
            "c167_o170_guarded": state["o170_guarded"],
            "c167_guard_errors": state["errors"],
        })
    except Exception:
        _C167_REPORT["c167_guard_errors"] = _C167_REPORT.get("c167_guard_errors", 0) + 1
    return result


agent.telemetry = _C167_REPORT
agent = globals().pop("agent")
'''


def main() -> None:
    expected = {
        PARENT: PARENT_SHA256,
        NOTEBOOK: NOTEBOOK_SHA256,
        SOURCE: SOURCE_SHA256,
        METADATA: METADATA_SHA256,
        COMPARISON: COMPARISON_SHA256,
    }
    for path, digest in expected.items():
        if sha256(path) != digest:
            raise ValueError("frozen source drift: " + str(path))

    encoded, route_hashes, no_yarn = prepare_payload()
    overlay_text = OVERLAY_TEMPLATE.replace("__C167_PAYLOAD_LITERAL__", repr(encoded))
    overlay = overlay_text.replace("\r\n", "\n").encode("utf-8")
    compile(overlay, str(OVERLAY), "exec")
    ast.parse(overlay.decode("utf-8"), str(OVERLAY))
    frozen_write(OVERLAY, overlay)

    parent = PARENT.read_bytes()
    header = (
        "# c167 build (GPT/Codex, 2026-09-15): frozen o182 + public V42 "
        "non-YARN production routes; Apache-2.0 notices retained.\n"
    ).encode()
    candidate = header + parent + b"\n\n" + overlay
    compile(candidate, str(TARGET), "exec")
    ast.parse(candidate.decode("utf-8"), str(TARGET))
    namespace = {"__name__": "c167_build_check"}
    exec(compile(candidate, str(TARGET), "exec"), namespace)
    callables = [name for name, value in namespace.items() if callable(value) and not name.startswith("__")]
    if not callables or callables[-1] != "agent":
        raise ValueError("last callable is not agent")
    if set(namespace["_ROUTES"]) != set(LEGACY_ROUTE_IDS) | set(NEW_ROUTE_IDS):
        raise ValueError("built route set differs")
    frozen_write(TARGET, candidate)

    map_raw = json.dumps(
        [[*shops, route] for shops, route in sorted(no_yarn.items())],
        separators=(",", ":"),
    ).encode()
    manifest = {
        "schema": 1,
        "candidate": "c167_v42_production_routes",
        "status": "implemented_unvalidated",
        "parent": {"path": "agent/o182_combo_overflow.py", "sha256": PARENT_SHA256},
        "overlay": {
            "path": "agent/overlays/c167_v42_production_routes.py",
            "sha256": hashlib.sha256(overlay).hexdigest(),
        },
        "output": {
            "path": "agent/c167_v42_production_routes.py",
            "sha256": hashlib.sha256(candidate).hexdigest(),
            "bytes": len(candidate),
        },
        "source": {
            "notebook": {"path": str(NOTEBOOK.relative_to(ROOT)).replace("\\", "/"), "sha256": NOTEBOOK_SHA256},
            "extracted": {"path": str(SOURCE.relative_to(ROOT)).replace("\\", "/"), "sha256": SOURCE_SHA256},
            "metadata": {"path": str(METADATA.relative_to(ROOT)).replace("\\", "/"), "sha256": METADATA_SHA256},
            "comparison": {"path": str(COMPARISON.relative_to(ROOT)).replace("\\", "/"), "sha256": COMPARISON_SHA256},
            "license": "Apache-2.0",
        },
        "route_contract": {
            "legacy_ids": list(LEGACY_ROUTE_IDS),
            "new_ids": list(NEW_ROUTE_IDS),
            "no_yarn_pairs": len(no_yarn),
            "shop_map_sha256": hashlib.sha256(map_raw).hexdigest(),
            "normalized_route_sha256": route_hashes,
            "opening": literal(ast.parse(PARENT.read_text(encoding="utf-8")), "_R42_OPENING"),
            "day6_step": 144,
            "day27_step": 648,
            "day27_route": 2,
        },
        "isolation": {
            "yarn_worlds_keep_o182": True,
            "o171_o170_disabled_for_new_routes": True,
            "runtime_notebook_access": False,
            "parent_calls_per_turn": 1,
        },
        "promotion": False,
    }
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode()
    frozen_write(MANIFEST, manifest_bytes)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
