"""c386: preserve inherited tomato opportunities while adding c384's public gate."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='05b8d6eedb266fcc131ec74b8b87659e15ed077707d91489a423ad4d1a567144'
LAYER=r'''

# c386, Taeyang/Codex, 2026-09-23: c384's borrowed forecast is approximate.
# Preserve the pre-c384 qualifying opportunities as well as forecast additions.
# Neither forecast constants nor the existing physical investment plan changes.
_C386_ENABLED = __ENABLED__
_C386_PARENT = agent
_C386_QUALIFY = _C365_CA_NS['_v219_qualifies']
_C386_ORIGINAL = _C365_CA_NS['_CXTB_BASE_QUALIFIES']
_C386_REPORT = dict(c386_calls=0,c386_restored=0,c386_errors=0)
if _C386_QUALIFY.__globals__ is not _C365_CA_NS:
    raise RuntimeError('c386 qualification namespace drift')

def _c386_qualifies(observation, native):
    _C386_REPORT['c386_calls'] += 1
    predicted = _C386_QUALIFY(observation, native)
    if predicted:
        return True
    try:
        original = bool(_C386_ORIGINAL(observation, native))
    except Exception:
        _C386_REPORT['c386_errors'] += 1
        raise
    if original:
        _C386_REPORT['c386_restored'] += 1
    return original

if _C386_ENABLED:
    _C365_CA_NS['_v219_qualifies'] = _c386_qualifies
_C386_TELEMETRY = {}

def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _C386_REPORT:
            _C386_REPORT[key] = 0
    action = _C386_PARENT(observation, configuration)
    _C386_TELEMETRY.clear()
    _C386_TELEMETRY.update(_C384_REPORT)
    _C386_TELEMETRY.update(_C386_REPORT)
    return action

agent.telemetry = _C386_TELEMETRY
c386_submission_agent = agent
'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--disabled',action='store_true');a=p.parse_args()
    body=(ROOT/'agent/c384_predictive_tomato.py').read_bytes()
    assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    data=body.rstrip()+LAYER.replace('__ENABLED__',str(not a.disabled)).encode('utf8')
    compile(data,str(a.out),'exec');assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data)
    print(str(a.out),hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
