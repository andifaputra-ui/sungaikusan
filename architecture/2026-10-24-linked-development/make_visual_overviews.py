"""Arrange all remaining fixed review views for complete visual screening."""
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent


def main() -> None:
    """Use only already-rendered optical images; no source/raster pixel access."""
    target=ROOT/'VISUAL_SCREEN_OVERVIEWS';target.mkdir(exist_ok=True)
    remaining=[3,5,6,8,10,11,14,15,16,17,19,20,24]
    for start in range(0,len(remaining),4):
        selected=remaining[start:start+4]
        canvas=Image.new('RGB',(460*len(selected),1600),'white')
        draw=ImageDraw.Draw(canvas)
        for col,index in enumerate(selected):
            with Image.open(ROOT/'BLINDED_OPTICAL_PACKET/images'/f'R{index:02d}_optical.png') as image:
                # The first column preserves the original four 490m RGB panels and labels.
                crop=image.crop((0,75,625,2100));crop.thumbnail((460,1550))
                canvas.paste(crop,(460*col,35))
                draw.text((460*col+10,10),f'R{index:02d} - visual screen; zoom views retained',fill='black')
        canvas.save(target/f'overview_{start//4+1}.png')


if __name__=='__main__':
    main()
