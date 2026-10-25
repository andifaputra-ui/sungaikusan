"""Offline bounded-read and provenance regression tests; no network or source pixel reads."""
from pathlib import Path
import io
import json
import tempfile
import unittest
from unittest.mock import patch
from acquire_four import body_fetch

ROOT=Path(__file__).resolve().parent


class BudgetMock:
    """A pre-reserved synthetic budget recording every received byte."""
    def __init__(self,maximum: int) -> None:
        self.credit=maximum;self.received=0;self.saved=False

    def after_read(self,amount: int) -> None:
        if amount>self.credit:
            raise AssertionError('Unreserved body read')
        self.credit-=amount;self.received+=amount

    def save(self) -> None:
        self.saved=True


class Response(io.BytesIO):
    """HTTP-like body with deterministic content length."""
    def __init__(self,data: bytes,declared: int | None=None) -> None:
        super().__init__(data);self.headers={} if declared is None else {'Content-Length':str(declared)}


class FourChipChecks(unittest.TestCase):
    """Test ceiling handling and transparent reference revision provenance."""

    def test_small_body_is_recorded_without_overread(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            budget=BudgetMock(16);path=Path(tmp)/'example.tif'
            with patch('acquire_four.urlopen',return_value=Response(b'abc')):
                result=body_fetch('https://unit.invalid',path,budget,16)
            self.assertEqual(result['bytes'],3);self.assertEqual(path.read_bytes(),b'abc')
            self.assertEqual(budget.received,3);self.assertTrue(budget.saved)

    def test_exact_limit_is_retained_as_partial_without_extra_byte(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            budget=BudgetMock(16);path=Path(tmp)/'example.tif'
            with patch('acquire_four.urlopen',return_value=Response(b'a'*100)):
                with self.assertRaises(RuntimeError):
                    body_fetch('https://unit.invalid',path,budget,16)
            self.assertEqual(budget.received,16)
            self.assertFalse(path.exists());self.assertEqual(path.with_suffix('.part').stat().st_size,16)

    def test_oversized_declaration_fails_before_body(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            budget=BudgetMock(16);path=Path(tmp)/'example.tif'
            with patch('acquire_four.urlopen',return_value=Response(b'a'*100,100)):
                with self.assertRaises(RuntimeError):
                    body_fetch('https://unit.invalid',path,budget,16)
            self.assertEqual(budget.received,0);self.assertTrue(budget.saved)

    def test_revision_refresh_changes_no_frozen_product_or_other_metadata(self) -> None:
        parent=ROOT.parent.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'
        previous=json.loads((parent/'OPTICAL_SOURCE_MATCH_FREEZE.json').read_text())['matches']
        by_id={v['image_id']:v for v in previous.values()}
        refresh=json.loads((ROOT/'REFRESHED_SOURCE_MATCH_FREEZE.json').read_text())
        self.assertEqual(len(refresh['matches']),4)
        for identifier,value in refresh['matches'].items():
            old={k:v for k,v in by_id[identifier]['metadata'].items() if k!='version'}
            new={k:v for k,v in value['metadata'].items() if k!='version'}
            self.assertEqual(old,new)
        result=json.loads((ROOT/'REFRESHED_ATTEMPT/ACQUISITION_SUMMARY.json').read_text())
        self.assertLessEqual(result['new_metered_body_bytes'],4*1024**2)
        self.assertLessEqual(result['new_conservative_charge_bytes'],4*1024**2)
        self.assertEqual(result['outcomes'],{'ACQUIRED_NOT_INTERPRETED':4})


if __name__=='__main__':
    unittest.main(verbosity=2)
