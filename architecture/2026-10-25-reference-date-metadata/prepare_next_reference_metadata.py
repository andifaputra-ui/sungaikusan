"""Prepare, but do not submit, two frozen-site Planet metadata queries and search AOIs."""
from pathlib import Path
import json
import hashlib
from shapely.geometry import box,mapping
from shapely.ops import transform
from pyproj import Transformer

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent/'REFERENCE_LED_DEVELOPMENT_20261025'


def main() -> None:
    """No credentials, authentication, network, previews, orders or pixel reads."""
    nominations=json.loads((BRANCH/'NOMINATION_FREEZE.json').read_text())['records']
    to_ll=Transformer.from_crs(32750,4326,always_xy=True).transform
    features=[];queries=[]
    for row in nominations:
        if row['id'] not in ['N03','N04']:
            continue
        x,y=row['centre_epsg32750'];geometry=mapping(transform(to_ll,box(x-245,y-245,x+245,y+245)))
        features.append({'type':'Feature','properties':{'id':row['id'],'role':'METADATA_SEARCH_ONLY',
            'frozen_target_SAR_interval_UTC':['2025-05-11T22:00:24Z','2025-05-11T22:00:49Z'],
            'context_width_m':490,'primary_support_m':30,'no_reference_class':True},'geometry':geometry})
        queries.append({'nomination':row['id'],'endpoint':'https://api.planet.com/data/v1/quick-search',
            'query_parameters':{'_page_size':50,'_sort':'acquired asc'},
            'body':{'item_types':['PSScene'],'filter':{'type':'AndFilter','config':[
                {'type':'GeometryFilter','field_name':'geometry','config':geometry},
                {'type':'DateRangeFilter','field_name':'acquired','config':{
                    'gte':'2025-05-10T00:00:00Z','lt':'2025-05-13T00:00:00Z'}}]}},
            'no_filter_by_cloud_class_or_detector':True,'no_permission_filter_initially':True,
            'reason':'List existence separately from asset-specific permissions; prioritize missing before-target evidence after full metadata inventory, no class-based selection',
            'candidate_order':'Pre-target first, then absolute acquisition offset, then source ID; retain after-target and inaccessible records explicitly',
            'maximum_records':50,'maximum_search_response_body_bytes':2*1024**2,
            'no_automatic_pagination':True,'not_executed':True})
    plan={'status':'TARGETED_METADATA_ONLY_OPTICAL_ACCESS_PROPOSAL; NOT_EXECUTED','queries':queries,
        'sites_and_target_date_unchanged':True,'new_source_order':False,'acquisition_or_activation':False,
        'no_thumbnail_tile_or_quicklook_requests':True,
        'asset_metadata_followup':'For at most2pre-target candidates per object, inspect published asset names/status/permissions only; never activate or download. Record RGB/NIR, quality mask, native support and original IDs.',
        'metadata_search_maximum_body_bytes':4*1024**2,'asset_metadata_maximum_body_bytes':4*1024**2,
        'quota_gate':'No download/order/activation until actual historical entitlement and account/order charging terms for the selected assets/AOI are verified. Metadata permission is not a quota guarantee.',
        'absence_rules':'No available scenes, no permissions, no radiometrically suitable assets, incomplete footprint and technical access failure are distinct outcomes. None becomes non-water or a replacement site.',
        'interpretation_gate':'Metadata cannot establish local clarity, W/N state or target-time transfer. No automatic fixed-hour rule.',
        'auth':'Use an authorized existing authenticated route if available; no credentials in logs/repo/chat. Browser/account access has not been verified in this step.',
        'final_validation':'SEALED; development-only frozen objects',
        'nomination_register_sha256':hashlib.sha256((BRANCH/'NOMINATION_FREEZE.json').read_bytes()).hexdigest(),
        'official_docs':['https://docs.planet.com/develop/apis/data/item-search/',
            'https://docs.planet.com/develop/apis/data/items/']}
    (ROOT/'PROPOSED_PLANET_METADATA_CHECK.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
    (ROOT/'PLANET_METADATA_SEARCH_AOIS.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2)+'\n',encoding='utf-8')
    print('PREPARED2_METADATA_QUERIES; NOT_SUBMITTED; NO_PIXELS')


if __name__=='__main__':
    main()
