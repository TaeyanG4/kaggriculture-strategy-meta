"""Reuse the existing supply guard across a next-turn hiring boundary."""
import argparse,ast,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT='52f0617e9287976d76c302fa6ce1fa5d14b84da7a1c71c2b5066336c2c327fe8'
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
    body=(ROOT/'agent/c400_feed_safe_carrot.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT
    decoded=(ROOT/'state/c398/embedded-11.py').read_text('utf8')
    node=next(n for n in ast.parse(decoded).body if isinstance(n,ast.FunctionDef) and n.name=='_r97_supply')
    fn=ast.get_source_segment(decoded,node)
    old='if len(next_orders)==10 and not any('
    assert fn.count(old)==1
    fn=fn.replace(old,"if (len(next_orders)==10 or any(o and o[0]=='HIRE' for o in next_orders)) and not any(")
    fn=fn.replace('def _r97_supply(', 'def _c401_supply(',1)
    if a.disabled:
        for key in ('_C399_ENABLED','_C400_ENABLED'):
            old=(key+' = True').encode();assert body.count(old)==1
            body=body.replace(old,(key+' = False').encode())
    layer='\n\n# c401: fund planned pickups before a hiring turn can fill its market queue.\n'
    layer+='_C401_ENABLED = '+str(not a.disabled)+'\n_C401_SUPPLY_SOURCE = '+repr(fn)+'\n'
    layer+='''
_C401_PARENT = agent
_C401_TELEMETRY = {}
if _C401_ENABLED:
    exec(compile(_C401_SUPPLY_SOURCE,'<c401-supply>','exec'),_C365_CA_NS)
    _C365_CA_NS['_r97_supply'].__code__ = _C365_CA_NS['_c401_supply'].__code__

def agent(observation,configuration=None):
    result=_C401_PARENT(observation,configuration)
    _C401_TELEMETRY.clear();_C401_TELEMETRY.update(_C400_TELEMETRY)
    for key in ('supply_prefund_changes','supply_prefund_units','supply_slot_declines','supply_errors'):
        _C401_TELEMETRY['c401_'+key]=_C365_CA_NS['_R97_REPORT'].get(key,0)
    return result

agent.telemetry=_C401_TELEMETRY
c401_submission_agent=agent
'''
    result=body.rstrip()+layer.encode();compile(result,str(a.out),'exec');assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(result)
    print(a.out,hashlib.sha256(result).hexdigest())
