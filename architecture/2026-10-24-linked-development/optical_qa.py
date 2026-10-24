"""Pure optical radiometry, diagnostic QA and fixed support calculations."""
from __future__ import annotations
import numpy as np


def reflectance(raw: np.ndarray,provider: str) -> np.ndarray:
    """Apply collection scaling once, without clipping physical values."""
    if provider=='S2':
        return raw.astype('float64')*0.0001
    if provider=='LS':
        return raw.astype('float64')*0.0000275-0.2
    raise ValueError('Unknown optical provider')


def diagnostic_qa(raw: np.ndarray,provider: str,native_valid: np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    """Return available and flagged masks; deliberately ignore source water classes."""
    valid=np.all(native_valid==1,axis=0)&np.all(np.isfinite(raw),axis=0)
    if provider=='S2':
        quality=raw[4].astype('int32')
        valid=valid&(quality!=0)
        flagged=np.isin(quality,[1,3,8,9,10,11])
    elif provider=='LS':
        quality=raw[4].astype('int32');sat=raw[5].astype('int32')
        valid=valid&((quality&1)==0)
        flagged=((quality&62)!=0)|((sat&((1<<1)|(1<<2)|(1<<3)|(1<<4)|(1<<11)))!=0)
    else:
        raise ValueError('Unknown optical provider')
    return valid,flagged&valid


def support_scenarios(valid: np.ndarray,flagged: np.ndarray,size: int) -> dict:
    """Retain all 25 fixed displacement fractions; no independent-pixel claims."""
    if size not in {10,30,50} or valid.shape!=(49,49) or flagged.shape!=(49,49):
        raise ValueError('Unexpected support/grid')
    radius=(size//10)//2
    scenarios=[]
    for dy in [-20,-10,0,10,20]:
        for dx in [-20,-10,0,10,20]:
            c=24+dx//10;r=24-dy//10
            region=(slice(r-radius,r+radius+1),slice(c-radius,c+radius+1))
            scenarios.append({'dx_m':dx,'dy_m':dy,'available_fraction':float(valid[region].mean()),
                'qa_flagged_fraction':float(flagged[region].mean()),
                'available_unflagged_fraction':float((valid&~flagged)[region].mean())})
    return {'support_m':size,'scenario_count':25,'scenarios':scenarios,
        'available_unflagged_range':[min(s['available_unflagged_fraction'] for s in scenarios),
            max(s['available_unflagged_fraction'] for s in scenarios)],
        'nominal':scenarios[12]}
