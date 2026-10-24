"""Offline regression checks for conservative cumulative transfer accounting."""
from pathlib import Path
import json
import tempfile
import unittest
from resource_budget import Budget


class BudgetTests(unittest.TestCase):
    def test_reservation_is_persisted_before_failed_read(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)/'budget.json'
            first = Budget(state)
            first.before_read(100)
            charged = first.data['charged_bytes']
            restored = Budget(state)
            self.assertEqual(restored.data['charged_bytes'], charged)
            self.assertEqual(restored.credit, 0)

    def test_limit_rejects_before_read(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)/'budget.json'
            budget = Budget(state)
            budget.data['limit_bytes'] = budget.data['charged_bytes']+10
            with self.assertRaises(RuntimeError):
                budget.before_read(11)

    def test_received_and_charged_are_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            budget = Budget(Path(directory)/'budget.json')
            budget.before_read(1024)
            budget.after_read(512)
            self.assertEqual(budget.data['received_metered_bytes'],512)
            self.assertGreaterEqual(budget.data['charged_bytes'],512)
            with self.assertRaises(RuntimeError):
                budget.after_read(budget.credit+1)


if __name__ == '__main__':
    result = unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(BudgetTests))
    (Path(__file__).parent/'RESOURCE_TESTS.json').write_text(json.dumps({
        'status':'PASS' if result.wasSuccessful() else 'FAIL', 'tests':result.testsRun,
        'scope':'OFFLINE_SYNTHETIC_BUDGET_ONLY'},indent=2)+'\n',encoding='utf-8')
    raise SystemExit(not result.wasSuccessful())
