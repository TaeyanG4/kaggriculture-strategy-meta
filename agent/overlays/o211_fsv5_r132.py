# o211_fsv5_r132 (Claude/o-series, 2026-09-15). lynnsakurai Farming Score V5 block ported verbatim onto the o199c stack: r132 same-day weed recovery + confirmed-mirror sale reorder (bounded pair swaps, gain>=25, similarity>=0.9, cash lead<=500)
# Source lines 2954-3253; upstream notices retained.



# EXP-260: replay-supported conservative guards.
#
# 1. A PLANT blocked by a same-day weed may be recovered when the original
#    per-worker tape contains an immediate WATER and a later PASS before dawn.
#    The inserted PLANT delays that worker's commands by one position; the PASS
#    absorbs the delay, so the worker is synchronized again within the same day.
# 2. At the end of a 72-turn block, an already-confirmed mirror race may reorder
#    an all-SELL queue.  Quantities and field actions are immutable.  A bounded
#    pair-swap search accepts only a positive gain under the exact public price
#    curve and the conservative hypothesis that the rival has the same queue and
#    saleable stock.  This layer never changes buys, hires, land or input stock.

_R132_PARENT = agent
_R132_STATES = {}
_R132_REPORT = {}


def _r132_commands(action):
    return [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]


def _r132_set_command(action, actor, command):
    result = copy.deepcopy(action)
    if actor == 0:
        result['farmer'] = list(command)
    else:
        hands = list(result.get('hands') or [])
        if actor - 1 >= len(hands):
            return action
        hands[actor - 1] = list(command)
        result['hands'] = hands
    return result


def _r132_standard(configuration):
    return configuration is None or all(
        configuration.get(key, value) == value
        for key, value in (
            ('boardSize', 10),
            ('turnsPerDay', 24),
            ('shedCapacity', 100),
            ('maxMarketOrdersPerTurn', 10),
            ('farmHandCostMult', 1),
        )
    )


def _r132_command_valid(observation, action, actor, command):
    view = FarmView(observation)
    if actor >= len(view.positions):
        return False
    position = view.positions[actor]
    tile = _tile_at(view.tiles, position)
    if _is_noop(command, tile, view.inv(actor), view.seeds, position, view.board):
        return False
    if command and command[0] == 'PLANT':
        crop = command[1]
        demand = sum(
            1 for current in _r132_commands(action)
            if current[:2] == ['PLANT', crop]
        )
        # Include the replacement if the parent's command was not this plant.
        parent = _r132_commands(action)[actor]
        demand += int(parent[:2] != ['PLANT', crop])
        if demand > int(view.seeds.get(crop, 0)):
            return False
    return True


def _r132_start_repair(observation, action, state):
    step = int(observation['step'])
    if step % 24 > 20 or state.get('repair'):
        return
    player = int(observation['player'])
    native = _IMPL.chassis.players.get(player)
    if not native or native.get('route') not in _IMPL.chassis.routes:
        return
    tape = _IMPL.chassis.routes[native['route']]
    if step + 2 >= len(tape):
        return
    raw = _r132_commands(tape[step])
    actual = _r132_commands(action)
    farm = observation['farms'][player]
    positions = [farm['farmer'], *farm['hands']]
    private = observation['private']
    day_end = min(len(tape), (step // 24 + 1) * 24)
    for actor, intended in enumerate(raw[:len(positions)]):
        if intended[:1] != ['PLANT'] or actor >= len(actual) or actual[actor] != ['DIG']:
            continue
        x, y = positions[actor]
        tile = farm['tiles'][y][x]
        crop = intended[1]
        if not (isinstance(tile, dict) and tile.get('kind') == 'WEED'):
            continue
        same_crop = sum(1 for command in raw if command[:2] == ['PLANT', crop])
        if int(private['seeds'].get(crop, 0)) < same_crop:
            continue
        next_commands = _r132_commands(tape[step + 1])
        if actor >= len(next_commands) or next_commands[actor] != ['WATER']:
            continue
        deadline = None
        for future_step in range(step + 1, day_end):
            future = _r132_commands(tape[future_step])
            command = future[actor] if actor < len(future) else ['PASS']
            if command == ['PASS']:
                deadline = future_step
                break
        if deadline is None:
            continue
        state['repair'] = {
            'actor': actor,
            'queue': [list(intended)],
            'next_step': step + 1,
            'deadline': deadline,
            'route': native['route'],
        }
        _R132_REPORT['weed_repair_started'] += 1
        return


def _r132_continue_repair(observation, action, state):
    repair = state.get('repair')
    if not repair:
        return action
    step = int(observation['step'])
    player = int(observation['player'])
    native = _IMPL.chassis.players.get(player) or {}
    if (step != repair['next_step'] or step > repair['deadline'] or
            native.get('route') != repair['route']):
        state.pop('repair', None)
        _R132_REPORT['weed_repair_aborted'] += 1
        return action
    actor = repair['actor']
    commands = _r132_commands(action)
    if actor >= len(commands) or not repair['queue']:
        state.pop('repair', None)
        _R132_REPORT['weed_repair_aborted'] += 1
        return action
    command = repair['queue'].pop(0)
    if not _r132_command_valid(observation, action, actor, command):
        state.pop('repair', None)
        _R132_REPORT['weed_repair_aborted'] += 1
        return action
    displaced = commands[actor]
    if displaced != ['PASS']:
        repair['queue'].append(list(displaced))
    if step >= repair['deadline'] and repair['queue']:
        state.pop('repair', None)
        _R132_REPORT['weed_repair_aborted'] += 1
        return action
    result = _r132_set_command(action, actor, command)
    repair['next_step'] = step + 1
    _R132_REPORT['weed_repair_shifted_steps'] += 1
    if command[:1] == ['PLANT']:
        _R132_REPORT['weed_repair_plants'] += 1
    if command == ['WATER']:
        _R132_REPORT['weed_repair_waters'] += 1
    if not repair['queue']:
        state.pop('repair', None)
        _R132_REPORT['weed_repair_completed'] += 1
    return result


def _r132_price_params(observation):
    params = {item: dict(values) for item, values in _R37_MARKET_PARAMS.items()}
    for item, patch in observation['market'].get('params', {}).items():
        if item in params:
            params[item].update(patch)
    return params


def _r132_mirror_revenue(observation, own_orders, rival_orders, stock):
    inventory = dict(observation['market']['inventory'])
    params = _r132_price_params(observation)
    stocks = [dict(stock), dict(stock)]
    revenue = 0
    for index in range(max(len(own_orders), len(rival_orders))):
        pair = []
        for side, orders in enumerate((own_orders, rival_orders)):
            if index >= len(orders):
                pair.append(None)
                continue
            order = orders[index]
            if not order or len(order) < 3 or order[0] != 'SELL':
                pair.append(None)
                continue
            item = order[1]
            quantity = min(
                max(0, int(order[2])),
                max(0, int(stocks[side].get(item, 0))),
            )
            pair.append([item, quantity])
        while any(current is not None and current[1] > 0 for current in pair):
            sold = []
            for side, current in enumerate(pair):
                if current is None or current[1] <= 0:
                    continue
                item = current[0]
                quote = _r37_market_price(item, inventory[item], params)
                if side == 0:
                    revenue += quote
                current[1] -= 1
                stocks[side][item] = max(0, stocks[side].get(item, 0) - 1)
                sold.append((item, quote))
            for item, quote in sold:
                if quote > 1:
                    inventory[item] += 1
    return revenue


def _r132_mirror_reorder(observation, action):
    step = int(observation['step'])
    player = int(observation['player'])
    rival = 1 - player
    orders = action.get('market') or []
    probe = _R44_PROBES.get(player) or {}
    if not (336 <= step < 696 and step % 72 == 71 and probe.get('matched')):
        return action
    if observation['farms'][player]['money'] > observation['farms'][rival]['money'] + 500:
        return action
    if _r37_similarity(observation) < 0.90 or len(orders) < 2:
        return action
    if any(
        not order or len(order) < 3 or order[0] != 'SELL' or
        order[1] not in PRODUCTS or type(order[2]) is not int or order[2] < 0
        for order in orders
    ):
        return action
    stock = projected_shed(action, FarmView(observation))
    if not any(min(order[2], max(0, int(stock.get(order[1], 0)))) > 0 for order in orders):
        return action
    rival_orders = copy.deepcopy(orders)
    current = copy.deepcopy(orders)
    baseline = _r132_mirror_revenue(observation, current, rival_orders, stock)
    score = baseline
    # At most ten orders: bounded deterministic pair-swap ascent is inexpensive.
    for _ in range(10):
        best_score = score
        best_orders = None
        for left in range(len(current)):
            for right in range(left + 1, len(current)):
                if current[left] == current[right]:
                    continue
                trial = copy.deepcopy(current)
                trial[left], trial[right] = trial[right], trial[left]
                trial_score = _r132_mirror_revenue(
                    observation, trial, rival_orders, stock
                )
                if trial_score > best_score:
                    best_score, best_orders = trial_score, trial
        if best_orders is None:
            break
        current, score = best_orders, best_score
    gain = score - baseline
    if gain < 25 or current == orders:
        return action
    _R132_REPORT['mirror_reorders'] += 1
    _R132_REPORT['mirror_modeled_gain'] += gain
    result = copy.deepcopy(action)
    result['market'] = current
    return result


def agent(observation, configuration=None):
    result = _R132_PARENT(observation, configuration)
    try:
        player = int(observation['player'])
        step = int(observation.get('step', observation['day'] * 24 + observation['hour']))
        state = _R132_STATES.get(player)
        if state is None or step <= state['step']:
            state = _R132_STATES[player] = {'step': -1}
            _R132_REPORT.update(
                weed_repair_started=0,
                weed_repair_shifted_steps=0,
                weed_repair_plants=0,
                weed_repair_waters=0,
                weed_repair_completed=0,
                weed_repair_aborted=0,
                mirror_reorders=0,
                mirror_modeled_gain=0,
                replay_guard_errors=0,
            )
        state['step'] = step
        if not _r132_standard(configuration):
            return result
        if state.get('repair'):
            result = _r132_continue_repair(observation, result, state)
        else:
            _r132_start_repair(observation, result, state)
        result = _r132_mirror_reorder(observation, result)
    except Exception:
        _R132_REPORT['replay_guard_errors'] = _R132_REPORT.get('replay_guard_errors', 0) + 1
    _R132_REPORT.update(getattr(_R132_PARENT, 'telemetry', {}))
    return result


agent.telemetry = _R132_REPORT
agent = globals().pop('agent')
