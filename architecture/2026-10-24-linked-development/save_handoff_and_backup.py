"""Save a resumable local checkpoint and an explicit public-safe backup allowlist."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
HISTORY=ROOT.parent.parent/'Gpt_6_Astra_historical_reasoning'
REPO=Path('E:/Bendungan_Kusan/GitHub_Backup/kusan')


def main() -> None:
    """Preserve earlier history; copy only code, protocols and aggregate findings."""
    now=datetime.now(timezone.utc).isoformat()
    sources=['acquire_frozen_references.py','run_reference_batch.py','test_reference_preread.py',
        'SCOPE.json','REFERENCE_EXECUTION_PROTOCOL.md','CURRENT_FINDINGS.md',
        'REFERENCE_SOURCE_AMENDMENT_01.json','REFERENCE_PANEL_FREEZE.sha256',
        'REFERENCE_SOURCE_PLAN_V2.sha256','save_handoff_and_backup.py']
    hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources}
    (ROOT/'EXECUTION_SOURCE_HASHES.json').write_text(json.dumps({'utc':now,'files':hashes},indent=2)+'\n',encoding='utf-8')
    (ROOT/'OFFLINE_TEST_RESULTS.json').write_text(json.dumps({'utc':now,'tests':3,'failures':0,
        'execution':'python -X utf8 test_reference_preread.py',
        'pixel_access':False,'limitations':'Synthetic CRS/window and immutable plan accounting only; not provider geolocation or semantic validation.'},indent=2)+'\n',encoding='utf-8')
    checkpoint='''# Linked development reference acquisition — 24 October 2026

The latest continuation advances the proposed linked S1-only/OPERA development block. Read Check_point_2/LINKED_DEVELOPMENT_COMPARISON_20261024/CURRENT_FINDINGS.md and REFERENCE_EXECUTION_PROTOCOL.md, then STATUS.json once. The completed native smoke must not be relaunched.

Twelve locations and 24 date-supports are frozen. Before pixels, the transparent dual-source amendment froze Sentinel-2 and Landsat nearest-before/after opportunities: 96 slots, 78 metadata opportunities, 18 absent, 20 unique items. No cloud/water/model ranking or replacements. Three offline pre-read/immutability tests pass. Actual classes, support quality and transferability are unknown.

One hidden reference acquisition supervisor PID21828 launched 2026-10-24 23:26:33 Makassar /15:26:33UTC. Worker cap60minutes: it will complete or stop by approximately 2026-10-25 00:26:35Makassar, subject to normal termination latency. No automatic follow-on model inference, water labeling or comparison. Internet/awake PC needed. Preserve partial files, charges and failures; never relaunch just because chat ended. If still active on continue, report phase and leave it running. Inspect STOP/summary/logs only if finished or stopped.

Additional transfer/storage ceilings are1GiB each, metadata charged with64MiB reserve. Prior smoke0.903GiB transfer/4.558GiB storage is separate. Same scientific environment retained, zero paid/Planet use. No old VV A/B, training, final sample/reference release, full series or method freeze.

Metadata supports same-pass RTC/native S1 orbit matching; canonical OPERA generation and per-location support remain gates. Native GEE time_end is degenerate in all5records; preserve filename intervals. Original slow metadata lookup was stopped and one indexed bounded retry succeeded; cause unisolated. All evidence and failures retained. OSM current geography is auxiliary, never2025 class truth. Source raw geography, fixed panel detailed coordinates/metadata and optical pixels remain local.

Next after acquisition: technical/display/radiometry QA and independently derived optical interval responses, separate spatial/time uncertainty, no prediction join before the protocol and reference adequacy pass. Keep30m primary/10&50m sensitivities and UNKNOWN/MIXED. Do not import old responses or treat model/OPERA/OSM as truth. Reference inadequacy triggers a meaningful decision, not automatic rescue.
'''
    target=HISTORY/'LINKED_DEVELOPMENT_REFERENCE_BACKGROUND_20261024.md'
    target.write_text(checkpoint,encoding='utf-8')
    start=HISTORY/'START_HERE.md'
    header='''# Latest: linked development reference acquisition running — 2026-10-24

Read LINKED_DEVELOPMENT_REFERENCE_BACKGROUND_20261024.md, then the linked package STATUS.json once. Frozen12locations/24date-supports; Sentinel-2/Landsat plan96slots,78opportunities,18absent. Hidden supervisor21828 started23:26Makassar with60-minute limit, no follow-on inference. Additional1GiB transfer/storage limits; prior smoke unchanged. Leave it running if active. No semantic join, A/B, final reference or method freeze. Exact source/time/OPERA generation cautions and3passing guard tests documented. This entry supersedes older no-job status for the completed smoke, not its technical findings.

---

'''
    old=start.read_text(encoding='utf-8')
    if not old.startswith(header):
        start.write_text(header+old,encoding='utf-8')
    destination=REPO/'architecture/2026-10-24-linked-development'
    destination.mkdir(parents=True,exist_ok=True)
    for name in sources+['EXECUTION_SOURCE_HASHES.json','OFFLINE_TEST_RESULTS.json']:
        shutil.copyfile(ROOT/name,destination/name)
    (REPO/'CHECKPOINT.md').write_text(checkpoint,encoding='utf-8')
    readme=REPO/'README.md'
    text=readme.read_text(encoding='utf-8')
    first,rest=text.split('\n\n',1)
    prefix='Latest continuation: [linked development reference acquisition](architecture/2026-10-24-linked-development/CURRENT_FINDINGS.md) launched locally within frozen limits. See [checkpoint](CHECKPOINT.md); earlier technical-smoke no-job statements describe that completed job, not the new reference worker. No semantic comparison or final method release.\n\n'
    if prefix not in text:
        readme.write_text(first+'\n\n'+prefix+rest,encoding='utf-8')
    manifest=json.loads((REPO/'BACKUP_MANIFEST.json').read_text(encoding='utf-8'))
    manifest.update(date_local='2026-10-24',scope='Curated source/protocol/aggregate findings including bounded linked development reference preparation')
    manifest['files']=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,
        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((REPO/'architecture').rglob('*'))
        if p.is_file() and '__pycache__' not in p.parts]
    (REPO/'BACKUP_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    assert all(hashlib.sha256((REPO/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in manifest['files'])
    print('CURATED_ARTIFACTS_VERIFIED',len(manifest['files']))


if __name__=='__main__':
    main()
