# SPDX-License-Identifier: Apache-2.0
# r000_terminal_hold (reverse-engineering series, 2026-09-15). Overlay appended to immutable c150.
"""r000: bounded endgame intervention reverse-engineered from the #1 team's public replays.

Field-ledger finding (o_tools/phase_ledger.py, o_tools/terminal_timing.py on 48 Majkel1337
replays): the leader is slightly BEHIND its opponents in money through step 672 and wins the
whole game (+3.5k mean) in the final 48 steps (+5.2k there), mostly on STRAWBERRY (+3.4k) and
TOMATO (+2.3k) plus WOOL/EGG/MILK. Mechanism: from day 26 it stops selling the steep-curve
products, holds ~30-40 units, and sells them in the final steps at the recovered price
(strawberry ~$116-123 at steps 700-719 vs ~$72-85 right after the cluster tape's day-27
"route 2" liquidation dump at step 648). Our c150 lineage dumps ~14 strawberries in the first
six steps of day 27 and again at day 28.

Intervention (frozen parent, narrow gate, every unit credited exactly once):
  HOLD  648 <= step < 696: remove the parent's SELL orders for HOLD_ITEMS while projected
        holdings (shed + carried) stay <= SHED_ROOM (leaves room for the parent's warehouse
        guards; never lets the shed overflow because of the hold).
  DRIP  696 <= step < 718: if the parent does not already sell the item this step and a market
        slot is free, add SELL item ceil(shed_qty / DRIP_DIV) so held stock is released
        gradually across day 29 instead of in one price-crashing batch; the parent's own
        step-718/719 terminal rescue sells whatever remains.
No cash, feed, movement, hire or price-threshold logic is touched. Telemetry: held units
suppressed per item, drip units requested per item (requests, not realised revenue), errors.
"""
import copy as _r000_copy
import math as _r000_math

_R000_PARENT = agent
_R000_STATE = {}
_R000_REPORT = {}
_R000_ITEMS = ('STRAWBERRY', 'TOMATO', 'WOOL')
_R000_HOLD = (648, 696)
_R000_DRIP = (696, 718)
_R000_SHED_ROOM = 85      # projected shed+carried units above which we stop holding
_R000_DRIP_DIV = 6        # sell ceil(shed/6) per step during the drip window
_R000_MAX_ORDERS = 10
del agent


def _r000_holdings(observation, seat):
    private = observation['private']
    total = sum(int(v) for v in (private.get('shed') or {}).values())
    for inv in private.get('inventories') or []:
        total += sum(int(v) for v in (inv or {}).values())
    return total


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _R000_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _R000_STATE[seat] = {'last': -1, 'errors': 0, 'hold_steps': 0, 'room_blocks': 0,
                                  **{'suppressed_' + k: 0 for k in _R000_ITEMS},
                                  **{'drip_requested_' + k: 0 for k in _R000_ITEMS}}
    st['last'] = step
    parent_action = _R000_PARENT(observation, configuration)   # exactly one parent call
    result = parent_action
    try:
        market = list(parent_action.get('market') or [])
        if _R000_HOLD[0] <= step < _R000_HOLD[1]:
            if _r000_holdings(observation, seat) <= _R000_SHED_ROOM:
                kept = []
                changed = False
                for order in market:
                    if order and order[0] == 'SELL' and len(order) >= 3 and order[1] in _R000_ITEMS:
                        st['suppressed_' + order[1]] += int(order[2]); changed = True
                        continue
                    kept.append(order)
                if changed:
                    result = _r000_copy.deepcopy(parent_action)
                    result['market'] = kept
                    st['hold_steps'] += 1
            else:
                st['room_blocks'] += 1
        elif _R000_DRIP[0] <= step < _R000_DRIP[1]:
            shed = observation['private'].get('shed') or {}
            selling = {o[1] for o in market if o and o[0] == 'SELL' and len(o) >= 3}
            extra = []
            for item in _R000_ITEMS:
                qty = int(shed.get(item, 0) or 0)
                if qty <= 0 or item in selling:
                    continue
                q = max(1, int(_r000_math.ceil(qty / _R000_DRIP_DIV)))
                extra.append(['SELL', item, q])
            if extra and len(market) < _R000_MAX_ORDERS:
                extra = extra[:_R000_MAX_ORDERS - len(market)]
                result = _r000_copy.deepcopy(parent_action)
                result['market'] = market + extra
                for o in extra:
                    st['drip_requested_' + o[1]] += o[2]
    except Exception:
        st['errors'] += 1
        result = parent_action
    _R000_REPORT.clear()
    _R000_REPORT.update(getattr(_R000_PARENT, 'telemetry', {}))
    _R000_REPORT.update({'r000_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _R000_REPORT
agent = globals().pop('agent')
