"""One frozen model, one patch, CPU/four-flip scores; no fitting or labels."""
from __future__ import annotations
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT=Path(__file__).resolve().parent
PREP=ROOT.parent/'NATIVE_MODEL_READINESS_20261023'
RUNTIME=Path('E:/Bendungan_Kusan/Model_Runtime/s1_smoke_cpu_20261024')


def load_module(name: str,path: Path):
    """Import a previously pinned local source without running its main routine."""
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    """Strictly load verified state tensors and write support-aware unvalidated scores."""
    start=time.monotonic()
    os.environ.update(TORCH_HOME=str(RUNTIME/'torch-cache'),
        HF_HOME=str(RUNTIME/'hf-cache'),HF_HUB_OFFLINE='1',
        MPLCONFIGDIR=str(RUNTIME/'matplotlib'),XDG_CACHE_HOME=str(RUNTIME/'xdg-cache'),
        GDAL_DATA=str(Path(sys.prefix)/'Lib/site-packages/rasterio/gdal_data'),
        PROJ_DATA=str(Path(sys.prefix)/'Lib/site-packages/rasterio/proj_data'))
    import numpy as np
    import rasterio
    import torch
    from scipy.ndimage import distance_transform_edt
    sys.path.insert(0,str(PREP))
    from input_contract import current_validity,validate_stats,validate_output_grid
    torch.set_num_threads(4)
    torch.manual_seed(0) # Technical construction only; not a reference-sample randomization.
    contract=json.loads((PREP/'FROZEN_ARTIFACT_CONTRACT.json').read_text(encoding='utf-8'))
    for item in contract['files']:
        if item['variant']=='s1_only_resnet34':
            local=RUNTIME/'model'/Path(item['path']).name
            if local.stat().st_size!=item['bytes'] or hashlib.sha256(local.read_bytes()).hexdigest()!=item['expected_sha256']:
                raise RuntimeError('Frozen payload verification failed before loading')
    if hashlib.sha1((PREP/'FROZEN_RELEASE_TRAINER.py').read_bytes()).hexdigest()!=contract['trainer_raw_sha1']:
        raise RuntimeError('Exact release trainer changed')
    grid=json.loads((PREP/'PROPOSED_SMOKE_INPUT_FREEZE.json').read_text(encoding='utf-8'))['grid']
    with rasterio.open(ROOT/'CURRENT_INPUT.tif') as source:
        observed=dict(crs=source.crs.to_string(),width=source.width,height=source.height,transform=list(source.transform)[:6])
        validate_output_grid(grid,observed)
        if source.count!=6:
            raise RuntimeError('Expected three observations and three separate masks')
        arrays=source.read()
        profile=source.profile.copy()
    values=arrays[:3]
    mask_values=arrays[3:]
    if not np.isfinite(mask_values).all() or np.any(mask_values<0) or np.any(mask_values>1):
        raise RuntimeError('Invalid source mask encoding')
    band_valid=(mask_values>0)&(values!=-9999)
    support=current_validity(values,band_valid)
    if not support.any():
        raise RuntimeError('No jointly valid current measurements')
    with np.load(RUNTIME/'model/band_stats.npz',allow_pickle=False) as stats:
        mean=stats['mean'].astype(np.float32)
        std=stats['std'].astype(np.float32)
    validate_stats(mean,std,3)
    # Match upstream fill at invalid current locations, retaining those locations as nodata.
    prepared=np.where(support[None],values,mean[:,None,None])
    prepared=(prepared-mean[:,None,None])/std[:,None,None]
    if not np.isfinite(prepared).all():
        raise RuntimeError('Nonfinite normalized input')
    infer=load_module('pinned_kusan_infer',PREP/'upstream/src/infer.py')
    trainer=infer.load_training_module(PREP/'FROZEN_RELEASE_TRAINER.py')
    device=torch.device('cpu')
    args=infer.build_model_args('s1',RUNTIME/'model','ce_dice',0)
    dls=infer.build_dummy_dls(trainer,3,512,RUNTIME/'model',device)
    learner=trainer.build_learner(args,dls)
    state=torch.load(RUNTIME/'model/s1dw_resnet34_best.pth',map_location='cpu',weights_only=True)
    if isinstance(state,dict) and 'model' in state:
        state=state['model']
    learner.model.load_state_dict(state,strict=True)
    model=learner.model.to(device).eval()
    inference_start=time.monotonic()
    with torch.inference_mode():
        logits=infer.forward_logits(model,torch.from_numpy(prepared[None].astype(np.float32)),device,False,True).numpy()[0]
    if logits.shape!=(2,512,512) or not np.isfinite(logits).all():
        raise RuntimeError('Invalid output logits')
    scores=infer.softmax_water_probability(logits)
    if scores.shape!=(512,512) or not np.isfinite(scores[support]).all() or np.any(scores[support]<0) or np.any(scores[support]>1):
        raise RuntimeError('Invalid supported model scores')
    scores[~support]=-9999
    profile.update(driver='GTiff',count=1,dtype='float32',nodata=-9999,compress='deflate')
    with rasterio.open(ROOT/'UNVALIDATED_SCORE.tif','w',**profile) as output:
        output.write(scores,1)
        output.set_band_description(1,'Unvalidated released-model score; development engineering only')
        output.update_tags(role='PERMANENT_DEVELOPMENT_ENGINEERING',semantic_release='NONE',accuracy='NOT_MEASURED')
    profile.update(dtype='uint8',nodata=None)
    with rasterio.open(ROOT/'CURRENT_SUPPORT.tif','w',**profile) as output:
        output.write(support.astype(np.uint8),1)
    # Continuous diagnostic only: no new reliability or semantic acceptance cutoff.
    distance=distance_transform_edt(np.pad(support,1,constant_values=False))[1:-1,1:-1].astype(np.float32)
    profile.update(dtype='float32',nodata=None)
    with rasterio.open(ROOT/'DISTANCE_TO_INVALID_OR_EDGE_PIXELS.tif','w',**profile) as output:
        output.write(distance,1)
    with rasterio.open(ROOT/'UNVALIDATED_SCORE.tif') as output:
        validate_output_grid(grid,dict(crs=output.crs.to_string(),width=output.width,height=output.height,transform=list(output.transform)[:6]))
        saved=output.read(1)
        assert np.all(saved[~support]==-9999)
    result={'status':'TECHNICAL_SMOKE_PASS','role':'PERMANENT_DEVELOPMENT_ENGINEERING',
        'total_seconds':time.monotonic()-start,'four_flip_inference_seconds':time.monotonic()-inference_start,
        'shape':[512,512],'joint_current_support_pixels':int(support.sum()),'total_pixels':int(support.size),
        'valid_pixels_by_band':[int(v.sum()) for v in band_valid],
        'score_min':float(scores[support].min()),'score_max':float(scores[support].max()),
        'score_quantiles':np.quantile(scores[support],[0,.01,.25,.5,.75,.99,1]).tolist(),
        'torch':torch.__version__,'cpu_threads':torch.get_num_threads(),'strict_state_load':True,
        'safe_weights_only_load':True,'tta':'Mean logits across identity,H,V,HV then softmax',
        'normalization':'Exact released three-band statistics; no local fitting',
        'input_band_quantiles_on_joint_support':{name:np.quantile(values[i][support],[0,.01,.5,.99,1]).tolist() for i,name in enumerate(['VV','VH','angle'])},
        'limitations':['No independent reference comparison or accuracy claim','Scores are not locally calibrated probabilities',
                      'Missing/edge context can affect supported neighbours; distance output is descriptive, not a reliability mask',
                      'No claim of equivalence with accepted SNAP/C1 radiometry','Two-scale visual overlay QA pending actual inspection']}
    (ROOT/'SMOKE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
