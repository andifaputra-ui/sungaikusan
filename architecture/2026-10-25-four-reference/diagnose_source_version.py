"""Metadata-only diagnosis of the first guarded source-version stop; no pixel requests."""
from pathlib import Path
from datetime import datetime,timezone
import json
import ee
import httplib2

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'


def main() -> None:
    """Retain the live source record and distinguish metadata from real source change."""
    plan=json.loads((ROOT.parent/'PROPOSED_FOUR_CHIP_SOURCE_PLAN.json').read_text())
    row=plan['requests'][0]
    matches=json.loads((PARENT/'OPTICAL_SOURCE_MATCH_FREEZE.json').read_text())['matches']
    old=next(v for v in matches.values() if v['image_id']==row['GEE_image_id'])['metadata']
    ee.Initialize(project='gen-lang-client-0932704594',http_transport=httplib2.Http(timeout=45))
    ee.data.setDeadline(45000);ee.data.setMaxRetries(0)
    new=ee.Image(row['GEE_image_id']).select(row['bands']).getInfo()
    (ROOT/'SOURCE_VERSION_LIVE_METADATA.json').write_text(json.dumps(new,indent=2)+'\n',encoding='utf-8')
    changed={k:{'old':old['properties'].get(k),'new':new['properties'].get(k)}
        for k in set(old['properties'])|set(new['properties']) if old['properties'].get(k)!=new['properties'].get(k)}
    result={'utc':datetime.now(timezone.utc).isoformat(),'no_pixel_request':True,
        'old_version':old.get('version'),'old_version_type':type(old.get('version')).__name__,
        'new_version':new.get('version'),'new_version_type':type(new.get('version')).__name__,
        'old_id':old.get('id'),'new_id':new.get('id'),'bands_equal':old['bands']==new['bands'],
        'changed_properties':changed,'old_top_level_keys':list(old),'new_top_level_keys':list(new)}
    (ROOT/'SOURCE_VERSION_DIAGNOSIS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
