import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src.kaggriculture_meta import championship_league as league


def healthy():
    return {"match_id": "one", "mode": "native_reacting", "stage": "train",
            "seed": 1, "candidate_seat": 0, "opponent_name": "other",
            "opponent_family": "other", "valid": True, "outcome": "win", "margin": 100,
            "candidate_telemetry": {}, "opponent_telemetry": {},
            "candidate_timing": {"over_1s": 0}, "opponent_timing": {"over_1s": 0}}


class ChampionshipLeagueContracts(unittest.TestCase):
    def test_nested_opponent_errors_do_not_count_as_a_valid_win(self):
        row = healthy()
        row["opponent_telemetry"] = {"upstream_error_counters": {"fallback": 2}}
        with self.assertRaisesRegex(ValueError, "opponent_internal_error"):
            league.require_valid([row], 1)
        self.assertEqual(league.positive_error_counters(row["opponent_telemetry"]),
                         {"upstream_error_counters.fallback": 2})
        row["opponent_telemetry"] = {"ordinary_fallback": 2, "repair_errors": 0}
        league.require_valid([row], 1)

    def test_one_second_gate_applies_to_both_players(self):
        for role in ("candidate", "opponent"):
            with self.subTest(role=role):
                row = healthy()
                row[role + "_timing"]["over_1s"] = 1
                with self.assertRaisesRegex(ValueError, role + "_over_one_second"):
                    league.require_valid([row], 1)

    def test_old_incomplete_duplicate_and_failed_results_fail_closed(self):
        row = healthy()
        del row["opponent_telemetry"]
        with self.assertRaisesRegex(ValueError, "evidence missing"):
            league.require_valid([row], 1)
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            league.require_valid([], 1)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            league.require_valid([healthy(), healthy()], 2)
        row = healthy()
        row.update(valid=False, error="wall_timeout")
        with self.assertRaisesRegex(ValueError, "invalid"):
            league.require_valid([row], 1)

    def test_nested_telemetry_survives_snapshot_and_json(self):
        raw = {"upstream_error_counters": {"repair": 3}, "cases": [{"errors": 1}],
               "ordinary_fallback": 2}
        snapshot = json.loads(json.dumps(league.telemetry_snapshot(raw)))
        self.assertEqual(league.positive_error_counters(snapshot),
                         {"upstream_error_counters.repair": 3, "cases[0].errors": 1})

    def test_coordinator_uses_new_worker_module_and_rejects_worker_crash(self):
        calls = []

        class FailedWorker:
            returncode = 1

            def poll(self):
                return self.returncode

            def wait(self):
                return self.returncode

        def launch(args, **kwargs):
            calls.append(args)
            return FailedWorker()

        job = {"match_id": "one", "mode": "native_reacting", "stage": "train",
               "seed": 1, "candidate_seat": 0, "opponent": {"name": "other", "family": "other"}}
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            out = Path(tmp)
            with patch.object(league.subprocess, "Popen", side_effect=launch):
                with self.assertRaisesRegex(ValueError, "invalid"):
                    league.run_jobs({"schema": league.SCHEMA}, [job], out, workers=1)
            saved = json.loads((out / "matches.jsonl").read_text())
            self.assertFalse(saved["valid"])
            self.assertEqual(saved["error"], "worker_failed")
        self.assertEqual(calls[0][2], "src.kaggriculture_meta.championship_league")


@unittest.skipUnless(os.environ.get("CHAMPIONSHIP_ENGINE_TESTS") == "1", "explicit engine integration gate")
class ChampionshipEngineContracts(unittest.TestCase):
    def test_actual_loader_captures_both_nested_telemetries(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            root = Path(tmp)
            source = root / "fixture.py"
            source.write_text('''calls=0
def agent(obs, config):
    global calls
    assert config.get("seed") is None and "seed" not in obs
    assert calls == obs["step"]
    calls += 1
    agent.telemetry["nested"]["calls"] = calls
    return {"farmer":["PASS"], "hands":[], "market":[]}
agent.telemetry={"nested":{"calls":0,"errors":0}}
''', encoding="utf-8")
            plan = {"splits": {"train": [919312], "selection": [919313], "holdout": [919314]},
                    "allow_mirror": True,
                    "opponents": [{"name": "fixture", "path": str(source), "family": "fixture"}]}
            identity, jobs = league.prepare(plan, source, "train", root / "run")
            result = league.run_jobs(identity, jobs[:1], root / "run", workers=1)
            self.assertEqual(result["native_reacting"]["overall"]["valid_games"], 1)
            row = json.loads((root / "run/matches.jsonl").read_text())
            for role in ("candidate", "opponent"):
                self.assertEqual(row[role + "_telemetry"]["nested"]["calls"], 719)
                self.assertEqual(row[role + "_timing"]["calls"], 719)
            self.assertEqual(league.run_jobs(identity, jobs[:1], root / "run", workers=1), result)


if __name__ == "__main__":
    unittest.main()
