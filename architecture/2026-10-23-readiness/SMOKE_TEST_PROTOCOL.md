# Proposed one-scene technical smoke test

Prepared23October2026; not executed. This protocol qualifies a runnable imported S1-only pipeline, not a classifier's scientific validity.

## Frozen inputs and purpose

- Model: matched S1-only control `s1_only_k0_seed42`, Hugging Face repository `rohitm9/surfaceWaterGlobal`, immutable revision `7c497187a9b7f53488e6577621e7d0961c23dcfd`. Require the exact checkpoint/normalization hashes in `FROZEN_ARTIFACT_CONTRACT.json`.
- Source: `COPERNICUS/S1_GRD/S1A_IW_GRDH_1SDV_20240901T220029_20240901T220054_055477_06C49D_489D`. Use this explicit scene; do not reconstruct from a calendar date by automatically mosaicking every same-day scene.
- Date selection: earliest UTC date in the saved OPERA/legacy acquisition-catalogue intersection. Geometry: a central512×512 window on the existing10m C1 indexing lattice. Both were frozen before image/prediction inspection. This is a purposive engineering case, not a validation sample.
- Output grid: EPSG32750, affine `[10,0,368031.7721720397,0,-10,9613405.8651008]`,512columns×512rows. Preserve geometry, native source provenance and per-band masks. No old reference response is copied to this patch.
- Inputs: current VV and VH sigma0 dB plus provider angle, in that order, following the published native-source contract. Native GEE products are a distinct experimental processing branch; no numerical equivalence with local SNAP products is claimed. No local dB floor repair or custom calibration is added.

## Reversible setup and resource envelope

1. Use a separate E:-resident CPU inference environment and caches. Preserve `kusan-c1`, SNAP and existing QGIS. Resolve compatible dependency versions from the frozen release's requirements and save the exact lock before inference; do not globally upgrade packages.
2. Cap cumulative transfer for packages, model/normalization and the single input at2GiB; cap new environment/cache/output storage at6GiB. Meter partial/failed transfers conservatively, retain receipts and do not reset on retry. Zero paid spend and Planet quota. These are proposed limits pending authorization, not a download already started.
3. Download only the S1-only checkpoint and its stats. Validate bytes/digests before loading. Use the exact release trainer for architecture construction, strict state loading, CPU, batch1, float32 and the declared four-flip inference. The inspected builder disables pretrained-backbone downloads; no training routine runs.
4. Extract only the declared source bands/geometry with source projection and resampling provenance. Register development-only role and authorized read scope including actual source rounding/halo before any pixel transfer. Use the prior role/native-window safeguard where applicable; do not infer safety from an output crop alone. Provider-side GEE extraction must record exact scene, requested grid/extent/masks and the limitations of source-read observability.
5. Set process-local GDAL_DATA and PROJ_DATA to the existing `kusan-c1/Library/share/gdal` and `.../proj` resources as appropriate to the chosen runtime. Put temporary files and framework caches onE:; no global configuration changes.

## Execution and verification

- Validate source identity, band order/units, CRS/affine/shape, all-band source masks and finite values. Normalization must have3 finite means and strictly positive finite standard deviations, with the exact released file hash. Any mismatch stops; no substitution chosen for attractive output.
- Require VV/VH/angle jointly valid for current support. Keep missing-current reasons. A source-valid pixel is not automatically physically reliable; preserve range/floor diagnostics without introducing a new censoring rule.
- Run one512×512 inference with the frozen model. Record wall time, actual peak resource behavior if available from the process, output shape and finite-score range. Use float probability output with a distinct nodata sentinel and a separate support mask. No semantic water layer, accuracy estimate or reference adjudication is released.
- Verify exact output grid preservation, probabilities within[0,1] on supported cells and nodata on unsupported cells. Check the output/source overlay at two scales when actual imagery is authorized; display scores as unvalidated engineering output.
- If one inference fails or reaches30minutes, checkpoint the cause and stop the bounded attempt. Do not launch an automatic model/threshold search. A slow but progressing setup or download may continue in the background within the resource ceiling, with a saved resumable state rather than repeated monitoring.
- Do not modify the published weights, fit a scaler locally, fine-tune, create training labels, load final reference evidence or process additional SAR dates. All generated evidence remains permanently development-only.

## Interpretation and next boundary

Passing means that the explicit source/model combination produces auditable, correctly located, support-aware output within measured resources. It does not mean the output is correct water, a calibrated probability, superior to OPERA, or valid for2017–2025.

After a pass, specify/execute only the already reviewed linked development comparison when its input/evidence acquisition is authorized. The fused arm remains pending exact source-encoded AEF access; the current-only smoke does not qualify that input. Never let an easy engineering case replace the difficult-water/land and genuine-transition reference cases that determine scientific usefulness.
