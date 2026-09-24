"""Add a farmer wheat pickup top-up to frozen o301: carry enough wheat for the tape's remaining FEEDs."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = '383d6fef780361b291f36428643e56739c5d5553c9d9364c9b27ac6e9e9db720'
WRAPPER = r'''

# o302: farmer feed pickup top-up. In the route-0 family the day-26 tape has
# the farmer pick up one wheat at h1 but FEED at h5 and h17; when the h17 goose
# is still unfed the FEED fails and the goose escapes (17/118 live games, same
# for public-lineage rivals). When the farmer's PICKUP WHEAT carries fewer units
# than its remaining tape FEEDs today, raise the pickup by the deficit, bounded
# by shed stock left after every other pickup planned for the rest of the day.
# Hands are untouched; unused units return to the shed at midnight.
_O302_ENABLED = __ON__
_O302_PARENT = agent
_O302_REPORT = {}

def _o302_frames(player, step):
    route = _C358_IMPL.chassis.players[player]['route']
    tape = _C358_IMPL.chassis.routes[route]
    return [tape[t] if isinstance(tape[t], dict) else {} for t in range(step + 1, min(len(tape), (step // 24 + 1) * 24))]

def _o302_topup(observation, action):
    farmer = list(action.get('farmer') or ['PASS'])
    if farmer[0] != 'PICKUP' or len(farmer) < 2 or farmer[1] != 'WHEAT':
        return action
    step = int(observation['step']); player = int(observation['player'])
    frames = _o302_frames(player, step)
    feeds = sum(1 for f in frames if (f.get('farmer') or ['PASS'])[0] == 'FEED')
    carried = int((observation['private'].get('inventories') or [{}])[0].get('WHEAT', 0))
    quantity = max(1, int(farmer[2])) if len(farmer) >= 3 else 1
    deficit = feeds - carried - quantity
    if deficit <= 0:
        return action
    shed = int((observation['private'].get('shed') or {}).get('WHEAT', 0))
    others = 0
    for c in (action.get('hands') or []):
        if c and c[0] == 'PICKUP' and len(c) >= 2 and c[1] == 'WHEAT':
            others += max(1, int(c[2])) if len(c) >= 3 else 1
    for f in frames:
        for c in [f.get('farmer')] + list(f.get('hands') or []):
            if c and c[0] == 'PICKUP' and len(c) >= 2 and c[1] == 'WHEAT':
                others += max(1, int(c[2])) if len(c) >= 3 else 1
    extra = min(deficit, shed - quantity - others)
    if extra <= 0:
        _O302_REPORT['topup_declined'] += 1
        return action
    action = dict(action)
    action['farmer'] = ['PICKUP', 'WHEAT', quantity + extra]
    _O302_REPORT['topups'] += 1
    _O302_REPORT['topup_units'] += extra
    return action

def agent(observation, configuration=None):
    action = _O302_PARENT(observation, configuration)
    if int(observation['step']) == 0:
        _O302_REPORT.clear()
        _O302_REPORT.update(topups=0, topup_units=0, topup_declined=0)
    _O302_REPORT.update(_O301_REPORT)
    if not _O302_ENABLED:
        return action
    return _o302_topup(observation, action)

agent.telemetry = _O302_REPORT
kaggle_submission_agent = agent
o302_submission_agent = agent
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    args = ap.parse_args()
    parent = (ROOT / 'agent/o301_hire_floor.py').read_bytes()
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
