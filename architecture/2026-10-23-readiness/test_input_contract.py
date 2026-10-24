"""Synthetic failure cases; no research rasters, labels or neural inference."""
from __future__ import annotations
from pathlib import Path
import json
import unittest
import numpy as np
from rasterio.io import MemoryFile
from rasterio.transform import from_origin
from input_contract import (InputContractError,current_validity,context_validity,
                            final_support,validate_stats,validate_output_grid)


class ContractTests(unittest.TestCase):
    def test_partial_current_band_nodata_defeats_dataset_mask(self):
        x=np.ones((3,3,3),np.float32);x[1,1,1]=-9999
        with MemoryFile() as memory:
            with memory.open(driver='GTiff',width=3,height=3,count=3,dtype='float32',nodata=-9999,
                             transform=from_origin(380000,9610000,10,10),crs=32750) as dataset:
                dataset.write(x)
                union=dataset.dataset_mask()!=0
                band_valid=dataset.read_masks()!=0
                required=current_validity(dataset.read(),band_valid)
        self.assertTrue(union[1,1])
        self.assertFalse(required[1,1])
        self.assertEqual(int(required.sum()),8)

    def test_nonfinite_current_not_filled_by_context(self):
        x=np.ones((3,2,2),np.float32);x[0,0,0]=np.nan
        valid=current_validity(x,np.ones(x.shape,bool))
        self.assertFalse(final_support(valid,np.ones((2,2),bool))[0,0])

    def test_current_only_retains_support_without_context(self):
        mask=np.array([[True,False]],bool)
        self.assertTrue(np.array_equal(mask,final_support(mask)))

    def test_source_nodata_any_context_band_rejected(self):
        x=np.zeros((64,2,2),np.int8);x[63,1,0]=-128
        mask=context_validity(x,np.ones(x.shape,bool))
        self.assertFalse(mask[1,0]);self.assertEqual(int(mask.sum()),3)

    def test_float_embedding_not_silently_reencoded(self):
        with self.assertRaises(InputContractError):
            context_validity(np.zeros((64,2,2),np.float64),np.ones((64,2,2),bool))

    def test_missing_current_band_rejected(self):
        with self.assertRaises(InputContractError):
            current_validity(np.ones((2,2,2)),np.ones((2,2,2),bool))

    def test_invalid_checkpoint_stats_rejected(self):
        for bad in (np.array([0.,1.,1.]),np.array([-1.,1.,1.]),np.array([np.nan,1.,1.])):
            with self.assertRaises(InputContractError):validate_stats(np.zeros(3),bad,3)
        validate_stats(np.zeros(3),np.ones(3),3)

    def test_checkpoint_band_count_rejected(self):
        with self.assertRaises(InputContractError):validate_stats(np.zeros(3),np.ones(3),67)

    def test_georeferencing_shift_rejected(self):
        grid=dict(crs='EPSG:32750',width=512,height=512,transform=[10,0,380000,0,-10,9610000])
        validate_output_grid(grid,grid.copy())
        changed={**grid,'transform':[10,0,380010,0,-10,9610000]}
        with self.assertRaises(InputContractError):validate_output_grid(grid,changed)

    def test_masks_must_be_boolean_and_aligned(self):
        with self.assertRaises(InputContractError):final_support(np.ones((2,2),bool),np.ones((1,2),bool))
        with self.assertRaises(InputContractError):current_validity(np.ones((3,2,2)),np.ones((3,2,2),np.uint8))


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests))
    out={'status':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,
         'failures':len(result.failures),'errors':len(result.errors),
         'scope':'SYNTHETIC_ARRAYS_AND_MEMORY_RASTER_ONLY; NO_NEURAL_MODEL_OR_RESEARCH_PIXELS',
         'material_regression':'dataset_mask union can hide one required current band nodata; all-band conjunction rejects it'}
    (Path(__file__).parent/'INPUT_CONTRACT_TEST_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
