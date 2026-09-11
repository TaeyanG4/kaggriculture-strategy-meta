import unittest

from src.kaggriculture_meta.optimizer import apply_changes, candidate_specs, rank_summaries


class OptimizerTests(unittest.TestCase):
    def test_search_is_bounded_to_ten_policy_dimensions(self):
        dimensions = set()
        for changes in candidate_specs().values():
            dimensions.update(changes)
        self.assertEqual(
            dimensions,
            {
                "hands",
                "land_after_animals",
                "animal_mix",
                "feed_float_days",
                "animal_buffer",
                "max_wheat_price",
                "carry",
                "sell_chunk",
                "shed_pressure",
                "liquidate_from_day",
            },
        )

    def test_animal_mix_updates_structure_capacity(self):
        base = {"animal_target": {"COW": 10, "SHEEP": 6}, "build": [{"target": 16}]}
        tuned = apply_changes(base, {"animal_mix": {"COW": 12, "SHEEP": 4}})
        self.assertEqual(tuned["animal_target"], {"COW": 12, "SHEEP": 4})
        self.assertEqual(tuned["build"][0]["target"], 16)
        self.assertEqual(base["animal_target"], {"COW": 10, "SHEEP": 6})

    def test_ranking_penalizes_errors_before_margin(self):
        summaries = {
            "stable": {
                "error_rate": 0.0,
                "win_rate_decided": 0.5,
                "worst_opponent_win_rate": 0.4,
                "mean_margin": 1,
                "median_margin": 1,
            },
            "erroring": {
                "error_rate": 0.1,
                "win_rate_decided": 1.0,
                "worst_opponent_win_rate": 1.0,
                "mean_margin": 1000,
                "median_margin": 1000,
            },
        }
        self.assertEqual(rank_summaries(summaries)[0], "stable")


if __name__ == "__main__":
    unittest.main()
