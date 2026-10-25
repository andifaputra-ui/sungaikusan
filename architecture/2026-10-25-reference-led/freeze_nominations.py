"""Freeze four development nominations and assess existing footprint reuse only."""
from __future__ import annotations
from pathlib import Path
import json
import hashlib
from shapely.geometry import box
from pyproj import Transformer

ROOT=Path(__file__).resolve().parent
C2=ROOT.parent
PARENT=C2/'LINKED_DEVELOPMENT_COMPARISON_20261024'


def read(path: Path) -> dict | list:
    """Load recorded source metadata without pixels or reference answers."""
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main() -> None:
    """Keep all nominations, even if subsequent reference qualification fails."""
    destination=ROOT/'NOMINATION_FREEZE.json'
    if destination.exists():
        raise RuntimeError('Nomination register exists; no silent relocation')
    plan=read(PARENT/'REFERENCE_SOURCE_PLAN_V2.json')['requests']
    current={r['id']:r for r in plan}
    key=read(PARENT/'PRIVATE_REVIEW_KEY.json')['aliases']
    alias_to_source={r['neutral_id']:r['original_case'] for r in key}
    def original(alias: str) -> dict:
        return next(r for r in plan if r['case_id']==alias_to_source[alias])
    def centre(row: dict) -> tuple[float,float]:
        bounds=row['support']['bounds_epsg32750']
        return (bounds[0]+bounds[2])/2,(bounds[1]+bounds[3])/2
    coast=centre(original('R21'));land=centre(original('R13'))
    runway=centre(next(r for r in plan if r['case_id']=='D06_2025-09-20'))
    legacy=read(ROOT/'LEGACY_SCREEN_FREEZE.json')['items'][28]
    scopes={r['id']:r for r in read(C2/'DEVELOPMENT_IMPLEMENTATION_20261009/SAVED_CHIP_SCOPE_MANIFEST.json')}
    old=scopes[legacy['evidence_id']]['bounds']
    # Manual visual nomination: native col10,row15 within the largest resolved basin,
    # not the original probability-sample centre or a SAR-selected point.
    pond=(old[0]+10*(10+0.5),old[3]-10*(15+0.5))
    nominees=[
        ('N01',coast[0]+120,coast[1],'COASTAL_OPEN_WATER_CONTROL',
            'Saved calibrated R21 S2 before/after views show interior east of shoreline; control only, not inland flood validation'),
        ('N02',*land,'ORDINARY_VISIBLE_LAND_CONTROL',
            'Reuse existing calibrated R13 broad vegetation case; original response retained, not reinterpreted for predictions'),
        ('N03',*pond,'INLAND_BOUNDED_BASIN_WATER_HYPOTHESIS',
            'Content-informed optical nomination from L29 native col10,row15; no mining/chemical or definitive water inference from shape/darkness'),
        ('N04',*runway,'MAPPED_RUNWAY_DIFFICULT_LAND_HYPOTHESIS',
            'Existing independent runway geography, new May11 target opportunity; actual dated surface state remains unqualified')]
    grid=read(C2.parent/'PHASE_1_6/FINAL_L1_GRID.json')
    l1=box(*grid['projected_bounds']);to_ll=Transformer.from_crs(32750,4326,always_xy=True)
    records=[]
    for identifier,x,y,context,reason in nominees:
        reused=[]
        for row in plan:
            if 'item_id' not in row:
                continue
            t=row['chip_grid']['transform'];bounds=box(t[2],t[5]-490,t[2]+490,t[5])
            if bounds.covers(box(x-45,y-45,x+45,y+45)):
                reused.append({'id':row['id'],'provider':row['provider'],
                    'optical_utc':row['optical_datetime'],'parent_case':row['case_id']})
        col=(x-grid['affine_transform'][2])/10-0.5
        line=(grid['affine_transform'][5]-y)/10-0.5
        if abs(col-round(col))>1e-6 or abs(line-round(line))>1e-6:
            raise RuntimeError('Nomination centre leaves accepted10m indexing lattice')
        records.append({'id':identifier,'target_S1_date':'2025-05-11','centre_epsg32750':[x,y],
            'centre_lonlat':list(to_ll.transform(x,y)),'C1_index_col_row':[round(col),round(line)],
            'context_hypothesis':context,'nomination_reason':reason,
            'support_m_primary':30,'support_sensitivity_m':[10,50],
            'position_scenarios_m':[-20,-10,0,10,20],
            'full_position_neighbourhood_inside_L1':bool(l1.covers(box(x-45,y-45,x+45,y+45))),
            'L1_is_processing_envelope_not_final_population_membership':True,
            'saved_current_views_covering_full90m_neighbourhood':reused,
            'qualification':'PENDING_OPTICAL_SUPPORT_AND_TIME; NOT_CLASS_TRUTH',
            'development_only':True,'no_new_SAR_values_or_predictions_used':True})
    output={'status':'EXACT_NOMINATIONS_FROZEN_BEFORE_NEW_PREDICTIONS',
        'systems':4,'date_supports':4,'target_date':'2025-05-11',
        'discovery':'INDEPENDENT_OPTICAL_CONTENT_AND_GEOGRAPHY; PURPOSIVE_DEVELOPMENT_ONLY',
        'previous_panel_unchanged':True,'records':records,
        'new_imagery_acquired':0,'new_SAR_processing':0,
        'domain_version':grid['domain_version_id'],
        'inference':'No inclusion probabilities or population accuracy inferred; repeated/nearby systems not assumed independent'}
    destination.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    (ROOT/'NOMINATION_FREEZE.sha256').write_text(hashlib.sha256(destination.read_bytes()).hexdigest()+'\n',encoding='utf-8')
    for r in records:
        print(r['id'],r['context_hypothesis'],r['centre_lonlat'],
            'existing_complete90m_views',len(r['saved_current_views_covering_full90m_neighbourhood']))


if __name__=='__main__':
    main()
