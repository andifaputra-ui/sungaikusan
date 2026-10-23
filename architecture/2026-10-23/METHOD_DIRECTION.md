# Method reassessment and recommended pivot

23 October 2026. Requested by the owner after expressing concern about continuing an unpromising approach. This assessment reopens the detector choice; it does not execute a new detector, training run, research-image acquisition or final validation.

**Recommendation: stop treating the handcrafted VV split/consistency architecture as the leading method. Move toward a small, reference-anchored comparison of an established surface-water product, a frozen learned Sentinel-1 model, and its matched spatial-context variant. Choose the eventual method by its ability to survive Kusan counterexamples.** The thesis contribution can be a defensible reconstruction and environmental analysis; it need not be an invented threshold algorithm.

## Why change direction

The engineering is reusable, but engineering completion is not evidence that a detector will work. The runway counterexample shows a real weakness in the scalar-VV family; same-signal shape and consistency do not repair it. Independent references remain difficult. These are separate problems and need simultaneous attention.

Three overgeneralizations must be avoided:

- The Phase2.3 results do not prove that every multivariate or learned SAR model fails. Local texture/polarization overlaps are counterexamples to simple rules, not a theorem against learned discrimination.
- The temporal pilot had eight sparse dates, seven objects and inadequate class evidence. It did not establish that temporal information is sufficient, and it did not establish that all temporal architectures are useless.
- Failure to validate the current detector is not a negative result about the broader possibility of reconstructing Kusan open water.

Local evidence: `C2_3_INFORMATIVE_TILE_EXPERIMENT/reports/C2_3_SCIENTIFIC_REPORT.md`, `DESCRIPTIVE_TEMPORAL_PILOT/FINDINGS_AND_DECISION.md`, and `DEVELOPMENT_IMPLEMENTATION_20261009/IMPLEMENTATION_FINDINGS.md`. No original response or historical scientific output was changed.

## What is newly concrete

**An operational comparator is actually indexed over Kusan.** A metadata-only Earth Engine query found185 OPERA DSWx-S1 records on78 UTC dates intersecting the L1 geographic envelope between27 August2024 and25 December2025. Forty-one dates intersect the approved legacy catalogue's UTC-day list. All queried products report descending pass and version1.0, across MGRS tiles50MLA/50MLB. These are opportunities, not185 independent acquisitions, full-L1 pixel support, exact S1-source matches or accuracy observations. See `AVAILABILITY_SUMMARY.json` and saved query/receipts.

OPERA's published product has30m posting and a broader water taxonomy: use its open-water class rather than its binary union with inundated vegetation. Its nominal large-water performance target and masks make small basins and new urban water important stress tests. Its accessible record does not itself cover the entire2017–2025 thesis period. [Official catalogue](https://developers.google.com/earth-engine/datasets/catalog/OPERA_DSWX_L3_V1_S1).

**A matched learned comparison is available in public source.** Mukherjee etal.'s October2026 preprint separates current S1 from annual spatial context and reports gains on external reference scenes. It is promising external evidence, not a Kusan result. The authors acknowledge weak-label errors, geographic overlap and limitations for flood inundation and narrow channels. [Full text](https://arxiv.org/html/2610.06704v1).

The repository publishes matched S1-only and S1+AEF checkpoints, normalization files, hashes and a CPU inference option. Its version history includes superseded weights and trainer changes, so pinning the exact release is essential. Inputs are VV/VH/angle and, for the context variant, the source-encoded annual embedding. [Repository](https://github.com/Rohit18/surfaceWaterMappingGlobal). `MODEL_RELEASE_AUDIT.json` records the examined source identities and release declarations; no weights were fetched.

**Annual context exists in the live catalogue, but compatibility is not established.** A second metadata-only query returned one intersecting AEF image for every year2017–2025. The browsed catalogue page still describes2017–2024. This live/static discrepancy is recorded, not silently reconciled. Live metadata reports mixed dataset versions1.0/1.1 and a floating-point band type; the candidate expects a specific SourceCooperative int8 representation. No interchangeability is assumed. [Official embedding documentation](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL).

## Alternatives compared

| Direction | Scientific attraction | Principal risk | Recommendation |
|---|---|---|---|
| More scalar VV thresholds, components or morphology | Cheap; established local engineering | Does not add the information needed for smooth dark land; another rescue cycle | Retain a weak engineering control; stop making it the lead |
| OPERA/DSWx-S1 as released | Established contextual system; actual2024–2025 catalogue opportunities | Different radiometry/support, masks, minimum-feature limitations and incomplete historical record | Preferred operational comparator; never reference truth |
| Frozen learned S1-only water model | Uses richer current spatial/polarization information without annual context | Domain shift, training-label biases, native preprocessing requirements | Essential learned control |
| Matched frozen S1 plus annual embedding | Tests whether learned context resolves otherwise ambiguous current observations | Static context can dominate new/receding water; retrospective and encoding issues | Most promising experimental challenger, conditional on interface qualification |
| GFM observed-water/likelihood products | Mature independent implementation family; historical archive described in literature | Flood anomaly is not total open water; product availability/access still unverified locally | Reserve comparator if OPERA fails access or coverage, using the correct water layer |
| Microsoft AI4G flood-change model | Public model/code and historical work | Change-focused target and RTC/pre-event inputs do not match persistent-water reconstruction | Defer as a possible event branch, not the main water detector |
| New locally trained deep model | Maximum local flexibility | Current labels, compute and validation are insufficient; high risk of teaching source errors | Do not start training from scratch |
| L-band, coherence or broad optical fusion | Could add different physical information | New processing/data chains; cannot solve missing contemporaneous reference by themselves | Keep as escalation options rather than default stack expansion |

The GFM paper describes an ensemble, reference-water logic and historical processing; that makes it a serious alternative without making its outputs independent truth. [Wagner etal.,2025](https://elib.dlr.de/218412/). The Microsoft model explicitly uses change information and source-specific RTC inputs. [Paper](https://arxiv.org/html/2411.01411v3), [implementation](https://github.com/microsoft/ai4g-flood). DLR SWIM is another credible candidate family, but its public service currently describes developmental validation, so catalogue presence cannot certify readiness. [DLR service](https://b.geoservice.dlr.de/web/datasets/swim).

## The next experiment should answer a decision

Proposed primary question: **Can a richer, frozen current-observation model resolve Kusan open water versus difficult land, and does annual context improve that ability without suppressing genuinely new water?** Do not ask whether another score or image looks smoother.

Start with the overlap period in late2024, where OPERA and known annual context are available. Dates are chosen from independent optical/reference opportunity and physical challenge coverage, not from favourable model performance. Contemporary success is a feasibility test; it does not validate2017 or all seasons. Later include an earlier-period transfer check before making a decade-wide claim.

Use three primary arms: OPERA, frozen S1-only, matched frozen S1+AEF. Keep old VV A/B as a secondary engineering control only if it can be run on exactly the same observations with an unchanged, documented estimator. Do not quietly reuse2018 thresholds on2024 inputs. No local fine-tuning in this first comparison.

Plan a small development panel of approximately12 physical systems, up to24 date-supports. Seek persistent water, a genuine independently observed transition, ordinary land, independently identifiable artificial/smooth land, small/mixed boundaries and poor support. These are workload/diversity goals, not representativeness or statistical-adequacy cutoffs. Include repeated dates on unchanged geometry so context cannot win by simply reproducing annual water patterns. Record missing challenge families explicitly. Existing development-only adversarial discovery remains allowed, with its selecting output kept out of interpretation packets.

The reference and model programmes should be linked at the same date/support rather than accumulating another unconnected random optical collection. A reference may be incomplete and still bound an error; the comparison must report when those bounds cannot distinguish methods. A visually persuasive output without independent state information remains a diagnostic.

## Input compatibility and response safeguards that matter

1. Use the released model's native input contract in a separately versioned experimental branch. Preserve the accepted SNAP products as the historical control. A candidate does not have to be pixel-identical to the old implementation to be scientifically legitimate; it must have defensible preprocessing and be evaluated as the pipeline actually used. Neither raw GEE assets nor any sigma0 image is automatically interchangeable with its training input.
2. Resolve current VH floor/support validity before using the existing local VH. Phase2.3 found extreme values and neighbourhood overlap; adding a ratio blindly is not progress. Source-native valid processing is an alternative to repairing an opaque local dB value. No source product is overwritten.
3. For embeddings, verify model version, basis, encoding, band order and normalization. Native int8 inputs cannot be replaced by GEE floats merely because both have64 bands. Preserve the dataset year/version and disclose annual future observations. Use the matched S1-only arm to isolate the value of context.
4. Keep probabilities as scores until calibration is demonstrated. Predeclare the publisher's operating point and any fixed sensitivity, instead of tuning to Kusan review answers. A shared numerical threshold across different algorithms is not automatically a fair comparison.
5. Keep30m primary reference supports and native source geometry. Use area overlap for different map grids; do not manufacture10m OPERA detail or interpret mean model probability as water area. Maintain10/50m sensitivity and separate registration uncertainty.
6. Independent optical evidence supplies W/N/O/U portions and time-transfer qualifications. OPERA, DW, embeddings, GFM and learned predictions are candidate inputs/outputs or diagnostics, never their own reference. If an optical source is later used for training, its role change is explicit and final validation uses separate evidence.
7. Preserve final probability sampling, sealed reference responses, genuine human reliability assessment and exposure reporting. All discovery and this comparison remain development-only; repeated favourable testing cannot become final accuracy.

## Positive signals, negative signals and exit decisions

A positive development signal is repeatable improvement on independently supported hard cases, with useful coverage and persistent/new-water retention. A gain confined to historical water, a polished map, agreement among SAR algorithms or reduced output through masking is insufficient.

Freeze the response and candidate settings before joining results. Report interval error bounds, mapped water, abstention/unavailable support, physical-context failures, repeated-date behavior and practical cost. The difference between methods must exceed or remain distinguishable within the relevant reference uncertainty; there is no honest universal success percentage to invent now.

- If the context model resolves ordinary and difficult land while retaining independently observed new water, advance it to a separate probability-evaluation plan.
- If S1-only performs as well or better, drop the embedding dependency and prefer the simpler model.
- If OPERA is best, use/adapt the established method rather than invent novelty; historical processing and target limitations still need a bounded test.
- If all fail on well-observed cases, change the information source or prospectively narrow the claim with explicit scientific approval. Do not keep tweaking the same low-intensity rule.
- If references cannot distinguish any method, stop calling it a detector contest. The next decision concerns evidence or the achievable historical claim, not a larger model search.

## What this assessment authorizes and recommends

The owner's current instruction authorized a creative reassessment and routine research/metadata checks. It did not explicitly authorize weights/environment downloads, new research pixels, semantic inference, a changed radiometry chain or final validation release; none occurred. The October9 generic0.75GiB development acquisition proposal is now an alternative under reconsideration, not the automatic next job.

**The consequential choice now is whether to adopt this stronger comparator-first direction and qualify one native-model input/inference example before committing to any broader batch.** That first technical example should establish exact artifact identity, input compatibility, CPU feasibility and correct output support; it is not a validation result. Then acquire only the linked development evidence needed to test the three arms. Do not use another large preparation programme as a substitute for that small decisive comparison.

The strongest objection to my recommendation is that it can exchange a transparent weak method for an opaque, externally trained model whose annual context encodes the answer and whose training geography overlaps Kusan. That is why release pinning, training-geography disclosure, matched current-only controls and real repeated-date reference transitions are central to the proposal. If those cannot be established, prefer the operational comparator or retain the inability to validate the reconstruction.

## Status of the hypothesis and progress estimates

There is no requirement that results support the original hypothesis. The prior completion percentages were rough planning judgments and are unsuitable as a go/no-go test. The useful new signal is that stronger, executable alternatives and local catalogue opportunities exist. Their Kusan accuracy and historical validity remain unknown.
