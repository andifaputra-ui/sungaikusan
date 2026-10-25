"""Audit/freeze current versions of the same four authorized optical products, no pixels."""
from pathlib import Path
from datetime import datetime,timezone
import json
import hashlib
import ee
import httplib2

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'


def main() -> None:
    """Permit only a version-field difference; retain its unresolved pixel-equivalence caveat."""
    output=ROOT/'REFRESHED_SOURCE_MATCH_FREEZE.json'
    if output.exists():
        raise RuntimeError('Current source metadata already frozen')
    plan_file=ROOT.parent/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.json'
    plan=json.loads(plan_file.read_text())
    old=json.loads((PARENT/'OPTICAL_SOURCE_MATCH_FREEZE.json').read_text())['matches']
    by_id={v['image_id']:v for v in old.values()}
    ee.Initialize(project='gen-lang-client-0932704594',http_transport=httplib2.Http(timeout=45))
    ee.data.setDeadline(45000);ee.data.setMaxRetries(0)
    matches={};changes=[]
    for row in plan['requests']:
        previous=by_id[row['GEE_image_id']]
        current=ee.Image(row['GEE_image_id']).select(row['bands']).getInfo()
        old_comparable={k:v for k,v in previous['metadata'].items() if k!='version'}
        new_comparable={k:v for k,v in current.items() if k!='version'}
        if old_comparable!=new_comparable:
            raise RuntimeError('Change beyond version field; do not proceed')
        matches[row['GEE_image_id']]={**previous,'metadata':current}
        changes.append({'image_id':row['GEE_image_id'],'old_version':previous['metadata'].get('version'),
            'new_version':current.get('version'),'all_other_returned_metadata_identical':True})
    result={'status':'CURRENT_REFERENCE_PRODUCT_METADATA_FROZEN_BEFORE_FIRST_PIXEL_ACCESS',
        'utc':datetime.now(timezone.utc).isoformat(),'matches':matches,'version_audit':changes,
        'source_plan_sha256':hashlib.sha256(plan_file.read_bytes()).hexdigest(),
        'new_pixels_at_freeze':0,'pixel_requests_in_initial_stopped_attempt':0,
        'technical_decision':'Use the current explicitly recorded provider revision of the same already-authorized reference product. No date/centre/product/band/radiometry/role changed; do not assume byte-equivalence to the earlier revision.',
        'unresolved':'Version change is real provider metadata; exact cause and historical pixel equivalence unverified. Archived original references are not rewritten.',
        'documentation':'https://developers.google.com/earth-engine/guides/image_info',
        'documentation_interpretation':'GEE describes version as ingestion timestamp, distinct from observation time; this is not evidence that pixels are unchanged.'}
    output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    (ROOT/'REFRESHED_SOURCE_MATCH_FREEZE.sha256').write_text(hashlib.sha256(output.read_bytes()).hexdigest()+'\n',encoding='utf-8')
    print(json.dumps({'version_audit':changes,'no_pixels':True},indent=2))


if __name__=='__main__':
    main()
