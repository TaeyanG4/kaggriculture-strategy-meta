# SPDX-License-Identifier: Apache-2.0
"""Public shop-demand scenarios for c151. Supply is a scenario, not known sales."""
_C151_SHOPS = {
    'BAKERY': ('EGG', 'WHEAT'),
    'PIZZA_SHOP': ('MILK', 'TOMATO', 'WHEAT'),
    'BRUNCH_SPOT': ('EGG', 'WHEAT', 'STRAWBERRY'),
    'YARN_STORE': ('WOOL',),
    'ICE_CREAM_SHOP': ('STRAWBERRY', 'MILK', 'WHEAT'),
    'PET_CAFE': ('CARROT',),
    'SMOOTHIE_SHOP': ('STRAWBERRY', 'MILK'),
    'FARMERS_MARKET': ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY'),
}


def _c151_ticks(start, end, interval):
    # Current action trades BEFORE current-step town consumption; harvest trades
    # BEFORE harvest-step consumption. Thus forecast consumption is [start, end).
    return 0 if end <= start else (end - 1) // interval - (start - 1) // interval


def _c151_consumption(shops, item, start, end):
    per_tick = sum((2 if len(_C151_SHOPS[s]) == 1 else 1)
                   for s in shops if item in _C151_SHOPS[s])
    return per_tick * _c151_ticks(start, end, 4) + _c151_ticks(start, end, 24)


def _c151_crop_supply(obs, item, harvest_step, plans):
    """Both visible farms at crop cap; own visible plans counted once.

    Rival stored goods, future planting, sales, watering and feed are unknown.
    A separate 32-unit carrot supply stress accounts for some of that uncertainty.
    This is deliberately conservative for CARROT revenue, not a hard upper bound.
    """
    cap = {'CARROT': 4, 'WHEAT': 6}[item]
    supply = 0
    represented = set()
    for seat, farm in enumerate(obs['farms']):
        for y, row in enumerate(farm['tiles']):
            for x, tile in enumerate(row):
                if (isinstance(tile, dict) and tile.get('crop') == item
                        and int(tile['planted_day']) + 2 <= harvest_step // 24):
                    supply += cap
                    if seat == int(obs['player']):
                        represented.add((x, y, int(tile['planted_day'])))
    if item == 'CARROT':
        for plan in plans:
            key = (*plan['xy'], plan['birth'])
            if plan['step'] <= harvest_step and key not in represented:
                supply += cap
                represented.add(key)
    private = obs['private']
    supply += max(0, private['shed'].get(item, 0))
    supply += sum(max(0, inv.get(item, 0)) for inv in private['inventories'])
    return supply


def _c151_economics(obs, certificate, state):
    step = int(obs['step']); end = int(certificate['step'])
    shops = obs['town']['unlocked_shops']
    market = obs['market']
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for item, patch in market.get('params', {}).items():
        if item in params:
            params[item].update(patch)
    carrot_demand = _c151_consumption(shops, 'CARROT', step, end)
    wheat_demand = _c151_consumption(shops, 'WHEAT', step, end)
    carrot_supply = _c151_crop_supply(obs, 'CARROT', end, state['plans']) + 32
    wheat_supply = _c151_crop_supply(obs, 'WHEAT', end, state['plans'])
    carrot_inventory = market['inventory']['CARROT'] + carrot_supply - carrot_demand
    wheat_inventory = market['inventory']['WHEAT'] + wheat_supply - wheat_demand
    # The native certificate guarantees two productive waters, hence 3 CARROT.
    # Quote a marginal batch, including its own price impact (not 3 * headline).
    value = sum(_r37_market_price('CARROT', carrot_inventory + q, params) for q in range(3))
    # Visible wheat may be fed, stored, or never harvested. Reserve its value in
    # a no-new-sales scarcity scenario as well as the public supply scenario.
    wheat_stress = market['inventory']['WHEAT'] - wheat_demand - 12
    grain_quote = max(market['prices']['WHEAT'],
                      _r37_market_price('WHEAT', wheat_inventory, params),
                      _r37_market_price('WHEAT', wheat_stress, params)) + 5
    cost = 20 + int(certificate['foregone_wheat_upper']) * grain_quote
    return {'value': value, 'cost': cost, 'carrot_demand': carrot_demand,
            'wheat_demand': wheat_demand, 'carrot_supply': carrot_supply,
            'wheat_supply': wheat_supply, 'carrot_inventory': carrot_inventory}
