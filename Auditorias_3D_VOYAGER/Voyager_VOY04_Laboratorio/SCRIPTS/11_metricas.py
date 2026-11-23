import json,sys,csv,math,collections,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import *;from geom import ray
def save(n,x):(R/'DATOS'/n).write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf8')
e=Env();seqs=json.loads((R/'DATOS/trayectorias.json').read_text());out=[];screens=[]
for key in ['Plane_94','Plane_95','Plane_96','Plane_139','Plane_138','Plane_140']:
 q=e.tri[e.names==key].reshape(-1,3);center=q.mean(0);_,_,v=np.linalg.svd(q-center);n=v[-1];n*=np.sign(n[2]);screens.append(dict(key=key,local_center=center.tolist(),local_normal=n.tolist(),plane_d=float(center@n),planarity_m=float(np.abs((q-center)@n).max()),local_lo=q.min(0).tolist(),local_hi=q.max(0).tolist(),source_materials=next(r['materials'] for r in e.rows if r['key']==key)))
save('consola_superficies.json',screens)
for seq in seqs:
 H=seq['H'];cfg=seq['config'];ee=Env().adapted(cfg['drop'],cfg['backshift']).rail(cfg['D']);p=seq['poses'][150];b=p['body'];parts={pt['name']:pt for pt in b['parts']};head=np.array(parts['CABEZA']['p']);eyes=head+[0,.055*H,.015*H];center=(np.array(screens[0]['local_center'])+screens[1]['local_center'])/2;view=center-eyes;angle=math.degrees(math.atan2(-view[2],np.linalg.norm(view[:2])));hands=[]
 for side,key in [(-1,'Plane_95'),(1,'Plane_94')]:
  part=parts[f'MANO_{side}'];sc=next(x for x in screens if x['key']==key);normal=np.array(sc['local_normal']);tip=np.array(part['q']);axis_gap=float(tip@normal-sc['plane_d']);dist=segment_tri(np.array(part['p']),tip,ee.tri[ee.names==key])-part['r'];j=b['joints'];sh=np.array(j[f'shoulder_{side}']);el=np.array(j[f'elbow_{side}']);w=np.array(part['p']);v1=sh-el;v2=w-el;elbow=math.degrees(math.acos(np.clip(np.dot(v1,v2)/np.linalg.norm(v1)/np.linalg.norm(v2),-1,1)))
  hands.append(dict(side=side,screen=key,shoulder_to_hand_m=float(np.linalg.norm(sh-tip)),capsule_tip_gap_to_plane_m=axis_gap-part['r'],minimum_to_screen_m=float(dist.min()),elbow_inner_angle_deg=elbow))
 backtri=ee.tri[np.isin(ee.names,['Object_76','Layer__3'])];back=[]
 for part in b['parts']:
  if part['name'].startswith('TORSO'):back.append(float(segment_tri(np.array(part['p']),np.array(part['q']),backtri).min()-part['r']))
 # Ray to center identifies first geometry: a visibility test for a point, not the complete screen.
 visibility=[]
 for sc in screens[:2]:
  v=np.array(sc['local_center'])-eyes;hit=ray(ee.tri,eyes,v/np.linalg.norm(v),np.linalg.norm(v)+.005);visibility.append(dict(screen=sc['key'],first_hit=str(ee.names[hit['triangle']]) if hit else None,visible=bool(hit and str(ee.names[hit['triangle']])==sc['key'])))
 row=dict(H=H,original_seat_height_m=e.m['seat_above_floor_m'],adapted_seat_height_over_local_foot_floor_m=e.P[2]-cfg['drop']-.0233257818,seat_drop_m=cfg['drop'],back_shift_m=cfg['backshift'],travel_m=cfg['D'],eyes_local=eyes.tolist(),look_down_to_center_deg=angle,visibility=visibility,hands=hands,backrest_min_capsule_gap_m=min(back),work_pose_geom=seq['config']['complete_sampled_body_clear'],back_support_certified=False,biomechanics_certified=False);out.append(row);print('ERGONOMY',row,flush=True)
save('ergonomia_resultados.json',out)
# Reference chair component roles, including common dais/bearing context.
inv=json.loads((R/'DATOS/inventario_medidas.json').read_text());components=[]
for m in inv:
 ee=Env(m['id']);p=np.array(m['seat_point']);hit=ray(ee.tri,[0,0,-.085],[0,0,-1],1)
 for part in m['pieces']:
  key=part['key'];lo=part['local_lo'];hi=part['local_hi']
  if key in m['seat_cushion_keys']:role='cojin_asiento'
  elif key.startswith('Armrest'):role='reposabrazos_existente'
  elif key.startswith('ChamferBox'):role='cojin_respaldo'
  elif key.startswith('Layer'):role='tapizado_respaldo'
  elif key in ['Object_76','Object_121','Object_123']:role='carcasa_respaldo'
  elif key in ['Object_77','Object_120','Object_122']:role='carcasa_asiento'
  elif key=='MSB_30191':role='pedestal_inferior_sin_guia_acreditada'
  elif key in ['MSB_30194','MSB_30200','MSB_30211']:role='vástago_superior'
  elif m['id'].startswith('LATERAL') and hi[2]<-.40:role='base_rueda_soporte_inferior_revisar_desglose'
  elif key.startswith('Box'):role='carcasa_mando'
  else:role='soporte_o_remate'
  components.append(dict(station=m['id'],key=key,role=role,dimensions_m=part['dimensions'],bounds_local=[lo,hi],materials=part['materials'],mechanism_proven=False))
save('componentes_clasificados.json',components)
with (R/'DATOS/objetos_sillas.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['puesto','objeto','funcion','ancho_local_m','fondo_local_m','alto_m','mecanismo_acreditado']);w.writerows([[r['station'],r['key'],r['role'],*r['dimensions_m'],False] for r in components])
comparison=[]
for m in inv:
 grade='C' if m['id']=='NAVEGACION' else 'E';comparison.append(dict(id=m['id'],parts=len(m['parts']),seat_height_m=m['seat_above_floor_m'],geometry_family='pedestal_8' if m['id']=='NAVEGACION' else 'ruedas_31' if m['id'].startswith('LATERAL') else 'mando_11',grade=grade,reason='Intervencion local: altura, apoyo, respaldo y mecanismo nuevo; prototipo muestreado positivo, ergonomia completa pendiente' if grade=='C' else 'Inventario y dimensiones, sin prueba articulada completa de entrada/trabajo/salida; no promover a A',reusable_method=True))
save('comparacion_puestos.json',comparison)
with (R/'DATOS/comparacion_puestos.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['puesto','piezas','familia','altura_asiento_m','grado','motivo']);w.writerows([[x['id'],x['parts'],x['geometry_family'],x['seat_height_m'],x['grade'],x['reason']] for x in comparison])
