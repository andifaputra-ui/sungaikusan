"""Offline tests of acquisition/production semantics, coverage and protected roles."""
from pathlib import Path
from datetime import datetime,timezone
import ast
import json
import hashlib
import unittest
from analyze_metadata_feasibility import acquisition_interval,parent_identifier

ROOT=Path(__file__).resolve().parent


class MetadataChecks(unittest.TestCase):
    """Prevent a later processing timestamp or archive variant from repairing missing truth."""

    def test_GRD_acquisition_start_and_end_are_distinct(self) -> None:
        start,end=acquisition_interval('S1A_IW_GRDH_1SDV_20250511T220024_20250511T220049_059152_0756E5_4873')
        self.assertEqual((end-start).total_seconds(),25)
        self.assertEqual(start,datetime(2025,5,11,22,0,24,tzinfo=timezone.utc))

    def test_parent_file_variants_deduplicate(self) -> None:
        base='OPERA_L2_RTC-S1_T105-example'
        self.assertEqual({parent_identifier(base+ending) for ending in ['.h5','_VV.tif','_VH.tif','_mask.tif']},{base})

    def test_search_interval_covers_all_closer_time_opportunities(self) -> None:
        summary=json.loads((ROOT/'FEASIBILITY_SUMMARY.json').read_text())
        self.assertTrue(summary['window_is_wide_enough_to_find_any_closer_record_if_present_in_queried_catalogues'])
        for key,gap in summary['nearest_optical_offsets_hours'].items():
            self.assertGreater(summary['minimum_absolute_offset_outside_search_window_hours'][key],abs(gap))

    def test_query_scripts_have_no_pixel_or_export_calls(self) -> None:
        forbidden={'getDownloadURL','getThumbURL','getMapId','reduceRegion','sample','sampleRegions','getRegion','getPixels','computePixels'}
        for filename in ['query_native_metadata.py','query_opera_metadata.py','query_asf_metadata.py']:
            tree=ast.parse((ROOT/filename).read_text())
            calls={n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)}
            self.assertFalse(calls&forbidden)

    def test_reference_response_locks_preserved(self) -> None:
        branch=ROOT.parent/'REFERENCE_LED_DEVELOPMENT_20261025'
        for directory,name in [(branch,'BRANCH_LOCK.json'),(branch/'FOUR_CHIP_EXECUTION','REFERENCE_RESPONSE_LOCK.json')]:
            lock=json.loads((directory/name).read_text())
            for file,sha in lock['files'].items():
                self.assertEqual(hashlib.sha256((directory/file).read_bytes()).hexdigest(),sha)


if __name__=='__main__':
    unittest.main(verbosity=2)
