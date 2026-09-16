# opp_bursty (Claude/o-series, 2026-09-16). OPPONENT PROXY ONLY. Mirror (c150) that sells in bursts: all SELL orders are
# dropped except every 8th step, when it dumps its whole shed. Emulates a bursty dumper (Artem-style sheds ~1 but batch
# sales) to test whether dip-selling (o228) finds dips against such rivals.
_BU_PARENT = agent
_BU_PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL', 'FERTILIZER')
del agent


def agent(observation, configuration=None):
    action = _BU_PARENT(observation, configuration)
    try:
        step = int(observation.get('step', 0))
        if 216 <= step < 696:
            market = [o for o in (action.get('market') or []) if not (o and o[0] == 'SELL')]
            if step % 8 == 0:
                shed = observation['private']['shed']
                for item in _BU_PRODUCTS:
                    q = int(shed.get(item, 0))
                    if q > 0 and len(market) < 10:
                        market.append(['SELL', item, q])
            action = dict(action); action['market'] = market
    except Exception:
        pass
    return action


agent = globals().pop('agent')
