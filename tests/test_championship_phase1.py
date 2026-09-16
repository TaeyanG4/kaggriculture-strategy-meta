import unittest

from src.kaggriculture_meta.championship_phase1 import paired_comparison, require_valid
from src.kaggriculture_meta.replay_accounting import stock


class PhaseOneContracts(unittest.TestCase):
    def test_internal_error_cannot_be_hidden_by_completed_win(self):
        row = {'valid': True, 'margin': 100, 'candidate_telemetry': {'repair_errors': 1}}
        with self.assertRaisesRegex(ValueError, 'Internal'):
            require_valid([row], 1)
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            require_valid([], 1)

    def test_pairing_uses_opponent_bytes_and_seat(self):
        left = [{'seed': 1, 'candidate_seat': 0, 'opponent_sha256': 'A',
                 'opponent_name': 'same-name', 'opponent_family': 'related', 'margin': 1}]
        right = [dict(left[0], opponent_sha256='B')]
        with self.assertRaisesRegex(ValueError, 'Panels'):
            paired_comparison(left, right)
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            paired_comparison(left * 2, left * 2)

    def test_tie_delta_and_degenerate_interval_are_explicit(self):
        left = [{'seed': seed, 'candidate_seat': seat, 'opponent_sha256': 'A',
                 'opponent_name': 'other', 'opponent_family': 'related', 'margin': -10}
                for seed in (1, 2) for seat in (0, 1)]
        right = [dict(r, margin=0) for r in left]
        result = paired_comparison(left, right)
        self.assertEqual(result['score_rate_delta'], .5)
        self.assertEqual(result['losses_to_wins'], 0)
        self.assertIsNone(result['seed_block_bootstrap_95'])

    def test_shed_transfer_is_not_production(self):
        a = {'shed': {'WHEAT': 3}, 'inventories': [{'WHEAT': 2}, {}]}
        b = {'shed': {'WHEAT': 1}, 'inventories': [{'WHEAT': 2}, {'WHEAT': 2}]}
        self.assertEqual(stock(a), stock(b))


if __name__ == '__main__':
    unittest.main()
