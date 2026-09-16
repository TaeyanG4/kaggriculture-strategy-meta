# o225_demand_feed_guard (Claude/o-series, 2026-09-16). Demand-aware livestock feed guard for the o219 stack.
# The o159 feed-value model prices a feed with the SPOT product price, which our own dumping depresses; when several
# shops consume the product (milk: PIZZA/ICE_CREAM/SMOOTHIE, eggs: BAKERY/BRUNCH) inventory drains 1 unit per shop per
# 4 steps and the price recovers, so abandoning cows/geese late (d24+ escapes) forfeits paid-for production
# (seed 7032 vs V43: 17->11 animals at d27, -5.8k). Rule: never skip a COW feed while >=2 milk shops are unlocked,
# never skip a GOOSE feed while >=2 egg shops are unlocked (day-29 feeds stay worthless via the parent model).
# Same hook as o206 (wraps _o159_value). Telemetry: o225_milk_shops, o225_egg_shops.
_O225_PARENT = agent
_O225_STATE = {'milk': 0, 'egg': 0}
_O225_REPORT = {}
_o225_orig_value = _o159_value
_O225_MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
_O225_EGG = ('BAKERY', 'BRUNCH_SPOT')
del agent


def _o159_value(tile, kind, day, prices):
    v, a = _o225_orig_value(tile, kind, day, prices)
    if day <= 28 and ((kind == 'COW' and _O225_STATE['milk'] >= 2) or (kind == 'GOOSE' and _O225_STATE['egg'] >= 2)):
        return 1e9, a
    return v, a


def agent(observation, configuration=None):
    shops = observation.get('town', {}).get('unlocked_shops', []) or []
    _O225_STATE['milk'] = sum(s in _O225_MILK for s in shops)
    _O225_STATE['egg'] = sum(s in _O225_EGG for s in shops)
    result = _O225_PARENT(observation, configuration)
    _O225_REPORT.clear()
    _O225_REPORT.update(getattr(_O225_PARENT, 'telemetry', {}))
    _O225_REPORT['o225_milk_shops'] = _O225_STATE['milk']
    _O225_REPORT['o225_egg_shops'] = _O225_STATE['egg']
    return result


agent.telemetry = _O225_REPORT
agent = globals().pop('agent')
