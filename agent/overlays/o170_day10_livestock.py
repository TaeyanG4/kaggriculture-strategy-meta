# o170_day10_livestock (Claude/o-series, 2026-09-15). Overlay on o162.
"""Day-10 livestock substitution from observed shops (route 0/2 only).
The parent tape buys 3 GOOSE at steps 241/265 regardless of demand. At step 241 the three
known shops decide a replacement species for that whole purchase block:
  SHEEP if a YARN_STORE is among the 3 shops (route 0 means none in the first two);
  COW   if no egg shop (BAKERY/BRUNCH) and >=_O170_MILK_MIN milk shops;
  else keep GOOSE.
Whole block is substituted (buys, pickups, places, coop builds -> pasture) or nothing; the
day-10 purchase must fit in cash (2*cost + _O170_CASH_MARGIN) or the block is left as is.
Telemetry: o170_mode ('' / SHEEP / COW), o170_rewrites, o170_cash_declines, o170_errors.
"""
import copy as _o170_copy

_O170_PARENT = agent
_O170_STATE = {}
_O170_REPORT = {}
_O170_WINDOW = (241, 300)
_O170_MILK_MIN = 2
_O170_COW_NEEDS_NO_EGG = True
_O170_CASH_MARGIN = 350
_O170_COST = {'SHEEP': 500, 'COW': 400}
_O170_MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
_O170_EGG = ('BAKERY', 'BRUNCH_SPOT')
del agent


def _o170_choose(shops):
    if 'YARN_STORE' in shops:
        return 'SHEEP'
    milk = sum(s in _O170_MILK for s in shops)
    egg = sum(s in _O170_EGG for s in shops)
    if milk >= _O170_MILK_MIN and (egg == 0 or not _O170_COW_NEEDS_NO_EGG):
        return 'COW'
    return ''


def _o170_rewrite(action, target, st):
    out = _o170_copy.deepcopy(action)
    n = 0
    for o in out.get('market') or []:
        if o and o[0] == 'BUY_ANIMAL' and o[1] == 'GOOSE':
            o[1] = target; n += 1
    cmds = [out.get('farmer')] + list(out.get('hands') or [])
    for i, c in enumerate(cmds):
        if not c:
            continue
        new = None
        if c[0] in ('PICKUP', 'PLACE') and len(c) >= 2 and c[1] == 'GOOSE':
            new = [c[0], target] + list(c[2:])
        elif c[0] == 'BUILD_COOP':
            new = ['BUILD_PASTURE']
        if new is not None:
            n += 1
            if i == 0:
                out['farmer'] = new
            else:
                out['hands'][i - 1] = new
    st['rewrites'] += n
    return out if n else action


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O170_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O170_STATE[seat] = {'last': -1, 'mode': '', 'rewrites': 0, 'cash_declines': 0, 'errors': 0}
    st['last'] = step
    parent_action = _O170_PARENT(observation, configuration)
    result = parent_action
    try:
        if step == _O170_WINDOW[0]:
            orders = parent_action.get('market') or []
            goose = [o for o in orders if o and o[0] == 'BUY_ANIMAL' and o[1] == 'GOOSE']
            if goose:  # route 0/2 signature: the day-10 goose purchase is present
                shops = list(observation['town'].get('unlocked_shops', []))
                target = _o170_choose(shops)
                if target:
                    need = sum(int(o[2]) for o in goose) * _O170_COST[target] + _O170_CASH_MARGIN
                    if observation['farms'][seat]['money'] >= need:
                        st['mode'] = target
                    else:
                        st['cash_declines'] += 1
        if st['mode'] and _O170_WINDOW[0] <= step < _O170_WINDOW[1]:
            result = _o170_rewrite(parent_action, st['mode'], st)
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O170_REPORT.clear()
    _O170_REPORT.update(getattr(_O170_PARENT, 'telemetry', {}))
    _O170_REPORT.update({'o170_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O170_REPORT
agent = globals().pop('agent')
