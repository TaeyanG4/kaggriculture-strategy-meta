# o234_carrot_demand2 (Claude/o-series, 2026-09-16): re-enable the o199c demand rule — switch the wheat cycle to CARROT while >= 2 carrot shops (PET_CAFE/FARMERS_MARKET) are unlocked (single-product PET_CAFE consumes 2 units per tick; carrot T=450). Frozen-Majkel losses cluster in PET-heavy worlds (-13k..-22k) and the price-only switch fires 0/1344 in the pool.
_O199_DEMAND = 2
agent = globals().pop("agent")
