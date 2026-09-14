# SPDX-License-Identifier: Apache-2.0
"""Swap a provably failed FEED with its next worker-owned WHEAT pickup.

Adapted from the service-order contract in Ahmed Berat Ozer's Apache-2.0
Kaggriculture V41 candidate.  This derivative keeps only the two-turn swap:
idle-worker preloads and sale-credit funding are deliberately excluded.

The parent action, current public observation, and the agent's own fixed route
are the only policy inputs.  A start is accepted only when the current FEED is
physically a no-op, the next command is that same worker's WHEAT pickup, and an
exact local unit transition proves every unchanged worker is preserved.
"""

import copy as _c149_copy


_C149_PARENT = agent
_C149_STATES = {}
_C149_REPORT = {}
_C149_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
del agent


def _c149_commands(action, count):
    commands = [list(action.get("farmer") or ["PASS"])]
    commands.extend(list(command) for command in (action.get("hands") or []))
    commands.extend([["PASS"] for _ in range(max(0, count - len(commands)))])
    return commands[:count]


def _c149_with_commands(action, commands):
    result = _c149_copy.deepcopy(action)
    result["farmer"] = commands[0]
    result["hands"] = commands[1:]
    return result


def _c149_after_units(obs, action):
    """Apply the current unit batch with the parent's embedded exact semantics."""
    seat = int(obs["player"])
    step = int(obs["step"])
    farm = _c149_copy.deepcopy(obs["farms"][seat])
    private = _c149_copy.deepcopy(obs["private"])
    count = min(1 + len(farm["hands"]), len(private["inventories"]))
    commands = _c149_commands(action, count)
    demand = {}
    for command in commands:
        if len(command) >= 2 and command[0] == "PLANT":
            demand[command[1]] = demand.get(command[1], 0) + 1
    blocked = {item for item, quantity in demand.items()
               if quantity > private["seeds"].get(item, 0)}
    for actor, command in enumerate(commands):
        effective = ["PASS"] if (len(command) >= 2 and command[0] == "PLANT"
                                  and command[1] in blocked) else command
        _UNIT_NS["_apply_unit_action"](
            farm, private, actor, effective, 10, step // 24, 24, 100
        )
    return farm, private


def _c149_start_safe(obs, parent, proposed, swaps):
    old_farm, old_private = _c149_after_units(obs, parent)
    new_farm, new_private = _c149_after_units(obs, proposed)
    if old_farm != new_farm or old_private["seeds"] != new_private["seeds"]:
        return False
    requested = sum(plan["quantity"] + 1 for plan in swaps.values())
    if any(old_private["shed"].get(item, 0) != new_private["shed"].get(item, 0)
           for item in set(old_private["shed"]) | set(new_private["shed"])
           if item != "WHEAT"):
        return False
    if new_private["shed"].get("WHEAT", 0) != old_private["shed"].get("WHEAT", 0) - requested:
        return False
    for actor, (old_inv, new_inv) in enumerate(zip(old_private["inventories"], new_private["inventories"])):
        if actor in swaps:
            expected = dict(old_inv)
            expected["WHEAT"] = expected.get("WHEAT", 0) + swaps[actor]["quantity"] + 1
            if new_inv != expected:
                return False
        elif new_inv != old_inv:
            return False
    return True


def _c149_start(obs, parent, state):
    step = int(obs["step"])
    seat = int(obs["player"])
    if not 144 <= step < 647 or step % 24 > 21 or state["pending"]:
        return parent
    farm = obs["farms"][seat]
    private = obs["private"]
    positions = [farm["farmer"], *farm["hands"]]
    count = min(len(positions), len(private["inventories"]))
    current = _c149_commands(parent, count)
    route = _IMPL.chassis.players[seat]["route"]
    future_step = step + 1
    tape = _IMPL.chassis.routes[2 if future_step >= 648 else route]
    future = _c149_commands(tape[future_step], count)
    proposed = list(current)
    swaps = {}
    for actor, command in enumerate(current):
        if command != ["FEED"] or private["inventories"][actor].get("WHEAT", 0) != 0:
            continue
        position = tuple(positions[actor])
        if position not in _C149_ACCESS:
            continue
        x, y = position
        tile = farm["tiles"][y][x]
        if not isinstance(tile, dict) or not tile.get("animal") or tile.get("fed_today"):
            continue
        pickup = future[actor]
        if len(pickup) < 2 or pickup[:2] != ["PICKUP", "WHEAT"]:
            continue
        quantity = max(0, int(pickup[2]) if len(pickup) > 2 else 1)
        if quantity <= 0:
            continue
        proposed[actor] = ["PICKUP", "WHEAT", quantity + 1]
        swaps[actor] = {
            "step": step + 1,
            "xy": list(position),
            "animal": tile["animal"],
            "birth": tile.get("placed_day"),
            "pickup": pickup,
            "quantity": quantity,
        }
    if not swaps:
        return parent
    changed = _c149_with_commands(parent, proposed)
    if not _c149_start_safe(obs, parent, changed, swaps):
        state["safety_declines"] += 1
        return parent
    state["pending"] = swaps
    state["swaps_started"] += len(swaps)
    state["wheat_loaded"] += sum(plan["quantity"] + 1 for plan in swaps.values())
    return changed


def _c149_finish(obs, parent, state):
    pending = state.pop("pending", {})
    if not pending:
        return parent
    step = int(obs["step"])
    seat = int(obs["player"])
    farm = obs["farms"][seat]
    private = obs["private"]
    positions = [farm["farmer"], *farm["hands"]]
    count = min(len(positions), len(private["inventories"]))
    commands = _c149_commands(parent, count)
    completed = 0
    for actor, plan in pending.items():
        valid = (
            step == plan["step"]
            and actor < count
            and list(positions[actor]) == plan["xy"]
            and commands[actor] == plan["pickup"]
            and private["inventories"][actor].get("WHEAT", 0) >= plan["quantity"] + 1
        )
        if valid:
            x, y = plan["xy"]
            tile = farm["tiles"][y][x]
            valid = (
                isinstance(tile, dict)
                and tile.get("animal") == plan["animal"]
                and tile.get("placed_day") == plan["birth"]
                and not tile.get("fed_today")
            )
        if not valid:
            state["contract_failures"] += 1
            continue
        commands[actor] = ["FEED"]
        completed += 1
    if not completed:
        return parent
    result = _c149_with_commands(parent, commands)
    state["swaps_completed"] += completed
    return result


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _C149_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _C149_STATES[seat] = {
            "last": -1,
            "pending": {},
            "swaps_started": 0,
            "swaps_completed": 0,
            "wheat_loaded": 0,
            "safety_declines": 0,
            "contract_failures": 0,
            "errors": 0,
        }
    parent = _C149_PARENT(observation, configuration)
    result = parent
    try:
        supported = configuration is None or all(
            configuration.get(key, value) == value
            for key, value in (
                ("boardSize", 10),
                ("turnsPerDay", 24),
                ("shedCapacity", 100),
                ("maxMarketOrdersPerTurn", 10),
                ("farmHandCostMult", 1),
            )
        )
        if supported:
            had_pending = bool(state["pending"])
            result = _c149_finish(observation, parent, state)
            if not had_pending:
                result = _c149_start(observation, result, state)
    except Exception:
        state["errors"] += 1
        state["pending"] = {}
        result = parent
    state["last"] = step
    _C149_REPORT.clear()
    _C149_REPORT.update(getattr(_C149_PARENT, "telemetry", {}))
    _C149_REPORT.update({"service_swap_" + key: value for key, value in state.items()
                         if isinstance(value, int) and key != "last"})
    return result


agent.telemetry = _C149_REPORT
agent = globals().pop("agent")
