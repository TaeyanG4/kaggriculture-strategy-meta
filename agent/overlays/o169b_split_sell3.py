# o169_split_sell: cap large SELL batches of steep-curve products and drip the remainder over the
# following steps. Evidence: 2750+ rivals sell MILK/STRAWBERRY/WOOL at ~1.5x more steps with smaller
# batches and realise $93 vs our $80 per MILK (o_tools/ divergence audit, reports/r000-*.md).
# Rule: for item in ITEMS, a SELL with qty > CAP is cut to CAP; the cut units go to a per-item deferred
# pool that is re-issued as SELL min(deferred, CAP) on later steps where the parent has no SELL of that
# item (only while the shed still holds it). Window: days 8-27; day 28+ untouched (terminal logic).
import copy as _o169_copy

_O169_PARENT = agent
_O169_STATE = {}
_O169_REPORT = {}
_O169_ITEMS = ('MILK', 'STRAWBERRY', 'WOOL')
_O169_CAP = 3
_O169_WINDOW = (192, 672)
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    st = _O169_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O169_STATE[seat] = {'last': -1, 'deferred': {}, 'cut_units': 0, 'drip_orders': 0, 'errors': 0}
    st['last'] = step
    parent = _O169_PARENT(observation, configuration); result = parent
    try:
        if _O169_WINDOW[0] <= step < _O169_WINDOW[1]:
            shed = observation['private'].get('shed') or {}
            market = [list(o) for o in (parent.get('market') or [])]
            changed = False; selling = set()
            for o in market:
                if o and o[0] == 'SELL' and len(o) >= 3 and o[1] in _O169_ITEMS:
                    selling.add(o[1]); q = min(int(o[2]), int(shed.get(o[1], 0)))   # parent orders overstate; use what the shed can fill
                    if q > _O169_CAP:
                        st['deferred'][o[1]] = st['deferred'].get(o[1], 0) + (q - _O169_CAP); st['cut_units'] += q - _O169_CAP
                        o[2] = _O169_CAP; changed = True
            for item in _O169_ITEMS:
                d = st['deferred'].get(item, 0)
                if d <= 0 or item in selling or len(market) >= 10:
                    continue
                q = min(d, _O169_CAP, int(shed.get(item, 0)))
                if q <= 0:
                    st['deferred'][item] = 0 if shed.get(item, 0) <= 0 else d
                    continue
                market.append(['SELL', item, q]); st['deferred'][item] = d - q; st['drip_orders'] += 1; changed = True
            if changed:
                result = _o169_copy.deepcopy(parent); result['market'] = market
    except Exception:
        st['errors'] += 1; result = parent
    _O169_REPORT.clear(); _O169_REPORT.update(getattr(_O169_PARENT, 'telemetry', {}))
    _O169_REPORT.update({'o169_' + k: v for k, v in st.items() if k not in ('last', 'deferred')})
    return result


agent.telemetry = _O169_REPORT
agent = globals().pop('agent')
