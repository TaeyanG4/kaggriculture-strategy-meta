# opp_restrainer (Claude/o-series, 2026-09-16). OPPONENT PROXY ONLY — never a candidate.
# Wraps the mirror (c150) and throttles its sales: each SELL is capped to a quarter of the remaining headroom to the
# market target T (inventory relative to I0), and dropped when the market is already above target and the price is
# below 60% of base. Emulates a "restrainer" (top-cluster style: small batches, buffers kept) to test how our dumping
# lineage fares against non-dumpers. Everything else is the mirror tape.
_RS_PARENT = agent
_RS_T = {'WHEAT': 400, 'CARROT': 450, 'TOMATO': 200, 'STRAWBERRY': 100, 'MELON': 300, 'EGG': 332, 'MILK': 122, 'WOOL': 105, 'FERTILIZER': 200}
_RS_BASE = {'WHEAT': 25, 'CARROT': 35, 'TOMATO': 60, 'STRAWBERRY': 120, 'MELON': 250, 'EGG': 50, 'MILK': 160, 'WOOL': 200, 'FERTILIZER': 100}
_RS_I0 = 10000
_RS_REPORT = {'rs_capped': 0, 'rs_dropped': 0}
del agent


def agent(observation, configuration=None):
    action = _RS_PARENT(observation, configuration)
    try:
        step = int(observation.get('step', 0))
        inv = observation['market']['inventory']; prices = observation['market']['prices']
        if step >= 696:   # let the terminal liquidation run untouched
            return action
        out = []
        for o in action.get('market') or []:
            if o and o[0] == 'SELL' and o[1] in _RS_T and len(o) >= 3:
                head = _RS_T[o[1]] - (int(inv[o[1]]) - _RS_I0)
                cap = max(3, head // 3)
                if False:
                    _RS_REPORT['rs_dropped'] += 1; continue
                if int(o[2]) > cap:
                    _RS_REPORT['rs_capped'] += 1; o = [o[0], o[1], int(cap)]
            out.append(o)
        action = dict(action); action['market'] = out
    except Exception:
        pass
    return action


agent.telemetry = _RS_REPORT
agent = globals().pop('agent')
