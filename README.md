# Kusan C2 research architecture backup

This is a **curated scientific-work backup**, not a full copy of the thesis datasets.

Current review package: [Architecture decision, 8 October 2026](architecture/2026-10-08/ARCHITECTURE_DECISION_FOR_REVIEW.md).

Short version: [Review summary](architecture/2026-10-08/REVIEW_SUMMARY.md).

The proposal separates evidence-first development falsification from a separately sealed probability audit of a locked retrospective reconstruction. It explicitly distinguishes fixed-map accuracy from transfer to untouched geography. The architecture awaits human approval; no new sample, imagery acquisition, detector evaluation or method freeze is authorized by these files.

## Reproduce the synthetic checks

Python3 standard library is sufficient:

```text
python architecture/2026-10-08/architecture_checks.py
python architecture/2026-10-08/synthetic_strata_checks.py
python architecture/2026-10-08/interval_accounting_checks.py
```

These enumerate artificial cases exactly. They create no random seed, research sample or detector predictions and read no imagery. On this backup, aggregate metadata in `ARCHITECTURE_INPUT_METADATA.json` substitutes for the local project's original metadata. Existing result files are checked rather than overwritten.

The source hashes record the local inputs used; the underlying protected datasets are intentionally absent. Synthetic checks establish arithmetic/accounting correctness, not reference adequacy or detector accuracy.

## Scope

Included: architecture documents, independent supporting analyses, aggregate metadata, synthetic scripts/results, preservation summary and continuation checkpoint. Exact copied-file hashes are in [BACKUP_MANIFEST.json](BACKUP_MANIFEST.json).

Excluded: imagery, scientific source datasets, raw reference labels and reader returns, sealed final evidence, credentials, raw account/browser receipts and installed applications. Authoritative SNAP/Python products and historical records remain in the local thesis workspace unchanged.
