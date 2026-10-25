"""Public OPERA product/burst catalogue metadata only; do not follow asset links."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlencode
from urllib.request import Request,urlopen
import json
import hashlib

ROOT=Path(__file__).resolve().parent
ENDPOINT='https://cmr.earthdata.nasa.gov/search/granules.umm_json'


def fetch(name: str,short_name: str,limit: int) -> None:
    """Save one bounded text response and flag completeness instead of silent pagination."""
    destination=ROOT/(name+'.json')
    if destination.exists():
        raise RuntimeError('Metadata response already saved')
    query={'short_name':short_name,'temporal':'2025-05-07T00:00:00Z,2025-05-21T00:00:00Z',
        'bounding_box':'115.63,-3.65,116.04,-3.39','page_size':limit}
    url=ENDPOINT+'?'+urlencode(query)
    with urlopen(Request(url,headers={'User-Agent':'Kusan-frozen-reference-date-metadata/1'}),timeout=90) as response:
        body=response.read(8*1024**2+1)
        if len(body)>8*1024**2:
            raise RuntimeError('Public metadata response exceeds8MiB bound')
        hits=response.headers.get('CMR-Hits')
    data=json.loads(body);destination.write_bytes(body)
    receipt={'retrieved_utc':datetime.now(timezone.utc).isoformat(),'query':query,'url':url,
        'response_body_bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
        'CMR_hits':int(hits) if hits is not None else None,'returned':len(data.get('items',[])),
        'complete_within_declared_bound':hits is not None and int(hits)<=limit,
        'pixel_or_asset_access':False}
    (ROOT/(name+'_RECEIPT.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(name,receipt['returned'],'HITS',receipt['CMR_hits'],'NO_ASSETS',flush=True)


def main() -> None:
    """Query product and RTC provenance serially; no imagery or orders."""
    fetch('DSWX_METADATA','OPERA_L3_DSWX-S1_V1',50)
    fetch('RTC_METADATA','OPERA_L2_RTC-S1_V1',100)


if __name__=='__main__':
    main()
