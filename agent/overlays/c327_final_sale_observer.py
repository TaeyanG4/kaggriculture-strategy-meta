# c327: observe final own sale quantities and abstain on floor-censored markets.
# Keeps the original v9 production, prices, forecast library and selling rules.
_C327_PARENT = agent
_C327_ON = True
_C327_ITEMS = ('MILK', 'WOOL', 'STRAWBERRY')
_C327_REPORT = dict(final_own_corrections=0, floor_censored=0, projections=0, errors=0)
del agent

def agent(observation, configuration=None):
    step = int(observation['step']); seat = int(observation['player'])
    if step == 0:
        _C327_REPORT.update(final_own_corrections=0, floor_censored=0, projections=0, errors=0)
    if not _C327_ON:
        return _C327_PARENT(observation, configuration)
    previous = (_V9_RACE.get(seat) or {}).get('prev')
    if previous and previous['step'] == step - 1:
        try:
            draw = _v9_town_draw(previous['shops'], previous['step'])
            for item in _C327_ITEMS:
                before_draw = observation['market']['inventory'][item] + draw.get(item, 0)
                if _r37_market_price(item, before_draw, observation['market'].get('params')) <= 1:
                    previous['prices'][item] = 1
                    _C327_REPORT['floor_censored'] += 1
        except Exception:
            _C327_REPORT['errors'] += 1
    action = _C327_PARENT(observation, configuration)
    try:
        previous = (_V9_RACE.get(seat) or {}).get('prev')
        if previous and previous['step'] == step:
            _, private = _ov_fields(observation, action)
            orders = action.get('market') or []
            stock, _, sales = _r97_market_stock(private['shed'], orders)
            own = {item: 0 for item in _C327_ITEMS}
            for index, quantity in sales.items():
                item = orders[index][1]
                if item in own:
                    own[item] += quantity
            for item in _C327_ITEMS:
                _C327_REPORT['final_own_corrections'] += int(previous['own'].get(item, 0) != own[item])
                previous['own'][item] = own[item]
                previous['left'][item] = max(0, int(stock.get(item, 0)))
                if any(len(o) >= 2 and o[:2] == ['BUY_PRODUCT', item] for o in orders):
                    previous['prices'][item] = 1
            _C327_REPORT['projections'] += 1
    except Exception:
        _C327_REPORT['errors'] += 1
    return action

agent.telemetry = _C327_REPORT
agent = globals().pop('agent')
