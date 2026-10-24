"""Offline regression checks; no file/network pixel reads or reference labels."""
from pathlib import Path
import hashlib
import json
import sys
import unittest
from affine import Affine
from pyproj import Transformer
from shapely.geometry import box

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD'))
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window,Denied


class PreReadChecks(unittest.TestCase):
    """Exercise source hemisphere, rounded halos and immutable plan sizes."""

    def test_northern_utm_negative_northing(self) -> None:
        """EPSG32650 south-of-equator coordinates must be transformed, not relabelled."""
        conversion=Transformer.from_crs(32750,32650,always_xy=True)
        x,y=conversion.transform(380000,9600000)
        self.assertAlmostEqual(x,380000,places=3)
        self.assertAlmostEqual(y,-400000,places=3)
        native=Affine(30,0,370000,0,-30,-390000)
        c,r=~native*(x,y)
        evidence=Evidence('test',Role.DEV_REFERENCE,Role.DEV_REFERENCE,
            independent_measurement=True,acquisition_utc='2025-01-11T00:00:00Z')
        scope=PixelScope('test',Role.DEV_REFERENCE,'test','EPSG:32650',
            box(370000,-420000,400000,-390000),operation_authorization_record='synthetic')
        result=check_native_window(evidence,Actor.DEVELOPER,scope,
            NativeWindow(c-8.2,r-8.2,c+8.2,r+8.2),native.to_gdal(),
            source_crs='EPSG:32650',source_width=1000,source_height=1000,halo=1,padding=0)
        self.assertIsInstance(result,dict)
        with self.assertRaises(Denied):
            check_native_window(evidence,Actor.DEVELOPER,scope,
                NativeWindow(-0.1,10,10,20),native.to_gdal(),
                source_crs='EPSG:32650',source_width=1000,source_height=1000,halo=1,padding=0)

    def test_halo_crosses_authorized_edge(self) -> None:
        """An interior raw window fails when outward rounding plus halo leaves scope."""
        evidence=Evidence('edge',Role.DEV_REFERENCE,Role.DEV_REFERENCE,
            independent_measurement=True,acquisition_utc='2025-01-11T00:00:00Z')
        scope=PixelScope('edge',Role.DEV_REFERENCE,'edge','EPSG:32750',box(100,-200,200,-100),
            operation_authorization_record='synthetic')
        with self.assertRaises(Denied):
            check_native_window(evidence,Actor.DEVELOPER,scope,
                NativeWindow(100.1,100.1,199.9,199.9),(0,1,0,0,0,-1),
                source_crs='EPSG:32750',source_width=500,source_height=500,halo=1,padding=0)

    def test_plan_digest_and_all_records(self) -> None:
        """No content-based replacement or dropped missing opportunity is permitted."""
        for stem in ['REFERENCE_PANEL_FREEZE','REFERENCE_SOURCE_PLAN_V2']:
            payload=(ROOT/(stem+'.json')).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(),
                (ROOT/(stem+'.sha256')).read_text(encoding='utf-8').strip())
        requests=json.loads((ROOT/'REFERENCE_SOURCE_PLAN_V2.json').read_text(encoding='utf-8'))['requests']
        self.assertEqual(len(requests),96)
        self.assertEqual(len({r['id'] for r in requests}),96)
        self.assertEqual(len({r['case_id'] for r in requests}),24)
        self.assertEqual(sum('item_id' not in r for r in requests),18)
        self.assertEqual(len({(r['provider'],r['item_id']) for r in requests if 'item_id' in r}),20)


if __name__=='__main__':
    unittest.main(verbosity=2)
