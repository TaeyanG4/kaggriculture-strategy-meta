# SPDX-License-Identifier: Apache-2.0
"""Reassign an already-funded o182 fertilizer tour using exact spawn timing.

The parent decides whether to hire, how much fertilizer to buy, how many hands
to hire, and which exact crop tiles to service.  This overlay changes none of
those economic decisions.  After the parent has created a fresh r51 ``pending``
plan, it may only reorder and reassign that fixed target multiset while keeping
each hand's path length and fertilizer quantity unchanged.

The search starts each new hand at its deterministic post-move HIRE spawn and
at step + 2, after its next-turn pickup.  A replacement is installed atomically
only if every target's existing r51 forecast gain is non-decreasing and at
least one target gains an additional unit.  Any malformed state, incomplete
route, equality, or exception retains the parent's action and pending plan.
"""
import copy as _c159_copy


_C159_PARENT = agent
_C159_STATES = {}
_C159_REPORT = {}
_C159_ACCESS = ((4, 4), (5, 4), (4, 5), (5, 5))
_C159_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1),
               "EAST": (1, 0), "WEST": (-1, 0)}
_C159_CROPS = ("WHEAT", "CARROT")
_C159_MAX_WORKERS = 2
_C159_MAX_TARGETS = 16
_C159_BEAM_WIDTH = 128
del agent


def _c159_new_state():
    return {
        "last": -1,
        "pending_seen": 0,
        "contract_declines": 0,
        "no_gain_declines": 0,
        "searches": 0,
        "search_expansions": 0,
        "reassignments": 0,
        "changed_worker_paths": 0,
        "forecast_extra_units": 0,
        "forecast_value_gain": 0,
        "errors": 0,
    }


def _c159_standard(observation, configuration):
    farm = observation["farms"][int(observation["player"])]
    if len(farm.get("tiles", ())) != 10:
        return False
    if configuration is None:
        return True
    return all(configuration.get(key, expected) == expected for key, expected in (
        ("boardSize", 10), ("turnsPerDay", 24), ("shedCapacity", 100),
        ("maxMarketOrdersPerTurn", 10), ("episodeSteps", 720)))


def _c159_commands(action, count):
    commands = [list(action.get("farmer") or ["PASS"])]
    commands.extend(list(command or ["PASS"])
                    for command in (action.get("hands") or []))
    commands.extend([["PASS"] for _ in range(max(0, count - len(commands)))])
    return commands[:count]


def _c159_spawn_starts(observation, action, worker_count):
    """Return exact (first post-pickup action step, HIRE spawn) pairs."""
    farm = observation["farms"][int(observation["player"])]
    positions = [list(farm["farmer"])] + [list(pos) for pos in farm.get("hands", [])]
    for actor, command in enumerate(_c159_commands(action, len(positions))):
        if command and command[0] in _C159_MOVES:
            dx, dy = _C159_MOVES[command[0]]
            positions[actor][0] = max(0, min(9, positions[actor][0] + dx))
            positions[actor][1] = max(0, min(9, positions[actor][1] + dy))
    starts = []
    for order in action.get("market") or []:
        if order and order[0] == "HIRE":
            chosen = min(
                _C159_ACCESS,
                key=lambda pos: (sum(tuple(current) == pos for current in positions),
                                 _C159_ACCESS.index(pos)),
            )
            positions.append(list(chosen))
            starts.append((int(observation["step"]) + 2, tuple(chosen)))
    if len(starts) != worker_count:
        raise ValueError("HIRE count differs from pending worker count")
    return starts


def _c159_pending_contract(observation, action, pending):
    if not isinstance(pending, dict) or not 1 <= len(pending) <= _C159_MAX_WORKERS:
        raise ValueError("pending worker count outside contract")
    farm = observation["farms"][int(observation["player"])]
    actors = sorted(pending)
    expected = list(range(len(farm.get("hands", [])) + 1,
                          len(farm.get("hands", [])) + 1 + len(actors)))
    if actors != expected:
        raise ValueError("pending actors are not the newly hired contiguous suffix")
    plans = []
    seen = set()
    for actor in actors:
        plan = pending[actor]
        if not isinstance(plan, dict) or plan.get("loaded") is not False:
            raise ValueError("pending plan is not a fresh unloaded plan")
        path = plan.get("path")
        quantity = plan.get("quantity")
        if not isinstance(path, list) or isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("pending path or quantity has invalid type")
        if quantity != len(path) or quantity <= 0:
            raise ValueError("pending fertilizer quantity differs from path length")
        normalized = []
        for row in path:
            if not isinstance(row, (list, tuple)) or len(row) != 4:
                raise ValueError("invalid target tuple")
            x, y, crop, birth = row
            if (isinstance(x, bool) or isinstance(y, bool) or isinstance(birth, bool) or
                    not isinstance(x, int) or not isinstance(y, int) or
                    not isinstance(birth, int) or crop not in _C159_CROPS or
                    not (0 <= x < 10 and 0 <= y < 10)):
                raise ValueError("invalid target fields")
            target = (x, y, crop, birth)
            if target in seen:
                raise ValueError("duplicate fertilizer target")
            seen.add(target)
            normalized.append(target)
        plans.append(normalized)
    if not 1 <= len(seen) <= _C159_MAX_TARGETS:
        raise ValueError("target count outside contract")

    market = action.get("market") or []
    hires = [order for order in market if order and order[0] == "HIRE"]
    if len(hires) != len(plans) or len(market) < len(plans) + 1:
        raise ValueError("market HIRE contract failed")
    if any(order != ["HIRE"] for order in market[-len(plans):]):
        raise ValueError("tour HIREs are not the exact market suffix")
    purchase = market[-len(plans) - 1]
    if (not isinstance(purchase, list) or len(purchase) < 3 or
            purchase[:2] != ["BUY_PRODUCT", "FERTILIZER"] or
            isinstance(purchase[2], bool) or not isinstance(purchase[2], int) or
            purchase[2] < sum(len(path) for path in plans)):
        raise ValueError("tour fertilizer purchase contract failed")
    return actors, plans, seen


def _c159_targets(observation, target_rows):
    seat = int(observation["player"])
    day = int(observation["step"]) // 24
    native = _IMPL.chassis.players.get(seat)
    if not isinstance(native, dict) or native.get("route") not in _IMPL.chassis.routes:
        raise ValueError("native route unavailable")
    planned = _v219_native_day(native, day)
    expected = max((len(action.get("hands", [])) for action in planned), default=0)
    forecast = _r51_input_forecast(observation, native["route"], expected)
    if not isinstance(forecast, dict):
        raise ValueError("input forecast unavailable")
    result = {}
    for row in target_rows:
        x, y, crop, birth = row
        target = forecast.get((x, y))
        if (not isinstance(target, dict) or target.get("crop") != crop or
                target.get("birth") != birth):
            raise ValueError("pending target no longer matches forecast")
        result[row] = target
    if len(result) != len(target_rows):
        raise ValueError("forecast target union differs")
    return result


def _c159_evaluate(paths, starts, targets, prices, day):
    close = day * 24 + 23
    gains = {}
    finishes = []
    for path, (ready, start) in zip(paths, starts):
        now = ready
        position = start
        for row in path:
            x, y, crop, _ = row
            arrival = now + abs(position[0] - x) + abs(position[1] - y)
            gain = int(_r51_input_gain(targets[row], arrival, day))
            gains[row] = max(0, gain)
            now = arrival + 1
            position = (x, y)
        finishes.append(now)
    units = {crop: sum(gain for row, gain in gains.items() if row[2] == crop)
             for crop in _C159_CROPS}
    return {
        "gains": gains,
        "units": units,
        "total": sum(units.values()),
        "value": sum(gain * prices[row[2]] for row, gain in gains.items()),
        "finishes": tuple(finishes),
        "complete": all(finish <= close for finish in finishes),
    }


def _c159_upper_bound(state, rows, targets, prices, day, quotas):
    gross, _, positions, nows, paths, _, remaining = state
    optimistic = gross
    for index in remaining:
        row = rows[index]
        x, y, crop, _ = row
        possible = []
        for actor in range(len(paths)):
            if len(paths[actor]) < quotas[actor]:
                arrival = nows[actor] + abs(positions[actor][0] - x) + abs(positions[actor][1] - y)
                possible.append(max(0, int(_r51_input_gain(targets[row], arrival, day))))
        if possible:
            optimistic += max(possible) * prices[crop]
    return optimistic


def _c159_search(rows, quotas, starts, targets, prices, day):
    slots = [actor for depth in range(max(quotas))
             for actor, quota in enumerate(quotas) if depth < quota]
    empty_paths = tuple(() for _ in quotas)
    state = (0, 0, tuple(start for _, start in starts),
             tuple(ready for ready, _ in starts), empty_paths,
             tuple(0 for _ in rows), tuple(range(len(rows))))
    beam = [state]
    expansions = 0
    close = day * 24 + 23
    for actor in slots:
        expanded = []
        for gross, total, positions, nows, paths, gains, remaining in beam:
            for target_index in remaining:
                row = rows[target_index]
                x, y, crop, _ = row
                arrival = nows[actor] + abs(positions[actor][0] - x) + abs(positions[actor][1] - y)
                if arrival >= close:
                    continue
                gain = max(0, int(_r51_input_gain(targets[row], arrival, day)))
                new_positions = list(positions); new_positions[actor] = (x, y)
                new_nows = list(nows); new_nows[actor] = arrival + 1
                new_paths = [tuple(path) for path in paths]
                new_paths[actor] = new_paths[actor] + (row,)
                new_gains = list(gains); new_gains[target_index] = gain
                new_remaining = tuple(index for index in remaining if index != target_index)
                expanded.append((gross + gain * prices[crop], total + gain,
                                 tuple(new_positions), tuple(new_nows), tuple(new_paths),
                                 tuple(new_gains), new_remaining))
                expansions += 1
        if not expanded:
            return None, expansions
        expanded.sort(key=lambda candidate: (
            -_c159_upper_bound(candidate, rows, targets, prices, day, quotas),
            -candidate[0], -candidate[1], max(candidate[3]), sum(candidate[3]),
            candidate[4],
        ))
        beam = expanded[:_C159_BEAM_WIDTH]
    complete = [candidate for candidate in beam if not candidate[6]]
    if not complete:
        return None, expansions
    complete.sort(key=lambda candidate: (
        -candidate[0], -candidate[1], max(candidate[3]), sum(candidate[3]), candidate[4]))
    return [list(path) for path in complete[0][4]], expansions


def agent(observation, configuration=None):
    step = int(observation.get("step", 0))
    seat = int(observation.get("player", 0))
    state = _C159_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _C159_STATES[seat] = _c159_new_state()
    state["last"] = step
    parent_action = _C159_PARENT(observation, configuration)
    action_snapshot = _c159_copy.deepcopy(parent_action)
    try:
        if not _c159_standard(observation, configuration):
            raise StopIteration
        input_state = _R51_INPUT_STATES.get(seat)
        pending = input_state.get("pending") if isinstance(input_state, dict) else None
        if not pending:
            raise StopIteration
        state["pending_seen"] += 1
        actors, parent_paths, target_rows = _c159_pending_contract(
            observation, parent_action, pending)
        targets = _c159_targets(observation, target_rows)
        starts = _c159_spawn_starts(observation, parent_action, len(actors))
        day = step // 24
        prices = {crop: max(1, int(observation["market"]["prices"][crop]) - 2)
                  for crop in _C159_CROPS}
        baseline = _c159_evaluate(parent_paths, starts, targets, prices, day)
        state["searches"] += 1
        rows = tuple(sorted(target_rows))
        replacement_paths, expansions = _c159_search(
            rows, tuple(len(path) for path in parent_paths), starts, targets, prices, day)
        state["search_expansions"] += expansions
        if replacement_paths is None:
            state["no_gain_declines"] += 1
            raise StopIteration
        replacement = _c159_evaluate(replacement_paths, starts, targets, prices, day)
        if (not replacement["complete"] or
                set(row for path in replacement_paths for row in path) != target_rows or
                any(len(new) != len(old) for new, old in zip(replacement_paths, parent_paths)) or
                any(replacement["gains"].get(row, -1) < baseline["gains"].get(row, -1)
                    for row in target_rows) or
                not any(replacement["gains"].get(row, 0) > baseline["gains"].get(row, 0)
                        for row in target_rows) or
                replacement["value"] <= baseline["value"]):
            state["no_gain_declines"] += 1
            raise StopIteration

        new_pending = _c159_copy.deepcopy(pending)
        for actor, path in zip(actors, replacement_paths):
            if new_pending[actor]["quantity"] != len(path):
                raise ValueError("replacement changed worker fertilizer quantity")
            new_pending[actor]["path"] = list(path)
        if parent_action != action_snapshot:
            raise ValueError("parent action mutated during search")
        changed_workers = sum(old != new for old, new in zip(parent_paths, replacement_paths))
        extra_units = replacement["total"] - baseline["total"]
        value_gain = replacement["value"] - baseline["value"]
        # Commit last: all validation and telemetry arithmetic above is complete,
        # so an exception cannot leave a partially rewritten parent plan.
        input_state["pending"] = new_pending
        state["reassignments"] += 1
        state["changed_worker_paths"] += changed_workers
        state["forecast_extra_units"] += extra_units
        state["forecast_value_gain"] += value_gain
    except StopIteration:
        pass
    except (KeyError, TypeError, ValueError, IndexError, OverflowError):
        state["contract_declines"] += 1
    except Exception:
        state["errors"] += 1
    _C159_REPORT.clear()
    _C159_REPORT.update(getattr(_C159_PARENT, "telemetry", {}))
    _C159_REPORT.update({"c159_" + key: value for key, value in state.items()
                         if key != "last"})
    return parent_action


agent.telemetry = _C159_REPORT
agent = globals().pop("agent")
