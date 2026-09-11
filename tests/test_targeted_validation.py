import tempfile
import unittest
from pathlib import Path

from src.kaggriculture_meta.targeted_validation import fisher_exact_two_sided, select_quantile_grid


class TargetedValidationTests(unittest.TestCase):
    def test_quantile_grid_is_bounded_unique_and_spans_bands(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.csv"
            path.write_text(
                "episode_id,create_time,avg_score,min_score,sum_score,agent_count,size_bytes\n"
                + "".join(
                    f"{1000+i},2026-09-10T00:00:00,{2800+i},2700,{5600+2*i},2,100\n"
                    for i in range(200)
                ),
                encoding="utf-8",
            )
            rows = select_quantile_grid("2026-09-10", path, 24)
            self.assertEqual(len(rows), 24)
            self.assertEqual(len({r["episode_id"] for r in rows}), 24)
            self.assertEqual({r["score_band"] for r in rows}, {"daily_low", "daily_mid", "daily_high"})

    def test_fisher_exact_is_symmetric(self):
        p1 = fisher_exact_two_sided(5, 15, 15, 5)
        p2 = fisher_exact_two_sided(15, 5, 5, 15)
        self.assertAlmostEqual(p1, p2)
        self.assertLess(p1, 0.01)


if __name__ == "__main__":
    unittest.main()
