"""Sequential fixed-plan optical chips; no reference labels or SAR predictions."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
from collections import Counter
import hashlib
import json
import sys
import re
import ee
import httplib2
from affine import Affine
from shapely.geometry import box
from shapely.ops import transform
from pyproj import Transformer

ROOT=Path(__file__).resolve().parent
C2=ROOT.parent
sys.path.insert(0,str(C2/'NATIVE_MODEL_SMOKE_20261024'))
from resource_budget import Budget
sys.path.insert(0,str(C2/'DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD'))
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window


def save(name: str,value: dict | list) -> None:
    """Persist a local receipt without signed URLs or automatic class decisions."""
    (ROOT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def status(phase: str,**kwargs) -> None:
    """Record phase/counts for one-check continuation."""
    save('STATUS.json',dict(phase=phase,utc=datetime.now(timezone.utc).isoformat(),**kwargs))
    print(phase,kwargs,flush=True)


def key_for(row: dict) -> tuple[str,str]:
    """Use immutable independent-catalogue item identity."""
    return row['provider'],row['item_id']


def main() -> None:
    """Match20 physical source products, freeze matches, then acquire fixed ROIs."""
    plan_file=ROOT/'REFERENCE_SOURCE_PLAN_V2.json'
    if hashlib.sha256(plan_file.read_bytes()).hexdigest()!=(ROOT/'REFERENCE_SOURCE_PLAN_V2.sha256').read_text(encoding='utf-8').strip():
        raise RuntimeError('Frozen source plan digest differs')
    plan=json.loads(plan_file.read_text(encoding='utf-8'))
    requests=plan['requests']
    unique={key_for(row):row for row in requests if 'item_id' in row}
    budget_path=ROOT/'REFERENCE_TRANSFER.json'
    if not budget_path.exists():
        save('REFERENCE_TRANSFER.json',{'limit_bytes':1024**3,'charged_bytes':64*1024**2,
            'received_metered_bytes':0,'unmetered_metadata_reserve_bytes':64*1024**2,
            'prior_smoke_charged_bytes_not_reset':969932800,
            'accounting':'Conservative64MiB reserve for this block metadata/connector traffic; artifact bodies reserved before reads; headers/TLS excluded. Separate1GiB additional ceiling.'})
    budget=Budget(budget_path)
    status('MATCHING_FROZEN_OPTICAL_SOURCE_IDENTITIES',unique_sources=len(unique),new_pixels=0)
    ee.Initialize(project='gen-lang-client-0932704594',http_transport=httplib2.Http(timeout=45))
    ee.data.setDeadline(45000);ee.data.setMaxRetries(0)
    matches={}
    match_path=ROOT/'OPTICAL_SOURCE_MATCH_FREEZE.json'
    if match_path.exists():
        frozen=json.loads(match_path.read_text(encoding='utf-8'))
        if frozen['source_plan_sha256']!=hashlib.sha256(plan_file.read_bytes()).hexdigest():
            raise RuntimeError('Source-match freeze belongs to another plan')
        matches=frozen['matches']
    else:
        for (provider,item_id),row in unique.items():
            props=row['properties']
            if provider=='S2':
                collection='COPERNICUS/S2_SR_HARMONIZED'
                property_name='PRODUCT_ID';expected=props['s2:product_uri'].removesuffix('.SAFE')
            else:
                satellite='LC08' if props['platform']=='landsat-8' else 'LC09'
                tier=props['landsat:collection_category']
                collection=f'LANDSAT/{satellite}/C02/{tier}_L2'
                property_name='LANDSAT_SCENE_ID';expected=props['landsat:scene_id']
            match_id=provider+':'+item_id
            try:
                result=ee.ImageCollection(collection).filterDate('2025-01-01','2026-01-01').filter(ee.Filter.eq(property_name,expected))
                ids=result.aggregate_array('system:index').getInfo()
                if len(ids)!=1:
                    matches[match_id]={'status':'NO_UNIQUE_EXACT_SOURCE_MATCH','count':len(ids),'collection':collection}
                    continue
                image=ee.Image(collection+'/'+ids[0])
                bands=['B4','B3','B2','B8','SCL'] if provider=='S2' else ['SR_B4','SR_B3','SR_B2','SR_B5','QA_PIXEL','QA_RADSAT']
                metadata=image.select(bands).getInfo()
                if metadata['properties'].get(property_name)!=expected:
                    raise RuntimeError('Matched identity changed')
                matches[match_id]={'status':'EXACT_SOURCE_ID_MATCH','image_id':collection+'/'+ids[0],
                    'property':property_name,'value':expected,'bands':bands,'metadata':metadata,
                    'radiometry':row['source_radiometry'],'native_resolution_m':row['nominal_native_resolution_m']}
            except Exception as error:
                matches[match_id]={'status':'SOURCE_METADATA_TECHNICAL_NONRESPONSE','error_type':type(error).__name__,
                    'error_summary':re.sub(r'https?://\S+','[URL omitted]',str(error))[:600]}
            save('OPTICAL_SOURCE_MATCH_PROGRESS.json',{'matches':matches,'new_pixels':0})
        save('OPTICAL_SOURCE_MATCH_FREEZE.json',{'status':'FROZEN_BEFORE_OPTICAL_PIXEL_ACCESS','matches':matches,
            'source_plan_sha256':hashlib.sha256(plan_file.read_bytes()).hexdigest(),'new_pixels_at_freeze':0})
    status('ACQUIRING_FIXED_REFERENCE_CHIPS',source_match_counts=dict(Counter(v['status'] for v in matches.values())))
    (ROOT/'reference_chips').mkdir(exist_ok=True)
    (ROOT/'reference_receipts').mkdir(exist_ok=True)
    # Role-specific physical scope is fixed before any request. Source projection transforms
    # are mathematical derivatives of this scope, never fitted to the requested window.
    physical_scope=box(347801.7721720397,9596435.8651008,393391.7721720397,9625255.8651008).buffer(50000)
    results=[]
    for row in requests:
        receipt_path=ROOT/'reference_receipts'/(row['id']+'.json')
        if receipt_path.exists():
            existing=json.loads(receipt_path.read_text(encoding='utf-8'))
            if existing['source_plan_sha256']!=hashlib.sha256(plan_file.read_bytes()).hexdigest():
                raise RuntimeError('Existing receipt belongs to another plan')
            if existing['status']=='PRE_READ_CHECKS_PASSED':
                # Keep the original receipt intact; no implicit pixel retry after interruption.
                existing=dict(existing,status='INTERRUPTED_AFTER_PREREAD_NO_AUTO_RETRY')
            results.append(existing)
            continue
        receipt={'id':row['id'],'case_id':row['case_id'],'role':row['role'],
                 'reference_state':'NOT_INTERPRETED','temporal_transfer':'UNKNOWN',
                 'source_plan_sha256':hashlib.sha256(plan_file.read_bytes()).hexdigest()}
        if 'item_id' not in row:
            receipt['status']='NO_FIXED_SEARCH_OPPORTUNITY'
        else:
            match=matches.get(row['provider']+':'+row['item_id'],{})
            receipt.update(provider=row['provider'],independent_item_id=row['item_id'],optical_utc=row['optical_datetime'],
                offset_hours=row['offset_hours'],native_resolution_m=row['nominal_native_resolution_m'])
            if match.get('status')!='EXACT_SOURCE_ID_MATCH':
                receipt['status']='SOURCE_MATCH_NONRESPONSE';receipt['match_status']=match.get('status')
            else:
                if budget.data['limit_bytes']-budget.data['charged_bytes']<1024**2:
                    raise RuntimeError('Insufficient conservative transfer reservation; stop before pixel request')
                try:
                    grid=row['chip_grid'];target=Affine(*grid['transform'])
                    corners=[target*point for point in [(0,0),(49,0),(49,49),(0,49)]]
                    checks=[]
                    for band in match['metadata']['bands']:
                        source_crs=band['crs'];conversion=Transformer.from_crs(32750,source_crs,always_xy=True).transform
                        allowed=transform(conversion,physical_scope)
                        native=Affine(*band['crs_transform'])
                        locations=[~native*conversion(*point) for point in corners]
                        cols,rows=zip(*locations)
                        artifact=row['id']+'/'+band['id']
                        evidence=Evidence(artifact_id=artifact,role=Role.DEV_REFERENCE,origin_role=Role.DEV_REFERENCE,
                            independent_measurement=True,acquisition_utc=row['optical_datetime'])
                        scope=PixelScope(scope_id='FROZEN_LINKED_REFERENCE_SCOPE',role=Role.DEV_REFERENCE,
                            artifact_id=artifact,crs=source_crs,authorized_geometry=allowed,
                            operation_authorization_record='SCOPE.json + REFERENCE_PANEL_FREEZE.json + REFERENCE_SOURCE_PLAN_V2.json')
                        checks.append(check_native_window(evidence,Actor.DEVELOPER,scope,
                            NativeWindow(min(cols),min(rows),max(cols),max(rows)),native.to_gdal(),
                            source_crs=source_crs,source_width=band['dimensions'][0],source_height=band['dimensions'][1],halo=1,padding=0))
                    receipt['pre_read_native_checks']=checks
                    receipt['provider_internal_read_limit']='GEE internal cache/tile reads unobservable; these are conservative planned source windows, not a full provider IO trace.'
                    # Save approved native checks before getDownloadURL or data transfer.
                    receipt['status']='PRE_READ_CHECKS_PASSED'
                    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
                    image=ee.Image(match['image_id']).select(match['bands']).float()
                    validity=image.mask().unmask(0,sameFootprint=False).rename(['valid_'+b for b in match['bands']]).float()
                    output=image.unmask(-9999,sameFootprint=False).addBands(validity)
                    params={'crs':grid['crs'],'crs_transform':grid['transform'],'dimensions':[49,49],
                            'format':'GEO_TIFF','filePerBand':False}
                    destination=ROOT/'reference_chips'/(row['id']+'.tif')
                    if sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())+1024**2>1024**3:
                        raise RuntimeError('Additional storage ceiling reached')
                    receipt['payload']=budget.fetch_bounded(output.getDownloadURL(deepcopy(params)),destination,1024**2)
                    receipt.update(status='ACQUIRED_NOT_INTERPRETED',path=str(destination),image_id=match['image_id'],
                        bands=match['bands'],radiometry=match['radiometry'],output_grid=grid,
                        source_properties=match['metadata']['properties'])
                except Exception as error:
                    receipt['status']='TECHNICAL_NONRESPONSE_NO_AUTO_RETRY'
                    receipt['error_type']=type(error).__name__
                    receipt['error_summary']=re.sub(r'https?://\S+','[URL omitted]',str(error))[:600]
        receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
        results.append(receipt)
        status('ACQUIRING_FIXED_REFERENCE_CHIPS',completed=len(results),total=len(requests),
            outcome_counts=dict(Counter(r['status'] for r in results)),charged_bytes=budget.data['charged_bytes'])
        if budget.data['charged_bytes']>=budget.data['limit_bytes']:
            raise RuntimeError('Additional transfer ceiling reached')
    summary={'status':'REFERENCE_ACQUISITION_PASS_COMPLETE_NOT_ADJUDICATED',
        'requests':len(requests),'date_supports':24,'systems':12,
        'outcomes':dict(Counter(r['status'] for r in results)),
        'source_matches':dict(Counter(v['status'] for v in matches.values())),
        'new_candidate_inference_runs':0,'new_reference_classes':0,
        'reader_exposure_rule':'Do not expose source context tags, scene water percentages, SAR scores or old responses in review packets',
        'metadata_boundaries':'Posting grid10m; Landsat native30m and S2 QA native20m retained; no added information claimed',
        'interpretation':'Reference pixel clarity, W/N/O/U bounds and temporal transfer remain to be adjudicated; no comparison is permitted yet.'}
    save('REFERENCE_ACQUISITION_SUMMARY.json',summary)
    status('REFERENCE_CHIPS_READY_FOR_BLINDED_OPTICAL_QA',summary='REFERENCE_ACQUISITION_SUMMARY.json',no_follow_on_inference=True)


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        status('REFERENCE_ACQUISITION_STOPPED',error_type=type(error).__name__,no_automatic_retry=True)
        raise
