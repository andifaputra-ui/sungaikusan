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
              'requirements_lock.txt','WHEEL_RECEIPTS.json','render_alignment_qa.py']}
    for source,names in allowlists.items():
        destination=REPO/'architecture'/('2026-10-23-readiness' if source==PREP else '2026-10-24-smoke')
        destination.mkdir(parents=True,exist_ok=True)
        for name in names:
            path=source/name
            if not path.is_file():
                raise FileNotFoundError(path)
            shutil.copyfile(path,destination/name)
    checkpoint='''# Approved technical smoke — 24 October 2026

The user approved one isolated CPU S1-only technical test. Read architecture/2026-10-24-smoke/RUN_SCOPE.md and architecture/2026-10-23-readiness/SMOKE_TEST_PROTOCOL.md. Isolated setup and verified weight downloads completed. Two acquisition-wrapper defects were preserved and repaired: initialization before deadline configuration, and defensive copying of EE download parameters. The downloaded input was recovered without a second imagery request. At this backup snapshot one CPU inference is running; this repository does not assert a completed result. Current execution status and pixels remain local. No final detector, accuracy claim or method freeze is authorized.

The frozen package's 30 hashes were verified; its ten synthetic input tests remain recorded. Three resource-accounting, two initialization-order and two mutable-request regression tests pass offline. All three live native-window checks passed before the one imagery request. The original input file is retained unchanged. Separate two-scale QA code is prepared but not asserted executed in this snapshot.

Permanent development engineering only. Separate runtime on E:, 2 GiB response-body transfer accounting ceiling and 6 GiB storage ceiling, no paid/Planet use. Accepted scientific environment, SNAP/C1 products, original responses and sealed final reference evidence are preserved. Model weights, research pixels, raw public training geography, third-party trainer code, live logs, account data and reader identities are excluded from this curated backup.

Resume by checking local NATIVE_MODEL_SMOKE_20261024/STATUS.json and the terminal result marker once. Do not relaunch setup/controller or download duplicates automatically. A successful run still requires two-scale visual QA and scientific review of the next comparison; a failure is retained rather than repaired into a positive finding.
'''
    (REPO/'CHECKPOINT.md').write_text(checkpoint,encoding='utf-8')
    readme=REPO/'README.md'
    text=readme.read_text(encoding='utf-8')
    prefix='Latest execution boundary, 24 October 2026: the one-scene [technical smoke](architecture/2026-10-24-smoke/RUN_SCOPE.md) is approved and launched locally. See [checkpoint](CHECKPOINT.md). This snapshot does not claim that inference has finished.\n\n'
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
