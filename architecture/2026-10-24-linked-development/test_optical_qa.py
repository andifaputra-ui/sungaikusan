"""Source scaling, QA-semantic separation and support accounting regressions."""
import unittest
import numpy as np
from optical_qa import reflectance,diagnostic_qa,support_scenarios


class OpticalChecks(unittest.TestCase):
    """Test cases where a QA/radiometry mistake could silently generate labels."""

    def test_scaling_preserves_negative_and_harmonized_values(self) -> None:
        self.assertAlmostEqual(reflectance(np.array([1000]),'S2')[0],0.1)
        self.assertAlmostEqual(reflectance(np.array([0]),'LS')[0],-0.2)
        self.assertGreater(reflectance(np.array([65535]),'LS')[0],1)

    def test_source_water_code_never_generates_quality_or_class(self) -> None:
        s2=np.zeros((5,2,2));s2[4]=np.array([[2,4],[5,6]])
        available,flagged=diagnostic_qa(s2,'S2',np.ones_like(s2))
        self.assertTrue(available.all());self.assertFalse(flagged.any())
        ls=np.zeros((6,2,2));ls[4]=128
        available,flagged=diagnostic_qa(ls,'LS',np.ones_like(ls))
        self.assertTrue(available.all());self.assertFalse(flagged.any())
        ls[4,0,0]=136
        self.assertTrue(diagnostic_qa(ls,'LS',np.ones_like(ls))[1][0,0])

    def test_missing_quality_remains_unavailable(self) -> None:
        ls=np.zeros((6,2,2));masks=np.ones_like(ls);masks[4,0,0]=0
        self.assertFalse(diagnostic_qa(ls,'LS',masks)[0][0,0])

    def test_support_counts_and_displacement(self) -> None:
        valid=np.ones((49,49),bool);flagged=np.zeros_like(valid);flagged[24,24]=True
        for support,expected in [(10,1),(30,1/9),(50,1/25)]:
            result=support_scenarios(valid,flagged,support)
            self.assertEqual(len(result['scenarios']),25)
            self.assertAlmostEqual(result['nominal']['qa_flagged_fraction'],expected)


if __name__=='__main__':
    unittest.main(verbosity=2)
