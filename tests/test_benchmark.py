import unittest

from src.kaggriculture_meta.benchmark import summarize_matches, wilson_interval


class BenchmarkTests(unittest.TestCase):
    def test_wilson_bounds_contain_observed_rate(self):
        low, high = wilson_interval(7, 10)
        self.assertLess(low, 0.7)
        self.assertGreater(high, 0.7)

    def test_summary_is_seat_aware(self):
        rows = [
            {
                "outcome": "win",
                "candidate_seat": 0,
                "candidate_reward": 10,
                "opponent_reward": 5,
                "reward_margin": 5,
                "candidate_status": "DONE",
                "opponent_status": "DONE",
                "runtime_seconds": 1,
            },
            {
                "outcome": "loss",
                "candidate_seat": 1,
                "candidate_reward": 4,
                "opponent_reward": 6,
                "reward_margin": -2,
                "candidate_status": "DONE",
                "opponent_status": "DONE",
                "runtime_seconds": 1,
            },
        ]
        summary = summarize_matches(rows, "candidate", "opponent")
        self.assertEqual(summary["win_rate_decided"], 0.5)
        self.assertEqual(summary["seat0_win_rate_decided"], 1.0)
        self.assertEqual(summary["seat1_win_rate_decided"], 0.0)
        self.assertTrue(summary["all_status_done"])


if __name__ == "__main__":
    unittest.main()
