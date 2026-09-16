# SPDX-License-Identifier: Apache-2.0
"""Complete a weed-blocked structure by consuming an existing same-day idle turn.

Append to a frozen c110/c111 source. Only the current observation and the policy's
own route are consulted. No episode IDs, replay data, opponent internals, or RNG
state are available to this overlay.
"""

_CP0_PARENT = agent
_CP0_STATES = {}
_CP0_REPORT = {}
_CP0_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}


def _cp0_command(action, actor):
    if actor == 0:
        return list(action.get("farmer") or ["PASS"])
    hands = action.get("hands") or []
    return list(hands[actor - 1]) if actor <= len(hands) else ["PASS"]


def _cp0_set(action, actor, command):
    if actor == 0:
        action["farmer"] = list(command)
    else:
        action["hands"][actor - 1] = list(command)


def _cp0_count(state, name):
    name = "pasture_" + name
    state["counts"][name] = state["counts"].get(name, 0) + 1


def _cp0_plan(obs, action, tape, actor):
    """Return a route detour only when it has an economically inert idle budget.

    Moving/WATER can be delayed within the same day. Resource transfers, harvest,
    feed, purchases of labor, and every other field command exclude the window.
    WATER targets must already be planted and survive the complete window.
    """
    step = int(obs["step"])
    farm = obs["farms"][int(obs["player"])]; positions = [farm["farmer"], *farm["hands"]]
    command = _cp0_command(tape[step], actor)
    if command not in (["BUILD_PASTURE"], ["BUILD_COOP"]):
        return None
    pos = list(positions[actor]); x, y = pos
    tile = farm["tiles"][y][x]
    if not (isinstance(tile, dict) and tile.get("kind") == "WEED"
            and _cp0_command(action, actor) == ["DIG"]):
        return None
    # The target belongs to one actor for this turn; don't displace shared work.
    if any(i != actor and list(p) == pos for i, p in enumerate(positions)):
        return None
    commands = []; current = list(pos)
    stop = min(len(tape), (step // 24 + 1) * 24)
    for future in range(step + 1, stop):
        if any(o and o[0] == "HIRE" for o in tape[future].get("market", [])):
            return None
        nxt = _cp0_command(tape[future], actor)
        if nxt == ["PASS"]:
            # If the first turn is already idle, the parent's queue can finish.
            if not commands:
                return None
            return {"start": step + 1, "end": future, "pos": pos,
                    "expected": list(pos), "build": command,
                    "kind": command[0][6:], "commands": commands}
        if len(nxt) != 1 or nxt[0] not in (*_CP0_MOVES, "WATER"):
            return None
        if nxt[0] in _CP0_MOVES:
            dx, dy = _CP0_MOVES[nxt[0]]
            current = [max(0, min(9, current[0] + dx)), max(0, min(9, current[1] + dy))]
        else:
            target = farm["tiles"][current[1]][current[0]]
            if not isinstance(target, dict) or target.get("kind") != "PLANT":
                return None
            # Avoid converting a decay-time weed cleanup into a delayed WATER.
            expiry = target.get("max_lifespan_step", -1)
            if expiry >= 0 and expiry <= stop:
                return None
        commands.append(nxt)
    return None


def _cp0_repair(obs, action, state, tape):
    step = int(obs["step"])
    farm = obs["farms"][int(obs["player"])]; positions = [farm["farmer"], *farm["hands"]]
    used = set()
    for actor, plan in list(state["plans"].items()):
        used.add(actor)
        if step == plan["end"] + 1 and step % 24 == 0:
            # Hands disappear at dawn. Each prior position was checked before
            # its command; next-day worker indices must not be treated as ours.
            state["plans"].pop(actor); _cp0_count(state, "overnight_completed"); continue
        if actor >= len(positions) or list(positions[actor]) != plan["expected"]:
            state["plans"].pop(actor); _cp0_count(state, "repair_errors"); continue
        if step == plan["end"] + 1:
            state["plans"].pop(actor); _cp0_count(state, "routes_rejoined"); continue
        if not plan["start"] <= step <= plan["end"]:
            state["plans"].pop(actor); _cp0_count(state, "repair_errors"); continue
        x, y = plan["pos"]; tile = farm["tiles"][y][x]
        if step == plan["start"]:
            if tile is not None:
                state["plans"].pop(actor); _cp0_count(state, "repair_errors"); continue
            command = plan["build"]
            _cp0_count(state, "build_requests")
        else:
            if step == plan["start"] + 1:
                if not isinstance(tile, dict) or tile.get("kind") != plan["kind"]:
                    state["plans"].pop(actor); _cp0_count(state, "repair_errors"); continue
                _cp0_count(state, "builds_confirmed")
            command = plan["commands"][step - plan["start"] - 1]
        _cp0_set(action, actor, command)
        if command[0] in _CP0_MOVES:
            dx, dy = _CP0_MOVES[command[0]]
            old = plan["expected"]
            plan["expected"] = [max(0, min(9, old[0] + dx)), max(0, min(9, old[1] + dy))]
        _cp0_count(state, "detour_commands")
    if step >= 144 or step >= len(tape):
        return action
    for actor in range(len(positions)):
        if actor in used:
            continue
        plan = _cp0_plan(obs, action, tape, actor)
        if plan is not None:
            state["plans"][actor] = plan
            _cp0_count(state, "detours_queued")
    return action


def agent(observation, configuration=None):
    parent = _CP0_PARENT(observation, configuration)
    step = int(observation["step"]); seat = int(observation["player"])
    state = _CP0_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _CP0_STATES[seat] = {"last": -1, "plans": {}, "counts": {}}
    state["last"] = step
    result = parent
    try:
        supported = len(observation["farms"][seat]["tiles"]) == 10
        if configuration is not None:
            supported = supported and all(configuration.get(k, v) == v for k, v in (
                ("turnsPerDay", 24), ("shedCapacity", 100), ("farmHandCostMult", 1)))
        if supported and (step < 144 or state["plans"]):
            route = _IMPL.chassis.players[seat]["route"]
            tape = _ROUTES[route]
            result = _cp0_repair(observation, copy.deepcopy(parent), state, tape)
    except Exception:
        _cp0_count(state, "repair_errors")
        state["plans"].clear()
        result = parent
    _CP0_REPORT.clear()
    _CP0_REPORT.update(getattr(_CP0_PARENT, "telemetry", {}))
    _CP0_REPORT.update(state["counts"])
    return result


agent.telemetry = _CP0_REPORT
# Kaggle 1.32.7 loads the last callable by insertion order.
agent = globals().pop("agent")
