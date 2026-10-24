# Approved single-scene native-model smoke — 24 October 2026

The user explicitly approved the bounded technical smoke test in this conversation. `AUTHORIZATION.json` records the scope. This authorization replaces the pending-execution state of the 23 October readiness checkpoint; it does not authorize model adoption or a scientific comparison.

One frozen 512 by 512 patch, one explicit 1 September 2024 Sentinel-1 image, one released S1-only checkpoint, CPU batch one and four-flip mean-logit inference. Separate runtime: `E:/Bendungan_Kusan/Model_Runtime/s1_smoke_cpu_20261024`. Scientific Python, SNAP/C1 products, reference responses and final evidence remain unchanged. No fitting, water map, class threshold, accuracy claim, new reference sample, annual-context arm or full-series processing.

## Reproducibility and resource controls

- Torch 2.8.0 CPU and torchvision 0.23.0 are a documented upstream pair. Model source, release trainer and checkpoint/statistic identities remain pinned to the 23 October package. Remaining packages are resolved from explicit roots, downloaded as wheels, hashed, installed offline and locked before inference. No global upgrade.
- The shared transfer ledger reserves response-body blocks before pip or artifact reads. Failed/partial reservations are not reset. An 8 MiB conservative reserve covers unmetered small metadata/API responses; headers/TLS overhead is excluded. This is explicitly different from measuring every network interface byte. Package/input/model transfer stops at the approved 2 GiB ledger ceiling.
- Installation is checked against 6 GiB using existing files, wheel uncompressed lengths and 512 MiB headroom for model/output artifacts. Actual runtime storage is checked afterward. No paid or Planet use.
- Frozen output geometry is unchanged. Planned native source windows include outward rounding and a one-source-pixel halo, including the coarse rotated angle grid. The physical engineering scope is frozen before source metadata queries. Policy checks occur before `getDownloadURL` and pixel reads. Provider-internal cached tile reads remain unobservable and are not falsely claimed as a fully audited provider IO trace.
- Three source masks accompany VV/VH/angle. Their conjunction and finite-value support are authoritative for the model input. Missing locations are filled with the released means for convolution, but remain nodata in output scores.

## Important interpretation limit

Convolution can transmit the effect of missing/filled context to nearby supported pixels. A continuous distance-to-invalid-or-edge diagnostic is retained without introducing a tuned reliability mask. Valid support is not a guarantee of local physical reliability. The test cannot establish accuracy, calibration, reference adequacy, unseen-geography generalization or equivalence to accepted SNAP/C1 products.

## Background controller and stopping

`prepare_runtime.py` is the isolated setup job. `continue_after_setup.py` waits for its success/failure marker, then makes one bounded input request and one inference attempt. It records `STATUS.json`, logs and `SMOKE_RESULT.json` on success. Inference has a 30-minute subprocess limit. Setup failure, a cap, an input/contract failure or an inference failure stops the chain without automatic retry or method switching. No work follows the result.

Two-scale visual/georegistration QA is still required after outputs exist; exact affine equality alone is not an independent geographic accuracy test. Do not interpret the result or start another arm automatically when returning later.

Sources checked 24 October 2026: [official PyTorch version pairs](https://pytorch.org/get-started/previous-versions/) and [Earth Engine download grid semantics](https://developers.google.com/earth-engine/apidocs/ee-image-getdownloadurl). The model-specific contract remains the pinned source in the readiness package.
