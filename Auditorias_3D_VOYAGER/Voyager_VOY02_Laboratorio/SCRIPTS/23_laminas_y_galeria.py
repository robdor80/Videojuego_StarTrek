"""Technical plates from recorded measurements; no invented geometry or image restoration."""
import json,math,textwrap,html
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];O=R/'LAMINAS';O.mkdir(exist_ok=True)
def read(n):return json.loads((R/'DATOS'/n).read_text(encoding='utf8'))
def font(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if bold else 'segoeui.ttf'),size)
def base(title,subtitle,width=1600,height=1100):
 im=Image.new('RGB',(width,height),'#f5f7fb');d=ImageDraw.Draw(im);d.rectangle((0,0,width,130),fill='#15263b');d.text((55,25),title,font=font(36,True),fill='white');d.text((55,80),subtitle,font=font(21),fill='#c5d6e8');return im,d
def footer(d,text,y=1035):
 for k,line in enumerate(textwrap.wrap(text,125)):d.text((55,y+25*k),line,font=font(19),fill='#33465c')
# Refined occupancy grid in physical metres; original XYZ frame of bridge at scale 1.10.
im,d=base('VOY-02 · Acceso desde el centro','Rejilla geométrica 0,10 m · H=1,90 m · radio 0,35 m · escala del puente 1,10')
test=read('acceso_central_revision.json')['tests'][1];box=(90,170,1010,990);xmin,xmax=-7.2,7.2;ymin,ymax=-6.4,7.2
factor=min((box[2]-box[0])/(xmax-xmin),(box[3]-box[1])/(ymax-ymin))
def pt(p):return box[0]+(p[0]-xmin)*factor,box[3]-(p[1]-ymin)*factor
colors={1:'#2786b9',8:'#dd9d30',10:'#8456b5'}
for p in test['blocked_nodes']:
 x,y=pt(p['foot']);d.rectangle((x-1,y-1,x+1,y+1),fill='#d7dee7')
for p in test['nodes']:
 x,y=pt(p['foot']);d.ellipse((x-1.8,y-1.8,x+1.8,y+1.8),fill=colors.get(p['component'],'#aab4c1'))
for x in range(-6,8,2):
 px,_=pt([x,0]);d.text((px-8,995),str(x),font=font(18),fill='#32465d')
for y in range(-6,8,2):
 _,py=pt([0,y]);d.text((45,py-10),str(y),font=font(18),fill='#32465d')
for i,r in enumerate(test['routes']):
 for label,p,color in [('INICIO',r['start_m'],'#16834a'),('SALIDA',r['goal_m'],'#b2253c')]:
  x,y=pt(p);d.ellipse((x-6,y-6,x+6,y+6),fill=color)
 if r.get('gap_endpoints'):
  a,b=map(pt,r['gap_endpoints']);d.line((a,b),fill='#c02c3a',width=4)
d.text((1080,190),'Resultados',font=font(28,True),fill='#15263b')
for i,line in enumerate(['Centro → posterior: sin ruta','Navegación → posterior: sin ruta','Pasarela: existe ruta previa válida','','5770 nodos H=1,60 m','5767 nodos H=1,90 m','','Colores: componentes de rejilla','Gris claro: poses bloqueadas','','No es NavMesh ni locomoción.','La ruta nueva de rejilla por la','pasarela roza un soporte al','refinar margen: no sustituye','la ruta previa ensayada.']):d.text((1080,245+i*36),line,font=font(20),fill='#33465c')
footer(d,'DATOS/acceso_central_revision.json. Un fallo de rejilla limita esta búsqueda: no prueba imposibilidad absoluta. Coordenadas del puente en metros.');im.save(O/'L01_acceso_central.png')
# Door contact curves.
im,d=base('VOY-02 · Carreras de las puertas','21 fracciones estáticas por puerta · contactos nuevos frente a cerrada · superficies completas')
door=read('carreras_investigacion.json')['doors']
for k,g in enumerate(door):
 x0=80+k*510;y0=250;w=440;h=590;maximum=max(p['new_pairs'] for p in g['poses']);maximum=max(10,math.ceil(maximum/50)*50)
 d.text((x0,y0-65),g['id']+' · adaptación C',font=font(25,True),fill='#15263b');d.line((x0,y0,x0,y0+h,x0+w,y0+h),fill='#6f8195',width=2)
 for j in range(5):
  val=maximum*j/4;y=y0+h-h*j/4;d.line((x0,y,x0+w,y),fill='#d6dde7');d.text((x0-35,y-10),str(round(val)),font=font(17),fill='#52657a')
 for key,color in [('new_pairs','#d08b1b'),('transverse','#c52d43')]:
  line=[(x0+w*p['fraction'],y0+h-h*p[key]/maximum) for p in g['poses']];d.line(line,fill=color,width=5)
 for f in [0,.25,.5,.75,1]:d.text((x0+w*f-10,y0+h+10),str(f),font=font(17),fill='#52657a')
 d.text((x0,y0+h+65),'Carrera por hoja: '+f"{g['stroke_m']:.4f} m",font=font(20),fill='#33465c')
d.text((80,955),'Ocre: contactos nuevos totales      Rojo: cruces transversales >10 µm',font=font(25,True),fill='#33465c')
footer(d,'No hay bolsillos certificados. Cero cruces transversales en D_POST no equivale a carrera libre: permanecen tangencias/bordes y posible contención.');im.save(O/'L02_carreras_contactos.png')
# Seat surfaces and human references.
im,d=base('VOY-02 · Asientos y referencias','Alturas de superficies reales medidas · escala 1,10 · postura y comodidad requieren validación propia')
seats=read('ergonomia_detallada.json')['seats'];left=400;barmax=900
for i,s in enumerate(seats):
 y=220+i*145;val=s['seat_height_above_floor_m'];d.text((70,y),s['id'],font=font(27,True),fill='#15263b');d.rectangle((left,y,left+barmax*val/.7,y+48),fill='#367da6');d.text((left+barmax*val/.7+18,y),f'{val:.3f} m',font=font(27,True),fill='#15263b');d.text((left,y+58),' / '.join(s['seat_object']),font=font(18),fill='#52657a')
footer(d,'Rayos sobre cojines, no máximos de carcasa. Navegación: referencia local Object_75; laterales: floorfront; mando: Mesh_1857. Proxies no son percentiles humanos.',y=1000);im.save(O/'L03_asientos_medidos.png')
im,d=base('VOY-02 · Presupuesto de imágenes','Hipótesis RGBA8 + mipmaps ideales ×4/3 · no es VRAM medida ni coste de Unreal')
m=read('materiales_rendimiento_revision.json')['texture_hypotheses'];keys=[('Resolución original','RGBA8_ideal_mips_MiB'),('Lado máximo 4096','cap4096_ideal_mips_MiB'),('Lado máximo 2048','cap2048_ideal_mips_MiB')]
for i,(label,key) in enumerate(keys):
 y=250+i*200;value=m[key];d.text((70,y),label,font=font(29,True),fill='#15263b');d.rectangle((450,y,450+value/2600*950,y+70),fill=['#ab4557','#d08b1b','#288f83'][i]);d.text((450,y+90),f'{value:.2f} MiB',font=font(29,True),fill='#15263b')
footer(d,'49 imágenes; mantiene proporción y redondea dimensiones enteras. No se han reducido archivos. Compresión, streaming y legibilidad LCARS requieren pruebas UE.',y=995);im.save(O/'L04_texturas_hipotesis.png')
# Contact sheets and navigable HTML preserving the native full-resolution captures.
manifest=sorted(read('capturas_manifest.json'),key=lambda x:x['file']);qa=[]
for page in range((len(manifest)+8)//9):
 im,d=base('VOY-02 · Capturas revisadas',f'Página {page+1} · Workbench diagnóstico · colores de módulo/adaptador, sin validación artística PBR',1600,1640)
 for k,row in enumerate(manifest[page*9:(page+1)*9]):
  x=35+(k%3)*525;y=160+(k//3)*470;pic=Image.open(R/'CAPTURAS'/row['file']);pic.thumbnail((500,330));im.paste(pic,(x+(500-pic.width)//2,y));d.text((x,y+338),row['file'][:44],font=font(17,True),fill='#15263b')
  for j,line in enumerate(textwrap.wrap(row['title'],48)[:2]):d.text((x,y+365+j*23),line,font=font(17),fill='#33465c')
  for j,line in enumerate(textwrap.wrap(row['note'] or 'Envolvente completa; laboratorio técnico.',53)[:2]):d.text((x,y+414+j*20),line,font=font(15),fill='#52657a')
 im.save(O/f'CONTACTO_{page+1:02d}.jpg',quality=90)
for row in manifest:
 with Image.open(R/'CAPTURAS'/row['file']) as im:resolution=list(im.size)
 qa.append(dict(file=row['file'],resolution=resolution,projected_bounds=row.get('projected_mesh_bounds'),bounds_pass=None if row.get('projected_mesh_bounds') is None else all(0<=v<=1 for v in row['projected_mesh_bounds'].values()),isolated_objects=row.get('temporarily_hidden_neighbors',0),review='Visual review via contact sheets and selected full-resolution views. Perspective details intentionally show local context; orthographic views include all selected mesh bounds.'))
body=''.join('<figure><a href="CAPTURAS/'+html.escape(m['file'])+'"><img loading="lazy" src="CAPTURAS/'+html.escape(m['file'])+'"></a><figcaption><b>'+html.escape(m['title'])+'</b><br>'+html.escape(m['note'])+'<small>'+html.escape(m['file'])+' · '+html.escape(m['scene'])+'</small></figcaption></figure>' for m in manifest)
(R/'GALERIA.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>VOY-02 · Galería técnica</title><style>body{background:#111e30;color:#edf4ff;font:17px Segoe UI,sans-serif;margin:35px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(430px,1fr));gap:25px}figure{margin:0;background:#20324b;padding:18px;border-radius:12px}img{width:100%;height:410px;object-fit:contain;background:#303030}figcaption{line-height:1.5}small{display:block;color:#a9bed6}a{color:#9cd8ff}</style><h1>Voyager · VOY-02</h1><p>Laboratorio técnico. Puertas abiertas estáticas; acceso central no demostrado; sin validación Unreal ni acabado PBR.</p><p><a href="README.md">Índice y nueve informes</a></p><main>'+body+'</main></html>',encoding='utf8')
(R/'DATOS/capturas_qa.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False),encoding='utf8');print('PLATES',len(list(O.glob('*'))),'CAPTURES',len(qa))
