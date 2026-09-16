"""Generate agent/overlays/o233_planner_takeover.py: embeds agent/opp_planner_proxy.py (minus its module-level agent)
in a private namespace and hands the field/purchase decisions to it from day KAGG_O233_DAY (default 15), keeping the
tape stack's SELL orders. Run: python o_tools/build_o233.py"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'agent', 'opp_planner_proxy.py'), encoding='utf-8').read()
core = src[:src.index('def agent(observation, configuration=None):')]
TEMPLATE = '''# o233_planner_takeover (Claude/o-series, 2026-09-16). From day KAGG_O233_DAY (default 15) the tape-free planner
# (agent/opp_planner_proxy.py, embedded below in its own namespace) takes over the FIELD commands and the purchase/hire
# orders, while the tape stack keeps producing the SELL orders (r36/r37/c115/o224/o227 race machinery stays intact).
# Rationale: our lineage leads the top planners until ~day 12 and falls behind in the d12-30 production loop
# (fertilizer use, strawberry cycles, labor); the planner runs that loop on the farm the tape built. Fallback: any
# planner exception returns the tape action for that step. Telemetry o233_days, o233_errors.
import os as _o233_os
_O233_PARENT = agent
_O233_DAY = int(_o233_os.environ.get('KAGG_O233_DAY', '15') or 15)
_O233_REPORT = {}
_O233_NS = {'__name__': 'o233_planner'}
_O233_SRC = __SRC__
exec(compile(_O233_SRC, 'o233_planner', 'exec'), _O233_NS)
_O233_PROXIES = {}
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0)); day = step // 24
    tape = _O233_PARENT(observation, configuration)
    if step == 0:
        _O233_PROXIES.pop(seat, None); _O233_REPORT.update(o233_days=0, o233_errors=0)
    if day < _O233_DAY:
        _O233_REPORT.update(getattr(_O233_PARENT, 'telemetry', {}))
        return tape
    try:
        px = _O233_PROXIES.get(seat)
        if px is None or step <= px.last_step:
            px = _O233_PROXIES[seat] = _O233_NS['Proxy'](seat)
        px.last_step = step
        plan = px.act(observation)
        sells = [o for o in (tape.get('market') or []) if o and o[0] == 'SELL']
        buys = [o for o in (plan.get('market') or []) if o and o[0] != 'SELL']
        result = {'farmer': plan['farmer'], 'hands': plan['hands'], 'market': (sells + buys)[:10]}
        if step % 24 == 0:
            _O233_REPORT['o233_days'] = _O233_REPORT.get('o233_days', 0) + 1
    except Exception:
        _O233_REPORT['o233_errors'] = _O233_REPORT.get('o233_errors', 0) + 1
        result = tape
    _O233_REPORT.update(getattr(_O233_PARENT, 'telemetry', {}))
    return result


agent.telemetry = _O233_REPORT
agent = globals().pop('agent')
'''
out = TEMPLATE.replace('__SRC__', repr(core))
path = os.path.join(ROOT, 'agent', 'overlays', 'o233_planner_takeover.py')
open(path, 'w', encoding='utf-8').write(out)
compile(out, path, 'exec')
print('wrote', path, len(out), 'bytes')
