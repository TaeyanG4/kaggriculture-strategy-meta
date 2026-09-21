# SPDX-License-Identifier: Apache-2.0
"""Execute certified own-route crop sequences; the bank is embedded at build.

Profiles are fixed synthesis weights, not forecasts. Replaces funded d11 berry
seed purchases only. No added movement, land, hiring, fertilizer or sale orders.
Unsupported calendars retain the parent. Observed weeds/missed plants receive
bounded repairs at existing production slots, counted separately from the plan.
"""
import copy as _c321_copy
import hashlib as _c321_hashlib
import json as _c321_json

_C321_PARENT = agent
_C321_ON = True
_C321_STATES = {}
_C321_REPORT = {}
_C321_OPS = {'WATER', 'HARVEST', 'FERTILIZE', 'DIG'}
del agent


def _c321_signature(obs, action, xy, start):
    visits = _ca_visits(obs, action, xy, 718, start=start)
    first = next(((t, i) for t, i, op in visits if t == start and op == 'PLANT'), None)
    if first is None:
        return None
    t, actor = first
    native = _ca_tape(int(obs['player']), t)
    commands = [native.get('farmer') or ['PASS'], *(native.get('hands') or [])]
    if actor >= len(commands) or commands[actor] != ['PLANT', 'STRAWBERRY']:
        return None
    end = next((t for t, i, op in visits if t > start and op in ('PLANT', 'BUILD_COOP', 'BUILD_PASTURE')), 719)
    events = [(start, -1, ['PLANT', 'STRAWBERRY'])] + [(t, i, [op]) for t, i, op in visits if start < t < end and op in _C321_OPS]
    sid = _c321_hashlib.sha256(_c321_json.dumps([start, end, events], separators=(',', ':')).encode()).hexdigest()[:16]
    return (sid, actor) if sid in _C321_BANK else None


def _c321_buy(obs, action, st):
    step = int(obs['step']); seat = int(obs['player'])
    if not 264 <= step < 288:
        return
    market = action.get('market') or []
    orders = [k for k, o in enumerate(market) if o[:2] == ['BUY_SEED', 'STRAWBERRY'] and o[2] > 0]
    if len(orders) != 1:
        return
    route = _IMPL.chassis.players[seat]['route']
    catalogue = _C321_CATALOGUE.get(str(route), [])
    if not catalogue:
        st['counts']['unsupported_route'] += 1
        return
    cmds = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    # Existing berry seeds fund earlier untouched plants; do not sell their plan.
    skip = max(0, int(obs['private']['seeds'].get('STRAWBERRY', 0)) - sum(c == ['PLANT', 'STRAWBERRY'] for c in cmds))
    upcoming = [(start, tuple(xy)) for start, xy in catalogue if start > step and tuple(xy) not in st['lanes']]
    upcoming.sort()
    upcoming = upcoming[skip:]
    index = orders[0]; n = int(market[index][2])
    selected = []; pack = {}
    for start, xy in upcoming[:n]:
        cert = _c321_signature(obs, action, xy, start)
        if cert is None:
            st['counts']['unsupported_calendar'] += 1
            break
        sid, actor = cert
        plan = _C321_BANK[sid]
        for crop, q in plan['seeds'].items():
            pack[crop] = pack.get(crop, 0) + q
        selected.append((xy, sid, actor))
    if not selected:
        return
    replacement = [['BUY_SEED', crop, q] for crop, q in sorted(pack.items()) if q]
    if n > len(selected):
        replacement.append(['BUY_SEED', 'STRAWBERRY', n - len(selected)])
    if len(market) - 1 + len(replacement) > 10:
        st['counts']['order_cap_declines'] += 1
        return
    # Confirmation must not be confused with simultaneous parent planting or
    # another same-product seed purchase. Leave those tranches unchanged.
    if any(c and c[0] == 'PLANT' and c[1] in pack for c in cmds) or any(k != index and o and o[0] == 'BUY_SEED' and o[1] in pack for k, o in enumerate(market)):
        st['counts']['seed_conflict_declines'] += 1
        return
    st['pending'] = dict(before={c: int(obs['private']['seeds'].get(c, 0)) for c in pack}, pack=pack, lanes=selected)
    for xy, sid, actor in selected:
        st['lanes'][xy] = dict(sid=sid, actor=actor, funded=False, started=False, crop=None, pending_crop=None, remaining=dict(_C321_BANK[sid]['seeds']), events={r[0]: r for r in _C321_BANK[sid]['trace']})
    action['market'] = market[:index] + replacement + market[index + 1:]
    st['counts']['seed_orders_replaced'] += len(selected)


def _c321_confirm(obs, st):
    farm = obs['farms'][int(obs['player'])]
    for xy, lane in st['lanes'].items():
        request = lane.pop('plant_request', None)
        if request:
            crop, step = request
            tile = farm['tiles'][xy[1]][xy[0]]
            if isinstance(tile, dict) and tile.get('crop') == crop and tile.get('planted_day') == step // 24:
                lane['remaining'][crop] -= 1
                lane['crop'] = crop; lane['pending_crop'] = None; lane['started'] = True
                st['counts']['plants_confirmed'] += 1
            else:
                st['counts']['plants_failed'] += 1
    pending = st.pop('pending', None)
    if not pending:
        return
    seeds = obs['private']['seeds']
    okay = all(int(seeds.get(c, 0)) >= pending['before'][c] + q for c, q in pending['pack'].items())
    if okay:
        for xy, sid, actor in pending['lanes']:
            st['lanes'][xy]['funded'] = True
        st['counts']['funded_lanes'] += len(pending['lanes'])
    else:
        # Do not pretend an emitted buy succeeded or plant with uncertain funds.
        st['counts']['unconfirmed_lanes'] += len(pending['lanes'])


def _c321_field(obs, action, st):
    step = int(obs['step']); seat = int(obs['player'])
    farm = obs['farms'][seat]
    positions = [farm['farmer'], *farm.get('hands', [])]
    cmds = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    available = dict(obs['private']['seeds'])
    targets = {}
    for xy, lane in st['lanes'].items():
        if not lane['funded'] or step not in lane['events']:
            continue
        record = lane['events'][step]
        actor = lane['actor'] if record[1] == -1 else record[1]
        if actor >= len(positions) or actor >= len(cmds) or tuple(positions[actor]) != xy:
            st['counts']['missed_actor_slots'] += 1
            continue
        expected = ['PLANT', 'STRAWBERRY'] if record[1] == -1 else None
        if (expected is not None and cmds[actor] != expected) or (expected is None and (not cmds[actor] or cmds[actor][0] not in _C321_OPS | {'PASS'})):
            st['counts']['parent_conflict_slots'] += 1
            continue
        if positions.count(list(xy)) > 1:
            st['counts']['shared_tile_slots'] += 1
            continue
        targets[actor] = (xy, lane, record)
    # Reserve every untouched same-step plant before new cohort plant requests.
    for actor, cmd in enumerate(cmds):
        if actor not in targets and cmd and cmd[0] == 'PLANT':
            available[cmd[1]] = available.get(cmd[1], 0) - 1
    for actor, (xy, lane, record) in targets.items():
        tile = farm['tiles'][xy[1]][xy[0]]
        chosen = list(record[2])
        if isinstance(tile, dict) and tile.get('kind') not in ('PLANT', 'WEED') or tile == 'LOCKED':
            st['counts']['foreign_tile_slots'] += 1
            continue
        if chosen[0] == 'PLANT':
            lane['pending_crop'] = chosen[1]
        if isinstance(tile, dict) and tile.get('kind') == 'WEED':
            chosen = ['DIG']
        elif tile is None and lane['pending_crop']:
            chosen = ['PLANT', lane['pending_crop']]
        elif tile is None:
            chosen = ['PASS']
        elif tile.get('crop') != lane['crop']:
            st['counts']['foreign_crop_slots'] += 1
            continue
        if isinstance(tile, dict) and tile.get('kind') == 'PLANT':
            if chosen[0] == 'PLANT':
                chosen = ['WATER']
            elif chosen[0] == 'HARVEST' and tile.get('yield_units', 0) <= 0:
                chosen = ['WATER']
        if chosen[0] == 'PLANT':
            crop = chosen[1]
            if available.get(crop, 0) <= 0 or lane['remaining'].get(crop, 0) <= 0:
                chosen = ['PASS']; st['counts']['seed_shortage_slots'] += 1
            else:
                available[crop] -= 1
                lane['pending_crop'] = crop
                # Clear prior-cycle identity; confirmation occurs on observation.
                lane['crop'] = None
                lane['plant_request'] = (crop, step)
        if chosen != list(record[2]):
            st['counts']['repair_slots'] += 1
        cmds[actor] = chosen
        st['counts']['executed_slots'] += 1
    action['farmer'], action['hands'] = cmds[0], cmds[1:]


def agent(observation, configuration=None):
    result = _C321_PARENT(observation, configuration)
    if not _C321_ON:
        return result
    seat = int(observation['player']); step = int(observation['step'])
    st = _C321_STATES.get(seat)
    if st is None or step <= st['last']:
        st = _C321_STATES[seat] = dict(last=-1, lanes={}, counts={k: 0 for k in (
            'unsupported_route', 'unsupported_calendar', 'order_cap_declines', 'seed_conflict_declines',
            'seed_orders_replaced', 'funded_lanes', 'unconfirmed_lanes', 'missed_actor_slots',
            'parent_conflict_slots', 'shared_tile_slots', 'foreign_tile_slots', 'foreign_crop_slots',
            'seed_shortage_slots', 'repair_slots', 'executed_slots', 'plants_confirmed', 'plants_failed', 'errors')})
    st['last'] = step
    try:
        _c321_confirm(observation, st)
        if 264 <= step < 719:
            result = _c321_copy.deepcopy(result)
            _c321_field(observation, result, st)
            _c321_buy(observation, result, st)
    except Exception:
        st['counts']['errors'] += 1
        raise
    finally:
        _C321_REPORT.clear()
        _C321_REPORT.update(getattr(_C321_PARENT, 'telemetry', {}))
        _C321_REPORT.update({'c321_' + k: v for k, v in st['counts'].items()})
    return result


agent.telemetry = _C321_REPORT
agent = globals().pop('agent')
