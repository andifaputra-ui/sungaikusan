# Optical information recovered; the May11 timing gate still fails

25 October2026. **OPTICAL_TIME_WATER_AND_ARTIFICIAL_LAND_RECOVERED; MAY11_ACQUISITION_TIME_ADEQUACY_NOT_DEMONSTRATED.** All four authorized reference chips were acquired, checked and interpreted. No source/date/site was substituted, no model was run and no comparison or final-method decision is released. No process remains running.

## Scientific finding

We now have a spatially defensible optical-time water interior in the inland basin and a dated artificial/non-water surface at the runway. Both retain their interpreted optical portions across30m primary,10/50m sensitivities and all25 fixed position scenarios. This is an improvement over geographic tags and mixed central supports; it is not acquisition-time validation of11May2025.

| Site and source | Actual optical response | Temporal implication for11May22:00UTC |
|---|---|---|
| Basin,S2 on14May02:48UTC | Visible bounded open water; primary neighbourhood clear and unflagged by selected QA. Basin function and chemistry unknown. | After-date evidence only; about52.8h offset does not authorize transfer. |
| Basin,Landsat9 on11May02:28UTC | Cloud/haze/shadow/coarse support prevents defensible central fractions. Source pixels valid, surface unresolved. | Before-date observation exists but cannot supply the missing surface state. |
| Runway,S2 on11May02:39UTC | Central neighbourhood visibly cloud-obscured despite valid source pixels. | No before-date non-water truth beneath cloud. |
| Runway,S2 on13May02:39UTC | Visible transport/runway-like strip and adjacent vegetated land; optical non-water interpretation.90m neighbourhood is not pure asphalt. | After-date evidence only; about28.6h offset does not rule out transient water at target. |

The two new cases are **E1**, with target-time transfer UNKNOWN and possible water[0,1] for every support representation. A durable runway is not proof it was never inundated; a bounded basin is not proof of its operating level, retention time or uninterrupted water state. No local rainfall, flood, tide, basin-operation or other event bridge was acquired. No claim is made that an event occurred or that it did not occur.

Optical W/N/O/U proportions remain interpretations at native information support, not exact physical subpixel fractions. Landsat's30m data do not become independent10m measurements by posting. Absolute registration remains unmeasured;25shifts are sensitivity scenarios only. Independent interpreter reliability remains unmeasured. The assistant knew geographic discovery context but did not inspect current-panel SAR predictions or rewrite prior responses.

The earlier coastal-water and ordinary-land controls remain E2conditional controls, with all transient-allowed bounds still[0,1]. Coastal controls cannot substitute for inland flood evidence or justify an OPERA accuracy penalty for an ocean-policy mask. Thus the complete four-site branch still cannot select a thesis detector or support a paired May11 accuracy claim. The frozen model has neither passed nor failed a semantic test here.

## Source-quality and provenance results

All four bodies passed fixed grid, CRS/affine, band-count, source validity/QA encoding and guarded local-read checks;21source-band window checks passed before downloads. TIFF band descriptions remain absent: order is traced to the frozen request and checked structurally, not independently certified by file labels. Radiometry is source-specific and applied once; QA remains diagnostic, never W/N truth. Provider-internal tile/cache IO is unobservable and not certified by these planned-window checks.

The initial execution stopped **before any pixel request** because Sentinel-2's recorded ingestion-version field had advanced since the previous batch. Metadata-only diagnosis found all other returned metadata identical for the three authorized S2products: IDs, acquisition/processing properties, bands, grids and footprints were unchanged. Landsat's version was unchanged. The [official GEE guide](https://developers.google.com/earth-engine/guides/image_info) distinguishes ingestion version from observation time. That does not establish unchanged pixels or explain the provider update.

The operational correction froze the current revisions as the source manifest for these newly authorized reads, retaining the earlier snapshot and stopped attempt. No product/date/geometry/radiometry/role changed. The current versions were checked again before first pixel access. This was not a retry or replacement of an already-read failed image body, and no old reference was overwritten. Historical pixel equivalence is not assumed. Full original/live metadata and the explicit refresh decision remain local.

## Local encoding diagnostic

Before decoding the new basin arrays, two fixed engineering hypotheses were registered: legacyDN*1e-4 versus legacyDN*1e-4-0.1, each compared with the harmonized GEE export. There was no fitted offset or class-dependent choice.

The two saved grids have **1,400 exactly overlapping sample centres**. Across four RGB/NIR bands, all **5,600 jointly valid values matched exactly at zeroDN difference**. None differed by1000DN. The no-extra-offset comparison had zero discrepancy; applying another-0.1 would introduce that discrepancy. This strongly supports the already-offset-adjusted encoding relationship **for the tested overlap**.

It does not prove absolute reflectance calibration, unchanged pixels throughout the provider revision, or correctness of every legacy item. The original full ESA generation URI was not independently re-established in this diagnostic; nominal STACitem/date/baseline and sample alignment are recorded. No global322-view contract or historical response was upgraded. The old and new basin views are the same nominal optical acquisition, not independent temporal observations or two class votes.

## Resources and tests

New image response bodies total **92,250bytes**. Conservative additional charge was **2MiB**, bringing the existing cumulative reference charge to **69MiB**, below both the authorized4MiB increment and retained1GiB ceiling. The worker's successful four-window pass took about19seconds, excluding provenance diagnosis and local QA. No Planet/paid order, new SAR scene processing, model inference or source raster modification. Parent and new artifacts remain within the unchanged1GiB aggregate storage ceiling; exact totals are in COMPLETION_AUDIT.json.

Four new focused tests pass: bounded-body success, exact-limit rejection without over-read, oversized declaration before body access, and unchanged non-version metadata plus acquisition accounting. They test execution/provenance contracts, not reference semantics. Earlier branch/support tests remain separate. A missing-space compilation error in the new renderer was corrected before execution; source data were not affected. All original nomination, source-plan and response locks remain preserved; this new return is separately locked.

## Next consequential decision

Do **not** automatically acquire more optical images for the frozen May11cases or launch their detector comparison. The four-chip attempt has identified the bottleneck specifically: useful optical states exist on13/14May, while the previously frozen May11 target acquisition remains poorly evidenced.

Recommend the next bounded step be **metadata-only reference-date/SAR co-registration feasibility**, starting from the actual clear optical dates13May(runway) and14May(basin), rather than another May11site rescue. Keep the same frozen objects, source roles and independent optical interpretations. Determine whether an available S1acquisition—and operational OPERA where genuinely contemporaneous—can be paired with those references using object-specific timing/geometry/event evidence. Do not treat same-day or any fixed hour tolerance as truth. No new SAR pixels, optical order, date substitution, threshold or method change is authorized by this recommendation.

This is a development temporal-allocation decision, not a revision of the scientific target or permission for full-series work. If only incompatible tracks, weak timing bridges or unrepresentative controls are available, preserve that result; do not loosen semantics to manufacture agreement. The strongest objection is that following clear optical dates selects fair-weather/easy development cases and may never test flood transitions. Such a branch can at most qualify narrow falsification cases; a separately sealed probability reference audit across the reconstruction remains necessary. No final detector or method freeze follows from a convenient matched pair.
