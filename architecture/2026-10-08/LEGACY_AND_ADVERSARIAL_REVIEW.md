# Independent adversarial review of the C2 validation redesign

**8 October 2026. Architecture analysis only; no sample, seed, imagery, final response, or detector output was opened or generated.** This report independently challenges both the legacy architecture and a role-based alternative. It is a recommendation, not implementation authority. Legacy records and restrictions have not been edited.

## 1. Verdict and the essential distinction

Recommend replacing universal geographic secrecy with a role-based architecture for **probability assessment of a specified, frozen finite reconstruction**. Retain a separate development falsification programme and a genuinely sealed final response process. Do not present this replacement as preserving the stronger claim of performance on geography that never influenced development.

The primary final question should be: how well does the frozen reconstruction describe observable open surface water across its explicitly enumerated acquisition-date/support population? That is different from how well the method would generalize to a new basin, a new period, or locations deliberately distant from development. The thesis can answer the former without pretending to answer the latter.

**Critical reservation:** fresh interpretation of a previously used site/date does not make the underlying physical state new or untouched. If development-influenced units enter a probability audit of a fixed map, label them accordingly and report that domain separately. A mathematically valid fixed-map estimate is not permission to advertise untouched predictive performance. Original response labels must never be recycled into a supposedly independent final response set.

Wadoux et al. (2021, section 2) explicitly distinguishes probability assessment of population map errors from spatial cross-validation; geographical proximity to calibration locations does not invalidate design-based assessment. Its argument does not authorize feedback from validation outcomes into the map under evaluation. [Author-hosted full paper](https://alexandrewadoux.github.io/assets/pdf/Wadoux_et_al_2021.pdf)

Roberts et al. (2017) supplies the strongest counterweight: structured dependence can make ordinary cross-validation optimistic for prediction to new conditions, while blocking can change the task towards extrapolation. Thus a transferability claim needs a corresponding test, not merely a probability map audit. [Publisher full text](https://nsojournals.onlinelibrary.wiley.com/doi/10.1111/ecog.02881)

## 2. What the legacy architecture actually protects and covers

The inspected legacy documents are `PHYSICAL_CONTEXT_REFERENCE_DESIGN/NEXT_PHYSICAL_CONTEXT_DESIGN.md`, `REFERENCE_RESPONSE_STAGE1/PROTOCOL.md`, `REFERENCE_RESPONSE_STAGE1/freeze.py`, aggregate sections of `FIREWALL.json`, `PERMANENT_EXPOSURE.json`, and `FRAME_FEASIBILITY/PROVIDER_QUALIFICATION_20261005/FRAME_OR_REDESIGN_DECISION_20261008.md`. No individual reference responses or imagery were inspected.

The current v1.1 proposal is 36 dates and up to 252 responses, rather than Wave 2's earlier 24-date/192-response qualification. It is explicitly conditional development qualification, not final full-domain inference.

Legacy geography arithmetic, verified from the saved grid and aggregate block counts:

| Geometry stage | Size | Implication |
|---|---:|---|
| L1 rectangular grid | 4,559 × 2,882 = 13,139,038 centres | 1,313.9038 km² nominal raster footprint; not the whole catchment |
| Complete 1 km blocks inside L1 | 1,260 blocks = 12,600,000 centres | 539,038 partial-edge centres excluded before exposure screening |
| Eligible complete blocks after prior-exposure exclusion | 981 blocks | 279 complete blocks removed by exposure-intersection rule |
| Random additional reserve | 199 blocks | About 20% within each quadrant; reserve is not an already labelled final sample |
| Development blocks | 782 blocks | 7,820,000 centres before chip-envelope restriction |
| Eligible central 50×50 positions in development blocks | 1,955,000 centres | Only 25% of each development block; 14.8793% of the full L1 lattice |
| Catalogue date × development-centre population | 270 × 1,955,000 = 527,850,000 | Conditional catalogue/support population, not all mission acquisitions |

The 14.8793% is a count ratio, **not a statement that all other land is scientifically unobservable or that the old qualification was invalid**. Its conclusions were explicitly conditional. It does show why simply retaining its weights and calling a later result whole-Kusan accuracy would be wrong.

Prior-exposure exclusions were whole-block intersections with buffered old points/windows. The reserve was then a random ceiling of 20% per quadrant: eligible counts NE257, NW256, SE206, SW262; reserved NE52, NW52, SE42, SW53. That random mechanism could support inference within its eligible pre-reserve domain if properly carried forward. It cannot give positive inclusion probability to the earlier excluded blocks or grid-edge centres. The 500 m sensitivity amendment did not repair that population coverage; it qualified ancillary support within the existing centre population.

### Strengths worth preserving

- Immutable probability draws, nonresponses, exposure history and reader returns; no quality-based replacement.
- Explicit separation of optical-time state, physical support, timing evidence and acquisition-time eligibility.
- A reproducible lattice, acquisition catalogue, response-size sensitivity and resource ledger.
- A genuinely enforceable access rule: source-window checks caught an actual implementation failure.
- Protection against unconscious reuse of repeatedly viewed successful objects and a transparent audit trail.
- Honest recognition that qualification yield did not establish accuracy adequacy.

### Project-specific constraints that are not universal statistical necessities

- Rejecting every ancillary transfer across a reserve boundary.
- Requiring all sampling auxiliaries to be non-SAR, from a single provider, or pre-2017.
- Requiring original authoritative physical-parent identity to construct every sampling stratum.
- Requiring seven contexts to be instantiated before any useful falsification work can begin.
- Fixed 1 km blocks, central 500 m sampling squares, a 20% geographic reserve, and their exact safety buffers.
- Treating arbitrary clip edges as a problem for source access rather than separately from physical-boundary inference.

Some remain useful operational choices; none becomes a theorem merely by appearing in a preregistration. An auxiliary used solely for a known-probability selection mechanism can contain correlated errors, radar inputs or a later map epoch without automatically biasing a design-weighted map audit. Such choices can still harm efficiency, context coverage, interpretability or blinding, and their lineage must be declared.

## 3. Minimum scientific invariants

1. **A declared target:** current-acquisition observable open surface water, including persistent and newly formed water. A dated historical polygon never supplies current state by fiat. The support and temporal estimand must be stated; a 30 m neighbourhood is not evidence of independent 10 m physical accuracy.
2. **A fixed inferential population:** every claimed unit has a known positive chance of selection under the final design, or an explicit non-covered domain. Undefined catalogue completeness and support losses cannot be concealed behind the word Kusan.
3. **Design-matched estimation:** unequal selection, repeated sites, dates and multistage selection are accounted for. Probability design validity does not require a model assumption that nearby ground conditions are independent.
4. **A valid response process:** evidence actually observes, or defensibly bounds, the target state and support. Optical state, cloud/obscuration, registration, mixture and temporal transfer remain distinct. Reference availability is not proof of reference adequacy.
5. **No development feedback from the final test:** lock detector, processing, response protocol, metrics and analysis before release; do not tune after seeing final failures and keep the same final claim.
6. **Measurement independence:** final interpreters are blind to evaluated predictions and previous responses, and their evidence is not silently derived from the candidate detector. Shared sensors or source lineage require disclosure and sensitivity, not an invented claim of zero error correlation.
7. **Truthful uncertainty and provenance:** missing/UNKNOWN is retained, not replaced with convenient classes; original records remain immutable; design and response uncertainty are not collapsed into binomial precision.

These are the scientific constraints. Exact buffers, software boundaries and source preferences should serve them, not displace them.

## 4. Strongest practical alternative

Separate three purposes rather than forcing one panel to do everything:

**Development falsification:** a modest evidence-qualified set chosen to challenge distinct physical failure mechanisms. It may deliberately enrich difficult situations. Do not use it for population accuracy. Failed candidate hypotheses and negative cases remain in its record. This purpose benefits from independently documented open-water interiors, narrow/mixed margins, ephemeral water/transition opportunity, smooth natural land, artificial surfaces, and observation/geometry limitations. It need not await a complete seven-stratum census.

**Reference qualification:** establish which acquisition-time/support claims can actually be supported, including difficult and low-opportunity conditions. Probability qualification remains useful for costs and nonresponse rates, but its allocation need not equal the final accuracy allocation. All prior qualification stays development evidence. Changing strata cannot cure cloud-related nonresponse or impossible state transfer.

**Final map audit:** after detector and response/analysis locks, draw a new probability sample spanning the declared final population. A reproducible small set of auxiliary strata can enrich rare contexts, with an everywhere-positive base component or exhaustive residual stratum. A custodian controls sample identities and optical responses. Report errors/bounds, abstention and reference nonresponse jointly. A separate transferability challenge is optional if the thesis makes a new-geography/time claim; it is not interchangeable with the map audit.

This is a structural recommendation. It does not prescribe an untested sample size, promise acquisition-time evidence, or authorize any draw.

## 5. Minimum role-based access specification

| Information | Sampling/response custodian | Detector development | Final interpreters | Release condition |
|---|---|---|---|---|
| Approved auxiliary maps, versions, coverage, metadata and source-derived strata | Full population | Allowed metadata/aggregate summaries and declared auxiliary use; discourage unconstrained exploration of prospective test neighbourhoods | Hide implied class/stratum where practical | Role registry before use |
| S1 acquisition metadata, grid and processing specification | Full population | Allowed | Acquisition time/support information only | No class suggestions |
| Development SAR, predictions, development references and disagreements | Allowed development domain | Allowed | Not shown as final evidence | Permanently development |
| Final sampled identities and selected target-date optical evidence | Held by custodian | Sealed before freeze and response lock | Assigned blinded packets only | Final lock or strictly separated automation |
| Final response values, independent-reader disagreements and evidence adequacy | Held, with originals immutable | Sealed | Reader sees own original response; reconciliation only under frozen protocol | Joint release after detector/response/analysis lock |
| Final prediction–reference comparison and error locations | Evaluation custodian | No access until one-time release | Hidden during initial interpretation | Report without retuning |

Different folders or separate assistants with inherited conversation history are not automatically independent custodians. A shared filesystem and one developer require process controls: access logging, hashed manifests, separate scripts, no map overlays that combine expected class with evidence, and a real independent interpreter where reliability is claimed. If secure role separation cannot be maintained operationally, delaying final reference acquisition until after detector freeze is simpler and more credible than pretending the same person remained blind.

The minimal rule is **no final response feedback into development**; it is not **no geography may ever be displayed**. Catalogue metadata can be sampled across the full population. Provider completeness, versioning and native-grid support remain data-quality concerns, while exact pre-transfer clipping solely to avoid reserve ancillary exposure can be retired prospectively after an explicit amendment.

## 6. Strongest arguments against this recommendation

### A. It can launder reuse through a change of vocabulary

Calling a label an auxiliary does not change what a developer learned. A hydrographic map, later water-occurrence product or a built-up layer can reveal stable state or expected failures almost as strongly as a response label. A knowingly curated full-population auxiliary may guide architecture to particular reserve objects. Role names alone do not establish independence. Mitigation: dataset-level role/version freeze; no final-site-driven auxiliary editing; separately report development-influenced domain results; prohibit case-specific corrections outside the preregistered general algorithm.

### B. A finite-map estimand can become an escape hatch

An overfit map may correctly reproduce known locations yet transfer poorly. A representative finite-population audit can honestly measure that map, but it cannot justify a reusable detector or reliable reconstruction outside its assessed population. The thesis must not quietly move from fixed reconstruction performance to methodological generality. A spatial/temporal transfer challenge is needed for the latter.

### C. The sampling architecture is not the main evidence bottleneck

The old failures involved cloudy optical observations, mixed support, uncertain registration and temporal transfer. More elaborate strata can merely distribute these failures more evenly. If final responses remain missing nonrandomly during floods, precise design weights do not identify acquisition-time accuracy. Complete-case results can still be misleading. A role-based redesign should be rejected if it merely enables another large low-yield wave without demonstrated response feasibility.

### D. Auxiliary errors can hide rare failures

Coarse water products miss ponds and narrow channels; built-up maps miss smooth natural surfaces; historical wetland classes do not locate every transition. An exclusive precedence hierarchy can suppress important overlaps. An exhaustive positive-probability base/residual component protects validity but does not guarantee enough rare cases to falsify the detector. Report auxiliary membership and independently observed physical context separately; do not call approximate map categories physical truth.

### E. Temporal selection can become fair-weather selection

Selecting dates only because clear reference imagery exists can change the target to clear-weather situations and under-represent peak floods. Known probabilities for an availability-enriched design solve sampling selection, not systematic inability to observe the missing states. Preserve positive probability for low-opportunity dates, or explicitly restrict the inference and quantify omitted support.

### F. Simpler access can mean a harder thesis defence

The legacy reserve allowed a compact story: these blocks were never viewed. A role-based design needs a longer but more accurate account of who saw which product and when. If the team cannot keep that ledger, the geographic rule is operationally safer despite its inefficiency. Do not erase original incidence reports to simplify the story.

### G. Scale mismatch survives the redesign

A 30 m interval reference tests 30 m-supported statements. It cannot by itself establish pixelwise 10 m classification accuracy. Aggregating 10 m predictions to a comparable support may support a fraction/error claim, while binary metrics require an independently justified class/mixture rule. Neither a convenient neighbourhood size nor a tolerance selected after A/B can solve that semantic issue.

## 7. Migration requirements: preserve facts, change prospective permissions

| Legacy item | Required treatment |
|---|---|
| 144-record Stage 1, 192-record Wave 2, earlier conditional intervals and all reader returns | Preserve original records, hashes, weights and original inference scope. Never relabel as final validation. |
| Existing source/protocol/synthetic tests and resource accounts | Archive as tested historical implementation; retain useful geometry/provenance tests. New-role configuration needs its own tests. |
| 782 development blocks and 199 additional reserve blocks | Keep original partition and randomization lineage. If retiring it, add a prospective supersession record; do not overwrite FIREWALL.json. |
| B0200_0000 and B2000_1100 | Permanently retain EXPOSED/INELIGIBLE_FOR_UNTOUCHED_FINAL_VALIDATION history. They could only enter a differently named fixed-map population audit under explicit new rules and exposure-domain reporting, never become untouched again. |
| D06_NW_2 and D12_SW_1 | Original quarantined technical nonresponse status remains; do not rewrite qualification estimates. |
| Oct 5 XML embedded binary | Remains UNVIEWED/EXTENT_UNKNOWN; architecture change is not evidence of its content. No need to decode it for redesign. |
| Oct 8 automatic preview concern | Preserve unknown transfer/rendering/extent and absence of a confirmed new affected block ID. Do not declare either a confirmed new final-label leak or scientifically cleared exposure. |
| Final labelled/held-out resources outside this new reserve | Continue sealed. A redesign authorization is not authority to read their labels. |
| Prior acquisition frame | Preserve 270-date catalogue and completeness limitation. Rebuild a broader mission/date frame only through a documented future metadata audit, not implied expansion. |
| Final population and exposure domains | New manifest must explicitly state geometry, date enumeration, support, exclusions, overlapping exposure categories and inference domains. Preserve all old totals as historical. |

A frozen exposure ledger should distinguish **bytes transferred**, **pixels decoded**, **displayed/viewed**, **interpreted**, **used for development**, and **final outcomes unblinded**. They are different events with different consequences. Evidence can remain unknown; no retrospective unexposure is possible. A historical access breach may cease to be a violation of a new prospective access rule, but it remains a historical fact.

## 8. Architecture acceptance conditions

Accept a role-based replacement only if the final package explicitly resolves:

1. Fixed-map finite-population inference versus new-place/time generalization, with distinct claims and denominators.
2. Full intended geographic support rather than inherited central-square convenience masks; honest handling of any remaining zero-probability units.
3. A realistic acquisition-time reference route, with UNKNOWN/MIXED and interval uncertainty retained.
4. A positive-probability, design-matched final assessment; selection independent of eventual response values and no convenience replacements.
5. A credible final lock/custodian/blinded interpretation workflow that works with actual staffing and tooling.
6. A migration ledger that does not turn old observations into new independent evidence or old exposures into untouched geography.
7. A separate falsification programme whose enriched cases are not pooled unweighted into population accuracy.

Until those conditions are specified, the alternative is an attractive access simplification rather than a defensible replacement architecture. Conversely, insisting on custom provider clipping and perfect physical-parent identity for every auxiliary is not justified merely by invoking statistical independence.

## 9. Literature consulted and limits

- Wadoux, Heuvelink, de Bruin & Brus (2021), *Spatial cross-validation is not the right way to evaluate map accuracy*, Ecological Modelling 457, 109692. Author-hosted full text inspected, especially section 2 and the finite-map experiment: https://alexandrewadoux.github.io/assets/pdf/Wadoux_et_al_2021.pdf . Supports design-based map audit, not unrestricted final-test reuse.
- Roberts et al. (2017), *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure*, Ecography 40, 913–929: https://nsojournals.onlinelibrary.wiley.com/doi/10.1111/ecog.02881 . Full publisher text inspected; used as a counterargument for predictive/transfer claims, not as a reason to reject survey inference.
- Brus (2021), *Statistical approaches for spatial sample survey: Persistent misconceptions and new developments*, European Journal of Soil Science 72, 686–703: https://bsssjournals.onlinelibrary.wiley.com/doi/10.1111/ejss.12988 . Distinguishes design and model randomness; publication online May 2020, journal issue 2021. Population independence is not synonymous with geographic separation.
- CEOS WGCV LPV, *Land Cover and Change Map Accuracy Assessment and Area Estimation Good Practices Protocol*, official document listing currently identifies **November 2025 version 1.1**, 188 pages: https://lpvs.gsfc.nasa.gov/documents.html . Version verified; this review did not successfully retrieve the complete v1.1 PDF, so no unverified page-specific claim is attributed to it. The older September 2025 draft is not represented as the current protocol.

The above literature establishes general principles. The access roles, migration inventory, exposure-domain reporting and suggested split between falsification and map audit are this review's reasoned recommendations for Kusan, not direct prescriptions or numerical constants from those papers.
