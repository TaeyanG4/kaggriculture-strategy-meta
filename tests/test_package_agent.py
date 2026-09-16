from pathlib import Path
import tempfile
import unittest

from src.kaggriculture_meta.package_agent import package, source_audit


class PackageTests(unittest.TestCase):
    def test_deterministic_archive_and_no_silent_overwrite(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as tmp:
            root = Path(tmp)
            source = root/'agent.py'
            source.write_text("def agent(obs, config): return {'farmer':['PASS']}\n", encoding='utf-8')
            first = package(source, root/'out')
            self.assertEqual(first, package(source, root/'out'))
            source.write_text(source.read_text(encoding='utf-8')+'\n# change\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'overwrite'):
                package(source, root/'out')

    def test_audit_descends_into_literal_exec(self):
        with self.assertRaisesRegex(ValueError, 'capability'):
            source_audit('exec("open(\'secret\')")')
        with self.assertRaisesRegex(ValueError, 'Nonliteral'):
            source_audit('exec(payload)')


if __name__ == '__main__':
    unittest.main()
