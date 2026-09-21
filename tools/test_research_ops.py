"""Regression checks for evidence handling; no simulations or frozen writes."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import research_ops as R


class ResearchOpsTests(unittest.TestCase):
    def test_subset_preserves_per_hypothesis_alpha_and_sources(self):
        path=R.ROOT/'configs/validation/c354_gemini_audit_v2.json'
        before=path.read_bytes(); old=R.read(path); new=R.subset(path,'g001,v9')
        self.assertEqual(set(new['models']),{'g001','v9'})
        self.assertEqual(new['opponents'],old['opponents'])
        self.assertEqual(new['models']['g001'],old['models']['g001'])
        for stage in old['stages']:
            self.assertEqual(new['stages'][stage]['alpha'],old['stages'][stage]['alpha']/2)
            self.assertEqual(new['stages'][stage]['seeds'],old['stages'][stage]['seeds'])
        self.assertEqual(path.read_bytes(),before)
        with self.assertRaises(ValueError):R.subset(path,'g001')

    def test_completed_campaign_recalculates_and_rejects_wrong_aggregate(self):
        path=R.ROOT/'state/agent_experiments/c354_g001_confirm_v2'
        summary=R.summarize(path)
        self.assertEqual(summary['games'],384)
        self.assertEqual(summary['counts']['g001']['wins'],154)
        self.assertEqual(summary['comparisons']['g001_vs_v9']['signal'],'inconclusive')
        original=R.read
        def corrupt(p):
            value=original(p)
            if Path(p)==path/'results.json':
                value=copy.deepcopy(value);value['by_candidate']['g001']['wins']+=1
            return value
        with patch.object(R,'read',corrupt):
            with self.assertRaisesRegex(ValueError,'aggregate differs'):R.summarize(path)

    def test_incomplete_rows_cannot_produce_performance(self):
        import validation_v2 as V
        with patch.object(V,'load_rows',return_value=[]):
            with self.assertRaisesRegex(ValueError,'Incomplete campaign'):
                R.summarize(R.ROOT/'state/agent_experiments/c354_g001_confirm_v2')

    def test_output_never_overwrites_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'manifest.json';p.write_text('preserved')
            with self.assertRaises(FileExistsError):R.output({'changed':True},p)
            self.assertEqual(p.read_text(),'preserved')


if __name__=='__main__':unittest.main()
