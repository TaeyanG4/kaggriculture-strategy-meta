# SPDX-License-Identifier: Apache-2.0
"""Move one-time-crop fertilizer before the WATER that can use it.

In engine 1.32.7, WHEAT/CARROT/MELON add yield when WATER executes and inspect
fertilization at that instant.  A later FERTILIZE cannot improve that already
executed WATER.  This overlay preserves one WATER and one FERTILIZE while
reordering only two tightly certified forms:

* exactly one WATER followed by exactly one FERTILIZE on the same tile in one
  unit-action batch; or
* a WATER followed on the immediately next callback by a native FERTILIZE.

For the two-callback form both workers must already own fertilizer, the first
worker must retain enough for its remaining native fertilizer commands, and the
next action is verified again before WATER is emitted.  No fertilizer purchase,
worker, market order, crop target, or harvest timing is added.  Telemetry counts
requested yield increments, not realized harvest or cash.
"""
import copy as _c164_copy


_C164_PARENT = agent
_C164_STATE = {}
_C164_REPORT = {}
_C164_CROPS = {
    "WHEAT": {"window": 2, "last": 4, "cap": 6},
    "CARROT": {"window": 2, "last": 3, "cap": 4},
    "MELON": {"window": 6, "last": 12, "cap": 6},
}
_C164_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
_C164_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
del agent


def _c164_new_state():
    return {"last": -1, "checks": 0, "same_turn_swaps": 0,
            "next_turn_starts": 0, "next_turn_completions": 0,
            "requested_extra_yield": 0, "fertilizer_confirmations": 0,
            "water_confirmations": 0, "contract_errors": 0,
            "declined_no_gain": 0, "declined_inventory": 0,
            "declined_future_commitment": 0, "declined_no_route": 0,
            "errors": 0, "pending": [], "confirm": []}


def _c164_standard(observation, configuration):
    farm = observation["farms"][int(observation["player"])]
    if len(farm["tiles"]) != 10:
        return False
    if configuration is None:
        return True
    return all(configuration.get(key, expected) == expected for key, expected in (
        ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100),
        ("maxMarketOrdersPerTurn", 10), ("farmHandCostMult", 1),
        ("episodeSteps", 720)))


def _c164_commands(action, count):
    result = [list(action.get("farmer") or ["PASS"])]
    result.extend(list(command or ["PASS"]) for command in (action.get("hands") or []))
    result.extend([["PASS"] for _ in range(max(0, count - len(result)))])
    return result[:count]


def _c164_set(action, actor, command):
    if actor == 0:
        action["farmer"] = list(command)
    else:
        hands = action.setdefault("hands", [])
        while len(hands) < actor:
            hands.append(["PASS"])
        hands[actor - 1] = list(command)


def _c164_gain(tile, day):
    crop = tile.get("crop") if isinstance(tile, dict) else None
    if crop not in _C164_CROPS or tile.get("watered_today"):
        return 0
    spec = _C164_CROPS[crop]
    age = day - int(tile.get("planted_day", day))
    if not spec["window"] <= age <= spec["last"]:
        return 0
    if int(tile.get("fertilized_until_day", -1)) >= day:
        return 0
    held = max(0, int(tile.get("yield_units", 0) or 0))
    ordinary = min(spec["cap"], held + 1)
    boosted = min(spec["cap"], held + 2)
    return max(0, boosted - ordinary)


def _c164_move_positions(positions, action):
    result = [list(pos) for pos in positions]
    for actor, command in enumerate(_c164_commands(action, len(result))):
        if command and command[0] in _C164_MOVES:
            dx, dy = _C164_MOVES[command[0]]
            x, y = result[actor]
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                result[actor] = [nx, ny]
    for order in action.get("market") or []:
        if order and order[0] == "HIRE":
            target = min(_C164_ACCESS,
                         key=lambda pos: (sum(tuple(p) == pos for p in result),
                                          _C164_ACCESS.index(pos)))
            result.append(list(target))
    return result


def _c164_native_context(observation, parent_action):
    seat = int(observation["player"])
    step = int(observation["step"])
    state = getattr(getattr(_IMPL, "chassis", None), "players", {}).get(seat, {})
    route = state.get("route")
    routes = getattr(getattr(_IMPL, "chassis", None), "routes", {})
    if route not in routes or step + 1 >= len(routes[route]):
        return None
    positions = [observation["farms"][seat]["farmer"],
                 *observation["farms"][seat].get("hands", [])]
    positions = _c164_move_positions(positions, parent_action)
    nxt = routes[route][step + 1]
    if not isinstance(nxt, dict):
        nxt = {}
    return route, routes[route], positions, nxt


def _c164_future_fertilizes(tape, actor, start, end):
    count = 0
    for step in range(start, min(end, len(tape) - 1) + 1):
        commands = _c164_commands(tape[step] if isinstance(tape[step], dict) else {}, actor + 1)
        count += int(actor < len(commands) and commands[actor] == ["FERTILIZE"])
    return count


def _c164_same_turn(observation, parent_action, state, blocked=None):
    seat = int(observation["player"])
    day = int(observation["step"]) // 24
    farm, private = observation["farms"][seat], observation["private"]
    positions = [farm["farmer"], *farm.get("hands", [])]
    commands = _c164_commands(parent_action, len(positions))
    inventories = private.get("inventories", [])
    blocked = blocked or set()
    by_tile = {}
    for actor, (pos, command) in enumerate(zip(positions, commands)):
        if command and command[0] != "PASS":
            by_tile.setdefault(tuple(pos), []).append((actor, command[0]))
    context = _c164_native_context(observation, parent_action)
    tape = context[1] if context is not None else None
    step = int(observation["step"])
    end = (day + 1) * 24 - 1
    changes = []
    for target, events in by_tile.items():
        if target in blocked or len(events) != 2:
            continue
        water = [actor for actor, op in events if op == "WATER"]
        fertilizer = [actor for actor, op in events if op == "FERTILIZE"]
        if len(water) != 1 or len(fertilizer) != 1 or water[0] > fertilizer[0]:
            continue
        state["checks"] += 1
        x, y = target
        tile = farm["tiles"][y][x]
        gain = _c164_gain(tile, day)
        if not gain:
            state["declined_no_gain"] += 1
            continue
        wa, fa = water[0], fertilizer[0]
        if (wa >= len(inventories) or fa >= len(inventories)
                or inventories[wa].get("FERTILIZER", 0) <= 0
                or inventories[fa].get("FERTILIZER", 0) <= 0):
            state["declined_inventory"] += 1
            continue
        # The WATER worker spends one fertilizer earlier than the native plan.
        # Preserve every remaining fertilizer command already committed to that
        # actor for the rest of the day.  If the route cannot be inspected, the
        # exchange is not certified and must fail closed.
        if tape is None:
            state["declined_no_route"] += 1
            continue
        later_need = _c164_future_fertilizes(tape, wa, step + 1, end)
        if inventories[wa].get("FERTILIZER", 0) < 1 + later_need:
            state["declined_future_commitment"] += 1
            continue
        changes.append((wa, fa, target, tile["crop"], int(tile["planted_day"]), gain))
    if not changes:
        return parent_action, set()
    result = _c164_copy.deepcopy(parent_action)
    touched = set()
    for wa, fa, target, crop, birth, gain in changes:
        _c164_set(result, wa, ["FERTILIZE"])
        _c164_set(result, fa, ["WATER"])
        touched.add(target)
        state["same_turn_swaps"] += 1
        state["requested_extra_yield"] += gain
        if int(observation["step"]) % 24 < 23:
            state["confirm"].append({"step": int(observation["step"]) + 1,
                                     "target": target, "crop": crop,
                                     "birth": birth, "day": day})
    return result, touched


def _c164_start_next(observation, action, state, touched):
    seat = int(observation["player"])
    step = int(observation["step"])
    day, hour = divmod(step, 24)
    if hour >= 23:
        return action
    context = _c164_native_context(observation, action)
    if context is None:
        state["declined_no_route"] += 1
        return action
    route, tape, next_positions, next_action = context
    farm, private = observation["farms"][seat], observation["private"]
    positions = [farm["farmer"], *farm.get("hands", [])]
    commands = _c164_commands(action, len(positions))
    next_commands = _c164_commands(next_action, len(next_positions))
    inventories = private.get("inventories", [])
    current_by_tile = {}
    for actor, (pos, command) in enumerate(zip(positions, commands)):
        if command and command[0] != "PASS":
            current_by_tile.setdefault(tuple(pos), []).append((actor, command[0]))
    next_by_tile = {}
    for actor, (pos, command) in enumerate(zip(next_positions, next_commands)):
        if command and command[0] != "PASS":
            next_by_tile.setdefault(tuple(pos), []).append((actor, command[0]))
    starts = []
    reserved_due_actors = {pending["actor"] for pending in state["pending"]
                           if pending["step"] == step + 1}
    for target, now_events in current_by_tile.items():
        if target in touched or len(now_events) != 1 or now_events[0][1] != "WATER":
            continue
        future_events = next_by_tile.get(target, [])
        if len(future_events) != 1 or future_events[0][1] != "FERTILIZE":
            continue
        wa, fa = now_events[0][0], future_events[0][0]
        if fa in reserved_due_actors:
            continue
        state["checks"] += 1
        x, y = target
        tile = farm["tiles"][y][x]
        gain = _c164_gain(tile, day)
        if not gain:
            state["declined_no_gain"] += 1
            continue
        if (wa >= len(inventories) or fa >= len(inventories)
                or inventories[wa].get("FERTILIZER", 0) <= 0
                or inventories[fa].get("FERTILIZER", 0) <= 0):
            state["declined_inventory"] += 1
            continue
        later_need = _c164_future_fertilizes(tape, wa, step + 2, (day + 1) * 24 - 1)
        if inventories[wa].get("FERTILIZER", 0) < 1 + later_need:
            state["declined_future_commitment"] += 1
            continue
        starts.append((wa, fa, target, tile["crop"], int(tile["planted_day"]), gain))
        reserved_due_actors.add(fa)
    if not starts:
        return action
    result = _c164_copy.deepcopy(action)
    for wa, fa, target, crop, birth, gain in starts:
        _c164_set(result, wa, ["FERTILIZE"])
        state["pending"].append({"step": step + 1, "actor": fa, "target": target,
                                 "crop": crop, "birth": birth, "day": day,
                                 "gain": gain})
        state["next_turn_starts"] += 1
        state["requested_extra_yield"] += gain
    return result


def _c164_complete_pending(observation, parent_action, state):
    step = int(observation["step"])
    seat = int(observation["player"])
    farm = observation["farms"][seat]
    positions = [farm["farmer"], *farm.get("hands", [])]
    commands = _c164_commands(parent_action, len(positions))
    result = None
    keep = []
    blocked = set()
    for pending in state["pending"]:
        if pending["step"] != step:
            if pending["step"] < step:
                state["contract_errors"] += 1
            else:
                keep.append(pending)
            continue
        x, y = pending["target"]
        blocked.add(pending["target"])
        tile = farm["tiles"][y][x]
        same = (isinstance(tile, dict) and tile.get("crop") == pending["crop"]
                and int(tile.get("planted_day", -1)) == pending["birth"])
        if not same:
            state["contract_errors"] += 1
            continue
        if int(tile.get("fertilized_until_day", -1)) >= pending["day"] + 2:
            state["fertilizer_confirmations"] += 1
        else:
            state["contract_errors"] += 1
            # The previous callback's replacement FERTILIZE did not take
            # effect.  Preserve the native FERTILIZE now; emitting WATER here
            # would silently turn a failed exchange into a lost application.
            continue
        actor = pending["actor"]
        exact = (actor < len(positions) and tuple(positions[actor]) == pending["target"]
                 and commands[actor] == ["FERTILIZE"])
        external_water = any(other != actor and tuple(pos) == pending["target"]
                             and command == ["WATER"]
                             for other, (pos, command) in enumerate(zip(positions, commands)))
        if external_water:
            # One WATER is already scheduled on the certified tile.  Remove
            # only the now-redundant native FERTILIZE from its expected actor.
            if exact:
                if result is None:
                    result = _c164_copy.deepcopy(parent_action)
                _c164_set(result, actor, ["PASS"])
            state["next_turn_completions"] += 1
            if step % 24 < 23:
                state["confirm"].append({"step": step + 1, "target": pending["target"],
                                         "crop": pending["crop"], "birth": pending["birth"],
                                         "day": pending["day"]})
        elif exact:
            if result is None:
                result = _c164_copy.deepcopy(parent_action)
            _c164_set(result, actor, ["PASS"] if tile.get("watered_today") else ["WATER"])
            state["next_turn_completions"] += 1
            if not tile.get("watered_today") and step % 24 < 23:
                state["confirm"].append({"step": step + 1, "target": pending["target"],
                                         "crop": pending["crop"], "birth": pending["birth"],
                                         "day": pending["day"]})
        else:
            state["contract_errors"] += 1
    state["pending"] = keep
    return (result if result is not None else parent_action), blocked


def _c164_confirm(observation, state):
    step = int(observation["step"])
    farm = observation["farms"][int(observation["player"])]
    keep = []
    for item in state["confirm"]:
        if item["step"] != step:
            if item["step"] < step:
                state["contract_errors"] += 1
            else:
                keep.append(item)
            continue
        x, y = item["target"]
        tile = farm["tiles"][y][x]
        if (isinstance(tile, dict) and tile.get("crop") == item["crop"]
                and int(tile.get("planted_day", -1)) == item["birth"]
                and tile.get("watered_today")
                and int(tile.get("fertilized_until_day", -1)) >= item["day"] + 2):
            state["water_confirmations"] += 1
        else:
            state["contract_errors"] += 1
    state["confirm"] = keep


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _C164_STATE.get(seat)
    if state is None or step <= state["last"]:
        state = _C164_STATE[seat] = _c164_new_state()
    parent_action = _C164_PARENT(observation, configuration)
    result = parent_action
    working = _c164_copy.deepcopy(state)
    working["last"] = step
    try:
        _c164_confirm(observation, working)
        if _c164_standard(observation, configuration):
            result, blocked = _c164_complete_pending(observation, parent_action, working)
            result, touched = _c164_same_turn(observation, result, working, blocked)
            result = _c164_start_next(observation, result, working, touched | blocked)
        state = working
        _C164_STATE[seat] = state
    except Exception:
        state["last"] = step
        state["errors"] += 1
        result = parent_action
    _C164_REPORT.clear()
    _C164_REPORT.update(getattr(_C164_PARENT, "telemetry", {}))
    _C164_REPORT.update({"c164_" + key: value for key, value in state.items()
                         if key not in ("last", "pending", "confirm")})
    return result


agent.telemetry = _C164_REPORT
agent = globals().pop("agent")
