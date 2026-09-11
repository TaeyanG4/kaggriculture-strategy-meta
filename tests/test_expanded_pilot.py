import tempfile
import unittest
from pathlib import Path

from src.kaggriculture_meta.expanded_pilot import select_day


class ExpandedPilotTests(unittest.TestCase):
    def test_select_day_is_bounded_and_labeled(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.csv"
            path.write_text(
                "episode_id,create_time,avg_score,min_score,sum_score,agent_count,size_bytes\n"
                + "".join(
                    f"{1000+i},2026-09-10T00:00:00,{2800+i},2700,{5600+2*i},2,100\n"
                    for i in range(100)
                ),
                encoding="utf-8",
            )
            rows = select_day("2026-09-10", path)
            self.assertEqual(len(rows), 6)
            self.assertEqual({r["score_band"] for r in rows}, {"daily_low", "daily_mid", "daily_high"})
            self.assertTrue(all(r["source_license"] == "CC0-1.0" for r in rows))


if __name__ == "__main__":
    unittest.main()
