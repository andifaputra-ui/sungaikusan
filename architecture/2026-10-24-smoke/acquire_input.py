"""One approved explicit EE image; pre-read source-window planning and masks."""
from __future__ import annotations
from pathlib import Path
from dataclasses import asdict
from math import floor, ceil
import json
import sys
import ee
from affine import Affine
from shapely.geometry import box
from resource_budget import Budget

ROOT = Path(__file__).resolve().parent
PREP = ROOT.parent/'NATIVE_MODEL_READINESS_20261023'
GUARD = ROOT.parent/'DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD'
sys.path.insert(0,str(GUARD))
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window

SCENE = 'COPERNICUS/S1_GRD/S1A_IW_GRDH_1SDV_20240901T220029_20240901T220054_055477_06C49D_489D'


def main() -> None:
    """Create a six-band input (three observations, three explicit source masks)."""
    if not (ROOT/'RUNTIME_READY.json').exists():
        raise RuntimeError('Runtime gate has not passed')
    authorization = json.loads((ROOT/'AUTHORIZATION.json').read_text(encoding='utf-8'))
    assert authorization['human_decision']=='Approve the bounded technical smoke test'
    grid = json.loads((PREP/'PROPOSED_SMOKE_INPUT_FREEZE.json').read_text(encoding='utf-8'))['grid']
    transform = Affine(*grid['transform'])
    corners = [transform*point for point in [(0,0),(512,0),(512,512),(0,512)]]
    xs,ys=zip(*corners)
    # Fixed physical engineering scope includes planned source rounding/coarse-angle support.
    # It is frozen before querying source grids, never fitted to a requested read window.
    scope_bounds=[min(xs)-50000,min(ys)-50000,max(xs)+50000,max(ys)+50000]
    scope_record={'role':'DEVELOPMENT_ENGINEERING','scene':SCENE,'output_grid':grid,
        'source_scope_crs':'EPSG:32750','source_scope_bounds':scope_bounds,
        'kernel':'GEE default nearest neighbour; no added resample call',
        'planning_halo_source_pixels':1,'padding':0,
        'limitations':'GEE internal tile/cache reads are provider-controlled and not observable. This validates a conservative planned source footprint, not a complete provider IO trace. No reference artifacts or final-validation evidence are accessed.'}
    (ROOT/'PRE_READ_SCOPE.json').write_text(json.dumps(scope_record,indent=2)+'\n',encoding='utf-8')
    ee.data.setDeadline(120000)
    ee.Initialize(project='gen-lang-client-0932704594')
    image=ee.Image(SCENE)
    metadata=image.getInfo()
    props=metadata['properties']
    if props['orbitProperties_pass']!='DESCENDING' or props['relativeOrbitNumber_start']!=105 or props['orbitNumber_start']!=55477:
        raise RuntimeError('Source identity/orbit differs')
    checks=[]
    for band in metadata['bands']:
        if band['id'] not in {'VV','VH','angle'}:
            continue
        if band['crs']!=grid['crs']:
            raise RuntimeError('Source projection changed; stop instead of guessing')
        native=Affine(*band['crs_transform'])
        positions=[~native*point for point in corners]
        cols,rows=zip(*positions)
        artifact=SCENE+'/'+band['id']
        evidence=Evidence(artifact_id=artifact,role=Role.ENGINEERING,origin_role=Role.ENGINEERING)
        scope=PixelScope(scope_id='APPROVED_SINGLE_PATCH_NATIVE_INPUT_20261024',
            role=Role.ENGINEERING,artifact_id=artifact,crs=grid['crs'],
            authorized_geometry=box(*scope_bounds),operation_authorization_record='AUTHORIZATION.json')
        result=check_native_window(evidence,Actor.DEVELOPER,scope,
            NativeWindow(min(cols),min(rows),max(cols),max(rows)),native.to_gdal(),
            source_crs=band['crs'],source_width=band['dimensions'][0],source_height=band['dimensions'][1],halo=1,padding=0)
        checks.append({'band':band['id'],'source_metadata':band,'check':result})
    if len(checks)!=3:
        raise RuntimeError('Required source bands absent')
    (ROOT/'PRE_READ_WINDOW_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    selected=image.select(['VV','VH','angle']).float()
    masks=selected.mask().unmask(0,sameFootprint=False).rename(['valid_VV','valid_VH','valid_angle']).float()
    output=selected.unmask(-9999,sameFootprint=False).addBands(masks)
    params={'name':'S1_ONLY_ENGINEERING_INPUT','crs':grid['crs'],
            'crs_transform':grid['transform'],'dimensions':[512,512],
            'format':'GEO_TIFF','filePerBand':False}
    (ROOT/'EE_GRAPH.json').write_text(output.serialize(),encoding='utf-8')
    receipt={'scene':SCENE,'properties':props,'request':params,
             'bands':['VV','VH','angle','valid_VV','valid_VH','valid_angle'],
             'native_processing':'COPERNICUS/S1_GRD catalogue sigma0 dB/provider angle; distinct experimental branch, not asserted equivalent to SNAP/C1',
             'role':'PERMANENT_DEVELOPMENT_ENGINEERING'}
    (ROOT/'INPUT_REQUEST.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    # All native-window checks and the explicit authorization precede pixel request/access.
    url=output.getDownloadURL(params)
    receipt['payload']=Budget().fetch_bounded(url,ROOT/'CURRENT_INPUT.tif',16*1024**2)
    (ROOT/'INPUT_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('INPUT_ACQUIRED',receipt['payload'],flush=True)


if __name__=='__main__':
    main()
