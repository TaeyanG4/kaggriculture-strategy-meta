import hashlib
from pathlib import Path

base_code = Path('state/c312/public_v9_4.py').read_text(encoding='utf-8')

# 1. Relax herd constants for cow swap
base_code = base_code.replace('V9_HERD_MAX_EGG_SHOPS_COW = 0', 'V9_HERD_MAX_EGG_SHOPS_COW = 2')
base_code = base_code.replace('V9_HERD_MIN_MILK_SHOPS = 3', 'V9_HERD_MIN_MILK_SHOPS = 2')

# 2. Add G000 Apex Layer: Physical Inventory Sale Advance
apex_layer = '''
# ===========================================================================
# G000 APEX LAYER: Physical Inventory Sale Advance & Order Protection
# ===========================================================================
_G000_PARENT = agent
del agent

_G000_PREMIUM = ('STRAWBERRY', 'WOOL', 'EGG', 'MILK', 'MELON', 'CARROT', 'TOMATO')
_G000_REPORT = {'g000_advance': 0, 'g000_errors': 0}

def _g000_future_market(obs, offset):
    step = int(obs['step']) + offset
    if step >= 719: return None
    native = _IMPL.chassis.players.get(int(obs['player']))
    route = 2 if step >= 648 else (native or {}).get('route')
    if route is None or route not in _IMPL.chassis.routes: return None
    tape = _IMPL.chassis.routes[route]
    return tape[step].get('market') if step < len(tape) and isinstance(tape[step], dict) else []

def _g000_process_market(obs, market):
    step = int(obs['step'])
    cur = [list(o) for o in market if o]
    
    # Advance planned premium sales by 1-2 steps if inventory is ALREADY physically in shed
    if step % 24 != 23 and step < 718:
        want = {}
        protected = None
        for off in (1, 2):
            fut = _g000_future_market(obs, off)
            if not fut: continue
            if protected is None and len(fut[0]) > 2 and fut[0][0] == 'SELL':
                protected = fut[0][1]
            for o in fut:
                if len(o) > 2 and o[0] == 'SELL' and o[1] in _G000_PREMIUM and o[1] != protected:
                    want[o[1]] = want.get(o[1], 0) + max(0, int(o[2]))
        if want:
            shed = obs.get('private', {}).get('shed', {})
            now = {}
            for o in cur:
                if len(o) > 2 and o[0] == 'SELL':
                    now[o[1]] = now.get(o[1], 0) + int(o[2])
            extra = []
            for item, q in want.items():
                n = min(q, int(shed.get(item, 0)) - now.get(item, 0))
                if n >= 1:
                    hit = next((o for o in cur if len(o) > 2 and o[0] == 'SELL' and o[1] == item), None)
                    if hit is not None:
                        hit[2] = int(hit[2]) + n
                    else:
                        extra.append(['SELL', item, n])
            if extra:
                extra = extra[:max(0, 10 - len(cur))]
                # Append extra sales to preserve integrity of tape execution order
                cur = cur + extra
                _G000_REPORT['g000_advance'] += len(extra)

    return cur[:10]

def agent(observation, configuration=None):
    action = _G000_PARENT(observation, configuration)
    try:
        if isinstance(action, dict) and 'market' in action:
            action = dict(action)
            action['market'] = _g000_process_market(observation, action['market'])
    except Exception:
        _G000_REPORT['g000_errors'] += 1
    return action

agent.telemetry = _G000_REPORT
agent = globals().pop('agent')
'''

full_code = base_code + '\n' + apex_layer
out_path = Path('agent/g000_apex_frontier.py')
out_path.write_text(full_code, encoding='utf-8', newline='\n')
sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
print(f"Created {out_path} (SHA-256: {sha})")
