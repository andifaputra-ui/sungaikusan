# C2 validation architecture: decision for review

**8 October 2026 — DESIGN_COMPLETE; ARCHITECTURE_APPROVAL_PENDING.** This is the requested major redesign, not another qualification wave. No research sample/seed, imagery acquisition, final reference use, detector execution, paid order, new SAR processing or method freeze occurred. The original scientific artifacts remain unchanged.

## Decision recommended

Adopt **two separate evidence programmes**:

1. **Development falsification:** a small, deliberately selected, evidence-first challenge panel. Select physical situations and dates from independent reference evidence; use it to expose failures and qualify response measurement. Do not claim population accuracy from this panel.
2. **Final fixed-map audit:** after one candidate and its complete processing/response/analysis protocol are locked, draw a new probability sample across the declared acquisition-by-area population. Use the frozen map's output categories to make efficient sampling strata, while keeping all reference interpretation blind to those categories. Retain every nonresponse and use weighted error/abstention bounds when references are uncertain.

The decisive simplification is that **a complete ancillary atlas is not required for the final sampling frame**. An exhaustive geographic lattice and acquisition catalogue define the population. RBI, historical water, land cover and terrain can aid development discovery and contextual diagnosis without having to supply seven complete, supposedly physical strata first. A small auxiliary-enriched final design remains an alternative if pre-test calculations later demonstrate a substantial omission-error benefit; it is not the default.

This deliberately replaces the previous rule that final sampling must be independent of detector predictions. Sampling from a **locked map using a preregistered probability mechanism** is legitimate accuracy assessment; hand-picking disagreements or changing the map in response to final labels is not. This change must be explicit in the architecture decision. Olofsson et al. discuss map-based stratification; Stehman provides estimators when sampling strata and assessed classes differ. [Olofsson et al., 2014](https://doi.org/10.1016/j.rse.2014.02.015); [Stehman, 2014](https://experts.esf.edu/esploro/outputs/journalArticle/Estimating-area-and-map-accuracy-for/99892428704826).

**Do not confuse an evaluation lock with final thesis method freeze.** A candidate is locked to permit an honest final test. The method is accepted or rejected only after that test and scientific review. A failed candidate may be revised, but its opened test then becomes development evidence; it cannot be advertised as a fresh independent test of the revision.

## 1. What remains scientifically invariant

- The target is observable open surface water at each acquisition, including persistent and newly formed water. Historical occurrence cannot force or veto state. Subcanopy inundation and chemical contamination are not silently added to the target.
- Keep accepted Sentinel-1 sigma0/C1 processing fidelity, separate validity information, orbit provenance and full-source write/read boundary. This redesign changes validation, not radiometry, sensor or detector semantics.
- State the exact spatial/temporal population, response support and estimand. Every unit included in a population claim has known positive inclusion probability under the final design.
- Final reference judgments and test outcomes do not feed back into the candidate under evaluation. Original responses and exposure history remain immutable.
- Independently measure or bound acquisition-time state. Separate observation, position/support, timing and interpretation uncertainty; UNKNOWN and MIXED do not become convenient binary labels.
- Use estimators matching selection, weights, area, date clustering and repeated measurement. A reference count is not an effective sample size or an adequacy theorem.
- Document all exclusions, nonresponse, assumptions, costs and deviations. A rigorous negative result is preferable to an unsupported accuracy claim.

The previous seven contexts, 20% geographic reserve, 1 km block interiors, non-SAR-only ancillary rule, pre-2017-only auxiliary preference, mandatory single-provider route, and exact ancillary clipping contract are **not invariants**. Their historical use is preserved; their prospective necessity is reconsidered here.

## 2. Population and claim boundaries

### Spatial target

Recommend retaining the existing **L1 Kusan lowland analysis rectangle** as the operational C2 spatial target: EPSG:32750, 4,559 columns by 2,882 rows, 10 m lattice, 1,313.9038 km². This is a defensible reproducible analysis window; **it is not the entire Kusan catchment**. A whole-catchment thesis claim would require a separately delineated target and corresponding catalogue/processing assessment. Do not disguise that enlargement as a routine validation change.

Retire the central-500 m and complete-1 km-block eligibility restrictions for the new final population. They existed to protect viewing windows, not to define the physical phenomenon. Include edge cells, old reserve geography and development-influenced geography in a fixed-map population audit, with exposure status reported separately. The legacy 1,955,000 possible centres were only **14.8793%** of this rectangle; the old estimates were correctly conditional on that frame and are not reweighted into new results.

### Time target

Use a finite list of acquisition instances, not calendar days. Deduplicate adjacent products/processing versions from the same relevant overpass, and preserve the accepted sensor/mode/orbit/coverage eligibility. The existing list has 270 full-envelope eligible catalogue entries across 2017–2025, but completeness outside that saved catalogue is unverified. A metadata-only catalogue/identity audit must establish the final list before randomization. Missing acquisitions cannot be called dry days; the audit does not interpolate between dates.

The primary mean weights eligible acquisitions equally and area equally within each date. Calendar-duration weighting, event-frequency estimation, every-date accuracy, upstream-basin accuracy and transfer to another basin are different estimands. They are not obtained automatically from this design.

### Primary response units

Use **non-overlapping 30 m tiles**, each normally containing 3×3 accepted 10 m map cells, anchored at the fixed lattice origin. Keep partial boundary tiles with their actual area. Metadata arithmetic gives 1,460,720 tiles: 1,458,240 full nine-cell tiles, 2,479 six-cell edge tiles and one four-cell corner tile. Their areas sum exactly to all 13,139,038 map cells.

Thirty metres is a pragmatic response support, not a claim about independent SAR measurements or an exact point-spread function. Preserve 10 m centre-cell and 50 m surrounding-window sensitivity readings; they are different-support diagnostics, not independent replicates or an interchangeable area partition. Position uncertainty comes from the actual source/registration evidence. The old ±20 m scenario grid may remain a labelled sensitivity, never a calibrated error distribution.

Old centred-neighbourhood responses are unchanged. They cannot be silently converted into responses for the newly anchored disjoint tiles. No majority-water cutoff or other new binary semantic tolerance is introduced.

## 3. Why two programmes beat the legacy design

| Architecture | Main strength | Main weakness | Decision |
|---|---|---|---|
| Legacy C1–C7, strict reserve, 36 dates/up to252 supports | Explicit physical intentions, immutable probability qualification and strong operational blinding | Conditional narrow geography; expensive source contract; one support/context/date cannot estimate within-date context variance; still poor timing evidence | Preserve as historical branch; replace as future architecture |
| GlobeLand30-only surrogate strata | Simple broad historical categories | Small/narrow/new water and particular confusers can be missed; broad classes are not physical states | Optional discovery auxiliary, not the foundation |
| Multi-source physical auxiliary frame | Can enrich rare omitted water and artificial contexts | More epochs, overlays, source gaps and hidden dependencies; another complete atlas can become a bottleneck | Optional precision enhancement, only when justified |
| Uniform probability final sample only | Fewest assumptions and simplest access | Inefficient for rare predicted water or abstention; weak falsification | Valid fallback, not preferred default |
| **Targeted development + locked-map probability audit** | Separates counterexample search from inference; exhaustive population; no official-source dependency; known probabilities and sealed responses | Map-negative omission errors may be rare; human governance and reference adequacy remain difficult | **Recommended** |

A probability design supports inference about a fixed map without requiring every location to be geographically distant from development. It does not establish transferability to untouched geography. [Wadoux et al., 2021, full paper](https://alexandrewadoux.github.io/assets/pdf/Wadoux_et_al_2021.pdf). Structured holdouts remain relevant when the intended claim is prediction to new places or periods. [Roberts et al., 2017](https://doi.org/10.1111/ecog.02881).

## 4. Development: seek falsification, not representativeness

Retire C1–C7 as compulsory exclusive quotas. Use overlapping physical failure tags:

| Required challenge | Appropriate independent evidence | What would falsify a claim |
|---|---|---|
| Persistent water | Dated visible water interiors, repeat evidence where useful | A change-dependent architecture systematically misses it |
| Newly inundated/receding water | Dated transition sequence with defensible acquisition-time constraints | Historical context vetoes new water or preserves vanished water |
| Smooth non-water | Dated visible pavement/industrial surfaces and smooth natural/bare ground | Darkness or coherent shape is promoted to water without resolving alternatives |
| Narrow/small/mixed features | Channels, basin edges and shores with registration/support evidence | Results depend on arbitrary centring or imply detail absent from the observation |
| Rough water and difficult observation | Exposed water, terrain/building obstruction, invalid processing/support | Bright water is systematically excluded or unobservable support becomes a confident class |
| Ordinary controls | Ordinary vegetation/land and broad water across independent systems | A method handles special cases but fails ordinary conditions or abstains everywhere |

OPERA documentation recognizes several of these distinct observation problems; its thresholds and masks are not adopted here. [OPERA DSWx-S1 specification](https://www.earthdata.nasa.gov/s3fs-public/2023-12/ProductSpec_DSWX_S1.pdf).

A practical proposed first cap is **24 distinct physical systems and up to48 date-support records**, covering all six challenge families where evidence exists. Two systems per family and meaningful repeated dates are diversity aspirations, not statistical minima. An unfilled transition or confuser family is a documented limitation, not permission to relabel another case. Existing eight-date SAR products may be preferred for cost only when reference suitability is comparable; 2018 is not mandatory.

Select with independent geography and dated reference evidence, not current VV, candidate maps or A/B disagreement. Clear-evidence selection is now permissible because this is explicitly a purposive development panel. Log rejected/ambiguous candidates and practical effort. It cannot estimate landscape prevalence, final accuracy or whole-population response yield. Once the panel is locked, later authorized detector comparisons can use it and all outcomes remain development evidence.

Do not launch that acquisition or A/B now. First qualify one coherent radiometric/display pipeline from already acquired evidence and product documentation, without reopening the nine old response conflicts. Preserve conflicting old interpretations. The Wave2 279/322 optical offset-metadata conflicts justify this source-quality task, not retroactive label correction.

## 5. Final probability design: the smallest operational specification

### Locks and ordering

1. Complete development/reference qualification. Choose one candidate using development evidence only.
2. Lock detector code, radiometry/processing, scene-level estimation rules, random-state handling if any, target population, response rules, metrics and final acquisition/fallback budget. This is an **evaluation lock**, not a success declaration.
3. Draw dates from the metadata frame. Only after this architecture is approved and later sampling is authorized may a seed exist.
4. Process the selected dates using the locked pipeline, producing complete W/N/abstention-support outputs for their full target area. Failures remain explicit unavailable/abstention support; they do not trigger replacement dates.
5. Construct each selected date's strata mechanically, record counts/hashes, then draw response tiles. Developers do not inspect sampled-location predictions or their optical evidence. Interpreters see neither strata nor predictions.
6. Lock the reference responses before joining them to predictions. Publish the single final audit without tuning the evaluated version.

This needs additional SAR processing later, but only for selected dates before validation; it does not require full 2017–2025 production to construct the sample. No such processing is authorized or run now.

### Dates and allocation

Use **year × calendar-halfyear** temporal strata. These are balanced calendar bins, not an asserted local wet/dry-season classification. The initial planning configuration is two dates by simple random sampling without replacement per nonempty stratum: 36 dates for the current18 strata. Census a stratum with fewer than2 eligible dates; a single available date contributes no within-stratum date-sampling variance because it is fully enumerated.

Use eight tiles/date as the initial cost/precision scenario: **up to288 tiles**, not a claim of sufficient final sample size. The exact final allocation is frozen before the final draw using development response widths, interpretation costs and prespecified precision calculations. Expanding automatically until final results look satisfactory is prohibited.

### Four mechanically defined map strata

For each 30 m tile, record whether any included 10 m cell is predicted W and whether any is abstention/invalid/unresolved (A). N means an actual explicit non-water output; unrecognized codes fail validation.

| Stratum | Any W? | Any A? |
|---|---:|---:|
| P0: all N | No | No |
| P1: W present, fully assigned | Yes | No |
| P2: A present, no W | No | Yes |
| P3: W and A present | Yes | Yes |

These are sampling categories, not reference labels. They preserve W/N mixtures and W/A mixtures without inventing purity thresholds. Census a stratum with one tile; otherwise initially allocate at least two tiles per nonempty stratum. Redistribute unused slots in fixed P0,P1,P2,P3 round-robin order subject to stratum capacity. If only P0 exists, eight tiles are sampled there; the absence of mapped water is not evidence that real water is absent. The allocation rule and stratum counts are recorded before reference access.

P0 is especially important: genuinely missed water can occur anywhere in it. A coarse historical-water mask must never remove any P0 tile. A map-based design may nevertheless estimate rare omission errors poorly. If pre-final development calculations show that P0's required precision cannot be met at affordable sample size, compare a **prospectively specified** additional water-opportunity split of P0 against a larger P0 allocation. Choose before final sampling; no final failure can trigger a selective extra search. Otherwise retain the simpler four strata and report the limitation.

Rare omission uncertainty is a recognized allocation problem, not proof that map-based probability sampling is biased. [Olofsson et al., 2020](https://www.sciencedirect.com/science/article/pii/S0034425719305115).

### Inclusion probabilities and estimators

Let temporal stratum h have D_h dates and d_h selected dates. For selected date t, map stratum k has M_tk tiles and m_tk selected tiles. Each eligible date-tile pair has

`pi(t,i) = (d_h / D_h) * (m_tk / M_tk) > 0`.

There is no reserve-selection factor because no geographic reserve is used to restrict the new primary population. A tile's weight is `1/pi`; its area a_i is a **separate** factor. An endpoint total is estimated by `sum_sample a_i * endpoint_i / pi_i`, divided by known total date-area `D * A` for the primary acquisition-area mean. Sampling by tile count and weighting by actual area preserves partial edge tiles correctly.

For exact two-stage variance, let Yhat_t be a stratified expansion of a date total and Vhat_t its within-date variance. Sum over temporal strata:

`Vhat(total) = sum_h [D_h^2 * (1-d_h/D_h) * s_h^2(Yhat_t)/d_h + (D_h/d_h) * sum_selected_dates Vhat_t]`.

Within each date, `Vhat_t = sum_k M_tk^2 * (1-m_tk/M_tk) * s_tk^2(a_i*y_i)/m_tk`. Census terms are zero. The same estimator applies to fixed response-bound endpoints; dividing by `(D*A)^2` gives mean variance. A date's repeated views, pixels and shifts do not become independent sample units. Ratio measures need ratio-aware variance or design-respecting resampling, not naive binomial intervals. Joint endpoint uncertainty and small date-stratum degrees of freedom must be reported; approximate confidence statements are not exact finite-sample guarantees.

## 6. Response protocol and measurements

Preserve four separate layers of each response:

1. **Optical-time observation:** spatially located W/N/obscured/unresolved portions; source, UTC acquisition time, native support, QA and radiometric/display provenance.
2. **Spatial support:** mixture, source registration uncertainty and plausible alignment scenarios. No output-guided snapping or optical/SAR water-boundary alignment.
3. **Temporal evidence:** same-state physical continuity, before/after observations, intervening event evidence, possible transients and their uncertainty. Neither ±24/72 hours nor a quiet event catalogue is an automatic transfer rule.
4. **Acquisition-time bounds:** directly supported, conditionally bounded under named assumptions, not transferable, or unresolved. Explicitly keep conditional bounds separate from an assumption-relaxed envelope.

For each acquisition-time tile, define an admissible water-area fraction interval `[l,u]`. UNKNOWN is `[0,1]`; visible mixture is not collapsed to a binary majority label. If spatially located optical constraints are defensible, preserve those constraints to tighten later error bounds. If only tile fractions are known, do not invent subpixel locations.

Let the locked map predict area fractions w,n,a, summing to1. Let xW,xN,xA be actual water portions inside the predicted W,N,A portions. Impose `0<=xW<=w`, `0<=xN<=n`, `0<=xA<=a`, and `l<=xW+xN+xA<=u`. Then:

- False-positive area = `w-xW`; false-negative assigned area = `xN`.
- Water left abstained = `xA`; non-water left abstained = `a-xA`.
- Assigned error area = `w-xW+xN`; correct assigned area = `xW+n-xN`.

Minimize/maximize each quantity over the admissible set, separately by reader/timing/alignment scenario. This gives honest partial-identification bounds. It is an accounting operation on fixed outputs, not a classifier or semantic fusion. A tile with map and reference water fractions both0.5 can have pixel disagreement anywhere from0 to1; fraction equality is not pixel accuracy. Spatially explicit evidence may narrow that range.

For fraction-only constraints the assigned-error endpoints have a simple closed form: `lower=max(0,w-u,l-w-a)` and `upper=w+n-max(0,n-u,l-n-a)`. Separate metric extrema need not coexist in one possible reality; ratios and paired A/B differences must respect common constraints rather than combining incompatible marginal endpoints.

Report **coverage/abstention, commission and omission mass, water/non-water bounds and reference nonresponse together**. Selective error among assigned pixels is undefined when assigned area is zero; do not reward an all-abstaining map with perfect accuracy. Producer/user accuracy can be bounded only with defensible numerator/denominator constraints; if water denominators can be zero or intervals are uninformative, report that rather than a point accuracy, F1 or kappa. Gross uncertainty cannot be hidden by reporting only clear/transferable cases.

Sampling confidence intervals describe variation from the design. Reference bounds describe imperfect measurement; they are not calibrated confidence intervals. Reader disagreement, positional scenarios and timing assumptions remain separately visible. This distinction is essential when imperfect references have correlated errors with evaluated maps. [Foody, 2010](https://www.sciencedirect.com/science/article/pii/S0034425710001434).

## 7. Sources and firewall roles

| Information | Permitted role after architecture approval | Forbidden shortcut |
|---|---|---|
| S1 metadata, lattice and catalogue | Whole-population frame; processing/support diagnostics | Dropping failed dates or support to improve results |
| RBI, hydrography, coastline, terrain, land-cover/built maps | Versioned development discovery; descriptive tags; optional preregistered sampling auxiliary | Acquisition-time truth, source-government status as accuracy proof, undocumented detector feature |
| Accepted JRC history | Retain its separately registered optional detector-context role; sampling role only if declared | Forcing persistent water, vetoing new water, silently changing version |
| GHSL, JAXA/L-band | Diagnostic/deferred roles retained unless a later explicit method change is approved | Introducing another detector chain because data exist |
| Dated optical/other independent contemporaneous evidence | Development response or separately sealed final response, with explicit provenance | Reusing a known development label as an independent final reading |
| Frozen candidate predictions | Mechanical final sample stratification and final comparison by custodian | Showing predictions/stratum labels to interpreters; tuning from final results |

The default final frame requires **no new thematic source acquisition**. For development, S2 and Landsat are complementary public routes; a successful catalogue query does not establish usable pixels or correct radiometry. Planet/other VHR may help narrow/built/basin supports but can still be cloudy or temporally unsuitable. Asset-specific entitlement, QA/bands, licence, delivery size and charging must be verified before later acquisition; no quota is consumed by this design.

Retire geographic restrictions for approved **sampling-only ancillary data**, not for every file with an auxiliary name. Full-source transfer may be scientifically permissible when it contains only the declared ancillary role; licence/security and resource limits remain. Original feature IDs and true boundaries are still required when an analysis actually measures physical feature boundaries or repetition. They are not required merely to construct an exhaustive sampling partition. Missing auxiliary coverage becomes a documented flag/residual, not population exclusion.

The safest operational separation on this shared computer is **time separation**: no final reference acquisition or review until the candidate and response protocol are locked. A separate folder or another assistant with inherited history does not create an independent reviewer. After lock, a custodian generates blinded packets; a human first reader records responses; a genuinely independent human second reader evaluates a randomly preselected subset. A proposed25% double-read allocation is a cost scenario, not demonstrated reliability. Stratify the subset across dates/map strata before interpretation and retain its conditional selection probabilities. If a second human is unavailable, report human–human reliability unmeasured and do not simulate independence through AI or endorsement.

Use neutral IDs; omit sampling class, historical expected state, detector output and previous answers. Log any accidental prediction/reference linkage. Original independent responses are retained before any blinded clarification; unresolved disagreement expands the admissible envelope rather than forcing consensus. The prior AI and human returns remain exactly as documented.

## 8. Exposure migration and the strongest objection

Preserve the legacy reserve and incident files as historical facts. **B0200_0000 and B2000_1100 remain EXPOSED and permanently ineligible for an untouched-validation claim.** Their inclusion in a future fixed-map population audit, if selected by the new design, does not make them untouched. The unviewed XML binary and potential catalogue preview remain recorded with unknown content/extent; nothing is decoded or retrospectively cleared.

Maintain exposure domains: (a) response/label or detector-tuning exposure; (b) ancillary/engineering-only exposure; (c) unresolved exposure; (d) no recorded development exposure under the audited ledger. Report final estimates by these domains where precision permits, and their population weights. Fresh blinded measurement of the same old site/date is a new measurement, not a new physical state. It may inform a fixed-map audit but cannot establish novel-site generalization. Never reuse original development labels as final answers. If new independent measurement is impossible, retain that final unit as bounded/UNKNOWN, without replacement.

**Strongest argument against this recommendation:** it can turn a simple geographic firewall into a subtle governance problem and make overfitting look respectable under the phrase “fixed-map accuracy.” Auxiliary maps and memorable development sites can influence people. Map-negative strata may contain too few reference observations to characterize rare omitted floods. A purposive development panel may be dominated by clear, easy-to-transfer conditions, while the true final population remains cloudy and dynamic. A mathematically correct weighted estimate cannot repair a systematically unmeasurable reference state.

The defence is limited and explicit: immutable evaluation lock, blind new measurements, full-population probability selection, exposure-domain reporting, a retained broad P0 stratum, no replacement of UNKNOWNs, and no claim of universal/new-basin generalization. If that governance cannot be implemented, keep a restricted geographic test and accept the narrower population claim instead. The role-based architecture is recommended because it removes unnecessary access bottlenecks while addressing actual inference; it is not a guarantee that the thesis can achieve accurate flood reconstruction.

## 9. Adequacy, resources and stopping rules

### Evidence before expense

Saved metadata provides combined optical opportunities within24h for230/270 dates and bracketing within7days for265/270. These are envelope intersections, not clear supported acquisition-time references. Wave2 produced only11 conditional bridges among192 supports, weighted5.55%, concentrated in land and one broad-water case. Increasing resolution or sample count does not remove this bottleneck.

If, optimistically, only5.55% of the population had exact reference states and the rest were completely unresolved, an observed90% accuracy on that resolved portion would allow whole-population accuracy from **4.995% to99.445%**. This is an illustrative identification calculation, not a re-analysis of Wave2 or a forecast. Unknown mass alone creates the94.45-point width.

Before committing a final audit, use development source/response findings to calculate achievable endpoint precision, sensitivity to timing assumptions, reader disagreement, expected unknown mass and rare-class precision. Prespecify the smallest decision-relevant differences and tolerable uncertainty for each claimed metric. There is no universal12+12 or288-record adequacy rule. If measurement bounds alone exceed the scientifically useful resolution, do not launch a larger audit to hide that fact; improve independently justified evidence, restrict the prospective claim openly, or retain failure to validate.

### Workload scenarios, not an authorization

| Configuration | Responses | Ideal SRS95% halfwidth at p=0.5 | Public-route byte extrapolation for4 slots/support |
|---|---:|---:|---:|
| 18 dates ×8 | 144 | ±8.17points |1.89GiB |
| 36 dates ×6 | 216 | ±6.67points |2.83GiB |
| **36 dates ×8** | **288** | **±5.77points** |**3.78GiB** |
| 54 dates ×8 | 432 | ±4.72points |5.67GiB |

The18-date case supplies only one date per year-halfyear and cannot estimate between-date variance there without changing temporal stratification. The6-support case cannot provide2 observations in four nonempty map strata. The36×8 scenario is therefore a practical starting configuration for this structure, not an optimized or approved final sample size. SRS intervals ignore date clustering, unequal weights and reference error; real uncertainty can be much larger. Byte extrapolations use historical failed/successful public-route attempts, not Planet prices or native VHR delivery volume. No human-hour estimate is invented.

Propose retaining a **6GiB imagery ceiling and16GiB new storage ceiling** for any later approved bounded programme, with an explicit shared ledger across development/final activity; these are planning caps, not renewed download authority. Development48 supports×4 slots would extrapolate to roughly0.63GiB by the same weak public-route assumption. Default paid spend and Planet quota consumption remain zero pending an explicit source/cost approval. If limits bind, preserve unattempted/nonresponse records according to a balanced preregistered schedule, without favourable replacements. Full-source S1 processing has separate storage/runtime requirements and requires a later bounded plan.

### Stop conditions

- A source cannot support a needed response: record UNKNOWN and source failure; do not alter class definitions or rescue only convenient sites.
- Development cannot substantiate dynamic water or confuser claims: restrict those claims or retain detector inadequacy; no final accuracy promotion.
- The final catalogue/domain or candidate lock is incomplete: no final draw.
- The anticipated final bounds/precision cannot answer the stated question: no expensive final audit merely to meet a count.
- Final evidence leaks into tuning: preserve the incident and retire that test for the changed candidate.
- Final results are inconclusive or adverse: report them. Any revised candidate needs a new independent test plan; do not reuse the same released test.

## 10. What approval would mean next

Approve the **architecture**, including the finite-L1/acquisition population claim, disjoint30m accounting, two-programme separation, role-based ancillary access, final locked-map strata and exposure-domain reporting. Then prepare the executable metadata/role manifest, source-quality response implementation and bounded development evidence plan. Do not automatically draw the288-record scenario, order imagery, run A/B, process new dates or launch production.

The future path is: reference-qualified development challenges → separately approved bounded candidate comparison → candidate evaluation lock and exact probability/resource specification → authorized final sample/selected-date processing → blinded independent response → one-time weighted audit → scientific acceptance/rejection and only then final method freeze. This distinguishes the methodological decision now from later acquisition and detector authorization.

## Verification and supporting reports

- `architecture_checks.py` / `ARCHITECTURE_CHECK_RESULTS.json`:21 checks including tile-area conservation, complete edge retention, metadata arithmetic, weighted selection and exact two-stage variance over243 fully enumerated artificial sample combinations. No random number generation.
- `synthetic_strata_checks.py` / `SYNTHETIC_STRATA_RESULTS.json`:27 checks; all19,683 artificial3×3 W/N/A arrangements assigned exhaustively; empty/tiny-stratum allocation and code-rejection checks. No real map was read.
- `interval_accounting_checks.py` / `INTERVAL_ACCOUNTING_RESULTS.json`:3,025 artificial composition/interval cases;12,100 bound pairs checked against exhaustive feasible truth allocations. These validate accounting, not the truth of any real reference interval.
- `SOURCE_AND_RESPONSE_RECOMMENDATION.md`: independent source/response assessment and verified provider-document limits.
- `LEGACY_AND_ADVERSARIAL_REVIEW.md`: independent challenge of the legacy and recommended alternative.
- Supporting independent contributions compare alternatives; this consolidated decision controls where their initial recommendations differ.

The current CEOS listing identifies the November2025 v1.1 land-cover validation protocol. Its188-page PDF endpoint did not return successfully during this review; this report does not claim to have read it in full. Core arguments were checked against accessible original papers, abstracts and author repositories. [Official CEOS document listing](https://lpvs.gsfc.nasa.gov/documents.html).

All new outputs are design/provenance artifacts. Source rasters, reference responses, old samples, reserve records and authoritative SNAP/Python products were not modified. No background processing is needed while this package is reviewed.
