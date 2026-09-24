"""Preserve inherited order slots while settling an adjacent, reserved wheat lot.

Reuses c398's funded trade and route-debt mechanism. Different execution contract:
partial lots, original market indices retained, sale in a later empty slot or at
the end. Source/config/readback identities remain explicit.
"""
import argparse, hashlib, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='dbc25e1a4464ad3c8e04a3ce6907cba1897efd0d87818563ba6e2a796c363797'

def build(enabled=True):
    spec=importlib.util.spec_from_file_location('prior_settlement',ROOT/'tools/build_c398_wheat_settlement.py')
    prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    overlay=prior.OVERLAY.replace('c398','c404').replace('C398','C404')
    overlay=overlay.replace('Only our own adjacent planned wheat trade is inspected.',
        'Partial wheat lots; preserve all existing absolute market slots.')
    overlay=overlay.replace('index, quantity = due','index, original_quantity, quantity = due')
    overlay=overlay.replace("orders[index] == ['SELL', 'WHEAT', quantity]","orders[index] == ['SELL', 'WHEAT', original_quantity]")
    overlay=overlay.replace("action['market'][index] = ['SELL', 'WHEAT', 0]","action['market'][index] = ['SELL', 'WHEAT', original_quantity - quantity]")
    overlay=overlay.replace("or len(orders)>=10:",":")
    overlay=overlay.replace("if len(legs)!=1 or legs[0][1]!=['SELL','WHEAT',quantity]:\n        return action", """if len(legs)!=1 or legs[0][1][0]!='SELL':
        return action
    future_quantity = int(legs[0][1][2])
    quantity = min(quantity, future_quantity)
    if quantity <= 0:
        return action
    # Do not move any inherited order across a rival's simultaneous slot.
    # The new sale must follow the buy; empty earlier slots stay empty.
    slot = next((i for i in range(index+1,len(orders)) if not orders[i]),len(orders))
    if slot >= 10:
        return action""")
    overlay=overlay.replace("result['market'].insert(index+1, ['SELL','WHEAT',quantity])", """sale = ['SELL','WHEAT',quantity]
    if slot < len(result['market']):
        result['market'][slot] = sale
    else:
        result['market'].append(sale)""")
    overlay=overlay.replace('(legs[0][0],quantity)','(legs[0][0],future_quantity,quantity)')
    overlay=overlay.replace('__FLAG__',str(enabled))
    source=(ROOT/'agent/c402_current_public_shadow.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==PARENT_SHA
    raw=source.rstrip()+overlay.encode();compile(raw,'c404','exec');return raw

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');args=ap.parse_args()
    assert not args.out.exists();raw=build(not args.disabled);args.out.write_bytes(raw)
    print(str(args.out),hashlib.sha256(raw).hexdigest())
