import unittest

from src.kaggriculture_meta.release_schema import (
    EXCLUDED_IDENTITY_FIELDS,
    V1_COLUMNS,
    build_v1_candidate,
    compare_with_georgy,
    project_v1,
)
import csv
import json
import tempfile
from pathlib import Path


class ReleaseSchemaTests(unittest.TestCase):
    def test_sensitive_identity_fields_are_not_in_v1(self):
        self.assertFalse(EXCLUDED_IDENTITY_FIELDS & set(V1_COLUMNS))

    def test_experimental_family_is_renamed(self):
        row = {"strategy_family_pilot": "sheep+strawberry"}
        self.assertEqual(project_v1(row)["strategy_family_experimental"], "sheep+strawberry")

    def test_georgy_comparison_tracks_exact_and_semantic_overlap(self):
        comparison = compare_with_georgy(
            V1_COLUMNS,
            ["episode_id", "seat", "engine_version", "final_money", "total_hires", "first_land_day"],
        )
        self.assertEqual(comparison["exact_name_overlap"], ["engine_version", "episode_id", "seat"])
        self.assertEqual(comparison["semantic_overlap"]["final_reward"], "final_money")

    def test_candidate_builder_excludes_identity_and_passes_core_qa(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.csv"
            out = Path(tmp) / "strategy_meta.csv"
            qa_path = Path(tmp) / "qa.json"
            row = {source_name: "" for _, source_name in __import__(
                "src.kaggriculture_meta.release_schema", fromlist=["V1_FIELD_MAP"]
            ).V1_FIELD_MAP}
            row.update({
                "source_dataset": "kaggle/example",
                "source_license": "CC0-1.0",
                "source_date": "2026-09-10",
                "episode_id": "123",
                "episode_date": "2026-09-10T00:00:00",
                "seat": "0",
                "engine_version": "1.32.7",
                "turns": "720",
                "final_reward": "1000",
                "manifest_avg_score": "3000",
                "manifest_min_score": "2950",
                "sample_quantile": "0.5",
                "strategy_family_pilot": "cow+strawberry",
            })
            for name in [
                "crop_carrot_share", "crop_melon_share", "crop_strawberry_share",
                "crop_tomato_share", "crop_wheat_share"
            ]:
                row[name] = "0.2"
            for name, value in [
                ("animal_cow_share", "0.5"), ("animal_goose_share", "0.2"), ("animal_sheep_share", "0.3")
            ]:
                row[name] = value
            row["team_id"] = "secret-ish"
            with source.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(row))
                writer.writeheader()
                writer.writerow(row)
            qa = build_v1_candidate(source, out, qa_path)
            self.assertTrue(qa["passes_core_qa"])
            with out.open(encoding="utf-8") as f:
                self.assertNotIn("team_id", next(csv.reader(f)))
            self.assertTrue(json.loads(qa_path.read_text(encoding="utf-8"))["passes_core_qa"])


if __name__ == "__main__":
    unittest.main()
