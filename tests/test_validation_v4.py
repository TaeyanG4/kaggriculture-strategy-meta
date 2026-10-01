import hashlib
import sys
import unittest
from collections import ChainMap
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import validation_v4 as v4


class MappingTelemetryRegression(unittest.TestCase):
    def call(self, source):
        times, errors, telemetry = [], [], {}
        fn = v4.timed_policy(source, 'opponent', times, errors, hashlib.sha256(), telemetry)
        action = fn({'step': 718}, {})
        return action, times, errors, telemetry

    def test_chainmap_keeps_terminal_action_and_nested_error_counters(self):
        source = '''from collections import ChainMap
def agent(obs, cfg):
    return {"farmer": ["PASS"], "hands": [], "market": [["SELL", "WOOL", 4]]}
agent.telemetry = ChainMap({"nested": ChainMap({"repair_errors": 2})}, {"calls": 719})
'''
        action, times, errors, telemetry = self.call(source)
        self.assertEqual(action['market'], [['SELL', 'WOOL', 4]])
        self.assertEqual(len(times), 1)
        self.assertEqual(errors, [])
        self.assertEqual(telemetry, {'calls': 719, 'nested': {'repair_errors': 2}})
        self.assertEqual(v4.V3.V.L.positive_error_counters(telemetry), {'nested.repair_errors': 2})

    def test_recorder_failure_marks_error_without_discarding_action(self):
        source = '''def agent(obs, cfg):
    return {"market": [["SELL", "CARROT", 5]]}
agent.telemetry = "invalid telemetry"
'''
        action, times, errors, telemetry = self.call(source)
        self.assertEqual(action, {'market': [['SELL', 'CARROT', 5]]})
        self.assertEqual(len(times), 1)
        self.assertEqual(errors[0]['stage'], 'telemetry')
        self.assertEqual(telemetry, {})

    def test_policy_exception_is_still_raised_and_recorded(self):
        times, errors = [], []
        fn = v4.timed_policy('def agent(obs, cfg):\n    raise RuntimeError("policy failed")\n', 'x', times, errors, hashlib.sha256(), {})
        with self.assertRaisesRegex(RuntimeError, 'policy failed'):
            fn({'step': 718}, {})
        self.assertEqual(len(times), 1)
        self.assertEqual(errors[0]['type'], 'RuntimeError')

    def test_mapping_precedence_and_nonfinite_values_are_preserved(self):
        self.assertEqual(v4.telemetry_snapshot(ChainMap({'x': 1}, {'x': 2, 'nested': [float('inf')]})),
                         {'x': 1, 'nested': ['inf']})


if __name__ == '__main__':
    unittest.main()
