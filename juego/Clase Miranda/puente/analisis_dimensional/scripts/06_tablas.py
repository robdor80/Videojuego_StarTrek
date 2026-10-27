"""Python estándar; genera tablas en cm a partir de la inspección de Blender."""
import json,csv,math,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'datos/inventario.json').read_text(encoding='utf-8'))
g=json.loads((ROOT/'datos/grupos_medidos.json').read_text(encoding='utf-8'))
r=json.loads((ROOT/'datos/mediciones_rayos.json').read_text(encoding='utf-8'))
s=json.loads((ROOT/'datos/sondeos.json').read_text(encoding='utf-8'))
with (ROOT/'Inventario_objetos_cm.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f,delimiter=';');w.writerow(['objeto','tipo','padre','malla','vertices','min_X_cm','min_Y_cm','min_Z_cm','max_X_cm','max_Y_cm','max_Z_cm','dimension_X_cm','dimension_Y_cm','dimension_Z_cm','escala_local','matriz_mundial_en_inventario_json'])
    for o in d['objects']:
        b=o['bounds_world_bu'];values=[round(v*100,5) for key in ['min','max','dimensions'] for v in b[key]] if b else ['']*9
        w.writerow([o['name'],o['type'],o['parent'],o.get('mesh',''),o.get('vertices','')]+values+[str(o['scale']),'datos/inventario.json'])
rows=[]
def add(id,element,value,method,evidence,uncertainty):rows.append({'id':id,'elemento':element,'medida_cm':round(value,3),'metodo':method,'evidencia':evidence,'incertidumbre':uncertainty})
def dist(a,b):return math.dist(a,b)*100
for z in [.1,1.5,2.5,3.7,3.8]:
    a=r[f'portal_turbo_o0_z{z}_s-1']['hits'][0]['point'];b=r[f'portal_turbo_o0_z{z}_s1']['hits'][0]['point']
    add(f'D1_W_{z}','Puerta turbo: anchura de marco a Z='+str(z*100),dist(a,b),'distancia entre impactos, hojas excluidas',f'portal_turbo_o0_z{z}_s+/-1','muestreo; no barrido de colisión')
add('D1_H','Puerta turbo: dintel central',r['dintel_turbo_o0_s0']['hits'][0]['point'][2]*100-.1001,'rayo vertical menos suelo','dintel_turbo_o0_s0; turbo_centro','suelo de cabina +0.1001 cm')
add('D2_W','Puertas +Y: anchura',dist(r['portal_Ypos_x6.49_z3.1_s-1']['hits'][0]['point'],r['portal_Ypos_x6.49_z3.1_s1']['hits'][0]['point']),'impactos a 250 cm sobre suelo +60 cm','portal_Ypos_x6.49_z3.1_s+/-1','lado X positivo medido; opuesto similar')
add('D2_H','Puertas +Y: altura central',r['dintel_Ypos_x6.49']['hits'][0]['point'][2]*100-60,'rayo vertical menos suelo','dintel_Ypos_x6.49','lado opuesto presenta ~1 cm de diferencia en hojas')
for id,key,point,floor in [('T1','Techo turbo central','turbo_centro',.1001),('T2','Techo turbo fuera de luminaria','vertical_-7_-9',.1001),('T3','Techo lateral','vertical_5.3_-3.7',0),('T4','Techo franja -Y','vertical_0_-8.5',0),('T5','Techo plataforma +Y','vertical_0_0.6',60),('T6','Techo lateral plataforma +Y','vertical_5.5_0.6',60)]:
    hits=(s.get(point) or r[point]['hits']);hits=[h for h in hits if h['point'][2]>3]
    add(id,key,hits[0]['point'][2]*100-floor,'primer impacto vertical sobre la zona',point,'medida local; techo estratificado')
for id,key,group in [('C1','Consola central: superficie','superficie_central'),('C2','Consola central: panel turbolcar','controles_centrales'),('L1','Consola lateral: superficie de control lcardtype','superficie_lateral'),('L2','Consola lateral: soporte gris bajo controles','soporte_lateral')]:
    add(id+'_MIN',key+' mínimo Z',g[group]['todo']['min_cm'][2],'extremos de vértices mundiales',group,'identificación por geometría/material')
    add(id+'_MAX',key+' máximo Z',g[group]['todo']['max_cm'][2],'extremos de vértices mundiales',group,'identificación por geometría/material')
add('S1','Capitán: asiento sobre podio',s['capitan'][4]['point'][2]*100-29.9,'superficie superior en X=0 Y=-180 cm','mueble_0_-1.8','punto local del cojín; curvatura')
add('S2','Capitán: apoyabrazos superior sobre podio',g['apoyabrazos_capitan']['todo']['max_cm'][2]-29.9,'máximo mundial menos suelo del podio','apoyabrazos_capitan','superficie inclinada')
add('S3','Silla lateral: asiento sobre suelo',r['mueble_4.7_-3.7']['hits'][0]['point'][2]*100,'rayo sobre cojín','mueble_4.7_-3.7','punto representativo; seis sillas')
add('P1','Paso entre consola central y base silla derecha',dist(r['pasillo_d_y-3.7_z0.1']['hits'][0]['point'],r['pasillo_i_y-3.7_z0.1']['hits'][0]['point']),'corte horizontal Z=10 cm Y=-370 cm','pasillo_d/i_y-3.7_z0.1','sección local; no anchura mínima global')
(ROOT/'datos/medidas_resumen.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
with (ROOT/'Medidas_cm.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
# Leer solo la cabecera JSON del GLB; no importar ni escribir el original.
with Path(d['glb']).open('rb') as f:
    header=f.read(12);length,kind=struct.unpack('<I4s',f.read(8));glb=json.loads(f.read(length))
(ROOT/'datos/glb_metadatos.json').write_text(json.dumps({'header':list(struct.unpack('<4sII',header))[1:],'asset':glb.get('asset'),'nodes':len(glb.get('nodes',[])),'meshes':len(glb.get('meshes',[])),'scenes':glb.get('scenes'),'note':'Lectura de metadatos; sin modificación, sin reinterpretar escala.'},indent=2,ensure_ascii=False),encoding='utf-8')
print('TABLAS_OK',len(rows),'medidas',len(d['objects']),'objetos')
