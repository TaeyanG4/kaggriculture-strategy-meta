"""User-run accounting using the pinned official engine, original actions only.

No candidate optimization occurs here. Original replay observations must match
every transition before the ledger is usable. Both private inventories are for
offline diagnostic attribution only and must never become policy inputs.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import copy
import importlib
import json
from pathlib import Path

from .league import digest, engine_identity, write_json


def stock(private):
    result = Counter(private['shed'])
    for inv in private['inventories']:
        result.update(inv)
    return dict(result)


def execute(job):
    from kaggle_environments import make
    from .replay_lab import tape_policy

    if engine_identity() != job['engine']:
        raise ValueError('Engine drift before accounting')
    if digest(Path(__file__).read_bytes()) != job['accounting_sha256']:
        raise ValueError('Accounting source drift')
    raw = Path(job['replay']).read_bytes()
    if digest(raw) != job['replay_sha256']:
        raise ValueError('Replay drift before accounting')
    replay = json.loads(raw)
    module = importlib.import_module('kaggle_environments.envs.kaggriculture.kaggriculture')
    env = make('kaggriculture', configuration=dict(replay['configuration'], seed=replay['info']['seed']))
    env.reset(2)
    farms = env.state[0].observation.farms
    privates = [s.observation.private for s in env.state]
    transactions, units, discards = [], [], []
    originals = {name: getattr(module, name) for name in
                 ('_commit_unit', '_do_hire', '_do_buy_land', '_apply_unit_action', '_drop_inventories_to_shed')}
    original_interpreter = env.interpreter

    def observed_interpreter(state, environment):
        nonlocal farms, privates
        # The framework recursively copies state before EVERY interpreter call.
        farms = state[0].observation.farms
        privates = [s.observation.private for s in state]
        return original_interpreter(state, environment)

    def seat_of(value, objects):
        for seat, obj in enumerate(objects):
            if value is obj:
                return seat
        raise ValueError('Unknown engine object in accounting')

    def step_now():
        return int(env.state[0].observation.step)

    def commit(op, item, price, farm, private, market, shed_capacity=100):
        before = farm['money']
        success = originals['_commit_unit'](op, item, price, farm, private, market, shed_capacity)
        if success:
            transactions.append({'step': step_now(), 'seat': seat_of(farm, farms),
                                 'op': op, 'item': item, 'quantity': 1,
                                 'cash_delta': farm['money'] - before, 'unit_price': price})
        return success

    def atomic(name, farm, *args, **kwargs):
        before = farm['money']
        result = originals[name](farm, *args, **kwargs)
        if farm['money'] != before:
            transactions.append({'step': step_now(), 'seat': seat_of(farm, farms),
                                 'op': 'HIRE' if name == '_do_hire' else 'BUY_LAND',
                                 'quantity': 1, 'cash_delta': farm['money']-before})
        return result

    def apply(farm, private, actor, action, *args, **kwargs):
        positions = [farm['farmer'], *farm['hands']]
        if actor >= len(positions):
            return originals['_apply_unit_action'](farm, private, actor, action, *args, **kwargs)
        x, y = positions[actor]
        before = copy.deepcopy({'pos': positions[actor], 'tile': farm['tiles'][y][x],
                                'stock': stock(private), 'seeds': private['seeds'],
                                'inventory': private['inventories'][actor]})
        result = originals['_apply_unit_action'](farm, private, actor, action, *args, **kwargs)
        positions_after = [farm['farmer'], *farm['hands']]
        after = {'pos': positions_after[actor], 'tile': farm['tiles'][y][x],
                 'stock': stock(private), 'seeds': private['seeds'],
                 'inventory': private['inventories'][actor]}
        # Movement between shed and carried inventory has no total-stock change;
        # record physical actor inventories too, so successful transfers are visible.
        deltas = {k: after['stock'].get(k, 0)-before['stock'].get(k, 0)
                  for k in set(before['stock']) | set(after['stock'])}
        deltas = {k: v for k, v in deltas.items() if v}
        units.append({'step': step_now(), 'seat': seat_of(farm, farms), 'actor': actor,
                      'action': action, 'pos': [x, y], 'stock_delta': deltas,
                      'tile_changed': before['tile'] != after['tile'],
                      'position_changed': before['pos'] != after['pos'],
                      'inventory_changed': before['inventory'] != after['inventory'],
                      'seeds_changed': before['seeds'] != after['seeds']})
        return result

    def drop(private, capacity):
        before = stock(private)
        result = originals['_drop_inventories_to_shed'](private, capacity)
        after = stock(private)
        lost = {k: v-after.get(k, 0) for k, v in before.items() if v > after.get(k, 0)}
        if lost:
            discards.append({'step': step_now(), 'seat': seat_of(private, privates), 'items': lost})
        return result

    module._commit_unit = commit
    module._do_hire = lambda farm, *a, **kw: atomic('_do_hire', farm, *a, **kw)
    module._do_buy_land = lambda farm, *a, **kw: atomic('_do_buy_land', farm, *a, **kw)
    module._apply_unit_action = apply
    module._drop_inventories_to_shed = drop
    env.interpreter = observed_interpreter
    mismatch = []
    try:
        # Match Environment.run's standard action adapter using the initialized
        # state; the interpreter wrapper refreshes ledger references each step.
        runner = env._Environment__agent_runner([tape_policy(replay, s) for s in (0, 1)])
        while not env.done:
            actions, logs = runner.act()
            env.step(actions, logs)
            n = len(env.steps)-1
            if n >= len(replay['steps']):
                raise ValueError('Replay length exceeded')
            for seat in (0, 1):
                actual, expected = env.steps[n][seat]['observation'], replay['steps'][n][seat]['observation']
                for key in ('farms', 'market', 'town', 'private', 'day', 'hour'):
                    if actual[key] != expected[key]:
                        mismatch.append({'step': n, 'seat': seat, 'field': key})
            if mismatch:
                break
    finally:
        for name, value in originals.items():
            setattr(module, name, value)
        env.interpreter = original_interpreter
    rewards = [s.reward for s in env.steps[-1]]
    expected_rewards = [s['reward'] for s in replay['steps'][-1]]
    if mismatch or len(env.steps) != len(replay['steps']) or rewards != expected_rewards:
        raise ValueError('Accounting replay differs: ' + str(mismatch[:3]))
    totals = []
    for seat in (0, 1):
        rows = [r for r in transactions if r['seat'] == seat]
        by_op, quantities, sales = defaultdict(float), Counter(), defaultdict(float)
        for r in rows:
            by_op[r['op']] += r['cash_delta']
            quantities[r['op'] + ':' + r.get('item', '')] += r['quantity']
            if r['op'] == 'SELL':
                sales[r['item']] += r['cash_delta']
        initial = replay['steps'][0][0]['observation']['farms'][seat]['money']
        residual = rewards[seat] - initial - sum(r['cash_delta'] for r in rows)
        if residual != 0:
            raise ValueError('Unattributed cash movement')
        harvested, consumed = Counter(), Counter()
        for r in units:
            if r['seat'] != seat:
                continue
            op = r['action'][0] if r['action'] else None
            for item, delta in r['stock_delta'].items():
                if op in ('HARVEST', 'COLLECT_FERTILIZER') and delta > 0:
                    harvested[item] += delta
                if op in ('FEED', 'FERTILIZE') and delta < 0:
                    consumed[item] -= delta
        totals.append({'seat': seat, 'final_cash': rewards[seat], 'initial_cash': initial,
                       'cash_delta_by_operation': dict(by_op), 'quantities': dict(quantities),
                       'sales_revenue_by_item': dict(sales), 'harvested_and_collected': dict(harvested),
                       'feed_and_fertilizer_consumed': dict(consumed), 'cash_residual': residual})
    result = {'episode': job['episode'], 'valid': True, 'original_observations_match': True,
              'states': len(env.steps), 'engine': job['engine'], 'replay_sha256': job['replay_sha256'],
              'totals': totals, 'transactions': transactions, 'field_events': units, 'day_end_discards': discards,
              'note': 'Realized cash attribution from original actions; not a causal counterfactual or future policy input.'}
    write_json(Path(job['output']), result)
    return result
