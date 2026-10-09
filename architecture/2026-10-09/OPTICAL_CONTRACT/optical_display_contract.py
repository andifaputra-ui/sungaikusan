"""Pure-array S2 display contract. No I/O, network, classes or response edits.

Legacy Earth Search COGs retain the historical DN*0.0001 visual transform.
The output is a DISPLAY_PROXY, never a claim of calibrated reflectance.
An independently verified raw-DN branch is available for future engineering
tests, but no existing research item has been approved for that branch here.
"""
from dataclasses import dataclass
from typing import Any
import numpy as np


class ContractError(ValueError):
    pass


@dataclass(frozen=True)
class DisplayFrame:
    values: np.ndarray
    valid_by_band: np.ndarray
    source_state: str
    quantitative_allowed: bool
    provenance: dict[str, Any]


def _raw(raw, nodata):
    if isinstance(raw, DisplayFrame):
        raise ContractError('Already transformed frame: reject double application')
    a = np.asarray(raw)
    if a.ndim != 3 or a.shape[0] != 4:
        raise ContractError('Expected four native/resampled DN bands: red green blue nir')
    if not np.isfinite(a).all() or np.any(a < 0) or np.any(a != np.floor(a)):
        raise ContractError('Raw DN must be finite nonnegative integer-valued data')
    if nodata is None or not np.isfinite(nodata):
        raise ContractError('Explicit source-domain nodata is required')
    valid = a != nodata
    return a.astype(np.float64, copy=True), valid


def legacy_display(raw, *, source_collection, source_host, bands, baseline,
                   boa_offset_applied, raw_representation='RAW_COG_DN'):
    """Preserve saved rendering, including a flag instead of guessing offset.

    Caller must supply audited source metadata and verified chip hash/access.
    This routine never upgrades metadata to exact-asset calibration evidence.
    """
    if raw_representation != 'RAW_COG_DN':
        raise ContractError('Expected unscaled cached DN, not an auto-scaled reader')
    if source_collection != 'sentinel-2-l2a' or source_host != 'sentinel-cogs.s3.us-west-2.amazonaws.com':
        raise ContractError('Unsupported route; do not apply legacy transform silently')
    if len(bands) != 4 or not baseline:
        raise ContractError('Four band metadata records and baseline required')
    for b in bands:
        if b.get('scale') != 0.0001 or b.get('nodata') != 0 or 'offset' not in b:
            raise ContractError('Unrecognized legacy scale/nodata/offset contract')
    a, valid = _raw(raw, 0)
    conflict = bool(boa_offset_applied is True and any(b['offset'] != 0 for b in bands))
    values = a * 0.0001
    values[~valid] = np.nan
    return DisplayFrame(values, valid, 'LEGACY_DISPLAY_PROXY', False, {
        'source_collection':source_collection, 'source_host':source_host,
        'processing_baseline':baseline, 'boa_offset_applied':boa_offset_applied,
        'metadata_offset_conflict':conflict,
        'all_source_offsets':[b['offset'] for b in bands],
        'display_formula':'DN * 0.0001; no additive correction',
        'offset_policy':'PRESERVE_HISTORICAL_TRANSFORM_NOT_RESOLVE_PHYSICAL_RADIOMETRY',
        'quantitative_reason':'Exact asset scale/offset and conversion provenance unverified',
    })


def verified_raw_dn(raw, *, nodata, scale, offset, contract_id,
                    exact_asset_verified=False, raw_representation='RAW_UNHARMONIZED_DN',
                    already_applied=False):
    """Future pure arithmetic route, blocked unless exact-asset proof supplied.

    exact_asset_verified is an external engineering assertion, not a provider
    flag or an image-content diagnostic. The caller must retain its proof.
    """
    if raw_representation != 'RAW_UNHARMONIZED_DN' or already_applied is not False:
        raise ContractError('Unknown or already transformed source encoding')
    if exact_asset_verified is not True or not contract_id:
        raise ContractError('Exact-asset transform proof required')
    scale = np.asarray(scale, dtype=float)
    offset = np.asarray(offset, dtype=float)
    if scale.shape != (4,) or offset.shape != (4,) or not np.isfinite(scale).all() or not np.isfinite(offset).all() or np.any(scale <= 0):
        raise ContractError('Finite positive per-band scales and finite offsets required')
    a, valid = _raw(raw, nodata)
    values = a * scale[:, None, None] + offset[:, None, None]
    values[~valid] = np.nan
    return DisplayFrame(values, valid, 'VERIFIED_REFLECTANCE', True, {
        'contract_id':contract_id, 'scale':scale.tolist(), 'offset':offset.tolist(),
        'source_nodata':nodata, 'formula':'DN * scale + offset exactly once',
    })


def render(frame, composite='RGB'):
    """Fixed legacy stretch; 8-bit display only, no auto histogram equalization."""
    if not isinstance(frame, DisplayFrame):
        raise ContractError('Explicit transform state required')
    if composite not in ['RGB','NIR']:
        raise ContractError('Only frozen RGB or NIR composite supported')
    channels, stretch = ([0,1,2],0.3) if composite=='RGB' else ([3,0,1],0.4)
    values=frame.values[channels]
    valid=frame.valid_by_band[channels].all(axis=0)
    # Clip only a display copy; calibrated negative values remain in frame.
    display=np.rint(np.clip(np.nan_to_num(values, nan=0.0)/stretch,0,1)**0.7*255).astype(np.uint8)
    image=np.moveaxis(display,0,-1)
    image[~valid]=[145,145,145]
    return image, {
        'composite':composite,'channels':channels,'stretch':stretch,'gamma':0.7,
        'valid_fraction':float(valid.mean()),'channel_values_below_display_floor':int(np.sum((values < 0) & np.isfinite(values))),
        'channel_values_above_display_ceiling':int(np.sum((values > stretch) & np.isfinite(values))),
        'saturation_interpretation':'Display clipping is not detector saturation',
        'quantitative_allowed':frame.quantitative_allowed,
    }


def scl_evidence(scl, *, baseline):
    """Return independent QA channels. Never emit W/N reference labels."""
    a=np.asarray(scl)
    if a.ndim != 2 or not np.isfinite(a).all() or np.any(a != np.floor(a)) or np.any((a<0)|(a>11)):
        raise ContractError('SCL must retain nearest-neighbour integer categories 0..11')
    if not baseline:
        raise ContractError('Processing baseline needed for SCL2 interpretation')
    try: major=int(str(baseline).split('.')[0])
    except ValueError as exc: raise ContractError('Invalid baseline') from exc
    return {
        'nodata':a==0,'saturated_defective':a==1,'dark_or_cast_shadow':a==2,
        'cloud_shadow':a==3,'unclassified':a==7,'cloud_or_cirrus':np.isin(a,[8,9,10]),
        'snow_ice':a==11,'vegetation_notvegetated_water_algorithm_codes':np.isin(a,[4,5,6]),
        'scl2_semantics':'DARK_FEATURES_SHADOWS' if major<4 else 'CAST_SHADOWS',
        'semantics_policy':'Quality evidence only; no water/nonwater reference assignment',
    }
