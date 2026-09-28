"""Transplant only Herd-Safe's confidence-gated distant sale signals.

The corpus, near-event path, selector, sale quantities, and inherited notices
remain unchanged. Use --disabled for an exact parent-behaviour control.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'agent/c416_current_policy_coverage.py'
PARENT_SHA = '4880a8522c31573e65d315edbe11c7c46085e708695f35e9d95b0b6bfec2e558'
DONOR = ROOT / 'state/public_league/artifacts/f08df802d6f40a855bef15a11fbf4684b4083bc210a016aa0d2f789176f1c879/main.py'
DONOR_SHA = '216c6919a71c24e8d26528fe0148481da50e00d608e4e13b524f491ed689074f'


def function(source, name):
    node = next(n for n in ast.parse(source).body
                if isinstance(n, ast.FunctionDef) and n.name == name)
    return '\n'.join(source.splitlines()[node.lineno - 1:node.end_lineno]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--disabled', action='store_true')
    args = ap.parse_args()
    parent = PARENT.read_bytes()
    donor = DONOR.read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_SHA
    assert hashlib.sha256(donor).hexdigest() == DONOR_SHA
    helper = function(donor.decode('utf8'), '_hp_quantity')
    original = Path(json.loads((ROOT / 'state/c384/agent258-identity.json').read_text('utf8'))['source_path']).read_text('utf8')
    assert hashlib.sha256(original.encode('utf8')).hexdigest() == '83fb106f37fcc10f3c3d9db8a78ded1529da30e9e232976ec0cf46fd6662fed4'
    predictor = function(original, '_v92_predict')
    old = 'votes = sum(1 for ev in best if ev.get((step + 1, i), 0) + ev.get((step + 2, i), 0) >= _V92_P_K)'
    new = 'votes = sum(1 for ev in best if _hp_quantity(ev, i, step, st["obs"]) >= _V92_P_K)'
    assert predictor.count(old) == 1
    predictor = predictor.replace(old, new)
    layer = (helper + '\n' + predictor).replace('_hp_quantity', '_c417_quantity')
    layer = layer.replace('_HP_WINDOW', '_C417_WINDOW').replace('_HP_STATS', '_C417_REPORT')
    wrapper = '''

# c417: Apache-2.0 Herd-Safe confidence gate for additional distant signals.
# Donor runtime SHA216c6919; c387 original forecast corpus stays unchanged.
_C417_ENABLED = __ENABLED__
_C417_PARENT = agent
_C417_REPORT = dict(extension_signals=0, rejected_signals=0)
_C417_TELEMETRY = {}
if _C417_ENABLED:
    # Keep the previous callable available for diagnostic identity checks.
    _c417_original_predict = _C365_CA_NS['_v92_predict']
    _C365_CA_NS['_C417_REPORT'] = _C417_REPORT
    _C365_CA_NS['_C417_WINDOW'] = 4
    exec(compile(__LAYER__, '<c417-confident-forecast>', 'exec'), _C365_CA_NS)

def agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _C417_REPORT:
            _C417_REPORT[key] = 0
    result = _C417_PARENT(observation, configuration)
    _C417_TELEMETRY.clear()
    _C417_TELEMETRY.update(getattr(_C417_PARENT, 'telemetry', {}))
    _C417_TELEMETRY.update({'c417_' + key: value for key, value in _C417_REPORT.items()})
    return result

agent.telemetry = _C417_TELEMETRY
c417_submission_agent = agent
'''.replace('__ENABLED__', str(not args.disabled)).replace('__LAYER__', repr(layer))
    # Validate static equivalence to the c387 forecast donor before injection.
    restored = predictor.replace(new, old)
    assert ast.dump(ast.parse(restored)) == ast.dump(ast.parse(function(original, '_v92_predict')))
    data = parent.rstrip() + wrapper.encode('utf8')
    compile(data, str(args.out), 'exec')
    assert not args.out.exists()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(data)
    print(args.out, hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    main()
