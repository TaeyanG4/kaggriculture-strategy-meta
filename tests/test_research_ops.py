"""Regression checks for descriptive parent exclusion, not promotion gates."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('research_ops', Path(__file__).resolve().parents[1] / 'tools/research_ops.py')
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)


class ParentExclusionTests(unittest.TestCase):
    def test_alias_excluded_but_modified_source_kept(self):
        plan = dict(models={'parent': {'sha256': 'a'*64}}, opponents={
            'c407': {'sha256': 'a'*64}, 'modified': {'sha256': 'b'*64}})
        rows = [dict(opponent='c407', point_delta=1, margin_delta=1000),
                dict(opponent='modified', point_delta=0, margin_delta=10)]
        result = ops.excluding_parent_source(plan, 'parent', rows)
        self.assertEqual(result['n'], 1)
        self.assertEqual(result['excluded_opponents'], ['c407'])
        self.assertEqual(result['point_delta'], 0)
        self.assertEqual(result['margin_delta'], 10)

    def test_name_alone_does_not_exclude_different_source(self):
        plan = dict(models={'parent': {'sha256': 'a'*64}},
                    opponents={'parent': {'sha256': 'b'*64}})
        result = ops.excluding_parent_source(plan, 'parent', [
            dict(opponent='parent', point_delta=0.5, margin_delta=10)])
        self.assertEqual(result['n'], 1)
        self.assertEqual(result['excluded_opponents'], [])

    def test_parent_only_has_no_descriptive_comparison(self):
        plan = dict(models={'parent': {'sha256': 'a'*64}},
                    opponents={'alias': {'sha256': 'a'*64}})
        self.assertIsNone(ops.excluding_parent_source(plan, 'parent', [
            dict(opponent='alias', point_delta=0.5, margin_delta=10)]))


if __name__ == '__main__':
    unittest.main()
