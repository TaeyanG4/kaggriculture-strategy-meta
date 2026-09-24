"""Build the final-action own-sale observer for c365's adaptive market layer."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SHA = 'd48e66c3c5aec21a55be8101d7544278d5303fc6a1b1a487d9a2df055c82e72f'
WRAPPER = r'''

# c367: update Boatlee-derived adaptive_market from the completed action,
# after the public sale-advance and order layers have finished. This is a
# different consumer from c327's old RACE observer; no prices or gates change.
# Physical projection reuses the parent's _ov_fields / _r97_market_stock.
_C367_ON = __ENABLED__
_C367_PARENT = agent
_C367_REPORT = {}


def _c367_find(namespace):
    seen = set()
    while isinstance(namespace, dict) and id(namespace) not in seen:
        seen.add(id(namespace))
        operator = namespace.get('_OPERATOR')
        if getattr(operator, '__name__', '') == 'adaptive_market':
            return operator.__globals__
        namespace = namespace.get('_BASE_NS')
    raise RuntimeError('c367 adaptive namespace contract drift')


_C367_ADAPTIVE = _c367_find(globals())


def agent(observation, configuration=None):
    step = int(observation['step'])
    if step == 0:
        _C367_REPORT.clear()
        _C367_REPORT.update(enabled=int(_C367_ON), projections=0,
                            corrected_item_turns=0, observer_errors=0)
    action = _C367_PARENT(observation, configuration)
    if not _C367_ON:
        return action
    state = _C367_ADAPTIVE['_ADAPTIVE_STATE'].get(int(observation['player']))
    if state is None or step >= 704:
        return action
    try:
        _, private = _C365_CA_NS['_ov_fields'](observation, action)
        orders = action.get('market') or []
        _, _, sales = _C365_CA_NS['_r97_market_stock'](private['shed'], orders)
        sold = {item: 0 for item in _C367_ADAPTIVE['_ADAPTIVE_ITEMS']}
        for index, quantity in sales.items():
            item = orders[index][1]
            if item in sold:
                sold[item] += quantity
        _C367_REPORT['corrected_item_turns'] += sum(
            state.get('last_sold', {}).get(item, 0) != quantity
            for item, quantity in sold.items())
        state['last_sold'] = sold
        _C367_REPORT['projections'] += 1
    except (KeyError, TypeError, ValueError, IndexError, AttributeError):
        _C367_REPORT['observer_errors'] += 1
    return action


agent.telemetry = _C367_REPORT
kaggle_submission_agent = agent
c367_submission_agent = agent
'''

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--disabled',action='store_true')
    args=parser.parse_args()
    body=(ROOT/'agent/c365_feed_reserve.py').read_bytes()
    assert hashlib.sha256(body).hexdigest()==PARENT_SHA
    data=body.rstrip()+b'\n'+WRAPPER.replace('__ENABLED__',str(not args.disabled)).encode()
    compile(data,str(args.out),'exec')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(data)
    print(args.out,hashlib.sha256(data).hexdigest())

if __name__=='__main__':main()
