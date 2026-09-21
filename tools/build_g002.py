"""Build candidate g002_route_certified_turnover.py adhering strictly to the 3 invariants."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
c306_p = ROOT / 'agent/c306_v48_native_sale_rotation.py'
raw = c306_p.read_bytes()
source = raw.decode('utf-8').replace('\r\n', '\n')

# 1. Update gates in _c146_control for route-certified late-game crop turnover
old_gate1 = "if not 18 <= day <= 25 or step % 24 >= 22 or state['requests'] >= 8 or state['last_buy_day'] == day:"
new_gate1 = "if not 18 <= day <= 25 or step % 24 >= 22 or state['requests'] >= 32 or state.get('buy_day_count', {}).get(day, 0) >= 4:"
assert old_gate1 in source, "Gate 1 not found"
source = source.replace(old_gate1, new_gate1)

old_demand = "if daily_demand < 25:"
new_demand = "if daily_demand < 7:"
assert old_demand in source, "Demand gate not found"
source = source.replace(old_demand, new_demand)

old_cash = "cash_failed = farm['money'] < native_seed_cost + cost + 3000"
new_cash = "cash_failed = farm['money'] < native_seed_cost + cost + 1000"
assert old_cash in source, "Cash gate not found"
source = source.replace(old_cash, new_cash)

old_state_upd = "state['requests'] += 1; state['last_buy_day'] = day"
new_state_upd = "state['requests'] += 1; state['last_buy_day'] = day; state.setdefault('buy_day_count', {})[day] = state.get('buy_day_count', {}).get(day, 0) + 1"
assert old_state_upd in source, "State update not found"
source = source.replace(old_state_upd, new_state_upd)

# 2. Invariant 3: Waste Action Conversion
# Clean up no-op HARVEST actions on empty tiles / 0-yield animals (d20+)
hook_point = "    # c306: native policy owns all carrot sales, including any added production."
waste_code = '''    # Invariant 3 (Waste Action Conversion): suppress no-op HARVEST on empty tiles or 0-yield units
    if day >= 20:
        for actor in range(min(len(positions), len(commands))):
            if commands[actor] == ['HARVEST']:
                x, y = positions[actor]
                tile = farm['tiles'][y][x]
                if not (isinstance(tile, dict) and (tile.get('crop') or tile.get('animal')) and tile.get('yield_units', 0) > 0):
                    set_command(actor, ['PASS'])
                    state['noop_harvest_suppressed'] = state.get('noop_harvest_suppressed', 0) + 1
'''
assert hook_point in source, "Hook point not found"
source = source.replace(hook_point, waste_code + '\n' + hook_point)

# 3. Update branding and exported agent
source = source.replace('_C306_', '_G002_')

out = ROOT / 'agent/g002_route_certified_turnover.py'
out.write_text(source, encoding='utf-8')
out_sha = hashlib.sha256(out.read_bytes()).hexdigest()
print(f"Generated {out.name} ({len(source)} bytes, SHA256: {out_sha})")
