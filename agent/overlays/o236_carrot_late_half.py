# o236_carrot_late_half (Claude/o-series, 2026-09-16). Measured late carrot pivot for PET-heavy worlds: the o199c switch
# is enabled by demand (>= 24 units/day = two PET_CAFEs) only from day 16, and its companion carrot-seed orders are
# halved so only every other wheat planting becomes a carrot (wheat keeps feeding the herd). Frozen-Majkel diagnosis
# (YARN,PET,PIZZA,PIZZA world): Majkel pivots to 23 carrots + 11 tomatoes by day 24 and out-earns us 36.5k vs 19.7k in
# d24-30; the full switch from day 8 (o235) over-supplied carrots and starved feed. Telemetry o236_halved.
_O199_DEMAND = 24
_O199_MIN_DAY = 16
_O236_PARENT = agent
_O236_REPORT = {}
del agent


def agent(observation, configuration=None):
    result = _O236_PARENT(observation, configuration)
    try:
        market = result.get('market') or []
        out = []; prev = None; halved = 0
        for o in market:
            if (o and o[0] == 'BUY_SEED' and o[1] == 'CARROT' and prev and prev[0] == 'BUY_SEED' and prev[1] == 'WHEAT'
                    and int(o[2]) == int(prev[2]) and int(o[2]) >= 2):
                o = ['BUY_SEED', 'CARROT', int(o[2]) // 2]; halved += 1
            out.append(o); prev = o
        if halved:
            result = dict(result); result['market'] = out
            _O236_REPORT['o236_halved'] = _O236_REPORT.get('o236_halved', 0) + halved
    except Exception:
        _O236_REPORT['o236_errors'] = _O236_REPORT.get('o236_errors', 0) + 1
    _O236_REPORT.update(getattr(_O236_PARENT, 'telemetry', {}))
    return result


agent.telemetry = _O236_REPORT
agent = globals().pop('agent')
