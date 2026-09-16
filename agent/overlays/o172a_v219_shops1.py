# o172a_v219_shops1 (Claude/o-series, 2026-09-15). Overlay on o162.
# Widens the V219 day-18 tomato program from "3+ tomato shops" to "_O172_MIN_SHOPS+" (leader plants
# tomato speculatively; hinge demand is the untapped lever). Everything else in V219 unchanged.
_O172_MIN_SHOPS = 1
_o172_orig_qualifies = _v219_qualifies


def _v219_qualifies(obs, native):
    shops = obs['town']['unlocked_shops']
    n = sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET') for s in shops)
    if n >= 3:
        return _o172_orig_qualifies(obs, native)
    if n < _O172_MIN_SHOPS:
        return False
    # re-run the original with the shop test satisfied by a padded view of the town
    padded = dict(obs)
    padded['town'] = dict(obs['town'], unlocked_shops=list(shops) + ['PIZZA_SHOP'] * (3 - n))
    return _o172_orig_qualifies(padded, native)

agent = globals().pop('agent')   # keep 'agent' the last callable for Kaggle's loader
