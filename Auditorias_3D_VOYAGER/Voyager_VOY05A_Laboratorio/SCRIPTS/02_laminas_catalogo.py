from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1]
mode=sys.argv[1] if len(sys.argv)>1 else 'ISO'
files=sorted((R/'CAPTURAS').glob(f'CAT_*_{mode}.png'),key=lambda p:int(p.stem.split('_')[1][4:]))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
for i in range(0,len(files),12):
 out=Image.new('RGB',(1800,1800),'#101922');draw=ImageDraw.Draw(out)
 for j,p in enumerate(files[i:i+12]):
  x=j%3*600;y=j//3*450;im=Image.open(p).convert('RGB');im.thumbnail((590,400));out.paste(im,(x,y+35));draw.text((x+12,y+5),p.stem.replace('CAT_','').replace('_ISO',''),font=font,fill='white')
 out.save(R/'CAPTURAS'/f'LAM_{mode}_{i//12+1:02}.jpg',quality=92)
print(len(files),'modelos en laminas')
