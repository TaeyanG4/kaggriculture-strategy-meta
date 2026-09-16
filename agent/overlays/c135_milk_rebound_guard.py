# SPDX-License-Identifier: Apache-2.0
"""c132 hypothesis with a conservative public milk-demand rebound guard.

Apply to immutable c129. Four days of already-open shop demand plus a reserve
for cumulative foregone care are priced without crediting speculative supply.
This is a stress scenario, not a known future price or opponent-profit bound.
"""
_C135_PARENT = agent
_C135_STATES = {}
_C135_REPORT = {}
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    state = _C135_STATES.get(seat)
    if state is None or step <= state['last']:
        state = _C135_STATES[seat] = {'last': -1, 'prices': [], 'skips': 0, 'blocked': 0, 'errors': 0}
    state['last'] = step
    prices = observation['market']['prices']
    state['prices'].append((step, prices['MILK']))
    state['prices'] = [row for row in state['prices'] if row[0] >= step - 23]
    parent = _C135_PARENT(observation, configuration); result = parent
    try:
        supported = configuration is None or all(configuration.get(k, v) == v for k, v in (
            ('boardSize', 10), ('turnsPerDay', 24), ('townShopSellInterval', 4), ('townCenterSellInterval', 24)))
        if supported and 336 <= step < 672 and len(state['prices']) == 24:
            recent = max(p for _, p in state['prices'])
            if 20 * recent < 8 * prices['WHEAT']:
                farm = observation['farms'][seat]
                positions = [farm['farmer'], *farm['hands']]
                commands = [parent.get('farmer') or ['PASS'], *(parent.get('hands') or [])]
                shops = observation['town']['unlocked_shops']
                daily_demand = 1 + 6 * sum(shops.count(shop) for shop in ('PIZZA_SHOP', 'SMOOTHIE_SHOP', 'ICE_CREAM_SHOP'))
                for actor, (pos, cmd) in enumerate(zip(positions, commands)):
                    if cmd != ['FEED'] or observation['private']['inventories'][actor].get('WHEAT', 0) < 1:
                        continue
                    x, y = pos; tile = farm['tiles'][y][x]
                    if not isinstance(tile, dict) or tile.get('animal') != 'COW' or tile.get('fed_today') or tile.get('consecutive_unfed', 0) != 0:
                        continue
                    age = step // 24 + 1 - tile['placed_day'] - 8
                    if age < 0 or age % 2 == 0:
                        continue
                    stress_inventory = observation['market']['inventory']['MILK'] - 4 * daily_demand - 2 * (state['skips'] + 1)
                    rebound = max(recent, _r37_market_price('MILK', stress_inventory))
                    if 20 * rebound >= 8 * prices['WHEAT']:
                        state['blocked'] += 1
                        continue
                    if result is parent: result = copy.deepcopy(parent)
                    if actor == 0: result['farmer'] = ['PASS']
                    else: result['hands'][actor - 1] = ['PASS']
                    state['skips'] += 1
    except Exception:
        state['errors'] += 1
        result = parent
    _C135_REPORT.clear(); _C135_REPORT.update(getattr(_C135_PARENT, 'telemetry', {}))
    _C135_REPORT.update({'milk_rebound_' + k: state[k] for k in ('skips', 'blocked', 'errors')})
    return result


agent.telemetry = _C135_REPORT
agent = globals().pop('agent')
