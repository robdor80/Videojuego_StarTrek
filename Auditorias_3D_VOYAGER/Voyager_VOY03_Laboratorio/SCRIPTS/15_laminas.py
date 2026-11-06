from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
R=Path(__file__).resolve().parents[1]
fontpath='C:/Windows/Fonts/arial.ttf';F=lambda s:ImageFont.truetype(fontpath,s)
def page(title,subtitle='',size=(2000,1300)):
 im=Image.new('RGB',size,'white');d=ImageDraw.Draw(im);d.text((60,30),title,fill='#172c40',font=F(38));d.text((60,86),subtitle,fill='#45576b',font=F(22));return im,d
def save(im,name):im.save(R/'LAMINAS'/name)
m=json.loads((R/'DATOS/mediciones_finales.json').read_text());data=json.loads((R/'DATOS/barridos_resultados.json').read_text());routes=[r for r in data['results'] if r['height_m']==1.9];polys=json.loads((R/'DATOS/soportes_finales_plot.json').read_text())
im,d=page('VOY-03 | Superficies y recorridos sobre geometría original','Metros · marco A · escala 1,10 · todos los obstáculos presentes en los cálculos',size=(2000,2100));X=lambda x:round(100+(x+7.7)*115);Y=lambda y:round(1850-(y+6.4)*115)
colors=['#c5def4','#badfd1','#eedfb0','#d7c9ee','#b2c6d8']
for p in sorted(polys,key=lambda p:p['z']):
 z=p['z'];k=0 if z<.1 else 1 if z<.4 else 2 if z<.55 else 3 if z<.7 else 4;d.polygon([(X(v[0]),Y(v[1])) for v in p['points']],fill=colors[k])
for x in range(-7,8):d.text((X(x),1880),str(x),fill='#667788',font=F(18))
for y in range(-6,9):d.text((45,Y(y)),str(y),fill='#667788',font=F(18))
for r,c in zip(routes[:6],['#078342','#1260b5','#b57b00','#8b3bac','#b93737','#303030']):
 pts=[(X(p[0]),Y(p[1])) for p in r['foot_points']];d.line(pts,fill=c,width=4)
for label,x,y in [('CENTRO',0,-.77),('NAV.',-.8,-2.9),('MANDO I',-1.43,-.22),('MANDO D',1.43,-.22),('PASARELA',3.96,2.97),('POSTERIOR',1.3101,6.688)]:
 a,b=X(x),Y(y);d.ellipse((a-7,b-7,a+7,b+7),fill='white',outline='#172c40',width=2);d.text((a+10,b-27),label,fill='#172c40',font=F(19))
for i,(txt,col) in enumerate(zip(['NAV 0,023 m','ANILLO 0,327 m','CENTRO 0,479 m','PELDAÑO 0,631 m','PASARELA 0,784 m'],colors)):
 x=80+i*375;d.rectangle((x,1970,x+25,1995),fill=col);d.text((x+35,1972),txt,fill='black',font=F(19))
d.text((80,2020),'Superficies = inventario de apoyo corregido. La planta no representa una certificación de toda el área.',fill='#45576b',font=F(21));save(im,'02_planta_soportes_y_rutas.png')
for flight in m['lateral_flights']:
 im,d=page('VOY-03 | Sección medida — escalera '+flight['id'].lower(),'Perfil central a 2 mm · apoyos reales · la sección no sustituye el volumen de cápsula');ox,oy=220,1050;sx=950;sy=950
 P=lambda u,z:(ox+(u+.65)*sx,oy-z*sy)
 pts=[P(r['u_m'],r['z_m']) for r in flight['profile'] if r['z_m'] is not None];d.line(pts,fill='#172c40',width=5)
 for z in [.327403,.479442,.631488,.783525]:
  yy=P(0,z)[1];d.line((100,yy,1750,yy),fill='#ccd3dc',width=1);d.text((55,yy-30),f'{z:.3f} m',fill='#45576b',font=F(24))
 for i,r in enumerate(flight['risers']):
  x,y=P(r['position_u_m'],.9);d.text((x-80,y-50-i%2*45),f'{r["riser_m"]*100:.2f} cm',fill='#b34228',font=F(26));d.line((x,y,x,P(0,.35)[1]),fill='#b34228',width=2)
 d.text((180,1120),f'Huella por eje: {flight["tread_depth_axis_m"]*100:.2f} cm · 3 contrahuellas de 15,20 cm',fill='#172c40',font=F(29));d.text((180,1175),f'Altura libre mínima vertical en eje: {flight["min_vertical_headroom_centerline_m"]:.3f} m (contexto completo)',fill='#45576b',font=F(24));save(im,'03_seccion_'+flight['id'].lower()+'.png')
im,d=page('VOY-03 | Navegación — sección central','Las ondulaciones de 5,85 mm corresponden a rejillas y marcos superpuestos; no se borraron superficies')
P=lambda y,z:(180+(y+3)*900,1040-z*1400);pts=[];previous=None
for r in m['navigation_centerline_transitions']:
 if r['z_m'] is None:continue
 if previous is not None:pts.append(P(r['y_m'],previous))
 pts.append(P(r['y_m'],r['z_m']));previous=r['z_m']
pts.append(P(-1.2,previous));d.line(pts,fill='#172c40',width=5)
for z,txt in [(.0233257,'Foso 0,0233 m'),(.175364,'Marco peldaño 1: 0,1754 m'),(.327403,'Marco peldaño 2: 0,3274 m'),(.479442,'Centro 0,4794 m')]:
 x,y=P(-3,z);d.line((150,y,1850,y),fill='#cbd5df');d.text((200,y-40),txt,fill='#172c40',font=F(25))
d.text((180,1140),'Tres cambios nominales de nivel de 15,20 cm. Huellas centrales aproximadas: 26,2 y 27,4 cm.',fill='#172c40',font=F(26));d.text((180,1195),'Mesh_1856 = marcos / narices; Mesh_2121–2122 = rellenos de apoyo; Mesh_1810–1811 = remates.',fill='#45576b',font=F(23));save(im,'04_seccion_navegacion.png')
im,d=page('VOY-03 | Antes / después del recorrido — misma arquitectura','Rojo: candidato descartado por apoyo lateral. Verde: recorrido final. No se ha reparado ni ocultado ninguna pieza.')
old=json.loads((R/'DATOS/barridos_A1_sin_apoyo_continuo.json').read_text())['results'][2];new=next(r for r in routes if r['id']=='CENTRO_A_PASARELA')
P=lambda p:(220+(p[0]-2.8)*950,1050-(p[1]+1.1)*600)
for r,col in [(old,'#c03b3b'),(new,'#078342')]:d.line([P(p) for p in r['foot_points'] if 2.8<=p[0]<=4.5 and -1.1<=p[1]<=.0],fill=col,width=7)
for p in [[3.59,-.71],[4.00183,.04558]]:
 x,y=P(p);d.ellipse((x-16,y-16,x+16,y+16),outline='#172c40',width=3)
d.text((100,1160),'El apoyo continuo rechazó el intervalo 364 del candidato inicial. Se conservan JSON, log y capturas negativos.',fill='#45576b',font=F(25));save(im,'05_atajo_descartado_y_ruta_final.png')
im,d=page('VOY-03 | Cápsulas en el mismo punto crítico','Radio 0,35 m en las tres pruebas. Imágenes Blender de la geometría original; sin cambios de escala ni mobiliario.')
for i,h in enumerate([1.6,1.75,1.9]):
 src=Image.open(R/'CAPTURAS'/f'B06_capsula_{h:.2f}.png').convert('RGB');src.thumbnail((620,980));x=50+i*650;y=180;im.paste(src,(x,y));d.text((x+160,1120),f'{h:.2f} m',fill='#172c40',font=F(34))
save(im,'06_tres_alturas.png')
im,d=page('VOY-03 | Misma escalera, nuevo método de comprobación','Antes: pie fijo 2 mm sobre el suelo bajo el centro. Después: cápsula continua con apoyo real y contrahuella medida.')
for i,fn in enumerate(['A02_escalera_derecha_contexto.png','B03_escalera_derecha_apoyo.png']):
 src=Image.open(R/'CAPTURAS'/fn).convert('RGB');src.thumbnail((920,900));im.paste(src,(60+i*980,180))
d.text((80,1100),'Geometría original: conservada',fill='#172c40',font=F(29));d.text((1080,1100),'Opción A: sin reparación arquitectónica',fill='#078342',font=F(29));save(im,'07_comparativa_sin_reparacion.png')
print('LAMINAS_GENERATED')
