# Reference gate failed for detector comparison; useful optical information retained

24 October 2026. **BOUNDED_REFERENCE_INFORMATION_RECOVERED; COMPARISON_ADEQUACY_NOT_DEMONSTRATED.** Acquisition and technical preparation are complete. No background process or candidate inference is scheduled. The frozen S1-only model has not been scientifically falsified or supported by this exercise: reference inadequacy prevents that test.

## What actually completed

All 96 frozen source slots and 24 date-supports remain. Seventy-eight chips were acquired (48 Sentinel-2, 30 Landsat); 18 slots had no fixed metadata opportunity. All 20 unique product identities matched their independent catalogue identities. They comprise 12 Sentinel-2 datatakes and five Landsat satellite/path/day overpasses; adjacent Landsat rows do not become independent acquisitions. These counts still do not establish statistical independence.

All 78 original bodies matched their recorded hashes, fixed 49x49 grid, CRS/affine and expected band count. Original source-window checks and guarded local reads passed. Seventy-seven chips have full RGB/NIR source validity over their entire footprint; one does not. Invalid source support remains separate from cloud/QA and semantics. TIFF band descriptions are absent: order is traced through the frozen ordered request, with QA-range and binary-mask sanity checks; it is not independently certified by self-describing file labels.

Scaling was applied once with source-specific factors. Negative and above-one reflectance values remain in numerical audit records; only fixed display stretches clip. Landsat remains 30 m information after 10 m posting, and S2 QA remains 20 m information. Source scene RMS and Tier2 limitations do not certify local registration. Absolute positional error is unmeasured; +/-20 m scenarios remain assumptions, not a guaranteed error bound.

A metadata-only band-label stop was repaired without changing or redownloading any source. A native Windows rendering crash was retained in a fault-handler log; providing the existing environment's Library/bin through process-local DLL/PATH settings allowed rendering to complete. The exact failing dependency/export was not isolated. No installations or global environment settings changed. The subsequent first render also built its local font cache. Test-fixture and compilation errors were caught and repaired before interpretation. Ten focused offline tests pass across pre-read geometry, QA/radiometry and interval bookkeeping; they do not validate semantic truth.

## Response information and failure modes

All 24 packets were visually screened, with detailed RGB/NIR zoom inspection for interpretable or ambiguous cases. The first reader was this assistant, which knew the auxiliary discovery context but did not inspect current-panel SAR predictions or reuse old reference responses. This is **not** a genuinely independent human reading or proof of blinding to discovery context. Independent interpreter reliability is unmeasured. The separate neutral packet contains no discovery tags, prior responses or SAR predictions.

The explicit first-pass ledger retains:

| Optical disposition | Offered observations |
|---|---:|
| Visibly cloud-obscured neighbourhood | 46 |
| Unresolved/partial/ambiguous surface | 24 |
| Broad visible non-water surface | 5 |
| Shoreline with bounded visible portions and unresolved transition | 3 |
| No fixed source opportunity | 18 |

These are observation counts, not independent samples, physical purity estimates or accuracy labels. Uniform interpreted portions are conditional on the resolved optical representation. Cloud-obscured and unresolved portions always retain possible water. No low-NIR threshold generated any water annotation. A dark patch near cloud remains ambiguous; a seemingly unflagged scene remains questionable on visual inspection. Native QA alone would both miss contamination and fail to resolve dark-land alternatives.

Only 12 acquired views have any nominal 30 m support available and unflagged by the selected QA bits, distributed over eight cases. None is a semantic response merely because of that status. January and December contribute no such nominal unflagged opportunities in this panel. Source quality, support and season are therefore strongly entangled; the sample cannot support a seasonal performance claim.

Temporal outcomes: **19 E0, three E1, two E2, zero E3**. Two cases offer compatible distinct bracketing S2 views: one broad vegetated surface and one shoreline. Those are continuity/position-conditional cases, not unconditional acquisition-time truth. The other visible land and shoreline observations are one-sided and remain target-time UNKNOWN. No local event record, tide evidence or absolute registration measurement was acquired. Small time offset never automatically releases a reference.

## Spatial versus temporal uncertainty

| Fixed support | Optical observations with nominal resolved W >0 | With nominal resolved N >0 | E2 cases with W lower bound >0 across all25 shifts |
|---|---:|---:|---:|
| 10 m sensitivity | 0 | 5 | 0 |
| 30 m primary | 2 | 5 | 0 |
| 50 m sensitivity | 2 | 5 | 0 |

The shoreline contains visible water farther east and land farther west. Its conservative nearshore transition remains unresolved. Under the preregistered +/-20 m scenarios, possible water at the primary support spans **[0,1]**. This is a support failure for a discriminating water reference, despite two compatible optical dates. Do not choose a different support or shift to improve this result. One E2 vegetated case has a more informative conditional non-water interval within the stated optical/continuity/position assumptions. All transient-allowed target-time bounds remain [0,1].

This separates two bottlenecks: clouds and one-sided evidence remove most temporal opportunities; nearshore location and unmeasured registration destroy the remaining putative water contrast. A clear-looking geography tag or a water-looking part of a chip cannot make the frozen central support a water interior. No interpreter agreement statistic can repair missing physical information.

## Practical cost

The acquisition worker ran 15:26:35-15:30:25 UTC, approximately **3m50s**, after prior metadata preparation. Actual image response bodies total **1,410,692 bytes**. Conservative additional charged transfer is **70,254,592 bytes (67 MiB)**, including the 64 MiB metadata reserve; prior smoke charges remain separate. Source/API headers and TLS are excluded. New local artifacts were about 17.3 MB at the initial post-review inventory, far below the additional 1 GiB ceiling; final exact accounting is in COMPLETION_AUDIT.json. Metadata, rendering and interpretation costs are additional and not hidden inside the acquisition runtime. Zero Planet orders, paid spend or new model runs.

## Consequential decision

Keep the detector-comparison gate closed. Do not refit thresholds, process more SAR, replace failed cases, use OPERA as reference truth or infer that the neural candidate has failed. Preserve this panel as a permanent negative reference-feasibility result.

Recommend a **reference-led development amendment**, described in NEXT_REFERENCE_DECISION.md, rather than another automatic rescue of these central supports. The objective is actual observable interiors and difficult physical surfaces with defensible temporal evidence, not sites that merely inherit a map tag. This changes the development-site/date qualification logic and therefore needs a scientific decision. It does not change the final probability-audit requirement or permit a final-method freeze.

Reader source/display definitions were checked against the official [S2 harmonized catalogue](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED), [Landsat C2 L2 catalogue](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T2_L2), and [USGS QA documentation](https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands). Provider labels are diagnostic, not reference truth.
