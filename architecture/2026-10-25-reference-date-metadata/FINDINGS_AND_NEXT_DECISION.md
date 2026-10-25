# No closer compatible SAR observation for the clear13/14May references

25 October2026. **NO_CLOSER_COMPATIBLE_IW_GRD_ACQUISITION_FOUND_IN_BOUNDED_PUBLIC_CATALOGUES.** Earth Engine and the independent ASF archive returned the same single11May2025scene. OPERA source provenance traces to that pass. Changing the SAR date to match these clear optical views is not supported by this metadata census. No new pixels, predictions, dates or reference labels were adopted; no job remains running.

## Actual acquisition availability

The window was frozen before querying: **7May00:00 through21May00:00UTC**, over the accepted L1 geography. The GEE query included all IW tracks/platforms before compatibility assessment; ASF independently searched the Sentinel-1 family,IW,GRD_HD/GRD_HS. No SAR intensity, candidate score, disagreement or inferred water state selected records. The archive queries remained below their declared record bounds.

| Catalogue | Returned evidence |
|---|---|
| GEE native S1GRD | One scene: S1A,IW,VV/VH,descending,relative orbit105,absolute orbit59152,11May22:00:24-22:00:49UTC. |
| ASF raw IWGRD | The exact same source ID, with metadata footprints covering the frozen sites. No closer record or alternative platform/pass appeared. |
| CMR DSWx-S1 | Four product records; processing/tile variants do not create four observation dates. |
| CMR RTC-S1 | Four locally intersecting burst records, with the relevant DSWx parent links and orbit59152. |

The nearest source remains:

`S1A_IW_GRDH_1SDV_20250511T220024_20250511T220049_059152_0756E5_4873`

The basin's clear14May02:48:57UTC optical view is about **52.81h after** the scene start. The runway's clear13May02:39:00UTC view is about **28.64h after**. The ledger retains offsets to the complete25s GRD interval as well as the GEE metadata timestamp, which has a degenerate time_end and an interior time anchor. Slight second-level differences from earlier offsets are timestamp-anchor differences, not changed reference dates. None affects the one-sided timing conclusion.

The search is wide enough to contain any closer record if present in these queried catalogues: any record outside the interval is at least165h from the basin reference or146h from the runway reference, already farther than the existing source. Repeating a wider version of this same nearest-time search cannot produce a closer timestamp outside the current interval. This is not proof that no mission observation exists in an excluded mode, uncatalogued holding or other archive; those would require explicit source/processing feasibility assessment rather than silent substitution.

## OPERA and spatial support

The queried T50MLB product has metadata footprint coverage of all four frozen90m support/position neighbourhoods. Its locally intersecting RTC parents match absolute orbit59152, supporting source-pass provenance. The three T50MLA records do not cover those full neighbourhoods, even where a larger RTC parent intersects one site. Product support and parent-scene extent must not be conflated.

A product-generation timestamp on13May2025orApril2026is not a new SAR observation on that date. Acquisition/parent times remain11May. No product mask, source pixel validity, ocean policy, WTR class, radiometric equivalence or classifier performance was assessed from this metadata. Those gates cannot be passed by footprint overlap alone.

Public CMR/ASF response bodies total **158,370bytes**; the GEE serialized metadata result is2,491bytes, not an exact HTTP-body measurement. These are covered by the retained metadata reserve; image transfer and previous cumulative reference charges were not reset. No source asset URL was followed. Five focused offline checks pass for temporal semantics, parent-file deduplication, search coverage, metadata-only operations and unchanged reference locks.

ASF query syntax was verified against its [official search manual](https://docs.asf.alaska.edu/api/keywords/). The actual availability conclusion comes from the saved bounded responses and reconciliation ledger, not a generic mission revisit claim.

## Scientific consequence

The useful optical observations and frozen interpretations stay intact. The two new inland/artificial cases remain E1for the May11SAR acquisition, with target-time possible water[0,1]; the earlier two controls remain explicitly conditional. No detector has failed or passed an accuracy test. Do not acquire another SAR scene, switch platform/radiometry, relabel May11from the later images, or rerun the same archive search to bypass this gap.

The remaining useful route is to seek **independent optical evidence before the actual11May22:00SAR pass at these same sites**, while retaining the existing after-date observations. Recommend one **metadata/access-only PlanetScope check for10-12May2025**, not another pixel order or source-tag-driven object sample. Exact490m AOIs and two query payloads are prepared locally in PLANET_METADATA_SEARCH_AOIS.geojson and PROPOSED_PLANET_METADATA_CHECK.json. Nothing was submitted to Planet.

The check should list all matching PSScene metadata for both frozen sites, prioritize the missing pre-target side independently of class or detector outcomes, retain inaccessible/absent/partial-coverage items, and inspect asset-specific historical permissions and published RGB/NIR/quality-mask support. Scene existence, access entitlement, local clarity, radiometry, quota and state transfer are separate questions. Do not initially hide inaccessible scenes with a permission filter or treat a cloud-percentage field as local clarity. No thumbnail, activation, order, download or saved-search notification is proposed.

The official [Planet item-search documentation](https://docs.planet.com/develop/apis/data/item-search/) distinguishes search metadata and per-item permissions; its [item/asset documentation](https://docs.planet.com/develop/apis/data/items/) warns that downloading consumes quota. Actual account terms/selected-asset charging still need verification before any data consumption. Previously reported browser/Education access is not treated as current asset-specific proof. No existing API key was found in the two checked environment-variable names or legacy configuration paths; browser access and other supported authentication routes were not inspected. This is not a claim that the account lacks access, and no new login or credentials were created/read.

If usable pre-target references exist and entitlement/costs are demonstrable, return with a bounded image-access proposal before consumption. If they do not, stop further automatic rescue and return a consequential choice between explicitly limited conditional falsification, a different reference design, or narrower scientific claims. Do not assume higher spatial resolution will solve missing observation time or event uncertainty.

The strongest objection is that further archive work could repeat the same cloud/timing failure while consuming account quota and favouring easy fair-weather cases. The proposed protection is a fixed two-site/three-day **metadata-only** inventory with no orders, explicit absent/inaccessible results and a stopping boundary. Even successful metadata is not reference adequacy. A separately sealed probability validation programme, current-date target, UNKNOWN/MIXED and the method-freeze block remain unchanged.
