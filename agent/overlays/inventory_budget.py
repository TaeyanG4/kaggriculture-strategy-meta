# SPDX-License-Identifier: Apache-2.0
# Original project addition, 2026-09-12, appended to Apache-2.0 public V37.
# Existing schedules keep buying inputs even after supplemental crops add stock.
# Reserve the observable own schedule's pickups and sales before reducing a buy.
_C108_PARENT = agent
_C108_REPORT = {}


def _c108_required(obs, item, native):
    step = int(obs['step'])
    required = 0
    stop = 719
    for t in range(step + 1, 719):
        route = 2 if t >= 648 else native['route']
        future = _IMPL.chassis.routes[route][t]
        commands = [future.get('farmer') or ['PASS']] + list(future.get('hands') or [])
        required += sum(max(0, int(c[2]) if len(c) > 2 else 1) for c in commands
                        if len(c) > 1 and c[:2] == ['PICKUP', item])
        # Units act before the market. A next-buy turn's pickup needs old stock.
        stop_here = False
        for order in future.get('market', []):
            if len(order) < 3 or order[1] != item:
                continue
            if order[0] == 'BUY_PRODUCT' and int(order[2]) > 0:
                stop = t
                stop_here = True
                break
            if order[0] == 'SELL':
                required += max(0, int(order[2]))
        if stop_here:
            break
    player = int(obs['player'])
    # Supplemental livestock never appears in native tapes. Reserve a full
    # six-animal feed load for every affected day, even if part was already fed.
    sheep = _V233_STATES.get(player, {})
    if item == 'WHEAT' and (sheep.get('committed') or sheep.get('pending')):
        required += 6 * (stop // 24 - step // 24 + 1)
    if item == 'FERTILIZER':
        crop = _V219_STATES.get(player, {})
        if crop.get('committed') or crop.get('pending'):
            required += 10 * (stop // 24 - step // 24 + 1)
    return required


def _c108_budget(obs, action):
    step = int(obs['step'])
    if not 144 <= step < 696:
        return action
    player = int(obs['player'])
    native = _IMPL.chassis.players[player]
    tape_action = _IMPL.chassis.routes[native['route']][step]
    native_buys = {o[1] for o in tape_action.get('market', [])
                   if len(o) >= 3 and o[0] == 'BUY_PRODUCT' and int(o[2]) > 0}
    eligible = native_buys & {'WHEAT', 'FERTILIZER'}
    if _R51_INPUT_STATES.get(player, {}).get('pending'):
        eligible.discard('FERTILIZER')
    if not eligible:
        return action
    commands = [action.get('farmer') or ['PASS']] + list(action.get('hands') or [])
    if any(len(c) > 1 and c[0] == 'PLACE' and c[1] in ANIMAL_STRUCTURE for c in commands):
        return action
    stock = projected_shed(action, FarmView(obs))
    orders = [list(o) for o in action.get('market', [])]
    needs = {item: _c108_required(obs, item, native) for item in eligible}
    changed = False
    for index, order in enumerate(orders):
        if len(order) < 3:
            continue
        op, item, amount = order[:3]
        amount = max(0, int(amount))
        if op == 'SELL':
            stock[item] = max(0, stock.get(item, 0) - amount)
        elif op == 'BUY_PRODUCT':
            if item in eligible and amount > 0:
                # Preserve later current-turn sells as well as the future tape.
                later_sales = sum(max(0, int(o[2])) for o in orders[index + 1:]
                                  if len(o) >= 3 and o[:2] == ['SELL', item])
                wanted = max(0, needs[item] + later_sales - stock.get(item, 0))
                quantity = min(amount, wanted)
                if quantity < amount:
                    order[2] = quantity  # Keep the original market barrier/slot.
                    _C108_REPORT['budget_avoided_' + item.lower()] += amount - quantity
                    _C108_REPORT['budget_changed_orders'] += 1
                    changed = True
                amount = quantity
            stock[item] = stock.get(item, 0) + amount
    return dict(action, market=orders) if changed else action


def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _C108_REPORT.clear()
        _C108_REPORT.update(budget_avoided_wheat=0, budget_avoided_fertilizer=0,
                            budget_changed_orders=0, inventory_budget_errors=0)
    result = _C108_PARENT(observation, configuration)
    try:
        result = _c108_budget(observation, result)
    except Exception:
        _C108_REPORT['inventory_budget_errors'] += 1
    _C108_REPORT.update(getattr(_C108_PARENT, 'telemetry', {}))
    return result


agent.telemetry = _C108_REPORT
agent = globals().pop('agent')
