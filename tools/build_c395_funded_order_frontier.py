"""Compose a bounded funded mixed-queue search from public unit-price helpers."""
import argparse, ast, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='2574f60424e319f5cd1df0221c94eb1bf33da57fa32ef0a15a8a7e7f65a2eae7'
DONOR_SHA='178ae0f727641cf4b618ebb98ade7aa1a1bed7517281aab9849de82a59d8ed3a'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');a=ap.parse_args()
    body=(ROOT/'agent/c387_forecast_frontier.py').read_bytes();assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    donor=next(x for x in json.loads((ROOT/'state/c394/league-current.json').read_text())['agents'] if x['id']==261)
    data=Path(donor['source_path']).read_bytes();assert hashlib.sha256(data).hexdigest()==DONOR_SHA
    text=data.decode();lines=text.splitlines(True);names=('_v44y_price','_v44y_params','_v44y_lockstep')
    nodes={n.name:n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
    layer='\n'.join(''.join(lines[nodes[n].lineno-1:nodes[n].end_lineno]) for n in names)
    wrapper=(ROOT/'agent/overlays/c395_funded_order_frontier.py').read_text().replace('__LAYER__',repr(layer))
    if a.disabled:wrapper=wrapper.replace('_C395_ENABLED = True','_C395_ENABLED = False')
    out=body.rstrip()+b'\n'+wrapper.encode();compile(out,str(a.out),'exec');assert not a.out.exists();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_bytes(out)
    print(a.out,hashlib.sha256(out).hexdigest())
if __name__=='__main__':main()
