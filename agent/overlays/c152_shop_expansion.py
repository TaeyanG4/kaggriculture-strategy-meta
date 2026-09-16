# SPDX-License-Identifier: Apache-2.0
"""Expansion-only shop forecast: c146's proven high-demand choices stay exact."""


def _c152_ticks(start, end, interval):
    # Trades occur before town consumption. Forecast consumption before harvest
    # therefore covers current step through the step immediately before harvest.
    return 0 if end <= start else (end - 1) // interval - (start - 1) // interval


def _c152_consumption(shops, item, start, end):
    products = {
        'BAKERY': ('EGG', 'WHEAT'), 'PIZZA_SHOP': ('MILK', 'TOMATO', 'WHEAT'),
        'BRUNCH_SPOT': ('EGG', 'WHEAT', 'STRAWBERRY'), 'YARN_STORE': ('WOOL',),
        'ICE_CREAM_SHOP': ('STRAWBERRY', 'MILK', 'WHEAT'), 'PET_CAFE': ('CARROT',),
        'SMOOTHIE_SHOP': ('STRAWBERRY', 'MILK'),
        'FARMERS_MARKET': ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY'),
    }
    per_tick = sum((2 if len(products[s]) == 1 else 1) for s in shops if item in products[s])
    return per_tick * _c152_ticks(start, end, 4) + _c152_ticks(start, end, 24)


def _c152_low_demand_economics(obs, certificate, state):
    """Price one extra low-demand conversion without suppressing legacy choices."""
    step = int(obs['step']); end = int(certificate['step'])
    shops = obs['town']['unlocked_shops']; market = obs['market']
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for item, patch in market.get('params', {}).items():
        if item in params:
            params[item].update(patch)
    carrot_demand = _c152_consumption(shops, 'CARROT', step, end)
    wheat_demand = _c152_consumption(shops, 'WHEAT', step, end)
    # Keep c146's already-tested supply stress. Do not count current private stock
    # as certain harvest-time supply: the native route may sell it before harvest.
    supply = _c146_public_supply(obs, end // 24) + 32 + 4 * (len(state['plans']) + 1)
    inventory = market['inventory']['CARROT'] + supply - carrot_demand
    value = sum(_r37_market_price('CARROT', inventory + q, params) for q in range(3))
    grain_quote = max(market['prices']['WHEAT'],
                      _r37_market_price('WHEAT', market['inventory']['WHEAT'] - wheat_demand - 12, params)) + 5
    scheduled = int(certificate['scheduled_wheat'])
    risk_units = max(0, int(certificate['foregone_wheat_upper']) - scheduled)
    # Scheduled units are certain. Only 25% of the route upper-bound excess is
    # charged until realized evidence justifies treating all potential yield as lost.
    cost = 20 + (scheduled + 0.25 * risk_units) * grain_quote
    return {'value': value, 'cost': cost, 'carrot_demand': carrot_demand,
            'wheat_demand': wheat_demand, 'supply': supply}
