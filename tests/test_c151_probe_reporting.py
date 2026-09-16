"""Check new probe summaries with synthetic records, never with engine games."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class ProbeReportingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / 'state/agent_experiments/c151_shop_probe_20260914/run_probe.py'
        spec = importlib.util.spec_from_file_location('report_test_probe', path)
        cls.probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.probe)
        cls.meta = cls.probe.read(cls.probe.MANIFEST)

    def records(self):
        records = []
        for job in self.meta['jobs']:
            row = {'match_id': job['match_id'], 'valid': True, 'seed': job['seed'],
                   'candidate_seat': job['candidate_seat'], 'opponent_name': job['opponent']['name'],
                   'opponent_family': job['opponent']['family'], 'outcome': 'tie', 'margin': 0,
                   'rewards': [100, 100], 'action_hashes': ['same', 'same'], 'shops': ['PET_CAFE'],
                   'candidate_telemetry': {'nested': {'data': 4}, 'carrot_rotation_conversions': 0},
                   'opponent_telemetry': {}, 'candidate_timing': {}, 'opponent_timing': {}}
            records.append((job, row))
        return records

    def summarize(self, records):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(self.probe, 'HERE', Path(temp)), contextlib.redirect_stdout(io.StringIO()):
                self.probe.summary(self.meta, records, 0)
            return json.loads((Path(temp) / 'results.json').read_text(encoding='utf-8'))

    def test_ties_inactivity_never_count_as_improvement(self):
        result = self.summarize(self.records())
        self.assertFalse(result['development_gate_passed'])
        self.assertFalse(result['promotion_authorized'])
        self.assertEqual(result['paired']['changed_conditions'], 0)
        self.assertEqual(result['by_candidate']['c151']['ties'], 64)

    def test_uniform_improvement_requires_further_validation(self):
        records = self.records()
        for job, row in records:
            if job['candidate']['name'] == 'c151':
                seat = row['candidate_seat']
                row.update(outcome='win', margin=10)
                row['rewards'][seat] += 10
                row['action_hashes'][seat] = 'changed'
                row['candidate_telemetry']['carrot_rotation_conversions'] = 1
        result = self.summarize(records)
        self.assertTrue(result['development_gate_passed'])
        self.assertFalse(result['promotion_authorized'])
        self.assertEqual(result['paired']['point_delta'], 32)
        self.assertEqual(result['paired']['own_cash_delta'], 640)

    def test_one_subgroup_regression_blocks_positive_average(self):
        records = self.records()
        for job, row in records:
            if job['candidate']['name'] == 'c151':
                seat = row['candidate_seat']
                margin = -30 if row['opponent_name'] == 'nagata' else 50
                row.update(outcome='loss' if margin < 0 else 'win', margin=margin)
                row['rewards'][seat] += margin
                row['action_hashes'][seat] = 'changed'
        result = self.summarize(records)
        self.assertGreater(result['paired']['point_delta'], 0)
        self.assertFalse(result['development_gate_passed'])
        self.assertLess(result['paired_subgroups']['opponent:nagata']['point_delta'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
