# Native-model readiness findings

23 October 2026. **Reversible readiness work is complete. One current-Sentinel-1 model smoke test is now concrete; model execution and the larger comparison remain unperformed.**

## What the checks established

- GitHub source is pinned to commit `9548384d8744beda3f3ed3a1a96183260b2caa93`. Six fetched text/metadata files match their provider Git blob identities after line-ending normalization. No upstream source was imported or executed.
- The live Hugging Face release resolves to `7c497187a9b7f53488e6577621e7d0961c23dcfd`. Its weight/normalization metadata agrees with all four expected hashes for the matched S1-only and current-year-context variants. Use immutable commit and hashes, not the movable tag alone. Weight payloads have not been fetched or verified locally.
- The exact frozen release trainer's raw SHA1 is `cd991e7424ae8d74c4737bd339f1ca66e563e506`, matching the author's documentation. Its different Git blob identity is not a trainer mismatch: raw-file SHA1 and Git blob SHA1 hash different byte sequences.
- The S1-only checkpoint plus normalization require165,059,495 bytes (about157.4MiB). Both primary variants together require330,577,359 bytes (about315.3MiB), excluding environment packages and imagery. Do not download all variants by default.
- The public training metadata contains5,278 unique sample centres:4,678 river entries and600 open-water supplements, split4,222 train/1,056 validation. No declared centre is inside L1. The nearest locally shortlisted centre is87.8km from L1; its reconstructed river tile is82.6km away. A second nearby supplement centre is239.6km away, but supplement raster boundaries are not published. This is qualified evidence against direct local label overlap, not proof that all model inputs/pretraining are independent of Kusan.
- A metadata-only query confirms one appropriate native S1 scene on1September2024, descending relative orbit105, absolute orbit55477, with VV/VH/angle and a catalogue footprint containing the fixed test patch. This is source availability, not valid pixels or optical reference truth.
- The scientific environment lacks torch, torchvision, fastai and huggingface-hub. It was only queried via package metadata and was not changed. A separate inference environment would be needed.

## Issues found and addressed in preparation

**Per-band current support.** The upstream reader uses Rasterio `dataset_mask()`. A synthetic three-band memory raster demonstrated that its union mask can remain valid when one required band is nodata. The new pure-array guard requires the intersection of explicit VV/VH/angle validity and finite values. Missing current data cannot be supplied by valid annual context. This is a possible failure mode, not an observed count of affected research pixels.

**Checkpoint statistics.** The upstream loader substitutes1 for nonpositive standard deviations. The new guard rejects invalid or nonfinite checkpoint statistics rather than silently changing normalization. No downloaded statistics were found defective: their payload has not been read.

**Windows and source scale.** The training-sample reconstruction helper imports Unix `fcntl` and expects a global AEF index larger than100MB. Do not run it unchanged on this Windows machine. The first S1-only smoke test avoids that index and annual-context dependency. A fused test still needs a bounded native-int8 retrieval route or independently verified encoding conversion; GEE floating-point embeddings are not silently substituted.

**Band geometry.** VV and VH declare10m source grids in EPSG32750. The angle band declares a much coarser rotated affine. Stacking it on a10m output grid does not create10m incidence-angle information. Preserve the source projections and use the pinned model's preprocessing semantics; do not replace the angle with a terrain/local-incidence product.

**No unnecessary backbone download.** The examined inference builder already sets `pretrained=False` and local-only configuration before strict checkpoint loading. There is no need to fetch separate ImageNet encoder weights merely to instantiate this released model.

Ten synthetic input-contract tests pass, including partial-band nodata, missing-current/context behavior, float-embedding rejection, invalid normalization and shifted output grid. The memory-raster test emitted a missing GDAL_DATA resource warning but passed; the future launcher must set the existing documented GDAL/PROJ paths. These are software checks, not water-detection performance results.

## Exact next experiment

Read `SMOKE_TEST_PROTOCOL.md` and `PROPOSED_SMOKE_INPUT_FREEZE.json`. The first test is deliberately one frozen current-only model, one native scene and one512×512 patch, with probability output and support diagnostics. It requires a separate CPU runtime, the157.4MiB model bundle and a small new native input extraction. It neither trains the model nor supplies reference labels. The proposed paired/OPERA scientific comparison follows only after input/runtime qualification and independently useful reference evidence.

The readiness work did not access research pixels, final references, response CSVs or the old nine-conflict queue. It did not download weights, install packages, train, run inference or alter accepted SNAP products. No scientific background job remains.

## Consequential decision

The question is now specific: authorize the single-scene native-input technical smoke test and its isolated runtime/resource envelope. This is the new processing/inference boundary identified in `METHOD_REASSESSMENT_20261023/METHOD_DIRECTION.md`; the earlier design-only reassessment did not execute it. The proposed cap is2GiB cumulative setup/artifact/input transfer and6GiB new storage, all onE:, zero paid data/Planet quota. Exceeding that cap or requiring a different processing contract returns a concrete failure rather than an automatic larger installation.

If the test passes, the result is a runnable engineering branch. Kusan accuracy, the annual-context contribution, full-series applicability and final method choice remain scientific questions for the linked reference comparison.
