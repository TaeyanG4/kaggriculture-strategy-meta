# o198_berry_fertilize (Claude/o-series, 2026-09-15). Overlay for o182.
"""Opportunistic strawberry fertilizing on a WATER turn.
Measured (o182, 2 seeds): 57-76 turns/game a worker WATERs an unfertilized STRAWBERRY tile while
carrying fertilizer; 20% of strawberry productions go unfertilized. Engine: an ongoing crop only
needs water every second day (weed at consecutive_unwatered >= 2) and the fertilizer bonus (+1 unit)
applies on a production night that was watered with fertilized_until_day >= day. So on a tile that is
watered (consecutive_unwatered == 0) and unfertilized, replacing today's WATER with FERTILIZE costs
nothing today (no bonus existed) and yields +1 on the next production night (day+1 or day+2), when the
tape waters again. Guards: STRAWBERRY only (V219 handles tomato), fertilizer in hand 1..4 (V219
workers carry 10), a production night must fall in [day+1, min(day+2, 28)], productions left < 4.
Telemetry: o198_swaps, o198_errors.
"""
import copy as _o198_copy

_O198_PARENT = agent
_O198_STATE = {}
_O198_REPORT = {}
_O198_MAX_FERT = 4
_O198_FIRST, _O198_INTERVAL, _O198_MAX = 10, 2, 4      # STRAWBERRY crop table
del agent


def _o198_gain_night(tile, day):
    """True if a strawberry production night falls on day+1 or day+2 (<= 28) with productions left."""
    planted = int(tile.get('planted_day', 0))
    for d in (day + 1, day + 2):
        if d > 28:
            return False
        since = d + 1 - planted - _O198_FIRST          # engine: days_since_first at end of day d
        if since >= 0 and since % _O198_INTERVAL == 0 and since // _O198_INTERVAL + 1 <= _O198_MAX:
            return True
    return False


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O198_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O198_STATE[seat] = {'last': -1, 'swaps': 0, 'errors': 0}
    st['last'] = step
    parent_action = _O198_PARENT(observation, configuration)
    result = parent_action
    try:
        day = step // 24
        if day <= 27:
            farm = observation['farms'][seat]
            positions = [farm['farmer'], *farm['hands']]
            invs = observation['private']['inventories']
            cmds = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
            out = None
            for i, c in enumerate(cmds[:len(positions)]):
                if c != ['WATER'] or i >= len(invs):
                    continue
                fert = int(invs[i].get('FERTILIZER', 0) or 0)
                if not 1 <= fert <= _O198_MAX_FERT:
                    continue
                x, y = positions[i]
                tile = farm['tiles'][y][x]
                if not (isinstance(tile, dict) and tile.get('kind') == 'PLANT' and tile.get('crop') == 'STRAWBERRY'):
                    continue
                if tile.get('watered_today') or int(tile.get('consecutive_unwatered', 0) or 0) != 0:
                    continue
                if int(tile.get('fertilized_until_day', -1)) >= day or not _o198_gain_night(tile, day):
                    continue
                out = out or _o198_copy.deepcopy(parent_action)
                if i == 0:
                    out['farmer'] = ['FERTILIZE']
                else:
                    out['hands'][i - 1] = ['FERTILIZE']
                st['swaps'] += 1
            if out is not None:
                result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O198_REPORT.clear()
    _O198_REPORT.update(getattr(_O198_PARENT, 'telemetry', {}))
    _O198_REPORT.update({'o198_swaps': st['swaps'], 'o198_errors': st['errors']})
    return result


agent.telemetry = _O198_REPORT
agent = globals().pop('agent')
