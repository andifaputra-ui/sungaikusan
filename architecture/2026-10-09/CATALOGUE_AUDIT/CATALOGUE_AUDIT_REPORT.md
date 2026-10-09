# Acquisition catalogue identity audit — 9 October 2026

**SAVED_CATALOGUE_IDENTITIES_CROSSCHECKED; PROCESSABILITY_NOT_ESTABLISHED.** The 270 previously eligible acquisition instances remain unchanged. January 5, 2017 remains included with an explicit catalogue-footprint disagreement. No new dates or platforms were adopted.

## Identity and scope

The original `DETECTOR_VALIDATION_DESIGN/metadata_probe.py` queried EarthSearch for relative orbit 105, descending, IW, VV-present Sentinel-1 GRD items over the full L1 geographic envelope for 2017–2025. Its saved compact metadata retains full SAFE product names in asset paths even though the STAC item ID omits the final four-character product CRC. All nine yearly metadata hashes match the receipts in `REFERENCE_RESPONSE_STAGE1/ACQUISITION_FRAME.json`.

The 273 unique products form 271 acquisition instances. They are all **Sentinel-1A, IW, GRDH, VV+VH, relative orbit 105, descending**. The defensible instance key is spacecraft plus absolute orbit within this fixed mode/orbit/direction/product scope; datatake identifiers and all constituent product IDs remain attached. Adjacent slices on January 5 and January 29, 2017 each belong to one instance. No duplicate SAFE products or multiple CRC processing versions were found in the saved catalogue.

Two public official ASF metadata requests returned exactly these same 273 full SAFE product names, with all inspected mode/orbit/polarization/identity fields agreeing. The second request broadened `platform=Sentinel-1A` to `platform=Sentinel-1`; its response was byte-identical. This establishes agreement between the saved EarthSearch snapshot and the current ASF catalogue under these queries, not perfect knowledge of all mission holdings. In particular, the alias's inclusion of newly introduced platform codes was not independently certified. **The accepted S1A platform target is retained; this does not authorize S1B/S1C or another processing/radiometry route.**

| Year | Products | Instances | Legacy eligible |
|---|---:|---:|---:|
| 2017 | 32 | 30 | 29 |
| 2018 | 29 | 29 | 29 |
| 2019 | 30 | 30 | 30 |
| 2020 | 31 | 31 | 31 |
| 2021 | 29 | 29 | 29 |
| 2022 | 31 | 31 | 31 |
| 2023 | 30 | 30 | 30 |
| 2024 | 31 | 31 | 31 |
| 2025 | 30 | 30 | 30 |
| **Total** | **273** | **271** | **270** |

## Material support finding

The historical gate required the union of catalogue footprints to cover L1 to within fraction `1e-8`. Recalculation reproduces all original classifications, but the independent ASF geometries disagree for January 5, 2017:

- EarthSearch coverage: 1.0; adjacent source polygons overlap.
- ASF coverage: 0.9996366656; a narrow gap between adjacent slice polygons leaves about **0.4774 km²** of the 1,313.9038 km² L1 rectangle uncovered by those polygon approximations.
- ASF's two source polygons are about 10.14 m apart at their closest points. This is a metadata seam finding, **not measured invalid raster support**.

January 29, 2017 remains historically excluded: EarthSearch coverage 0.9996013763 and ASF 0.9996417621. Its catalogue gap likewise follows the adjacent-slice seam. This exclusion is explicitly documented as a legacy population restriction; it is not evidence of no water or proof that the underlying source pixels are unusable. Changing that date population is outside this audit.

**Do not remove January 5 to manufacture complete support.** Retain its identity, flag the disagreement, and carry future actual processed validity separately; missing current support must yield abstention/UNKNOWN. A catalogue footprint cannot replace the accepted full-source, precise-orbit write/read processing and validity checks. No SAR pixels were inspected and no source was processed here.

## Timing and provenance omissions

Exact fractional-second start/end UTC times are retained. All acquisitions occur late UTC evening and on the following calendar day in Asia/Makassar. Historical date labels are UTC labels; future optical/event comparisons must use timestamps, not assume that the displayed local date is the same.

Three approximately 24-day catalogue gaps occur: January 5–29, 2017; August 16–September 9, 2018; and October 23–November 16, 2021. They are gaps in both matching catalogue inventories; absence of an indexed product does not establish a dry state or mission non-acquisition.

ASF records 20 PGE/IPF version values spanning `002.72` to `004.02`. They are preserved product provenance, not proof of per-date processing comparability. Precise orbit availability, per-date materialized orbit provenance, source download checksum verification, actual support and SNAP success remain unassessed for unprocessed dates. The archive byte fields sum to 290,854,801,188 bytes (270.88 GiB) across all 273 products; this is a metadata total, not an approved download or a peak working-storage estimate.

## Files and verification

- `ELIGIBLE_ACQUISITION_INSTANCES.json`: unchanged 270-instance operational list with stable IDs, constituent SAFE names, UTC/local dates and both coverage values.
- `ACQUISITION_INSTANCE_REGISTER.json`: all 271 instances, including the historical exclusion.
- `PRODUCT_IDENTITY_REGISTER.json`: all 273 products with full IDs, datatakes, checks, metadata footprints and product provenance.
- `AUDIT_SUMMARY.json`, `FOOTPRINT_BOUNDARY_DIAGNOSTIC.json`, `CATALOGUE_GAPS.json`: machine-readable findings.
- `INPUT_HASHES.json`: source hash receipts.
- `AUDIT_TESTS.json`: **8 passed checks**, including synthetic duplicate-CRC/adjacent-slice grouping and separation of different spacecraft/orbits.
- `NETWORK_LEDGER.json` and `PLATFORM_SCOPE_NETWORK_LEDGER.json`: 2 scripted requests, **1,401,360 response-body bytes**, no assets/authentication; below 20 requests / 8 MiB. One documentation web search is additional unmetered documentation traffic, not imagery transfer.

The reproducible audit reads metadata only. No source files were altered, no seed/sample was generated, no optical census was repeated, and no images or asset URLs were opened. No further catalogue queries are needed for this bounded audit.

## Official API documentation

[ASF search keywords and endpoint documentation](https://docs.asf.alaska.edu/api/keywords/) supports the query fields and GeoJSON catalogue response. The two exact URLs, parameters, retrieval times and hashes are in the request ledgers. The original source scripts and hashes establish the historical EarthSearch query lineage; no undocumented catalogue expansion was made.
