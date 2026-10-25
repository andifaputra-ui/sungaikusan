"""Inspect current calibrated saved optical controls at frozen new centres only."""
from __future__ import annotations
from pathlib import Path
import os
import sys
import json
import hashlib

ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent/'LINKED_DEVELOPMENT_COMPARISON_20261024'
ENV=Path('E:/Bendungan_Kusan/Miniforge/envs/kusan-c1')
_dll=os.add_dll_directory(str(ENV/'Library/bin')) if os.name=='nt' else None
os.environ['PATH']=str(ENV/'Library/bin')+os.pathsep+os.environ.get('PATH','')
os.environ['GDAL_DATA']=str(ENV/'Library/share/gdal')
os.environ['PROJ_DATA']=str(ENV/'Library/share/proj')
os.environ['MPLCONFIGDIR']=str(ROOT/'matplotlib-config')
import numpy as np
import rasterio
from affine import Affine
from shapely.geometry import box
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0,str(PARENT))
sys.path.insert(0,str(ROOT.parent/'DEVELOPMENT_IMPLEMENTATION_20261009/ROLE_GUARD'))
from optical_qa import reflectance,diagnostic_qa
from role_guard import Evidence,Role,Actor,PixelScope,NativeWindow,check_native_window


def read(path: Path) -> dict | list:
    """Read recorded provenance without previous responses or predictions."""
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main() -> None:
    """Re-read only frozen chip scopes and provide local QA for two controls."""
    freeze=ROOT/'NOMINATION_FREEZE.json'
    if hashlib.sha256(freeze.read_bytes()).hexdigest()!=(ROOT/'NOMINATION_FREEZE.sha256').read_text().strip():
        raise RuntimeError('Nomination register changed')
    nominations=read(freeze)['records'];plans={r['id']:r for r in read(PARENT/'REFERENCE_SOURCE_PLAN_V2.json')['requests']}
    outputs=[]
    for nomination in nominations[:2]:
        offered=[r for r in nomination['saved_current_views_covering_full90m_neighbourhood']
            if plans[r['id']]['case_id'].endswith('2025-05-11')]
        fig,axes=plt.subplots(len(offered),3,figsize=(12,4*len(offered)),layout='constrained',squeeze=False)
        fig.suptitle(f'{nomination["id"]} frozen new development control | target2025-05-11 | optical only\n'
            'FixedSR0-0.30, gamma1; 30m white,50m cyan,90m gray; north up, EPSG32750',fontsize=10)
        for index,item in enumerate(offered):
            row=plans[item['id']];receipt=read(PARENT/'reference_receipts'/(item['id']+'.json'))
            transform=Affine(*row['chip_grid']['transform']);x0,y0=transform*(0,0);x1,y1=transform*(49,49)
            e=Evidence(item['id'],Role.DEV_REFERENCE,Role.DEV_REFERENCE,independent_measurement=True,
                acquisition_utc=row['optical_datetime'])
            scope=PixelScope('FROZEN_SAVED_CHIP',Role.DEV_REFERENCE,e.artifact_id,'EPSG:32750',
                box(x0,y1,x1,y0),operation_authorization_record='SCOPE.json + NOMINATION_FREEZE.json + parent source plan')
            permit=check_native_window(e,Actor.DEVELOPER,scope,NativeWindow(0,0,49,49),transform.to_gdal(),
                source_crs='EPSG:32750',source_width=49,source_height=49)
            (ROOT/'CONTROL_PREREAD_LAST.json').write_text(json.dumps({'id':item['id'],'permit':permit,
                'before_file_body_or_pixels':True},indent=2)+'\n',encoding='utf-8')
            path=Path(receipt['path'])
            if hashlib.sha256(path.read_bytes()).hexdigest()!=receipt['payload']['sha256']:
                raise RuntimeError('Saved body differs')
            with rasterio.open(path) as ds:
                if ds.width!=49 or ds.height!=49 or not ds.transform.almost_equals(transform):
                    raise RuntimeError('Saved grid differs')
                data=ds.read()
            n=len(receipt['bands']);raw=data[:n];masks=data[n:]
            physical=reflectance(raw[:4],row['provider']);available,flagged=diagnostic_qa(raw,row['provider'],masks)
            x,y=nomination['centre_epsg32750'];colf,rowf=~transform*(x,y)
            col=int(round(colf-0.5));line=int(round(rowf-0.5))
            if abs(col+0.5-colf)>1e-6 or abs(line+0.5-rowf)>1e-6:
                raise RuntimeError('New centre not aligned to saved indexing grid')
            diagnostic={}
            for size in [10,30,50]:
                radius=size//20;scenarios=[]
                for dy in [-20,-10,0,10,20]:
                    for dx in [-20,-10,0,10,20]:
                        rr=line-dy//10;cc=col+dx//10
                        part=(slice(rr-radius,rr+radius+1),slice(cc-radius,cc+radius+1))
                        scenarios.append({'dx_m':dx,'dy_m':dy,'available':float(available[part].mean()),
                            'flagged':float(flagged[part].mean())})
                diagnostic[str(size)]=scenarios
            valid=np.all(masks[:4]==1,axis=0)
            extent=[x0-x,x1-x,y1-y,y0-y]
            for j,(channel,zoom,title) in enumerate([([0,1,2],False,'RGB490m'),([0,1,2],True,'RGB110m'),([3,0,1],True,'NIR-red-green110m')]):
                rgb=np.moveaxis(np.clip(physical[channel]/0.30,0,1),0,-1);rgb[~valid]=0.55
                ax=axes[index,j];ax.imshow(rgb,extent=extent,origin='upper',interpolation='nearest')
                for size,color in [(30,'white'),(50,'cyan'),(90,'#bbbbbb')]:
                    ax.add_patch(Rectangle((-size/2,-size/2),size,size,fill=False,edgecolor=color,lw=0.9))
                if zoom:
                    ax.set_xlim(-55,55);ax.set_ylim(-55,55)
                ax.set_title(row['provider']+' '+row['optical_datetime'][:19]+'\n'+title,fontsize=9)
                ax.set_xlabel('east offset(m)',fontsize=8);ax.set_ylabel('north offset(m)',fontsize=8)
            outputs.append({'nomination':nomination['id'],'source_request':item['id'],
                'optical_utc':row['optical_datetime'],'provider':row['provider'],'permit':permit,
                'centre_native_col_row':[col,line],'quality_diagnostic':diagnostic,
                'quantitative_source_radiometry':'PARENT_VERIFIED_COLLECTION_SCALING',
                'reference_class':'NOT_AUTOMATED','temporal_transfer':'NOT_AUTOMATED'})
        fig.savefig(ROOT/(nomination['id']+'_saved_control.png'),dpi=140);plt.close(fig)
    (ROOT/'SAVED_CONTROL_AUDIT.json').write_text(json.dumps(outputs,indent=2)+'\n',encoding='utf-8')
    print('PREPARED_SAVED_CONTROLS',len(outputs),flush=True)


if __name__=='__main__':
    main()
