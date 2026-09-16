# SPDX-License-Identifier: Apache-2.0
"""Production-calendar harvests that recover animal yield otherwise clipped at dawn.

This overlay is deliberately narrower than a harvest-threshold tuner.  It changes
only a parent's CARE command when the official 1.32.7 calendar proves that the
animal produces at the coming end of day and its held yield plus that production
would exceed the species cap.  The parent's remaining native actions for the same
day are projected from the current real positions; a planned later HARVEST makes
the overlay abstain.

Replacing an effective CARE may forfeit one bonus unit at a later sellable
production.  A swap therefore requires strictly more clipped units than that
worst-case loss.  A same-turn or later native CARE preserves the bonus and reduces
the charge to zero.  On day 28 there is no later end-of-day production before the
game stops, so CARE has no future production value.

The parent is called exactly once.  Market orders, movement, feeding, purchases,
and all non-CARE commands are preserved byte-for-byte.  Requested/forecast units
in telemetry are mechanism diagnostics, not realized harvest or revenue.
"""
import copy as _c156_copy


_C156_PARENT = agent
_C156_STATE = {}
_C156_REPORT = {}
_C156_SPEC = {
    "GOOSE": {"first": 4, "interval": 1, "cap": 4, "product": "EGG"},
    "COW": {"first": 8, "interval": 2, "cap": 6, "product": "MILK"},
    "SHEEP": {"first": 6, "interval": 3, "cap": 6, "product": "WOOL"},
}
_C156_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
_C156_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
_C156_LAST_EOD = 28
_C156_MAX_FORECAST_STEPS = 8
del agent


def _c156_new_state():
    return {
        "last": -1,
        "calendar_checks": 0,
        "clip_opportunities": 0,
        "forecast_clipped_units": 0,
        "harvest_swaps": 0,
        "requested_harvest_units": 0,
        "confirmed_harvest_units": 0,
        "confirmation_errors": 0,
        "declined_not_fed": 0,
        "declined_lookahead": 0,
        "declined_no_route": 0,
        "declined_parent_harvest": 0,
        "declined_future_harvest": 0,
        "declined_tradeoff": 0,
        "declined_eod_capacity": 0,
        "care_preserved": 0,
        "errors": 0,
        "pending": [],
    }


def _c156_standard(observation, configuration):
    farm = observation["farms"][int(observation["player"])]
    if len(farm["tiles"]) != 10:
        return False
    if configuration is None:
        return True
    return all(configuration.get(key, expected) == expected for key, expected in (
        ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100),
        ("maxMarketOrdersPerTurn", 10), ("farmHandCostMult", 1),
        ("episodeSteps", 720)))


def _c156_commands(action, count):
    result = [list(action.get("farmer") or ["PASS"])]
    result.extend(list(command or ["PASS"]) for command in (action.get("hands") or []))
    result.extend([["PASS"] for _ in range(max(0, count - len(result)))])
    return result[:count]


def _c156_set_command(action, actor, command):
    if actor == 0:
        action["farmer"] = list(command)
    else:
        action["hands"][actor - 1] = list(command)


def _c156_produces(tile, end_day):
    spec = _C156_SPEC[tile["animal"]]
    age = end_day + 1 - int(tile.get("placed_day", 0)) - spec["first"]
    return age >= 0 and age % spec["interval"] == 0


def _c156_has_later_sellable_production(tile, day):
    return any(_c156_produces(tile, future_day)
               for future_day in range(day + 1, _C156_LAST_EOD + 1))


def _c156_move_positions(positions, action):
    result = [list(pos) for pos in positions]
    for actor, command in enumerate(_c156_commands(action, len(result))):
        if command and command[0] in _C156_MOVES:
            dx, dy = _C156_MOVES[command[0]]
            x, y = result[actor]
            nx, ny = x + dx, y + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                result[actor] = [nx, ny]
    for order in action.get("market") or []:
        if order and order[0] == "HIRE":
            target = min(_C156_ACCESS,
                         key=lambda pos: (sum(tuple(p) == pos for p in result),
                                          _C156_ACCESS.index(pos)))
            result.append(list(target))
    return result


def _c156_remaining_native_events(observation, parent_action, target):
    """Return later native HARVEST/CARE signals for one tile before this dawn.

    The check is a veto/preservation proof only.  It never calls the policy or
    assumes future private resources.  If route state cannot be read, the caller
    abstains instead of guessing.
    """
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
    positions = _c156_move_positions(positions, parent_action)
    later_harvest = False
    later_care = False
    for future_step in range(step + 1, min(end_step, len(tape) - 1) + 1):
        native = tape[future_step] if isinstance(tape[future_step], dict) else {}
        commands = _c156_commands(native, len(positions))
        for pos, command in zip(positions, commands):
            if tuple(pos) != target or not command:
                continue
            later_harvest = later_harvest or command[0] == "HARVEST"
            later_care = later_care or command[0] == "CARE"
        positions = _c156_move_positions(positions, native)
    return later_harvest, later_care


def _c156_known_fed(tile, target, positions, commands, inventories):
    if tile.get("fed_today"):
        return True
    for actor, (pos, command) in enumerate(zip(positions, commands)):
        if (tuple(pos) == target and command == ["FEED"] and
                actor < len(inventories) and inventories[actor].get("WHEAT", 0) > 0):
            return True
    return False


def _c156_eod_capacity_safe(observation, parent_action, added_units):
    """Conservative hour-23 bound; prior hours are covered by o182 on its later call."""
    if int(observation["step"]) % 24 != 23:
        return True
    private = observation["private"]
    total = sum(max(0, int(v)) for v in private.get("shed", {}).values())
    total += sum(max(0, int(v)) for inv in private.get("inventories", []) for v in inv.values())
    # Ignore sales and consumed unit cargo; count every requested capacity-using buy.
    buys = sum(max(0, int(order[2])) for order in (parent_action.get("market") or [])
               if len(order) >= 3 and order[0] in ("BUY_PRODUCT", "BUY_ANIMAL"))
    return total + buys + added_units <= 100


def _c156_confirm(observation, state):
    step = int(observation["step"])
    remaining = []
    inventories = observation["private"].get("inventories", [])
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
        now = int(inventories[actor].get(pending["product"], 0))
        gained = max(0, now - pending["before"])
        state["confirmed_harvest_units"] += min(pending["units"], gained)
        if gained < pending["units"]:
            state["confirmation_errors"] += 1
    state["pending"] = remaining


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _C156_STATE.get(seat)
    if state is None or step <= state["last"]:
        state = _C156_STATE[seat] = _c156_new_state()
    state["last"] = step
    parent_action = _C156_PARENT(observation, configuration)
    result = parent_action
    try:
        _c156_confirm(observation, state)
        day, hour = divmod(step, 24)
        if not _c156_standard(observation, configuration) or day > _C156_LAST_EOD:
            raise StopIteration
        remaining = 23 - hour
        if remaining > _C156_MAX_FORECAST_STEPS:
            state["declined_lookahead"] += 1
            raise StopIteration
        farm = observation["farms"][seat]
        private = observation["private"]
        positions = [farm["farmer"], *farm.get("hands", [])]
        commands = _c156_commands(parent_action, len(positions))
        inventories = private.get("inventories", [])
        care_by_tile = {}
        harvest_tiles = set()
        for actor, (pos, command) in enumerate(zip(positions, commands)):
            target = tuple(pos)
            if command == ["CARE"]:
                care_by_tile.setdefault(target, []).append(actor)
            elif command == ["HARVEST"]:
                harvest_tiles.add(target)
        swaps = []
        added = 0
        for target, care_actors in care_by_tile.items():
            x, y = target
            tile = farm["tiles"][y][x]
            if not isinstance(tile, dict) or tile.get("animal") not in _C156_SPEC:
                continue
            state["calendar_checks"] += 1
            if target in harvest_tiles:
                state["declined_parent_harvest"] += 1
                continue
            if not _c156_produces(tile, day):
                continue
            held = max(0, int(tile.get("yield_units", 0) or 0))
            if held <= 0:
                continue
            if not _c156_known_fed(tile, target, positions, commands, inventories):
                state["declined_not_fed"] += 1
                continue
            spec = _C156_SPEC[tile["animal"]]
            incoming = 1 + max(0, int(tile.get("pending_care_bonus", 0) or 0))
            clipped = max(0, held + incoming - spec["cap"])
            if clipped <= 0:
                continue
            state["clip_opportunities"] += 1
            state["forecast_clipped_units"] += clipped
            events = _c156_remaining_native_events(observation, parent_action, target)
            if events is None:
                state["declined_no_route"] += 1
                continue
            later_harvest, later_care = events
            if later_harvest:
                state["declined_future_harvest"] += 1
                continue
            # Use the last same-turn CARE: earlier CARE then remains effective.
            actor = care_actors[-1]
            care_preserved = len(care_actors) > 1 or later_care or tile.get("cared_today", False)
            future_cost = 0 if care_preserved or not _c156_has_later_sellable_production(tile, day) else 1
            if clipped <= future_cost:
                state["declined_tradeoff"] += 1
                continue
            if not _c156_eod_capacity_safe(observation, parent_action, added + held):
                state["declined_eod_capacity"] += 1
                continue
            swaps.append((actor, tile["animal"], spec["product"], held,
                          int(inventories[actor].get(spec["product"], 0)) if actor < len(inventories) else 0,
                          care_preserved))
            added += held
        if swaps:
            result = _c156_copy.deepcopy(parent_action)
            for actor, kind, product, held, before, care_preserved in swaps:
                _c156_set_command(result, actor, ["HARVEST"])
                state["harvest_swaps"] += 1
                state["requested_harvest_units"] += held
                state["care_preserved"] += int(bool(care_preserved))
                if hour < 23:
                    state["pending"].append({"step": step + 1, "actor": actor,
                                             "product": product, "before": before,
                                             "units": held, "kind": kind})
    except StopIteration:
        pass
    except Exception:
        state["errors"] += 1
        result = parent_action
    _C156_REPORT.clear()
    _C156_REPORT.update(getattr(_C156_PARENT, "telemetry", {}))
    _C156_REPORT.update({"c156_" + key: value for key, value in state.items()
                         if key not in ("last", "pending")})
    return result


agent.telemetry = _C156_REPORT
agent = globals().pop("agent")
