# o171d_day6_goose_all4 (shop_rule=False, four=True) (Claude/o-series, 2026-09-15). Overlay on o162.
"""Day-6 COW pair -> GOOSE pair when the first two shops show no milk demand (route 0/2 only).
Leader's first divergence from our lineage (r000 report): COW->GOOSE on day 6 in bakery/brunch/pet
worlds. Route 0 buys 2 COW at step 150 and places them on (5,4)/(5,3) via a fixed worker schedule;
this rewrites exactly that block (buy, 2 pickups, 2 pasture builds -> coops, 2 places) after a
signature check at step 150. Each later step is rewritten only if the parent command and worker
position match the expected schedule (otherwise counted in o171_mismatch and left untouched).
Variant flag _O171_NEED_EGG_SHOP: also require BAKERY/BRUNCH among the first two shops.
Telemetry: o171_mode, o171_rewrites, o171_mismatch, o171_errors.
"""
import copy as _o171_copy

_O171_PARENT = agent
_O171_STATE = {}
_O171_REPORT = {}
_O171_NEED_EGG_SHOP = False
_O171_SHOP_RULE = False      # False: substitute in every route-0 world
_O171_FOUR = True          # True: also the day-7 cows (steps 169/176) -> geese
_O171_MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
_O171_EGG = ('BAKERY', 'BRUNCH_SPOT')
# step -> list of (worker index, expected parent command, expected worker position or None, new command)
_O171_SCHEDULE = {
    151: [(7, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    152: [(1, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    153: [(1, ['BUILD_PASTURE'], (5, 4), ['BUILD_COOP'])],
    155: [(7, ['BUILD_PASTURE'], (5, 3), ['BUILD_COOP']), (1, ['PLACE', 'COW'], (5, 4), ['PLACE', 'GOOSE'])],
    156: [(7, ['PLACE', 'COW'], (5, 3), ['PLACE', 'GOOSE'])],
}
_O171_SCHEDULE4 = {
    153: [(6, ['BUILD_PASTURE'], (5, 2), ['BUILD_COOP'])],
    159: [(1, ['BUILD_PASTURE'], (6, 4), ['BUILD_COOP'])],
    170: [(3, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    177: [(3, ['PLACE', 'COW'], (6, 4), ['PLACE', 'GOOSE']), (5, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    179: [(6, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    182: [(6, ['PLACE', 'COW'], (5, 2), ['PLACE', 'GOOSE'])],
}
_O171_BUY4 = (169, 176)
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O171_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O171_STATE[seat] = {'last': -1, 'mode': '', 'rewrites': 0, 'mismatch': 0, 'errors': 0}
    st['last'] = step
    parent_action = _O171_PARENT(observation, configuration)
    result = parent_action
    try:
        if step == 150:
            shops = list(observation['town'].get('unlocked_shops', []))[:2]
            orders = parent_action.get('market') or []
            sig = (['BUY_ANIMAL', 'COW', 2] in orders and 'YARN_STORE' not in shops
                   and (not _O171_SHOP_RULE or not any(s in _O171_MILK for s in shops))
                   and (not _O171_NEED_EGG_SHOP or any(s in _O171_EGG for s in shops)))
            if sig:
                st['mode'] = 'GOOSE'
                result = _o171_copy.deepcopy(parent_action)
                for o in result['market']:
                    if o == ['BUY_ANIMAL', 'COW', 2]:
                        o[1] = 'GOOSE'; st['rewrites'] += 1
        elif st['mode'] and _O171_FOUR and step in _O171_BUY4 and ['BUY_ANIMAL', 'COW', 1] in (parent_action.get('market') or []):
            result = _o171_copy.deepcopy(parent_action)
            for o in result['market']:
                if o == ['BUY_ANIMAL', 'COW', 1]:
                    o[1] = 'GOOSE'; st['rewrites'] += 1
        elif st['mode'] and (step in _O171_SCHEDULE or (_O171_FOUR and step in _O171_SCHEDULE4)):
            farm = observation['farms'][seat]
            positions = [farm['farmer'], *farm['hands']]
            cmds = [parent_action.get('farmer')] + list(parent_action.get('hands') or [])
            out = None
            plan = list(_O171_SCHEDULE.get(step, [])) + (list(_O171_SCHEDULE4.get(step, [])) if _O171_FOUR else [])
            for idx, expect, pos, new in plan:
                ok = idx < len(cmds) and cmds[idx] == expect and (pos is None or (idx < len(positions) and tuple(positions[idx]) == pos))
                if not ok:
                    st['mismatch'] += 1
                    continue
                if out is None:
                    out = _o171_copy.deepcopy(parent_action)
                if idx == 0:
                    out['farmer'] = list(new)
                else:
                    out['hands'][idx - 1] = list(new)
                st['rewrites'] += 1
            if out is not None:
                result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O171_REPORT.clear()
    _O171_REPORT.update(getattr(_O171_PARENT, 'telemetry', {}))
    _O171_REPORT.update({'o171_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O171_REPORT
agent = globals().pop('agent')
