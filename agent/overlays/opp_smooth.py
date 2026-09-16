# opp_smooth (Claude/o-series, 2026-09-16). OPPONENT PROXY ONLY. Mirror (c150) turned into a smooth seller in the
# style of the top planners (Majkel shed buffers ~6 milk / ~11 strawberry / ~7 wool, batches of 2-4): every SELL of a
# race product is capped at 4 units per step, and each step the proxy adds its own SELL orders to sell stock above a
# buffer of 6 (max 4 per step). Terminal steps (>= 696) untouched. Everything else is the mirror tape.
_SM_PARENT = agent
_SM_ITEMS = ('CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
_SM_BATCH = 4
_SM_BUFFER = 6
del agent


def agent(observation, configuration=None):
    action = _SM_PARENT(observation, configuration)
    try:
        step = int(observation.get('step', 0))
        if 48 <= step < 696:
            shed = observation['private']['shed']; prices = observation['market']['prices']
            out = []; selling = set()
            for o in action.get('market') or []:
                if o and o[0] == 'SELL' and o[1] in _SM_ITEMS and len(o) >= 3:
                    o = [o[0], o[1], int(min(int(o[2]), _SM_BATCH))]; selling.add(o[1])
                out.append(o)
            for item in _SM_ITEMS:
                stock = int(shed.get(item, 0))
                if item in selling or stock <= _SM_BUFFER or prices.get(item, 0) <= 1 or len(out) >= 10:
                    continue
                out.append(['SELL', item, int(min(_SM_BATCH, stock - _SM_BUFFER))])
            action = dict(action); action['market'] = out
    except Exception:
        pass
    return action


agent = globals().pop('agent')
