import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AuditTests(unittest.TestCase):
    def setUp(self):
        script = ROOT / 'audit.py'
        self.assertTrue(script.exists(), 'audit.py must implement the public utilities')
        spec = importlib.util.spec_from_file_location('audit', script)
        self.audit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.audit)
        self.budget = {
            'global_power_erg_s': {'component_a': 3., 'component_b': 7., 'Htotal': 10.},
            'radial_band_power_erg_s': {
                'inner': {'component_a': 1., 'component_b': 2., 'Htotal': 3.},
                'outer': {'component_a': 2., 'component_b': 5., 'Htotal': 7.},
            },
        }

    def test_valid_partition(self):
        self.assertEqual(self.audit.validate_budget(self.budget)['total_power_erg_s'], 10.)

    def test_invalid_component_total(self):
        self.budget['global_power_erg_s']['Htotal'] = 11.
        with self.assertRaises(ValueError):
            self.audit.validate_budget(self.budget)

    def test_partition_must_match_each_component(self):
        self.budget['radial_band_power_erg_s']['inner'].update(component_a=2., component_b=1.)
        with self.assertRaises(ValueError):
            self.audit.validate_budget(self.budget)

    def test_invalid_powers(self):
        for value in (-1., float('nan'), float('inf'), True, '3'):
            with self.subTest(value=value):
                data = copy.deepcopy(self.budget)
                data['global_power_erg_s']['component_a'] = value
                with self.assertRaises(ValueError):
                    self.audit.validate_budget(data)

    def test_tiny_inconsistent_total_rejected(self):
        with self.assertRaises(ValueError):
            self.audit.validate_budget({'global_power_erg_s': {'a': 1e-20, 'Htotal': 2e-20}})

    def test_global_only_supported(self):
        del self.budget['radial_band_power_erg_s']
        self.assertEqual(self.audit.validate_budget(self.budget)['bands_checked'], 0)

    def test_metrics(self):
        result = self.audit.compare_pairs([(3., 1.), (2., 4.)])
        self.assertEqual(result, {'count': 2, 'bias': 0., 'mae': 2., 'rmse': 2.})

    def test_empty_or_nonfinite_pairs_rejected(self):
        for pairs in ([], [(float('nan'), 1.)], [(1., float('inf'))]):
            with self.assertRaises(ValueError):
                self.audit.compare_pairs(pairs)

    def test_example_commands(self):
        for command, filename in [('budget', 'synthetic_budget.json'), ('compare', 'synthetic_pairs.csv')]:
            result = subprocess.run([sys.executable, str(ROOT / 'audit.py'), command,
                                     str(ROOT / 'examples' / filename)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIsInstance(json.loads(result.stdout), dict)


if __name__ == '__main__':
    unittest.main()
