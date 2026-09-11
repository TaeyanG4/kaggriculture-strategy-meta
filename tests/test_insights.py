import unittest

from src.kaggriculture_meta.insights import benjamini_hochberg, paired_rows, sign_test_two_sided


class InsightTests(unittest.TestCase):
    def test_sign_test_detects_one_sided_pairs(self):
        self.assertLess(sign_test_two_sided(20, 0), 0.001)

    def test_bh_adjustment_is_monotonic_by_p_rank(self):
        q = benjamini_hochberg([0.001, 0.01, 0.5])
        self.assertLessEqual(q[0], q[1])
        self.assertLessEqual(q[1], q[2])

    def test_paired_rows_requires_one_win_and_one_loss(self):
        rows = [
            {"episode_id": "1", "outcome": "win"},
            {"episode_id": "1", "outcome": "loss"},
            {"episode_id": "2", "outcome": "win"},
        ]
        self.assertEqual(len(paired_rows(rows)), 1)


if __name__ == "__main__":
    unittest.main()
