"""Stage an explicit public-safe source/protocol allowlist; never imagery or logs."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
PREP=ROOT.parent/'NATIVE_MODEL_READINESS_20261023'
REPO=Path('E:/Bendungan_Kusan/GitHub_Backup/kusan')


def main() -> None:
    """Preserve old backups and add only our own code, aggregate QA and protocols."""
    allowlists={
        PREP:['READINESS_FINDINGS.md','SMOKE_TEST_PROTOCOL.md','FROZEN_ARTIFACT_CONTRACT.json',
              'PROPOSED_SMOKE_INPUT_FREEZE.json','TRAINING_GEOGRAPHY_AUDIT.json',
              'TRAINING_GRID_EXTENT_SANITY.json','UPSTREAM_IDENTITY_CHECK.json',
              'input_contract.py','test_input_contract.py','INPUT_CONTRACT_TEST_RESULTS.json'],
        ROOT:['AUTHORIZATION.json','RUN_SCOPE.md','resource_budget.py','metered_pip.py',
              'prepare_runtime.py','acquire_input.py','run_inference.py','continue_after_setup.py',
              'test_resource_budget.py','RESOURCE_TESTS.json','SOURCE_SCOPE_OFFLINE_CHECK.json',
              'requirements_roots.txt','prepare_public_backup.py','test_initialization_order.py',
              'INITIALIZATION_REGRESSION_TESTS.json','test_request_mutation.py','REQUEST_MUTATION_TESTS.json',
              'CONTINUATION_REPAIR.json','RECEIPT_RECOVERY.json','RUNTIME_READY.json',
              'requirements_lock.txt','WHEEL_RECEIPTS.json','render_alignment_qa.py',
              'SMOKE_RESULT.json','COMPLETION_AUDIT.json','VISUAL_QA_REVIEW.json',
              'FINDINGS_FOR_REVIEW.md','NEXT_DECISION.md','audit_completion.py','finalize_handoff.py']}
    for source,names in allowlists.items():
        destination=REPO/'architecture'/('2026-10-23-readiness' if source==PREP else '2026-10-24-smoke')
        destination.mkdir(parents=True,exist_ok=True)
        for name in names:
            path=source/name
            if not path.is_file():
                raise FileNotFoundError(path)
            shutil.copyfile(path,destination/name)
    checkpoint='''# Approved technical smoke — 24 October 2026

The approved one-scene smoke is COMPLETE: TECHNICAL_SMOKE_PASS; SCIENTIFIC_PERFORMANCE_UNKNOWN. Read architecture/2026-10-24-smoke/FINDINGS_FOR_REVIEW.md and NEXT_DECISION.md. All 262,144 pixels had current VV/VH/angle support; exact grid, release hashes, strict state loading and finite scores passed. Four-flip CPU computation46.094seconds, internal script281.375seconds, controller stage510.092seconds. Actual audited storage4.558GiB and charged transfer0.903GiB were within6/2GiB ceilings. No scientific job remains queued.

Two acquisition-wrapper defects were preserved and repaired; one original input was retained without a second imagery request. The two fixed QA views were inspected. No gross source-relative displacement was apparent, but the nearly uniform central score crop cannot establish fine boundary alignment. Absolute geographic accuracy and water accuracy remain unmeasured. No final detector, semantic comparison or method freeze is authorized.

The frozen package's 30 hashes were verified; its ten synthetic input tests remain recorded. Three resource-accounting, two initialization-order and two mutable-request regression tests pass offline. All three live native-window checks passed before the one imagery request. Source pixels, weights and the local QA figure remain excluded from this public backup. The real patch has no missing current pixels; synthetic nodata checks are separate evidence and do not become empirical validation.

Permanent development engineering only. Separate runtime on E:, 2 GiB response-body transfer accounting ceiling and 6 GiB storage ceiling, no paid/Planet use. Accepted scientific environment, SNAP/C1 products, original responses and sealed final reference evidence are preserved. Model weights, research pixels, raw public training geography, third-party trainer code, live logs, account data and reader identities are excluded from this curated backup.

Resume at the scientific decision in NEXT_DECISION.md. Recommended next is a reference-linked development comparison of frozen S1-only and operational OPERA where actual observations can be paired; the unqualified annual-context arm is not a prerequisite. No new imagery acquisition, inference dates, thresholds, old VV A/B, final evidence or method freeze starts automatically. Do not relaunch the completed setup/controller.
'''
    (REPO/'CHECKPOINT.md').write_text(checkpoint,encoding='utf-8')
    readme=REPO/'README.md'
    text=readme.read_text(encoding='utf-8')
    obsolete='Latest execution boundary, 24 October 2026: the one-scene [technical smoke](architecture/2026-10-24-smoke/RUN_SCOPE.md) is approved and launched locally. See [checkpoint](CHECKPOINT.md). This snapshot does not claim that inference has finished.\n\n'
    text=text.replace(obsolete,'')
    prefix='Latest result, 24 October 2026: [native S1-only technical smoke passed](architecture/2026-10-24-smoke/FINDINGS_FOR_REVIEW.md). Scientific performance remains unknown. No background job is queued. Read the [next decision](architecture/2026-10-24-smoke/NEXT_DECISION.md) and [checkpoint](CHECKPOINT.md).\n\n'
    if prefix not in text:
        first,rest=text.split('\n\n',1)
        readme.write_text(first+'\n\n'+prefix+rest,encoding='utf-8')
    manifest=json.loads((REPO/'BACKUP_MANIFEST.json').read_text(encoding='utf-8'))
    manifest.update(date_local='2026-10-24',scope='Curated architecture, reassessment, native readiness and approved smoke source/protocol snapshot')
    manifest['files']=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,
        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((REPO/'architecture').rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts]
    (REPO/'BACKUP_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    assert all(hashlib.sha256((REPO/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in manifest['files'])
    print('CURATED_ARTIFACTS_VERIFIED',len(manifest['files']))


if __name__=='__main__':
    main()
