"""Guarded local QA and neutral optical-only view preparation; no class responses."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import os
import sys
import hashlib
import json
import csv

ENV=Path('E:/Bendungan_Kusan/Miniforge/envs/kusan-c1')
_dll_directory=os.add_dll_directory(str(ENV/'Library/bin')) if os.name=='nt' else None
os.environ['PATH']=str(ENV/'Library/bin')+os.pathsep+os.environ.get('PATH','')
os.environ.setdefault('GDAL_DATA',str(ENV/'Library/share/gdal'))
os.environ.setdefault('PROJ_DATA',str(ENV/'Library/share/proj'))
os.environ['MPLCONFIGDIR']=str(Path(__file__).resolve().parent/'matplotlib-config')
import numpy as np
import rasterio
from affine import Affine
from shapely.geometry import box
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from optical_qa import reflectance,diagnostic_qa,support_scenarios

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD'))
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window
OUT=ROOT/'BLINDED_OPTICAL_PACKET'


def save(path: Path,value: dict | list) -> None:
    """Write a local inspection record without deriving reference classes."""
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def draw_image(ax: plt.Axes,image: np.ndarray,valid: np.ndarray,zoom: bool,title: str) -> None:
    """Show fixed metric extents and identical support outlines for every observation."""
    colors=np.clip(image/0.30,0,1).copy()
    colors[~valid]=[0.55,0.55,0.55]
    ax.imshow(colors,extent=[-245,245,-245,245],origin='upper',interpolation='nearest')
    for size,color,style in [(10,'#ffcc33',':'),(30,'#ffffff','-'),(50,'#33ddff','--'),(90,'#dddddd',':')]:
        ax.add_patch(Rectangle((-size/2,-size/2),size,size,fill=False,color=color,linestyle=style,lw=0.8))
    extent=55 if zoom else 245
    ax.set_xlim(-extent,extent);ax.set_ylim(-extent,extent)
    ax.set_title(title,fontsize=9);ax.tick_params(labelsize=7)
    ax.set_xlabel('east offset (m)',fontsize=7);ax.set_ylabel('north offset (m)',fontsize=7)


def main() -> None:
    """Check all original payloads before reading guarded chips and rendering views."""
    plan_path=ROOT/'REFERENCE_SOURCE_PLAN_V2.json'
    plan_hash=hashlib.sha256(plan_path.read_bytes()).hexdigest()
    if plan_hash!=(ROOT/'REFERENCE_SOURCE_PLAN_V2.sha256').read_text(encoding='utf-8').strip():
        raise RuntimeError('Frozen plan changed')
    if (OUT/'PACKET_LOCK.json').exists():
        raise RuntimeError('Existing packet is locked; do not overwrite or silently rerender')
    OUT.mkdir(exist_ok=True);(OUT/'images').mkdir(exist_ok=True)
    requests=json.loads(plan_path.read_text(encoding='utf-8'))['requests']
    case_ids=sorted({row['case_id'] for row in requests})
    aliases={case:f'R{i:02d}' for i,case in enumerate(case_ids,1)}
    private=[];audit=[];observation_forms=[];temporal_forms=[]
    protocol=ROOT/'OPTICAL_RESPONSE_PROTOCOL_V1.md'
    protocol_hash=hashlib.sha256(protocol.read_bytes()).hexdigest()
    # All TIFF headers and hashes first. This opens metadata, never pixel arrays.
    for row in requests:
        receipt=json.loads((ROOT/'reference_receipts'/(row['id']+'.json')).read_text(encoding='utf-8'))
        if receipt['source_plan_sha256']!=plan_hash:
            raise RuntimeError('Acquisition receipt source plan mismatch')
        if receipt['status']!='ACQUIRED_NOT_INTERPRETED':
            continue
        path=Path(receipt['path'])
        with rasterio.open(path) as ds:
            expected=Affine(*row['chip_grid']['transform'])
            names=receipt['bands']+['valid_'+b for b in receipt['bands']]
            if (ds.width,ds.height,ds.count,ds.crs.to_epsg())!=(49,49,len(names),32750):
                raise RuntimeError('Downloaded dimensions/bands/CRS mismatch')
            if not ds.transform.almost_equals(expected,precision=1e-7):
                raise RuntimeError('Downloaded affine mismatch')
            if any(ds.descriptions) and tuple(ds.descriptions)!=tuple(names):
                raise RuntimeError('Downloaded band descriptions/order mismatch')
            x0,y0=expected*(0,0);x1,y1=expected*(49,49)
            evidence=Evidence(row['id'],Role.DEV_REFERENCE,Role.DEV_REFERENCE,
                independent_measurement=True,acquisition_utc=row['optical_datetime'])
            scope=PixelScope('FROZEN_DOWNLOADED_CHIP',Role.DEV_REFERENCE,row['id'],'EPSG:32750',
                box(min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1)),
                operation_authorization_record='REFERENCE_SOURCE_PLAN_V2.json + OPTICAL_RESPONSE_PROTOCOL_V1.md')
            guard=check_native_window(evidence,Actor.DEVELOPER,scope,NativeWindow(0,0,49,49),
                ds.transform.to_gdal(),source_crs='EPSG:32750',source_width=49,source_height=49,halo=0,padding=0)
            save(ROOT/'LOCAL_PIXEL_PREREAD_LAST.json',{'id':row['id'],'check':guard,'before_body_hash_and_pixel_read':True})
        if hashlib.sha256(path.read_bytes()).hexdigest()!=receipt['payload']['sha256']:
            raise RuntimeError('Downloaded source body differs from frozen receipt')
    for case in case_ids:
        alias=aliases[case];rows=[r for r in requests if r['case_id']==case]
        fig,axes=plt.subplots(4,3,figsize=(13,15),layout='constrained')
        target_interval=rows[0]['S1_filename_interval_utc']
        fig.suptitle(f'{alias} | target UTC {target_interval[0]} to {target_interval[1]}\n'
            'OPTICAL ONLY | fixed reflectance 0-0.30 | 10m dotted yellow,30m white,50m cyan,90m gray\n'
            'North up; EPSG32750; source QA is diagnostic; no water labels or predictions',fontsize=10)
        observations=[]
        for index,row in enumerate(rows):
            observation=f'O{index+1:02d}'
            receipt=json.loads((ROOT/'reference_receipts'/(row['id']+'.json')).read_text(encoding='utf-8'))
            private.append({'neutral_id':alias,'observation':observation,'original_id':row['id'],
                'original_case':case,'status':receipt['status']})
            form={'neutral_id':alias,'observation':observation,'optical_utc':row.get('optical_datetime',''),
                'support_m':30,'w_min':'','w_max':'','n_min':'','n_max':'','o_min':'','o_max':'','u_min':'','u_max':'',
                'visible_mixture':'','confidence':'','registration_notes':'','evidence_notes':'','response_status':'NOT_REVIEWED'}
            observation_forms.append(form)
            if receipt['status']!='ACQUIRED_NOT_INTERPRETED':
                for ax in axes[index]:
                    ax.axis('off');ax.text(0.5,0.5,f'{observation}: {receipt["status"]}\nUNKNOWN',ha='center',va='center',wrap=True)
                observations.append({'observation':observation,'status':receipt['status']})
                continue
            path=Path(receipt['path']);grid=row['chip_grid'];affine=Affine(*grid['transform'])
            # Scope comes from the frozen manifest, not from a fitted/read-derived footprint.
            x0,y0=affine*(0,0);x1,y1=affine*(49,49)
            evidence=Evidence(row['id'],Role.DEV_REFERENCE,Role.DEV_REFERENCE,
                independent_measurement=True,acquisition_utc=row['optical_datetime'])
            scope=PixelScope('FROZEN_DOWNLOADED_CHIP',Role.DEV_REFERENCE,row['id'],'EPSG:32750',
                box(min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1)),
                operation_authorization_record='REFERENCE_SOURCE_PLAN_V2.json + OPTICAL_RESPONSE_PROTOCOL_V1.md')
            with rasterio.open(path) as ds:
                guard=check_native_window(evidence,Actor.DEVELOPER,scope,NativeWindow(0,0,49,49),
                    ds.transform.to_gdal(),source_crs='EPSG:32750',source_width=49,source_height=49,halo=0,padding=0)
                save(ROOT/'LOCAL_PIXEL_PREREAD_LAST.json',{'id':row['id'],'check':guard,'before_pixel_read':True})
                data=ds.read()
            n=len(receipt['bands']);raw=data[:n];masks=data[n:]
            if not np.isin(masks,[0,1]).all():
                raise RuntimeError('Validity flags changed by interpolation')
            for b in range(4,n):
                values=raw[b][masks[b]==1]
                upper=11 if row['provider']=='S2' else 65535
                if not (np.isfinite(values).all() and np.equal(values,np.floor(values)).all()
                        and (values>=0).all() and (values<=upper).all()):
                    raise RuntimeError('Categorical QA encoding/order sanity check failed')
            available,flagged=diagnostic_qa(raw,row['provider'],masks)
            physical=reflectance(raw[:4],row['provider'])
            rgb=np.moveaxis(physical[:3],0,-1);nir=np.moveaxis(physical[[3,0,1]],0,-1)
            native_sr_valid=np.all(masks[:4]==1,axis=0)&np.isfinite(physical).all(axis=0)
            props=receipt['source_properties']
            allowed_props={k:props[k] for k in ['PROCESSING_BASELINE','COLLECTION_CATEGORY','GEOMETRIC_RMSE_MODEL',
                'GEOMETRIC_RMSE_MODEL_X','GEOMETRIC_RMSE_MODEL_Y','GEOMETRIC_RMSE_VERIFY','SPACECRAFT_ID'] if k in props}
            support={str(size):support_scenarios(available,flagged,size) for size in [10,30,50]}
            source_summary={'neutral_id':alias,'observation':observation,'provider':row['provider'],
                'optical_utc':row['optical_datetime'],'offset_hours':row['offset_hours'],
                'nominal_native_resolution_m':row['nominal_native_resolution_m'],
                'processing_and_geolocation':allowed_props,'local_native_guard':guard,
                'band_identity_evidence':'Frozen ordered select/addBands request and band count; returned TIFF has no band descriptions. QA integer/range and binary-mask sanity checks pass; no independent per-band identity checksum.',
                'payload_sha256':receipt['payload']['sha256'],
                'joint_sr_valid_fraction':float(native_sr_valid.mean()),
                'available_fraction':float(available.mean()),'qa_flagged_fraction':float(flagged.mean()),
                'support_diagnostics':support,
                'physical_sr_range_by_band':[[float(physical[b][native_sr_valid].min()),float(physical[b][native_sr_valid].max())]
                    if native_sr_valid.any() else None for b in range(4)],
                'negative_sr_values_retained':int(((physical<0)&native_sr_valid).sum()),
                'above_one_sr_values_retained':int(((physical>1)&native_sr_valid).sum()),
                'semantic_response':'NOT_REVIEWED','temporal_transfer':'UNKNOWN'}
            audit.append(source_summary)
            metadata_label=f'{observation} {row["provider"]} {row["side"]} | {row["optical_datetime"]}\n'
            nominal=support['30']['nominal']
            draw_image(axes[index,0],rgb,native_sr_valid,False,
                metadata_label+f'native {row["nominal_native_resolution_m"]}m; offset {row["offset_hours"]:+.1f}h | RGB 490m')
            draw_image(axes[index,1],rgb,native_sr_valid,True,'RGB central 110m | '+
                f'30m available {nominal["available_fraction"]:.2f}; QA flagged {nominal["qa_flagged_fraction"]:.2f}')
            draw_image(axes[index,2],nir,native_sr_valid,True,'NIR-red-green central 110m | not a class map')
            observations.append({k:source_summary[k] for k in ['observation','provider','optical_utc','offset_hours',
                'nominal_native_resolution_m','processing_and_geolocation']})
        image_path=OUT/'images'/(alias+'_optical.png')
        if sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())+8*1024**2>1024**3:
            raise RuntimeError('Additional storage ceiling before packet image')
        fig.savefig(image_path,dpi=140);plt.close(fig)
        save(OUT/(alias+'_metadata.json'),{'neutral_id':alias,'target_acquisition_utc':target_interval,
            'support_m':[10,30,50],'primary_support_m':30,'displacement_scenarios_m':[-20,-10,0,10,20],
            'protocol_sha256':protocol_hash,'observations':observations})
        temporal_forms.append({'neutral_id':alias,'target_acquisition_utc':target_interval[0],
            'evidence_tier':'','continuity_notes':'','event_evidence':'','temporal_transfer':'UNKNOWN',
            'acquisition_time_eligibility':'UNKNOWN','conditional_interval_notes':'','response_status':'NOT_REVIEWED'})
        print('PREPARED',alias,flush=True)
    save(ROOT/'PRIVATE_REVIEW_KEY.json',{'aliases':private,'not_reader_material':True})
    save(ROOT/'OPTICAL_TECHNICAL_AUDIT.json',{'protocol_sha256':protocol_hash,'observations':audit,
        'status':'SOURCE_GRID_MASK_AND_DISPLAY_AUDIT_NOT_SEMANTIC_ADJUDICATION'})
    for filename,forms in [('OPTICAL_RESPONSE_BLANK.csv',observation_forms),('TEMPORAL_RESPONSE_BLANK.csv',temporal_forms)]:
        with (OUT/filename).open('w',newline='',encoding='utf-8') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(forms[0]));writer.writeheader();writer.writerows(forms)
    (OUT/'INSTRUCTIONS.md').write_text(protocol.read_text(encoding='utf-8'),encoding='utf-8')
    summary={'status':'TECHNICAL_QA_AND_OPTICAL_PACKET_PREPARED_NOT_INTERPRETED',
        'completed_utc':datetime.now(timezone.utc).isoformat(),'request_slots':96,'acquired':len(audit),
        'absent_opportunities':96-len(audit),'date_supports':len(case_ids),'physical_locations':12,
        'grid_body_and_band_count_checks_passed':len(audit),'local_pixel_preread_checks_passed':len(audit),
        'band_identity_caveat':'TIFF descriptions absent; order traced from frozen ordered select/addBands request, not independently certified by file labels. QA ranges/binary flags checked.',
        'all_sources_have_full_sr_support':all(r['joint_sr_valid_fraction']==1 for r in audit),
        'provider_counts':dict(Counter(r['provider'] for r in audit)),
        'primary30_nominal_available_unflagged_positive':sum(r['support_diagnostics']['30']['nominal']['available_unflagged_fraction']>0 for r in audit),
        'reference_classes_released':0,'comparison_gate':'CLOSED','source_roles_unchanged':True,
        'reference_adequacy':'NOT_YET_ADJUDICATED','qa_is_not_reference_truth':True}
    save(ROOT/'OPTICAL_PREPARATION_SUMMARY.json',summary)
    manifest={p.relative_to(OUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(OUT.rglob('*')) if p.is_file()}
    save(OUT/'PACKET_LOCK.json',{'status':'LOCKED_BEFORE_REFERENCE_RESPONSES',
        'protocol_sha256':protocol_hash,'files':manifest,'no_prediction_material':True})
    save(ROOT/'STATUS.json',{'phase':summary['status'],'utc':summary['completed_utc'],
        'no_background_job':True,'comparison_gate':'CLOSED','next':'SOURCE_DISPLAY_VISUAL_QA_AND_OPTICAL_RESPONSE'})
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':
    main()
