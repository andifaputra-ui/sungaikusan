"""Audit completion, lock new response artifacts, and stage a curated public backup."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
HISTORY=ROOT.parent.parent/'Gpt_6_Astra_historical_reasoning'
REPO=Path('E:/Bendungan_Kusan/GitHub_Backup/kusan')


def digest(path: Path) -> str:
    """Hash a saved artifact without decoding imagery."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path,value: dict) -> None:
    """Write explicit UTF8 accounting and provenance."""
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def main() -> None:
    """Keep detailed reader/geographic evidence local and freeze this decision boundary."""
    now=datetime.now(timezone.utc).isoformat()
    packet=ROOT/'BLINDED_OPTICAL_PACKET'
    lock=json.loads((packet/'PACKET_LOCK.json').read_text(encoding='utf-8'))
    assert all(digest(packet/name)==expected for name,expected in lock['files'].items())
    assert digest(ROOT/'OPTICAL_RESPONSE_PROTOCOL_V1.md')==lock['protocol_sha256']
    summary=json.loads((ROOT/'REFERENCE_RESPONSE_SUMMARY.json').read_text(encoding='utf-8'))
    ledger=json.loads((ROOT/'BOUNDED_OPTICAL_RESPONSE_LEDGER.json').read_text(encoding='utf-8'))
    assert ledger['manual_response_sha256']==digest(ROOT/'ASSISTANT_OPTICAL_REVIEW.json')
    assert len(ledger['observations'])==96 and len(ledger['cases'])==24
    source_matches=json.loads((ROOT/'OPTICAL_SOURCE_MATCH_FREEZE.json').read_text(encoding='utf-8'))['matches']
    overpasses=set()
    for key,match in source_matches.items():
        props=match['metadata']['properties']
        if key.startswith('S2:'):
            overpasses.add(('S2',props['DATATAKE_IDENTIFIER'].split('_N')[0]))
        else:
            scene=props['LANDSAT_SCENE_ID']
            # Standard scene ID: satellite+path+row+YYYYDDD+station/version.
            overpasses.add(('LS',scene[:6]+scene[9:16]))
    assert len(overpasses)==17
    budget=json.loads((ROOT/'REFERENCE_TRANSFER.json').read_text(encoding='utf-8'))
    artifact_bytes=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
    assert artifact_bytes<1024**3 and budget['charged_bytes']<1024**3
    save(ROOT/'READER_DECLARATION_ASSISTANT.json',{
        'reader':'Codex assistant first pass','response_files':['ASSISTANT_OPTICAL_REVIEW.json'],
        'genuinely_independent_interpreter':False,'knew_auxiliary_discovery_context':True,
        'current_panel_SAR_predictions_inspected':False,'previous_reference_answers_used':False,
        'independent_interpreter_reliability':'UNMEASURED','source_role':'DEVELOPMENT_ONLY',
        'uncertainty':'No local absolute registration or intervening-event evidence; no final semantic truth claim'})
    save(ROOT/'RESPONSE_LOCK.json',{'utc':now,'files':{name:digest(ROOT/name) for name in [
        'ASSISTANT_OPTICAL_REVIEW.json','BOUNDED_OPTICAL_RESPONSE_LEDGER.json',
        'READER_DECLARATION_ASSISTANT.json','OPTICAL_RESPONSE_PROTOCOL_V1.md']},
        'no_candidate_join':True,'do_not_rewrite_for_later_predictions':True})
    save(ROOT/'COMPLETION_AUDIT.json',{'utc':now,'status':summary['status'],
        'all_packet_hashes_verified':len(lock['files']),'response_hash_and_counts_verified':True,
        'unique_optical_products':20,'S2_datatakes':12,'LS_satellite_path_day_overpasses':5,
        'overpasses_not_assumed_statistically_independent':True,
        'artifact_file_bytes_at_audit':artifact_bytes,'artifact_storage_limit_bytes':1024**3,
        'image_body_bytes':budget['received_metered_bytes'],'charged_additional_transfer_bytes':budget['charged_bytes'],
        'additional_transfer_limit_bytes':1024**3,'no_new_candidate_inference':True,
        'no_background_job_or_queue':True,'comparison_gate':'CLOSED','method_freeze':False})
    save(ROOT/'FOCUSED_TEST_RESULTS.json',{'utc':now,'tests_run':10,'failures':0,
        'command':'python -X utf8 -m unittest discover -s LINKED_DEVELOPMENT_COMPARISON_20261024 -p test_*.py -v',
        'not_semantic_validation':True,'warning':'Affine multiplication pending deprecation; no effect on current calculations'})
    save(ROOT/'STATUS.json',{'phase':'COMPLETED_REFERENCE_ADEQUACY_DECISION_FOR_REVIEW','utc':now,
        'result':summary['status'],'no_background_job':True,'comparison_gate':'CLOSED',
        'next':'NEXT_REFERENCE_DECISION.md; no automatic site relocation, acquisition or inference'})
    checkpoint='''# Linked reference block completed — 24 October 2026

Read Check_point_2/LINKED_DEVELOPMENT_COMPARISON_20261024/REFERENCE_FINDINGS_FOR_REVIEW.md and NEXT_REFERENCE_DECISION.md. BOUNDED_REFERENCE_INFORMATION_RECOVERED; COMPARISON_ADEQUACY_NOT_DEMONSTRATED. No background job or automatic follow-on inference. Do not relaunch acquisition or rendering. This supersedes the earlier running checkpoint.

All96 slots and24date-supports preserved:78chips acquired,18absent,zero acquisition failures;20unique products represent12S2datatakes and5Landsat overpasses. Acquisition finished23:30:25Makassar. All original body/grid/count/pre-read checks pass. TIFF labels absent, request-traced band order caveat explicit. Windows DLL rendering failure retained; process-local existing-library paths resolved it, exact export unisolated, no installation changes. Ten focused tests pass. Additional charge67MiB including64MiB metadata reserve; actual imagery1,410,692bytes. Local artifacts about17MB before final accounting, limit1GiB. Prior smoke budget untouched.

All24optical packets screened. Assistant first-pass dispositions46obscured,24unresolved,5visible non-water,3shoreline,18missing. These are interpretations, not final labels. Assistant knew auxiliary context, did not inspect current-panel SAR predictions; independent interpreter reliability remains UNMEASURED. Original separate reader returns unchanged. Packet and new responses are hash-locked locally. Do not rewrite them to fit predictions.

Temporal19E0,3E1,2E2,0E3. Only one vegetation case has an informative conditional non-water interval. Bracketed shoreline water loses primary-support certainty under fixed25position shifts, possible water[0,1]. No E2water lower bound>0 for10/30/50m; all transient-allowed target-time bounds[0,1]. No certified absolute registration or independent event bridge. Keep comparison gate closed. No model performance, scientific hypothesis direction or method freeze follows from reference failure.

Consequential proposal: a NEW permanently-development, reference-led qualification branch using saved evidence first (up to4systems/8supports), preserving this failed panel intact. No moving existing centres, selecting convenient replacements, new imagery/orders, SAR processing or semantic comparison without that design decision. Coastal controls alone cannot justify inland flood performance. Final probability audit and source roles remain sealed/separate. Source evidence, geometry, manual responses and images stay local; public backup contains code/protocol/aggregate summaries only.
'''
    (HISTORY/'LINKED_REFERENCE_COMPLETED_20261024.md').write_text(checkpoint,encoding='utf-8')
    start=HISTORY/'START_HERE.md'
    header='''# Latest: linked reference block completed; adequacy decision ready — 2026-10-24

Read LINKED_REFERENCE_COMPLETED_20261024.md and the linked package REFERENCE_FINDINGS_FOR_REVIEW.md / NEXT_REFERENCE_DECISION.md.78chips/18absent,24date-supports preserved;10technical/accounting tests pass. Only2conditional bracketed cases; shoreline possible-water[0,1] under fixed position shifts. No adequate water/land comparison, no model performance claim. Assistant first pass only; independent reliability unmeasured. No job running/queued. Do not restart completed workers or automatically rescue/relocate sites. Proposed new reference-led development branch awaits the consequential decision; final sealing and method-freeze block persist.

---

'''
    text=start.read_text(encoding='utf-8')
    if not text.startswith(header):
        start.write_text(header+text,encoding='utf-8')
    (REPO/'CHECKPOINT.md').write_text(checkpoint,encoding='utf-8')
    allow=['OPTICAL_RESPONSE_PROTOCOL_V1.md','optical_qa.py','test_optical_qa.py','prepare_optical_review.py',
        'make_visual_overviews.py','account_optical_responses.py','test_response_accounting.py',
        'OPTICAL_PREPARATION_SUMMARY.json','REFERENCE_RESPONSE_SUMMARY.json','REFERENCE_ACQUISITION_SUMMARY.json',
        'REFERENCE_FINDINGS_FOR_REVIEW.md','NEXT_REFERENCE_DECISION.md','COMPLETION_AUDIT.json',
        'FOCUSED_TEST_RESULTS.json','PREPARATION_REPAIRS.json','finalize_reference_block.py']
    destination=REPO/'architecture/2026-10-24-linked-development'
    for name in allow:
        shutil.copyfile(ROOT/name,destination/name)
    save(ROOT/'COMPLETED_SOURCE_HASHES.json',{'utc':now,'files':{name:digest(ROOT/name) for name in allow},
        'previous_execution_hashes_preserved':True})
    shutil.copyfile(ROOT/'COMPLETED_SOURCE_HASHES.json',destination/'COMPLETED_SOURCE_HASHES.json')
    readme=REPO/'README.md';text=readme.read_text(encoding='utf-8');first,rest=text.split('\n\n',1)
    prefix='Latest completed block: [reference evidence findings](architecture/2026-10-24-linked-development/REFERENCE_FINDINGS_FOR_REVIEW.md). Acquisition/QA completed; reference adequacy for detector comparison is not demonstrated. No job running. Read the [new consequential decision](architecture/2026-10-24-linked-development/NEXT_REFERENCE_DECISION.md) and [checkpoint](CHECKPOINT.md). Earlier running entries are historical.\n\n'
    if prefix not in text:
        readme.write_text(first+'\n\n'+prefix+rest,encoding='utf-8')
    manifest=json.loads((REPO/'BACKUP_MANIFEST.json').read_text(encoding='utf-8'))
    manifest['scope']='Curated source/protocol and aggregate completed-reference findings; no detailed responses, geography or imagery'
    manifest['files']=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
        for p in sorted((REPO/'architecture').rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    save(REPO/'BACKUP_MANIFEST.json',manifest)
    assert all(digest(REPO/item['path'])==item['sha256'] for item in manifest['files'])
    print('CURATED_ARTIFACTS_VERIFIED',len(manifest['files']))
    print(json.dumps(json.loads((ROOT/'COMPLETION_AUDIT.json').read_text()),indent=2))


if __name__=='__main__':
    main()
