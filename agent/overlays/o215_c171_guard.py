# o215_c171_guard (Claude/o-series, 2026-09-15). Overlay for c171: drop the V42 routes for shop pairs where
# the world bank shows V42 losing to the legacy o182 route (n>=8 & wins>=base & worst>-8000 required to keep).
# Kept pairs: 27, dropped pairs: 16.
_O215_DROP = [["FARMERS_MARKET", "FARMERS_MARKET"], ["PET_CAFE", "FARMERS_MARKET"], ["PET_CAFE", "BRUNCH_SPOT"], ["SMOOTHIE_SHOP", "PIZZA_SHOP"], ["PIZZA_SHOP", "ICE_CREAM_SHOP"], ["BAKERY", "PET_CAFE"], ["PIZZA_SHOP", "SMOOTHIE_SHOP"], ["PIZZA_SHOP", "PIZZA_SHOP"], ["BAKERY", "FARMERS_MARKET"], ["PET_CAFE", "BAKERY"], ["BAKERY", "BAKERY"], ["FARMERS_MARKET", "BAKERY"], ["BRUNCH_SPOT", "BRUNCH_SPOT"], ["BRUNCH_SPOT", "PET_CAFE"], ["ICE_CREAM_SHOP", "PIZZA_SHOP"], ["SMOOTHIE_SHOP", "BRUNCH_SPOT"]]
for _p in _O215_DROP:
    _C171_ROUTE_MAP.pop(tuple(_p), None)
agent = globals().pop('agent')
