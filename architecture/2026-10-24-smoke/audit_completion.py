"""Read-only final integrity/support/resource audit; no inference or network."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import os
import sys
from datetime import datetime

ROOT=Path(__file__).resolve().parent
PREP=ROOT.parent/'NATIVE_MODEL_READINESS_20261023'
RUNTIME=Path('E:/Bendungan_Kusan/Model_Runtime/s1_smoke_cpu_20261024')


def sha256(path: Path) -> str:
    """Hash a file without loading its full body into memory."""
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024**2),b''):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    """Verify the completed artifacts, qualifying what was actually exercised."""
    os.environ.setdefault('GDAL_DATA','E:/Bendungan_Kusan/Miniforge/envs/kusan-c1/Library/share/gdal')
    os.environ.setdefault('PROJ_DATA','E:/Bendungan_Kusan/Miniforge/envs/kusan-c1/Library/share/proj')
    import numpy as np
    import rasterio
    sys.path.insert(0,str(PREP))
    from input_contract import validate_output_grid,current_validity,validate_stats
    result=json.loads((ROOT/'SMOKE_RESULT.json').read_text(encoding='utf-8'))
    if result['status']!='TECHNICAL_SMOKE_PASS':
        raise RuntimeError('No successful numerical smoke result')
    original=json.loads((PREP/'PACKAGE_SHA256.json').read_text(encoding='utf-8'))
    assert all(sha256(PREP/name)==digest for name,digest in original['files'].items())
    contract=json.loads((PREP/'FROZEN_ARTIFACT_CONTRACT.json').read_text(encoding='utf-8'))
    payloads=[]
    for item in contract['files']:
        if item['variant']!='s1_only_resnet34':
            continue
        file=RUNTIME/'model'/Path(item['path']).name
        assert file.stat().st_size==item['bytes'] and sha256(file)==item['expected_sha256']
        payloads.append({'file':file.name,'bytes':item['bytes'],'sha256':item['expected_sha256']})
    receipt=json.loads((ROOT/'INPUT_RECEIPT.json').read_text(encoding='utf-8'))
    assert (ROOT/'CURRENT_INPUT.tif').stat().st_size==receipt['payload']['bytes']
    assert sha256(ROOT/'CURRENT_INPUT.tif')==receipt['payload']['sha256']
    checks=json.loads((ROOT/'PRE_READ_WINDOW_CHECKS.json').read_text(encoding='utf-8'))
    assert len(checks)==3 and all(c['check']['status']=='WINDOW_POLICY_CHECK_PASSED_NOT_AN_IO_OPERATION' for c in checks)
    grid=json.loads((PREP/'PROPOSED_SMOKE_INPUT_FREEZE.json').read_text(encoding='utf-8'))['grid']
    arrays={}
    rasters=[]
    for name in ['CURRENT_INPUT.tif','UNVALIDATED_SCORE.tif','CURRENT_SUPPORT.tif','DISTANCE_TO_INVALID_OR_EDGE_PIXELS.tif']:
        with rasterio.open(ROOT/name) as source:
            validate_output_grid(grid,dict(crs=source.crs.to_string(),width=source.width,height=source.height,transform=list(source.transform)[:6]))
            arrays[name]=source.read()
            rasters.append({'file':name,'bytes':(ROOT/name).stat().st_size,'sha256':sha256(ROOT/name),
                            'band_names':list(source.descriptions),'nodata':source.nodata,'dtype':list(source.dtypes)})
    raw=arrays['CURRENT_INPUT.tif']
    valid=current_validity(raw[:3],(raw[3:]>0)&(raw[:3]!=-9999))
    support=arrays['CURRENT_SUPPORT.tif'][0]
    score=arrays['UNVALIDATED_SCORE.tif'][0]
    distance=arrays['DISTANCE_TO_INVALID_OR_EDGE_PIXELS.tif'][0]
    assert np.array_equal(valid,support.astype(bool)) and set(np.unique(support))<={0,1}
    assert np.isfinite(score[valid]).all() and np.all((score[valid]>=0)&(score[valid]<=1))
    assert np.all(score[~valid]==-9999)
    assert np.isfinite(distance).all() and np.all(distance>=0)
    with np.load(RUNTIME/'model/band_stats.npz',allow_pickle=False) as stats:
        validate_stats(stats['mean'],stats['std'],3)
    runtime_bytes=sum(p.stat().st_size for p in RUNTIME.rglob('*') if p.is_file())
    run_bytes=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
    budget=json.loads((ROOT/'RESOURCE_BUDGET.json').read_text(encoding='utf-8'))
    assert runtime_bytes+run_bytes<6*1024**3
    assert budget['charged_bytes']<=2*1024**3
    completed_status=ROOT/'attempts/completed_controller_status.json'
    finish=json.loads((completed_status if completed_status.exists() else ROOT/'STATUS.json').read_text(encoding='utf-8'))
    if finish['phase']!='TECHNICAL_SMOKE_FINISHED_REVIEW_REQUIRED':
        raise RuntimeError('Original completed-controller timing receipt is required')
    started=datetime.fromisoformat('2026-10-24T11:10:14.440228+00:00')
    ended=datetime.fromisoformat(finish['utc'])
    report={'status':'FINAL_NUMERICAL_AND_RESOURCE_AUDIT_PASS',
        'readiness_files_unchanged':len(original['files']),'model_payloads':payloads,
        'rasters':rasters,'pre_read_band_guards_passed':len(checks),
        'current_valid_pixels':int(valid.sum()),'current_total_pixels':int(valid.size),
        'actual_missing_current_pixels':int((~valid).sum()),
        'missing_current_test_qualification':'This patch has no missing current pixels; real nodata failure behaviour was not empirically exercised by this smoke. Existing synthetic guards are separate evidence.',
        'normalization_verified':True,'output_grid_verified':True,
        'runtime_storage_bytes':runtime_bytes,'run_artifact_storage_bytes':run_bytes,
        'storage_bytes_total':runtime_bytes+run_bytes,'storage_ceiling_bytes':6*1024**3,
        'transfer_accounting':budget,
        'timing':{'controller_phase_span_seconds':(ended-started).total_seconds(),
                  'within_script_seconds':result['total_seconds'],
                  'four_flip_forward_seconds':result['four_flip_inference_seconds'],
                  'qualification':'Different clock boundaries; startup/launch/teardown difference not separately instrumented. No whole-scene/full-series runtime extrapolation.'},
        'peak_memory':'NOT_MEASURED','accuracy':'NOT_MEASURED',
        'independent_absolute_registration':'NOT_MEASURED',
        'scientific_method_frozen':False,'further_processing_queued':False}
    (ROOT/'COMPLETION_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'storage_GiB':round((runtime_bytes+run_bytes)/1024**3,3),
                      'charged_transfer_GiB':round(budget['charged_bytes']/1024**3,3)}))


if __name__=='__main__':
    main()
