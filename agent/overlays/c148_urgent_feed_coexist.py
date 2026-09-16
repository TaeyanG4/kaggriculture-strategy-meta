# SPDX-License-Identifier: Apache-2.0
"""Let imminent-escape feed support coexist with the parent's market prefix.

The c129 parent already funds next-turn WHEAT pickups when the current market
queue is empty or SELL-only.  This overlay handles only the otherwise rejected
case: a currently unfed animal has consecutive_unfed >= 1, its known own route
will PICKUP WHEAT next turn and FEED that same day, and the parent also needs a
HIRE/BUY order now.  Parent unit actions and market-prefix order are immutable.
"""

import copy as _c148_copy


_C148_PARENT = agent
_C148_STATES = {}
_C148_REPORT = {}
_C148_SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                   "STRAWBERRY": 100, "MELON": 80}
_C148_ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
_C148_LAND_COST = (1000, 2000, 4000)
del agent


def _c148_command(action, actor):
    if actor == 0:
        return list(action.get("farmer") or ["PASS"])
    hands = action.get("hands") or []
    return list(hands[actor - 1]) if actor <= len(hands) else ["PASS"]


def _c148_move(pos, command):
    dx, dy = _CP0_MOVES.get(command[0], (0, 0))
    return [max(0, min(9, pos[0] + dx)), max(0, min(9, pos[1] + dy))]


def _c148_unit_cost(obs, item):
    price = max(1, int(obs["market"]["prices"][item]))
    return max(price + 10, 2 * price)


def _c148_market_projection(obs, orders, projected):
    """Return conservative prefix cash cost, total stock and next-turn WHEAT.

    SELL proceeds are not credited.  BUY costs are upper-bounded and every
    product/animal purchase is assumed to fill the shed before our final order.
    """
    farm = obs["farms"][int(obs["player"])]
    stock = {key: int(value) for key, value in projected.items()}
    total = sum(stock.values())
    hires = int(farm.get("hires_today", 0))
    unlocked = max(0, len(farm.get("unlocked_quadrants", [])) - 1)
    lands = 0
    cost = 0
    for order in orders:
        if not isinstance(order, list) or not order:
            return None
        op = order[0]
        if op == "SELL" and len(order) == 3 and order[1] in stock:
            quantity = max(0, int(order[2]))
            sold = min(quantity, stock.get(order[1], 0))
            stock[order[1]] = stock.get(order[1], 0) - sold
            total -= sold
        elif op == "HIRE" and len(order) == 1:
            cost += _v219_fib(hires)
            hires += 1
        elif op == "BUY_LAND" and len(order) == 1:
            slot = unlocked + lands
            if slot >= len(_C148_LAND_COST):
                return None
            cost += _C148_LAND_COST[slot]
            lands += 1
        elif op == "BUY_SEED" and len(order) == 3 and order[1] in _C148_SEED_COST:
            cost += max(0, int(order[2])) * _C148_SEED_COST[order[1]]
        elif op == "BUY_PRODUCT" and len(order) == 3 and order[1] in PRODUCTS:
            quantity = max(0, int(order[2]))
            cost += quantity * _c148_unit_cost(obs, order[1])
            stock[order[1]] = stock.get(order[1], 0) + quantity
            total += quantity
        elif op == "BUY_ANIMAL" and len(order) == 3 and order[1] in _C148_ANIMAL_COST:
            quantity = max(0, int(order[2]))
            cost += quantity * _C148_ANIMAL_COST[order[1]]
            stock[order[1]] = stock.get(order[1], 0) + quantity
            total += quantity
        else:
            return None
        if total > 100:
            return None
    return {"cost": cost, "total": total, "wheat": stock.get("WHEAT", 0)}


def _c148_urgent_targets(obs, parent, tape):
    """Find existing consecutive-unfed animals reached after next WHEAT pickup."""
    step = int(obs["step"])
    seat = int(obs["player"])
    farm = obs["farms"][seat]
    private = obs["private"]
    positions = [farm["farmer"], *farm["hands"]]
    current = [_c148_command(parent, actor) for actor in range(len(positions))]
    targets = []
    for actor, pos in enumerate(positions):
        pickup = _cp0_command(tape[step + 1], actor)
        if len(pickup) < 2 or pickup[:2] != ["PICKUP", "WHEAT"]:
            continue
        future_pos = _c148_move(pos, current[actor])
        if not _shed_adjacent(future_pos, 10):
            continue
        cursor = list(future_pos)
        end = min(len(tape), step + 10, (step // 24 + 1) * 24)
        for future in range(step + 2, end):
            command = _cp0_command(tape[future], actor)
            if command and command[0] in _CP0_MOVES:
                cursor = _c148_move(cursor, command)
                continue
            if command != ["FEED"]:
                continue
            tile = farm["tiles"][cursor[1]][cursor[0]]
            if (isinstance(tile, dict) and tile.get("animal")
                    and not tile.get("fed_today")
                    and int(tile.get("consecutive_unfed", 0)) >= 1):
                carried = int(private["inventories"][actor].get("WHEAT", 0))
                need = max(0, 1 - carried)
                if need and (int(pickup[2]) if len(pickup) > 2 else 1) >= need:
                    targets.append({
                        "actor": actor,
                        "animal": tile["animal"],
                        "position": list(cursor),
                        "pickup_step": step + 1,
                        "feed_step": future,
                        "survival_step": (future // 24 + 1) * 24,
                        "need": need,
                    })
            break
    return targets


def _c148_required_wheat(obs, parent, tape, targets):
    """Minimal next-turn shed stock that lets every target obtain one WHEAT."""
    seat = int(obs["player"])
    farm = obs["farms"][seat]
    private = obs["private"]
    positions = [farm["farmer"], *farm["hands"]]
    current = [_c148_command(parent, actor) for actor in range(len(positions))]
    urgent = {target["actor"]: target for target in targets}
    cumulative = 0
    required = 0
    for actor in range(max(urgent) + 1):
        pickup = _cp0_command(tape[int(obs["step"]) + 1], actor)
        if len(pickup) < 2 or pickup[:2] != ["PICKUP", "WHEAT"]:
            continue
        if actor >= len(positions):
            continue
        future_pos = _c148_move(positions[actor], current[actor])
        if not _shed_adjacent(future_pos, 10):
            continue
        quantity = max(0, int(pickup[2]) if len(pickup) > 2 else 1)
        if actor in urgent:
            carried = int(private["inventories"][actor].get("WHEAT", 0))
            required = max(required, cumulative + max(0, 1 - carried))
        cumulative += quantity
    return required


def _c148_observe(obs, state):
    step = int(obs["step"])
    seat = int(obs["player"])
    farm = obs["farms"][seat]
    private = obs["private"]
    remaining = []
    for plan in state["plans"]:
        actor = plan["actor"]
        if step == plan["pickup_step"] and not plan["purchase_checked"]:
            plan["purchase_checked"] = True
            plan["purchase_ok"] = int(private["shed"].get("WHEAT", 0)) >= plan["required_wheat"]
            state["purchase_confirmed"] += int(plan["purchase_ok"])
        if step == plan["pickup_step"] + 1 and not plan["pickup_checked"]:
            plan["pickup_checked"] = True
            inv = private["inventories"][actor] if actor < len(private["inventories"]) else {}
            plan["pickup_ok"] = int(inv.get("WHEAT", 0)) >= 1
            state["pickup_confirmed"] += int(plan["pickup_ok"])
        if step == plan["feed_step"] + 1 and not plan["feed_checked"]:
            plan["feed_checked"] = True
            x, y = plan["position"]
            tile = farm["tiles"][y][x]
            plan["feed_ok"] = bool(isinstance(tile, dict)
                                   and tile.get("animal") == plan["animal"]
                                   and tile.get("fed_today"))
            state["feed_confirmed"] += int(plan["feed_ok"])
        if step == plan["survival_step"]:
            x, y = plan["position"]
            tile = farm["tiles"][y][x]
            plan["survival_ok"] = bool(isinstance(tile, dict)
                                       and tile.get("animal") == plan["animal"])
            state["survival_confirmed"] += int(plan["survival_ok"])
            if not all(plan.get(key, False) for key in
                       ("purchase_ok", "pickup_ok", "feed_ok", "survival_ok")):
                state["contract_failures"] += 1
            continue
        if step > plan["survival_step"]:
            state["contract_failures"] += 1
            continue
        remaining.append(plan)
    state["plans"] = remaining


def _c148_control(obs, parent, state, parent_units, parent_day_units):
    step = int(obs["step"])
    seat = int(obs["player"])
    if not 144 <= step < 432 or step % 24 >= 22 or state["plans"]:
        return parent
    orders = [list(order) for order in parent.get("market", [])]
    # SELL-only queues remain exclusively owned by the existing parent buffer.
    if len(orders) >= 10 or not any(order and order[0] != "SELL" for order in orders):
        return parent
    farm = obs["farms"][seat]
    if len(farm["tiles"]) != 10 or float(farm["money"]) < 100:
        return parent
    route = _IMPL.chassis.players[seat]["route"]
    tape = _ROUTES[route]
    targets = _c148_urgent_targets(obs, parent, tape)
    if not targets:
        return parent
    state["urgent_opportunities"] += 1
    required = _c148_required_wheat(obs, parent, tape, targets)
    projected = projected_shed(parent, FarmView(obs))
    prefix = _c148_market_projection(obs, orders, projected)
    if prefix is None:
        state["prefix_declines"] += 1
        return parent
    deficit = max(0, required - int(prefix["wheat"]))
    if deficit <= 0:
        state["already_funded"] += 1
        return parent
    day_room = 4 - parent_day_units - state["day_units"]
    game_room = 12 - parent_units - state["units"]
    if deficit > min(day_room, game_room):
        state["quantity_declines"] += 1
        return parent
    if prefix["total"] + deficit > 96:
        state["capacity_declines"] += 1
        return parent
    cost = prefix["cost"] + deficit * _c148_unit_cost(obs, "WHEAT")
    if float(farm["money"]) < cost + 100:
        state["budget_declines"] += 1
        return parent
    result = _c148_copy.deepcopy(parent)
    result.setdefault("market", []).append(["BUY_PRODUCT", "WHEAT", deficit])
    expected = int(prefix["wheat"]) + deficit
    for target in targets:
        target.update({
            "required_wheat": required,
            "expected_wheat": expected,
            "purchase_checked": False,
            "purchase_ok": False,
            "pickup_checked": False,
            "pickup_ok": False,
            "feed_checked": False,
            "feed_ok": False,
            "survival_ok": False,
        })
    state["plans"] = targets
    state["requests"] += 1
    state["units"] += deficit
    state["day_units"] += deficit
    state["targets"] += len(targets)
    return result


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _C148_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _C148_STATES[seat] = {
            "last": -1, "day": -1, "day_units": 0, "units": 0,
            "last_parent_units": 0, "parent_units_at_day_start": 0,
            "plans": [], "requests": 0, "targets": 0,
            "urgent_opportunities": 0, "already_funded": 0,
            "purchase_confirmed": 0, "pickup_confirmed": 0,
            "feed_confirmed": 0, "survival_confirmed": 0,
            "prefix_declines": 0, "quantity_declines": 0,
            "capacity_declines": 0, "budget_declines": 0,
            "contract_failures": 0, "errors": 0,
        }
    if state["day"] != step // 24:
        state["day"] = step // 24
        state["day_units"] = 0
        state["parent_units_at_day_start"] = state["last_parent_units"]
    state["last"] = step
    _c148_observe(observation, state)
    parent = _C148_PARENT(observation, configuration)
    parent_report = getattr(_C148_PARENT, "telemetry", {})
    parent_units = int(parent_report.get("feed_buffer_units", 0))
    parent_day_units = max(0, parent_units - state["parent_units_at_day_start"])
    result = parent
    try:
        supported = configuration is None or all(configuration.get(key, value) == value for key, value in (
            ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100),
            ("farmHandCostMult", 1), ("maxMarketOrdersPerTurn", 10)))
        if supported:
            result = _c148_control(observation, parent, state, parent_units, parent_day_units)
    except Exception:
        state["errors"] += 1
        result = parent
    state["last_parent_units"] = parent_units
    _C148_REPORT.clear()
    _C148_REPORT.update(parent_report)
    _C148_REPORT.update({"urgent_feed_" + key: value for key, value in state.items()
                         if isinstance(value, int) and key not in
                         ("last", "day", "day_units", "last_parent_units", "parent_units_at_day_start")})
    return result


agent.telemetry = _C148_REPORT
agent = globals().pop("agent")
