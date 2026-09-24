"""Preserve c371 and use the public Clone Race Horizon's existing 48-turn bound."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = 'e23cc84b4b801a40f92e209f43e5c9ad18e825e54dd6ed5527ea8f57b1cef12e'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    args = ap.parse_args()
    parent = (ROOT/'agent/c371_resource_budget.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    suffix = '''

# c372: the public Clone Race Horizon's existing bounded reservation horizon.
# Reference: https://www.kaggle.com/code/nihilisticneuralnet/kaggriculture-clone-race-horizon
# Reference SHA 0070f9e125902d690995acbbb0df1e3f46185a560771c0843d074f315345c778.
# Original controller/Apache attribution retained above; integration Taeyang/Codex.
# Change only default40 -> existing maximum48; preserve gates and every other rule.
_C372_PARENT = agent
_C372_ENABLED = __ON__
if _C365_CA_NS['V9_RACE_DEFAULT'] != 40 or _C365_CA_NS['V9_RACE_MAX'] != 48:
    raise RuntimeError('c372 parent race contract drift')
if _C372_ENABLED:
    _C365_CA_NS['V9_RACE_DEFAULT'] = 48
_C372_REPORT = {}

def agent(observation, configuration=None):
    action = _C372_PARENT(observation, configuration)
    _C372_REPORT.clear()
    _C372_REPORT.update(_C371_REPORT)
    _C372_REPORT.update(_C365_CA_NS['_V9_RACE_REPORT'])
    _C372_REPORT['race_default'] = _C365_CA_NS['V9_RACE_DEFAULT']
    return action

agent.telemetry = _C372_REPORT
kaggle_submission_agent = agent
c372_submission_agent = agent
'''.replace('__ON__', str(not args.disabled))
    data = parent.rstrip() + suffix.encode('utf8')
    compile(data, str(args.out), 'exec')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    main()
