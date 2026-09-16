# SPDX-License-Identifier: Apache-2.0
"""Defer an unusable partial seed order that would prevent tomorrow's hires.

Research derivative of c129. The official seed batch rule suppresses all same-
crop plants when the available seeds cannot cover the whole turn. Preserve that
already-blocked turn, retain hire cash, and repay the baseline's affordable seed
quantity before the route next uses wheat seeds. No new field commands.
"""
_C139_PARENT = agent
_C139_STATES = {}
_C139_REPORT = {}
del agent


def _c139_wheat_plants(action):
    return sum(c == ['PLANT', 'WHEAT'] for c in
               [action.get('farmer') or ['PASS'], *(action.get('hands') or [])])


def _c139_seed_after_field(obs, action):
    seat = int(obs['player'])
    farm = copy.deepcopy(obs['farms'][seat])
    private = copy.deepcopy(obs['private'])
    commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    demand = {}
    for cmd in commands:
        if len(cmd) >= 2 and cmd[0] == 'PLANT':
            demand[cmd[1]] = demand.get(cmd[1], 0) + 1
    blocked = {k for k, v in demand.items() if private['seeds'].get(k, 0) < v}
    for actor, cmd in enumerate(commands):
        if len(cmd) >= 2 and cmd[0] == 'PLANT' and cmd[1] in blocked:
            cmd = ['PASS']
        _UNIT_NS['_apply_unit_action'](farm, private, actor, cmd, 10,
                                      int(obs['step']) // 24, 24, 100)
    return int(private['seeds'].get('WHEAT', 0))


def _c139_control(obs, action, state):
    step = int(obs['step']); seat = int(obs['player'])
    farm = obs['farms'][seat]
    if state['check_block'] == step:
        count = _c139_wheat_plants(action)
        available = int(obs['private']['seeds'].get('WHEAT', 0))
        if count == state['expected_plants'] and available < count:
            state['blocked_turn_confirmed'] += 1
        else:
            state['contract_errors'] += 1
        state['check_block'] = -1
    if state['repay_check'] == step:
        if obs['private']['seeds'].get('WHEAT', 0) >= state['repay_expected']:
            state['repay_confirmed'] += state['debt']
            state['debt'] = 0
        else:
            state['repay_errors'] += 1
        state['repay_check'] = -1
    if state['events'] and step == 25:
        actual = int(farm['hires_today'])
        state['nextday_hires'] = actual
        if actual < state['expected_hires']:
            state['hire_shortfalls'] += state['expected_hires'] - actual
    orders = action.get('market', [])
    if state['debt']:
        if step > 40:
            if not state['overdue_reported']:
                state['repay_errors'] += 1
                state['overdue_reported'] = 1
            return action
        if (26 <= step <= 40 and state['repay_check'] < 0 and len(orders) < 10
                and all(o and o[0] == 'SELL' for o in orders)
                and farm['money'] >= 10 * state['debt'] + 20
                and _c139_wheat_plants(action) == 0):
            result = copy.deepcopy(action)
            result.setdefault('market', []).append(['BUY_SEED', 'WHEAT', state['debt']])
            state['repay_check'] = step + 1
            state['repay_expected'] = _c139_seed_after_field(obs, action) + state['debt']
            state['repay_requests'] += state['debt']
            return result
        return action
    if state['events'] or not 16 <= step <= 21 or len(orders) != 1:
        return action
    order = orders[0]
    if len(order) != 3 or order[:2] != ['BUY_SEED', 'WHEAT']:
        return action
    quantity = max(0, int(order[2]))
    affordable = min(quantity, int(farm['money']) // 10)
    if not 0 < affordable < quantity:
        return action
    route = _IMPL.chassis.players[seat]['route']
    tape = _ROUTES[route]
    hires = tape[24].get('market', [])
    if not hires or not all(o == ['HIRE'] for o in hires):
        return action
    required = 0; a, b = 1, 1
    for _ in hires:
        required += a
        a, b = b, a + b
    if not farm['money'] - 10 * affordable < required <= farm['money']:
        return action
    next_count = _c139_wheat_plants(tape[step + 1])
    seeds = _c139_seed_after_field(obs, action)
    if next_count <= seeds + affordable:
        return action
    # Require no seed consumption until the bounded repayment window has ended.
    if any(_c139_wheat_plants(tape[t]) for t in range(step + 2, 42)):
        return action
    result = copy.deepcopy(action)
    result['market'] = []
    state['events'] = 1
    state['debt'] = affordable
    state['cash_retained'] = 10 * affordable
    state['check_block'] = step + 1
    state['expected_plants'] = next_count
    state['expected_hires'] = len(hires)
    return result


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    state = _C139_STATES.get(seat)
    if state is None or step <= state['last']:
        state = _C139_STATES[seat] = dict(last=-1, events=0, debt=0,
            cash_retained=0, check_block=-1, expected_plants=0, blocked_turn_confirmed=0,
            expected_hires=0, nextday_hires=0, hire_shortfalls=0,
            repay_check=-1, repay_expected=0, repay_requests=0, repay_confirmed=0,
            overdue_reported=0, contract_errors=0, repay_errors=0, errors=0)
    state['last'] = step
    parent = _C139_PARENT(observation, configuration)
    result = parent
    try:
        supported = configuration is None or all(configuration.get(k, v) == v for k, v in
            [('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100),
             ('farmHandCostMult', 1), ('maxMarketOrdersPerTurn', 10)])
        if supported:
            result = _c139_control(observation, parent, state)
    except Exception:
        state['errors'] += 1
    _C139_REPORT.clear()
    _C139_REPORT.update(getattr(_C139_PARENT, 'telemetry', {}))
    for key in ('events', 'debt', 'cash_retained', 'blocked_turn_confirmed',
                'expected_hires', 'nextday_hires', 'hire_shortfalls', 'repay_requests',
                'repay_confirmed', 'contract_errors', 'repay_errors', 'errors'):
        _C139_REPORT['seed_commitment_' + key] = state[key]
    return result


agent.telemetry = _C139_REPORT
agent = globals().pop('agent')
