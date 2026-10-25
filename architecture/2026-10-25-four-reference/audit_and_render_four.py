"""Guarded source QA, fixed displays and a preregistered overlap-encoding diagnostic."""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import sys

ROOT=Path(__file__).resolve().parent
RUN=ROOT/'REFRESHED_ATTEMPT'
BRANCH=ROOT.parent
C2=BRANCH.parent
ENV=Path('E:/Bendungan_Kusan/Miniforge/envs/kusan-c1')
_dll=os.add_dll_directory(str(ENV/'Library/bin')) if os.name=='nt' else None
os.environ['PATH']=str(ENV/'Library/bin')+os.pathsep+os.environ.get('PATH','')
os.environ['GDAL_DATA']=str(ENV/'Library/share/gdal');os.environ['PROJ_DATA']=str(ENV/'Library/share/proj')
os.environ['MPLCONFIGDIR']=str(BRANCH/'matplotlib-config')
import numpy as np
import rasterio
from affine import Affine
from shapely.geometry import box
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0,str(C2/'LINKED_DEVELOPMENT_COMPARISON_20261024'))
sys.path.insert(0,str(C2/'DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD'))
from optical_qa import reflectance,diagnostic_qa,support_scenarios
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window


def read(path: Path) -> dict | list:
    """Read local metadata, never infer a class from it."""
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(name: str,value: dict | list) -> None:
    """Save local diagnostic counts and provenance."""
    (ROOT/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def guarded_array(path: Path,grid: dict,identifier: str,optical_utc: str,digest: str) -> tuple[np.ndarray,dict]:
    """Check the frozen full-chip scope before reading file bodies or arrays."""
    t=Affine(*grid['transform']);x0,y0=t*(0,0);x1,y1=t*(49,49)
    e=Evidence(identifier,Role.DEV_REFERENCE,Role.DEV_REFERENCE,independent_measurement=True,acquisition_utc=optical_utc)
    scope=PixelScope('FOUR_REFERENCE_CHIPS_FROZEN_SCOPE',Role.DEV_REFERENCE,identifier,'EPSG:32750',
        box(x0,y1,x1,y0),operation_authorization_record='AUTHORIZATION.json + frozen source plan + unchanged response protocol')
    permit=check_native_window(e,Actor.DEVELOPER,scope,NativeWindow(0,0,49,49),t.to_gdal(),
        source_crs='EPSG:32750',source_width=49,source_height=49)
    save('LOCAL_PREREAD_LAST.json',{'id':identifier,'permit':permit,'before_body_and_pixel_read':True})
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        raise RuntimeError('Source body differs')
    with rasterio.open(path) as ds:
        if (ds.width,ds.height,ds.crs.to_epsg())!=(49,49,32750) or not ds.transform.almost_equals(t):
            raise RuntimeError('Source grid differs')
        array=ds.read()
    return array,permit


def overlap_encoding(new_data: np.ndarray,new_grid: dict) -> None:
    """Compare only fixed encoding hypotheses on exact overlapping indexing centres."""
    plan=read(ROOT/'OVERLAP_ENCODING_DIAGNOSTIC_PLAN.json')
    pool=read(BRANCH/'LEGACY_SCREEN_FREEZE.json')['items'];legacy=pool[28]
    scopes={r['id']:r for r in read(C2/'DEVELOPMENT_IMPLEMENTATION_20261009/SAVED_CHIP_SCOPE_MANIFEST.json')}
    declared=scopes[legacy['evidence_id']];bounds=declared['bounds']
    old_transform=Affine(10,0,bounds[0],0,-10,bounds[3])
    e=Evidence(legacy['evidence_id'],Role.DEV_REFERENCE,Role.DEV_REFERENCE,independent_measurement=True,
        acquisition_utc=legacy['optical_datetime'])
    scope=PixelScope('EXISTING_PASS_SCOPE',Role.DEV_REFERENCE,e.artifact_id,'EPSG:32750',box(*bounds),
        operation_authorization_record='Existing saved chip scope + OVERLAP_ENCODING_DIAGNOSTIC_PLAN.json')
    permit=check_native_window(e,Actor.DEVELOPER,scope,NativeWindow(0,0,49,49),old_transform.to_gdal(),
        source_crs='EPSG:32750',source_width=49,source_height=49)
    save('ENCODING_PREREAD.json',{'permit':permit,'before_body_or_pixel_read':True})
    path=Path(legacy['stored_chip_path'])
    if hashlib.sha256(path.read_bytes()).hexdigest()!=declared['source_sha256']:
        raise RuntimeError('Legacy body differs')
    with np.load(path,allow_pickle=False) as saved:
        old=saved['data'].copy();actual=Affine(*saved['transform'].tolist()[:6])
    if not actual.almost_equals(old_transform):
        raise RuntimeError('Legacy grid differs')
    new_transform=Affine(*new_grid['transform']);pairs=[]
    for r in range(49):
        for c in range(49):
            x,y=old_transform*(c+.5,r+.5);cc,rr=~new_transform*(x,y)
            nc=int(round(cc-.5));nr=int(round(rr-.5))
            if 0<=nc<49 and 0<=nr<49:
                if abs(nc+.5-cc)>1e-6 or abs(nr+.5-rr)>1e-6:
                    raise RuntimeError('Overlapping sample centres do not align')
                pairs.append((r,c,nr,nc))
    bands=[]
    for b,label in enumerate(['red','green','blue','nir']):
        differences=[]
        for r,c,nr,nc in pairs:
            if old[b,r,c]>0 and new_data[5+b,nr,nc]==1 and new_data[b,nr,nc]!=-9999:
                differences.append(float(old[b,r,c]-new_data[b,nr,nc]))
        d=np.array(differences)
        bands.append({'band':label,'joint_valid_pairs':int(d.size),
            'DN_difference_min_max':[float(d.min()),float(d.max())] if d.size else None,
            'exact0DN_count':int(np.sum(d==0)),'exact1000DN_count':int(np.sum(d==1000)),
            'H1_no_extra_offset_max_abs_error_SR':float(np.max(np.abs(d*1e-4))) if d.size else None,
            'H2_literal_minus0point1_max_abs_error_SR':float(np.max(np.abs(d*1e-4-.1))) if d.size else None})
    save('OVERLAP_ENCODING_RESULT.json',{'nominal_source_item':legacy['optical_item_id'],
        'old_acquisition_utc':legacy['optical_datetime'],'overlapping_index_centres':len(pairs),
        'bands':bands,'diagnostic_plan':plan,'new_export_uses_current_recorded_ingestion_revision':True,
        'identity_limit':'NominalSTACitem/date/baseline match; original full ESA generation URI not asserted here. No global/absolute calibration proof.',
        'no_fitted_offset_or_class_tuning':True,'no_extra_temporal_observation':True,
        'legacy_arrays_responses_and_contract_unchanged':True})


def main() -> None:
    """Render all four unchanged requests and preserve source/support failures."""
    plan=read(BRANCH/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.json')['requests'];audits=[];loaded={}
    for nominee in ['N03','N04']:
        rows=[r for r in plan if r['nomination']==nominee]
        fig,axes=plt.subplots(2,3,figsize=(12,8),layout='constrained')
        fig.suptitle(f'{nominee}: frozen reference-only target11May2025 | fixedSR0-0.30,gamma1\n'
            'North up,EPSG32750;30m white,50m cyan,90m gray; QA is diagnostic, no reference class generated',fontsize=10)
        for i,row in enumerate(rows):
            identifier=f'{row["nomination"]}_{row["provider"]}_{row["side"]}'
            receipt=read(RUN/'receipts'/(identifier+'.json'))
            if receipt['status']!='ACQUIRED_NOT_INTERPRETED':
                for ax in axes[i]:
                    ax.text(.5,.5,receipt['status'],ha='center');ax.axis('off')
                audits.append({'id':identifier,'status':receipt['status']});continue
            data,permit=guarded_array(Path(receipt['path']),row['grid'],identifier,row['optical_utc'],receipt['payload']['sha256'])
            n=len(row['bands'])
            if data.shape!=(2*n,49,49) or not np.isin(data[n:],[0,1]).all():
                raise RuntimeError('Band count/mask encoding differs')
            for b in range(4,n):
                values=data[b][data[n+b]==1];upper=11 if row['provider']=='S2' else 65535
                if not (np.equal(values,np.floor(values)).all() and (values>=0).all() and (values<=upper).all()):
                    raise RuntimeError('QA encoding differs')
            raw=data[:n];masks=data[n:];physical=reflectance(raw[:4],row['provider'])
            valid=np.all(masks[:4]==1,axis=0);available,flagged=diagnostic_qa(raw,row['provider'],masks)
            supports={str(size):support_scenarios(available,flagged,size) for size in [10,30,50]}
            audits.append({'id':identifier,'status':'GRID_BODY_MASK_QA_SCALING_CHECKED_NOT_INTERPRETED',
                'provider':row['provider'],'optical_utc':row['optical_utc'],'offset_hours':row['offset_hours'],
                'native_resolution_m':row['native_resolution_m'],'payload_sha256':receipt['payload']['sha256'],
                'local_pre_read_check':permit,'full_SR_valid_fraction':float(valid.mean()),
                'support_diagnostics':supports,'band_order':'Frozen ordered request; TIFF descriptions absent',
                'reflectance_range':[[float(physical[b][valid].min()),float(physical[b][valid].max())] if valid.any() else None for b in range(4)],
                'reference_class':'NOT_AUTOMATED','transfer':'UNKNOWN'})
            for j,(channels,zoom,title) in enumerate([([0,1,2],False,'RGB490m'),([0,1,2],True,'RGB110m'),([3,0,1],True,'NIR-red-green110m')]):
                display=np.moveaxis(np.clip(physical[channels]/.30,0,1),0,-1);display[~valid]=.55
                ax=axes[i,j];ax.imshow(display,extent=[-245,245,-245,245],origin='upper',interpolation='nearest')
                for size,color in [(30,'white'),(50,'cyan'),(90,'#bbbbbb')]:
                    ax.add_patch(Rectangle((-size/2,-size/2),size,size,fill=False,edgecolor=color,lw=.9))
                if zoom:
                    ax.set_xlim(-55,55);ax.set_ylim(-55,55)
                q=supports['30']['nominal']
                ax.set_title(f'{row["provider"]} {row["side"]} {row["optical_utc"][:19]}\n{title}; available{q["available_fraction"]:.2f},QAflag{q["qa_flagged_fraction"]:.2f}',fontsize=8)
                ax.set_xlabel('east offset(m)',fontsize=8);ax.set_ylabel('north offset(m)',fontsize=8)
            loaded[identifier]=(data,row['grid'])
        fig.savefig(ROOT/(nominee+'_reference_views.png'),dpi=140);plt.close(fig)
        print('PREPARED',nominee,flush=True)
    save('FOUR_CHIP_TECHNICAL_AUDIT.json',{'observations':audits,'no_automatic_reference_labels':True})
    if 'N03_S2_AFTER' in loaded:
        overlap_encoding(*loaded['N03_S2_AFTER'])
    save('STATUS.json',{'phase':'FOUR_REFERENCES_TECHNICALLY_AUDITED_AND_RENDERED; OPTICAL_INTERPRETATION_PENDING',
        'acquired':4,'no_background_job':True,'comparison_gate':'CLOSED'})


if __name__=='__main__':
    main()
