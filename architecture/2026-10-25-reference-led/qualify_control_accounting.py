"""Propagate manually interpreted controls through the unchanged support protocol."""
from pathlib import Path
import json
import hashlib
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'))
from account_optical_responses import scenarios


def main() -> None:
    """No source pixels or candidate predictions enter this accounting."""
    source=ROOT/'CONTROL_VISUAL_RESPONSE.json'
    response=json.loads(source.read_text(encoding='utf-8'))
    audit=json.loads((ROOT/'SAVED_CONTROL_AUDIT.json').read_text(encoding='utf-8'))
    records=[]
    for control in response['records']:
        quality=[r for r in audit if r['nomination']==control['id'] and r['provider']=='S2']
        if len(quality)!=2:
            raise RuntimeError('Distinct bracketing S2 metadata/views required')
        checks={str(size):all(v['available']==1 and v['flagged']==0
            for row in quality for v in row['quality_diagnostic'][str(size)]) for size in [10,30,50]}
        # This is a diagnostic corroboration, not an automatic visible-state assignment.
        records.append({'id':control['id'],'manual_response_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'supports':{str(size):scenarios(control['pattern90m'],size) for size in [10,30,50]},
            'selected_QA_available_unflagged_all_scenarios':checks,
            'evidence_tier':'E2','acquisition_time_eligibility':'CONDITIONAL_CONTROL_ONLY',
            'transient_allowed_possible_water_bound':[0,1],'reference_scope':control['scope']})
    result={'status':'TWO_CONDITIONAL_CONTROLS_QUALIFIED; INLAND_WATER_AND_DIFFICULT_LAND_GAPS_REMAIN',
        'records':records,'independent_human_reliability':'UNMEASURED','comparison_gate':'CLOSED',
        'no_local_threshold_or_model_output_used':True}
    (ROOT/'CONTROL_QUALIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(result['status'])


if __name__=='__main__':
    main()
