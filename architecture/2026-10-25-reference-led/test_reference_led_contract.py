"""Offline checks for preserved scope, hypotheses, positive geography and request bounds."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT=Path(__file__).resolve().parent


class ReferenceLedChecks(unittest.TestCase):
    """Prevent an unqualified site, label or fresh acquisition being silently promoted."""

    def test_screen_accounts_for_every_fixed_view(self) -> None:
        screen=json.loads((ROOT/'DISCOVERY_SCREEN_NOTES.json').read_text(encoding='utf-8'))
        aliases=[alias for group in screen['groups'] for alias in group['aliases']]
        self.assertEqual(len(aliases),62)
        self.assertEqual(set(aliases),{f'L{i:02d}' for i in range(1,63)})

    def test_frozen_sites_remain_development_and_on_lattice(self) -> None:
        path=ROOT/'NOMINATION_FREEZE.json'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),(ROOT/'NOMINATION_FREEZE.sha256').read_text().strip())
        result=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(result['systems'],4);self.assertEqual(result['date_supports'],4)
        for row in result['records']:
            self.assertTrue(row['development_only'])
            self.assertTrue(row['full_position_neighbourhood_inside_L1'])
            self.assertEqual(row['qualification'],'PENDING_OPTICAL_SUPPORT_AND_TIME; NOT_CLASS_TRUTH')

    def test_new_requests_not_authorized_and_within_retained_ceiling(self) -> None:
        path=ROOT/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.json'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),(ROOT/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.sha256').read_text().strip())
        plan=json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(len(plan['requests']),4)
        self.assertEqual(plan['maximum_new_response_body_bytes'],4*1024**2)
        self.assertLess(plan['maximum_cumulative_charge_after_four_new_1MiB_reservations'],1024**3)
        for row in plan['requests']:
            self.assertFalse(row['acquisition_authorized'])
            self.assertTrue(row['full_chip_inside_recorded_STAC_footprint'])
            self.assertTrue(all(check['status']=='WINDOW_POLICY_CHECK_PASSED_NOT_AN_IO_OPERATION'
                for check in row['native_window_feasibility_checks']))

    def test_old_panel_and_response_locks_unchanged(self) -> None:
        parent=ROOT.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'
        lock=json.loads((parent/'RESPONSE_LOCK.json').read_text(encoding='utf-8'))
        for name,digest in lock['files'].items():
            self.assertEqual(hashlib.sha256((parent/name).read_bytes()).hexdigest(),digest)
        for stem in ['REFERENCE_PANEL_FREEZE','REFERENCE_SOURCE_PLAN_V2']:
            self.assertEqual(hashlib.sha256((parent/(stem+'.json')).read_bytes()).hexdigest(),
                (parent/(stem+'.sha256')).read_text().strip())


if __name__=='__main__':
    unittest.main(verbosity=2)
