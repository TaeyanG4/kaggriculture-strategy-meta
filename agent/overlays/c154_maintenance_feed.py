# SPDX-License-Identifier: Apache-2.0
"""Keep an intentionally low-margin animal alive with every-other-day feed.

c124 suppresses every planned late COW/SHEEP feed when there is no matching
shop and the optimistic product value is far below grain value.  Restoring all
such feeds was rejected by c137.  This overlay restores only the second
consecutive suppressed feed, preventing escape while retaining at least half
of c124's grain saving.  It acts only when c124's own counter and the complete
set of reconstructed replacements agree, so unrelated PASS actions are never
rewritten.
"""

import copy as _c154_copy

_C154_PARENT = agent
_C154_STATES = {}
_C154_REPORT = {}
del agent


def _c154_candidates(observation, parent_action):
    seat = int(observation["player"])
    shops = observation["town"].get("unlocked_shops", [])
    if not (504 <= int(observation["step"]) < 696 and len(shops) == 8):
        return []
    prices = observation["market"]["prices"]
    farm = observation["farms"][seat]
    inventories = observation["private"]["inventories"]
    positions = [farm["farmer"], *farm["hands"]]
    commands = [parent_action.get("farmer") or ["PASS"], *(parent_action.get("hands") or [])]
    candidates = []
    for actor, command in enumerate(commands[:len(positions)]):
        if command != ["PASS"] or actor >= len(inventories) or inventories[actor].get("WHEAT", 0) < 1:
            continue
        x, y = positions[actor]
        tile = farm["tiles"][y][x]
        if not isinstance(tile, dict) or tile.get("animal") not in _C124_PRODUCTS or tile.get("fed_today"):
            continue
        kind = tile["animal"]
        if any(shop in shops for shop in _C124_SHOPS[kind]):
            continue
        benefit = 3 * prices[_C124_PRODUCTS[kind]] + prices["FERTILIZER"]
        if 10 * benefit >= 7 * prices["WHEAT"]:
            continue
        candidates.append((actor, kind, int(tile.get("consecutive_unfed", 0))))
    return candidates


def agent(observation, configuration=None):
    seat = int(observation.get("player", 0))
    step = int(observation.get("step", 0))
    state = _C154_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _C154_STATES[seat] = {"last": -1, "audited_skips": 0,
                                     "maintenance_feeds": 0, "ambiguous": 0,
                                     "errors": 0}
    state["last"] = step
    before = int(_C124_STATE.get(seat, {}).get("feed_skips", 0))
    parent = _C154_PARENT(observation, configuration)
    after = int(_C124_STATE.get(seat, {}).get("feed_skips", 0))
    result = parent
    try:
        suppressed = max(0, after - before)
        if suppressed:
            state["audited_skips"] += suppressed
            candidates = _c154_candidates(observation, parent)
            if len(candidates) != suppressed:
                state["ambiguous"] += 1
            else:
                endangered = [(actor, kind) for actor, kind, unfed in candidates if unfed >= 1]
                if endangered:
                    result = _c154_copy.deepcopy(parent)
                    for actor, _kind in endangered:
                        if actor == 0:
                            result["farmer"] = ["FEED"]
                        else:
                            result["hands"][actor - 1] = ["FEED"]
                    state["maintenance_feeds"] += len(endangered)
    except Exception:
        state["errors"] += 1
        result = parent
    _C154_REPORT.clear()
    _C154_REPORT.update(getattr(_C154_PARENT, "telemetry", {}))
    _C154_REPORT.update({"maintenance_feed_" + key: value for key, value in state.items() if key != "last"})
    return result


agent.telemetry = _C154_REPORT
agent = globals().pop("agent")
