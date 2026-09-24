"""Compose isolated public maintenance and fertilizer savings on frozen c369."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = 'e3bc73c98b2ea83f7635653d43c8ed94a2aa118ce6be614a87dca5da841d2682'
V54_SHA = '5fbb75c9c40e6d9e26d95272ace47329b1ca319b3b2118232404de30806e7e9c'
V56_SHA = 'a1ad0fd1d174477ee2cbdd561a812bcb7029647ce34599e79d6b79e9057eff6c'

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    ap.add_argument('--tomato-only', action='store_true')
    args = ap.parse_args()
    parent = (ROOT/'agent/c369_shop_herd.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    sources = []
    for sha in (V54_SHA, V56_SHA):
        data = (ROOT/'state/public_league/sources'/f'{sha}.py').read_bytes()
        assert hashlib.sha256(data).hexdigest() == sha
        sources.append(data.decode('utf8'))
    tomato = sources[0][sources[0].index('V13V_SKIP_DAYS ='):sources[0].index('_V13V_PARENT = agent')]
    fertilizer = sources[1][sources[1].index('_E410_REPORT='):]
    assert fertilizer.count('def e410_agent(') == 1
    suffix = '''

# c371: isolated V54 maintenance-day and V56 harvest-aware fertilizer savings.
# Public donor author Ahmed Berat Ozer; Apache-2.0 attribution retained.
# https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v54-productive-wheat-and-patient
# https://www.kaggle.com/code/ahmedberatozer/kaggriculture-v56-smarter-seeds-and-fertilizer
# V54 SHA __V54__; V56 SHA __V56__.
# Frozen c369 economic/sale layers preserved; donor thresholds unchanged.
# Composition: Taeyang/Codex, 2026-09-22.
_C371_PARENT = agent
_C371_ENABLED = __ON__
_C371_FERTILIZER = __FERT__
_C371_REPORT = {}
if _C371_ENABLED:
    if '_V13V_ORIG_REQUEST' in _C365_CA_NS:
        raise RuntimeError('c371 parent already has V219SKIP')
    exec(compile(__TOMATO__, '<c371-tomato>', 'exec'), _C365_CA_NS)
    if _C371_FERTILIZER:
        _C365_CA_NS['e402_agent'] = _C371_PARENT
        exec(compile(__FERTILIZER__, '<c371-fertilizer>', 'exec'), _C365_CA_NS)

def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        _C371_REPORT.clear()
        if _C371_ENABLED:
            for key in _C365_CA_NS['_V13V_REPORT']:
                _C365_CA_NS['_V13V_REPORT'][key] = 0
    if _C371_ENABLED and _C371_FERTILIZER:
        action = _C365_CA_NS['e410_agent'](observation, configuration)
    else:
        action = _C371_PARENT(observation, configuration)
    _C371_REPORT.update({'herd_'+k:v for k,v in _Y_REPORT.items()})
    if _C371_ENABLED:
        _C371_REPORT.update(_C365_CA_NS['_V13V_REPORT'])
        if _C371_FERTILIZER:
            _C371_REPORT.update({'fert_'+k:v for k,v in _C365_CA_NS['_E410_REPORT'].items()})
    return action

agent.telemetry = _C371_REPORT
kaggle_submission_agent = agent
c371_submission_agent = agent
'''.replace('__V54__', V54_SHA).replace('__V56__', V56_SHA).replace('__ON__', str(not args.disabled)).replace('__FERT__', str(not args.tomato_only)).replace('__TOMATO__', repr(tomato)).replace('__FERTILIZER__', repr(fertilizer))
    data = parent.rstrip() + suffix.encode('utf8')
    compile(data, str(args.out), 'exec')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(args.out)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())

if __name__ == '__main__':
    main()
