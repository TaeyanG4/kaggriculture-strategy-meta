import tempfile
import unittest
from pathlib import Path

from src.kaggriculture_meta.current_v1 import daily_summary, sha256_file


class CurrentV1Tests(unittest.TestCase):
    def test_sha256_file_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.txt"
            path.write_text("kaggriculture", encoding="utf-8")
            self.assertEqual(sha256_file(path), sha256_file(path))

    def test_daily_summary_counts_openings_and_family(self):
        base = {
            "source_date": "2026-09-10",
            "strategy_family_pilot": "cow+strawberry",
            "cash_t24": 1,
            "cash_t168": 2,
            "cash_t360": 3,
            "crop_strawberry_share": 0.4,
            "crop_tomato_share": 0.1,
            "animal_cow_share": 0.5,
            "animal_goose_share": 0.1,
            "animal_sheep_share": 0.4,
        }
        rows = [
            dict(base, episode_id="1", opening_hash_t24="a", opening_hash_t48="x"),
            dict(base, episode_id="1", opening_hash_t24="b", opening_hash_t48="y"),
        ]
        summary = daily_summary(rows)[0]
        self.assertEqual(summary["episodes"], 1)
        self.assertEqual(summary["seats"], 2)
        self.assertEqual(summary["cow_strawberry_share"], 1.0)
        self.assertEqual(summary["distinct_openings_t24"], 2)


if __name__ == "__main__":
    unittest.main()
