"""Cap the CARROT2 reserve by remaining terminal-route planting slots."""
from __future__ import annotations
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='d48e66c3c5aec21a55be8101d7544278d5303fc6a1b1a487d9a2df055c82e72f'
WRAPPER=r'''

# c368: preserve c365's production decisions and one-day feed horizon.
# Once its chassis has irrevocably entered terminal route 2, a reserve larger
# than ALL remaining wheat/carrot planting commands cannot be consumed.
# Include both crops for a conservative bound; do not predict future prices.
_C368_ON = __ENABLED__
_C368_PARENT = agent
_C368_REPORT = {}
_C368_OLD_BUFFER = _C365_CA_NS['_CA_BUFFER']
_C368_TAIL = _C365_CA_NS['_IMPL'].chassis.routes[2]
_C368_FUTURE = [0] * (len(_C368_TAIL) + 1)
for _c368_t in range(len(_C368_TAIL) - 1, -1, -1):
    _c368_a = _C368_TAIL[_c368_t]
    _c368_commands = [_c368_a.get('farmer') or ['PASS'], *_c368_a.get('hands', [])]
    _C368_FUTURE[_c368_t] = _C368_FUTURE[_c368_t + 1] + sum(
        c[:2] in (['PLANT', 'WHEAT'], ['PLANT', 'CARROT'])
        for c in _c368_commands)


def agent(observation, configuration=None):
    step = int(observation['step'])
    if step == 0:
        _C368_REPORT.clear()
        _C368_REPORT.update(enabled=int(_C368_ON), capped_turns=0,
                            current_reserve=_C368_OLD_BUFFER, ca_errors=0)
    reserve = _C368_OLD_BUFFER
    if _C368_ON and step >= 648:
        reserve = min(reserve, _C368_FUTURE[min(step + 1, len(_C368_TAIL))])
        _C368_REPORT['capped_turns'] += int(reserve < _C368_OLD_BUFFER)
    _C365_CA_NS['_CA_BUFFER'] = reserve
    try:
        action = _C368_PARENT(observation, configuration)
    finally:
        _C365_CA_NS['_CA_BUFFER'] = _C368_OLD_BUFFER
    _C368_REPORT['current_reserve'] = reserve
    _C368_REPORT['ca_errors'] = _C365_CA_NS['_CA_REPORT'].get('ca_errors', 0)
    return action


agent.telemetry = _C368_REPORT
kaggle_submission_agent = agent
c368_submission_agent = agent
'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--disabled',action='store_true');a=p.parse_args()
    body=(ROOT/'agent/c365_feed_reserve.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    data=body.rstrip()+b'\n'+WRAPPER.replace('__ENABLED__',str(not a.disabled)).encode()
    compile(data,str(a.out),'exec');a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data)
    print(a.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
