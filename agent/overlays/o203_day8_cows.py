# o203_day8_cows (Claude/o-series, 2026-09-15). Overlay for the o199c stack.
"""Day-8 SHEEP pair -> COW pair when both of the first two shops are milk shops (route 0/2 only).
Live losses (o182 -5,230, o178 -6,287): in two-milk worlds the rival bought cows at day 8 and out-earned
us on milk by 4.7-8.5k; o201's EV run showed the same (12 games +2,998). COW uses the same PASTURE, so
only the buy (196) and the pickups/places (197/198 -> 201/213) are renamed. Telemetry o203_mode/rewrites/mismatch/errors.
"""
import copy as _o203_copy

_O203_PARENT = agent
_O203_STATE = {}
_O203_REPORT = {}
_O203_MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
_O203_SCHEDULE = {197: [(5, ['PICKUP', 'SHEEP'], None)], 198: [(6, ['PICKUP', 'SHEEP'], None)],
                  201: [(6, ['PLACE', 'SHEEP'], (7, 4))], 213: [(5, ['PLACE', 'SHEEP'], (6, 3))]}
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O203_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O203_STATE[seat] = {'last': -1, 'mode': '', 'rewrites': 0, 'mismatch': 0, 'errors': 0}
    st['last'] = step
    parent_action = _O203_PARENT(observation, configuration)
    result = parent_action
    try:
        if step == 196:
            shops = list(observation['town'].get('unlocked_shops', []))[:2]
            if len(shops) == 2 and all(s in _O203_MILK for s in shops) and ['BUY_ANIMAL', 'SHEEP', 2] in (parent_action.get('market') or []):
                st['mode'] = 'COW'
                result = _o203_copy.deepcopy(parent_action)
                for o in result['market']:
                    if o == ['BUY_ANIMAL', 'SHEEP', 2]:
                        o[1] = 'COW'; st['rewrites'] += 1
        elif st['mode'] and step in _O203_SCHEDULE:
            farm = observation['farms'][seat]
            positions = [farm['farmer'], *farm['hands']]
            cmds = [parent_action.get('farmer')] + list(parent_action.get('hands') or [])
            out = None
            for w, cmd, pos in _O203_SCHEDULE[step]:
                ok = w < len(cmds) and cmds[w] == cmd and (pos is None or (w < len(positions) and tuple(positions[w]) == pos))
                if not ok:
                    st['mismatch'] += 1; continue
                out = out or _o203_copy.deepcopy(parent_action)
                new = [cmd[0], 'COW'] + list(cmd[2:])
                if w == 0:
                    out['farmer'] = new
                else:
                    out['hands'][w - 1] = new
                st['rewrites'] += 1
            if out is not None:
                result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O203_REPORT.clear()
    _O203_REPORT.update(getattr(_O203_PARENT, 'telemetry', {}))
    _O203_REPORT.update({'o203_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O203_REPORT
agent = globals().pop('agent')
