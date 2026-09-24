# c388, Taeyang/Codex, 2026-09-23. Preserve the parent's purchase quantities.
# Moon251 loss diagnosis: fixed-price seed slots delayed price-sensitive wheat.
# Reorder only pure seed/wheat purchase turns with provable full funding/capacity.
# Existing public engine-price and physical-state helpers retain their notices.
_C388_ENABLED = True
_C388_PARENT = agent
_C388_REPORT = {}
_C388_TELEMETRY = {}


def _c388_priority(obs, action):
    orders = action.get('market') or []
    if not 2 <= len(orders) <= 10:
        return action
    # No sales, land, livestock, hiring, empty slots, or other product purchases
    # may be crossed. Their cash/capacity dependencies are deliberately excluded.
    wheat = []
    for index, order in enumerate(orders):
        if not isinstance(order, list) or len(order) != 3:
            return action
        op, item, quantity = order
        if type(quantity) is not int or quantity <= 0:
            return action
        if op == 'BUY_PRODUCT' and item == 'WHEAT':
            wheat.append(index)
        elif op != 'BUY_SEED' or item not in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON'):
            return action
    if len(wheat) != 1 or wheat[0] == 0:
        return action
    _C388_REPORT['c388_offers'] += 1
    ns = _C365_CA_NS
    # _r97_budget uses standard fixed seed prices and a conservative wheat
    # quote at inventory-2000 (two players, <=10 orders, <=100 units per order).
    # Decline nonstandard wheat curves instead of applying that bound blindly.
    standard = ns['_R37_MARKET_PARAMS']['WHEAT']
    current = dict(standard, **obs['market'].get('params', {}).get('WHEAT', {}))
    if current != standard or not ns['_r97_budget'](obs, orders):
        _C388_REPORT['c388_budget_declines'] += 1
        return action
    _, private = ns['_ov_fields'](obs, action)
    q = orders[wheat[0]][2]
    if q + sum(private['shed'].values()) > 100:
        _C388_REPORT['c388_capacity_declines'] += 1
        return action
    # Field actions precede all market slots; BUY_SEED never consumes shed room.
    # Both queues therefore fill the same seed/wheat quantities, with only the
    # competitive purchase quote and subsequent policy reactions able to differ.
    ordered = [orders[wheat[0]], *orders[:wheat[0]], *orders[wheat[0]+1:]]
    _C388_REPORT['c388_turns'] += 1
    _C388_REPORT['c388_slots_advanced'] += wheat[0]
    return dict(action, market=ordered)


def agent(observation, configuration=None):
    step = int(observation['step'])
    if step == 0:
        _C388_REPORT.clear()
        _C388_REPORT.update(c388_offers=0,c388_budget_declines=0,
                           c388_capacity_declines=0,c388_turns=0,
                           c388_slots_advanced=0,c388_errors=0)
    action = _C388_PARENT(observation, configuration)
    if _C388_ENABLED and step >= 144:
        standard = configuration is None or all(configuration.get(k,v)==v for k,v in
            [('episodeSteps',720),('turnsPerDay',24),('boardSize',10),
             ('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
        if standard:
            try:
                action = _c388_priority(observation, action)
            except Exception:
                _C388_REPORT['c388_errors'] += 1
                raise
    _C388_TELEMETRY.clear()
    _C388_TELEMETRY.update(_C384_REPORT)
    _C388_TELEMETRY.update(_C388_REPORT)
    return action


agent.telemetry = _C388_TELEMETRY
c388_submission_agent = agent
