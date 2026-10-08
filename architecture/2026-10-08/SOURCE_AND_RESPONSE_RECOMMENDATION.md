# Independent source and reference-response recommendation

Prepared 8 October 2026 for the major architecture redesign. This is an independently reasoned contribution to the architecture-freeze package, not authorization to acquire sources, draw samples, inspect pixels, process SAR or evaluate detectors. Only saved designs, aggregate qualification summaries, existing metadata summaries and primary-source publications/provider documentation were examined. Individual response labels, research imagery, browser map catalogues and final reference evidence were not opened.

## Recommendation

Separate three tasks that the legacy architecture tried to solve with one increasingly elaborate physical-context frame:

1. **Detector falsification in development:** a deliberately enriched, evidence-first challenge panel, selected without inspecting detector predictions or current VV. It should seek physically informative counterexamples, not estimate landscape prevalence or final accuracy.
2. **Reference feasibility:** qualify the observation and temporal-transfer protocol on that development evidence, record failures and quantify cost. A probability qualification subsample is useful if population response yield is a decision target, but is not a necessary prerequisite for every development comparison.
3. **Final inference:** an exhaustive date-by-location base frame, a separately sealed probability draw after the detector/protocol are fixed, and design-consistent estimates or bounds. Optional frozen auxiliaries improve efficiency; their complete thematic truth, common publisher and complete physical-parent ontology are not prerequisites for frame validity.

The preferred final sampling architecture is therefore a **geometry/date base frame with a small auxiliary enrichment**, not RBI-only or GlobeLand30-only. Keep an explicit ordinary/residual/missing-auxiliary component with positive probability. No source may silently turn an optical-time state into an acquisition-time state. Reference inadequacy, not missing official boundaries, remains the critical scientific problem.

This recommendation changes what development selection claims: the challenge panel is purposive and cannot provide unbiased whole-domain accuracy. That loss is acceptable only because the final probability sample performs a different job and remains isolated.

## 1. What the acquired evidence actually establishes

The saved, completed metadata census contains 270 eligible catalogued S1 dates, 3,333 Sentinel-2 items representing 1,210 overpasses, and 876 Landsat items representing 447 overpasses. Adjacent tiles and processing versions are not independent observations.

| Metadata opportunity over the old domain envelope | Sentinel-2 | Landsat | Combined |
|---|---:|---:|---:|
| At least one observation within 24 hours | 194/270 | 138/270 | 230/270 (85.2%) |
| Within 72 hours | 257/270 | 146/270 | 264/270 (97.8%) |
| Within seven days | 267/270 | 266/270 | 270/270 |
| Observations on both sides within seven days | 250/270 | 137/270 | 265/270 (98.1%) |

These are envelope-intersection metadata opportunities, not support coverage, asset access, clear pixels, resolved states or temporal-transfer eligibility. They do not describe a future expanded spatial population until coverage is checked against that population. No archive census was repeated for this report.

Wave 2 supplies the empirical warning:

- 192 sampled supports on 24 dates; 171 had a chip, but only 54 had some resolved optical information.
- At primary 30 m support, best-view resolved fraction was approximately 27.00–28.21% design-weighted; 11 supports had conditional temporal bridges, weighted 5.55%.
- Conditional evidence occupied four dates and three of twelve era-quarter strata; ten were land/canopy contexts and one broad-water context. There was no demonstrated conditional transition, artificial-confuser or resolved boundary coverage.
- Changing 10/30/50 m representation did not change the 54 informative/11 conditional counts. The problem cannot be fixed merely by choosing a larger reference window.
- Weighted whole-wave water envelopes were 0.43–95.06% under the stated continuity assumptions; they were not confidence intervals. Allowing arbitrary unobserved intervening changes returns uninformative bounds.
- Received/charged imagery was about 1.89 GB/1.764 GiB; actual human interpretation hours were not recorded and cannot be reconstructed. Resource availability alone is not evidence that another larger wave will succeed.

Human–AI agreement was measured, not human–human reliability. High eligibility agreement mostly reflected shared UNKNOWN. The old declared human return and AI return also had a documented concordance anomaly; preserve that record without deciding dishonesty or treating it as independent replication. A future final response workflow requires clear custody, genuinely independent first and second human readings on a prespecified subset, and originals retained before adjudication.

Local sources: `PHYSICAL_CONTEXT_REFERENCE_DESIGN/FRAME_FEASIBILITY/OPTICAL_OPPORTUNITY_SUMMARY.json`; `REFERENCE_QUALIFICATION_WAVE2/FINAL_QUALIFICATION/WAVE_SUMMARY.json`, `UNCERTAINTY_AND_CONTEXT_SUMMARY.json`, `CLUSTERING_AND_PROVENANCE.json`, and `DECISION_FOR_REVIEW.md`. These are qualification findings, not detector accuracy.

## 2. Re-derive falsification domains from failure mechanisms

Current VV is affected by roughness, incidence/geometry, material, vegetation and mixtures. Spatial coherence and low intensity do not resolve competing physical explanations. The challenge questions should therefore precede map categories. OPERA's separation of water, partial-water/support and problematic observation classes illustrates why a single land-cover partition is insufficient; its rules are not imported as Kusan rules. [DSWx-S1 specification](https://www.earthdata.nasa.gov/s3fs-public/2023-12/ProductSpec_DSWX_S1.pdf)

| Challenge question | Evidence-first development domain | Why C1–C7 alone is insufficient |
|---|---|---|
| Can water be detected without a temporal change signal? | Independently visible persistent open-water interiors, both sheltered and rough/exposed settings | Persistence is a temporal property; one static water polygon cannot establish it. |
| Can water be detected where historical maps say land, and removed where it recedes? | Independently observed inundation/recession, wetland/floodplain/agricultural transitions | A river buffer is not a demonstrated transition. |
| Can smooth non-water avoid false positives? | Visible paved/industrial/open artificial surfaces; bare or smooth natural ground; selected canopy/vegetated controls | “Built” omits smooth natural confusers, while building roofs are not all dark in VV. |
| Does resolution/registration change the conclusion? | Narrow channels, small basins, shoreline mixtures, boundaries at different orientations | Size and mixture cross inland, pond and coastal categories. |
| Can uncertainty remain uncertainty when the sensor cannot observe reliably? | Terrain/building-obstruction risk and independently documented poor processing/support cases | Land-cover strata do not represent observation quality. |
| Does the detector behave sensibly on the ordinary landscape? | Ordinary canopy, cropland, other land and broad water controls | A collection of dramatic counterexamples does not establish ordinary performance. |

Use overlapping tags for inland/coastal, artificial/natural, size, edge/interior, persistent/transition, topographic risk and reference-source quality. Do not force them into seven mutually exclusive sampling strata. Coastal rough water is a useful challenge if inside the target population, but “coastal” need not consume one equal-allocation stratum. Basin type is useful context, but mapped basin existence is not contemporaneous water.

For development only, choose among independently supported object/date pairs using source clarity, temporal proximity, physical diversity and cost. Do not use VV values, candidate maps or A/B disagreement. Choosing clear reference evidence is appropriate for a deliberately selected mechanistic panel; it does not create a representative final sample. Maintain a failed-candidate log to expose selection limits. Freeze each development panel before detector comparison. New evaluation SAR processing, if the suitable pairs lie outside the existing eight dates, is a later explicit resource/processing authorization.

A manageable first development allocation is a small number of distinct physical systems per challenge, with repeat observations where they establish a meaningful temporal contrast. Any numeric allocation should be a workload cap, not a claim of statistical sufficiency. Do not fabricate a successful dynamic-water example merely to fill a cell; the missing domain constrains the eventual claim.

## 3. Compare source architectures

| Criterion | RBI-only | GlobeLand30-only | Minimal multi-source auxiliary frame | Base frame without exhaustive auxiliaries |
|---|---|---|---|---|
| Independence | No inherent immunity to shared inputs; source role matters | Optical-derived does not mean perfect or independent reference truth | Track each role and inputs; sampling auxiliaries need not be independent of all detector covariates | Strong separation from thematic assumptions |
| Temporal relevance | Mixed input/update dates; production year is not feature observation date | Nominal epochs may miss 2017–2025 changes | Different vintages disclosed; can capture complementary opportunities | No historical class assumptions; date coverage explicit |
| Resolution | 1:50,000 source scale does not certify 10 m boundaries | 30 m class cells cannot resolve every narrow/small feature | Match each use to native support; no invented finer detail | Grid indexes supports; not physical independence |
| Completeness | Thematic and delivery gaps currently unresolved | Broad legend/exhaustive coverage except no-data, but small confusers omitted | Residual/missing stratum makes imperfect coverage survivable | Complete once target geometry and date eligibility are fixed |
| Probability validity | Valid if exhaustive partition and correct probabilities | Same | Same; overlaps require explicit handling | Simplest probability logic |
| Reproducibility | Release/theme/feature provenance needed; current live route cumbersome | Fixed tile/version/hash relatively simple | More source/version/overlay decisions to freeze | Minimal inputs and audit burden |
| Rare confusers | Potentially valuable local detail if available | Weak | Best potential enrichment without demanding all details | Weak unless paired with challenge development and later auxiliary enrichment |

Government status does not establish reference quality. RBI original IDs/boundaries remain valuable for source auditing and physical-system reasoning, but are not required to give every centre a known selection probability. Frame validity requires stable derived membership and documented provenance; it does not require knowing every feature's physical parent.

GlobeLand30's broad 30 m land-cover categories provide an opportunity map, not the required acquisition-time physical states. [Chen et al., 2015](https://doi.org/10.1016/j.isprsjprs.2014.09.002) HydroLAKES explicitly targets lakes at least 10 ha, so absence cannot establish absence of small Kusan ponds. [HydroLAKES documentation](https://www.hydrosheds.org/products/hydrolakes)

**Minimal proposed hierarchy:** use one frozen water-opportunity source, one frozen artificial-surface source, and an exhaustive residual. Keep geometry/terrain as optional diagnostic flags rather than making a third mandatory census. Existing JRC history and GHSL E2018 are practical candidates for sampling-only roles because they have already been investigated, not because they are guaranteed optimal. RBI or attributable mapped local features can supplement development discovery without blocking the final base frame. A general vegetation layer is unnecessary merely to define ordinary controls: the residual is sampled and its actual context is interpreted independently.

If the parent architecture chooses simple mutually exclusive final strata, four flag combinations of water-opportunity yes/no and artificial-opportunity yes/no are simpler than an arbitrary precedence hierarchy; include explicit auxiliary-missing handling. Alternatively a positive-probability base component plus enrichment can handle overlap, but its union probabilities and variance are more complicated. Prefer the simpler design unless the rare-domain gain justifies that complexity.

Sampling-only auxiliaries may cover the full population and may even share a sensor or covariate with the detector. That is not automatically circular reference measurement: probability sampling may be stratified on the map under assessment itself. The critical conditions are known positive inclusion probabilities, frozen selection rules, appropriate weighting and independently measured reference responses. Shared ancestry must still be disclosed, especially when interpretation may inherit a map's mistakes. [Olofsson et al., 2014](https://doi.org/10.1016/j.rse.2014.02.015)

No proposed source becomes acquisition-time truth. If JRC also remains a candidate detector context, explicitly register the dual sampling/context roles and prevent readers seeing it; a sample can validly be stratified by a detector covariate, but a label derived from that covariate cannot validate it independently.

## 4. Reference source and response hierarchy

### Source roles

1. **Sampling auxiliaries:** archived maps, hydrography, built-up or terrain opportunity flags; whole-population coverage permitted under a role-based amendment; no current class truth.
2. **Acquisition metadata:** timestamps, footprints, sensor generation, processing level, QA availability and prospective access/cost. Use for logistics and feasibility; never equate catalogue cloud percentage with local clarity.
3. **Reference observations:** dated original optical images and their native QA/registration metadata, independently interpreted. Sentinel-2/Landsat remain useful for broad interiors; high-resolution PlanetScope/RapidEye are most scientifically justified for small, artificial and boundary contexts, not as an automatic rescue of whichever final cases prove difficult.
4. **Temporal supporting evidence:** independently dated stage/rainfall/event/operational records and before/after optical observations. Each observation has a specific inference limit; regional rainfall absence cannot prove no local pumping, inundation, tide or management change.
5. **Detector inputs and diagnostics:** current S1 and specifically approved ancillary inputs stay outside reference-reader packets. Later freeze records which source roles were actually used.

The acquisition hierarchy must be fixed before final responses. For each final sampled unit, use the same prespecified search/ranking/escalation rules, exposure budget and failure categories, independent of predictions and first labels. It is legitimate to select a better *reference observation for the same sampled unit* using QA; it is not legitimate to replace the sampled unit with one that is clear. Escalating costly imagery only where disagreement with the detector occurs is prohibited. A preallocated, probability-selected enhancement subset is an alternative if uniform high-resolution escalation is unaffordable.

### Planet-specific feasibility limits

Planet products can be valuable, but do not treat 3 m posting as 3 m positional certainty. Provider documentation recommends ground-locked imagery for positional work and distinguishes visual display products from analytic/SR products. [PlanetScope documentation](https://docs.planet.com/data/imagery/planetscope/) UDM2 is global only from August 2018, with some missing assets; older periods need an explicit QA protocol. [UDM documentation](https://docs.planet.com/data/imagery/udm/)

The saved October 4–5 terms review established only plan plausibility: an account balance of 3,000 km²/month did not establish asset-specific access, charge stage, repeat-order treatment or current minimum charge. An indexed historical 100 km²/scene minimum would allow at most 30 fresh minimum-charge scene operations per monthly allocation. Do not reuse it as a confirmed current tariff or forecast. A small clipped chip and a small billed order are not synonymous. No account probe or order was performed here.

This argues for a development panel that learns the marginal information gain of genuine high-resolution evidence before adopting an expensive final response protocol. It does not justify selecting final sample units near cheap/clear scenes without accounting for the changed population/probabilities.

### Response protocol simplification

Maintain four separate fields instead of forcing one label:

1. **Optical-time observable composition:** W/N/O/U fractions or intervals on a fixed 30 m support, with 10/50 m sensitivities. Visible canopy is observable non-open-water canopy, not proof that water is absent beneath it. Keep unobserved fractions explicit.
2. **Spatial support:** registration evidence, uncertain shifts, boundary mixture, native resolution, scene coverage and resulting interval envelope. Do not align optical imagery to maximize agreement with S1 predictions. Apply measured/source-supported registration uncertainty, not a convenient performance-selected shift.
3. **Temporal transfer:** source timing, before/after states, physical continuity evidence, conceivable intervening changes and evidence quality. Return direct/closely supported, conditional transfer, contradicted transfer, or UNKNOWN; exact field names can preserve the existing protocol. No universal hour cutoff and no requirement to prove the impossibility of every transient.
4. **Acquisition-time response:** an interval conditional on explicitly stated transfer assumptions, or UNKNOWN. A conditional interval is not an unconditional confidence interval or calibrated probability.

If no transfer claim is defensible, preserve the useful optical-time information for development/feasibility, while acquisition-time bounds remain broad. If transfer is reasonable under stated ordinary-continuity assumptions, report it in a conditional analysis and include a pessimistic/no-transfer sensitivity. This avoids both automatic ±24-hour truth and the impossible demand for literally zero temporal uncertainty.

Before/after agreement is corroboration, not direct observation of the intervening instant. For dynamic floodplain and managed basin cases, two agreeing endpoints may be particularly inadequate. High-resolution optics improve spatial evidence but do not solve this temporal identifiability problem. A coarse contemporaneous weather observation likewise cannot establish a 30 m water boundary.

The OPERA validation repository uses independently generated high-resolution Planet reference imagery, demonstrating the value of an independently produced reference source. It does not establish that its dates, binary rules or tolerance are appropriate for Kusan. [OPERA validation repository](https://github.com/OPERA-Cal-Val/DSWx-Requirement-Verification)

## 5. Adequacy and stopping criteria

Architecture approval must not imply that a sample size or provider has already qualified. Before final sampling/acquisition, specify intended precision or decision resolution, date-cluster allocation, source-cost ceiling and unknown-bound reporting. These numeric choices are scientific design decisions; literature does not supply a universal minimum of two water and two land cases or an 85% pass mark.

The development programme should proceed to candidate comparison only when:

- Both observable water and non-water contrasts are independently evidenced on the chosen support, with multiple physical systems and dates rather than many adjacent pixels in one pond.
- Persistent water, new/receding water, smooth land and support-limited situations are either represented or explicitly excluded from the claims being tested. No quota-completion fiction.
- Source display/radiometry, registration and temporal assumptions are inspectable and reproducible; independent-reader discrepancies are retained.
- A concrete bounded paired comparison is informative under those response intervals. If all candidate differences are swallowed by reference uncertainty, collect no more similar evidence merely to inflate the count.

The final evaluation should report design-weighted abstention and reference-response rates for the full sampled population, plus support/time/reader uncertainty. If UNKNOWN mass leaves whole-population bounds too wide, do not turn complete-case accuracy into whole-population accuracy. Return either a restricted, honestly named reference-observable-domain result with its limits, wider population bounds, or a resource/design decision. Selection probabilities do not eliminate nonignorable missing reference information. [Stehman & Foody, 2019](https://doi.org/10.1016/j.rse.2019.05.018)

A purely retrospective programme may never validate rapid flood transitions adequately across 2017–2025. That negative feasibility result must remain possible. Prospective field/timely imagery validation could improve mechanism understanding later, but it would not retrospectively observe missing historical states or automatically validate every reconstruction year.

## 6. Strongest argument against this recommendation

The legacy common-source physical frame was cumbersome, but it tried to force systematic attention to missing contexts and prevent subconscious test-location learning. The simpler design can lose that discipline: easily visible persistent lakes and broad dry land may dominate development; residual samples may miss rare confusers; historical auxiliary errors can hide exactly the novel water of interest; clear-weather validation can miss flood-weather failure. Permitting whole-population ancillary access also makes “never-seen geography” an indefensible claim.

A development challenge panel can produce a detector that survives a curated collection yet fails elsewhere. It therefore cannot replace a separately sealed final probability evaluation. Auxiliary enrichment should be judged by expected information/coverage rather than apparent detector success, and response operators must remain blind to predictions. Record unresolved challenge domains prominently. If the project requires a claim of geographic generalization to untouched regions, use an additional independent geographical holdout with a correspondingly narrower estimand; do not pretend that a role-based whole-population evaluation supplies that stronger claim automatically.

## 7. Version and migration cautions

- Preserve all old designs, incidents, sampled units, responses, reader declarations and hashes. Superseding a rule is not rewriting its history. No existing record is relabelled as untouched final validation by this report.
- Retire the proposition that one qualified official theme family is necessary for final probability validity. The current provider-safe-export harness remains useful engineering evidence, but becomes unnecessary when whole-population sampling-auxiliary access is explicitly adopted and no actual reference content is transferred.
- Retain normal security/licence limits and reference-evidence access controls. A broad ancillary exception is not permission to inspect target-date imagery.
- Do not silently update JRC: the current official page describes GSW1.5 with revised seasonality/yearly history and a Collection 1/2 registration discontinuity. Fix the exact snapshot for each role, preserving accepted products until an explicit change. [JRC version notes, updated 26 August 2026](https://global-surface-water.appspot.com/download)
- GHSL's E2018 10 m estimate derives from Sentinel-2 with additional training sources; it is a built-up opportunity indicator, not proof of pavement or current non-water. [GHSL data package documentation](https://publications.jrc.ec.europa.eu/repository/bitstream/JRC133256/JRC133256_01.pdf)
- No source, final stratum counts, final probabilities, new reserve or source-access budget was operationally created here. The architecture decision must precede those implementation details and any sampling.

## References and verification scope

Primary documents were checked on 8 October 2026 through text retrieval. No systematic review is claimed; some papers were available only through publisher abstracts/author repository descriptions. Olofsson/Stehman arguments concern sampling, response and inference principles; source-specific implementation choices above are our proposals, not requirements purportedly imposed by those papers.

- Olofsson et al. (2014), *Good practices for estimating area and assessing accuracy of land change*: https://doi.org/10.1016/j.rse.2014.02.015 ; author repository https://nottingham-repository.worktribe.com/output/728216/good-practices-for-estimating-area-and-assessing-accuracy-of-land-change
- Stehman & Foody (2019), *Key issues in rigorous accuracy assessment of land cover products*: https://doi.org/10.1016/j.rse.2019.05.018
- Stehman & Czaplewski (1998), *Design and analysis for thematic map accuracy assessment: Fundamental principles*: https://research.fs.usda.gov/treesearch/28388
- Chen et al. (2015), GlobeLand30 operational approach: https://doi.org/10.1016/j.isprsjprs.2014.09.002
- OPERA product and validation documentation: https://www.jpl.nasa.gov/go/opera/products/dswx-product-suite/ ; https://github.com/OPERA-Cal-Val/DSWx-Requirement-Verification
- PlanetScope/QA documentation: https://docs.planet.com/data/imagery/planetscope/ ; https://docs.planet.com/data/imagery/udm/
- HydroLAKES: https://www.hydrosheds.org/products/hydrolakes
- JRC GSW current version notes: https://global-surface-water.appspot.com/download
- GHSL data package: https://publications.jrc.ec.europa.eu/repository/bitstream/JRC133256/JRC133256_01.pdf

No research source was downloaded, no paid quota used, no random seed generated, no new sample drawn, no labels reread, no SAR processing/evaluation performed, and no authoritative existing output modified by this subtask.
