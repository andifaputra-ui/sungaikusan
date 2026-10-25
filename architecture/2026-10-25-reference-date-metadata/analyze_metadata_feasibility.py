"""Compare frozen optical dates with bounded raw/product metadata, never SAR values."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json
import re
import hashlib
from shapely.geometry import shape,Polygon,box
from shapely.ops import unary_union,transform
from pyproj import Transformer

ROOT=Path(__file__).resolve().parent
C2=ROOT.parent
BRANCH=C2/'REFERENCE_LED_DEVELOPMENT_20261025'


def read(path: Path) -> dict | list:
    """Read saved catalogue provenance only."""
    return json.loads(path.read_text(encoding='utf-8-sig'))


def utc(value: str) -> datetime:
    """Parse explicit source UTC without local-calendar assumptions."""
    return datetime.fromisoformat(value.replace('Z','+00:00'))


def acquisition_interval(identifier: str) -> tuple[datetime,datetime]:
    """Use actual encoded GRD start/end, preserving degenerate GEE time_end separately."""
    match=re.search(r'_(20\d{6}T\d{6})_(20\d{6}T\d{6})_',identifier)
    if match is None:
        raise ValueError('No known GRD acquisition interval')
    return tuple(datetime.strptime(v,'%Y%m%dT%H%M%S').replace(tzinfo=timezone.utc) for v in match.groups())


def footprint(value: dict) -> Polygon:
    """Convert a metadata ring to a polygon without guessing or repairing geometry."""
    geom=Polygon(value['coordinates']) if value['type']=='LinearRing' else shape(value)
    if not geom.is_valid or geom.is_empty:
        raise ValueError('Invalid catalogue footprint')
    return geom


def umm_footprint(item: dict):
    """Parse recorded UMMG polygons; absence is unknown, never invented support."""
    geometry=item.get('SpatialExtent',{}).get('HorizontalSpatialDomain',{}).get('Geometry',{})
    polygons=[]
    for polygon in geometry.get('GPolygons',[]):
        points=polygon['Boundary']['Points']
        geom=Polygon([(p['Longitude'],p['Latitude']) for p in points])
        if not geom.is_valid:
            raise ValueError('Invalid UMM source polygon')
        polygons.append(geom)
    for rectangle in geometry.get('BoundingRectangles',[]):
        polygons.append(box(rectangle['WestBoundingCoordinate'],rectangle['SouthBoundingCoordinate'],
            rectangle['EastBoundingCoordinate'],rectangle['NorthBoundingCoordinate']))
    return unary_union(polygons) if polygons else None


def parent_identifier(value: str) -> str:
    """Do not count HDF5 and VV/VH/mask files as separate physical burst parents."""
    for ending in ['.h5','_VV.tif','_VH.tif','_mask.tif']:
        if value.endswith(ending):
            return value[:-len(ending)]
    return value


def main() -> None:
    """Produce complete offset/support/provenance tables and retain negative availability."""
    nominations=read(BRANCH/'NOMINATION_FREEZE.json')['records']
    to_ll=Transformer.from_crs(32750,4326,always_xy=True).transform
    units={r['id']:transform(to_ll,box(r['centre_epsg32750'][0]-45,r['centre_epsg32750'][1]-45,
        r['centre_epsg32750'][0]+45,r['centre_epsg32750'][1]+45)) for r in nominations}
    references={'N03':'2025-05-14T02:48:57.751Z','N04':'2025-05-13T02:39:00.548Z'}
    native=read(ROOT/'S1_METADATA.json');asf=read(ROOT/'ASF_METADATA.json')
    assert native['count']==len(native['records'])<40
    assert not read(ROOT/'ASF_METADATA_RECEIPT.json')['limit_reached']
    scenes=[]
    for item in native['records']:
        start,end=acquisition_interval(item['gee_id']);polygon=footprint(item['system:footprint'])
        preferred=(item['platform_number']=='A' and item['relativeOrbitNumber_start']==105
            and item['orbitProperties_pass']=='DESCENDING' and {'VV','VH'}<=set(item['transmitterReceiverPolarisation']))
        scenes.append({'native_id':item['gee_id'],'acquisition_start':start.isoformat(),'acquisition_end':end.isoformat(),
            'platform':item['platform_number'],'absolute_orbit':item['orbitNumber_start'],
            'relative_orbit':item['relativeOrbitNumber_start'],'pass':item['orbitProperties_pass'],
            'polarizations':item['transmitterReceiverPolarisation'],'same_accepted_geometry_and_platform':preferred,
            'degenerate_GEE_time_end_retained':item['system:time_end']==item['system:time_start'],
            'GEE_metadata_time_start_UTC':datetime.fromtimestamp(item['system:time_start']/1000,timezone.utc).isoformat(),
            'GEE_metadata_time_end_UTC':datetime.fromtimestamp(item['system:time_end']/1000,timezone.utc).isoformat(),
            'full90m_metadata_coverage':{key:polygon.covers(unit) for key,unit in units.items()},
            'optical_minus_SAR_start_hours':{key:(utc(date)-start).total_seconds()/3600 for key,date in references.items()},
            'optical_minus_SAR_interval_hours':{key:[(utc(date)-end).total_seconds()/3600,
                (utc(date)-start).total_seconds()/3600] for key,date in references.items()},
            'valid_pixels_and_current_observability':'NOT_TESTED; metadata footprint is not a validity mask'})
    asf_rows=[]
    for feature in asf.get('features',[]):
        item=feature['properties'];identifier=item['fileID'].removesuffix('-GRD_HD').removesuffix('-GRD_HS')
        polygon=footprint(feature['geometry'])
        asf_rows.append({'native_id':identifier,'platform':item.get('platform'),'start':item.get('startTime'),
            'pass':item.get('flightDirection'),'matches_GEE_scene':identifier in {s['native_id'] for s in scenes},
            'full90m_metadata_coverage':{key:polygon.covers(unit) for key,unit in units.items()}})
    rtcs=read(ROOT/'RTC_METADATA.json')['items'];products=read(ROOT/'DSWX_METADATA.json')['items']
    assert read(ROOT/'RTC_METADATA_RECEIPT.json')['complete_within_declared_bound']
    assert read(ROOT/'DSWX_METADATA_RECEIPT.json')['complete_within_declared_bound']
    rtc_by_name={r['umm']['GranuleUR']:r['umm'] for r in rtcs}
    product_rows=[]
    for record in products:
        item=record['umm'];polygon=umm_footprint(item)
        parents={parent_identifier(name) for name in item.get('InputGranules',[])}
        local=[]
        for name,rtc in rtc_by_name.items():
            if name not in parents:
                continue
            geometry=umm_footprint(rtc)
            orbits=[r.get('OrbitNumber') for r in rtc.get('OrbitCalculatedSpatialDomains',[])]
            local.append({'RTC_id':name,'absolute_orbits':orbits,'time':rtc.get('TemporalExtent'),
                'intersecting_frozen_sites':{key:bool(geometry.intersects(unit)) if geometry is not None else None for key,unit in units.items()},
                'fully_covering_frozen_sites':{key:bool(geometry.covers(unit)) if geometry is not None else None for key,unit in units.items()}})
        product_rows.append({'DSWx_id':item['GranuleUR'],'concept_id':record['meta']['concept-id'],
            'temporal':item.get('TemporalExtent'),'unique_RTC_parent_ids':len(parents),'resolved_local_RTC_parents':local,
            'full90m_product_metadata_coverage':{key:bool(polygon.covers(unit)) if polygon is not None else None for key,unit in units.items()},
            'local_parent_orbits_by_site':{key:sorted({orbit for parent in local if parent['intersecting_frozen_sites'][key]
                for orbit in parent['absolute_orbits']}) for key in units},
            'no_product_masks_or_water_classes_read':True})
    source_date_count=len({s['acquisition_start'][:10] for s in scenes})
    public_body_bytes=sum(read(ROOT/(name+'_RECEIPT.json'))['response_body_bytes']
        for name in ['DSWX_METADATA','RTC_METADATA','ASF_METADATA'])
    summary={'status':'NO_CLOSER_COMPATIBLE_IW_GRD_ACQUISITION_FOUND_IN_BOUNDED_PUBLIC_CATALOGUES',
        'window_UTC':['2025-05-07','2025-05-21'],'native_GEE_scenes':len(scenes),'ASF_IW_GRD_records':len(asf_rows),
        'cross_archive_exact_ID_matches':sum(row['matches_GEE_scene'] for row in asf_rows),
        'native_acquisition_days':source_date_count,'DSWx_product_records':len(product_rows),'local_RTC_records':len(rtcs),
        'nearest_existing_scene':scenes[0]['native_id'] if len(scenes)==1 else None,
        'nearest_optical_offsets_hours':scenes[0]['optical_minus_SAR_start_hours'] if len(scenes)==1 else None,
        'alternative_tracks_or_platforms_returned':sum(not s['same_accepted_geometry_and_platform'] for s in scenes),
        'new_images_or_predictions':0,'new_reference_labels':0,'date_substitutions':0,
        'public_metadata_response_body_bytes':public_body_bytes,'GEE_serialized_metadata_bytes':read(ROOT/'S1_METADATA_RECEIPT.json')['recorded_JSON_bytes'],
        'comparison_gate':'CLOSED','frozen_reference_eligibility_unchanged':True,
        'claim_limit':'Bounded catalogue availability for compatibleIWGRD, not proof no mission observation exists in other modes, uncatalogued holdings or outside this window',
        'no_SAR_pixel_validity_or_classifier_equivalence_claim':True}
    lower=utc('2025-05-07T00:00:00Z');upper=utc('2025-05-21T00:00:00Z')
    summary['minimum_absolute_offset_outside_search_window_hours']={key:min((utc(date)-lower).total_seconds(),
        (upper-utc(date)).total_seconds())/3600 for key,date in references.items()}
    summary['window_is_wide_enough_to_find_any_closer_record_if_present_in_queried_catalogues']=all(
        summary['minimum_absolute_offset_outside_search_window_hours'][key]>
        min(abs(s['optical_minus_SAR_start_hours'][key]) for s in scenes) for key in references) if scenes else False
    result={'summary':summary,'native_scenes':scenes,'ASF_crosscheck':asf_rows,'OPERA_local_provenance':product_rows}
    (ROOT/'FEASIBILITY_LEDGER.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (ROOT/'FEASIBILITY_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    for row in product_rows:
        print(row['DSWx_id'],'coverage',row['full90m_product_metadata_coverage'],
            'site_orbits',row['local_parent_orbits_by_site'])


if __name__=='__main__':
    main()
