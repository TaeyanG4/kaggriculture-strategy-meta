"""Update only the inherited forecast event corpus, with pinned public provenance."""
import argparse,ast,base64,hashlib,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='2574f60424e319f5cd1df0221c94eb1bf33da57fa32ef0a15a8a7e7f65a2eae7'
DONOR_SHA='83fb106f37fcc10f3c3d9db8a78ded1529da30e9e232976ec0cf46fd6662fed4'
RAW_SHA='f5c3d06b214d369768a92e6dfb8e07aa5e5da6cffe15bd423af4160261ee73d4'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
    parent=(ROOT/'agent/c387_forecast_frontier.py').read_bytes();assert hashlib.sha256(parent).hexdigest()==PARENT_SHA
    identity=json.loads((ROOT/'state/c384/agent258-identity.json').read_text('utf8'))
    donor=Path(identity['source_path']).read_bytes();assert hashlib.sha256(donor).hexdigest()==DONOR_SHA
    values={}
    for n in ast.parse(donor).body:
        if isinstance(n,ast.Assign):
            for t in n.targets:
                if isinstance(t,ast.Name) and t.id in ('_V92_P_BLOB','_V92_P_INDEX'):
                    values[t.id]=ast.literal_eval(n.value)
    raw=zlib.decompress(base64.b85decode(values['_V92_P_BLOB']));assert hashlib.sha256(raw).hexdigest()==RAW_SHA
    # Validate all binary records before importing the public corpus.
    count=0
    for start,length in values['_V92_P_INDEX']:
        pos=start;num=int.from_bytes(raw[pos:pos+2],'little');pos+=2;count+=num
        for _ in range(num):
            m=int.from_bytes(raw[pos:pos+2],'little');pos+=2;last=0
            for _ in range(m):
                delta=raw[pos];pos+=1
                if delta==255:t=int.from_bytes(raw[pos:pos+2],'little');pos+=2
                else:t=last+delta
                assert 0<=t<720 and 0<=raw[pos]<5 and raw[pos+1]>0
                last=t;pos+=2
        assert pos==start+length,(pos,start,length)
    assert count==2398
    overlay='''

# c393: forecast corpus refresh; public More Wheat, Smarter Sales / Clone Race
# corpus, original author notices retained. No new price/time/quantity rules.
# https://www.kaggle.com/code/dmitriigluzdov/kaggriculture-more-wheat-smarter-sales
# Donor source SHA __SHA__; decoded corpus SHA __RAW_SHA__.
_C393_ENABLED = __ENABLED__
_C393_PARENT = agent
_C393_TELEMETRY = {}
if _C393_ENABLED:
    # The pinned parent's reader uses base85. Keep its parser and all scorers.
    if 'b85decode' not in _C365_CA_NS['_v92_p_pair'].__code__.co_names:
        raise RuntimeError('c393 corpus decoder contract changed')
    _C365_CA_NS['_V92_P_BLOB'] = __BLOB__
    _C365_CA_NS['_V92_P_INDEX'] = __INDEX__
    _C365_CA_NS['_V92_P_RAW'] = None
    _C365_CA_NS['_V92_P_LIB'] = None

def agent(observation, configuration=None):
    action = _C393_PARENT(observation, configuration)
    _C393_TELEMETRY.clear()
    _C393_TELEMETRY.update(_C387_TELEMETRY)
    _C393_TELEMETRY['c393_corpus_paths'] = 2398 if _C393_ENABLED else 1998
    return action

agent.telemetry = _C393_TELEMETRY
c393_submission_agent = agent
'''.replace('__SHA__',DONOR_SHA).replace('__RAW_SHA__',RAW_SHA).replace('__ENABLED__',str(not a.disabled)).replace('__BLOB__',repr(values['_V92_P_BLOB'])).replace('__INDEX__',repr(values['_V92_P_INDEX']))
    data=parent.rstrip()+overlay.encode('utf8');compile(data,str(a.out),'exec');assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(data)
    print(a.out,hashlib.sha256(data).hexdigest(),'corpus_paths',count)

if __name__=='__main__':main()
