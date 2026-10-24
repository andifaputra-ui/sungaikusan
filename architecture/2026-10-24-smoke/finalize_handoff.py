"""Save an audited local handoff without changing scientific outputs."""
from pathlib import Path
from datetime import datetime,timezone
import argparse
import hashlib
import json

ROOT=Path(__file__).resolve().parent
HISTORY=ROOT.parents[1]/'Gpt_6_Astra_historical_reasoning'


def main() -> None:
    """Record the final role/status, current code identities and verified backup."""
    parser=argparse.ArgumentParser()
    parser.add_argument('--backup-commit',required=True)
    parser.add_argument('--artifact-count',type=int,required=True)
    args=parser.parse_args()
    original=ROOT/'STATUS.json'
    archived=ROOT/'attempts/completed_controller_status.json'
    if not archived.exists():
        archived.write_bytes(original.read_bytes())
    status={'phase':'TECHNICAL_SMOKE_AUDITED_STOPPED_FOR_SCIENTIFIC_REVIEW',
        'utc':datetime.now(timezone.utc).isoformat(),'technical_result':'PASS',
        'scientific_performance':'UNKNOWN','review_package':'FINDINGS_FOR_REVIEW.md',
        'next_decision':'NEXT_DECISION.md','visual_qa':'Two fixed views inspected; absolute/fine boundary registration not established',
        'no_further_work_queued':True,'running_scientific_jobs':[],
        'no_automatic_retry_or_scaling':True}
    original.write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
    backup={'date_local':'2026-10-24','remote':'https://github.com/andifaputra-ui/sungaikusan',
        'commit':args.backup_commit,'remote_sha_verified':True,'curated_artifacts_verified':args.artifact_count,
        'scope':'Curated code/protocols, exact runtime lock, aggregate smoke/audit and review findings. Excludes source pixels, weights, QA image and reference/reader data.'}
    (ROOT/'BACKUP_SUCCESS.json').write_text(json.dumps(backup,indent=2)+'\n',encoding='utf-8')
    sources=sorted(list(ROOT.glob('*.py'))+[ROOT/'AUTHORIZATION.json',ROOT/'RUN_SCOPE.md',ROOT/'requirements_roots.txt'])
    (ROOT/'FROZEN_EXECUTION_SOURCES_SHA256.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},indent=2)+'\n',encoding='utf-8')
    checkpoint=HISTORY/'NATIVE_MODEL_SMOKE_COMPLETED_20261024.md'
    checkpoint.write_text('''# Native S1-only smoke complete — 24 October 2026

Read Check_point_2/NATIVE_MODEL_SMOKE_20261024/FINDINGS_FOR_REVIEW.md and NEXT_DECISION.md. The approved single-scene test passed; its numerical result is SMOKE_RESULT.json, resource/integrity audit COMPLETION_AUDIT.json, and limited visual inspection VISUAL_QA_REVIEW.json. No scientific/background job is running or queued. Do not relaunch setup/controller, infer again, or request the same technical-test approval.

Actual input: one explicit 1 September 2024 S1 scene and frozen512x512 C1 indexing-grid patch, separate native GEE sigma0 VV/VH/provider-angle branch. Exact immutable release checkpoint/stats and trainer, strict restricted state loading, CPU four-flip inference. All262,144pixels have joint current support; no real missing-current case was exercised. Finite unvalidated scores and exact output grid passed. No threshold, water map, training, accuracy, final references or method freeze.

Four-flip forward46.094s; inside-script281.375s; controller-stage510.092s. Different clock boundaries; startup difference not separately instrumented. Peak memory not measured and no full-series runtime extrapolation. Charged response-body transfer969,932,800bytes (0.903GiB) below2GiB; runtime/run storage4,893,588,289bytes (4.558GiB) below6GiB at audit. Budget includes conservative reservations, not headers/TLS. No paid/Planet use.

All30original readiness hashes unchanged. Three live native-window guards passed before the one pixel request. Initialization-order and mutable-download-request defects were archived and fixed with four passing mock regression tests; original downloaded input was reused without another request or budget reset. One actual model inference only. Original inputs/outputs and failed-attempt logs remain unchanged. The original SMOKE_RESULT visual-pending note is a historical run receipt, superseded for QA by the separate review rather than rewritten.

Fixed full512/central128 panels were rendered and visually inspected. No obvious gross source-relative rotation/displacement; central score crop nearly uniform and cannot establish fine boundary alignment. Exact shared grid is not independent absolute geolocation or water accuracy. No optical reference or second-reader labels were created. Scores are not calibrated probabilities or fractional water area. Extreme source values retained; support is not a guarantee of reliability and existing Phase2.4 safeguards remain.

Scientific status: positive local executability, unknown Kusan detection performance. Recommended next is a reference-linked development comparison, starting frozen S1-only versus OPERA only if actual observation/source intervals can be paired. Approximately12physicalsystems/up-to24date-supports is a proposed development workload, not a final probability sample. Prioritize independently evidenced persistent water, transitions, ordinary land, artificial dark land, boundaries and poor support. AEF remains a gated optional later arm; do not wait on or silently substitute its encoding. Proposed new acquisition budget and semantic/product mappings require separate review in NEXT_DECISION.md. Old VV A/B, original intervals/reader responses, final evidence/separate probability audit, no-full-series and no-method-freeze limits remain.

GitHub curated backup verified at COMMIT_PLACEHOLDER, COUNT_PLACEHOLDER artifacts. Includes aggregate results, review documents and exact runtime source/lock; excludes source rasters, weights, local QA image, detailed reference/reader material. Local BACKUP_SUCCESS.json and execution-source manifest are refreshed. Preserve old running/stop checkpoints as dated history; this completed checkpoint is current.
'''.replace('COMMIT_PLACEHOLDER',args.backup_commit).replace('COUNT_PLACEHOLDER',str(args.artifact_count)),encoding='utf-8')
    start=HISTORY/'START_HERE.md'
    entry='''# Latest: native S1-only technical smoke completed and audited — 2026-10-24

Read NATIVE_MODEL_SMOKE_COMPLETED_20261024.md, FINDINGS_FOR_REVIEW.md and NEXT_DECISION.md in the smoke package. TECHNICAL_SMOKE_PASS; scientific performance UNKNOWN. Full current support, frozen identities, grid and score checks pass. Four-flip CPU46.094s; charged transfer0.903GiB/storage4.558GiB within2/6GiB limits. Fixed two-scale QA inspected with fine/absolute-registration limits explicit. No job running/queued. Do not relaunch the completed test. Next is scientific authorization of a reference-linked development comparison, not another setup loop or method freeze. Curated GitHub backup COMMIT_PLACEHOLDER; COUNT_PLACEHOLDER artifacts verified. Existing scientific data, responses and final sealing preserved.

---

'''.replace('COMMIT_PLACEHOLDER',args.backup_commit).replace('COUNT_PLACEHOLDER',str(args.artifact_count))
    start.write_text(entry+start.read_text(encoding='utf-8-sig'),encoding='utf-8')
    print('AUDITED_HANDOFF_SAVED',checkpoint)


if __name__=='__main__':
    main()
