# Approved architecture: implementation and development evidence readiness

9 October 2026. **Architecture approval and the development-discovery amendment are implemented. The next consequential boundary is authorization of a bounded development reference acquisition pass.** No final validation or detector freeze is ready.

## Completed work

- Recorded the exact owner approval and the approved architecture hash in `AUTHORIZATION_AND_MIGRATION.json`. The October 8 package remains unchanged; its old pending-review status is historical, not the current authorization.
- Implemented role/access, development lineage, blind-packet and native-window checks. Detector-informed/A-B-disagreement discovery is permitted during development, while independently interpreted reference evidence and all resulting artifacts remain permanently development-only. A discovery permission does not authorize an A/B run.
- Separated candidate lock, prediction-processing authorization, reference release and response/join release. This avoids incorrectly requiring final reference release before a custodian can construct the locked map's strata. The helper is not authentication or a global access-control system; it has now been integrated into the two new saved-chip read callers. Legacy acquisition callers/guards were not bypassed or changed.
- Crosschecked all 273 saved complete S1A SAFE identities against two official ASF metadata queries. The270 eligible acquisition instances remain unchanged. Adjacent slices are grouped by spacecraft/absolute orbit, with original products/datatakes retained. Exact UTC and Asia/Makassar dates are explicit.
- Indexed322 saved optical views:76 source items,61 overpasses,171 source supports and23 target dates. No old response or interval was imported into a new support.
- Executed guarded hash/grid/display checks on all 322 saved chips. Their existing valid RGB values reproduce the frozen legacy transform. All 279 offset-metadata conflicts remain unresolved. The per-composite nodata correction changed zero of these RGB views. This qualifies a reproducible **display proxy**, not calibrated reflectance or interpretable/clear support.
- Prepared and inspected a preregistered12-view development first look using saved metadata/QA ranking. It yields potential ordinary/managed-land and observation-quality challenges, but no qualified transition pair or verified artificial dark-confuser contrast. No acquisition-time W/N/O/U response, interval, human reliability result or A/B result was produced.

## Findings that change practical planning

**The old evidence and current SAR products do not line up.** None of the Wave2 pool's target dates matches the existing eight processed SAR dates. This is not permission to reject references or return to the January2018 bottleneck. It means a later useful candidate comparison will probably need a separately costed bounded set of new dates, after reference adequacy is demonstrated.

**Support cannot be relabelled by a filename change.** The new disjoint 30 m tile can shift up to14.142 m from an old centred-neighbourhood response. All saved chips contain the new30 m and50 m footprints, but old intervals cannot be copied to those supports. Registration uncertainty is still unmeasured, and native 20 m SCL repeated at 10 m is not extra information.

**Metadata footprint coverage is approximate.** On January 5, 2017, EarthSearch reports full L1 coverage while ASF's slice polygons leave an approximately 0.4774 km² seam. The date remains included and flagged. The discrepancy is not a measured raster gap; future actual validity determines support/abstention. January 29 remains the explicitly documented historical population exclusion; no new date was silently dropped or added.

**Offset ambiguity is preserved rather than cosmetically solved.** Current provider documentation and historical conversion details do not establish exact-asset calibration for the 279 conflicting views. Apply no speculative −0.1 correction. The 43 unflagged views are also not independently calibrated by this work. A bounded C1 metadata probe found a later example but no items in one tested2018 window; it does not qualify a complete alternative archive or authorize a sensor/source-chain switch.

**Saved clear-looking content is still not a sufficient falsification panel.** The 12 first-look supports cluster on four dates and have substantial offsets. Some views show cloud-like/shadow ambiguity despite favourable SCL ranking. Broad-dark and bounded-feature appearances are discovery leads only. No persistent-water claim, inundation transition, small-water boundary or mining association was manufactured.

## Verification and preservation

The role guard, display contract and catalogue tests have saved passing results. See their individual reports for the exact tests and limits. The saved-pixel integration additionally verified322 identities, grids and complete pre-read scopes; the first-look renderer verified its 12 scopes again before actual access. These checks establish software/provenance behavior, not reference accuracy.

All 108 files in the three historical preservation manifests still match; the two previously approved physical-design files are unchanged. All 18 hashed October 8 architecture files also match. Old exposure incidents, unviewed/unknown provider content, reader originals and conditional intervals remain as recorded. A failed attempt to rerun the old write-once preservation script refused to overwrite its old result; the same check was then run in this new directory. No old artifact was changed.

Two ASF metadata responses and three optical C1 JSON responses total 1,432,012 metered response-body bytes. Documentation web traffic is not included in that body count. New research-imagery transfer, paid spend and Planet quota consumption are zero. Local saved-chip numerical QA took about 22 seconds; all work is complete and no scientific processing job remains in the background.

## Recommended next authorization

Approve the concrete pass in `DEVELOPMENT_EVIDENCE_PLAN.md`: up to24 physical systems/48 date-supports, reusing existing evidence first and allowing bounded public Sentinel-2/Landsat chips where needed; **0.75 GiB incremental imagery and2 GiB new local storage ceilings**, zero paid/Planet quota. These are caps, not promised sample adequacy. Preserve failed proposals and unresolved observations. Reference interpretation remains independent of any selecting detector output; this entire panel stays development-only.

This request is needed because the approved architecture's sections 4 and 10 expressly authorize preparation but exclude automatic research imagery acquisition. The old6 GiB/16 GiB figures were planning scenarios, not active budgets. No new A/B or SAR run is included in this proposed tranche. A later candidate-comparison decision must specify its exact references, detector implementation and selected-date processing cost; final inference still requires a separately locked probability audit.

If new acquisition is deferred, the prepared software and saved discovery leads remain usable. Do not replace that boundary with repeated adjudication of the old conflicts, an invented calibrated optical product, a semantic interpretation of engineering components, or a manufactured independent reader.

## Main files

- `DEVELOPMENT_EVIDENCE_PLAN.md`: concrete workload, source hierarchy, blinding, response and stopping plan.
- `SOURCE_ROLE_REGISTER.json` and `DISCOVERY_LEDGER_TEMPLATE.json`: source roles and permanent development discovery provenance.
- `ROLE_GUARD/ROLE_GUARD_REPORT.md`: role checks, corrected locking order, pre-read scope and limitations.
- `OPTICAL_CONTRACT/OPTICAL_DISPLAY_CONTRACT_FINDINGS.md`: provider evidence, display-only contract and unresolved physical calibration.
- `CATALOGUE_AUDIT/CATALOGUE_AUDIT_REPORT.md`: identity, timing, product-version and footprint findings.
- `EXISTING_DISCOVERY/DISCOVERY_FINDINGS.md`: actual12-view first-look findings, without new reference labels.
- `SAVED_DISPLAY_QA_SUMMARY.json`, `PRESERVATION_CHECK.json` and `APPROVED_ARCHITECTURE_PRESERVATION.json`: actual integration/preservation outcomes.

The curated GitHub backup contains text/code/aggregate findings only. Detailed evidence records, discovery images, original reader returns and sealed material stay local.
