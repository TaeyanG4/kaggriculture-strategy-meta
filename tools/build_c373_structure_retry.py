"""Build a bounded retry of weed-interrupted opening structures on c371."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = 'e23cc84b4b801a40f92e209f43e5c9ad18e825e54dd6ed5527ea8f57b1cef12e'
WRAPPER = r'''

# c373: preserve the parent's pending BUILD after DIG by consuming the
# same worker's next PASS, before midnight, in the first four days only.
# No additional purchases, workers, land, or speculative future observations.
_C373_ENABLED = __ON__
_C373_PARENT = agent
_C373_ORIGINAL = _C365_CA_NS['Chassis']._weed_repair
_C373_EDITS = {}
_C373_REPORT = {}

def _c373_command(frame, actor):
    if actor == 0:
        return frame.get('farmer') or ['PASS']
    hands = frame.get('hands') or []
    return hands[actor-1] if actor <= len(hands) else None

def _c373_set(frame, actor, command):
    if actor == 0:
        frame['farmer'] = list(command)
    else:
        frame['hands'][actor-1] = list(command)

def _c373_repair(self, action, view, state, route, step):
    if not _C373_ENABLED or not 0 < step < 96:
        return _C373_ORIGINAL(self, action, view, state, route, step)
    tape = self.routes[route]
    units = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    for actor, queue in list(state['pending'].items()):
        if not queue or actor >= len(view.positions) or actor >= len(units):
            continue
        position, retry = queue[0]
        x, y = map(int, view.positions[actor])
        if (tuple(position) != (x, y) or view.tiles[y][x] is not None
                or retry[0] not in ('BUILD_PASTURE', 'BUILD_COOP')
                or units[actor][0] not in ('NORTH', 'SOUTH', 'EAST', 'WEST')):
            continue
        # Move the existing commands intact to their next slots, ending at
        # the first real PASS. Do not cross a hand's daily lifetime boundary.
        end = None
        commands = [list(units[actor])]
        for future in range(step+1, min(len(tape), (step//24+1)*24)):
            command = _c373_command(tape[future], actor)
            if command is None:
                break
            if command == ['PASS']:
                end = future
                break
            commands.append(list(command))
        if end is None:
            _C373_REPORT['no_slack'] += 1
            continue
        for future, command in zip(range(step+1, end+1), commands):
            key = (route, future, actor)
            if key not in _C373_EDITS:
                _C373_EDITS[key] = list(_c373_command(tape[future], actor))
            _c373_set(tape[future], actor, command)
        units[actor] = ['PASS']  # existing queue logic now replays BUILD
        _C373_REPORT['structure_retries'] += 1
        _C373_REPORT['shifted_commands'] += len(commands)
    action['farmer'], action['hands'] = units[0], units[1:]
    return _C373_ORIGINAL(self, action, view, state, route, step)

if _C373_ENABLED:
    _C365_CA_NS['Chassis']._weed_repair = _c373_repair

def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for (route, future, actor), command in _C373_EDITS.items():
            _c373_set(_C358_IMPL.chassis.routes[route][future], actor, command)
        _C373_EDITS.clear()
        _C373_REPORT.clear()
        _C373_REPORT.update(structure_retries=0, shifted_commands=0, no_slack=0)
    action = _C373_PARENT(observation, configuration)
    _C373_REPORT.update(_C371_REPORT)
    return action

agent.telemetry = _C373_REPORT
kaggle_submission_agent = agent
c373_submission_agent = agent
'''

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--disabled', action='store_true')
    args = parser.parse_args()
    parent = (ROOT/'agent/c371_resource_budget.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    data = parent.rstrip() + WRAPPER.replace('__ON__', str(not args.disabled)).encode()
    compile(data, str(args.out), 'exec')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    main()
