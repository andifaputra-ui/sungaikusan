"""Audit saved Planet opportunities, spatial coverage and access without network/pixel access."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
from shapely.geometry import shape, box
from shapely.ops import transform
from pyproj import Transformer

ROOT = Path(__file__).resolve().parent
ATTEMPT = ROOT / 'ATTEMPT_01'
BRANCH = ROOT.parent / 'REFERENCE_LED_DEVELOPMENT_20261025'
TARGET = datetime(2025, 5, 11, 22, 0, 24, tzinfo=timezone.utc)


def read(path: Path) -> dict:
    """Read saved sanitized metadata only."""
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path: Path) -> str:
    """Hash provenance without rewriting original responses."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    """Keep footprint, timing, permissions and observable-reference state separate."""
    execution = read(ATTEMPT / 'STATUS.json')
    account = read(ATTEMPT / 'ACCOUNT.json')
    lock = read(ATTEMPT / 'PLAN_LOCK.json')
    assert execution['status'] == 'METADATA_INVENTORY_COMPLETE'
    assert lock['worker_sha256'] == sha(ROOT / 'query_targeted_metadata.py')
    assert account['requests'] == 5 and account['reserved_bytes'] <= account['maximum_bytes']
    assert account['orders'] == account['activation_calls'] == account['pixel_or_thumbnail_calls'] == 0
    protected = []
    for directory, name in [(BRANCH, 'BRANCH_LOCK.json'),
                             (BRANCH / 'FOUR_CHIP_EXECUTION', 'REFERENCE_RESPONSE_LOCK.json')]:
        for file, expected in read(directory / name)['files'].items():
            assert sha(directory / file) == expected
            protected.append(str(directory / file))
    centres = {x['id']: x['centre_epsg32750'] for x in read(BRANCH / 'NOMINATION_FREEZE.json')['records']}
    projection = Transformer.from_crs(4326, 32750, always_xy=True).transform
    records = []
    summaries = {}
    for site in ['N03', 'N04']:
        inventory = read(ATTEMPT / (site + '_INVENTORY.json'))
        assert not inventory['pagination_incomplete']
        x, y = centres[site]
        supports = {str(width): box(x-width/2, y-width/2, x+width/2, y+width/2)
                    for width in [10, 30, 50, 90, 490]}
        site_records = []
        for item in inventory['items']:
            geom = shape(item['geometry'])
            assert geom.is_valid and not geom.is_empty
            metric = transform(projection, geom)
            assert metric.is_valid and not metric.is_empty
            acquired = datetime.fromisoformat(item['properties']['acquired'].replace('Z', '+00:00'))
            offset = (acquired - TARGET).total_seconds() / 3600
            asset_path = ATTEMPT / (site + '_' + item['id'] + '_ASSETS.json')
            asset = read(asset_path) if asset_path.exists() else None
            entry = {'site': site, 'id': item['id'], 'acquired_utc': acquired.isoformat(),
                     'signed_offset_hours_from_SAR_start': offset,
                     'side': 'BEFORE' if offset < 0 else 'AFTER',
                     'scene_download_permissions': item['permissions'],
                     'asset_metadata_checked': asset is not None,
                     'asset_entries_returned': len(asset.get('assets', {})) if asset else None,
                     'asset_result': asset.get('status', 'EMPTY_ASSET_LIST' if not asset.get('assets') else 'ASSETS_LISTED') if asset else 'NOT_CHECKED_BY_FIXED_BOUND',
                     'full_metadata_coverage_by_width_m': {k: metric.covers(v) for k, v in supports.items()},
                     'intersection_fraction_by_width_m': {k: metric.intersection(v).area / v.area for k, v in supports.items()},
                     'ground_control_metadata': item['properties'].get('ground_control'),
                     'pixel_posting_m_metadata': item['properties'].get('pixel_resolution'),
                     'gsd_m_metadata': item['properties'].get('gsd'),
                     'quality_category_metadata': item['properties'].get('quality_category'),
                     'whole_scene_clear_percent_not_local_clarity': item['properties'].get('clear_percent'),
                     'whole_scene_light_haze_percent': item['properties'].get('light_haze_percent'),
                     'strip_id': item['properties'].get('strip_id'),
                     'no_local_clarity_state_or_registration_verified': True}
            # Coverage of a larger nested square cannot exceed that of a smaller one.
            booleans = [entry['full_metadata_coverage_by_width_m'][str(k)] for k in [10, 30, 50, 90, 490]]
            assert booleans == sorted(booleans, reverse=True)
            site_records.append(entry)
        records.extend(site_records)
        sides = Counter(r['side'] for r in site_records)
        summaries[site] = {'scene_items': len(site_records), 'before_items': sides['BEFORE'],
            'after_items': sides['AFTER'], 'distinct_strip_groups': len({r['strip_id'] for r in site_records}),
            'nearest_before_hours': min((-r['signed_offset_hours_from_SAR_start'] for r in site_records if r['side'] == 'BEFORE'), default=None),
            'nearest_after_hours': min((r['signed_offset_hours_from_SAR_start'] for r in site_records if r['side'] == 'AFTER'), default=None),
            'full90m_coverage_items': sum(r['full_metadata_coverage_by_width_m']['90'] for r in site_records),
            'full490m_coverage_items': sum(r['full_metadata_coverage_by_width_m']['490'] for r in site_records),
            'permission_bearing_scene_items': sum(bool(r['scene_download_permissions']) for r in site_records),
            'asset_metadata_checks': sum(r['asset_metadata_checked'] for r in site_records),
            'nonempty_checked_asset_lists': sum(bool(r['asset_entries_returned']) for r in site_records),
            'local_reference_clarity_state_transfer': 'UNASSESSED_NO_PIXELS'}
    receipts = [read(path) for path in sorted(ATTEMPT.glob('RECEIPT_*.json'))]
    assert len(receipts) == account['requests']
    assert sum(r['body_bytes'] for r in receipts) == account['completed_body_bytes']
    assert all(r['http_status'] == 200 and not r['redirects_followed'] for r in receipts)
    summary = {'date_local': '2026-10-27',
        'status': 'CATALOGUE_OPPORTUNITIES_FOUND; CURRENT_ACCOUNT_ASSET_ACCESS_NOT_AVAILABLE_IN_CHECKED_METADATA',
        'sites': summaries, 'scene_items': len(records),
        'distinct_site_strip_groups_not_claimed_statistically_independent': sum(v['distinct_strip_groups'] for v in summaries.values()),
        'scene_items_with_download_permissions': sum(bool(r['scene_download_permissions']) for r in records),
        'checked_asset_lists': sum(r['asset_metadata_checked'] for r in records),
        'nonempty_checked_asset_lists': sum(bool(r['asset_entries_returned']) for r in records),
        'requests': account['requests'], 'response_body_bytes': account['completed_body_bytes'],
        'reserved_metadata_bytes': account['reserved_bytes'],
        'reference_charge_bytes_unchanged': 72351744,
        'new_imagery_predictions_labels_orders': 0,
        'protected_files_verified': len(protected),
        'source_pixel_validity_and_absolute_registration': 'UNASSESSED',
        'temporal_transfer_and_reference_eligibility': 'UNCHANGED_UNKNOWN',
        'comparison_gate': 'CLOSED', 'scientific_job_running': False,
        'no_claim_that_the_Education_licence_itself_expired': True}
    (ROOT / 'METADATA_OPPORTUNITY_LEDGER.json').write_text(json.dumps({'records': records}, indent=2)+'\n', encoding='utf-8')
    (ROOT / 'METADATA_FINDINGS_SUMMARY.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
