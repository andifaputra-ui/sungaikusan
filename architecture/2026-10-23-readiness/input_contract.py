"""Pure-array input safeguards for the proposed frozen-model smoke test.

No network, model, image IO or class assignment. Caller supplies per-band
source validity and retains source/grid/normalization identities separately.
"""
from __future__ import annotations
import numpy as np


class InputContractError(ValueError):
    """Input cannot be used without changing its declared contract."""


def current_validity(values: np.ndarray, band_valid: np.ndarray) -> np.ndarray:
    """Require all three current VV/VH/angle observations, not a band-mask union."""
    values=np.asarray(values)
    band_valid=np.asarray(band_valid)
    if values.ndim!=3 or values.shape[0]!=3:
        raise InputContractError('Expected current VV/VH/angle in that order')
    if band_valid.shape!=values.shape or band_valid.dtype!=np.bool_:
        raise InputContractError('Explicit boolean per-band validity is required')
    return band_valid.all(axis=0)&np.isfinite(values).all(axis=0)


def context_validity(values: np.ndarray, band_valid: np.ndarray, nodata: int=-128) -> np.ndarray:
    """Validate the declared source-encoded64-band int8 context; do not convert it."""
    values=np.asarray(values)
    band_valid=np.asarray(band_valid)
    if values.ndim!=3 or values.shape[0]!=64 or values.dtype!=np.int8:
        raise InputContractError('Expected exact int8 source encoding, not GEE float embeddings')
    if band_valid.shape!=values.shape or band_valid.dtype!=np.bool_:
        raise InputContractError('Explicit boolean per-band context validity required')
    return band_valid.all(axis=0)&np.all(values!=nodata,axis=0)


def final_support(current: np.ndarray, context: np.ndarray | None=None) -> np.ndarray:
    """Context never creates current support; return one declared variant's support."""
    current=np.asarray(current)
    if current.ndim!=2 or current.dtype!=np.bool_:
        raise InputContractError('Expected2D boolean current mask')
    if context is None:
        return current.copy()
    context=np.asarray(context)
    if context.shape!=current.shape or context.dtype!=np.bool_:
        raise InputContractError('Context/current support grids differ')
    return current&context


def validate_stats(mean: np.ndarray, std: np.ndarray, expected_bands: int) -> None:
    """Reject invalid checkpoint stats instead of silently repairing the release."""
    mean,std=np.asarray(mean),np.asarray(std)
    if mean.shape!=(expected_bands,) or std.shape!=(expected_bands,):
        raise InputContractError('Checkpoint normalization has wrong band count')
    if not np.isfinite(mean).all() or not np.isfinite(std).all() or np.any(std<=0):
        raise InputContractError('Checkpoint normalization must be finite with positive std')


def validate_output_grid(source: dict, output: dict) -> None:
    """Enforce exact declared grid/CRS preservation; no posthoc alignment to labels."""
    keys=('crs','width','height','transform')
    if any(k not in source or k not in output for k in keys):
        raise InputContractError('Source/output georeferencing fields missing')
    if not source['crs'] or source['width']<=0 or source['height']<=0:
        raise InputContractError('Invalid source grid')
    if any(source[k]!=output[k] for k in keys):
        raise InputContractError('Output grid differs from frozen input grid')
