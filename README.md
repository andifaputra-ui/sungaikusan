# Kusan C2 research architecture backup

This is a **curated scientific-work backup**, not a full copy of the thesis datasets.

Current status: the [8 October architecture](architecture/2026-10-08/ARCHITECTURE_DECISION_FOR_REVIEW.md) was approved on 9 October, with detector-informed/adversarial discovery allowed during development only. References remain independently interpreted and permanently development-only.

Read the [implementation findings](architecture/2026-10-09/IMPLEMENTATION_FINDINGS.md), [development evidence plan](architecture/2026-10-09/DEVELOPMENT_EVIDENCE_PLAN.md), and [continuation checkpoint](CHECKPOINT.md). No new probability sample, semantic A/B run, evaluation SAR, final reference release or method freeze occurred. The proposed acquisition budget is not automatically authorized.

## Reproduce the software checks

The October 8 arithmetic checks require Python standard library:

```
python architecture/2026-10-08/architecture_checks.py
python architecture/2026-10-08/synthetic_strata_checks.py
python architecture/2026-10-08/interval_accounting_checks.py
```

The October 9 role and display tests require NumPy and Shapely (already installed in the project scientific environment):

```
python architecture/2026-10-09/ROLE_GUARD/test_role_guard.py
python architecture/2026-10-09/OPTICAL_CONTRACT/test_optical_display_contract.py
```

These test synthetic cases without imagery, real randomization or classifier output. Results do not establish scientific accuracy, calibration, independent human reliability or reference adequacy. Saved-chip/catalogue audit scripts require local authoritative inputs, intentionally excluded from this repository.

## Scope

Included: approved design, implementation reports, pure policy/display code, synthetic tests/results, aggregate findings and continuation records. Exact copied-file hashes are in BACKUP_MANIFEST.json.

Excluded: imagery, source rasters/vectors, detailed reference/discovery records, sealed final evidence, reader returns and identities, credentials, raw account/browser receipts and installations. Authoritative scientific data remain in the local thesis workspace. No source result or original response is overwritten by this backup.
