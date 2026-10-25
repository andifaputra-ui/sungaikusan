"""Lock the completed reference-only experiment and preserve a curated backup."""
from pathlib import Path
from datetime import datetime,timezone
import json
import hashlib
import shutil

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
PARENT=BRANCH.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'
HISTORY=BRANCH.parent.parent/'Gpt_6_Astra_historical_reasoning'
REPO=Path('E:/Bendungan_Kusan/GitHub_Backup/kusan')


def read(path: Path) -> dict:
    """Read recorded state only."""
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path: Path) -> str:
    """Hash saved text/provenance artifacts without decoding source imagery."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path,value: dict) -> None:
    """Write UTF8 audit and continuation state."""
    path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')


def main() -> None:
    """Validate preservation/costs and stop at the meaningful timing decision."""
    now=datetime.now(timezone.utc).isoformat()
    for folder,name in [(PARENT,'RESPONSE_LOCK.json'),(BRANCH,'BRANCH_LOCK.json')]:
        lock=read(folder/name)
        assert all(digest(folder/key)==sha for key,sha in lock['files'].items())
    acquired=read(ROOT/'REFRESHED_ATTEMPT/ACQUISITION_SUMMARY.json')
    response=read(ROOT/'FOUR_CHIP_RESPONSE_LEDGER.json')
    assert acquired['outcomes']=={'ACQUIRED_NOT_INTERPRETED':4}
    assert response['manual_return_sha256']==digest(ROOT/'OPTICAL_READER_RETURN.json')
    assert len(response['observations'])==4 and len(response['target_time_cases'])==2
    assert acquired['new_metered_body_bytes']<=4*1024**2 and acquired['new_conservative_charge_bytes']<=4*1024**2
    initial=read(ROOT/'BUDGET_BEFORE.json');resumed=read(ROOT/'REFRESHED_ATTEMPT/BUDGET_BEFORE.json')
    assert initial['charged_bytes']==resumed['charged_bytes']
    assert not list((ROOT/'chips').glob('*'))
    encoding=read(ROOT/'OVERLAP_ENCODING_RESULT.json')
    assert all(b['exact0DN_count']==b['joint_valid_pairs']==1400 for b in encoding['bands'])
    technical=read(ROOT/'FOUR_CHIP_TECHNICAL_AUDIT.json')['observations']
    assert len(technical)==4
    files_bytes=sum(p.stat().st_size for folder in [PARENT,BRANCH] for p in folder.rglob('*') if p.is_file())
    assert files_bytes<1024**3
    summary={'utc':now,'status':response['status'],'acquired_reference_chips':4,
        'new_metered_image_body_bytes':acquired['new_metered_body_bytes'],
        'new_conservative_charge_bytes':acquired['new_conservative_charge_bytes'],
        'cumulative_reference_charge_bytes':acquired['cumulative_charge_bytes'],
        'retained_transfer_ceiling_bytes':1024**3,'aggregate_artifact_file_bytes_at_audit':files_bytes,
        'retained_storage_ceiling_bytes':1024**3,'source_band_preread_checks':21,'local_guarded_reads':4,
        'optical_time_water_views':1,'optical_time_nonwater_views':1,'obscured_views':1,'unresolved_views':1,
        'new_target_time_eligible_cases':0,'new_temporal_tiers':{'E1':2},
        'same_nominal_S2_overlap_centres':1400,'RGB_NIR_pairs_exact0DN':5600,
        'historical_pixel_equivalence_or_absolute_calibration_claim':False,
        'ingestion_version_changes_retained':3,'all_other_checked_source_metadata_unchanged':True,
        'initial_metadata_only_stop_pixel_requests':0,'substituted_sites_dates_or_products':0,
        'focused_tests_run':4,'test_failures':0,'original_branch_and_parent_locks_preserved':True,
        'new_candidate_inference':0,'new_SAR_processing':0,'Planet_or_paid_orders':0,
        'comparison_gate':'CLOSED','no_background_job':True,'method_freeze':False,
        'next_proposal':'Metadata-only reference-date/SAR feasibility for actual clear13/14May optical dates; not executed'}
    save(ROOT/'COMPLETION_AUDIT.json',summary)
    save(ROOT/'REFERENCE_RESPONSE_LOCK.json',{'utc':now,'files':{name:digest(ROOT/name) for name in [
        'OPTICAL_READER_RETURN.json','FOUR_CHIP_RESPONSE_LEDGER.json','OVERLAP_ENCODING_DIAGNOSTIC_PLAN.json',
        'OVERLAP_ENCODING_RESULT.json','REFRESHED_SOURCE_MATCH_FREEZE.json']},
        'new_readings_not_independent_human_reliability':True,'no_rewriting_to_fit_predictions':True})
    save(ROOT/'STATUS.json',{'phase':'FOUR_REFERENCE_QUALIFICATION_COMPLETE; TIMING_ADEQUACY_DECISION_FOR_REVIEW',
        'utc':now,'no_background_job':True,'comparison_gate':'CLOSED','next':'FINDINGS_AND_DECISION.md'})
    save(BRANCH/'STATUS.json',{'phase':'FOUR_REFERENCE_QUALIFICATION_COMPLETE; MAY11_TIME_GATE_NOT_PASSED',
        'utc':now,'no_background_job':True,'comparison_gate':'CLOSED',
        'next':'FOUR_CHIP_EXECUTION/FINDINGS_AND_DECISION.md'})
    checkpoint='''# Four targeted optical references completed — 25 October2026

Read Check_point_2/REFERENCE_LED_DEVELOPMENT_20261025/FOUR_CHIP_EXECUTION/FINDINGS_AND_DECISION.md. OPTICAL_TIME_WATER_AND_ARTIFICIAL_LAND_RECOVERED; MAY11_ACQUISITION_TIME_ADEQUACY_NOT_DEMONSTRATED. No process or automatic follow-on acquisition/inference remains. Do not relaunch any completed worker.

The user continue authorized the exact four-chip proposal. Initial metadata-only guard stopped on changed GEE ingestion versions, before any pixel request. All returned metadata except version matched for the3S2products; Landsat version unchanged. After primary-doc research, current revisions were explicitly refrozen as the same authorized reference products, not assumed old pixel-equivalent. Initial source/stop/version records retained. Current versions rechecked immediately before first pixel reads. No product,date,centre,role or radiometry substitution. A missing-space compilation error was fixed before rendering. No packages/global environment changed.

All4chips acquired:92,250imagebodybytes,2MiB conservative new charge,69MiB cumulative within retained1GiB ceiling and authorized4MiB increment.21source-band native-window checks and4localgrid/body/mask/scaling checks pass. Four focused execution/provenance tests pass. Actual images and detailed manifests stay local. Parent24-support failures, frozen nominations, controls and reader responses are hash-preserved. No SAR/model/Planet/paid action.

N03basin after-view14May2025 clear opticalW across30/10/50m and25shifts; beforeLandsat11May unresolved/cloud affected. N04runway after-view13May visible artificial/non-water surface plus vegetated land; before11May cloud-obscured.90m support is not pure asphalt. Both new cases E1, targetMay11transferUNKNOWN and possiblewater[0,1]. No event/operation bridge or measured absolute registration. No independent interpreter reliability measured. ExistingN01coastal andN02ordinary-land E2conditional controls do not resolve missing inland/hardland target-time evidence. Detector comparison stays CLOSED, no hypothesis/model verdict or method freeze.

Encoding diagnostic was frozen before new pixel-array inspection:1400exactoverlappingcentres x4RGB/NIRbands=5600values, all0DNdifference between legacyL29 and current harmonizedS2May14 export. Additional-0.1would introduce a discrepancy. This is a local same-nominal-product encoding relationship, not absolute calibration or global322-view proof; original full ESA generationURI not re-established. Old/newsameMay14acquisition is one temporal observation, not two independent votes. Original legacy arrays/contracts/answers unchanged.

Next consequential proposal only: metadata-only co-registration/temporal feasibility starting from actual clear13Mayrunway and14Maybasin optical dates, keeping objects and optical interpretations frozen. Do not keep rescuingMay11or substitute dates automatically. No new SARpixels, optical orders, candidate runs or fixed-hour transfer rule. If alternate tracks/timing cannot support intended claims, preserve the failure. Final probability reference evidence remains sealed; retrospective2017-2025claims and full-series production are not authorized.
'''
    (HISTORY/'FOUR_REFERENCE_COMPLETED_20261025.md').write_text(checkpoint,encoding='utf-8')
    start=HISTORY/'START_HERE.md';old=start.read_text(encoding='utf-8')
    header='''# Latest: four optical references completed; target timing still unresolved — 2026-10-25

Read FOUR_REFERENCE_COMPLETED_20261025.md and FOUR_CHIP_EXECUTION/FINDINGS_AND_DECISION.md.4/4chips acquired, clear basinW and runwayN at optical time, both E1forMay11SAR because before-views fail.0newtarget-timeeligible cases. Local5600RGB/NIRoverlapvalues match exactly; no globalcalibration claim. GEEingestionversionrefresh/initialzero-pixelstop retained, allothermetadataequal.92,250imagebytes;2MiBnewcharge/69MiBcumulative;4tests pass. No job or automatic rescue/inference. Next proposal is metadata-only optical-date/SAR feasibility, not executed. Parent/nominations/responses/finalsealing intact.

---

'''
    if not old.startswith(header):
        start.write_text(header+old,encoding='utf-8')
    allow=['AUTHORIZATION.json','acquire_four.py','acquire_four_initial_version_guard.py',
        'diagnose_source_version.py','freeze_current_reference_metadata.py','audit_and_render_four.py',
        'OVERLAP_ENCODING_DIAGNOSTIC_PLAN.json','OVERLAP_ENCODING_RESULT.json','test_four_chip_contract.py',
        'account_four_responses.py','FINDINGS_AND_DECISION.md','COMPLETION_AUDIT.json','finalize_four_reference.py']
    destination=REPO/'architecture/2026-10-25-four-reference';destination.mkdir(parents=True,exist_ok=True)
    for name in allow:
        shutil.copyfile(ROOT/name,destination/name)
    save(ROOT/'PUBLIC_SOURCE_HASHES.json',{'utc':now,'files':{name:digest(ROOT/name) for name in allow}})
    shutil.copyfile(ROOT/'PUBLIC_SOURCE_HASHES.json',destination/'PUBLIC_SOURCE_HASHES.json')
    (REPO/'CHECKPOINT.md').write_text(checkpoint,encoding='utf-8')
    readme=REPO/'README.md';text=readme.read_text(encoding='utf-8');first,rest=text.split('\n\n',1)
    prefix='Latest completed result: [four targeted optical references](architecture/2026-10-25-four-reference/FINDINGS_AND_DECISION.md) recovered optical-time basin water and artificial land, but May11 acquisition-time adequacy remains unproven. No job/model evaluation running. Read [checkpoint](CHECKPOINT.md). Earlier source-request/running entries are historical.\n\n'
    if prefix not in text:
        readme.write_text(first+'\n\n'+prefix+rest,encoding='utf-8')
    manifest=read(REPO/'BACKUP_MANIFEST.json')
    manifest.update(date_local='2026-10-25',scope='Curated code/protocol/aggregate four-reference results; imagery, detailed source geometry and reader returns excluded')
    manifest['files']=[{'path':p.relative_to(REPO).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)}
        for p in sorted((REPO/'architecture').rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    save(REPO/'BACKUP_MANIFEST.json',manifest)
    assert all(digest(REPO/r['path'])==r['sha256'] for r in manifest['files'])
    print('CURATED_ARTIFACTS_VERIFIED',len(manifest['files']))
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
