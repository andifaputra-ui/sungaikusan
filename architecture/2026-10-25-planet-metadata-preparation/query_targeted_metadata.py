"""Two fixed-site metadata queries only; no pixels, activation, orders or raw credentials saved."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
import hashlib
import json
import os
import re
import sys
import requests

ROOT = Path(__file__).resolve().parent
PLAN_PATH = ROOT.parent / 'REFERENCE_DATE_SAR_FEASIBILITY_20261025/PROPOSED_PLANET_METADATA_CHECK.json'
HOST = 'https://api.planet.com'
MAX_TOTAL = 8 * 1024**2
SEARCH_LIMIT = 2 * 1024**2
ASSET_LIMIT = 1024**2
TARGET = datetime(2025, 5, 11, 22, 0, 24, tzinfo=timezone.utc)
SCIENTIFIC_PROPERTIES = {'acquired', 'published', 'updated', 'item_type', 'provider',
    'satellite_id', 'instrument', 'pixel_resolution', 'gsd', 'rows', 'columns',
    'epsg_code', 'ground_control', 'view_angle', 'quality_category', 'cloud_cover',
    'clear_percent', 'clear_confidence_percent', 'cloud_percent', 'shadow_percent',
    'heavy_haze_percent', 'light_haze_percent', 'visible_percent', 'anomalous_pixels',
    'strip_id', 'sun_azimuth', 'sun_elevation', 'processing_level', 'usable_data'}


def save(path: Path, data: dict) -> None:
    """Write sanitized scientific/accounting records only."""
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def allowed(method: str, url: str) -> None:
    """Restrict credentials and calls to exact metadata-only HTTPS endpoints."""
    parsed = urlparse(url)
    if (parsed.scheme != 'https' or parsed.netloc != 'api.planet.com'
            or parsed.query or parsed.fragment or parsed.username or parsed.password):
        raise ValueError('BLOCKED_ENDPOINT')
    if method == 'POST' and parsed.path == '/data/v1/quick-search':
        return
    if method == 'GET' and re.fullmatch(
            r'/data/v1/item-types/PSScene/items/[A-Za-z0-9_-]+/assets', parsed.path):
        return
    raise ValueError('BLOCKED_ENDPOINT')


def sanitized_item(item: dict) -> dict:
    """Retain every item but discard URLs, undocumented fields and account data."""
    return {'id': item['id'], 'type': item.get('type'), 'geometry': item.get('geometry'),
            'permissions': item.get('_permissions', []),
            'properties': {k: v for k, v in item.get('properties', {}).items()
                           if k in SCIENTIFIC_PROPERTIES}}


def sanitized_assets(assets: dict) -> dict:
    """Asset status/permissions are metadata; never retain location or activation links."""
    return {name: {key: value[key] for key in ['status', '_permissions', 'type'] if key in value}
            for name, value in assets.items()
            if not name.startswith('_') and isinstance(value, dict)}


def select_pre_target(items: list[dict]) -> list[dict]:
    """Rank at most two before-target items by time and ID, never state or cloud content."""
    def timestamp(item: dict) -> datetime:
        return datetime.fromisoformat(item['properties']['acquired'].replace('Z', '+00:00'))
    before = [item for item in items if timestamp(item) < TARGET]
    return sorted(before, key=lambda x: ((TARGET - timestamp(x)).total_seconds(), x['id']))[:2]


def read_bounded(response: requests.Response, limit: int) -> bytes:
    """Never read past a reserved allowance; reaching it stops without assuming completeness."""
    body = bytearray()
    while len(body) < limit:
        part = response.raw.read(min(16384, limit - len(body)), decode_content=True)
        if not part:
            return bytes(body)
        body.extend(part)
    raise RuntimeError('RESPONSE_REACHED_CAP_INCOMPLETE')


class Client:
    """Single bounded attempt, with pessimistic per-request reservations and no retries."""
    def __init__(self, key: str, destination: Path) -> None:
        self.key = key
        self.destination = destination
        self.account = {'requests': 0, 'reserved_bytes': 0, 'completed_body_bytes': 0,
                        'maximum_bytes': MAX_TOTAL, 'orders': 0, 'activation_calls': 0,
                        'pixel_or_thumbnail_calls': 0,
                        'covered_by_existing_metadata_reserve': True}
        self.session = requests.Session()
        self.session.trust_env = False

    def request(self, method: str, path: str, cap: int, body: dict | None = None) -> dict:
        """Authenticate only to Planet; reject redirects before any follow-up access."""
        url = HOST + path
        allowed(method, url)
        if self.account['requests'] >= 6 or self.account['reserved_bytes'] + cap > MAX_TOTAL:
            raise RuntimeError('REQUEST_OR_CUMULATIVE_BOUND')
        self.account['requests'] += 1
        self.account['reserved_bytes'] += cap
        save(self.destination / 'ACCOUNT.json', self.account)
        params = {'_page_size': 50, '_sort': 'acquired asc'} if method == 'POST' else None
        try:
            with self.session.request(method, url, json=body, params=params, auth=(self.key, ''),
                    timeout=(10, 35), stream=True, allow_redirects=False) as response:
                if response.status_code != 200:
                    raise RuntimeError('METADATA_HTTP_' + str(response.status_code))
                data = read_bounded(response, cap)
                self.account['completed_body_bytes'] += len(data)
                save(self.destination / 'ACCOUNT.json', self.account)
                record = {'method': method, 'path': path, 'http_status': response.status_code,
                          'body_bytes': len(data), 'body_sha256': hashlib.sha256(data).hexdigest(),
                          'retrieved_utc': datetime.now(timezone.utc).isoformat(),
                          'raw_response_not_saved': True, 'redirects_followed': False}
                save(self.destination / f'RECEIPT_{self.account["requests"]:02}.json', record)
                return json.loads(data)
        except requests.RequestException:
            raise RuntimeError('NETWORK_FAILURE_RESERVED_NO_RETRY') from None


def validate_plan(plan: dict) -> None:
    """Check the frozen two-site/date/type scope before any credential-bearing request."""
    assert [q['nomination'] for q in plan['queries']] == ['N03', 'N04']
    for query in plan['queries']:
        assert query['endpoint'] == HOST + '/data/v1/quick-search'
        assert query['body']['item_types'] == ['PSScene']
        config = query['body']['filter']['config']
        assert [x['type'] for x in config] == ['GeometryFilter', 'DateRangeFilter']
        assert config[1]['config'] == {'gte': '2025-05-10T00:00:00Z', 'lt': '2025-05-13T00:00:00Z'}


def verify_freeze() -> None:
    """Match the previous completion hash and original nomination register before access."""
    audit = json.loads((PLAN_PATH.parent / 'COMPLETION_AUDIT.json').read_text(encoding='utf-8'))
    if hashlib.sha256(PLAN_PATH.read_bytes()).hexdigest() != audit['files'][PLAN_PATH.name]:
        raise RuntimeError('FROZEN_QUERY_CHANGED')
    plan = json.loads(PLAN_PATH.read_text(encoding='utf-8'))
    nominations = ROOT.parent / 'REFERENCE_LED_DEVELOPMENT_20261025/NOMINATION_FREEZE.json'
    if hashlib.sha256(nominations.read_bytes()).hexdigest() != plan['nomination_register_sha256']:
        raise RuntimeError('FROZEN_NOMINATIONS_CHANGED')


def main() -> int:
    """Stop explicitly on auth failure; never convert access failure into imagery absence."""
    plan = json.loads(PLAN_PATH.read_text(encoding='utf-8'))
    validate_plan(plan)
    verify_freeze()
    key = os.environ.get('PL_API_KEY', '')
    if not key:
        print('MANUAL_API_AUTH_REQUIRED; NO_REQUEST_MADE')
        return 2
    destination = ROOT / 'ATTEMPT_01'
    destination.mkdir(exist_ok=False)
    save(destination / 'PLAN_LOCK.json', {'sha256': hashlib.sha256(PLAN_PATH.read_bytes()).hexdigest(),
        'worker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'no_role_site_date_or_response_change': True, 'no_imagery_authorization': True})
    client = Client(key, destination)
    try:
        inventories = []
        # Finish both searches before selecting asset metadata; no class/clarity filtering.
        for query in plan['queries']:
            result = client.request('POST', '/data/v1/quick-search', SEARCH_LIMIT, query['body'])
            if result.get('type') != 'FeatureCollection' or not isinstance(result.get('features'), list):
                raise RuntimeError('UNEXPECTED_SEARCH_SCHEMA')
            items = [sanitized_item(x) for x in result.get('features', [])]
            if len(items) > 50:
                raise RuntimeError('RECORD_BOUND_EXCEEDED')
            incomplete = bool(result.get('_links', {}).get('_next'))
            inventory = {'site': query['nomination'], 'items': items, 'item_count': len(items),
                         'pagination_incomplete': incomplete,
                         'status': 'INCOMPLETE' if incomplete else ('ITEMS_FOUND' if items else 'NO_ITEM_RETURNED'),
                         'no_pixel_evidence': True}
            save(destination / (query['nomination'] + '_INVENTORY.json'), inventory)
            inventories.append(inventory)
        for inventory in inventories:
            if inventory['pagination_incomplete']:
                continue
            for item in select_pre_target(inventory['items']):
                try:
                    asset_result = client.request('GET',
                        '/data/v1/item-types/PSScene/items/' + item['id'] + '/assets', ASSET_LIMIT)
                except RuntimeError as error:
                    if str(error) != 'METADATA_HTTP_403':
                        raise
                    save(destination / (inventory['site'] + '_' + item['id'] + '_ASSETS.json'),
                         {'id': item['id'], 'status': 'ASSET_METADATA_ACCESS_FORBIDDEN',
                          'not_an_imagery_absence_or_content_result': True})
                    continue
                save(destination / (inventory['site'] + '_' + item['id'] + '_ASSETS.json'),
                     {'id': item['id'], 'assets': sanitized_assets(asset_result),
                      'permission_is_not_quota_or_clarity_proof': True})
        save(destination / 'STATUS.json', {'status': 'METADATA_INVENTORY_COMPLETE',
            'any_incomplete_inventory': any(x['pagination_incomplete'] for x in inventories),
            'new_reference_eligibility': False, 'comparison_gate': 'CLOSED',
            'no_orders_activation_download_or_label': True})
        print('METADATA_INVENTORY_COMPLETE; NO_PIXELS; NO_ORDERS')
        return 0
    except (RuntimeError, ValueError, KeyError, AssertionError, OSError) as error:
        # Do not log exception objects that could contain request/credential details.
        safe = str(error) if isinstance(error, RuntimeError) else type(error).__name__
        save(destination / 'STATUS.json', {'status': 'STOPPED_NOT_AN_ABSENCE_RESULT',
            'reason': safe, 'no_retry': True, 'comparison_gate': 'CLOSED'})
        print('STOPPED_NOT_AN_ABSENCE_RESULT', safe)
        return 1
    finally:
        client.session.close()
        client.key = ''


if __name__ == '__main__':
    sys.exit(main())
