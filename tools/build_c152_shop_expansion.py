"""Build c152 as a byte-guarded, expansion-only derivative of c146."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_HASH = '5e51caad786dac00f98639e8eb8ef911a169904f86cff3d2fe777853cd89a928'


def build():
    parent = (ROOT / 'agent/c146_carrot_sched3.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_HASH, 'Parent drift'
    source = parent.decode('utf-8').replace('\r\n', '\n')
    marker = '_C146_PARENT = agent'
    before, body = source.split(marker)
    helpers = (ROOT / 'agent/overlays/c152_shop_expansion.py').read_text(encoding='utf-8')
    body = marker + body
    old_gate = """    shops = obs['town']['unlocked_shops']
    daily_demand = 1 + 6 * (2 * shops.count('PET_CAFE') + shops.count('FARMERS_MARKET'))
    if daily_demand < 25:
        state['gate_demand'] += 1
        return result
"""
    new_gate = """    shops = obs['town']['unlocked_shops']
    daily_demand = 1 + 6 * (2 * shops.count('PET_CAFE') + shops.count('FARMERS_MARKET'))
    legacy_eligible = daily_demand >= 25
    if not legacy_eligible:
        state['shop_expansion_candidates'] += 1
"""
    assert body.count(old_gate) == 1
    body = body.replace(old_gate, new_gate)
    start = body.index('        # Include visible competing crops, 32 speculative')
    end = body.index('        value_failed = value < cost + 100', start)
    legacy = body[start:end]
    replacement = """        if legacy_eligible:
""" + ''.join('    ' + line if line.strip() else line for line in legacy.splitlines(keepends=True)) + """        else:
            forecast = _c152_low_demand_economics(obs, certificate, state)
            value, cost = forecast['value'], forecast['cost']
            state['shop_expansion_forecasts'] += 1
            state['shop_expansion_carrot_demand'] += forecast['carrot_demand']
            state['shop_expansion_wheat_demand'] += forecast['wheat_demand']
"""
    body = body[:start] + replacement + body[end:]
    state_anchor = "'last_buy_day': -1, 'conversions': 0"
    state_new = "'shop_expansion_candidates': 0, 'shop_expansion_forecasts': 0,\n            'shop_expansion_carrot_demand': 0, 'shop_expansion_wheat_demand': 0,\n            'last_buy_day': -1, 'conversions': 0"
    assert body.count(state_anchor) == 1
    body = body.replace(state_anchor, state_new)
    request_anchor = "state['requests'] += 1; state['last_buy_day'] = day"
    request_new = "state['requests'] += 1; state['last_buy_day'] = day\n        if not legacy_eligible: state['shop_expansion_requests'] += 1"
    assert body.count(request_anchor) == 1
    body = body.replace(request_anchor, request_new)
    counter_anchor = "'shop_expansion_candidates': 0, 'shop_expansion_forecasts': 0,"
    counter_new = "'shop_expansion_candidates': 0, 'shop_expansion_forecasts': 0, 'shop_expansion_requests': 0,"
    assert body.count(counter_anchor) == 1
    body = body.replace(counter_anchor, counter_new)
    config_anchor = "('maxMarketOrdersPerTurn', 10)]):"
    config_new = "('maxMarketOrdersPerTurn', 10), ('townShopSellInterval', 4),\n             ('townCenterSellInterval', 24), ('episodeSteps', 720)]):"
    assert body.count(config_anchor) == 1
    body = body.replace(config_anchor, config_new)
    artifact = (before + '\n' + helpers + '\n' + body).encode('utf-8')
    target = ROOT / 'agent/c152_shop_expansion.py'
    if target.exists() and target.read_bytes() != artifact:
        raise RuntimeError('Candidate exists with different bytes; use a new version')
    target.write_bytes(artifact)
    print('c152 SHA256:', hashlib.sha256(artifact).hexdigest())


if __name__ == '__main__':
    build()
