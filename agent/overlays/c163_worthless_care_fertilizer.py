# SPDX-License-Identifier: Apache-2.0
"""Collect expiring fertilizer instead of a CARE that cannot add sellable yield.

Every surviving animal exposes one fertilizer after each end-of-day refresh,
even when it was not fed.  The item does not accumulate.  This overlay changes
only a parent's CARE on that same animal when fertilizer is currently available,
the remaining native plan has no collection before dawn, and the CARE is either
duplicated/preserved or cannot bank a bonus with value before the last real dawn.

It does not add FEED, change market orders, or count an early collection as an
extra unit when the parent would collect it later.  The parent is called once.
Telemetry describes requested and next-observation confirmed units only.
"""
import copy as _c163_copy


_C163_PARENT = agent
_C163_STATE = {}
_C163_REPORT = {}
_C163_SPEC = {"GOOSE": (4, 1), "COW": (8, 2), "SHEEP": (6, 3)}
_C163_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
_C163_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
_C163_LAST_EOD = 28
_C163_MAX_FORECAST_STEPS = 8
del agent


def _c163_new_state():
    return {"last": -1, "care_checks": 0, "collect_swaps": 0,
            "requested_fertilizer_units": 0, "confirmed_fertilizer_units": 0,
            "confirmation_errors": 0, "care_preserved": 0,
            "worthless_unfed": 0, "worthless_no_future": 0,
            "declined_lookahead": 0, "declined_no_route": 0,
            "declined_parent_collect": 0, "declined_future_collect": 0,
            "declined_future_feed_value": 0, "declined_eod_capacity": 0,
            "errors": 0, "pending": []}


def _c163_standard(observation, configuration):
    farm = observation["farms"][int(observation["player"])]
    if len(farm["tiles"]) != 10:
        return False
    if configuration is None:
        return True
    return all(configuration.get(key, expected) == expected for key, expected in (
        ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100),
        ("maxMarketOrdersPerTurn", 10), ("farmHandCostMult", 1),
        ("episodeSteps", 720)))


def _c163_commands(action, count):
    result = [list(action.get("farmer") or ["PASS"])]
    result.extend(list(command or ["PASS"]) for command in (action.get("hands") or []))
    result.extend([["PASS"] for _ in range(max(0, count - len(result)))])
    return result[:count]


def _c163_set(action, actor, command):
    if actor == 0:
        action["farmer"] = list(command)
    else:
        action["hands"][actor - 1] = list(command)


def _c163_produces(tile, end_day):
    first, interval = _C163_SPEC[tile["animal"]]
    age = end_day + 1 - int(tile.get("placed_day", 0)) - first
    return age >= 0 and age % interval == 0


def _c163_has_future_sellable_production(tile, day):
    return any(_c163_produces(tile, d) for d in range(day + 1, _C163_LAST_EOD + 1))


def _c163_move_positions(positions, action):
    result = [list(pos) for pos in positions]
    for actor, command in enumerate(_c163_commands(action, len(result))):
        if command and command[0] in _C163_MOVES:
            dx, dy = _C163_MOVES[command[0]]
            x, y = result[actor]
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                result[actor] = [nx, ny]
    for order in action.get("market") or []:
        if order and order[0] == "HIRE":
            target = min(_C163_ACCESS,
                         key=lambda pos: (sum(tuple(p) == pos for p in result),
                                          _C163_ACCESS.index(pos)))
            result.append(list(target))
    return result


def _c163_remaining_events(observation, parent_action, target):
    seat = int(observation["player"])
    step = int(observation["step"])
    end_step = (step // 24 + 1) * 24 - 1
    state = getattr(getattr(_IMPL, "chassis", None), "players", {}).get(seat, {})
    route = state.get("route")
    routes = getattr(getattr(_IMPL, "chassis", None), "routes", {})
    if route not in routes:
        return None
    tape = routes[route]
    positions = [observation["farms"][seat]["farmer"],
                 *observation["farms"][seat].get("hands", [])]
    positions = _c163_move_positions(positions, parent_action)
    events = set()
    for future_step in range(step + 1, min(end_step, len(tape) - 1) + 1):
        native = tape[future_step] if isinstance(tape[future_step], dict) else {}
        commands = _c163_commands(native, len(positions))
        for pos, command in zip(positions, commands):
            if tuple(pos) == target and command:
                events.add(command[0])
        positions = _c163_move_positions(positions, native)
    return events


def _c163_valid_same_turn_feed(tile, target, positions, commands, inventories):
    if tile.get("fed_today"):
        return True
    return any(tuple(pos) == target and command == ["FEED"] and actor < len(inventories)
               and inventories[actor].get("WHEAT", 0) > 0
               for actor, (pos, command) in enumerate(zip(positions, commands)))


def _c163_eod_capacity_safe(observation, parent_action):
    if int(observation["step"]) % 24 != 23:
        return True
    private = observation["private"]
    total = sum(max(0, int(v)) for v in private.get("shed", {}).values())
    total += sum(max(0, int(v)) for inv in private.get("inventories", []) for v in inv.values())
    buys = sum(max(0, int(order[2])) for order in (parent_action.get("market") or [])
               if len(order) >= 3 and order[0] in ("BUY_PRODUCT", "BUY_ANIMAL"))
    return total + buys + 1 <= 100


def _c163_confirm(observation, state):
    step = int(observation["step"])
    inventories = observation["private"].get("inventories", [])
    remaining = []
    for pending in state["pending"]:
        if pending["step"] != step:
            if pending["step"] < step:
                state["confirmation_errors"] += 1
            else:
                remaining.append(pending)
            continue
        actor = pending["actor"]
        if actor >= len(inventories):
            state["confirmation_errors"] += 1
            continue
        gained = max(0, int(inventories[actor].get("FERTILIZER", 0)) - pending["before"])
        state["confirmed_fertilizer_units"] += min(1, gained)
        if gained < 1:
            state["confirmation_errors"] += 1
    state["pending"] = remaining


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _C163_STATE.get(seat)
    if state is None or step <= state["last"]:
        state = _C163_STATE[seat] = _c163_new_state()
    state["last"] = step
    parent_action = _C163_PARENT(observation, configuration)
    result = parent_action
    try:
        _c163_confirm(observation, state)
        day, hour = divmod(step, 24)
        if not _c163_standard(observation, configuration) or day > _C163_LAST_EOD:
            raise StopIteration
        if 23 - hour > _C163_MAX_FORECAST_STEPS:
            state["declined_lookahead"] += 1
            raise StopIteration
        farm = observation["farms"][seat]
        private = observation["private"]
        positions = [farm["farmer"], *farm.get("hands", [])]
        commands = _c163_commands(parent_action, len(positions))
        inventories = private.get("inventories", [])
        care_by_tile = {}
        collect_tiles = set()
        for actor, (pos, command) in enumerate(zip(positions, commands)):
            target = tuple(pos)
            if command == ["CARE"]:
                care_by_tile.setdefault(target, []).append(actor)
            elif command == ["COLLECT_FERTILIZER"]:
                collect_tiles.add(target)
        swaps = []
        for target, care_actors in care_by_tile.items():
            x, y = target
            tile = farm["tiles"][y][x]
            if not (isinstance(tile, dict) and tile.get("animal") in _C163_SPEC
                    and tile.get("fertilizer_available")):
                continue
            state["care_checks"] += 1
            if target in collect_tiles:
                state["declined_parent_collect"] += 1
                continue
            events = _c163_remaining_events(observation, parent_action, target)
            if events is None:
                state["declined_no_route"] += 1
                continue
            if "COLLECT_FERTILIZER" in events:
                state["declined_future_collect"] += 1
                continue
            care_preserved = (bool(tile.get("cared_today")) or len(care_actors) > 1
                              or "CARE" in events)
            fed = (_c163_valid_same_turn_feed(tile, target, positions, commands, inventories)
                   or "FEED" in events)
            future = _c163_has_future_sellable_production(tile, day)
            if not care_preserved and fed and future:
                state["declined_future_feed_value"] += 1
                continue
            if not fed:
                state["worthless_unfed"] += 1
            elif not future:
                state["worthless_no_future"] += 1
            if not _c163_eod_capacity_safe(observation, parent_action):
                state["declined_eod_capacity"] += 1
                continue
            actor = care_actors[-1]
            before = int(inventories[actor].get("FERTILIZER", 0)) if actor < len(inventories) else 0
            swaps.append((actor, before, care_preserved))
        if swaps:
            result = _c163_copy.deepcopy(parent_action)
            for actor, before, care_preserved in swaps:
                _c163_set(result, actor, ["COLLECT_FERTILIZER"])
                state["collect_swaps"] += 1
                state["requested_fertilizer_units"] += 1
                state["care_preserved"] += int(bool(care_preserved))
                if hour < 23:
                    state["pending"].append({"step": step + 1, "actor": actor,
                                             "before": before})
    except StopIteration:
        pass
    except Exception:
        state["errors"] += 1
        result = parent_action
    _C163_REPORT.clear()
    _C163_REPORT.update(getattr(_C163_PARENT, "telemetry", {}))
    _C163_REPORT.update({"c163_" + key: value for key, value in state.items()
                         if key not in ("last", "pending")})
    return result


agent.telemetry = _C163_REPORT
agent = globals().pop("agent")
