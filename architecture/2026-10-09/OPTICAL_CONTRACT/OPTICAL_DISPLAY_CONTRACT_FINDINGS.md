# Existing-evidence optical display contract

Date: 2026-10-09 (Asia/Makassar).
Status: `LEGACY_DISPLAY_ROUTE_SPECIFIED_AND_SYNTHETICALLY_TESTED; PHYSICAL_OFFSET_AMBIGUITY_RETAINED`.

## Decision

Use one canonical route for the **already acquired Sentinel-2 evidence**: retain cached unscaled COG DN, render the documented legacy `DN * 0.0001` display proxy, and preserve the per-view radiometry warning. Do not apply `-0.1` to these caches merely because it appears in STAC. Do not relabel the output as verified surface reflectance. Quantitative indices, reflectance differences and radiometric thresholds remain blocked for every exact asset lacking verified conversion provenance.

This is permission to inspect a reproducible optical display with explicit limitations, not a finding that all 279 contradictory metadata cases have been calibrated. No original image, label, conditional interval or response is replaced. The old nine-conflict queue was not reopened. The contract is a prospective development implementation; final reference evidence was not accessed.

## Concrete diagnosis from saved metadata and code

`inspect_saved_metadata.py` opened only selection metadata and acquisition receipts. It reproduced:

|Quantity|Result|
|---|---:|
|Frozen observation slots|538|
|Successfully acquired views|322|
|Acquisition failures|205|
|Pre-read native-window guard nonresponses|11|
|Acquired S2 views / acquired Landsat views|322 / 0|
|Unique acquired S2 item IDs|76|
|Offset-conflict views / unique conflicted items|279 / 62|
|Metadata-consistent pre-offset views / unique items|43 / 14|

All acquired views came from **Earth Search v1 `sentinel-2-l2a` legacy COGs**, hosted at `sentinel-cogs.s3.us-west-2.amazonaws.com`. Planetary Computer was used for Landsat metadata/signing attempts, not these S2 arrays. There is no acquired PC-S2 evidence in this wave to certify or repair.

The 43 unflagged views comprise 36 at baseline 00.01 and seven at 02.14. The 279 flags comprise 30 at 04.00, 137 at 05.00, 33 at 05.09, 17 at 05.10 and 62 at 05.11. Each flagged view records `earthsearch:boa_offset_applied=true` while at least one raster-band offset is nonzero. These are repeat views of 62 source items, not 279 independent calibration failures.

`acquire.py` read raw values with Rasterio, used nearest-neighbour reprojection, and saved float32 arrays of DN values plus SCL. It did not apply reflectance scale/offset. `prepare_review.py` used S2 `DN * 0.0001`, RGB ceiling 0.3, NIR ceiling 0.4, gamma 0.7 and nearest-neighbour display enlargement. The previous nine-view audit established reproduction of its displays, not physical correctness of their reflectance. This new audit does not extend that pixel-level reproduction claim to all 322 views: no research pixels were read here.

## Why the display route is defensible but quantitatively limited

The provider's historical conversion discussion describes COGs with the offset already applied; low values were clamped while original zero nodata was retained. That supports retaining the historic scale-only display when `boa_offset_applied=true`; subtracting again could double-correct. The same discussion later distinguishes a raw-value preview collection. Thus collection/asset identity matters, and there is no universal Earth Search offset rule across versions. [Element84 conversion discussion](https://github.com/Element84/earth-search/discussions/26).

Current provider documentation instructs users to apply nonzero asset offsets and distinguishes legacy v1, C1 v1 and C1-derived v2 collections. It also documents missing items and excludes baseline 05.09 from v2 C1. These instructions conflict with the legacy per-item already-applied flag and historical conversion description in our records. [Element84 current collection documentation](https://github.com/Element84/earth-search/blob/main/docs/collections/sentinel-2-l2a.md).

A provider issue contains reports of incorrect `boa_offset_applied` values and disagreeing original-JP2/COG DN values. It is a warning about reliability, not proof about our exact 62 items. We therefore cannot resolve individual assets by trusting that boolean or by inspecting whether a dark patch "looks like water." [Element84 issue 66](https://github.com/Element84/earth-search/issues/66).

ESA defines conversion of genuine unharmonized L2A DN through the per-band offset and quantification factor, with DN=0 reserved for no data. That is distinct from deciding whether a mirror has already transformed its stored values. Preserve negative valid reflectance when a verified raw-DN route eventually is used; clip only its display copy. [Copernicus L2A data-quality report, radiometric offset](https://sentiwiki.copernicus.eu/__attachments/1673423/OMPC.CS.DQR.002.07-2024%20-%20MSI%20L2A%20DQR%20August%202024%20-%2076.0.pdf).

## Prospective interpretation eligibility

|Existing evidence|Permitted role|Remaining limitation|
|---|---|---|
|43 unflagged pre-offset views|Optical visual review using the frozen display, subject to ordinary QA, registration, support and time checks|Metadata-consistent does not mean independently calibrated; no quantitative promotion from this audit|
|279 flagged views|**Conditional visual/context review**, with warning exposed to reader|An assertion requiring physically calibrated darkness, colour ratios or cross-date brightness is unsupported; flags remain unchanged|
|Any view with cloud, shadow, clipping, ambiguous texture, mixture or positional uncertainty|Record observable portions and unresolved portions separately|A display/calibration permission is not an acquisition-time eligibility decision|
|All unavailable slots|Retain technical nonresponse/UNKNOWN as recorded|No replacement or synthetic evidence|

The 279 flagged views are not automatically useless. Shapes, boundaries and spatial relationships may remain visually informative. But darkness alone cannot establish water, and a uniform reflectance offset affects display brightness and band ratios. The reader must record whether the claim depends on the uncertain radiometry; if it does, that portion remains unresolved without independent corroboration. This audit supplies **no numeric tolerance** for promoting conditional content and computes no new response yield.

No image-content-dependent choice between applying and ignoring the offset is allowed. No alternative rendering may be chosen because it produces a preferred class. An optional diagnostic rendering would need separate preregistration and must not silently replace this canonical view.

## Executable contract and safeguards

`optical_display_contract.py` is a pure-array module: no filesystem reads, downloads, source selection or reference labels. Its implemented rules are:

1. Require the exact legacy collection/host, baseline, all four band metadata records and explicit raw-DN representation. Reject unknown provider/scale/nodata and already-transformed inputs.
2. Preserve raw-source nodata before transformation. A valid DN=1 remains valid; it can represent a provider-clamped low signal and is not automatically nodata or water.
3. Apply scale-only display once. Emit `LEGACY_DISPLAY_PROXY`, `quantitative_allowed=false`, the original offsets and the unresolved flag. A separate quantitative function rejects use without an externally verified exact-asset contract; **no research asset was assigned such a contract here**.
4. RGB validity uses red/green/blue; NIR-composite validity uses NIR/red/green. The old packet code greyed all composites if **any** RGB+NIR band was zero. That can hide a valid RGB view when only NIR is missing. This is a prospective correction only; whether any old view was affected was not tested and is not asserted.
5. Retain SCL as a separate categorical QA array. No interpolation to fractional classes; resampling must remain nearest neighbour. SCL 0/1, shadow, cloud/cirrus, unclassified and snow remain distinct; SCL 6 is not reference truth. SCL is native 20 m, so duplicating it on the 10 m indexing grid adds no physical information. SCL 2 semantics depend on processing baseline; 7 is unclassified, not automatically cloud. [Copernicus scene-classification documentation](https://sentiwiki.copernicus.eu/web/s2-processing).
6. Clip only the rendered copy, log display clipping, and preserve the underlying valid values. A white display is not proof of sensor saturation. No automatic W/N/O/U assignment is implemented.

**22 synthetic tests passed**, including double offset, double transform, unproved quantitative use, raw nodata versus negative valid reflectance, DN=1 retention, per-band masks, clipping versus saturation, SCL7, SCL2 baseline semantics and categorical interpolation rejection. These test software behavior, not provider asset equivalence or visual interpretation reliability.

Caller requirements before real use: verify original cached-chip hashes; enforce the approved role/access contract; retain native resolution/transform, source item/datake/baseline and resampling provenance; log which view version a reader saw. The module does not replace spatial-access checks or registration/support analysis. This work does not call or modify the old geographic firewall.

## Bounded fallback metadata assessment — not adoption

Three fixed JSON-only requests checked Earth Search v1 `sentinel-2-c1-l2a`: collection metadata plus two small Kusan time windows, **30,652 response bytes** in total. No asset, thumbnail, preview, TIFF header or image pixel was requested. Receipt files preserve the exact requests and response hashes.

- The 2018-09-07 through 2018-09-12 window returned no items. This is only that bounded query's result, not a statement that all 2018 C1 coverage is absent.
- The 2025-09-18 through 2025-09-23 query returned a metadata example, `S2C_T50MLA_20250921T024625_L2A`, with baseline 05.11, scale 0.0001, offset -0.1, zero nodata, 10 m RGB/NIR and 20 m SCL, plus per-asset checksum/size. It was a limit-one endpoint test, not an evidence ranking or scene selection.

C1 offers a cleaner candidate encoding route, but exact payload equivalence was not verified and coverage cannot be assumed. **It remains deferred fallback design only**; no source-chain switch or download is authorized by this audit. Original JP2 asset links are present in legacy metadata, but their requester-pays status/access and cost have not been exercised; do not silently use them as a free fallback.

## Files and continuation

- `SAVED_METADATA_AUDIT.json`: aggregate counts, unique item metadata, selection hash and receipt hashes; no interpretation.
- `optical_display_contract.py`: canonical legacy display proxy plus a closed quantitative gate.
- `SYNTHETIC_TEST_RESULTS.json`: 22/22 passing synthetic checks.
- `metadata_receipts/`: three bounded C1 JSON responses and request receipt summary.

Continue prospectively within development by using the declared display state and recording source uncertainty alongside optical-time state, support and temporal-transfer evidence. Preserve old responses unchanged. Metadata uncertainty should not blanket-discard every visual observation, but it must not be converted into quantitative calibration or confident semantics by convenience. No A/B, SAR processing, sample draw, paid order or final evidence access occurred.

## Subsequent saved-chip integration by the parent task

After this metadata/synthetic audit, the parent integrated the role guard and this display module into `../audit_saved_display.py`. All322 cached PASS chip hashes/grids and valid RGB transforms passed;279 flags were retained. The composite-specific mask changed zero RGB pixels in this pool. See `../SAVED_DISPLAY_QA_SUMMARY.json` and its detailed receipts. This verifies reproducibility, not exact-asset physical calibration. A separate12-view development first look was subsequently rendered and inspected; no old response, numeric reference interval or acquisition-time class was changed.
