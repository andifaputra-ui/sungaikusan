# Metadata-only probe, executed 2026-10-23 through initialized geeViz.
# No pixel reducers, getDownloadURL, map display, export, classifier or sample.
# Requires ee initialized to an authorized project before running standalone.
import ee
import json
reset_aoi_20261023=ee.Geometry.Rectangle([115.63,-3.65,116.04,-3.39],geodesic=False)
reset_opera_20261023=ee.ImageCollection('OPERA/DSWX/L3_V1/S1').filterBounds(reset_aoi_20261023).filterDate('2024-08-01','2026-01-01')
reset_opera_summary_20261023=ee.Dictionary({'count':reset_opera_20261023.size(),'min_time':reset_opera_20261023.aggregate_min('system:time_start'),'max_time':reset_opera_20261023.aggregate_max('system:time_start'),'first_ids':reset_opera_20261023.limit(3).aggregate_array('system:index')})
print(json.dumps(reset_opera_summary_20261023.getInfo()))

print(json.dumps(ee.Dictionary({'unique_timestamps':reset_opera_20261023.aggregate_count_distinct('system:time_start'),'bands':reset_opera_20261023.first().bandNames(),'properties':reset_opera_20261023.first().propertyNames()}).getInfo()))

print(json.dumps(ee.Dictionary({'pass_direction_histogram':reset_opera_20261023.aggregate_histogram('RTC_ORBIT_PASS_DIRECTION'),'product_version_histogram':reset_opera_20261023.aggregate_histogram('DSWX_PRODUCT_VERSION'),'tile_histogram':reset_opera_20261023.map(lambda i:i.set('tile',ee.String(i.get('system:index')).slice(0,6))).aggregate_histogram('tile'),'sample_spatial_coverage':reset_opera_20261023.first().get('SPATIAL_COVERAGE')}).getInfo()))

reset_opera_dates_20261023=reset_opera_20261023.map(lambda i:i.set('target_utc_day',ee.Date(i.get('system:time_start')).format('YYYY-MM-dd')))
print(json.dumps(ee.Dictionary({'dates':reset_opera_dates_20261023.aggregate_histogram('target_utc_day'),'ids':reset_opera_20261023.aggregate_array('system:index')}).getInfo()))
