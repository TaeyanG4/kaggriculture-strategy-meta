# SPDX-License-Identifier: Apache-2.0
"""Carrot substitution using a route-certified WHEAT opportunity-cost upper bound.

Only current public market/farms and the agent's own fixed continuation are used.
This is an unqualified research derivative; parent opening and movement stay intact.
"""
_C143_PARENT = agent
_C143_STATES = {}
_C143_REPORT = {}
del agent


def _c143_after_field(obs, action):
    # Same deterministic own-unit model already embedded in the immutable parent.
    # Includes simultaneous seed-batch suppression before sequential worker actions.
    seat = int(obs['player']); step = int(obs['step'])
    farm = copy.deepcopy(obs['farms'][seat])
    private = copy.deepcopy(obs['private'])
    commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    demand = {}
    for cmd in commands:
        if len(cmd) >= 2 and cmd[0] == 'PLANT':
            demand[cmd[1]] = demand.get(cmd[1], 0) + 1
    blocked = {k for k, v in demand.items() if private['seeds'].get(k, 0) < v}
    for actor, cmd in enumerate(commands):
        if len(cmd) >= 2 and cmd[0] == 'PLANT' and cmd[1] in blocked:
            cmd = ['PASS']
        _UNIT_NS['_apply_unit_action'](farm, private, actor, cmd, 10, step // 24, 24, 100)
    _UNIT_NS['_decay_plants'](farm, step)
    return farm


def _c143_public_supply(obs, harvest_day):
    """Overestimate existing carrot supply: every visible plant yields its cap."""
    supply = 0
    for farm in obs['farms']:
        for row in farm['tiles']:
            for tile in row:
                if isinstance(tile, dict) and tile.get('crop') == 'CARROT':
                    if int(tile['planted_day']) + 2 <= harvest_day:
                        supply += 4
    return supply


def _c143_certificate(obs, positions, xy, birth, state):
    """Require two productive waters then a native harvest before carrot expiry."""
    step = int(obs['step'])
    route = _IMPL.chassis.players[int(obs['player'])]['route']
    pos = [list(p) for p in positions]
    watered = set(); plant_seen = False; dry_nights = 0; minimum_yield = 0
    access = ((4, 4), (5, 4), (4, 5), (5, 5))
    for t in range(step + 1, min((birth + 4) * 24, 712)):
        action = _IMPL.chassis.routes[2 if t >= 648 else route][t]
        commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
        for actor, cmd in enumerate(commands[:len(pos)]):
            if tuple(pos[actor]) == xy:
                if cmd == ['PLANT', 'WHEAT'] and not plant_seen and t == step + 1:
                    plant_seen = True
                elif plant_seen:
                    if cmd[0] in ('DIG', 'PLANT'):
                        state['certificate_replaced'] += 1
                        return None
                    if cmd == ['HARVEST']:
                        if 2 <= t // 24 - birth <= 3 and minimum_yield >= 2:
                            return {'step': t, 'actor': actor, 'birth': birth, 'xy': xy,
                                    'foregone_wheat_upper': min(6, 1 + 2 * minimum_yield)}
                        state['certificate_harvest'] += 1
                        return None
                    if cmd == ['WATER'] and t // 24 not in watered:
                        watered.add(t // 24)
                        if 2 <= t // 24 - birth <= 3:
                            minimum_yield += 1
            if cmd[0] in _CP0_MOVES:
                dx, dy = _CP0_MOVES[cmd[0]]
                pos[actor] = [max(0, min(9, pos[actor][0] + dx)), max(0, min(9, pos[actor][1] + dy))]
        for order in action.get('market', []):
            if order == ['HIRE']:
                chosen = min(access, key=lambda p: (sum(tuple(q) == p for q in pos), access.index(p)))
                pos.append(list(chosen))
        if (t + 1) % 24 == 0:
            if plant_seen:
                dry_nights = 0 if t // 24 in watered else dry_nights + 1
                if dry_nights >= 2:
                    state['certificate_dry'] += 1
                    return None
            pos = [[4, 4]]
    state['certificate_expired'] += 1
    return None


def _c143_control(obs, parent, state):
    step = int(obs['step']); day = step // 24; seat = int(obs['player'])
    farm = obs['farms'][seat]; private = obs['private']
    positions = [farm['farmer'], *farm['hands']]
    commands = [parent.get('farmer') or ['PASS'], *(parent.get('hands') or [])]
    result = copy.deepcopy(parent) if state['plans'] or state['pending'] else parent
    def set_command(actor, command):
        if actor == 0: result['farmer'] = command
        else: result['hands'][actor - 1] = command
    pending = state['pending']
    if pending and step == pending['plant_step']:
        state['pending'] = None
        actor = pending['actor']; x, y = pending['xy']
        if (actor < len(positions) and tuple(positions[actor]) == (x, y)
                and commands[actor] == ['PLANT', 'WHEAT'] and farm['tiles'][y][x] is None
                and private['seeds'].get('CARROT', 0) > pending['seed_before']
                and private['shed'].get('WHEAT', 0) >= pending['wheat_after_purchase']):
            set_command(actor, ['PLANT', 'CARROT'])
            state['plans'].append(pending['certificate'])
            state['conversions'] += 1
        else:
            state['purchase_or_route_errors'] += 1
    elif pending and step > pending['plant_step']:
        state['pending'] = None; state['purchase_or_route_errors'] += 1
    for plan in list(state['plans']):
        x, y = plan['xy']; tile = farm['tiles'][y][x]
        if not plan.get('checked_plant') and step > (plan['birth'] * 24) and step > plan['plant_step']:
            plan['checked_plant'] = True
            if isinstance(tile, dict) and tile.get('crop') == 'CARROT' and tile['planted_day'] == plan['birth']:
                state['confirmed_plants'] += 1
            else: state['purchase_or_route_errors'] += 1
        if step > plan['step']:
            state['harvest_errors'] += 1; state['plans'].remove(plan); continue
        if step == plan['step']:
            actor = plan['actor']
            if (actor < len(positions) and tuple(positions[actor]) == (x, y)
                    and commands[actor] == ['HARVEST'] and isinstance(tile, dict)
                    and tile.get('crop') == 'CARROT' and tile['planted_day'] == plan['birth']
                    and tile.get('yield_units', 0) >= 2):
                set_command(actor, ['HARVEST'])
                state['harvest_units_requested'] += tile['yield_units']
            else:
                state['harvest_errors'] += 1
            state['plans'].remove(plan)
    # Sell only physically projected carrot stock. Existing native orders retain priority.
    if state['conversions']:
        if result is parent: result = copy.deepcopy(parent)
        stock = projected_shed(result, FarmView(obs)).get('CARROT', 0)
        sale = sum(max(0, int(o[2])) for o in result['market'] if o[:2] == ['SELL', 'CARROT'])
        if stock > sale and len(result['market']) < 10:
            result['market'].append(['SELL', 'CARROT', stock - sale])
    if not 18 <= day <= 25 or step % 24 >= 22 or state['requests'] >= 8 or state['last_buy_day'] == day:
        return result
    if state['pending'] or _IMPL.chassis.players[seat].get('pending'):
        return result
    orders = result.get('market', [])
    # Avoid joint funding obligations; parent sales remain unchanged.
    if len(orders) > 8 or any(o and o[0] != 'SELL' and o[:2] != ['BUY_SEED', 'WHEAT'] for o in orders):
        state['gate_orders'] += 1
        return result
    native_seed_cost = sum(10 * max(0, int(o[2])) for o in orders if len(o) >= 3 and o[:2] == ['BUY_SEED', 'WHEAT'])
    shops = obs['town']['unlocked_shops']
    daily_demand = 1 + 6 * (2 * shops.count('PET_CAFE') + shops.count('FARMERS_MARKET'))
    if daily_demand < 25:
        state['gate_demand'] += 1
        return result
    route = _IMPL.chassis.players[seat]['route']
    nxt = _IMPL.chassis.routes[route][step + 1]
    next_commands = [nxt.get('farmer') or ['PASS'], *(nxt.get('hands') or [])]
    projected_positions = []
    for pos, cmd in zip(positions, commands):
        dx, dy = _CP0_MOVES.get(cmd[0], (0, 0))
        projected_positions.append((max(0, min(9, pos[0] + dx)), max(0, min(9, pos[1] + dy))))
    after_field = None
    for actor, (xy, cmd) in enumerate(zip(projected_positions, next_commands)):
        x, y = xy
        if cmd != ['PLANT', 'WHEAT']: continue
        if after_field is None:
            after_field = _c143_after_field(obs, result)
            state['post_field_checks'] += 1
        if after_field['tiles'][y][x] is not None:
            state['gate_occupied'] += 1
            continue
        if farm['tiles'][y][x] is not None:
            state['post_field_empty_candidates'] += 1
        certificate = _c143_certificate(obs, projected_positions, xy, day, state)
        if certificate is None:
            state['gate_route'] += 1
            continue
        state['certified_routes'] += 1
        # WHEAT starts at one unit. Before this certified native HARVEST, each
        # distinct productive WATER can add at most two units even if fertilized.
        # This is a route-derived upper bound, not an empirical average.
        foregone_wheat = int(certificate['foregone_wheat_upper'])
        state['foregone_wheat_upper_total'] += foregone_wheat
        state['foregone_wheat_upper_five'] += int(foregone_wheat == 5)
        state['foregone_wheat_upper_six'] += int(foregone_wheat == 6)
        # Include visible competing crops, 32 speculative extra competing units,
        # and all own commitments. Two harvested units are the conservative yield.
        supply = _c143_public_supply(obs, day + 3) + 32 + 4 * (len(state['plans']) + 1)
        known_days = max(0, (certificate['step'] - step) // 24)
        inventory = obs['market']['inventory']['CARROT'] + supply - known_days * daily_demand
        value = sum(_r37_market_price('CARROT', inventory + q) for q in range(2))
        grain_quote = max(obs['market']['prices']['WHEAT'], _r37_market_price('WHEAT', obs['market']['inventory']['WHEAT'] - 12)) + 5
        cost = 20 + foregone_wheat * grain_quote
        # Buy the full route-certified foregone-WHEAT upper bound now. This keeps
        # c138's feed/liquidity protection while removing only the impossible six-unit
        # assumption. The unused native wheat seed still receives no value credit.
        if value < cost + 100 or farm['money'] < native_seed_cost + cost + 3000:
            state['gate_value_or_cash'] += 1
            continue
        stock = projected_shed(result, FarmView(obs))
        carried = sum(sum(inv.values()) for inv in private['inventories'])
        if sum(stock.values()) + carried + foregone_wheat > 90: continue
        if result is parent: result = copy.deepcopy(parent)
        certificate['plant_step'] = step + 1
        wheat_after = max(0, stock.get('WHEAT', 0) - sum(max(0, int(o[2])) for o in orders if o[:2] == ['SELL', 'WHEAT'])) + foregone_wheat
        result['market'] += [['BUY_SEED', 'CARROT', 1], ['BUY_PRODUCT', 'WHEAT', foregone_wheat]]
        state['pending'] = {'plant_step': step + 1, 'actor': actor, 'xy': xy,
                            'seed_before': private['seeds'].get('CARROT', 0),
                            'wheat_after_purchase': wheat_after, 'certificate': certificate}
        state['requests'] += 1; state['last_buy_day'] = day
        state['forecast_gain'] += value - cost
        break
    return result


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    state = _C143_STATES.get(seat)
    if state is None or step <= state['last']:
        state = _C143_STATES[seat] = {'last': -1, 'pending': None, 'plans': [], 'requests': 0,
            'last_buy_day': -1, 'conversions': 0, 'confirmed_plants': 0, 'harvest_units_requested': 0, 'forecast_gain': 0,
            'purchase_or_route_errors': 0, 'harvest_errors': 0, 'errors': 0,
            'gate_orders': 0, 'gate_demand': 0, 'gate_route': 0, 'certified_routes': 0, 'gate_value_or_cash': 0,
            'post_field_checks': 0, 'post_field_empty_candidates': 0, 'gate_occupied': 0,
            'certificate_replaced': 0, 'certificate_harvest': 0, 'certificate_dry': 0, 'certificate_expired': 0,
            'foregone_wheat_upper_total': 0, 'foregone_wheat_upper_five': 0, 'foregone_wheat_upper_six': 0}
    state['last'] = step
    parent = _C143_PARENT(observation, configuration); result = parent
    try:
        if configuration is None or all(configuration.get(k, v) == v for k, v in
            [('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100), ('maxMarketOrdersPerTurn', 10)]):
            result = _c143_control(observation, parent, state)
    except Exception: state['errors'] += 1
    _C143_REPORT.clear(); _C143_REPORT.update(getattr(_C143_PARENT, 'telemetry', {}))
    _C143_REPORT.update({'carrot_rotation_' + k: v for k, v in state.items() if isinstance(v, int) and k not in ('last', 'last_buy_day')})
    return result


agent.telemetry = _C143_REPORT
agent = globals().pop('agent')
