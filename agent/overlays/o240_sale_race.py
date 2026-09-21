# o240 sale race (Claude, 2026-09-19). The public K0006 (jaxa623) beats our o227/o238/o239 22-24/32 in pinned worlds by
# ~$150 margins with three sale-timing habits that our r36/r37 machinery only half has: (1) the reservation horizon is a
# whole day (ours: 8 turns in the 288..696 window), (2) premium sales the tape plans for the next two turns are executed
# now when the units already sit in the shed, (3) every turn's SELL orders are listed before hires/seeds/animals so they
# execute at earlier lockstep indices than a mirror's. Same ideas, own implementation; knobs via env for the sweep.
import os as _o240_os
_O240_PARENT = agent
_O240_H = int(_o240_os.environ.get('KAGG_O240_H', '24') or 24)
_O240_ADV = int(_o240_os.environ.get('KAGG_O240_ADV', '2') or 0)
_O240_FRONT = int(_o240_os.environ.get('KAGG_O240_FRONT', '1') or 0)
_O240_PREMIUM = ('STRAWBERRY', 'WOOL', 'EGG', 'MILK', 'MELON', 'CARROT', 'TOMATO')
_O240_REPORT = {'o240_adv_turns': 0, 'o240_adv_units': 0, 'o240_front_turns': 0, 'o240_errors': 0}
del agent


class _O240Horizons(dict):
    """r36_reserve reads _R37_HORIZONS.get(player, 2); the parent writes 2/3/4/8 into it. Widen every value >= 4 to a day."""
    def get(self, key, default=None):
        v = dict.get(self, key, default)
        return _O240_H if (v is not None and v >= 4 and _O240_H > v) else v


_R37_HORIZONS = _O240Horizons(_R37_HORIZONS)


def _o240_future_market(observation, offset):
    step = int(observation['step']) + offset
    if step >= 719:
        return None
    native = _IMPL.chassis.players.get(int(observation['player']))
    route = 2 if step >= 648 else (native or {}).get('route')
    if route is None or route not in _IMPL.chassis.routes:
        return None
    return _IMPL.chassis.routes[route][step].get('market') or []


def _o240_advance(observation, market):
    step = int(observation['step'])
    if _O240_ADV <= 0 or step % 24 == 23 or step >= 718:
        return market
    want = {}; protected = None
    for off in range(1, _O240_ADV + 1):
        fut = _o240_future_market(observation, off)
        if not fut:
            continue
        if protected is None and fut and len(fut[0]) > 2 and fut[0][0] == 'SELL':
            protected = fut[0][1]   # the parent's sale-credit funds the next turn's feed from its first-listed sell
        for o in fut:
            if len(o) > 2 and o[0] == 'SELL' and o[1] in _O240_PREMIUM and o[1] != protected:
                want[o[1]] = want.get(o[1], 0) + max(0, int(o[2]))
    if not want:
        return market
    shed = observation['private']['shed']
    cur = [list(o) for o in market]
    now = {}
    for o in cur:
        if len(o) > 2 and o[0] == 'SELL':
            now[o[1]] = now.get(o[1], 0) + int(o[2])
    extra = []; merged = 0
    for item, q in want.items():
        n = min(q, int(shed.get(item, 0)) - now.get(item, 0))
        if n < 1:
            continue
        hit = next((o for o in cur if len(o) > 2 and o[0] == 'SELL' and o[1] == item), None)
        if hit is not None:
            hit[2] = int(hit[2]) + n; merged += n
        else:
            extra.append(['SELL', item, n])
    extra = extra[:max(0, 10 - len(cur))]
    if not extra and not merged:
        return market
    _O240_REPORT['o240_adv_turns'] += 1; _O240_REPORT['o240_adv_units'] += merged + sum(e[2] for e in extra)
    return extra + cur


_O240_STEEP = {'MELON': 0, 'WOOL': 1, 'STRAWBERRY': 2, 'MILK': 3, 'TOMATO': 4, 'CARROT': 5, 'EGG': 6, 'FERTILIZER': 7, 'WHEAT': 8}   # sq/linear curves first: when a mirror lists the same items in another order, index 0 wins the steep one outright
_O240_STEEP_ON = int(_o240_os.environ.get('KAGG_O240_STEEP', '0') or 0)


def _o240_frontload(market):
    if not _O240_FRONT or len(market) < 2:
        return market
    sells, buys, rest = [], [], []
    for j, o in enumerate(market):
        if o[0] == 'SELL' and not any(p[0] == 'BUY_PRODUCT' and len(p) > 1 and len(o) > 1 and p[1] == o[1] for p in market[:j]):
            sells.append(o)
        elif o[0] in ('SELL', 'BUY_PRODUCT'):
            buys.append(o)
        else:
            rest.append(o)
    if _O240_STEEP_ON:
        sells.sort(key=lambda o: _O240_STEEP.get(o[1], 9))
    new = sells + buys + rest
    if new != market:
        _O240_REPORT['o240_front_turns'] += 1
    return new


_O240_FEED0 = int(_o240_os.environ.get('KAGG_O240_FEED0', '0') or 0)
_O238_UNITS = int(_o240_os.environ.get('KAGG_O238_UNITS', '10') or 10)   # o240 default pair = 10: vs single-pair openers (Jaxa 10, V46 7/2) a 50-pair only pays the lift twice (Jaxa 44% -> 62% wins)


def agent(observation, configuration=None):
    action = _O240_PARENT(observation, configuration)
    try:
        step = int(observation.get('step', 0))
        if isinstance(action, dict) and step == 0:
            _O240_REPORT.update(o240_adv_turns=0, o240_adv_units=0, o240_front_turns=0, o240_errors=0)
        if _O240_FEED0 and isinstance(action, dict):
            m = [list(o) for o in (action.get('market') or [])]
            if step == 0 and len(m) == 2 and m[0][:2] == ['BUY_PRODUCT', 'WHEAT'] and m[1][:2] == ['SELL', 'WHEAT'] and m[0][2] == m[1][2]:
                m[0][2] += 5   # feed bought at index 0 of turn 0: V46's turn-1 lift (BUY 30 at index 0) then hits nobody
                action = dict(action, market=m)
            elif step == 1 and ['BUY_PRODUCT', 'WHEAT', 5] in m:
                m.remove(['BUY_PRODUCT', 'WHEAT', 5]); action = dict(action, market=m)
        if isinstance(action, dict):
            market = [list(o) for o in (action.get('market') or []) if isinstance(o, (list, tuple)) and o]
            new = _o240_frontload(_o240_advance(observation, market))
            if new != market:
                action = dict(action, market=new)
    except Exception:
        _O240_REPORT['o240_errors'] += 1
    _O240_REPORT.update(getattr(_O240_PARENT, 'telemetry', {}))
    return action


agent.telemetry = _O240_REPORT
agent = globals().pop('agent')
