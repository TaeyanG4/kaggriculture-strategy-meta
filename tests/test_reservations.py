"""Behavior gates for the selected derivative's physically funded sale reservations."""
import copy
import importlib.util
from pathlib import Path
import unittest


class ReservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / 'agent/c110_reserve8.py'
        spec = importlib.util.spec_from_file_location('reservation_test_agent', path)
        cls.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.m)

    def setUp(self):
        m = self.m
        self.old_routes = m._IMPL.chassis.routes
        self.old_players = m._IMPL.chassis.players
        m._IMPL.chassis.routes = {0: [{'farmer': ['PASS'], 'hands': [], 'market': []} for _ in range(719)]}
        m._IMPL.chassis.players = {0: {'route': 0, 'pending': {}, 'sell_state': {}}}
        m._R37_HORIZONS[0] = 8
        m._R36_SALE_REPORT.update(sale_reserved_units=0, sale_reservations=0)
        farm = {'tiles': [[None]*10 for _ in range(10)], 'farmer': [4,4], 'hands': [],
                'money': 3000, 'unlocked_quadrants': ['NW'], 'hires_today': 0}
        self.obs = {'step': 300, 'player': 0, 'farms': [farm, copy.deepcopy(farm)],
                    'private': {'shed': {'TOMATO': 5, 'WHEAT': 20}, 'seeds': {}, 'inventories': [{}]},
                    'market': {'prices': {'TOMATO': 80, 'WHEAT': 25}}}
        self.action = {'farmer': ['PASS'], 'hands': [], 'market': []}

    def tearDown(self):
        self.m._IMPL.chassis.routes = self.old_routes
        self.m._IMPL.chassis.players = self.old_players

    def test_stock_cap_and_debt_prevent_double_sale(self):
        m = self.m
        m._IMPL.chassis.routes[0][308]['market'] = [['SELL','TOMATO',20], ['SELL','WHEAT',20]]
        result = m._r36_reserve(self.obs, self.action)
        self.assertEqual(result['market'], [['SELL','TOMATO',5]])
        debt = m._IMPL.chassis.players[0]['sell_state']
        future = copy.deepcopy(m._IMPL.chassis.routes[0][308])
        m._r36_suppress(future, debt, 308)
        self.assertEqual(future['market'], [['SELL','TOMATO',15], ['SELL','WHEAT',20]])
        self.assertNotIn(308, debt['r36_debts'])

    def test_future_input_consumer_blocks_reservation(self):
        tape = self.m._IMPL.chassis.routes[0]
        tape[302]['farmer'] = ['PICKUP','TOMATO',5]
        tape[303]['market'] = [['SELL','TOMATO',20]]
        self.assertEqual(self.m._r36_reserve(self.obs, self.action)['market'], [])

    def test_route_boundary_blocks_reservation(self):
        self.obs['step'] = 359
        self.m._IMPL.chassis.routes[0][360]['market'] = [['SELL','TOMATO',20]]
        self.assertEqual(self.m._r36_reserve(self.obs, self.action)['market'], [])


if __name__ == '__main__':
    unittest.main()
