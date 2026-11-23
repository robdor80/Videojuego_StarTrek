import json,html
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];rows=json.loads((R/'DATOS/inventario_puertas_accesos.json').read_text());by={x['id']:x for x in rows};font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24);small=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
def label(row):
 e=row.get('front_surface_envelope');w=e['width'] if e else row['width'];h=e['height'] if e else row['height'];return f'{row["id"]} | {w:.3f} x {h:.3f} m | '+('frente, no vano' if e else 'perfil/envolvente') if w and h else row['id']
for row in rows:
 p=R/row['capture'];im=Image.open(p).convert('RGB');dr=ImageDraw.Draw(im);dr.rectangle((0,0,im.width,66),fill='#101922');dr.text((16,8),label(row),font=font,fill='white');dr.text((16,38),f'Grado {row["grade"]} | modelo original cerrado | amarillo = borde real, cuando existe',font=small,fill='#bfd3e4');im.save(p)
boards={
 '01_PUENTE':[(x,'capture') for x in ['BR_01','BR_02','BR_03','BR_04']]+[('BR_01','context_capture'),('BR_03','context_capture')],
 '02_PUERTAS_MODULARES':[(x,'capture') for x in ['PT_Mesh14_01','PT_Mesh25_01','PT_Mesh28_01','PT_Mesh51_01','PT_Mesh27_01','PT_Mesh93_01']],
 '03_PASILLOS_Y_DESVIOS':[(x,'context_capture') for x in ['AC_Mesh12_00','AC_Mesh41_00','AC_Mesh40_00','AC_Mesh38_00','AC_Mesh2_00','AC_Mesh52_00']],
 '04_SALAS_Y_TECNICOS':[(x,'context_capture') for x in ['AC_Mesh4_00','AC_Mesh9_03','AC_Mesh81_00','AC_Mesh17_00','AC_Mesh19_02','AC_Mesh16_01']],
 '05_MARCOS_Y_PLACAS':[(x,'context_capture') for x in ['PT_Mesh27_01','PT_Mesh53_01','PT_Mesh55_01','PT_Mesh93_01','PT_Mesh54_01','PT_Mesh57_01']]}
for name,items in boards.items():
 out=Image.new('RGB',(1800,1740),'#101922');dr=ImageDraw.Draw(out)
 for i,(id,field) in enumerate(items):
  row=by[id];im=Image.open(R/row[field]).convert('RGB');im.thumbnail((880,500));x=i%2*900;y=i//2*580;out.paste(im,(x+(900-im.width)//2,y+65));dr.text((x+12,y+8),label(row),font=small,fill='white');dr.text((x+12,y+36),row['architectural_family']+' / '+row['grade'],font=small,fill='#a5c9dd')
 out.save(R/'CAPTURAS'/f'LAM_FINAL_{name}.jpg',quality=94)
parts=['<!doctype html><meta charset="utf-8"><title>VOY-05A — Galería</title><style>body{font:16px system-ui;background:#101922;color:#eee;margin:24px}article{display:inline-block;width:47%;vertical-align:top;margin:1%}img{width:100%}a{color:#8dd9ff}</style><h1>VOY-05A · Evidencias de modelos reales</h1><p>Puertas cerradas. Amarillo: segmentos de borde original. Las vistas CUT son cortes desechables; no arquitectura modificada. Dimensiones de frente no equivalen a vano libre.</p>']
for name in boards:parts.append(f'<h2>{name}</h2><img src="CAPTURAS/LAM_FINAL_{name}.jpg">')
for row in rows:parts.append(f'<article><h3>{row["id"]}</h3><p>{html.escape(label(row))} · grado {row["grade"]}</p><a href="{row["context_capture"]}">Contexto completo</a><img loading="lazy" src="{row["capture"]}"></article>')
(R/'GALERIA.html').write_text('\n'.join(parts),encoding='utf8');print('Laminas finales y galeria',len(rows))
