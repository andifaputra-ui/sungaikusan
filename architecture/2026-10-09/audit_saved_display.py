"""Guarded numerical display/QA audit of already acquired development chips.

No source changes, reference interpretation, SAR values, network, or new panels.
The full cached 49x49 read is authorized and checked before file bytes are read.
All source pixels are in legacy PASS receipts; failed/quarantined reads stay out.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys
import time
from urllib.parse import urlparse

import numpy as np
from shapely.geometry import box

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'ROLE_GUARD'))
sys.path.insert(0, str(HERE / 'OPTICAL_CONTRACT'))
from role_guard import Evidence, Role, Actor, PixelScope, NativeWindow, check_native_window
from optical_display_contract import legacy_display, render, scl_evidence


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    start = time.monotonic()
    pool = read(HERE/'EXISTING_DEVELOPMENT_EVIDENCE_POOL.json')
    metadata = read(HERE/'OPTICAL_CONTRACT/SAVED_METADATA_AUDIT.json')
    items = {x['id']: x for x in metadata['items']}
    wave = HERE.parent/'REFERENCE_QUALIFICATION_WAVE2'
    samples = {x['id']:x for x in read(wave/'SAMPLE.json')}
    # Freeze scopes from the previously executed producer's fixed grid, never
    # by shrinking/expanding them to accommodate a requested read.
    scopes = []
    for row in pool:
        s = samples[row['record_id']]
        scopes.append({'id': row['evidence_id'], 'bounds': [s['x']-245,s['y']-245,s['x']+245,s['y']+245],
                       'width':49,'height':49,'crs':'EPSG:32750',
                       'source_sha256':row['stored_chip_sha256_recorded_not_reread']})
    (HERE/'SAVED_CHIP_SCOPE_MANIFEST.json').write_text(json.dumps(scopes,indent=2)+'\n',encoding='utf-8')
    outputs=[]
    for row, declared in zip(pool,scopes, strict=True):
        item=items[row['optical_item_id']]
        s=samples[row['record_id']]
        transform=(10.,0.,s['x']-245,0.,-10.,s['y']+245)
        gdal_transform=(transform[2],transform[0],transform[1],transform[5],transform[3],transform[4])
        e=Evidence(row['evidence_id'],Role.DEV_REFERENCE,Role.DEV_REFERENCE,
                   independent_measurement=True,acquisition_utc=row['optical_datetime'])
        scope=PixelScope('SAVED_WAVE2_PASS_ONLY',Role.DEV_REFERENCE,e.artifact_id,'EPSG:32750',
                         box(*declared['bounds']),operation_authorization_record='AUTHORIZATION_AND_MIGRATION.json: existing-evidence source/display qualification')
        permit=check_native_window(e,Actor.DEVELOPER,scope,NativeWindow(0,0,49,49),gdal_transform,
                                  source_crs='EPSG:32750',source_width=49,source_height=49)
        # The NPZ is loaded in full, so the permit is for the full cached extent.
        path=Path(row['stored_chip_path']).resolve()
        if path.parent != (wave/'chips').resolve() or path.suffix != '.npz':
            raise RuntimeError('Unexpected cached chip path; stop before file byte access')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=declared['source_sha256']:
            raise RuntimeError('Saved chip identity mismatch; stop, do not repair or reread source')
        with np.load(path,allow_pickle=False) as z:
            data=z['data'].copy()
            saved_transform=z['transform'].tolist()
        if data.shape!=(5,49,49) or not np.allclose(saved_transform[:6],transform,rtol=0,atol=1e-7):
            raise RuntimeError('Cached source grid mismatch')
        receipt=read(wave/'receipts'/f"{row['evidence_id']}.json")
        host=urlparse(receipt['bands']['red']['href']).hostname
        bands=[receipt['bands'][b]['raster_band_metadata'][0] for b in ('red','green','blue','nir')]
        frame=legacy_display(data[:4],source_collection='sentinel-2-l2a',source_host=host,
                             bands=bands,baseline=item['baseline'],boa_offset_applied=item['boa_offset_applied'])
        rgb,rgb_info=render(frame,'RGB')
        nir,nir_info=render(frame,'NIR')
        assert not frame.quantitative_allowed
        qa=scl_evidence(data[4],baseline=item['baseline'])
        oldvalid=(data[:4]!=0).all(axis=0)
        newvalid=(data[:3]!=0).all(axis=0)
        # Historical rendering is compared on formerly valid pixels, avoiding
        # any claim that a masking-policy difference changes a reference state.
        oldrgb=np.moveaxis(np.rint(np.clip(data[:3].astype(np.float64)*.0001/.3,0,1)**.7*255).astype(np.uint8),0,-1)
        same=bool(np.array_equal(rgb[oldvalid],oldrgb[oldvalid]))
        if not same:
            raise RuntimeError('Display transform failed reproducibility check')
        tile_r,tile_c=row['prospective_disjoint_tile_row_col']
        # Tile centre on the cached map lattice; all sampled Wave2 tiles are full.
        rr=24+(tile_r*3+1-s['row'])
        cc=24+(tile_c*3+1-s['col'])
        support={}
        for size,radius in ((10,0),(30,1),(50,2)):
            subset=(slice(rr-radius,rr+radius+1),slice(cc-radius,cc+radius+1))
            vals=data[4][subset]
            support[str(size)]={
                'posted_pixels':int(vals.size),
                'rgb_non_nodata_fraction':float(newvalid[subset].mean()),
                'nir_composite_non_nodata_fraction':float(frame.valid_by_band[[3,0,1]].all(axis=0)[subset].mean()),
                'scl_counts':{str(k):int(v) for k,v in zip(*np.unique(vals.astype(int),return_counts=True))},
                'interpretation':'QA categories only; no clear/water/nonwater label or temporal transfer inferred'
            }
        outputs.append({'evidence_id':row['evidence_id'],'source_sha256_verified':declared['source_sha256'],
            'permit':permit,'display_proxy_state':frame.source_state,
            'offset_metadata_conflict_retained':frame.provenance['metadata_offset_conflict'],
            'old_valid_rgb_values_reproduced':same,
            'rgb_pixels_previously_hidden_only_by_nir_nodata':int(np.sum(newvalid & ~oldvalid)),
            'rgb':rgb_info,'nir':nir_info,'support_sensitivity':support,
            'raw_values_unchanged':True,'source_scl_preserved':True})
    (HERE/'SAVED_DISPLAY_QA_RECORDS.json').write_text(json.dumps(outputs,indent=2)+'\n',encoding='utf-8')
    dates=sorted({x['s1_datetime'][:10] for x in pool})
    existing=read(HERE.parent/'TEMPORAL_OBJECT_GATES/EIGHT_DATE_REGISTER.json')
    existing_dates={x['date'][:10] for x in existing}
    summary={
        'status':'SAVED_LEGACY_DISPLAY_PROXY_TECHNICALLY_REPRODUCED_NOT_CALIBRATED',
        'guarded_saved_chips':len(outputs),'hash_and_grid_verified':len(outputs),
        'historical_valid_rgb_transform_reproduced':sum(x['old_valid_rgb_values_reproduced'] for x in outputs),
        'offset_conflict_views_retained':sum(x['offset_metadata_conflict_retained'] for x in outputs),
        'views_with_rgb_mask_change_from_nir_nodata':sum(x['rgb_pixels_previously_hidden_only_by_nir_nodata']>0 for x in outputs),
        'rgb_pixels_previously_hidden_only_by_nir_nodata':sum(x['rgb_pixels_previously_hidden_only_by_nir_nodata'] for x in outputs),
        'qa_only_complete_rgb_support_views':{k:sum(x['support_sensitivity'][k]['rgb_non_nodata_fraction']==1 for x in outputs) for k in ['10','30','50']},
        'warning':'Non-nodata is not clear sky, correct radiometry or observable state. No semantic response was generated.',
        'existing_eight_sar_date_intersection':sorted(set(dates)&existing_dates),
        'existing_sar_date_match_views':sum(x['s1_datetime'][:10] in existing_dates for x in pool),
        'new_reference_responses':0,'new_imagery_bytes':0,'new_sar_processing':0,
        'elapsed_seconds':round(time.monotonic()-start,3),
        'next_use':'Prospective development visual inspection may use this explicitly marked proxy. Quantitative optical use stays blocked; old responses and intervals are unchanged.'}
    (HERE/'SAVED_DISPLAY_QA_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
