# o212_fsv5_r151 (Claude/o-series, 2026-09-15). lynnsakurai Farming Score V5 block ported verbatim onto the o199c stack: r151 exact dawn-overflow recovery (insertion-order ledger) - replaces the r148 approximation
# Source lines 3417-3621; upstream notices retained.



# EXP-284: insertion-ledger dawn overflow recovery.
# The replay JSON canonicalizes dictionary keys, while the engine deposits each
# worker's inventory in the original insertion order.  Reconstruct that order
# from consecutive observations (one unit action can introduce at most one new
# item per worker), then sell only a prefix of the exact discarded suffix whose
# replacement proves the complete next-day shed vector invariant.

_R151_PARENT = agent
_R151_STATES = {}
_R151_REPORT = {}


def _r151_same_stock(left, right):
    return all(
        int(left.get(item, 0)) == int(right.get(item, 0))
        for item in set(left) | set(right)
    )


def _r151_empty(inventories):
    return all(
        not any(int(quantity) > 0 for quantity in inventory.values())
        for inventory in inventories
    )


def _r151_sync_orders(state, inventories):
    previous = state.get('orders', [])
    current = []
    for actor, inventory in enumerate(inventories):
        positive = {
            item for item, quantity in inventory.items() if int(quantity) > 0
        }
        order = [
            item for item in (previous[actor] if actor < len(previous) else [])
            if item in positive
        ]
        added = [item for item in positive if item not in order]
        if len(added) > 1:
            state['trusted'] = False
            _R151_REPORT['overflow_order_ambiguities'] += 1
        order.extend(added)
        current.append(order)
    state['orders'] = current


def _r151_project_orders(orders, inventories):
    projected = []
    for actor, inventory in enumerate(inventories):
        positive = {
            item for item, quantity in inventory.items() if int(quantity) > 0
        }
        order = [
            item for item in (orders[actor] if actor < len(orders) else [])
            if item in positive
        ]
        added = [item for item in positive if item not in order]
        # A single unit command cannot legitimately introduce two item kinds.
        if len(added) > 1:
            return None
        order.extend(added)
        if set(order) != positive:
            return None
        projected.append(order)
    return projected


def _r151_delivery(stock, inventories, orders, capacity=100):
    result = dict(stock)
    discarded = []
    if orders is None or len(orders) != len(inventories):
        return None, None
    for inventory, order in zip(inventories, orders):
        positive = {
            item for item, quantity in inventory.items() if int(quantity) > 0
        }
        if set(order) != positive:
            return None, None
        for item in order:
            quantity = max(0, int(inventory.get(item, 0)))
            room = max(0, capacity - sum(result.values()))
            accepted = min(quantity, room)
            result[item] = result.get(item, 0) + accepted
            discarded.extend([item] * (quantity - accepted))
    return result, discarded


def _r151_recover_overflow(observation, action, state):
    step = int(observation['step'])
    if (step % 24 != 23 or step > 695 or not state.get('trusted') or
            state.get('disabled')):
        return action
    orders = action.get('market') or []
    if len(orders) >= 10 or not _r97_budget(observation, orders):
        return action
    _, private = _r127_fields(observation, action)
    inventory_orders = _r151_project_orders(
        state.get('orders', []), private['inventories']
    )
    if inventory_orders is None:
        _R151_REPORT['overflow_projection_ambiguities'] += 1
        return action
    stock, _, _ = _r97_market_stock(private['shed'], orders)
    original, discarded = _r151_delivery(
        stock, private['inventories'], inventory_orders
    )
    if original is None or not discarded:
        return action

    released = {}
    best = None
    for item in discarded:
        released[item] = released.get(item, 0) + 1
        if (item not in observation['market']['prices'] or
                released[item] > stock.get(item, 0) or
                len(orders) + len(released) > 10):
            break
        proposed = list(orders) + [
            ['SELL', product, quantity]
            for product, quantity in released.items()
        ]
        after_market, _, _ = _r97_market_stock(private['shed'], proposed)
        final, remaining_loss = _r151_delivery(
            after_market, private['inventories'], inventory_orders
        )
        if final is not None and _r151_same_stock(original, final):
            exposure = sum(
                quantity * int(observation['market']['prices'][product])
                for product, quantity in released.items()
            )
            best = proposed, dict(released), dict(final), len(remaining_loss), exposure
    if best is None or best[4] < 25:
        return action

    proposed, released, final, remaining_loss, exposure = best
    state['pending'] = (step + 1, final)
    _R151_REPORT['overflow_turns'] += 1
    _R151_REPORT['overflow_units_reclaimed'] += sum(released.values())
    _R151_REPORT['overflow_quote_exposure'] += exposure
    _R151_REPORT['overflow_units_still_discarded'] += remaining_loss
    result = copy.deepcopy(action)
    result['market'] = proposed
    return result


def agent(observation, configuration=None):
    result = _R151_PARENT(observation, configuration)
    try:
        player = int(observation['player'])
        step = int(observation.get(
            'step', observation['day'] * 24 + observation['hour']
        ))
        inventories = observation['private']['inventories']
        state = _R151_STATES.get(player)
        consecutive = state is not None and step == state.get('step', -2) + 1
        if state is None or step <= state.get('step', -1) or not consecutive:
            trusted = _r151_empty(inventories)
            state = _R151_STATES[player] = {
                'step': step,
                'orders': [],
                'trusted': trusted,
                'disabled': False,
            }
            _R151_REPORT.update(
                overflow_turns=0,
                overflow_units_reclaimed=0,
                overflow_quote_exposure=0,
                overflow_units_still_discarded=0,
                overflow_contract_checks=0,
                overflow_contract_errors=0,
                overflow_tracking_resets=0,
                overflow_order_ambiguities=0,
                overflow_projection_ambiguities=0,
                overflow_errors=0,
            )
        else:
            state['step'] = step

        pending = state.pop('pending', None)
        if pending:
            if step == pending[0] and _r151_same_stock(
                    observation['private']['shed'], pending[1]):
                _R151_REPORT['overflow_contract_checks'] += 1
            else:
                _R151_REPORT['overflow_contract_errors'] += 1
                state['disabled'] = True

        if step % 24 == 0 and _r151_empty(inventories):
            state['orders'] = [[] for _ in inventories]
            state['trusted'] = not state.get('disabled', False)
            _R151_REPORT['overflow_tracking_resets'] += 1
        _r151_sync_orders(state, inventories)

        if _r132_standard(configuration):
            result = _r151_recover_overflow(observation, result, state)
    except Exception:
        _R151_REPORT['overflow_errors'] = _R151_REPORT.get('overflow_errors', 0) + 1
    _R151_REPORT.update(getattr(_R151_PARENT, 'telemetry', {}))
    return result


agent.telemetry = _R151_REPORT
agent = globals().pop('agent')
