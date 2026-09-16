# SPDX-License-Identifier: Apache-2.0
"""Fund the first feed for an already-purchased animal placement bundle.

The parent sometimes picks up a COW/SHEEP, then attempts to pick up WHEAT on
the next turn before BUILD/PLACE/FEED.  If the shed is short, the engine
silently drops the pickup and the newly placed animal can escape before it
ever produces.  This overlay changes only the current market orders: it buys
the bounded shortfall while the animal pickup is actually being attempted.

Only current public observations, the parent action, and the policy's own
route are used.  Episode IDs, rival private state, future shops, and replay
content are never consulted.
"""

import copy as _c147_copy


_C147_PARENT = agent
_C147_STATES = {}
_C147_REPORT = {}
_C147_ANIMAL_STRUCTURE = {"COW": "PASTURE", "SHEEP": "PASTURE"}
_C147_PRODUCT = {"COW": "MILK", "SHEEP": "WOOL"}
_C147_SHOPS = {
    "COW": ("PIZZA_SHOP", "SMOOTHIE_SHOP", "ICE_CREAM_SHOP"),
    "SHEEP": ("YARN_STORE",),
}
_C147_SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                   "STRAWBERRY": 100, "MELON": 80}
_C147_ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
_C147_LAND_COST = (1000, 2000, 4000)
del agent


def _c147_command(action, actor):
    if actor == 0:
        return list(action.get("farmer") or ["PASS"])
    hands = action.get("hands") or []
    return list(hands[actor - 1]) if actor <= len(hands) else ["PASS"]


def _c147_move(pos, command):
    dx, dy = _CP0_MOVES.get(command[0], (0, 0))
    return [max(0, min(9, pos[0] + dx)), max(0, min(9, pos[1] + dy))]


def _c147_market_budget(obs, orders):
    """Conservative cash need; sale proceeds are never credited."""
    seat = int(obs["player"])
    farm = obs["farms"][seat]
    hires = int(farm.get("hires_today", 0))
    unlocked = max(0, len(farm.get("unlocked_quadrants", [])) - 1)
    lands = 0
    total = 0
    for order in orders:
        if not isinstance(order, list) or not order:
            return None
        op = order[0]
        if op == "SELL" and len(order) == 3:
            continue
        if op == "HIRE" and len(order) == 1:
            total += _v219_fib(hires)
            hires += 1
        elif op == "BUY_LAND" and len(order) == 1:
            slot = unlocked + lands
            if slot >= len(_C147_LAND_COST):
                return None
            total += _C147_LAND_COST[slot]
            lands += 1
        elif op == "BUY_PRODUCT" and len(order) == 3 and order[1] in PRODUCTS:
            total += max(0, int(order[2])) * (int(obs["market"]["prices"][order[1]]) + 10)
        elif op == "BUY_SEED" and len(order) == 3 and order[1] in _C147_SEED_COST:
            total += max(0, int(order[2])) * _C147_SEED_COST[order[1]]
        elif op == "BUY_ANIMAL" and len(order) == 3 and order[1] in _C147_ANIMAL_COST:
            total += max(0, int(order[2])) * _C147_ANIMAL_COST[order[1]]
        else:
            return None
    return total


def _c147_bundle(obs, parent, tape, actor):
    """Certify PICKUP animal -> next-turn WHEAT -> PLACE -> first FEED."""
    step = int(obs["step"])
    seat = int(obs["player"])
    command = _c147_command(parent, actor)
    if len(command) < 2 or command[0] != "PICKUP" or command[1] not in _C147_ANIMAL_STRUCTURE:
        return None
    animal = command[1]
    private = obs["private"]
    if private["shed"].get(animal, 0) <= 0:
        return None
    shops = obs.get("town", {}).get("unlocked_shops", [])
    if not any(shop in shops for shop in _C147_SHOPS[animal]):
        return None
    prices = obs["market"]["prices"]
    benefit = 3 * prices[_C147_PRODUCT[animal]] + prices["FERTILIZER"]
    if prices["WHEAT"] > 100 or 10 * benefit < 13 * prices["WHEAT"]:
        return None
    stop = min(len(tape), (step // 24 + 1) * 24, step + 9)
    if step + 1 >= stop:
        return None
    pickup = _cp0_command(tape[step + 1], actor)
    if len(pickup) < 2 or pickup[:2] != ["PICKUP", "WHEAT"]:
        return None
    farm = obs["farms"][seat]
    positions = [farm["farmer"], *farm["hands"]]
    if actor >= len(positions):
        return None
    pos = list(positions[actor])
    place_step = feed_step = None
    place_xy = None
    for future in range(step + 1, stop):
        future_command = _cp0_command(tape[future], actor)
        if future_command and future_command[0] in _CP0_MOVES:
            pos = _c147_move(pos, future_command)
        elif future_command == ["PLACE", animal]:
            place_step = future
            place_xy = list(pos)
        elif future_command == ["FEED"] and place_step is not None:
            feed_step = future
            break
    if place_step is None or feed_step is None or place_xy is None:
        return None
    x, y = place_xy
    tile = farm["tiles"][y][x]
    expected = _C147_ANIMAL_STRUCTURE[animal]
    if tile is not None and not (isinstance(tile, dict) and tile.get("kind") == expected
                                 and not tile.get("animal")):
        return None
    inventory = private["inventories"][actor] if actor < len(private["inventories"]) else {}
    needed = max(0, 1 - int(inventory.get("WHEAT", 0)))
    if not needed:
        return None
    return {"actor": actor, "animal": animal, "pickup_step": step + 1,
            "place_step": place_step, "feed_step": feed_step, "place_xy": place_xy,
            "needed": needed, "purchase_seen": False, "pickup_seen": False,
            "place_seen": False, "feed_seen": False}


def _c147_observe(obs, state):
    step = int(obs["step"])
    seat = int(obs["player"])
    farm = obs["farms"][seat]
    private = obs["private"]
    remaining = []
    for plan in state["plans"]:
        actor = plan["actor"]
        if step == plan["pickup_step"] and not plan["purchase_seen"]:
            plan["purchase_seen"] = private["shed"].get("WHEAT", 0) >= plan["required_before_pickup"]
            state["purchase_confirmed_units"] += int(plan["purchase_seen"])
        if step == plan["pickup_step"] + 1 and not plan["pickup_seen"]:
            inventory = private["inventories"][actor] if actor < len(private["inventories"]) else {}
            plan["pickup_seen"] = inventory.get("WHEAT", 0) >= 1
            state["pickup_confirmed"] += int(plan["pickup_seen"])
        if step == plan["place_step"] + 1 and not plan["place_seen"]:
            x, y = plan["place_xy"]
            tile = farm["tiles"][y][x]
            plan["place_seen"] = isinstance(tile, dict) and tile.get("animal") == plan["animal"]
            state["placement_confirmed"] += int(plan["place_seen"])
        if step == plan["feed_step"] + 1:
            x, y = plan["place_xy"]
            tile = farm["tiles"][y][x]
            plan["feed_seen"] = (isinstance(tile, dict) and tile.get("animal") == plan["animal"]
                                 and bool(tile.get("fed_today")))
            state["feed_confirmed"] += int(plan["feed_seen"])
            if not all(plan[key] for key in ("purchase_seen", "pickup_seen", "place_seen", "feed_seen")):
                state["contract_failures"] += 1
            continue
        if step <= plan["feed_step"] + 1:
            remaining.append(plan)
    state["plans"] = remaining


def _c147_control(obs, parent, state):
    step = int(obs["step"])
    seat = int(obs["player"])
    if not 144 <= step < 504 or step % 24 >= 20 or state["plans"]:
        return parent
    route = _IMPL.chassis.players[seat]["route"]
    tape = _ROUTES[route]
    farm = obs["farms"][seat]
    positions = [farm["farmer"], *farm["hands"]]
    proposed = [plan for actor in range(len(positions))
                if (plan := _c147_bundle(obs, parent, tape, actor)) is not None]
    available_animals = {animal: int(obs["private"]["shed"].get(animal, 0))
                         for animal in _C147_ANIMAL_STRUCTURE}
    plans = []
    for plan in proposed:
        animal = plan["animal"]
        if available_animals[animal] > 0:
            plans.append(plan)
            available_animals[animal] -= 1
    if not plans:
        return parent
    orders = [list(order) for order in parent.get("market", [])]
    if len(orders) >= 10 or any(order[:2] == ["SELL", "WHEAT"] for order in orders):
        state["market_declines"] += 1
        return parent
    projected = projected_shed(parent, FarmView(obs))
    commands_next = [_cp0_command(tape[step + 1], actor) for actor in range(len(positions))]
    last_actor = max(plan["actor"] for plan in plans)
    required = 0
    for actor, command in enumerate(commands_next[:last_actor + 1]):
        if len(command) >= 2 and command[:2] == ["PICKUP", "WHEAT"]:
            inventory = obs["private"]["inventories"][actor] if actor < len(obs["private"]["inventories"]) else {}
            required += max(0, (int(command[2]) if len(command) > 2 else 1)
                            - int(inventory.get("WHEAT", 0)))
    existing_buy = sum(max(0, int(order[2])) for order in orders
                       if len(order) == 3 and order[:2] == ["BUY_PRODUCT", "WHEAT"])
    deficit = max(0, required - int(projected.get("WHEAT", 0)) - existing_buy)
    if deficit <= 0:
        return parent
    if deficit > 4:
        state["quantity_declines"] += 1
        return parent
    if sum(projected.values()) + existing_buy + deficit > 98:
        state["capacity_declines"] += 1
        return parent
    budget = _c147_market_budget(obs, orders)
    price = int(obs["market"]["prices"]["WHEAT"])
    if budget is None or float(farm["money"]) < budget + deficit * (price + 10) + 500:
        state["budget_declines"] += 1
        return parent
    result = _c147_copy.deepcopy(parent)
    result.setdefault("market", []).append(["BUY_PRODUCT", "WHEAT", deficit])
    for plan in plans:
        plan["required_before_pickup"] = required
    state["plans"] = plans
    state["requests"] += 1
    state["units_requested"] += deficit
    state["bundles_funded"] += len(plans)
    return result


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _C147_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _C147_STATES[seat] = {
            "last": -1, "plans": [], "requests": 0, "units_requested": 0,
            "bundles_funded": 0, "purchase_confirmed_units": 0,
            "pickup_confirmed": 0, "placement_confirmed": 0, "feed_confirmed": 0,
            "market_declines": 0, "quantity_declines": 0, "capacity_declines": 0,
            "budget_declines": 0, "contract_failures": 0, "errors": 0,
        }
    state["last"] = step
    _c147_observe(observation, state)
    parent = _C147_PARENT(observation, configuration)
    result = parent
    try:
        supported = configuration is None or all(configuration.get(key, value) == value for key, value in (
            ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100),
            ("farmHandCostMult", 1), ("maxMarketOrdersPerTurn", 10)))
        if supported:
            result = _c147_control(observation, parent, state)
    except Exception:
        state["errors"] += 1
        result = parent
    _C147_REPORT.clear()
    _C147_REPORT.update(getattr(_C147_PARENT, "telemetry", {}))
    _C147_REPORT.update({"feed_commitment_" + key: value for key, value in state.items()
                         if isinstance(value, int) and key != "last"})
    return result


agent.telemetry = _C147_REPORT
agent = globals().pop("agent")
