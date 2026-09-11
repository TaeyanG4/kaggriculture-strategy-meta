import unittest

from src.kaggriculture_meta.pilot import classify_strategy, prefix_hash, wilson_interval


class PilotTests(unittest.TestCase):
    def test_resource_mix_family(self):
        row = {
            "animal_goose_share": 0.05,
            "animal_cow_share": 0.30,
            "animal_sheep_share": 0.65,
            "crop_carrot_share": 0.10,
            "crop_melon_share": 0.05,
            "crop_strawberry_share": 0.25,
            "crop_tomato_share": 0.02,
        }
        self.assertEqual(classify_strategy(row), "sheep+strawberry")

    def test_prefix_hash_is_deterministic(self):
        steps = [[{"action": {}}, {"action": {}}],
                 [{"action": {"market": [["BUY_SEED", "WHEAT", 1]]}}, {"action": {}}]]
        self.assertEqual(prefix_hash(steps, 0, 24), prefix_hash(steps, 0, 24))

    def test_wilson_interval_contains_observed_rate(self):
        low, high = wilson_interval(4, 5)
        self.assertLess(low, 0.8)
        self.assertGreater(high, 0.8)


if __name__ == "__main__":
    unittest.main()
