"""Account explicit visual annotations without reading imagery or model predictions."""
from __future__ import annotations
from pathlib import Path
from collections import Counter
import hashlib
import json
import numpy as np

ROOT=Path(__file__).resolve().parent


def scenarios(pattern: list[str],size: int) -> dict:
    """Return complete joint vectors and conditional marginal bounds for fixed supports."""
    grid=np.array([list(row) for row in pattern])
    if grid.shape!=(9,9) or not np.isin(grid,list('WNOU')).all() or size not in {10,30,50}:
        raise ValueError('Invalid explicit visual annotation/support')
    radius=(size//10)//2;values=[]
    for dy in [-20,-10,0,10,20]:
        for dx in [-20,-10,0,10,20]:
            c=4+dx//10;r=4-dy//10
            part=grid[r-radius:r+radius+1,c-radius:c+radius+1]
            fractions={label:float((part==label).mean()) for label in 'WNOU'}
            if abs(sum(fractions.values())-1)>1e-12:
                raise RuntimeError('Joint fraction conservation failed')
            values.append({'dx_m':dx,'dy_m':dy,**fractions})
    bounds={label:[min(v[label] for v in values),max(v[label] for v in values)] for label in 'WNOU'}
    return {'support_m':size,'scenarios':values,'nominal':values[12],'resolved_bounds':bounds,
        'possible_water_bounds':[bounds['W'][0],max(v['W']+v['O']+v['U'] for v in values)],
        'possible_nonwater_bounds':[bounds['N'][0],max(v['N']+v['O']+v['U'] for v in values)],
        'bounds_are_conditional_not_statistical':True}


def main() -> None:
    """Retain all 96 source slots and24 cases; summarize only development response information."""
    source=ROOT/'ASSISTANT_OPTICAL_REVIEW.json'
    responses=json.loads(source.read_text(encoding='utf-8'))
    patterns=responses['patterns'];rows=[];cases=[]
    for record in responses['records']:
        metadata=json.loads((ROOT/'BLINDED_OPTICAL_PACKET'/(record['id']+'_metadata.json')).read_text(encoding='utf-8'))
        observations=[]
        for index,label in enumerate(record['observations']):
            actual=metadata['observations'][index]
            missing=actual.get('status')=='NO_FIXED_SEARCH_OPPORTUNITY'
            if (label=='MISSING')!=missing:
                raise RuntimeError('Visual return dropped or invented a missing source')
            row={'neutral_id':record['id'],'observation':f'O{index+1:02d}','visual_pattern':label,
                'optical_utc':actual.get('optical_utc'),'native_resolution_m':actual.get('nominal_native_resolution_m'),
                'response_status':'MISSING_RETAINED' if missing else 'ASSISTANT_VISUAL_FIRST_PASS',
                'supports':{str(size):scenarios(patterns.get(label,patterns['U']),size) for size in [10,30,50]},
                'notes':record['notes'],'independent_reader':False}
            rows.append(row);observations.append(row)
        eligible=record['tier']=='E2'
        target={}
        for size in [10,30,50]:
            # The documented two bracketing S2 observations are independent dates, not duplicate generations.
            offered=[o['supports'][str(size)] for o in observations[:2]]
            target[str(size)]={
                'continuity_conditional_possible_water_hull':[
                    min(o['possible_water_bounds'][0] for o in offered),max(o['possible_water_bounds'][1] for o in offered)] if eligible else [0,1],
                'continuity_conditional_resolved_water_hull':[
                    min(o['resolved_bounds']['W'][0] for o in offered),max(o['resolved_bounds']['W'][1] for o in offered)] if eligible else [0,1],
                'transient_allowed_water_bound':[0,1],
                'eligibility':'CONDITIONAL_ONLY' if eligible else 'UNKNOWN'}
        cases.append({'neutral_id':record['id'],'evidence_tier':record['tier'],
            'temporal_transfer':'TRANSFERABLE_CONDITIONAL_ASSUMPTIONS_ONLY' if eligible else 'UNKNOWN',
            'supports':target,'event_support':'NONE','absolute_registration':'UNMEASURED','notes':record['notes']})
    summary={'status':'BOUNDED_REFERENCE_INFORMATION_RECOVERED; COMPARISON_ADEQUACY_NOT_DEMONSTRATED',
        'all_case_count':24,'all_source_slots':96,'acquired_visual_views':78,'missing_slots_preserved':18,
        'visual_dispositions':dict(Counter(row['visual_pattern'] for row in rows)),
        'temporal_tiers':dict(Counter(case['evidence_tier'] for case in cases)),
        'conditional_cases':sum(c['evidence_tier']=='E2' for c in cases),'E3_cases':0,
        'unconditional_acquisition_time_reference_count':0,'independent_interpreter_reliability':'UNMEASURED',
        'supports':{str(size):{
            'optical_views_with_positive_resolved_W_nominal':sum(r['supports'][str(size)]['nominal']['W']>0 for r in rows),
            'optical_views_with_positive_resolved_N_nominal':sum(r['supports'][str(size)]['nominal']['N']>0 for r in rows),
            'E2_cases_with_conditional_possible_water_upper_below_one':sum(c['evidence_tier']=='E2' and c['supports'][str(size)]['continuity_conditional_possible_water_hull'][1]<1 for c in cases),
            'E2_cases_with_positive_water_lower_across_displacements':sum(c['evidence_tier']=='E2' and c['supports'][str(size)]['continuity_conditional_possible_water_hull'][0]>0 for c in cases)
        } for size in [10,30,50]},
        'comparison_gate':'CLOSED','no_candidate_scores_read':True,'no_old_response_modified':True,
        'panel_is_not_probability_accuracy_sample':True}
    output={'manual_response_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'summary':summary,
        'observations':rows,'cases':cases}
    (ROOT/'BOUNDED_OPTICAL_RESPONSE_LEDGER.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    (ROOT/'REFERENCE_RESPONSE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
