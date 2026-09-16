"""Mechanism checks for expansion-only c152; no simulated games."""
import copy
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class ShopExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from kaggle_environments.envs.kaggriculture import kaggriculture as engine
        cls.engine = engine
        cls.spaces = {}
        for name in ('c146_carrot_sched3.py', 'c152_shop_expansion.py'):
            result = runpy.run_path(str(ROOT / 'agent' / name))
            cls.spaces[name[:4]] = result['_c146_control'].__globals__

    def obs(self, shops, carrot_offset=-1000, money=100000):
        farms = [{'tiles': [[None] * 10 for _ in range(10)], 'farmer': [0, 0],
                  'hands': [], 'money': money} for _ in range(2)]
        market = self.engine._new_market()
        market['inventory']['CARROT'] += carrot_offset
        self.engine._refresh_prices(market)
        return {'step': 432, 'player': 0, 'farms': farms, 'town': {'unlocked_shops': list(shops)},
                'market': market, 'private': {'shed': {}, 'inventories': [{}],
                                              'seeds': {'WHEAT': 1, 'CARROT': 0}}}

    @staticmethod
    def certificate():
        return {'step': 504, 'actor': 0, 'birth': 18, 'xy': (0, 0),
                'scheduled_wheat': 3, 'foregone_wheat_upper': 5}

    def control(self, version, obs, config=None):
        ns = self.spaces[version]
        parent = {'farmer': ['PASS'], 'hands': [], 'market': []}
        tape = {433: {'farmer': ['PLANT', 'WHEAT'], 'hands': [], 'market': []}}
        chassis = SimpleNamespace(players={0: {'route': 0}}, routes={0: tape})
        replacements = {
            '_C146_PARENT': lambda *a: copy.deepcopy(parent),
            '_IMPL': SimpleNamespace(chassis=chassis),
            '_c146_after_field': lambda *a: copy.deepcopy(obs['farms'][0]),
            '_c146_certificate': lambda *a: self.certificate(),
            'projected_shed': lambda *a: {}, 'FarmView': lambda o: o,
            '_C146_STATES': {}, '_C146_REPORT': {},
        }
        with patch.dict(ns, replacements):
            action = ns['agent'](obs, config)
            state = copy.deepcopy(ns['_C146_STATES'][0])
        self.assertEqual(state['errors'], 0)
        return action, state

    def test_high_demand_preserves_c146_action_and_economics(self):
        obs = self.obs(['PET_CAFE', 'PET_CAFE', 'FARMERS_MARKET'])
        legacy_action, legacy_state = self.control('c146', obs)
        action, state = self.control('c152', obs)
        self.assertEqual(action, legacy_action)
        self.assertEqual(state['requests'], legacy_state['requests'])
        self.assertEqual(state['forecast_gain'], legacy_state['forecast_gain'])
        self.assertEqual(state['shop_expansion_forecasts'], 0)
        self.assertEqual(state['shop_expansion_requests'], 0)

    def test_single_pet_can_expand_when_market_is_scarce(self):
        action, state = self.control('c152', self.obs(['PET_CAFE']))
        self.assertIn(['BUY_SEED', 'CARROT', 1], action['market'])
        self.assertEqual(state['shop_expansion_forecasts'], 1)
        self.assertEqual(state['shop_expansion_requests'], 1)
        self.assertEqual(state['requests'], 1)

    def test_single_pet_oversupply_is_rejected(self):
        action, state = self.control('c152', self.obs(['PET_CAFE'], carrot_offset=700))
        self.assertEqual(action['market'], [])
        self.assertEqual(state['shop_expansion_forecasts'], 1)
        self.assertEqual(state['gate_value'], 1)

    def test_c146_still_rejects_low_count_before_route(self):
        action, state = self.control('c146', self.obs(['PET_CAFE']))
        self.assertEqual(action['market'], [])
        self.assertEqual(state['gate_demand'], 1)
        self.assertEqual(state['certified_routes'], 0)

    def test_consumption_matches_official_engine(self):
        fn = self.spaces['c152']['_c152_consumption']
        for shops in ([], ['PET_CAFE'], ['PET_CAFE'] * 2 + ['FARMERS_MARKET'], list(self.engine.SHOPS)):
            market = self.engine._new_market(); original = dict(market['inventory'])
            state = [SimpleNamespace(observation=SimpleNamespace(market=market, town={'unlocked_shops': shops}))]
            for step in range(432, 504):
                self.engine._town_consume(SimpleNamespace(configuration={}), state, step)
            for item in ('CARROT', 'WHEAT', 'MILK', 'WOOL'):
                self.assertEqual(original[item] - market['inventory'][item], fn(shops, item, 432, 504))

    def test_full_upper_bound_is_only_quarter_weighted(self):
        ns = self.spaces['c152']; obs = self.obs(['PET_CAFE'])
        forecast = ns['_c152_low_demand_economics'](obs, self.certificate(), {'plans': []})
        params = {k: dict(v) for k, v in ns['_R37_MARKET_PARAMS'].items()}
        demand = forecast['wheat_demand']
        quote = max(obs['market']['prices']['WHEAT'],
                    ns['_r37_market_price']('WHEAT', obs['market']['inventory']['WHEAT'] - demand - 12, params)) + 5
        self.assertEqual(forecast['cost'], 20 + 3.5 * quote)

    def test_nonstandard_market_clock_fails_closed(self):
        action, state = self.control('c152', self.obs(['PET_CAFE']), {'townShopSellInterval': 3})
        self.assertEqual(action['market'], [])
        self.assertEqual(state['shop_expansion_forecasts'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
