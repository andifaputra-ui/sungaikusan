"""Enlarge already rendered diagnostic views and add native index guides."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parent


def main() -> None:
    """No source pixel read, rescaling change or inferred class is performed."""
    for alias in ['L29','L30','L35','L36','L43','L44']:
        with Image.open(ROOT/'legacy_discovery_views'/(alias+'.png')) as source:
            canvas=Image.new('RGB',(1280,700),'white');draw=ImageDraw.Draw(canvas)
            font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
            for i,bounds in enumerate([(5,77,299,371),(315,77,609,371)]):
                panel=source.crop(bounds).resize((588,588),Image.Resampling.NEAREST)
                x=35+i*640;y=60;canvas.paste(panel,(x,y))
                draw.text((x,5),alias+' | '+('RGB' if i==0 else 'NIR-red-green')+' | DISPLAY_PROXY',font=font,fill='black')
                for k in range(0,50,5):
                    offset=k*12
                    draw.line((x+offset,y,x+offset,y+588),fill='#888888',width=1)
                    draw.line((x,y+offset,x+588,y+offset),fill='#888888',width=1)
                    draw.text((x+offset,y-23),str(k),font=font,fill='black')
                    draw.text((x-25,y+offset),str(k),font=font,fill='black')
            canvas.save(ROOT/(alias+'_index_guide.png'))


if __name__=='__main__':
    main()
