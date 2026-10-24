# One-scene native S1-only smoke: completed findings

24 October 2026. **TECHNICAL_SMOKE_PASS; SCIENTIFIC_PERFORMANCE_UNKNOWN.** The approved experiment is complete. No further scientific job is queued. Recommend proceeding to a linked independent development comparison, subject to its separate scope/semantic-evaluation decision in `NEXT_DECISION.md`.

## What passed

The exact frozen S1-only model ran on the frozen 1 September 2024 scene and central 512 by 512 patch. Current VV/VH sigma0 dB and provider angle were supplied in the declared order, using exact released normalization. The native Earth Engine input remains a separately versioned experimental pipeline; equivalence with the accepted SNAP/C1 products was neither assumed nor tested.

| Check | Observed result |
|---|---|
| Frozen checkpoint and normalization | Exact byte counts and SHA256 identities verified |
| State loading | Strict architecture/state match; restricted `weights_only=True` loading succeeded |
| Current support | 262,144 / 262,144 pixels jointly valid in VV, VH and angle |
| Output | 512 by 512 float scores, finite and within [0,1] on supported cells |
| Score range | Approximately 0.00000657 to 0.996833; these are unvalidated scores |
| Geometry | Exact EPSG:32750 affine, size and common coordinate anchors preserved |
| Four-flip model computation | 46.094 seconds, CPU with four threads |
| Timer inside inference script | 281.375 seconds |
| Controller inference-stage span | 510.092 seconds, about 8 minutes 30 seconds |
| Charged cumulative response-body transfer | 969,932,800 bytes, about 0.903 GiB, below 2 GiB |
| Runtime plus run artifacts at final audit | 4,893,588,289 bytes, about 4.558 GiB, below 6 GiB |
| Peak RAM | Not measured |

The three timing figures have different boundaries. The difference between controller span and the internal timer was not separately instrumented; it must not be silently assigned to model computation. This one patch does not justify a whole-scene or 2017–2025 runtime extrapolation. Storage is a file-byte snapshot including the isolated environment and retained wheels, not a RAM measurement.

`COMPLETION_AUDIT.json` records the integrity, grid, support and resource checks. All 30 files in the original readiness manifest remain unchanged. The transfer ledger distinguishes measured response bodies from conservative reservations, includes an 8 MiB reserve for small unmetered metadata/API responses, and excludes headers/TLS overhead. No paid imagery or Planet quota was used.

## What visual QA can establish

The fixed full-patch and central-crop panels were rendered and inspected. At full-patch scale there is no obvious rotation or gross source-relative displacement. The score field varies spatially; its appearance does not supply reference truth. The fixed central crop is nearly uniform in score and cannot establish fine boundary alignment. No more attractive crop was substituted to improve that conclusion.

Exact copied grids, common anchors and source/score co-location do **not** independently measure absolute geolocation. No optical/control-point registration or semantic correctness was established. `VISUAL_QA_REVIEW.json` records this limited engineering inspection. The local figure `ALIGNMENT_QA_TWO_SCALES.png` is excluded from the public text/code backup.

## Limits that remain material

- This patch contains no missing current pixels. Consequently it did not empirically exercise real nodata propagation; synthetic input safeguards are separate evidence. Convolution may transmit missing or edge-context effects to otherwise supported neighbours. The distance diagnostic has no tuned reliability cutoff.
- Provider-valid support does not establish physical reliability. The observed VH minimum was about -48.75 dB and the VV maximum about +12.85 dB. Values were retained under the frozen native-input contract; display clipping did not censor model inputs. No extreme-backscatter value was declared water or physically reliable. Existing Phase 2.4 safeguards remain relevant to any later interpretation.
- The score is neither a calibrated local probability nor a fractional water-area estimate. No threshold, binary water map, reference response, accuracy statistic or winning method was produced.
- The declared training-centre audit found no centre inside L1, but incomplete supplemental boundaries and broader training/weak-label exposure prevent a complete geographic-independence claim. The model was not retrained or fine-tuned.
- Performance on ordinary land, artificial dark surfaces, persistent water, genuinely new/receding water, boundaries, poor support and earlier years remains unmeasured. The attractive appearance of any curving high-score feature cannot resolve those questions.
- The annual-context model and native int8 embedding route were not qualified by this test. Do not substitute GEE floating embeddings or introduce GHSL/L-band automatically.

## Failures retained, not hidden

Two acquisition-wrapper defects occurred before neural inference. Attempt 1 set the EE deadline before session initialization. Attempt 2 downloaded the input successfully after all three native-window guards, then failed to serialize a request dictionary mutated by `getDownloadURL`. Both attempts and logs are retained. Call order and defensive-copy fixes each passed two offline regression tests. The second receipt was recovered from its pre-mutation saved request and original downloaded file, without another imagery request or budget reset. The controller verified that input before the single actual inference. See `CONTINUATION_REPAIR.json` and `RECEIPT_RECOVERY.json`.

The final audit emitted the previously observed GDAL resource-path warning but completed its numerical checks. Its launcher now explicitly supplies the existing GDAL/PROJ paths for future audits; no environment upgrade or inference rerun was made. Original `SMOKE_RESULT.json` remains the run receipt, including its then-pending visual-QA note; the separate QA review records completion without rewriting that receipt.

## Scientific conclusion

**The new evidence is positive for local executability only.** The richer current-S1 model is technically available on this computer, using traceable input, support and release artifacts within the approved resources. It is still neutral regarding the scientific water-detection hypothesis. The bottleneck has moved from "can this frozen pipeline run?" to "does independent acquisition-time evidence distinguish useful detection from plausible-looking mistakes?"

Stop this technical branch here. Do not run additional dates, a context arm, old VV A/B, semantic evaluation, final-validation release or full-series processing automatically. The next proposed decision is in `NEXT_DECISION.md`; final method freeze remains blocked.
