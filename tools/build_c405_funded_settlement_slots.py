"""Allow funded fixed-cost orders to yield to the reserved wheat sale.

Same c402 parent and c404 reservations. Variable-price inherited slots stay put.
Prepared from development ledger evidence, before c404's independent readout.
"""
import argparse,hashlib,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build(enabled=True):
    spec=importlib.util.spec_from_file_location('reserved',ROOT/'tools/build_c404_reserved_wheat_settlement.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
    parent=(ROOT/'agent/c402_current_public_shadow.py').read_bytes().rstrip()
    previous=prior.build(enabled);assert previous.startswith(parent)
    overlay=previous[len(parent):].decode().replace('c404','c405').replace('C404','C405')
    overlay=overlay.replace('Partial wheat lots; preserve all existing absolute market slots.',
        'Partial wheat lots; preserve inherited variable-price market slots.')
    marker="    _C405_DEBTS[(seat,t+1,route)] = (legs[0][0],future_quantity,quantity)"
    assert marker in overlay
    change="""    # All original purchases are fully cash-funded by _r97_budget above.
    # Only fixed-price HIRE/BUY_SEED may move right. Never cross a product
    # order, animal/land commitment or empty slot: those indices are protected.
    while slot > index + 1:
        left = result['market'][slot-1]
        fixed = left == ['HIRE'] or (len(left)==3 and left[0]=='BUY_SEED'
                  and type(left[2]) is int and left[2]>0)
        if not fixed:
            break
        result['market'][slot], result['market'][slot-1] = left, result['market'][slot]
        slot -= 1
"""
    raw=parent+overlay.replace(marker,change+marker).encode();compile(raw,'c405','exec');return raw
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');args=ap.parse_args();assert not args.out.exists()
    raw=build(not args.disabled);args.out.write_bytes(raw);print(args.out,hashlib.sha256(raw).hexdigest())
