"""Build self-contained attributed derivatives of the immutable public V37."""
import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARENT = '94c1c2c05ae7cde8fca9ee3957b01112c1cbab82c7434aae6a5f24fa7485bc4c'


def replace_function(text, name, replacements):
    nodes = [n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(nodes) != 1:
        raise ValueError(f'Expected one {name}')
    n = nodes[0]
    lines = text.splitlines(keepends=True)
    block = ''.join(lines[n.lineno - 1:n.end_lineno])
    for before, after in replacements:
        if block.count(before) != 1:
            raise ValueError(f'Ambiguous replacement in {name}: {before}')
        block = block.replace(before, after)
    return ''.join(lines[:n.lineno - 1]) + block + ''.join(lines[n.end_lineno:])


def build(output, repair=False, tomato_day=None, tomato_shops=2,
          input_start=12, input_ratio=1.5, input_workers=2, repair_actions=None, inventory_budget=False,
          sale_horizon=4):
    parent = (ROOT / 'agent/public_v37_more_yield.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT
    text = parent.decode('utf-8')
    if sale_horizon != 4:
        before = 'if 288 <= step < 696:_R37_HORIZONS[player] = 4'
        assert text.count(before) == 1
        text = text.replace(before, f'if 288 <= step < 696:_R37_HORIZONS[player] = {sale_horizon}')
    if (input_start, input_ratio, input_workers) != (12, 1.5, 2):
        text = replace_function(text, '_r51_input_control', [
            ('12<=day<=28', f'{input_start}<=day<=28'),
            ('value<1.5*cost+50', f'value<{input_ratio}*cost+50')])
        assert text.count('_R51_INPUT_MAX_WORKERS=2') == 1
        text = text.replace('_R51_INPUT_MAX_WORKERS=2', f'_R51_INPUT_MAX_WORKERS={input_workers}')
    if tomato_day is not None:
        if tomato_day not in (12, 15):
            raise ValueError('Supported planting days: 12, 15')
        # Modify only the named investment functions and the uniquely identified
        # investment wrapper. The full parent license and all notices survive.
        text = replace_function(text, '_v219_qualifies', [
            ("< 3:", f"< {tomato_shops}:"),
            ('tape[432:719]', f'tape[{tomato_day * 24}:719]')])
        text = replace_function(text, '_v219_request', [
            ('day!=18', f'day!={tomato_day}'),
            ('day in (24,27)', f'day in {tuple(range(tomato_day + 6, 29, 3))}'),
            ('day in (19,20,21,22,23,25)', f'{tomato_day}<day<{tomato_day+8} and not fertilizer'),
            ('26<=day<=28', f'{tomato_day+8}<=day<=28'),
            ('day==27 and labor is None', 'fertilizer and labor is None')])
        text = replace_function(text, '_v219_worker', [('day==18', f'day=={tomato_day}')])
        # These exact strings occur once in the investment wrapper.
        for before, after in [
            ("if step==432:state['eligible']=_v219_qualifies(observation,native)",
             f"if step=={tomato_day*24}:state['eligible']=_v219_qualifies(observation,native)"),
            ("if not state.get('eligible') or day<18:return action", f"if not state.get('eligible') or day<{tomato_day}:return action"),
            ("pending['fertilizer'] and (day==24 or fertilizer_worker)",
             f"pending['fertilizer'] and (day=={tomato_day+6} or fertilizer_worker)")]:
            if text.count(before) != 1:
                raise ValueError('Investment wrapper changed upstream')
            text = text.replace(before, after)
    if repair:
        overlay = (ROOT / 'agent/overlays/observation_repair.py').read_text(encoding='utf-8')
        if repair_actions is not None:
            overlay = overlay.replace('if replacement is not None:', f'if replacement is not None and replacement[0] in {tuple(repair_actions)!r}:')
        text += '\n' + overlay
    if inventory_budget:
        text += '\n' + (ROOT / 'agent/overlays/inventory_budget.py').read_text(encoding='utf-8')
    notice = '# PROJECT DERIVATIVE, 2026-09-12; Apache-2.0.\n'
    notice += f'# Changed: observation_repair={repair}; tomato_planting_day={tomato_day}; tomato_shop_gate={tomato_shops}.\n'
    notice += f'# Input allocation: start_day={input_start}, value_cost_ratio={input_ratio}, max_workers={input_workers}; repair_actions={repair_actions!r}.\n'
    notice += f'# Inventory budget enabled: {inventory_budget}.\n'
    notice += f'# Physically funded sale reservation horizon: {sale_horizon}.\n'
    notice += '# Public V37 parent and every upstream license/attribution retained below.\n'
    payload = (notice + text).encode('utf-8')
    compile(payload, str(output), 'exec')
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.read_bytes() != payload:
        raise ValueError('Candidate exists with different bytes; choose a new name')
    output.write_bytes(payload)
    manifest = {'parent_sha256': PARENT, 'sha256': hashlib.sha256(payload).hexdigest(),
                'bytes': len(payload), 'repair': repair, 'tomato_day': tomato_day, 'tomato_shops': tomato_shops,
                'input_start': input_start, 'input_ratio': input_ratio, 'input_workers': input_workers,
                'repair_actions': repair_actions,
                'inventory_budget': inventory_budget,
                'sale_horizon': sale_horizon,
                'source': 'https://www.kaggle.com/code/ahmedberatozer/more-yield-smarter-labor'}
    output.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--repair', action='store_true')
    ap.add_argument('--tomato-day', type=int)
    ap.add_argument('--tomato-shops', type=int, default=2)
    ap.add_argument('--input-start', type=int, default=12)
    ap.add_argument('--input-ratio', type=float, default=1.5)
    ap.add_argument('--input-workers', type=int, default=2)
    ap.add_argument('--repair-actions', nargs='+')
    ap.add_argument('--inventory-budget', action='store_true')
    ap.add_argument('--sale-horizon', type=int, default=4)
    args = ap.parse_args()
    print(json.dumps(build(args.output, args.repair, args.tomato_day, args.tomato_shops,
                           args.input_start, args.input_ratio, args.input_workers, args.repair_actions,
                           args.inventory_budget, args.sale_horizon), indent=2))


if __name__ == '__main__':
    main()
