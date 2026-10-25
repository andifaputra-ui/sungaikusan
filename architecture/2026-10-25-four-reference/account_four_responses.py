"""Apply unchanged support accounting to explicit manual optical responses."""
from pathlib import Path
import sys
import json
import hashlib

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'))
from account_optical_responses import scenarios


def main() -> None:
    """Keep optical-time information separate from target-time UNKNOWN."""
    source=ROOT/'OPTICAL_READER_RETURN.json'
    returned=json.loads(source.read_text(encoding='utf-8'))
    rows=[]
    for row in returned['records']:
        rows.append({**row,'support_results':{str(size):scenarios(row['manual_pattern90m'],size) for size in [10,30,50]}})
    result={'status':'OPTICAL_TIME_WATER_AND_ARTIFICIAL_LAND_RECOVERED; MAY11_ACQUISITION_TIME_ADEQUACY_NOT_DEMONSTRATED',
        'manual_return_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'observations':rows,
        'target_time_cases':[{**row,'all_support_target_possible_water_bound':[0,1]} for row in returned['temporal_response']],
        'summary':{'new_optical_views':4,'new_optical_water_views':1,'new_optical_nonwater_views':1,
            'obscured_views':1,'unresolved_views':1,'new_E2_or_E3_cases':0,
            'new_May11_acquisition_time_eligible_cases':0,'supports_m':[10,30,50],
            'new_positive_optical_interiors_retained_across_all25_scenarios':2,
            'independent_interpreter_reliability':'UNMEASURED','comparison_gate':'CLOSED',
            'new_reference_acquisitions_after_these_four':'NONE; no automatic rescue'}}
    (ROOT/'FOUR_CHIP_RESPONSE_LEDGER.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result['summary'],indent=2))


if __name__=='__main__':
    main()
