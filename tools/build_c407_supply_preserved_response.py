"""Preserve public market inventory as well as own execution in sale response."""
import argparse,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build(enabled=True):
    raw=(ROOT/'agent/c406_public_sale_coverage.py').read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='cbbce2d21b687da9db86400199be674c32400b91c920f9ed52c1b58ae95230ee'
    if not enabled:
        assert raw.count(b'_C406_ENABLED = True')==1
        raw=raw.replace(b'_C406_ENABLED = True',b'_C406_ENABLED = False')
    layer='''

# c407: public sale coverage with a market-supply invariant.
# Kaggriculture 1.32.7 ignores $1 sales when adding market inventory.
# Equal sold units can therefore leave unequal public supply after reordering.
# Keep the parent's own execution checks and additionally preserve that supply
# for every surviving public hypothesis. No new orders or field edits.
_C407_ENABLED = __ENABLED__
def _c407_market(farms, privates, market, orders, configuration, own):
    f = _c396_copy.deepcopy(farms)
    p = _c396_copy.deepcopy(privates)
    m = _c396_copy.deepcopy(market)
    state = [_c396_box(observation=_c396_box(farms=f, market=m, private=p[i]),
                      action=dict(market=orders[i])) for i in (0, 1)]
    _C396_ENGINE['_process_market'](state, _c396_box(configuration=configuration))
    cash = [x['money'] for x in f]
    own_farm = dict(f[own])
    own_farm.pop('money')
    # _c396_response already requires result[2:] == base[2:] under all models.
    return cash[own], cash[own]-cash[1-own], p[own], own_farm, m['inventory']
if _C407_ENABLED:
    _c396_market = _c407_market
c407_submission_agent = agent
'''.replace('__ENABLED__',str(enabled))
    payload=raw.rstrip()+layer.encode();compile(payload,'c407','exec');return payload
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--disabled',action='store_true');args=ap.parse_args()
    assert not args.out.exists();args.out.parent.mkdir(exist_ok=True,parents=True)
    raw=build(not args.disabled);args.out.write_bytes(raw);print(args.out,hashlib.sha256(raw).hexdigest())
