"""Record the Oct 9 approval and index acquired development metadata, without pixels.

This does not select a new panel, reinterpret old responses, or randomize anything.
Run with the project scientific Python. Inputs are named explicitly, not discovered
by crawling sealed evidence directories. Public backup should omit the detailed pool.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
C2 = HERE.parent
ARCH = C2 / 'VALIDATION_ARCHITECTURE_REDESIGN_20261008'
WAVE = C2 / 'REFERENCE_QUALIFICATION_WAVE2'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, content):
    (HERE / name).write_text(json.dumps(content, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    stamp = datetime.now(timezone.utc).isoformat()
    decision = ARCH / 'ARCHITECTURE_DECISION_FOR_REVIEW.md'
    approval = {
        'recorded_at_utc': stamp,
        'human_decision_date_local': '2026-10-09',
        'architecture_status': 'APPROVED_WITH_DEVELOPMENT_DISCOVERY_AMENDMENT',
        'architecture_document': str(decision).replace('\\', '/'),
        'architecture_sha256': digest(decision),
        'human_instruction_verbatim': 'Continue. Architecture approved. One amendment: during development only, detector-informed or A/B-disagreement-based adversarial case discovery is allowed when useful, provided reference interpretation remains independently derived and all such evidence is permanently development-only. Otherwise proceed autonomously with the architecture you recommended and stop only at genuinely consequential scientific decision boundaries.',
        'supersedes_prospectively': ['architecture approval pending', 'mandatory C1-C7 atlas', 'single official source dependency', 'geographic exclusion for approved sampling-only ancillary access', 'ban on detector-informed DEVELOPMENT discovery'],
        'preserved': ['historical packages and responses', 'source role separation', 'current S1 sigma0/C1 primary observation', 'persistent and new water eligibility', 'UNKNOWN/MIXED and interval responses', 'old exposure facts including B0200_0000 and B2000_1100', 'final evidence lock and blinded response', 'no new-basin or untouched-geography claim from fixed-map audit'],
        'authorized_now': ['prospective role policy implementation and synthetic tests', 'source/display qualification using saved evidence and metadata', 'catalogue metadata reconciliation', 'bounded development evidence plan', 'development-only detector-informed discovery where useful'],
        'not_automatically_authorized': ['new probability draw or seed', 'research imagery acquisition', 'paid orders or Planet quota', 'semantic A/B execution', 'new evaluation SAR processing', 'final reference release', 'final method freeze', 'full-series production'],
        'amendment_does_not_imply': 'Existing nonsemantic split/component diagnostics are not A/B predictions. Any future detector-informed discovery must record the exact selecting output/version and remain development-only; reference readers do not see the selecting output.'
    }
    save('AUTHORIZATION_AND_MIGRATION.json', approval)

    samples = read(WAVE / 'SAMPLE.json')
    selections = read(WAVE / 'OPTICAL_SELECTION.json')
    records = {r['id']: r for r in samples}
    candidates = {r['record']['id']: {c['id']: c for c in r['candidates']} for r in selections}
    x0, y0, nx, ny = 347801.7721720397, 9625255.8651008, 4559, 2882
    pool, receipts, status_counts = [], [], Counter()
    for p in sorted((WAVE / 'receipts').glob('*.json')):
        d = read(p)
        status_counts[d.get('status', 'MISSING')] += 1
        receipts.append({'name': p.name, 'sha256': digest(p)})
        if d.get('status') != 'PASS':
            continue
        s = records[d['record_id']]
        c = candidates[d['record_id']][d['item_id']]
        row, col = s['row'], s['col']
        assert abs(s['x'] - (x0 + (col + .5) * 10)) < 1e-6
        assert abs(s['y'] - (y0 - (row + .5) * 10)) < 1e-6
        r0, c0 = 3 * (row // 3), 3 * (col // 3)
        r1, c1 = min(r0 + 3, ny), min(c0 + 3, nx)
        tx, ty = x0 + (c0+c1)*5, y0 - (r0+r1)*5
        bounds = [x0+c0*10, y0-r1*10, x0+c1*10, y0-r0*10]
        chip_bounds = [s['x']-245, s['y']-245, s['x']+245, s['y']+245]
        # A footprint claim only. Actual valid/clear pixels remain untested here.
        spatial_footprint_ok = all([bounds[0]-10 >= chip_bounds[0], bounds[1]-10 >= chip_bounds[1], bounds[2]+10 <= chip_bounds[2], bounds[3]+10 <= chip_bounds[3]])
        assert spatial_footprint_ok
        pool.append({
            'evidence_id': p.stem,
            'record_id': s['id'],
            'role': 'DEVELOPMENT_ONLY',
            'selection_history': 'LEGACY_PROBABILITY_QUALIFICATION; no new selection',
            's1_datetime': s['datetime'],
            'optical_item_id': d['item_id'],
            'optical_datetime': d['datetime'],
            'optical_overpass_id': d['overpass'],
            'offset_hours': d['offset_hours'],
            'provider': d['provider'],
            'stored_chip_path': d['path'].replace('\\', '/'),
            'stored_chip_sha256_recorded_not_reread': d['sha256'],
            'old_cell_row_col': [row, col],
            'prospective_disjoint_tile_row_col': [row//3, col//3],
            'prospective_tile_bounds_epsg32750': bounds,
            'prospective_tile_area_m2': (r1-r0)*(c1-c0)*100,
            'old_to_tile_centre_shift_m': [tx-s['x'], ty-s['y']],
            'fifty_m_context_footprint_contained': spatial_footprint_ok,
            'reference_response': 'NOT_IMPORTED',
            'local_clarity': 'NOT_ASSESSED',
            'temporal_transfer': 'NOT_ASSESSED',
            'spatial_registration': 'NOT_ASSESSED',
            'new_tile_response_requires_new_interpretation': True,
            'receipt_sha256': digest(p),
            'native_resolutions_m': {b: v['native_resolution'] for b,v in d['bands'].items()},
            'display_contract': 'SEE_OPTICAL_CONTRACT; metadata consistency is not pixel qualification',
        })
    save('EXISTING_DEVELOPMENT_EVIDENCE_POOL.json', pool)
    shifts = Counter(tuple(round(v, 6) for v in r['old_to_tile_centre_shift_m']) for r in pool)
    summary = {
        'status': 'METADATA_POOL_INDEXED_NOT_PANEL_SELECTED',
        'legacy_records_preserved': len(samples),
        'attempt_receipt_statuses': dict(status_counts),
        'saved_views': len(pool),
        'distinct_optical_items': len({r['optical_item_id'] for r in pool}),
        'distinct_optical_overpasses': len({r['optical_overpass_id'] for r in pool}),
        'distinct_source_supports': len({r['record_id'] for r in pool}),
        'distinct_s1_dates_with_saved_views': len({r['s1_datetime'][:10] for r in pool}),
        'new_tile_grid': 'disjoint30m anchored accepted10m; historical labels not migrated',
        'chip_footprint_covers_30m_and_50m_context': sum(r['fifty_m_context_footprint_contained'] for r in pool),
        'centre_shift_counts_by_view': {str(k):v for k,v in sorted(shifts.items())},
        'max_centre_shift_m': max(math.hypot(*r['old_to_tile_centre_shift_m']) for r in pool),
        'pixels_read': 0,
        'new_imagery_bytes': 0,
        'new_reference_responses': 0,
        'new_panel_selections': 0,
        'interpretation': 'Existing development views provide a reusable footprint pool, not demonstrated clear support or acquisition-time truth. Repeated items/overpasses and date-supports are not independent systems. The old responses remain on old supports.',
        'inputs': [{'path': str(p).replace('\\','/'), 'sha256': digest(p)} for p in [WAVE/'SAMPLE.json', WAVE/'OPTICAL_SELECTION.json']],
        'receipt_manifest_sha256': hashlib.sha256(json.dumps(receipts, sort_keys=True).encode()).hexdigest()
    }
    save('EXISTING_EVIDENCE_POOL_SUMMARY.json', summary)
    save('INPUT_RECEIPT_HASHES.json', receipts)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['inputs','centre_shift_counts_by_view']}, indent=2))


if __name__ == '__main__':
    main()
