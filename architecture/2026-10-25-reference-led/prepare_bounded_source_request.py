"""Freeze a four-chip proposal from already verified source identities; no network IO."""
from __future__ import annotations
from pathlib import Path
import json
import hashlib
from affine import Affine
from pyproj import Transformer
from shapely.geometry import shape,box
from shapely.ops import transform as geometry_transform
import sys

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'
sys.path.insert(0,str(ROOT.parent/'DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD'))
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window


def read(path: Path) -> dict | list:
    """Load previously verified provider metadata, never pixels."""
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main() -> None:
    """Record exact sources, windows and maximum cost without authorizing access."""
    out=ROOT/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.json'
    if out.exists():
        raise RuntimeError('Source proposal already frozen; do not silently change it')
    nominations={r['id']:r for r in read(ROOT/'NOMINATION_FREEZE.json')['records']}
    source_rows={r['provider']+':'+r['item_id']:r for r in read(PARENT/'REFERENCE_SOURCE_PLAN_V2.json')['requests'] if 'item_id' in r}
    matches=read(PARENT/'OPTICAL_SOURCE_MATCH_FREEZE.json')['matches']
    operations=[('N03','S2:S2C_50MLB_20250514_0_L2A','AFTER'),
        ('N03','LS:LC09_L2SP_117062_20250511_02_T1','BEFORE'),
        ('N04','S2:S2C_50MLB_20250511_0_L2A','BEFORE'),
        ('N04','S2:S2A_50MLB_20250513_0_L2A','AFTER')]
    allowed=box(347801.7721720397,9596435.8651008,393391.7721720397,9625255.8651008).buffer(50000)
    to_ll=Transformer.from_crs(32750,4326,always_xy=True).transform
    requests=[]
    for nominee,key,side in operations:
        source=source_rows[key];match=matches[key]
        if match['status']!='EXACT_SOURCE_ID_MATCH':
            raise RuntimeError('Source identity not verified')
        x,y=nominations[nominee]['centre_epsg32750']
        target=Affine(10,0,x-245,0,-10,y+245)
        corners=[target*p for p in [(0,0),(49,0),(49,49),(0,49)]]
        evidence=Evidence(nominee,Role.DEV_REFERENCE,Role.DEV_REFERENCE,
            independent_measurement=True,acquisition_utc=source['optical_datetime'])
        checks=[]
        for band in match['metadata']['bands']:
            source_crs=band['crs'];native=Affine(*band['crs_transform'])
            convert=Transformer.from_crs(32750,source_crs,always_xy=True).transform
            pixels=[~native*convert(*p) for p in corners];cols,rows=zip(*pixels)
            scope=PixelScope('PROPOSED_ROLE_SCOPE_METADATA_FEASIBILITY_ONLY',Role.DEV_REFERENCE,
                nominee,source_crs,geometry_transform(convert,allowed),
                operation_authorization_record='Source-scope geometric feasibility proposal only; actual acquisition remains unauthorized')
            checks.append(check_native_window(evidence,Actor.DEVELOPER,scope,
                NativeWindow(min(cols),min(rows),max(cols),max(rows)),native.to_gdal(),
                source_crs=source_crs,source_width=band['dimensions'][0],source_height=band['dimensions'][1],halo=1,padding=0))
        requests.append({'nomination':nominee,'side':side,'provider':source['provider'],
            'independent_item_id':source['item_id'],'GEE_image_id':match['image_id'],
            'optical_utc':source['optical_datetime'],'offset_hours':source['offset_hours'],
            'grid':{'crs':'EPSG:32750','width':49,'height':49,'transform':list(target)[:6]},
            'bands':match['bands'],'radiometry':match['radiometry'],
            'native_resolution_m':source['nominal_native_resolution_m'],
            'point_inside_recorded_STAC_footprint':bool(shape(source['footprint']).covers(geometry_transform(to_ll,box(x-0.01,y-0.01,x+0.01,y+0.01)))),
            'full_chip_inside_recorded_STAC_footprint':bool(shape(source['footprint']).covers(geometry_transform(to_ll,box(x-245,y-245,x+245,y+245)))),
            'native_window_feasibility_checks':checks,
            'metadata_source_previous_access':'Exact same provider product used successfully in parent acquisition; these spatial windows have not been fetched',
            'output_bands_with_validity':2*len(match['bands']),
            'uncompressed_array_bytes':49*49*2*len(match['bands'])*4,
            'maximum_body_bytes':1024**2,'acquisition_authorized':False,
            'pixel_validity_clarity_state_and_transfer':'UNKNOWN_PENDING_ACTUAL_REFERENCE_EVIDENCE'})
    budget=read(PARENT/'REFERENCE_TRANSFER.json')
    result={'status':'CONCRETE_REFERENCE_SOURCE_REQUEST_FOR_REVIEW; NOT_EXECUTED',
        'requests':requests,'maximum_new_response_body_bytes':4*1024**2,
        'uncompressed_array_bytes':sum(r['uncompressed_array_bytes'] for r in requests),
        'current_cumulative_charge_bytes':budget['charged_bytes'],
        'maximum_cumulative_charge_after_four_new_1MiB_reservations':budget['charged_bytes']+4*1024**2,
        'existing_additional_transfer_ceiling_bytes':1024**3,'storage_ceiling_unchanged_bytes':1024**3,
        'Planet_orders':0,'paid_asset_orders':0,'new_SAR_processing':0,'no_candidate_predictions':True,
        'metadata_checks_are_not_acquisition_permission':True,
        'nomination_freeze_sha256':hashlib.sha256((ROOT/'NOMINATION_FREEZE.json').read_bytes()).hexdigest(),
        'source_choice':'Only already verified existing products; complementary30m pre-target Landsat and10m harmonized after-target S2 for basin; exact bracketing S2 dates for mapped runway',
        'no_fallback_or_replacement_after_failure':True,
        'post_acquisition_gate':'Qualify optical state,30/10/50m support,25position scenarios and temporal evidence; retain UNKNOWN. No automatic candidate inference/comparison.'}
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (ROOT/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.sha256').write_text(hashlib.sha256(out.read_bytes()).hexdigest()+'\n',encoding='utf-8')
    for r in requests:
        print(r['nomination'],r['side'],r['provider'],r['optical_utc'],
            'footprint',r['full_chip_inside_recorded_STAC_footprint'],'native_checks',len(r['native_window_feasibility_checks']))
    print('PROPOSED_MAX_NEW_BYTES',result['maximum_new_response_body_bytes'],'NOT_EXECUTED')


if __name__=='__main__':
    main()
