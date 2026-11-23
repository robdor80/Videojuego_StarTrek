import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];data=json.loads((R/'DATOS/planos_soporte_plot.json').read_text());im=Image.new('RGB',(1600,1600),'#f4f6fa');d=ImageDraw.Draw(im);font=lambda s:ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',s)
def pt(p):return (800+p[0]*100,900-p[1]*100)
colors={.023:'#e6c66c',.129:'#f29a6c',.175:'#df704d',.187:'#d65d49',.281:'#f3a055',.327:'#b4c1db',.433:'#9b7bc7',.479:'#76b8cf',.585:'#59aa74',.737:'#d4a0b7',.784:'#8fb394'}
for x in sorted(data,key=lambda x:x['z']):
 z=round(x['z'],3);d.polygon([pt(p) for p in x['points']],fill=colors.get(z,'#b8bdc9'))
d.text((30,25),'VOY-03 · superficies horizontales reales (no mapa de navegación)',font=font(30),fill='#15263b')
for k,(z,c) in enumerate(colors.items()):d.rectangle((20,100+k*40,45,125+k*40),fill=c);d.text((55,95+k*40),f'Z = {z:.3f} m',font=font(22),fill='#15263b')
for name,p in [('Centro',[0,-.77]),('Navegacion / punto previo',[0,-4.84]),('Pasarela',[3.96,2.97])]:
 x,y=pt(p);d.ellipse((x-6,y-6,x+6,y+6),fill='#b51e40');d.text((x+10,y),name,font=font(20),fill='#15263b')
for k in range(-6,7):
 x,y=pt([k,0]);d.text((x,1530),str(k),font=font(18),fill='#35475d')
im.save(R/'LAMINAS/01_superficies_originales.png')
