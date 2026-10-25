"""One bounded attempt for each of four frozen optical-reference windows."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
from collections import Counter
from urllib.request import urlopen
import hashlib
import json
import os
import re
import sys

ENV=Path('E:/Bendungan_Kusan/Miniforge/envs/kusan-c1')
_dll=os.add_dll_directory(str(ENV/'Library/bin')) if os.name=='nt' else None
os.environ['PATH']=str(ENV/'Library/bin')+os.pathsep+os.environ.get('PATH','')
import ee
import httplib2
from affine import Affine
from shapely.geometry import box
from shapely.ops import transform as geometry_transform
from pyproj import Transformer

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
C2=BRANCH.parent
PARENT=C2/'LINKED_DEVELOPMENT_COMPARISON_20261024'
sys.path.insert(0,str(C2/'NATIVE_MODEL_SMOKE_20261024'))
sys.path.insert(0,str(C2/'DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD'))
from resource_budget import Budget
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window,Denied
MAXIMUM=1024**2


def read(path: Path) -> dict:
    """Read frozen metadata without accessing imagery."""
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(name: str,value: dict) -> None:
    """Persist a receipt without signed request URLs."""
    (ROOT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def status(phase: str,**values) -> None:
    """Expose compact phase/counts, not monitoring loops."""
    value={'phase':phase,'utc':datetime.now(timezone.utc).isoformat(),**values}
    save('STATUS.json',value);print(json.dumps(value),flush=True)


def body_fetch(url: str,destination: Path,budget: Budget,maximum: int=MAXIMUM) -> dict:
    """Read at most a pre-reserved body; exact-limit responses are conservatively rejected."""
    part=destination.with_suffix('.part')
    if destination.exists() or part.exists():
        raise RuntimeError('Body/partial exists; no implicit retry or overwrite')
    count=0;sha=hashlib.sha256()
    try:
        with urlopen(url,timeout=90) as response,part.open('xb') as output:
            declared=response.headers.get('Content-Length')
            if declared and int(declared)>maximum:
                raise RuntimeError('Response declaration exceeds frozen body bound')
            while count<maximum:
                block=response.read(min(65536,maximum-count))
                budget.after_read(len(block))
                if not block:
                    break
                output.write(block);sha.update(block);count+=len(block)
            else:
                # No extra byte is consumed merely to detect an oversized response.
                raise RuntimeError('Body reached limit without proven EOF; retain partial')
        part.replace(destination)
        return {'bytes':count,'sha256':sha.hexdigest(),'maximum':maximum}
    finally:
        budget.save()


def main() -> None:
    """Revalidate exact source metadata and native windows before each pixel request."""
    if (ROOT/'ATTEMPT_START.json').exists():
        raise RuntimeError('Four-chip attempt already started; inspect it, do not relaunch')
    plan_file=BRANCH/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.json'
    if hashlib.sha256(plan_file.read_bytes()).hexdigest()!=(BRANCH/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.sha256').read_text().strip():
        raise RuntimeError('Frozen source plan differs')
    plan=read(plan_file);auth=read(ROOT/'AUTHORIZATION.json')
    if len(plan['requests'])!=4 or auth['maximum_new_response_body_bytes']!=4*MAXIMUM:
        raise RuntimeError('Bounded source authorization differs')
    budget=Budget(PARENT/'REFERENCE_TRANSFER.json')
    budget_before=dict(budget.data)
    save('BUDGET_BEFORE.json',budget_before)
    save('ATTEMPT_START.json',{'utc':datetime.now(timezone.utc).isoformat(),
        'plan_sha256':hashlib.sha256(plan_file.read_bytes()).hexdigest(),
        'no_automatic_retry':True,'requests':4,'new_candidate_inference':False})
    status('INITIALIZING_REFERENCE_ONLY_REQUESTS',total=4)
    ee.Initialize(project='gen-lang-client-0932704594',http_transport=httplib2.Http(timeout=45))
    ee.data.setDeadline(45000);ee.data.setMaxRetries(0)
    matches=read(PARENT/'OPTICAL_SOURCE_MATCH_FREEZE.json')['matches']
    known={v['image_id']:v for v in matches.values() if v['status']=='EXACT_SOURCE_ID_MATCH'}
    physical_scope=box(347801.7721720397,9596435.8651008,393391.7721720397,9625255.8651008).buffer(50000)
    (ROOT/'chips').mkdir(exist_ok=True);(ROOT/'receipts').mkdir(exist_ok=True)
    results=[]
    for row in plan['requests']:
        identifier=f'{row["nomination"]}_{row["provider"]}_{row["side"]}'
        receipt={'id':identifier,'role':'DEVELOPMENT_REFERENCE','nomination':row['nomination'],
            'optical_utc':row['optical_utc'],'reference_state':'NOT_INTERPRETED','temporal_transfer':'UNKNOWN',
            'new_acquisition_authorization':'AUTHORIZATION.json; user continue after concrete four-chip proposal'}
        try:
            frozen=known[row['GEE_image_id']]
            image=ee.Image(row['GEE_image_id']).select(row['bands'])
            actual=image.getInfo()
            if actual['properties'].get(frozen['property'])!=frozen['value']:
                raise Denied('Exact provider product identity changed')
            old_version=frozen['metadata'].get('version');new_version=actual.get('version')
            if old_version!=new_version:
                raise Denied('Provider asset version changed; stop for provenance review')
            original_band_specs=[(b['id'],b['crs'],b['crs_transform'],b['dimensions']) for b in frozen['metadata']['bands']]
            actual_band_specs=[(b['id'],b['crs'],b['crs_transform'],b['dimensions']) for b in actual['bands']]
            if original_band_specs!=actual_band_specs:
                raise Denied('Source grid/bands changed')
            receipt['source_metadata']=actual
            grid=row['grid'];affine=Affine(*grid['transform'])
            corners=[affine*p for p in [(0,0),(49,0),(49,49),(0,49)]]
            checks=[]
            for band in actual['bands']:
                native=Affine(*band['crs_transform']);crs=band['crs']
                conversion=Transformer.from_crs(32750,crs,always_xy=True).transform
                pixels=[~native*conversion(*p) for p in corners];cols,lines=zip(*pixels)
                e=Evidence(identifier+'/'+band['id'],Role.DEV_REFERENCE,Role.DEV_REFERENCE,
                    independent_measurement=True,acquisition_utc=row['optical_utc'])
                scope=PixelScope('AUTHORIZED_FOUR_REFERENCE_WINDOWS',Role.DEV_REFERENCE,e.artifact_id,crs,
                    geometry_transform(conversion,physical_scope),
                    operation_authorization_record='AUTHORIZATION.json + immutable source plan and nominations')
                checks.append(check_native_window(e,Actor.DEVELOPER,scope,
                    NativeWindow(min(cols),min(lines),max(cols),max(lines)),native.to_gdal(),
                    source_crs=crs,source_width=band['dimensions'][0],source_height=band['dimensions'][1],halo=1,padding=0))
            receipt['pre_read_checks']=checks
            receipt['source_grid_matches_frozen']=True
            receipt['provider_internal_IO']='Unobservable; conservative planned source windows, not an internal cache read trace'
            receipt['status']='PRE_READ_PASSED'
            save('receipts/'+identifier+'.json',receipt)
            storage=sum(p.stat().st_size for folder in [PARENT,BRANCH] for p in folder.rglob('*') if p.is_file())
            if storage+MAXIMUM>=1024**3:
                raise RuntimeError('Retained aggregate storage ceiling reached')
            if budget.data['charged_bytes']-budget_before['charged_bytes']+MAXIMUM>4*MAXIMUM:
                raise RuntimeError('Four-chip conservative charge bound reached')
            # Reserve before generating the pixel-download request or reading a response body.
            budget.before_read(MAXIMUM)
            value=image.float();valid=value.mask().unmask(0,sameFootprint=False).rename(['valid_'+b for b in row['bands']]).float()
            exported=value.unmask(-9999,sameFootprint=False).addBands(valid)
            params={'crs':grid['crs'],'crs_transform':grid['transform'],'dimensions':[49,49],
                'format':'GEO_TIFF','filePerBand':False}
            destination=ROOT/'chips'/(identifier+'.tif')
            receipt['payload']=body_fetch(exported.getDownloadURL(deepcopy(params)),destination,budget)
            receipt.update(status='ACQUIRED_NOT_INTERPRETED',path=str(destination),
                bands=row['bands'],grid=grid,provider=row['provider'],radiometry=row['radiometry'],
                offset_hours=row['offset_hours'],native_resolution_m=row['native_resolution_m'])
        except Denied as error:
            receipt.update(status='PROVENANCE_OR_NATIVE_WINDOW_STOP',error=str(error))
            save('receipts/'+identifier+'.json',receipt)
            raise
        except Exception as error:
            receipt.update(status='TECHNICAL_NONRESPONSE_NO_RETRY',error_type=type(error).__name__,
                error_summary=re.sub(r'https?://\S+','[URL omitted]',str(error))[:600])
        save('receipts/'+identifier+'.json',receipt);results.append(receipt)
        status('ACQUIRING_FOUR_FROZEN_REFERENCE_WINDOWS',completed=len(results),total=4,
            outcomes=dict(Counter(r['status'] for r in results)))
    summary={'status':'FOUR_CHIP_ACQUISITION_COMPLETE_NOT_ADJUDICATED','requests':4,
        'outcomes':dict(Counter(r['status'] for r in results)),
        'new_metered_body_bytes':budget.data['received_metered_bytes']-budget_before['received_metered_bytes'],
        'new_conservative_charge_bytes':budget.data['charged_bytes']-budget_before['charged_bytes'],
        'cumulative_charge_bytes':budget.data['charged_bytes'],'new_candidate_inference':0,
        'new_reference_labels':0,'no_fallback_or_retry':True}
    save('ACQUISITION_SUMMARY.json',summary)
    status('FOUR_CHIPS_READY_FOR_LOCAL_QUALITY_AND_RESPONSE',summary='ACQUISITION_SUMMARY.json',no_automatic_inference=True)


if __name__=='__main__':
    try:
        main()
    except Exception as error:
        status('FOUR_CHIP_EXECUTION_STOPPED',error_type=type(error).__name__,no_automatic_retry=True)
        raise
