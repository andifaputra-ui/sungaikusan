"""Synthetic regressions only; no imagery, source pixels or reader responses."""
from pathlib import Path
import json, unittest
import numpy as np
from optical_display_contract import ContractError, legacy_display, verified_raw_dn, render, scl_evidence

def meta(offset=-0.1): return [dict(scale=.0001,offset=offset,nodata=0) for _ in range(4)]
def legacy(a, **kw):
    args=dict(source_collection='sentinel-2-l2a',source_host='sentinel-cogs.s3.us-west-2.amazonaws.com',bands=meta(),baseline='05.11',boa_offset_applied=True)
    args.update(kw)
    return legacy_display(a,**args)
def verified(a, **kw):
    args=dict(nodata=0,scale=[.0001]*4,offset=[-.1]*4,contract_id='SYNTHETIC_PROOF_ONLY',exact_asset_verified=True)
    args.update(kw)
    return verified_raw_dn(a,**args)

class Safeguards(unittest.TestCase):
    def test_legacy_no_double_offset(self):
        f=legacy(np.full((4,1,1),1000));np.testing.assert_allclose(f.values,.1);self.assertFalse(f.quantitative_allowed);self.assertTrue(f.provenance['metadata_offset_conflict'])
    def test_legacy_prebaseline_consistent(self):
        f=legacy(np.full((4,1,1),1000),bands=meta(0),baseline='02.14',boa_offset_applied=False);self.assertFalse(f.provenance['metadata_offset_conflict']);self.assertFalse(f.quantitative_allowed)
    def test_nodata_before_offset(self):
        a=np.tile([0,1,1000,1100],(4,1,1));f=verified(a);self.assertTrue(np.isnan(f.values[:,0,0]).all());np.testing.assert_allclose(f.values[:,0,1],-.0999);np.testing.assert_allclose(f.values[:,0,2],0,atol=1e-15)
    def test_valid_negative_not_erased(self):
        f=verified(np.full((4,1,1),500));render(f);np.testing.assert_allclose(f.values,-.05);self.assertTrue(f.valid_by_band.all())
    def test_legacy_dn_one_is_not_missing(self):
        f=legacy(np.ones((4,1,1)));self.assertTrue(f.valid_by_band.all());np.testing.assert_allclose(f.values,.0001)
    def test_transformed_object_rejected(self):
        with self.assertRaises(ContractError):legacy(legacy(np.ones((4,1,1))))
    def test_autoscaled_reader_rejected(self):
        with self.assertRaises(ContractError):legacy(np.ones((4,1,1)),raw_representation='REFLECTANCE')
    def test_unproved_quantitative_rejected(self):
        with self.assertRaises(ContractError):verified(np.ones((4,1,1)),exact_asset_verified=False)
    def test_already_applied_quantitative_rejected(self):
        with self.assertRaises(ContractError):verified(np.ones((4,1,1)),already_applied=True)
    def test_unknown_encoding_rejected(self):
        with self.assertRaises(ContractError):verified(np.ones((4,1,1)),already_applied=None)
    def test_missing_scale_rejected(self):
        b=meta();b[0].pop('scale')
        with self.assertRaises(ContractError):legacy(np.ones((4,1,1)),bands=b)
    def test_other_provider_not_silently_accepted(self):
        with self.assertRaises(ContractError):legacy(np.ones((4,1,1)),source_host='sentinel2l2a01.blob.core.windows.net')
    def test_fractional_dn_rejected(self):
        with self.assertRaises(ContractError):legacy(np.full((4,1,1),.2))
    def test_composite_specific_nodata(self):
        a=np.full((4,1,1),1000);a[3]=0;f=legacy(a);rgb,m=render(f,'RGB');nir,n=render(f,'NIR');self.assertEqual(m['valid_fraction'],1);self.assertEqual(n['valid_fraction'],0);np.testing.assert_equal(nir[0,0],[145]*3)
    def test_nodata_grey_not_dark(self):
        image,m=render(legacy(np.zeros((4,1,1))));np.testing.assert_equal(image[0,0],[145]*3);self.assertEqual(m['valid_fraction'],0)
    def test_display_clipping_separate(self):
        f=legacy(np.full((4,1,1),9000));image,m=render(f);np.testing.assert_equal(image[0,0],[255]*3);np.testing.assert_allclose(f.values,.9);self.assertEqual(m['channel_values_above_display_ceiling'],3)
    def test_scl7_is_not_cloud(self):
        q=scl_evidence(np.array([[7]]),baseline='05.11');self.assertTrue(q['unclassified'][0,0]);self.assertFalse(q['cloud_or_cirrus'][0,0])
    def test_scl2_baseline_semantics(self):
        self.assertEqual(scl_evidence(np.array([[2]]),baseline='00.01')['scl2_semantics'],'DARK_FEATURES_SHADOWS');self.assertEqual(scl_evidence(np.array([[2]]),baseline='05.11')['scl2_semantics'],'CAST_SHADOWS')
    def test_no_scl_water_label(self):
        q=scl_evidence(np.array([[4,5,6]]),baseline='05.11');self.assertNotIn('water',q);self.assertNotIn('nonwater',q)
    def test_scl_fractional_rejected(self):
        with self.assertRaises(ContractError):scl_evidence(np.array([[5.5]]),baseline='05.11')
    def test_scl_outside_legend_rejected(self):
        with self.assertRaises(ContractError):scl_evidence(np.array([[12]]),baseline='05.11')
    def test_perband_offset(self):
        f=verified(np.full((4,1,1),2000),offset=[-.1,-.09,-.08,-.07]);np.testing.assert_allclose(f.values[:,0,0],[.1,.11,.12,.13])

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Safeguards)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    out=Path(__file__).with_name('SYNTHETIC_TEST_RESULTS.json')
    if out.exists(): raise FileExistsError(out)
    out.write_text(json.dumps({'tests_run':result.testsRun,'errors':len(result.errors),'failures':len(result.failures),'status':'PASS' if result.wasSuccessful() else 'FAIL','scope':'SYNTHETIC_ONLY_NO_RESEARCH_PIXELS','test_names':sorted(x for x in dir(Safeguards) if x.startswith('test_'))},indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
