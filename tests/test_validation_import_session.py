import unittest
from unittest.mock import patch
from tests import test_bounded_validation_import as fixtures
from tools.validation_import_session import ValidationSession
from tools import import_validation_league as bulk
from tools import bounded_validation_import as bounded

class SessionBoundedTests(unittest.TestCase):
    ref=fixtures.BoundedImportTests.ref
    write=fixtures.BoundedImportTests.write
    freeze_plan=fixtures.BoundedImportTests.freeze_plan
    def setUp(self):
        fixtures.BoundedImportTests.setUp(self)
        self.session=ValidationSession();self.session.__enter__()

    def tearDown(self):
        self.session.__exit__(None,None,None)
        fixtures.BoundedImportTests.tearDown(self)

    def test_manifest_rows_files_equal_original(self):
        self.session.__exit__(None,None,None)
        original=bounded.collect(self.campaign)
        self.session=ValidationSession();self.session.__enter__()
        actual=bounded.collect(self.campaign)
        self.assertEqual(actual,original)
        self.session.verify_all()

    def test_repeated_ancestor_identical_and_final_hash_check(self):
        bounded.seal_bounded(self.campaign)
        first=bounded.checked_bounded(self.campaign)
        again=bounded.checked_bounded(self.campaign)
        self.assertEqual(first,again)
        self.assertEqual(self.session.campaign_hits,1)
        self.session.verify_all()

    def test_modified_file_rejected_after_cache(self):
        p=self.campaign/'completion-ready.json'
        bulk.digest(p);p.write_text('{}','utf8')
        with self.assertRaises(bulk.ImportRejected):bulk.digest(p)
        with self.assertRaises(bulk.ImportRejected):self.session.verify_all()

    def test_same_metadata_different_bytes_rejected_at_commit_boundary(self):
        p=self.campaign/'completion-ready.json';old=p.read_bytes();bulk.digest(p)
        sig=self.session.files[p][0]
        p.write_bytes(b' '*len(old))
        with patch.object(self.session,'signature',return_value=sig):
            self.assertEqual(bulk.digest(p),self.session.files[p][1])
            with self.assertRaises(bulk.ImportRejected):self.session.verify_all()

    def test_cached_cycle_still_rejected(self):
        bounded.seal_bounded(self.campaign);bounded.checked_bounded(self.campaign)
        with self.assertRaises(bulk.ImportRejected):bounded.checked_bounded(self.campaign,ancestors=(self.campaign.resolve(),))
