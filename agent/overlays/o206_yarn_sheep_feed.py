# o206_yarn_sheep_feed (Claude/o-series, 2026-09-15). Overlay for the o199c stack.
"""Never skip SHEEP feeds on yarn routes (YARN_STORE among the first two shops).
World bank: o162's feed gate loses -540 vs V43/FSV4/MSF in yarn worlds (11-14 sheep) while winning
elsewhere - skipped sheep feeds cut wool output, which is our dumping weapon there. Implemented by
wrapping o159's value function: on a yarn route a SHEEP feed is valued as infinite (abandonment path
untouched). Telemetry o206_on (1 = yarn route this game).
"""
_O206_PARENT = agent
_O206_FLAG = {}
_O206_REPORT = {}
_o206_orig_value = _o159_value
del agent


def _o159_value(tile, kind, day, prices):
    v, a = _o206_orig_value(tile, kind, day, prices)
    if kind == 'SHEEP' and _O206_FLAG.get('on'):
        return 1e9, a
    return v, a


def agent(observation, configuration=None):
    shops = observation.get('town', {}).get('unlocked_shops', []) or []
    _O206_FLAG['on'] = 'YARN_STORE' in shops[:2]
    result = _O206_PARENT(observation, configuration)
    _O206_REPORT.clear()
    _O206_REPORT.update(getattr(_O206_PARENT, 'telemetry', {}))
    _O206_REPORT['o206_on'] = int(_O206_FLAG['on'])
    return result


agent.telemetry = _O206_REPORT
agent = globals().pop('agent')
