"""Mechanism checks only: no simulated games or campaign execution."""
import copy
import runpy
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class ShopForecastTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from kaggle_environments.envs.kaggriculture import kaggriculture as engine
        cls.engine = engine
        cls.ns = runpy.run_path(str(ROOT / 'agent/c151_shop_forecast.py'))
        # runpy copies the result dict; use actual function globals for patches.
        cls.ns = cls.ns['_c151_economics'].__globals__

    def obs(self, shops=('PET_CAFE',), inventory=-700):
        farms = [{'tiles': [[None] * 10 for _ in range(10)], 'farmer': [0, 0],
                  'hands': [], 'money': 100000} for _ in range(2)]
        market = self.engine._new_market()
        market['inventory']['CARROT'] += inventory
        self.engine._refresh_prices(market)
        return {'step': 432, 'player': 0, 'farms': farms, 'town': {'unlocked_shops': list(shops)},
                'market': market, 'private': {'shed': {}, 'inventories': [{}], 'seeds': {'WHEAT': 1}}}

    def certificate(self):
        return {'step': 504, 'actor': 0, 'birth': 18, 'xy': (0, 0),
                'scheduled_wheat': 3, 'foregone_wheat_upper': 5}

    def test_consumption_matches_official_engine_and_tick_edges(self):
        for shops in ([], ['PET_CAFE'], ['PET_CAFE'] * 2 + ['FARMERS_MARKET'], list(self.engine.SHOPS)):
            for start, end in ((0, 1), (3, 4), (4, 5), (23, 25), (432, 504), (433, 433)):
                market = self.engine._new_market()
                original = dict(market['inventory'])
                state = [SimpleNamespace(observation=SimpleNamespace(market=market, town={'unlocked_shops': shops}))]
                for t in range(start, end):
                    self.engine._town_consume(SimpleNamespace(configuration={}), state, t)
                for item in ('WHEAT', 'CARROT', 'MILK', 'WOOL', 'EGG'):
                    self.assertEqual(original[item] - market['inventory'][item],
                                     self.ns['_c151_consumption'](shops, item, start, end))

    def test_shop_mapping_exact(self):
        self.assertEqual({k: tuple(v) for k, v in self.engine.SHOPS.items()}, self.ns['_C151_SHOPS'])

    def test_prices_match_engine_with_public_parameters(self):
        params = copy.deepcopy(self.engine.MARKET_PARAMS)
        params['CARROT']['base'] += 7
        for item in params:
            for offset in (-900, -450, -1, 0, 40, 100, 600):
                inv = params[item]['I0'] + offset
                self.assertEqual(self.engine.market_price(item, inv, params),
                                 self.ns['_r37_market_price'](item, inv, params))

    def test_more_carrot_demand_increases_value(self):
        a = self.ns['_c151_economics'](self.obs([]), self.certificate(), {'plans': []})
        b = self.ns['_c151_economics'](self.obs(['PET_CAFE'] * 2), self.certificate(), {'plans': []})
        self.assertGreater(b['value'], a['value'])

    def test_rival_carrot_supply_decreases_value(self):
        obs = self.obs()
        a = self.ns['_c151_economics'](obs, self.certificate(), {'plans': []})
        obs['farms'][1]['tiles'][0][1] = {'crop': 'CARROT', 'planted_day': 18}
        b = self.ns['_c151_economics'](obs, self.certificate(), {'plans': []})
        self.assertLess(b['value'], a['value'])
        self.assertEqual(b['carrot_supply'] - a['carrot_supply'], 4)

    def test_visible_commitment_counted_once(self):
        obs = self.obs()
        obs['farms'][0]['tiles'][0][0] = {'crop': 'CARROT', 'planted_day': 18}
        supply = self.ns['_c151_crop_supply']
        self.assertEqual(supply(obs, 'CARROT', 504, []), supply(obs, 'CARROT', 504, [self.certificate()]))

    def test_more_wheat_shops_raise_opportunity_cost(self):
        a = self.ns['_c151_economics'](self.obs(), self.certificate(), {'plans': []})
        b = self.ns['_c151_economics'](self.obs(['PET_CAFE'] + ['BAKERY'] * 4), self.certificate(), {'plans': []})
        self.assertGreater(b['cost'], a['cost'])

    def control(self, obs, certificate=True, config=None):
        parent = {'farmer': ['PASS'], 'hands': [], 'market': []}
        tape = {433: {'farmer': ['PLANT', 'WHEAT'], 'hands': [], 'market': []}}
        chassis = SimpleNamespace(players={0: {'route': 0}}, routes={0: tape})
        replacements = {
            '_C151_PARENT': lambda *a: copy.deepcopy(parent),
            '_IMPL': SimpleNamespace(chassis=chassis),
            '_c151_after_field': lambda *a: copy.deepcopy(obs['farms'][0]),
            '_c151_certificate': lambda *a: self.certificate() if certificate else None,
            'projected_shed': lambda *a: {}, 'FarmView': lambda o: o,
            '_C151_STATES': {}, '_C151_REPORT': {},
        }
        with patch.dict(self.ns, replacements):
            action = self.ns['agent'](obs, config)
            state = copy.deepcopy(self.ns['_C151_STATES'][0])
        self.assertEqual(state['errors'], 0)
        return action, state

    def test_single_pet_changes_actual_buy_decision(self):
        action, state = self.control(self.obs())
        self.assertIn(['BUY_SEED', 'CARROT', 1], action['market'])
        self.assertEqual(state['requests'], 1)
        self.assertEqual(state['shop_low_count_evaluations'], 1)
        # c146 daily demand for one PET is 13 < 25: old policy rejects this.

    def test_two_pets_oversupply_rejects_conversion(self):
        action, state = self.control(self.obs(['PET_CAFE'] * 2, 500))
        self.assertEqual(action['market'], [])
        self.assertEqual(state['gate_value'], 1)

    def test_route_cash_and_time_guards(self):
        obs = self.obs()
        action, state = self.control(obs, certificate=False)
        self.assertEqual(action['market'], [])
        self.assertEqual(state['gate_route'], 1)
        obs['farms'][0]['money'] = 30
        action, state = self.control(obs)
        self.assertEqual(action['market'], [])
        self.assertEqual(state['gate_cash'], 1)
        obs = self.obs(); obs['step'] = 648
        action, state = self.control(obs)
        self.assertEqual(action['market'], [])
        self.assertEqual(state['shop_forecasts'], 0)

    def test_nonstandard_timing_falls_back(self):
        action, state = self.control(self.obs(), config={'townShopSellInterval': 3})
        self.assertEqual(action['market'], [])
        self.assertEqual(state['shop_forecasts'], 0)

    def test_forecast_ignores_unrevealed_future_shop_data(self):
        obs = self.obs()
        a = self.ns['_c151_economics'](obs, self.certificate(), {'plans': []})
        obs['town']['future_shops'] = ['PET_CAFE'] * 100
        obs['seed'] = 1234
        self.assertEqual(a, self.ns['_c151_economics'](obs, self.certificate(), {'plans': []}))


if __name__ == '__main__':
    unittest.main(verbosity=2)
