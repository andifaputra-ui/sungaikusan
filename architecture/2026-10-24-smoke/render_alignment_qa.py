"""Two fixed-scale input/score panels; engineering QA, never reference truth."""
from __future__ import annotations
from pathlib import Path
import json
import os
import sys

ROOT=Path(__file__).resolve().parent
PREP=ROOT.parent/'NATIVE_MODEL_READINESS_20261023'


def main() -> None:
    """Check grids/support and render fixed full-patch and central-128 views."""
    os.environ['MPLCONFIGDIR']=str(ROOT/'matplotlib-config')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import rasterio
    sys.path.insert(0,str(PREP))
    from input_contract import validate_output_grid,current_validity
    if not (ROOT/'SMOKE_RESULT.json').exists():
        raise RuntimeError('Numerical inference result is not available')
    frozen=json.loads((PREP/'PROPOSED_SMOKE_INPUT_FREEZE.json').read_text(encoding='utf-8'))['grid']
    loaded={}
    profiles={}
    for name,file in [('input','CURRENT_INPUT.tif'),('score','UNVALIDATED_SCORE.tif'),('support','CURRENT_SUPPORT.tif')]:
        with rasterio.open(ROOT/file) as source:
            validate_output_grid(frozen,dict(crs=source.crs.to_string(),width=source.width,height=source.height,transform=list(source.transform)[:6]))
            loaded[name]=source.read()
            profiles[name]=source.profile
    values=loaded['input'][:3]
    valid=current_validity(values,(loaded['input'][3:]>0)&(values!=-9999))
    assert np.array_equal(valid,loaded['support'][0].astype(bool))
    assert np.all(loaded['score'][0][~valid]==-9999)
    transform=profiles['input']['transform']
    anchors=[]
    for row,col in [(16,16),(256,256),(495,495)]:
        xy=transform*(col+.5,row+.5)
        output_xy=profiles['score']['transform']*(col+.5,row+.5)
        assert xy==output_xy
        anchors.append({'row':row,'col':col,'world_xy':list(xy),'input_vv_db':float(values[0,row,col]),
                        'output_score':float(loaded['score'][0,row,col]),'exact_grid_coordinate_match':True})
    displays=[('VV sigma0 (dB)',values[0],-30,0,'gray'),
              ('VH sigma0 (dB)',values[1],-35,-5,'gray'),
              ('Unvalidated model score',loaded['score'][0],0,1,'viridis')]
    fig,axes=plt.subplots(2,3,figsize=(13,9.4),layout='constrained')
    clipping=[]
    for row,(start,size,label) in enumerate([(0,512,'Full 5.12 km patch'),(192,128,'Fixed central 1.28 km crop')]):
        end=start+size
        x0,y1=transform*(start,start)
        x1,y0=transform*(end,end)
        for col,(title,array,low,high,palette) in enumerate(displays):
            data=np.ma.masked_where(~valid[start:end,start:end],array[start:end,start:end])
            cmap=plt.get_cmap(palette).copy()
            cmap.set_bad('#bdbdbd')
            image=axes[row,col].imshow(data,extent=[x0,x1,y0,y1],origin='upper',interpolation='nearest',
                                       cmap=cmap,vmin=low,vmax=high)
            axes[row,col].set_title(label+'\n'+title,fontsize=10)
            axes[row,col].set_xlabel('Easting (m), EPSG:32750',fontsize=8)
            axes[row,col].set_ylabel('Northing (m)',fontsize=8)
            axes[row,col].tick_params(labelsize=7)
            axes[row,col].ticklabel_format(style='plain',useOffset=False)
            axes[row,col].set_aspect('equal')
            for r,c in [(size//4,size//4),(size//2,size//2),(3*size//4,3*size//4)]:
                x,y=transform*(start+c+.5,start+r+.5)
                axes[row,col].plot(x,y,'+',color='#d95f02',ms=7,mew=.8)
            fig.colorbar(image,ax=axes[row,col],shrink=.75,pad=.015)
            observed=data.compressed()
            clipping.append({'view':label,'display':title,'display_limits':[low,high],
                             'below_display_range':int((observed<low).sum()),'above_display_range':int((observed>high).sum())})
    fig.suptitle('1 September 2024 | Native S1-only technical smoke | DEVELOPMENT ONLY',fontsize=13)
    fig.supxlabel('Identical requested grid and nearest-neighbour display. Crosses are shared grid anchors, not control truth.\n'
                  'Gray = unsupported. Fixed dB stretches are display choices, not class rules. No optical/reference overlay.',fontsize=9)
    fig.savefig(ROOT/'ALIGNMENT_QA_TWO_SCALES.png',dpi=160)
    plt.close(fig)
    result={'status':'PROGRAMMATIC_GRID_AND_SUPPORT_CHECKS_PASS_VISUAL_REVIEW_PENDING',
        'anchors':anchors,'display_clipping':clipping,'views':'Frozen full512 and central128; no outcome-based zoom selection',
        'limitations':'Copied grid agreement and source/score panels cannot independently establish absolute geolocation or water accuracy.'}
    (ROOT/'ALIGNMENT_QA_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('TWO_SCALE_QA_RENDERED')


if __name__=='__main__':
    main()
