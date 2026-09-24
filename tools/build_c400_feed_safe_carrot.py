"""c399 correction: preserve wheat harvests supplying the carrier's later feed."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT='6c5fb7597cd3a29c119279067e6b0fd1e4967dc07acb3551a78df60066ea6fc9'
LAYER=r'''

# c400: retain wheat grown for a harvesting worker's subsequent animal feed.
# Source is our own route and current observation, not future opponent actions.
_C400_ENABLED = __ENABLED__
_C400_PARENT = agent
_C400_YIELD = _C365_CA_NS['_ca_yield_path']
_C400_OBSERVATION = None
_C400_REPORT = {}
_C400_TELEMETRY = {}

def _c400_yield_path(crop, planted, visits, y0=1, fert_until=-1, watered_day=-1, now_step=0):
    if _C400_ENABLED and crop=='CARROT' and now_step==0 and _C400_OBSERVATION is not None:
        obs=_C400_OBSERVATION;seat=int(obs['player'])
        for t,actor,op in visits:
            if op!='HARVEST':continue
            # Do not replace a feed-bearing wheat harvest. A later pickup of
            # wheat or a cargo deposit ends this particular harvest's duty.
            for future in range(t+1,min((t//24+1)*24,720)):
                act=_C365_CA_NS['_ca_tape'](seat,future)
                cmds=[act.get('farmer') or ['PASS']]+list(act.get('hands') or [])
                cmd=cmds[actor] if actor<len(cmds) else ['PASS']
                if cmd[0]=='DROP' or cmd[:2]==['PICKUP','WHEAT']:break
                if cmd[0]=='FEED':
                    _C400_REPORT['c400_feed_lane_blocks']=_C400_REPORT.get('c400_feed_lane_blocks',0)+1
                    return (0,0,None)
            break
    return _C400_YIELD(crop,planted,visits,y0,fert_until,watered_day,now_step)

if _C400_ENABLED:
    _C365_CA_NS['_ca_yield_path'] = _c400_yield_path

def agent(observation,configuration=None):
    global _C400_OBSERVATION
    _C400_OBSERVATION=observation
    if int(observation['step'])==0:_C400_REPORT.clear()
    action=_C400_PARENT(observation,configuration)
    _C400_TELEMETRY.clear();_C400_TELEMETRY.update(_C399_TELEMETRY);_C400_TELEMETRY.update(_C400_REPORT)
    return action

agent.telemetry=_C400_TELEMETRY
c400_submission_agent=agent
'''

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
    body=(ROOT/'agent/c399_route_valued_carrot.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT
    # Combined OFF is the development control against c397, not c399 ON.
    if a.disabled:
        assert body.count(b'_C399_ENABLED = True')==1
        body=body.replace(b'_C399_ENABLED = True',b'_C399_ENABLED = False')
    result=body.rstrip()+LAYER.replace('__ENABLED__',str(not a.disabled)).encode()
    compile(result,str(a.out),'exec');assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(result)
    print(a.out,hashlib.sha256(result).hexdigest())
