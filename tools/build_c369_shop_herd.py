"""Reuse the pinned public V54 shop-herd layer on the frozen c368 body."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = 'fed4a96fafe96a80a37ec480fcf12de8ded716517fd4226d2b0ed4bcaeeab1b0'
DONOR_SHA = '5fbb75c9c40e6d9e26d95272ace47329b1ca319b3b2118232404de30806e7e9c'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    a = ap.parse_args()
    body = (ROOT/'agent/c368_terminal_seed_budget.py').read_bytes()
    donor = (ROOT/'state/public_league/sources'/f'{DONOR_SHA}.py').read_bytes()
    assert hashlib.sha256(body).hexdigest() == PARENT_SHA
    assert hashlib.sha256(donor).hexdigest() == DONOR_SHA
    source = donor.decode('utf-8')
    layer = source[source.index('_Y_CFG='):source.index('# V47 attribution')]
    prelude = '''

# c369: shop-aware herd substitution from public V54 (Apache-2.0).
# Original layer: Seyit Kaan Gunes, kaggle.com/code/seyitkaangunes/kaggriculture-2820-score;
# V54 integration: Ahmed Berat Ozer, kaggle.com/code/ahmedberatozer/kaggriculture-v54-productive-wheat-and-patient.
# This isolated composition onto c368: Taeyang/Codex, 2026-09-21.
# Donor SHA: __SHA__. Its thresholds and purchase window are unchanged.
_C369_PARENT = agent
_C369_ENABLED = __ENABLED__
_Y_HOST = _C369_PARENT
projected_shed = _C365_CA_NS['projected_shed']
FarmView = _C365_CA_NS['FarmView']
'''.replace('__SHA__', DONOR_SHA).replace('__ENABLED__', str(not a.disabled))
    suffix = '''

def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _Y_REPORT:
            _Y_REPORT[key] = 0
    if _C369_ENABLED:
        return _y_agent_shopherd(observation, configuration)
    return _C369_PARENT(observation, configuration)

agent.telemetry = _Y_REPORT
kaggle_submission_agent = agent
c369_submission_agent = agent
'''
    data = body.rstrip() + (prelude + layer + suffix).encode('utf-8')
    compile(data, str(a.out), 'exec')
    a.out.parent.mkdir(parents=True, exist_ok=True)
    if a.out.exists():
        raise FileExistsError(a.out)
    a.out.write_bytes(data)
    print(a.out, hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    main()
