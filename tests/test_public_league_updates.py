"""Provisional BT and owner file upload regression checks."""
import io
import math
import tarfile
import unittest
from unittest.mock import patch

from tests import test_public_league as fixtures
from src.kaggriculture_meta import public_league as league

AGENT = fixtures.AGENT


class ProvisionalRatingTests(unittest.TestCase):
    def test_newcomer_moves_faster_in_both_directions(self):
        anchors = [{"agent_a": 1, "agent_b": 2, "outcome_a": .5}] * 400
        for outcome in (0, 1):
            rows = anchors + [{"agent_a": 3, "agent_b": 1, "outcome_a": outcome}] * 8
            new = league.bradley_terry_ratings([1, 2, 3], rows)
            old = league.bradley_terry_ratings([1, 2, 3], rows, provisional_games=0)
            self.assertGreater(abs(new[3] - new[1]), abs(old[3] - old[1]))
            self.assertEqual(new[3] > new[1], outcome == 1)

    def test_taper_and_exact_mature_equivalence(self):
        fractions = [league.rating_prior_fraction(n) for n in (0, 16, 32, 64, 128, 1000)]
        self.assertEqual(fractions, [.25, .34375, .4375, .625, 1, 1])
        rows = ([{"agent_a": 1, "agent_b": 2, "outcome_a": 1}] * 100
                + [{"agent_a": 1, "agent_b": 2, "outcome_a": 0}] * 60)
        self.assertEqual(league.bradley_terry_ratings([1, 2], rows),
                         league.bradley_terry_ratings([1, 2], rows, provisional_games=0))

    def test_no_games_and_ties_stay_neutral(self):
        rows = [{"agent_a": 1, "agent_b": 2, "outcome_a": .5}] * 8
        self.assertEqual(league.bradley_terry_ratings([1, 2, 3], rows),
                         {1: 1500.0, 2: 1500.0, 3: 1500.0})

    def test_unequal_priors_fit_objective_and_ignore_row_order(self):
        rows = ([{"agent_a": 1, "agent_b": 2, "outcome_a": 1}] * 150
                + [{"agent_a": 2, "agent_b": 1, "outcome_a": 1}] * 50
                + [{"agent_a": 3, "agent_b": 1, "outcome_a": 1}] * 8
                + [{"agent_a": 3, "agent_b": 2, "outcome_a": 0}] * 2)
        ratings = league.bradley_terry_ratings([1, 2, 3, 4], rows)
        reversed_ratings = league.bradley_terry_ratings([1, 2, 3, 4], list(reversed(rows)))
        for ident in ratings:
            self.assertAlmostEqual(ratings[ident], reversed_ratings[ident], places=7)
        theta = {i: (r - 1500) * math.log(10) / 400 for i, r in ratings.items()}
        counts = {i: sum(i in (r['agent_a'], r['agent_b']) for r in rows) for i in theta}
        gradient = {i: -league.rating_prior_fraction(counts[i]) * theta[i] for i in theta}
        for row in rows:
            a, b = row['agent_a'], row['agent_b']
            residual = row['outcome_a'] - 1 / (1 + math.exp(theta[b] - theta[a]))
            gradient[a] += residual; gradient[b] -= residual
        self.assertLess(max(abs(g) for g in gradient.values()), 1e-6)


class LocalUploadTests(unittest.TestCase):
    setUp = fixtures.PublicLeagueTests.setUp
    tearDown = fixtures.PublicLeagueTests.tearDown

    @staticmethod
    def archive(files):
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
            for name, data in files.items():
                member = tarfile.TarInfo(name); member.size = len(data)
                archive.addfile(member, io.BytesIO(data))
        return buffer.getvalue()

    def test_upload_and_exact_repeat_preserve_games_and_micro_edit_is_new(self):
        with patch.object(league, 'qa_source', return_value={'ok': True, 'entrypoint': 'agent'}) as qa:
            first = league.register_local_upload(self.store, 'my.py', AGENT.encode(), 'My Agent')
            with self.store.db:
                self.store.db.execute('UPDATE agents SET games=150,rating=2200 WHERE id=?', (first['agent_id'],))
            second = league.register_local_upload(self.store, 'another.tar.gz',
                self.archive({'main.py': AGENT.encode()}))
            self.assertEqual(first['agent_id'], second['agent_id'])
            self.assertEqual(second['duplicate_type'], 'exact_source_duplicate')
            self.assertEqual(second['games'], 150)
            self.assertEqual(self.store.db.execute('SELECT rating FROM agents').fetchone()[0], 2200)
            self.assertEqual(qa.call_count, 1)
            link = 'https://www.kaggle.com/competitions/kaggriculture/submissions?submissionId=123'
            before = self.store.db.execute('SELECT discovered_at FROM aliases').fetchone()[0]
            linked = league.register_local_upload(self.store, 'same.py', AGENT.encode(), 'Submitted Agent', link)
            league.register_local_upload(self.store, 'same.py', AGENT.encode())
            self.assertEqual(linked['agent_id'], first['agent_id'])
            self.assertEqual(linked['games'], 150)
            alias = self.store.db.execute('SELECT notebook_title,notebook_url,discovered_at FROM aliases').fetchone()
            self.assertEqual(tuple(alias), ('Submitted Agent', link, before))
            notebook = self.store.db.execute('SELECT title,url FROM notebooks').fetchone()
            self.assertEqual(tuple(notebook), ('Submitted Agent', link))
            self.assertEqual(self.store.db.execute('SELECT rating FROM agents').fetchone()[0], 2200)
            self.assertEqual(qa.call_count, 1)
            edited = league.register_local_upload(self.store, 'edited.py', (AGENT + '\n# tiny edit\n').encode())
            self.assertNotEqual(first['agent_id'], edited['agent_id'])
            self.assertEqual(edited['duplicate_type'], 'unique_artifact')

    def test_bundle_preserves_sidecar_identity_and_platform(self):
        with patch.object(league, 'qa_source', return_value={'ok': True, 'entrypoint': 'agent'}) as qa:
            payload = self.archive({'main.py': AGENT.encode(), 'agent.so': b'linux-binary'})
            result = league.register_local_upload(self.store, 'bundle.tgz', payload)
            self.assertEqual(result['execution_platform'], 'linux')
            self.assertEqual(result['artifact_files'], ['agent.so', 'main.py'])
            self.assertEqual(qa.call_args.kwargs['execution_platform'], 'linux')
            duplicate = league.register_local_upload(self.store, 'bundle.tgz', payload)
            self.assertEqual(duplicate['duplicate_type'], 'exact_artifact_duplicate')

    def test_code_failure_is_quarantined(self):
        result = league.register_local_upload(self.store, 'broken.py', b'def agent(:\n')
        self.assertEqual(result['status'], 'quarantine')
        self.assertEqual(result['qa_status'], 'failed')
        with patch.object(league, 'qa_source', return_value={'ok': False, 'error': 'TypeError'}):
            result = league.register_local_upload(self.store, 'bad-return.py', AGENT.encode())
            self.assertEqual(result['status'], 'quarantine')

    def test_invalid_or_ambiguous_archives_do_not_register(self):
        for files in ({'../main.py': AGENT.encode()},
                      {'main.py': AGENT.encode(), '../sidecar': b'bad'},
                      {'a/main.py': AGENT.encode(), 'b/main.py': AGENT.encode()},
                      {'helper.py': AGENT.encode()}):
            with self.assertRaises(ValueError):
                league.register_local_upload(self.store, 'bad.tar.gz', self.archive(files))
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM agents').fetchone()[0], 0)


if __name__ == '__main__':
    unittest.main()
