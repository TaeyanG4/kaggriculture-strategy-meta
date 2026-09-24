"""Package verified public policies and official deterministic transitions."""
import argparse,base64,hashlib,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='2574f60424e319f5cd1df0221c94eb1bf33da57fa32ef0a15a8a7e7f65a2eae7'
def packed(data):return base64.b85encode(zlib.compress(data,9)).decode()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
    folder=ROOT/'state/c396';plan=json.loads((folder/'shadow-plan-v2.json').read_text());qa=json.loads((folder/'shadow-diagnostic-v2.json').read_text())
    assert all(x['correct_actions']==719 and x['correct_private']==719 for x in qa)
    parent=(ROOT/'agent/c387_forecast_frontier.py').read_bytes();assert hashlib.sha256(parent).hexdigest()==PARENT_SHA
    sources={}
    for key,entry in plan['models'].items():
        b=Path(entry['source_path']).read_bytes();assert hashlib.sha256(b).hexdigest()==entry['source_sha256'];sources[key]=packed(b)
    engine=(folder/'engine_subset.py').read_bytes();assert hashlib.sha256(engine).hexdigest()==plan['subset_sha256']
    tracker=(folder/'shadow_core_v2.py').read_bytes();assert hashlib.sha256(tracker).hexdigest()==plan['tracker_v2_sha256']
    layer=(ROOT/'agent/overlays/c396_public_shadow.py').read_text()
    layer=layer.replace('__SOURCES__',repr(sources)).replace('__ENGINE__',repr(packed(engine))).replace('__TRACKER__',repr(packed(tracker)))
    if a.disabled:layer=layer.replace('_C396_ENABLED = True','_C396_ENABLED = False')
    b=parent.rstrip()+b'\n'+layer.encode();compile(b,str(a.out),'exec');assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(b);print(a.out,hashlib.sha256(b).hexdigest(),len(b))
if __name__=='__main__':main()
