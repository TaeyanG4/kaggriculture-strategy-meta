# SPDX-License-Identifier: Apache-2.0
"""Harvest existing persistent-crop yield before the terminal planner starts.

The parent terminal planner takes control at step 712.  During steps 696..711,
WATER or FERTILIZE cannot create another sellable end-of-day TOMATO/STRAWBERRY
crop, but an already present yield can still be harvested and handed to that
planner.  This overlay changes only that exact unit command and leaves market,
movement, hiring, planting, and all earlier production policy untouched.
"""
import copy as _c160_copy


_C160_PARENT = agent
_C160_STATE = {}
_C160_REPORT = {}
_C160_PERSISTENT = {"TOMATO", "STRAWBERRY"}
del agent


def _c160_standard(observation, configuration):
    try:
        farm = observation["farms"][int(observation["player"])]
        if len(farm["tiles"]) != 10 or any(len(row) != 10 for row in farm["tiles"]):
            return False
        if configuration is None:
            return True
        return all(configuration.get(key, expected) == expected for key, expected in (
            ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100),
            ("maxMarketOrdersPerTurn", 10), ("farmHandCostMult", 1),
            ("episodeSteps", 720)))
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def _c160_commands(action, count):
    commands = [list(action.get("farmer") or ["PASS"])]
    commands.extend(list(command or ["PASS"]) for command in (action.get("hands") or []))
    commands.extend([["PASS"] for _ in range(max(0, count - len(commands)))])
    return commands[:count]


def _c160_set(action, actor, command):
    if actor == 0:
        action["farmer"] = list(command)
        return
    hands = action.setdefault("hands", [])
    while len(hands) < actor:
        hands.append(["PASS"])
    hands[actor - 1] = list(command)


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _C160_STATE.get(seat)
    if state is None or step <= state["last"]:
        state = {"last": -1, "checks": 0, "harvest_replacements": 0,
                 "tomato_replacements": 0, "strawberry_replacements": 0,
                 "yield_units_requested": 0, "errors": 0}
        _C160_STATE[seat] = state
    state["last"] = step
    parent_action = _C160_PARENT(observation, configuration)
    result = parent_action
    try:
        if 696 <= step < 712 and _c160_standard(observation, configuration):
            farm = observation["farms"][seat]
            positions = [farm["farmer"], *farm.get("hands", [])]
            commands = _c160_commands(parent_action, len(positions))
            replacements = []
            for actor, (position, command) in enumerate(zip(positions, commands)):
                if command not in (["WATER"], ["FERTILIZE"]):
                    continue
                state["checks"] += 1
                x, y = position
                tile = farm["tiles"][y][x]
                if not isinstance(tile, dict) or tile.get("crop") not in _C160_PERSISTENT:
                    continue
                available = max(0, int(tile.get("yield_units", 0) or 0))
                if available <= 0:
                    continue
                replacements.append((actor, tile["crop"], available))
            if replacements:
                result = _c160_copy.deepcopy(parent_action)
                for actor, crop, available in replacements:
                    _c160_set(result, actor, ["HARVEST"])
                    state["harvest_replacements"] += 1
                    state[crop.lower() + "_replacements"] += 1
                    state["yield_units_requested"] += available
    except (KeyError, TypeError, ValueError, IndexError):
        state["errors"] += 1
        result = parent_action
    _C160_REPORT.clear()
    _C160_REPORT.update(getattr(_C160_PARENT, "telemetry", {}))
    _C160_REPORT.update({"day29_harvest_" + key: value for key, value in state.items()
                         if key != "last"})
    return result


agent.telemetry = _C160_REPORT
agent = globals().pop("agent")
