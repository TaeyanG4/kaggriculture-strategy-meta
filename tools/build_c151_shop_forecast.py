"""Build a standalone c146 derivative; preserve frozen parent bytes and gates."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_HASH = '5e51caad786dac00f98639e8eb8ef911a169904f86cff3d2fe777853cd89a928'


def build():
    parent = (ROOT / 'agent/c146_carrot_sched3.py').read_bytes()
    assert hashlib.sha256(parent).hexdigest() == PARENT_HASH, 'Parent drift'
    source = parent.decode('utf-8').replace('\r\n', '\n')
    marker = '_C146_PARENT = agent'
    assert source.count(marker) == 1
    before, body = source.split(marker)
    helpers = (ROOT / 'agent/overlays/c151_shop_forecast.py').read_text(encoding='utf-8')
    body = marker + body
    start = body.index("    shops = obs['town']['unlocked_shops']\n    daily_demand")
    end = body.index("    route = _IMPL.chassis.players[seat]['route']", start)
    body = body[:start] + "    # Economic forecast below replaces the fixed shop-count threshold.\n" + body[end:]
    start = body.index('        # Include visible competing crops, 32 speculative')
    end = body.index('        value_failed = value < cost + 100', start)
    body = body[:start] + '''        forecast = _c151_economics(obs, certificate, state)
        value, cost = forecast['value'], forecast['cost']
        state['shop_forecasts'] += 1
        state['shop_carrot_demand'] += forecast['carrot_demand']
        state['shop_wheat_demand'] += forecast['wheat_demand']
        state['shop_low_count_evaluations'] += int(
            1 + 6 * (2 * obs['town']['unlocked_shops'].count('PET_CAFE')
                     + obs['town']['unlocked_shops'].count('FARMERS_MARKET')) < 25)
''' + body[end:]
    body = body.replace("'last_buy_day': -1, 'conversions': 0", "'shop_forecasts': 0, 'shop_carrot_demand': 0, 'shop_wheat_demand': 0,\n            'shop_low_count_evaluations': 0, 'last_buy_day': -1, 'conversions': 0")
    body = body.replace("('maxMarketOrdersPerTurn', 10)]):", "('maxMarketOrdersPerTurn', 10),\n             ('townShopSellInterval', 4), ('townCenterSellInterval', 24), ('episodeSteps', 720)]):")
    # New candidate namespace; no c146 wrapper is stacked or called twice.
    body = body.replace('_C146', '_C151').replace('_c146', '_c151')
    artifact = (before + '\n' + helpers + '\n' + body).encode('utf-8')
    target = ROOT / 'agent/c151_shop_forecast.py'
    if target.exists() and target.read_bytes() != artifact:
        raise RuntimeError('Candidate exists with different bytes; use a new version')
    target.write_bytes(artifact)
    print('c151 SHA256:', hashlib.sha256(artifact).hexdigest())
    return target


if __name__ == '__main__':
    build()
