"""Isolate the pinned public V54 V219 maintenance-day labor saving on c368."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = 'fed4a96fafe96a80a37ec480fcf12de8ded716517fd4226d2b0ed4bcaeeab1b0'
DONOR_SHA = '5fbb75c9c40e6d9e26d95272ace47329b1ca319b3b2118232404de30806e7e9c'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--disabled', action='store_true')
    args = parser.parse_args()
    parent = (ROOT/'agent/c368_terminal_seed_budget.py').read_bytes()
    donor = (ROOT/'state/public_league/sources'/f'{DONOR_SHA}.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    assert hashlib.sha256(donor).hexdigest() == DONOR_SHA
    source = donor.decode('utf-8')
    layer = source[source.index('V13V_SKIP_DAYS ='):source.index('_V13V_PARENT = agent')]
    suffix = '''

# c370: V219 maintenance-day labor saving from public V54, Apache-2.0.
# Donor: Ahmed Berat Ozer, kaggle.com/code/ahmedberatozer/kaggriculture-v54-productive-wheat-and-patient
# Original public source and attribution remain in the pinned League archive.
# Donor SHA __SHA__; original skip days (19,21,23) and safety check unchanged.
# Isolated integration on c368: Taeyang/Codex, 2026-09-21.
_C370_ENABLED = __ENABLED__
_C370_PARENT = agent
if _C370_ENABLED:
    if '_V13V_ORIG_REQUEST' in _C365_CA_NS:
        raise RuntimeError('c370 parent already has V219SKIP')
    if _C365_CA_NS['_v219_request'].__globals__ is not _C365_CA_NS:
        raise RuntimeError('c370 V219 namespace contract drift')
    exec(compile(__LAYER__, '<c370-v219-maintenance>', 'exec'), _C365_CA_NS)
    _C370_REPORT = _C365_CA_NS['_V13V_REPORT']
else:
    _C370_REPORT = dict(v_skipped=0, v_blocked=0, v_errors=0)

def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _C370_REPORT:
            _C370_REPORT[key] = 0
    return _C370_PARENT(observation, configuration)

agent.telemetry = _C370_REPORT
kaggle_submission_agent = agent
c370_submission_agent = agent
'''.replace('__SHA__', DONOR_SHA).replace('__ENABLED__', str(not args.disabled)).replace('__LAYER__', repr(layer))
    data = parent.rstrip() + suffix.encode('utf-8')
    compile(data, str(args.out), 'exec')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    main()
