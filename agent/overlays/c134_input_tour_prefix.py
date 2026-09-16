# SPDX-License-Identifier: Apache-2.0
"""Keep profitable prefixes of native optional fertilizer tours.

The parent proposes a greedy tour then accepts/rejects the whole bundle. A costly
tail can reject useful earlier stops. Compare prefixes using the parent's same
prices, yield forecast and 1.5 cost hurdle; actual funding/stock gates still run.
No opponent identity, future environment, or private opponent state is read.
"""
_C134_PATH_PARENT = _r51_input_path
_C134_AGENT_PARENT = agent
_C134_STATS = {}
_C134_REPORT = {}
del agent


def _r51_input_path(obs, targets):
    path, quantities = _C134_PATH_PARENT(obs, targets)
    if len(path) <= 3:
        return path, quantities
    seat = int(obs['player'])
    stats = _C134_STATS.setdefault(seat, {'prefix_choices': 0, 'pruned_stops': 0, 'errors': 0})
    try:
        farm = obs['farms'][seat]
        step = int(obs['step']); day = step // 24
        now = step + 4; pos = (4, 4); units = {'WHEAT': 0, 'CARROT': 0}
        choices = []
        for index, (x, y, crop, birth) in enumerate(path):
            arrival = now + abs(pos[0] - x) + abs(pos[1] - y)
            units[crop] += _r51_input_gain(targets[(x, y)], arrival, day)
            now = arrival + 1; pos = (x, y)
            count = index + 1
            if count < 3:
                continue
            quote = _r37_market_price('FERTILIZER', obs['market']['inventory']['FERTILIZER'] - count)
            cost = count * (quote + 2) + _v219_fib(int(farm['hires_today']))
            value = sum(n * max(1, _r37_market_price(item, obs['market']['inventory'][item] + n) - 2)
                        for item, n in units.items())
            choices.append((value - 1.5 * cost, count, dict(units)))
        best = max(choices, key=lambda row: (row[0], row[1]))
        # Preserve the original route on equal utility and on insufficient margin.
        # The caller rechecks topups, earlier tours, cash, market slots and hires.
        if best[0] >= 50 and best[1] < len(path) and best[0] > choices[-1][0]:
            stats['prefix_choices'] += 1
            stats['pruned_stops'] += len(path) - best[1]
            return path[:best[1]], best[2]
    except Exception:
        stats['errors'] += 1
    return path, quantities


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    stats = _C134_STATS.get(seat)
    if stats is None or step <= stats.get('last', -1):
        stats = _C134_STATS[seat] = {'last': -1, 'prefix_choices': 0, 'pruned_stops': 0, 'errors': 0}
    stats['last'] = step
    result = _C134_AGENT_PARENT(observation, configuration)
    _C134_REPORT.clear()
    _C134_REPORT.update(getattr(_C134_AGENT_PARENT, 'telemetry', {}))
    _C134_REPORT.update({'input_prefix_' + key: value for key, value in stats.items() if key != 'last'})
    return result


agent.telemetry = _C134_REPORT
agent = globals().pop('agent')
