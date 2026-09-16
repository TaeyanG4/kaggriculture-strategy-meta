
# SPDX-License-Identifier: Apache-2.0
# Unqualified research derivative: isolate opening purchase quantity/order slots.
# All subsequent decisions and all field commands are inherited unchanged.
_C140_PARENT = agent
_C140_REPORT = {}
_C140_COUNTS = {}
del agent

def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    if step == 0:
        _C140_COUNTS.clear()
        _C140_COUNTS.update(opening_queue_events=0, opening_queue_parent_mismatch_errors=0,
            opening_queue_errors=0, opening_queue_buy_quantity=0, opening_queue_order_count=0)
    result = _C140_PARENT(observation, configuration)
    try:
        if step in (1, 2, 24, 25):
            # Current observable diagnostics only; these never choose an action.
            prefix = 'opening_queue_at' + str(step) + '_'
            _C140_COUNTS[prefix + 'own_cash'] = observation['farms'][seat]['money']
            _C140_COUNTS[prefix + 'rival_cash'] = observation['farms'][1-seat]['money']
            _C140_COUNTS[prefix + 'own_shed_wheat'] = observation['private']['shed'].get('WHEAT', 0)
            _C140_COUNTS[prefix + 'own_seed_wheat'] = observation['private']['seeds'].get('WHEAT', 0)
            _C140_COUNTS[prefix + 'own_hands'] = len(observation['farms'][seat]['hands'])
            _C140_COUNTS[prefix + 'market_wheat'] = observation['market']['inventory']['WHEAT']
        supported = configuration is None or all(configuration.get(k, v) == v for k, v in
            [('boardSize', 10), ('turnsPerDay', 24), ('maxMarketOrdersPerTurn', 10)])
        if step == 0 and supported:
            if result.get('market') != [['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 10], ['SELL', 'WHEAT', 30]]:
                _C140_COUNTS['opening_queue_parent_mismatch_errors'] += 1
            else:
                result = copy.deepcopy(result)
                result['market'] = [['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 3], ['SELL', 'WHEAT', 30]]
                _C140_COUNTS['opening_queue_events'] = 1
                _C140_COUNTS['opening_queue_buy_quantity'] = 16
                _C140_COUNTS['opening_queue_order_count'] = 3
    except Exception:
        _C140_COUNTS['opening_queue_errors'] += 1
    _C140_REPORT.clear()
    _C140_REPORT.update(getattr(_C140_PARENT, 'telemetry', {}))
    _C140_REPORT.update(_C140_COUNTS)
    return result

agent.telemetry = _C140_REPORT
agent = globals().pop('agent')
