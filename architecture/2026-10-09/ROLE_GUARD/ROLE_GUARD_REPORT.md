# Role guard implementation — 9 October 2026

**Implemented and tested offline; not a production access-control system or an acquisition authorization.** This directory contains only new policy code, synthetic tests and their results. No source pixels, response CSVs, sealed references or existing exposure records were read or changed. Existing acquisition/native-window guards remain unchanged.

## Approved amendment represented

Detector-informed or A/B-disagreement discovery is allowed during development. This selects where to look; it does not supply the reference response. Its artifacts receive permanent development taint. A reference artifact additionally requires independent measurement and acquisition metadata. Derived artifacts preserve parent identities and taint. Neither renaming a development artifact nor deriving an intermediate product can promote it to final reference.

This does not permit detector information in a reader packet or make purposively selected cases a probability sample. It does not authorize running A/B or ordering/downloading evidence.

## Implemented roles

| Artifact / actor | Policy boundary |
|---|---|
| Whole-population acquisition metadata and approved sampling/discovery auxiliaries | Developer/custodian context permitted; neither establishes acquisition-time reference truth. Pixel access still needs its own artifact-bound role scope and operation record. |
| Development engineering and reference artifacts | Development use; detector-informed discovery permitted; independent response requirement remains. All derived evidence remains development-only. |
| Final reference | Explicit matching candidate/protocol lock and reference release required. Developer access rejected. A blinded reader sees only a validated packet; a custodian manages separation. |
| Final predictions | Custodian access requires the evaluation lock plus separate matching processing/stratification authorization, **not** reference release. This permits map construction and strata formation before drawing/reference opening. Final analyst joining additionally requires reference release, response lock and analysis release. Never reader packet material. |
| Final response/prediction join | Response lock and separate analysis release required in addition to candidate lock and reference release. A retired test is rejected as a fresh test of a changed candidate. |

The policy does **not** globally blacklist old geographic blocks. New architecture permits fixed-map population inference over previously exposed geography when a later authorized sample selects it; the exposure history remains reportable. This does not make old geography untouched. Reusing an original development response as the final answer is blocked. A genuinely fresh, blind measurement at the same geography must be registered as a new artifact by the custodian and disclose the geographical exposure history; it cannot be manufactured by stripping parent taint.

## Blind-packet boundary

`validate_blinded_packet` accepts only neutral aliases, response geometry/CRS, the registered 10/30/50 m support, target acquisition time, protocol version, and optical images with acquisition/sensor/native-support/display/registration metadata. Image paths are neutral relative paths such as `images/R01_optical.png`.

The structured schema rejects detector values, candidate IDs, sampling strata, discovery reasons, hidden keys, first-reader answers and any other unapproved field, including nested fields. This is intentionally an allowlist. A future justified packet field needs an explicit schema update rather than silently passing through a free-form dictionary. The function validates field structure, not the scientific truth of its contents or whether rendered image text encodes an answer. Independent package QA must inspect image annotations, content, identifiers and display pipeline provenance. No research image was opened to perform that QA in this task.

## Native-window safeguard

`check_native_window` performs the following before any caller may open/read pixels:

1. Validate artifact/actor role and, for final evidence, lock/release state.
2. Require a separate operation-authorization record and bind the scope to an exact artifact and role.
3. Require matching CRS, a valid nonsingular source affine transform and known dimensions.
4. Round source-grid window edges outward; add every specified resampling halo and padding pixel.
5. Convert the complete expanded source window to a polygon, including rotated grids.
6. Require its coverage by the approved role-specific geometry and no intersection with an explicitly prohibited geometry, including boundary contact.

The result records the exact native window to be read. It never silently crops it to fit, reprojects it, or converts a failed request into a permitted one. A full-population ancillary scope cannot authorize a development-reference or engineering file. Metadata cannot request pixels. Holes are respected; bounding-box overlap alone is insufficient. The actual IO code must use the checked window and declared full halo/padding. Boundless reads, additional resampling and hidden decoder overreads are not assessed by this standalone checker.

Production integration remains required. The caller must resolve source metadata without unguarded pixel access, load a trusted role manifest, record the scope/transform and expanded window, invoke this check **before** opening pixel-bearing assets, and ensure no downstream reader expands the read again. Provider/archive file formats may require whole-file transfer; this local window check does not pretend to prevent that transfer. Such a source needs a separately authorized whole-file role scope or a provider-side safe delivery route.

The synthetic edge regression reconstructs the failure mechanism: an intended footprint ending at native column49.8 is rounded to50 and padded to51, crossing a protected boundary at column50. The fake reader is never called. This reproduces the rounding/padding mechanism, not unrecorded exact source coordinates from the historical incident.

## Exposure history

Exposure events are immutable dataclasses, appended to an ordered tuple. Extension verification rejects removal, change or duplicate event IDs. A `UNVIEWED_EXTENT_UNKNOWN` event cannot be overwritten by `CLEARED`; additional evidence is a separate linked observation. This task creates no real event and clears no historical incident. The Oct5 incidental binary and Oct8 possible auto-preview retain their previously recorded unknown status.

## Verification and limits

`test_role_guard.py` contains 59 synthetic test methods, including eight separately exercised prohibited packet fields. They test positive permitted paths and negative paths; their passing status does not demonstrate production enforcement or scientific reference adequacy. See `SYNTHETIC_ROLE_GUARD_RESULTS.json` for the executed result.

Independent functional inspection caught and corrected an initial ordering error: the first implementation incorrectly required reference release for custodian access to locked predictions. The amended checker now separates evaluation lock, prediction-processing authorization, reference release and response/join release. Regression tests verify that prediction construction can proceed while final references remain sealed, and that analysis joins cannot use that earlier permission.

Run with the existing scientific Python, without installation:

```powershell
& 'E:/Bendungan_Kusan/Miniforge/envs/kusan-c1/python.exe' -X utf8 'E:/Bendungan_Kusan/Thesis_Project/Check_point_2/DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD/test_role_guard.py'
```

The checker is deliberately honest about trust: actors, provenance, parent lists, independent-measurement claims, locks and authorization IDs are asserted by a surrounding workflow. A caller that fabricates or omits these can defeat the policy. Hash-looking strings are not verified signatures. Folder separation does not establish an independent interpreter. No actual candidate lock, final release, pixel-access grant, random seed, sample, network request or research evidence is created here. Integration and audit remain necessary before any operational use.
