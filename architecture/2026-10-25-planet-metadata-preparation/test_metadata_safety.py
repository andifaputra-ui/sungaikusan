"""Offline access and selection safeguards; no real key or HTTP request is used."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock
import io
import json
import unittest
from query_targeted_metadata import (Client, allowed, read_bounded, sanitized_item,
    sanitized_assets, select_pre_target, validate_plan, verify_freeze, PLAN_PATH, MAX_TOTAL)


class MetadataSafety(unittest.TestCase):
    """Exercise consequential routes, caps, redaction and outcome-independent candidate order."""

    def test_exact_metadata_routes_and_unsafe_alternatives(self) -> None:
        allowed('POST', 'https://api.planet.com/data/v1/quick-search')
        allowed('GET', 'https://api.planet.com/data/v1/item-types/PSScene/items/20250511_example/assets')
        for method, url in [
            ('POST', 'https://api.planet.com/compute/ops/orders/v2'),
            ('GET', 'https://api.planet.com/data/v1/item-types/PSScene/items/a/assets/x/activate'),
            ('GET', 'https://tiles.planet.com/thumb'),
            ('GET', 'https://api.planet.com.evil/data/v1/item-types/PSScene/items/a/assets'),
            ('GET', 'https://api.planet.com/data/v1/item-types/PSScene/items/a/assets?api_key=fake'),
            ('GET', 'http://api.planet.com/data/v1/item-types/PSScene/items/a/assets'),
            ('GET', 'https://fake@api.planet.com/data/v1/item-types/PSScene/items/a/assets')]:
            with self.assertRaises(ValueError):
                allowed(method, url)

    def test_sanitization_discards_links_credentials_and_account_fields(self) -> None:
        original = {'id': 'example', '_links': {'thumbnail': 'https://x/?key=FAKE_SECRET'},
            '_permissions': ['assets:download'], 'properties': {'acquired': '2025-05-11T00:00:00Z',
            'account_id': 'PRIVATE', 'token': 'FAKE_SECRET', 'gsd': 3}}
        item = sanitized_item(original)
        assets = sanitized_assets({'ortho_analytic_4b_sr': {'status': 'inactive',
            'location': 'https://x/?key=FAKE_SECRET', '_links': {'activate': 'x'},
            '_permissions': ['download']}, '_links': {'self': 'PRIVATE'}})
        encoded = json.dumps([item, assets])
        self.assertNotIn('FAKE_SECRET', encoded)
        self.assertNotIn('PRIVATE', encoded)
        self.assertEqual(assets['ortho_analytic_4b_sr']['status'], 'inactive')

    def test_time_ranking_ignores_cloud_and_state(self) -> None:
        def item(identifier: str, time: str, cloud: float) -> dict:
            return {'id': identifier, 'properties': {'acquired': time, 'cloud_cover': cloud}}
        records = [item('old_clear', '2025-05-10T02:00:00Z', 0),
                   item('near_cloud', '2025-05-11T02:00:00Z', 1),
                   item('tie_B', '2025-05-11T02:00:00Z', 0),
                   item('after', '2025-05-12T02:00:00Z', 0)]
        self.assertEqual([x['id'] for x in select_pre_target(records)], ['near_cloud', 'tie_B'])
        self.assertEqual(select_pre_target([]), [])

    def test_read_cap_no_extra_byte(self) -> None:
        class Raw:
            def __init__(self, data: bytes) -> None:
                self.body = io.BytesIO(data)
            def read(self, size: int, decode_content: bool = True) -> bytes:
                return self.body.read(size)
        short = Mock(raw=Raw(b'abcd'))
        self.assertEqual(read_bounded(short, 5), b'abcd')
        long = Mock(raw=Raw(b'abcdef'))
        with self.assertRaisesRegex(RuntimeError, 'CAP'):
            read_bounded(long, 5)
        self.assertEqual(long.raw.body.tell(), 5)

    def test_redirect_and_budget_rejected_without_followup(self) -> None:
        with TemporaryDirectory() as folder:
            client = Client('FAKE_KEY', Path(folder))
            session = Mock()
            response = Mock(status_code=302)
            context = Mock()
            context.__enter__ = Mock(return_value=response)
            context.__exit__ = Mock(return_value=False)
            session.request.return_value = context
            client.session = session
            with self.assertRaisesRegex(RuntimeError, 'HTTP_302'):
                client.request('POST', '/data/v1/quick-search', 100, {})
            self.assertEqual(session.request.call_count, 1)
            self.assertFalse(session.request.call_args.kwargs['allow_redirects'])
            self.assertEqual(client.account['reserved_bytes'], 100)
            client.account['reserved_bytes'] = MAX_TOTAL
            with self.assertRaisesRegex(RuntimeError, 'BOUND'):
                client.request('POST', '/data/v1/quick-search', 100, {})
            self.assertEqual(session.request.call_count, 1)
            self.assertNotIn('FAKE_KEY', (Path(folder) / 'ACCOUNT.json').read_text())

    def test_original_plan_and_nomination_hashes(self) -> None:
        validate_plan(json.loads(PLAN_PATH.read_text(encoding='utf-8')))
        verify_freeze()


if __name__ == '__main__':
    unittest.main(verbosity=2)
