"""Interpretation bookkeeping tests, never tests of semantic truth."""
import unittest
from account_optical_responses import scenarios


class ResponseChecks(unittest.TestCase):
    """Ensure unknown mass and displaced boundary ambiguity survive accounting."""

    def test_nonwater_and_unknown_remain_distinct(self) -> None:
        self.assertEqual(scenarios(['N'*9]*9,30)['possible_water_bounds'],[0,0])
        self.assertEqual(scenarios(['U'*9]*9,30)['possible_water_bounds'],[0,1])
        self.assertEqual(scenarios(['O'*9]*9,30)['possible_water_bounds'],[0,1])

    def test_shoreline_loses_purity_under_displacement(self) -> None:
        result=scenarios(['NNUUUWWWW']*9,30)
        self.assertAlmostEqual(result['nominal']['W'],1/3)
        self.assertEqual(result['possible_water_bounds'],[0,1])
        self.assertEqual(len(result['scenarios']),25)
        for row in result['scenarios']:
            self.assertAlmostEqual(sum(row[k] for k in 'WNOU'),1)

    def test_invalid_annotation_rejected(self) -> None:
        with self.assertRaises(ValueError):
            scenarios(['X'*9]*9,30)


if __name__=='__main__':
    unittest.main(verbosity=2)
