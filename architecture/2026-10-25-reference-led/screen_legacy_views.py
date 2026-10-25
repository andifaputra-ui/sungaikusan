"""Render a complete metadata-defined saved2025 development discovery screen."""
from __future__ import annotations
from pathlib import Path
from urllib.parse import urlparse
import os
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parent
C2=ROOT.parent
OLD=C2/'DEVELOPMENT_IMPLEMENTATION_20261009'
ENV=Path('E:/Bendungan_Kusan/Miniforge/envs/kusan-c1')
_dll=os.add_dll_directory(str(ENV/'Library/bin')) if os.name=='nt' else None
os.environ['PATH']=str(ENV/'Library/bin')+os.pathsep+os.environ.get('PATH','')
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from shapely.geometry import box
sys.path.insert(0,str(OLD/'ROLE_GUARD'))
sys.path.insert(0,str(OLD/'OPTICAL_CONTRACT'))
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window
from optical_display_contract import legacy_display,render


def read(path: Path) -> dict | list:
    """Read immutable metadata only."""
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main() -> None:
    """Check fixed cached scopes/digests before full local pixel reads; no old responses."""
    pool=[r for r in read(OLD/'EXISTING_DEVELOPMENT_EVIDENCE_POOL.json') if r['s1_datetime'].startswith('2025')]
    pool=sorted(pool,key=lambda r:r['evidence_id'])
    if len(pool)!=62:
        raise RuntimeError('Metadata-defined screen changed')
    screen_file=ROOT/'LEGACY_SCREEN_FREEZE.json'
    if screen_file.exists():
        raise RuntimeError('Do not replace the saved screening manifest')
    screen={'status':'FROZEN_BEFORE_NEW_SAVED_PIXEL_READS','items':pool,'new_reference_responses':0,
        'ranking':'All2025operational overlap views, stable evidenceID order; no clarity/class/prediction filter',
        'pool_sha256':hashlib.sha256((OLD/'EXISTING_DEVELOPMENT_EVIDENCE_POOL.json').read_bytes()).hexdigest()}
    screen_file.write_text(json.dumps(screen,indent=2)+'\n',encoding='utf-8')
    scopes={r['id']:r for r in read(OLD/'SAVED_CHIP_SCOPE_MANIFEST.json')}
    items={r['id']:r for r in read(OLD/'OPTICAL_CONTRACT/SAVED_METADATA_AUDIT.json')['items']}
    samples={r['id']:r for r in read(C2/'REFERENCE_QUALIFICATION_WAVE2/SAMPLE.json')}
    image_dir=ROOT/'legacy_discovery_views';image_dir.mkdir(exist_ok=True)
    receipts=[];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
    for index,row in enumerate(pool,1):
        alias=f'L{index:02d}';declared=scopes[row['evidence_id']];sample=samples[row['record_id']]
        affine=(10,0,sample['x']-245,0,-10,sample['y']+245)
        native=(affine[2],affine[0],affine[1],affine[5],affine[3],affine[4])
        e=Evidence(row['evidence_id'],Role.DEV_REFERENCE,Role.DEV_REFERENCE,
            independent_measurement=True,acquisition_utc=row['optical_datetime'])
        scope=PixelScope('SAVED_PASS_ONLY_2025',Role.DEV_REFERENCE,e.artifact_id,'EPSG:32750',
            box(*declared['bounds']),operation_authorization_record='SCOPE.json + prior SAVED_CHIP_SCOPE_MANIFEST.json')
        check=check_native_window(e,Actor.DEVELOPER,scope,NativeWindow(0,0,49,49),native,
            source_crs='EPSG:32750',source_width=49,source_height=49)
        receipt={'alias':alias,'evidence_id':row['evidence_id'],'pre_read_native_check':check}
        (ROOT/'LOCAL_PREREAD_LAST.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
        path=Path(row['stored_chip_path']).resolve()
        if path.parent!=(C2/'REFERENCE_QUALIFICATION_WAVE2/chips').resolve():
            raise RuntimeError('Unexpected saved source path')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=declared['source_sha256']:
            raise RuntimeError('Saved body differs; no repair')
        with np.load(path,allow_pickle=False) as source:
            data=source['data'].copy();saved=source['transform'].tolist()
        if data.shape!=(5,49,49) or not np.allclose(saved[:6],affine,rtol=0,atol=1e-7):
            raise RuntimeError('Saved source grid differs')
        original=read(C2/'REFERENCE_QUALIFICATION_WAVE2/receipts'/f'{row["evidence_id"]}.json')
        item=items[row['optical_item_id']]
        frame=legacy_display(data[:4],source_collection='sentinel-2-l2a',
            source_host=urlparse(original['bands']['red']['href']).hostname,
            bands=[original['bands'][b]['raster_band_metadata'][0] for b in ['red','green','blue','nir']],
            baseline=item['baseline'],boa_offset_applied=item['boa_offset_applied'])
        rgb,rgb_info=render(frame,'RGB');nir,nir_info=render(frame,'NIR')
        assert not frame.quantitative_allowed
        picture=Image.new('RGB',(620,385),'white');draw=ImageDraw.Draw(picture)
        draw.text((5,3),f'{alias} OPTICAL DISCOVERY ONLY - LEGACY DISPLAY PROXY',font=font,fill='black')
        draw.text((5,25),f'opt {row["optical_datetime"][:19]} | target {row["s1_datetime"][:10]}',font=font,fill='black')
        draw.text((5,47),'490m square, north up; RGB / NIR-red-green; no labels',font=font,fill='black')
        picture.paste(Image.fromarray(rgb).resize((294,294),Image.Resampling.NEAREST),(5,77))
        picture.paste(Image.fromarray(nir).resize((294,294),Image.Resampling.NEAREST),(315,77))
        picture.save(image_dir/(alias+'.png'))
        receipt.update(source_sha256=declared['source_sha256'],source_state=frame.source_state,
            quantitative_allowed=False,rgb=rgb_info,nir=nir_info,
            original_source_key=row['optical_item_id'],optical_utc=row['optical_datetime'],
            target_utc=row['s1_datetime'],saved_scope=declared['bounds'])
        receipts.append(receipt)
    for start in range(0,62,12):
        chosen=receipts[start:start+12]
        board=Image.new('RGB',(1860,1540),'white')
        for i,receipt in enumerate(chosen):
            with Image.open(image_dir/(receipt['alias']+'.png')) as image:
                board.paste(image,((i%3)*620,(i//3)*385))
        board.save(ROOT/f'LEGACY_BOARD_{start//12+1:02d}.png')
    (ROOT/'LEGACY_SCREEN_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n',encoding='utf-8')
    total=sum(p.stat().st_size for directory in [ROOT,C2/'LINKED_DEVELOPMENT_COMPARISON_20261024'] for p in directory.rglob('*') if p.is_file())
    if total>=1024**3:
        raise RuntimeError('Parent/new branch aggregate storage exceeds retained ceiling')
    (ROOT/'STATUS.json').write_text(json.dumps({'phase':'LEGACY_SAVED_DISCOVERY_SCREEN_READY',
        'views':62,'new_reference_classes':0,'new_imagery_bytes':0,'combined_artifact_bytes':total,
        'no_background_job':True,'comparison_gate':'CLOSED'},indent=2)+'\n',encoding='utf-8')
    print('PREPARED62_SAVED_PROXY_VIEWS; NEW_REFERENCE_CLASSES0',flush=True)


if __name__=='__main__':
    main()
