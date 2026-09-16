import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src.kaggriculture_meta.league import (digest, prepare, read_journal,
                                         summarize, validate_splits)


class LeagueTests(unittest.TestCase):
    def test_splits_reject_reused_world_seeds(self):
        with self.assertRaisesRegex(ValueError, "leakage"):
            validate_splits({"train": [1], "selection": [2], "holdout": [1]})

    def test_copies_are_not_independent_opponents(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            root = Path(tmp)
            candidate = root / "candidate.py"
            opponent = root / "opponent.py"
            clone = root / "renamed.py"
            candidate.write_text("def agent(obs, config): return {}\n")
            opponent.write_text("def agent(obs, config): return {'market': []}\n")
            clone.write_bytes(opponent.read_bytes())
            plan = {"splits": {"train": [1], "selection": [2], "holdout": [3]},
                    "opponents": [{"name": p.stem, "path": str(p), "family": "same"}
                                  for p in (opponent, clone)]}
            with patch("src.kaggriculture_meta.league.engine_identity", return_value={"version": "test"}):
                identity, jobs = prepare(plan, candidate, "train", root / "out")
            self.assertEqual(len(jobs), 2)
            self.assertEqual({j["candidate_seat"] for j in jobs}, {0, 1})
            self.assertEqual(len(identity["deduplicated"]), 1)
            self.assertEqual(Path(identity["candidate"]["path"]).read_bytes(), candidate.read_bytes())
            with self.assertRaisesRegex(ValueError, "train"):
                prepare(plan, candidate, "holdout", root / "out", 1)

    def test_resume_recovers_only_incomplete_tail(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            path = Path(tmp) / "matches.jsonl"
            good = json.dumps({"match_id": "one"}).encode() + b"\n"
            path.write_bytes(good + b'{"match_id": "tw')
            self.assertEqual(len(read_journal(path)), 1)
            self.assertEqual(path.read_bytes(), good)
            path.write_bytes(good.rstrip(b'\n'))
            self.assertEqual(len(read_journal(path)), 1)
            self.assertEqual(path.read_bytes(), good)
            path.write_bytes(good + b"broken\n")
            with self.assertRaisesRegex(ValueError, "Corrupt"):
                read_journal(path)
            path.write_bytes(good + good)
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                read_journal(path)

    def test_controlled_diagnostics_and_failures_do_not_inflate_native_wins(self):
        common = {"candidate_seat": 0, "seed": 123, "opponent_name": "one", "opponent_family": "same"}
        rows = [dict(common, mode="native_reacting", valid=True, outcome="loss", margin=-1),
                dict(common, mode="native_reacting", valid=False, outcome="win", margin=99),
                dict(common, mode="fixed_shops_frozen_opponent", valid=True, outcome="win", margin=50)]
        result = summarize(rows)
        native = result["native_reacting"]["overall"]
        self.assertEqual((native["wins"], native["losses"], native["failures"]), (0, 1, 1))
        self.assertEqual(native["seed_clusters"], 1)
        self.assertIsNone(native["seed_cluster_bootstrap_95"])

    def test_match_identity_depends_on_content_not_mapping_order(self):
        self.assertEqual(digest({"a": 1, "b": 2}), digest({"b": 2, "a": 1}))
        self.assertNotEqual(digest(b"v1"), digest(b"v2"))

    def test_all_observed_wins_do_not_claim_certain_future_wins(self):
        rows = [dict(mode='native_reacting', candidate_seat=0, seed=seed,
                     opponent_name='same', opponent_family='same', valid=True,
                     outcome='win', margin=1) for seed in range(5)]
        self.assertIsNone(summarize(rows)['native_reacting']['overall']['seed_cluster_bootstrap_95'])


if __name__ == "__main__":
    unittest.main()
