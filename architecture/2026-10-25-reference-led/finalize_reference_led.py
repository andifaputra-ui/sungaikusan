"""Preserve the saved-evidence branch and stage only public-safe aggregate/code artifacts."""
from __future__ import annotations
from pathlib import Path
from datetime import datetime,timezone
import json
import hashlib
import shutil

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'
HISTORY=ROOT.parent.parent/'Gpt_6_Astra_historical_reasoning'
REPO=Path('E:/Bendungan_Kusan/GitHub_Backup/kusan')


def digest(path: Path) -> str:
    """Hash saved provenance without decoding image arrays."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path,value: dict) -> None:
    """Save a UTF8 checkpoint or manifest."""
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def main() -> None:
    """Record qualification limits and unexecuted source needs without changing parent evidence."""
    now=datetime.now(timezone.utc).isoformat()
    parent_lock=json.loads((PARENT/'RESPONSE_LOCK.json').read_text(encoding='utf-8'))
    assert all(digest(PARENT/name)==sha for name,sha in parent_lock['files'].items())
    source_plan=json.loads((ROOT/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.json').read_text(encoding='utf-8'))
    controls=json.loads((ROOT/'CONTROL_QUALIFICATION.json').read_text(encoding='utf-8'))
    groups=json.loads((ROOT/'DISCOVERY_SCREEN_NOTES.json').read_text(encoding='utf-8'))['groups']
    assert len([alias for group in groups for alias in group['aliases']])==62
    actual_bytes=sum(p.stat().st_size for folder in [ROOT,PARENT] for p in folder.rglob('*') if p.is_file())
    assert actual_bytes<1024**3
    summary={'status':controls['status'],'utc':now,'legacy_views_screened':62,
        'new_reference_pixels_acquired':0,'candidate_predictions_read':0,'nominated_systems':4,
        'nominated_date_supports':4,'target_date':'2025-05-11','conditional_controls':2,
        'inland_basin_qualification':'UNRESOLVED_RADIOMETRY_AND_TIME','difficult_land_qualification':'NO_DATED_MAY_REFERENCE',
        'parent_response_hashes_preserved':True,'proposed_new_chips':4,
        'proposed_new_maximum_response_body_bytes':4*1024**2,'acquisition_authorized':False,
        'combined_parent_and_branch_file_bytes_at_audit':actual_bytes,'unchanged_storage_ceiling_bytes':1024**3,
        'prior_charge_bytes_not_reset':70254592,'new_network_pixel_charge_bytes':0,
        'focused_tests':4,'test_failures':0,'no_background_job':True,'comparison_gate':'CLOSED',
        'final_validation':'SEALED','method_freeze':False,'no_Planet_orders':True}
    save(ROOT/'COMPLETION_SUMMARY.json',summary)
    save(ROOT/'STATUS.json',{'phase':'SAVED_EVIDENCE_BRANCH_COMPLETE; FOUR_CHIP_SOURCE_DECISION_FOR_REVIEW',
        'utc':now,'no_background_job':True,'next':'FINDINGS_AND_NEXT_SOURCE_DECISION.md',
        'comparison_gate':'CLOSED','new_acquisition_authorized':False})
    save(ROOT/'BRANCH_LOCK.json',{'utc':now,'files':{name:digest(ROOT/name) for name in [
        'SCOPE.json','NOMINATION_FREEZE.json','LEGACY_SCREEN_FREEZE.json','DISCOVERY_SCREEN_NOTES.json',
        'CONTROL_VISUAL_RESPONSE.json','CONTROL_QUALIFICATION.json','PROPOSED_FOUR_CHIP_SOURCE_PLAN.json']},
        'all_permanent_development':True,'parent_unchanged':True})
    checkpoint='''# Reference-led saved-evidence branch completed — 25 October 2026

Read Check_point_2/REFERENCE_LED_DEVELOPMENT_20261025/FINDINGS_AND_NEXT_SOURCE_DECISION.md. TWO_CONDITIONAL_CONTROLS_QUALIFIED; INLAND_WATER_AND_DIFFICULT_LAND_GAPS_REMAIN. No background job, acquisition, candidate processing or automatic continuation is queued.

The user's continue advanced the saved-evidence-first amendment, maximum4systems/8supports. All62legacy2025overlap views were guarded/hash/grid checked and screened; legacy display remains proxy-only. The completed78-view parent screen was reused. Exact4nominations/4date-supports on11May2025are frozen before predictions: coastal control, ordinary vegetation control, a real inland basin-like interior visible14May2025, and mapped runway requiring actual May observations. Parent24-support failures/intervals and original reader returns are unchanged; hashes verified.

Two calibrated saved controls support E2conditional optical water/non-water portions across30mprimary/10&50m and25fixedposition scenarios. N01is coastal/marine, not inland flood evidence. Both retain unmeasured absolute registration, unmeasured independent-reader reliability and unconstrained transient-allowed target-time[0,1]. No detector evaluation/accuracy claim follows. Inland basin has one-sided legacy proxy evidence; no mining/pond-function/contamination inferred. Runway tag is not dated land truth.

Concrete next proposal, NOT executed: only4referencechips from already identity-verified products: basin Landsat9May11before+harmonizedS2May14after, runway S2May11before+May13after. All4recorded footprints cover full490m;21band-window metadata checks pass. New windows not fetched, clarity/state/transferUNKNOWN. Max4MiB new bodies,403,368bytes uncompressed arrays. Retain parent's67MiB cumulative charge and1GiB ceiling; no Planet/paid order/newSAR. If approved, only acquire/qualify those4and stop at adequacy, no substitutions or automatic candidate run.

Four focused contract tests pass. BRANCH_LOCK protects all new exact locations/source plan/manual control response. Detailed geography, raw imagery, per-view discovery/reader responses remain local; public backup is curated code/protocol/aggregate findings. Parent source/response locks match. This is a purposive DEVELOPMENT_ONLY branch; no probability sample drawn or final evidence used. Final sealed probability validation and method freeze remain blocked.
'''
    (HISTORY/'REFERENCE_LED_COMPLETED_20261025.md').write_text(checkpoint,encoding='utf-8')
    start=HISTORY/'START_HERE.md';old=start.read_text(encoding='utf-8')
    header='''# Latest: saved reference-led branch completed; four-chip decision ready — 2026-10-25

Read REFERENCE_LED_COMPLETED_20261025.md and REFERENCE_LED_DEVELOPMENT_20261025/FINDINGS_AND_NEXT_SOURCE_DECISION.md.62legacyviews screened,4exactdevelopmentnominations frozen,2conditionalcalibratedcontrols retained. Inland basin/radiometry/time and runway dated-reference gaps remain. Concrete4chip proposal max4MiB, allsource/window/footprintmetadata feasible, NOT acquired/authorized. No job running or candidate comparison. Parent24support failures and responses unchanged.4contract tests pass; source/reader roles/final sealing preserved.

---

'''
    if not old.startswith(header):
        start.write_text(header+old,encoding='utf-8')
    destination=REPO/'architecture/2026-10-25-reference-led';destination.mkdir(parents=True,exist_ok=True)
    allow=['SCOPE.json','screen_legacy_views.py','enlarge_saved_discovery.py','freeze_nominations.py',
        'qualify_saved_controls.py','prepare_bounded_source_request.py','qualify_control_accounting.py',
        'test_reference_led_contract.py','FINDINGS_AND_NEXT_SOURCE_DECISION.md','COMPLETION_SUMMARY.json',
        'NOMINATION_FREEZE.sha256','PROPOSED_FOUR_CHIP_SOURCE_PLAN.sha256','finalize_reference_led.py']
    for name in allow:
        shutil.copyfile(ROOT/name,destination/name)
    save(ROOT/'PUBLIC_SOURCE_HASHES.json',{'utc':now,'files':{name:digest(ROOT/name) for name in allow}})
    shutil.copyfile(ROOT/'PUBLIC_SOURCE_HASHES.json',destination/'PUBLIC_SOURCE_HASHES.json')
    (REPO/'CHECKPOINT.md').write_text(checkpoint,encoding='utf-8')
    readme=REPO/'README.md';text=readme.read_text(encoding='utf-8');first,rest=text.split('\n\n',1)
    prefix='Latest result,25October2026: [saved reference-led qualification](architecture/2026-10-25-reference-led/FINDINGS_AND_NEXT_SOURCE_DECISION.md) recovered two conditional controls and a concrete inland basin lead. Four tiny optical reference chips are proposed, not acquired. No job or detector comparison running. See [checkpoint](CHECKPOINT.md).\n\n'
    if prefix not in text:
        readme.write_text(first+'\n\n'+prefix+rest,encoding='utf-8')
    manifest=json.loads((REPO/'BACKUP_MANIFEST.json').read_text(encoding='utf-8'))
    manifest.update(date_local='2026-10-25',scope='Curated code, protocols and aggregate saved-evidence reference-led findings; detailed geography/responses/images excluded')
    manifest['files']=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
        for p in sorted((REPO/'architecture').rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    save(REPO/'BACKUP_MANIFEST.json',manifest)
    assert all(digest(REPO/r['path'])==r['sha256'] for r in manifest['files'])
    print('CURATED_ARTIFACTS_VERIFIED',len(manifest['files']))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
