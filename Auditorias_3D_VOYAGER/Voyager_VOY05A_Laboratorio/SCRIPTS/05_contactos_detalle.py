from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
R=Path(__file__).resolve().parents[1];font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',23)
for n in [1,3,4,5,6,7,8,9,10,11,14,16,17,19,25,26,27,28,29,35,50,51,52,53,54,55,57,64,65,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,91,93,94,95,96,97,103]:
 out=Image.new('RGB',(1600,1400),'#101922');dr=ImageDraw.Draw(out)
 for i,s in enumerate(['XM','XP','YM','YP']):
  p=R/'CAPTURAS'/f'DET_Mesh{n}_{s}.png'
  if not p.exists():continue
  im=Image.open(p).convert('RGB');im.thumbnail((800,665));x=i%2*800;y=i//2*700;out.paste(im,(x,y+35));dr.text((x+15,y+5),f'Mesh{n} / {s}',font=font,fill='white')
 out.save(R/'CAPTURAS'/f'LAM_DET_Mesh{n}.jpg',quality=92)
