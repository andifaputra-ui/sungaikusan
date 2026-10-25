"""One independent raw-SAR catalogue metadata cross-check, no downloads or login."""
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlencode
from urllib.request import Request,urlopen
import json
import hashlib

ROOT=Path(__file__).resolve().parent


def main() -> None:
    """Keep processing-level variants separate from physical acquisitions."""
    destination=ROOT/'ASF_METADATA.json'
    if destination.exists():
        raise RuntimeError('ASF metadata already recorded; no automatic repeat')
    query={'dataset':'SENTINEL-1','start':'2025-05-07T00:00:00Z','end':'2025-05-21T00:00:00Z',
        'intersectsWith':'POLYGON((115.63 -3.65,116.04 -3.65,116.04 -3.39,115.63 -3.39,115.63 -3.65))',
        'beamMode':'IW','processingLevel':'GRD_HD,GRD_HS','maxResults':40,'output':'geojson'}
    url='https://api.daac.asf.alaska.edu/services/search/param?'+urlencode(query)
    with urlopen(Request(url,headers={'User-Agent':'Kusan-reference-date-metadata/1'}),timeout=90) as response:
        body=response.read(8*1024**2+1)
        if len(body)>8*1024**2:
            raise RuntimeError('ASFmetadata body exceeds bound')
    data=json.loads(body);destination.write_bytes(body)
    features=data.get('features',[])
    receipt={'retrieved_utc':datetime.now(timezone.utc).isoformat(),'query':query,'url':url,
        'returned_features':len(features),'response_body_bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
        'limit_reached':len(features)>=40,'no_asset_or_pixel_access':True,
        'completeness_caveat':'Result below explicit bound; archive coverage is not proof of all possible mission acquisitions'}
    (ROOT/'ASF_METADATA_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print('ASF_METADATA_COMPLETE',len(features),'NO_ASSETS',flush=True)
    for row in features:
        properties=row['properties']
        print(properties.get('fileID'),properties.get('startTime'),properties.get('platform'),properties.get('flightDirection'),flush=True)


if __name__=='__main__':
    main()
