import json,collections,csv,hashlib,sys
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from importlib import import_module
ray=import_module('06_sondear').ray
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
obs={x['object']:x for x in read('DATOS/coleccion_auditoria.json')['objects']};loops=read('DATOS/bordes_abiertos.json');surfs=read('DATOS/superficies_candidatas.json');byS={s['id']:s for s in surfs};oldclass={x['mesh']:x['family'] for x in read('REFERENCIAS/clasificacion_modulos.json')}
rows=[];decisions=[]
def base(id,obj,kind,center,normal,w,h):
 o=obs.get(obj,{});return dict(id=id,source='coleccion',source_file='FUENTES/COLECCION/star-trek-voyager-collection/source/StarTrekVoyagerCollection.blend',scene=o.get('scenes'),collections=o.get('collections'),objects=[obj],meshes=[o.get('mesh')],architectural_context=oldclass.get(obj,'puente_detallado'),kind=kind,center_world=center,normal_world=normal,tangent_world=np.cross([0,0,1],normal).tolist(),matrix_source=o.get('matrix_world'),object_scale=o.get('scale'),unit='m provisional: 1 unidad de mundo = 1 m; no certificacion canonica',applied_audit_scale=1.0,width=w,height=h,frame_depth=None,leaf_dimensions=None,leaf_count=0,opening_type='sin hojas; mecanismo no suministrado',frame_independent=False,pocket_status='No hay bolsillo certificado; no deducirlo de una pared superficial',grade='B',grade_scope='interfaz abierta existente: conservar arquitectura y diseñar inserto; no sistema de puerta independiente',materials=o.get('materials'),uv=o.get('uv_layers'),geometry_status=dict(boundary=o.get('weld_10um_boundary'),nonmanifold=o.get('weld_10um_nonmanifold')),floor_relation='cota inferior de perfil; soporte continuo no validado',wall_relation='marco/contorno incluido en arquitectura fuente',ceiling_relation='perfil superior medido; volumen completo no validado',obstacles=['sin marco intercambiable ni cavidad certificada'],recommendation='Conservar arquitectura; proponer marco y mecanismo independiente en fases futuras',reconstruction_required='sistema ausente; habrá que suministrarlo',capture=f'CAPTURAS/{id}.png',context_capture=f'CAPTURAS/CAT_{obj}_ISO.png',measurement_method='perfil del borde geometrico soldado solo para analisis a 10 um',measurement_confidence='alta para contorno, media para funcion',profile_ref=None)
for l in loops:
 selected=l['vertical'] and l['width']>=.5 and l['height']>=.65 and l['plane_error']<.07 and l['object'] not in ['Mesh53','Mesh55','Mesh93']
 reason='perfil de acceso' if selected else 'borde no aceptado como acceso: pequeño, horizontal, ventana inclinada, no plano o perimetro exterior de placa'
 decisions.append(dict(id=l['id'],selected=bool(selected),reason=reason))
 if not selected:continue
 r=base(l['id'].replace('L_','AC_'),l['object'],'hueco_o_boca',l['center'],l['normal'],l['width'],l['height']);r['profile_ref']=l['id'];r['profile_points']=l['points'];r['profile_segments']=l['segments'];r['plane_error_m']=l['plane_error'];r['floor_z']=l['lo'][2];r['border_cycle']=l['cycle'];r['widths_by_height']=[]
 tan=np.array(l['tangent']);pp=np.array(l['points']);umin=(pp@tan).min();umax=(pp@tan).max()
 for dz in [.2,.4,1.,1.7,2.2]:
  z=l['lo'][2]+dz;inter=[]
  for aa,bb in l['segments']:
   aa=np.array(aa);bb=np.array(bb)
   if (aa[2]<=z<bb[2]) or (bb[2]<=z<aa[2]):inter.append(float((aa+(bb-aa)*(z-aa[2])/(bb[2]-aa[2]))@tan))
  inter=sorted(set(round(x,6) for x in inter));r['widths_by_height'].append(dict(above_bottom=dz,width=(inter[-1]-inter[0]) if len(inter)>=2 else None,intersections=inter))
 if l['object'] in ['Mesh2','Mesh24','Mesh45','Mesh62'] or not l['cycle']:
  r['grade']='C';r['measurement_confidence']='media: borde abierto/ramificado o perfil no plano';r['obstacles'].append('sanear borde antes de definir montaje')
 if l['object'] in ['Mesh7','Mesh103'] and l['vertices']==4:
  r['grade']='E';r['kind']='abertura_estructural_funcion_no_confirmada';r['recommendation']='Confirmar funcion antes de convertir en acceso';r['measurement_confidence']='alta geometria, baja semantica'
 if l['height']<1.3:r['kind']='conducto_bajo_o_escotilla';r['opening_type']='paso tecnico bajo sin hojas';r['obstacles'].append('No apto para personaje de pie')
 rows.append(r)
# Horizontal shaft mouths (two ends of the same shaft are distinct ports, not two doors).
shaft_objects=['Mesh16','Mesh65','Mesh67','Mesh73','Mesh76','Mesh78','Mesh79','Mesh82','Mesh83']
for l in loops:
 if l['object'] not in shaft_objects or l['height']>.001:continue
 size=np.array(l['hi'])-l['lo']
 if min(size[:2])<.5:continue
 r=base(l['id'].replace('L_','AC_'),l['object'],'boca_vertical',l['center'],[0,0,1],float(size[0]),float(size[1]));r['profile_ref']=l['id'];r['profile_points']=l['points'];r['profile_segments']=l['segments'];r['height_meaning']='segunda dimension horizontal Y; altura del hueco no aplica';r['shaft_pair']=l['object']+'_EJE_VERTICAL';r['floor_z']=l['lo'][2];r['grade']='C';r['obstacles']=['abertura en suelo/techo; requiere seguridad y conexion vertical; no puerta de pie'];rows.append(r)
# Mesh54 has a roof opening and a detached cover perimeter: one aperture, not two holes.
l=next(x for x in loops if x['id']=='L_Mesh54_02');r=base('AC_Mesh54_TECHO','Mesh54','registro_techo_con_tapa',l['center'],[0,0,1],l['hi'][0]-l['lo'][0],l['hi'][1]-l['lo'][1]);r.update(profile_ref=l['id'],profile_points=l['points'],profile_segments=l['segments'],leaf_count=1,opening_type='tapa; articulacion no identificada',grade='C',shaft_pair=None,height_meaning='segunda dimension horizontal',obstacles=['tapa es isla de la misma malla; no objeto separado; sin articulacion']);rows.append(r)
# Closed doors visually confirmed in elevations. Seeds identify actual coplanar source faces.
seeds=['S_Mesh14_0248','S_Mesh14_0249','S_Mesh25_0337','S_Mesh26_0344','S_Mesh54_0509','S_Mesh54_0511','S_Mesh51_0449','S_Mesh51_0452','S_Mesh28_0363','S_Mesh28_0367','S_Mesh57_0514','S_Mesh57_0522','S_Mesh52_0463','S_Mesh52_0465','S_Mesh80_0816','S_Mesh80_0833','S_Mesh27_0352','S_Mesh53_0502','S_Mesh55_0512','S_Mesh93_0951']
for seed in seeds:
 s=byS[seed];n=np.array(s['normal']);n/=np.linalg.norm(n);tan=np.cross([0,0,1],n);plane=s['plane'];parts=[];local_tri=[]
 for ss in surfs:
  if ss['object']!=s['object']:continue
  ns=np.array(ss['normal']);ns/=np.linalg.norm(ns);sign=1 if ns@n>0 else -1
  if abs(ns@n)>.99999 and abs(ss['plane']*sign-plane)<.003:parts.append(ss)
 pts=[]
 # Read actual triangles of the candidate planes; merge roundoff partitions only.
 z=np.load(R/'DATOS/coleccion_geometria.npz');tr=z['vertices'][z['triangles'][z['object_ids']==list(obs).index(s['object'])]]
 for part in parts:pts.extend(tr[part['triangles']].reshape(-1,3).tolist());local_tri.extend(part['triangles'])
 p=np.array(pts);u=p@tan;c=n*(p@n).mean()+tan*(u.min()+u.max())/2+[0,0,(p[:,2].min()+p[:,2].max())/2];w=float(np.ptp(u));h=float(np.ptp(p[:,2]));count=sum(x['objects']==[s['object']] and x['kind']=='puerta_cerrada' for x in rows)+1
 r=base(f'PT_{s["object"]}_{count:02}',s['object'],'puerta_cerrada',c.tolist(),n.tolist(),None,None);r.update(front_surface_envelope=dict(width=w,height=h,normal_extent=float(np.ptp(p@n))),front_surface_triangles=sorted(set(local_tri)),surface_ref=seed,measurement_method='envolvente de caras frontales coplanares; NO anchura/altura libre de vano',measurement_confidence='alta para envolvente frontal; vano libre sin medir',leaf_count=2,opening_type='doble corredera lateral aparente; no mecanismo existente',grade='C',grade_scope='sistema integrado en una sola malla conectada con mamparo/marco',leaf_dimensions=dict(combined_front_width=w,combined_front_height=h,per_leaf=None,thickness=None),obstacles=['hojas/marco/mamparo conectados tras soldadura diagnostica','cavidad fisica no acreditada','dimension frontal no certifica vano libre'],reconstruction_required='separacion importante; reconstruir alojamientos y marco modular',floor_z=float(p[:,2].min()),frame_depth=None)
 if s['object'] in ['Mesh27','Mesh53']:
  r['opening_type']='cierre asimetrico: dos grupos visuales; movimiento por determinar';r['leaf_count']=None
 if s['object'] in ['Mesh53','Mesh55','Mesh93']:
  r['grade']='D';r['grade_scope']='placa completa independiente como objeto, hojas y marco fusionados; reconstruccion modular recomendada';r['obstacles'].append('envolvente normal de placa completa ~73 mm; sin bolsillo');r['recommendation']='Usar como referencia visual y reconstruir modulo completo';r['reconstruction_required']='recomendada'
 rows.append(r)
# Three existing bridge pairs: new static measurements; no movement is executed.
z=np.load(R/'DATOS/puente_obj_geometria.npz');tr=z['vertices'][z['triangles']];ids=z['object_ids'];bo=read('DATOS/puente_obj_auditoria.json')['objects'];bn=[o['object'] for o in bo]
for i,d in enumerate(read('REFERENCIAS/puertas_medidas.json'),1):
 n=np.array(d['normal']);t=np.array(d['tangent']);c=np.array(d['center']);groups=[d['leafA'],d['leafB']];dims=[]
 for group in groups:
  p=tr[np.isin(ids,[bn.index(x) for x in group])].reshape(-1,3);dims.append(dict(objects=group,width=float(np.ptp(p@t)),height=float(np.ptp(p[:,2])),thickness_envelope=float(np.ptp(p@n)),z_min=float(p[:,2].min()),z_max=float(p[:,2].max())))
 context=tr[~np.isin(ids,[bn.index(x) for group in groups for x in group])];ww=[];depth_samples=[]
 for h in [.1,.4,1.,1.5,1.7]:
  values=[]
  for off in [-.08,-.04,-.02,0,.02,.04,.08]:
   p=c+n*off+[0,0,h];aa=ray(context,p,-t,2);bb=ray(context,p,t,2);w=aa['distance']+bb['distance'] if aa and bb else None;depth_samples.append(dict(height=h,normal_offset=off,width=w))
   if w is not None and .4<w<1.5:values.append(w)
  ww.append(dict(above_floor=h,width=min(values) if values else None))
 heights=[]
 for off in [-.08,-.04,-.02,0,.02,.04,.08]:
  hh=ray(context,c+n*off+[0,0,.01],[0,0,1],4)
  if hh:heights.append(hh['point'][2]-c[2])
 height=min(heights) if heights else None;r=base(f'BR_{i:02}',None,'puerta_cerrada',c.tolist(),n.tolist(),ww[1]['width'],height)
 r.update(source='puente_obj',source_file='FUENTES/PUENTE/Voyager Bridge.obj',scene=['Scene'],collections=['Scene Collection'],objects=sum(groups,[]),meshes=[bo[bn.index(x)]['mesh'] for x in sum(groups,[])],architectural_context='puente_detallado',legacy_id=d['id'],object_scale=[1,1,1],matrix_source='ver DATOS/puente_obj_auditoria.json para cada fragmento',leaf_count=2,leaf_dimensions=dims,grade='C',grade_scope='hojas recuperables por grupos (B); marcos/mamparos/alojamientos requieren intervencion (C)',opening_type='doble corredera lateral aparente',measurement_method='medicion estatica actual; rayos al contexto sin hojas, 7 planos normales entre -80 y +80 mm; minimo muestreado, no barrido continuo',widths_by_height=ww,depth_ray_samples=depth_samples,floor_z=float(c[2]),experimental_1p10=dict(width=ww[1]['width']*1.1 if ww[1]['width'] else None,height=height*1.1 if height else None,leaf_dimensions=[dict(width=q['width']*1.1,height=q['height']*1.1,thickness=q['thickness_envelope']*1.1) for q in dims]),leaf_groups_independent=True,materials=sorted(set(m for x in sum(groups,[]) for m in bo[bn.index(x)]['materials'] if m)),uv=['UVMap: ver auditoria por fragmento'],context_capture=f'CAPTURAS/BR_{d["id"]}_CONTEXTO.png',obstacles=['marcos fijos integrados en contexto','escala 1.10 experimental','interferencias historicas VOY02; no repetidas en VOY05A'],reconstruction_required='alojamientos y marco; conservar hojas si encajan',pocket_status='No certificado. VOY02 documenta cruces transversales laterales; posterior solo contactos sin bolsillo probado')
 rows.append(r)
l=next(x for x in read('DATOS/bordes_puente_obj.json') if x['id']=='L_PUENTE_AGREGADO_225');r=base('BR_04',None,'acceso_turbolift_sin_hojas',l['center'],l['normal'],l['width'],l['height']);r.update(source='puente_obj',source_file='FUENTES/PUENTE/Voyager Bridge.obj',objects=['ver objetos intersectados en DATOS/BR04_contexto.json'],scene=['Scene'],collections=['Scene Collection'],architectural_context='puente_detallado',profile_ref=l['id'],profile_points=l['points'],grade='E',grade_scope='borde ramificado y ligeramente no plano; montaje y vano minimo pendientes',measurement_method='envolvente de borde soldado del acceso de cabina; no ancho minimo garantizado',floor_z=l['lo'][2],plane_error_m=l['plane_error'],context_capture='CAPTURAS/BR_GENERAL.png',obstacles=['cabina existente; sin hojas identificadas','borde no ciclico','confirmar vano minimo y suelo de transicion']);rows.append(r)
# Profiles are grouped independently from complete-door geometry. Rounded dimensions are not identity.
keys=sorted(set((x['kind'],round(x['width'],3) if x['width'] is not None else None,round(x['height'],3) if x['height'] is not None else None) for x in rows),key=str);profiles={k:f'FP_{i+1:02}' for i,k in enumerate(keys)}
for x in rows:
 key=(x['kind'],round(x['width'],3) if x['width'] is not None else None,round(x['height'],3) if x['height'] is not None else None);x['dimensional_group']=profiles[key]
 if x['kind']=='puerta_cerrada':
  obj=x['objects'][0];x['visual_family']='V_PUENTE_DETALLADO' if x['source']=='puente_obj' else ('V_CIERRE_ASIMETRICO' if obj in ['Mesh27','Mesh53'] else 'V_BIPARTIDA_LCARS')
 else:x['visual_family']='V_TECNICA' if x['kind'] in ['boca_vertical','conducto_bajo_o_escotilla','registro_techo_con_tapa'] else 'V_CONTORNO_SIN_HOJAS'
 x['architectural_family']=('AR_CIERRE_ASIMETRICO' if x['visual_family']=='V_CIERRE_ASIMETRICO' else 'AR_PUENTE_DETALLADO' if x['source']=='puente_obj' else 'AR_PUERTA_BIPARTIDA' if x['kind']=='puerta_cerrada' else 'AR_CONDUCTO_BAJO' if x['kind']=='conducto_bajo_o_escotilla' else 'AR_EJE_VERTICAL' if x['kind']=='boca_vertical' else 'AR_REGISTRO_TECHO' if x['kind']=='registro_techo_con_tapa' else 'AR_HUECO_HABITACION' if x['objects'][0] in ['Mesh4','Mesh5','Mesh6','Mesh7','Mesh9','Mesh10','Mesh11','Mesh81','Mesh103'] else 'AR_TURBOLIFT' if x['objects'][0] in ['Mesh17','Mesh37','Mesh42','Mesh94'] and x['width']<1.5 else 'AR_MANTENIMIENTO' if x['architectural_context']=='mantenimiento' else 'AR_BOCA_MODULAR')
 x['mechanical_family']='MC_DOBLE_LINEAL_CANDIDATA' if x['kind']=='puerta_cerrada' and x['visual_family']!='V_CIERRE_ASIMETRICO' else 'MC_INDETERMINADA' if x['visual_family']=='V_CIERRE_ASIMETRICO' else 'MC_TAPA_POR_DEFINIR' if x['kind']=='registro_techo_con_tapa' else 'MC_NO_SUMINISTRADA'
(R/'DATOS/inventario_puertas_accesos.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8');(R/'DATOS/decisiones_bordes.json').write_text(json.dumps(decisions,indent=2,ensure_ascii=False),encoding='utf8')
fields=list(dict.fromkeys(k for x in rows for k in x))
with (R/'DATOS/inventario_puertas_accesos.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in x.items()} for x in rows)
summary=dict(total_records=len(rows),kinds=dict(collections.Counter(x['kind'] for x in rows)),grades=dict(collections.Counter(x['grade'] for x in rows)),architectural_families=dict(collections.Counter(x['architectural_family'] for x in rows)),dimensional_groups=len(keys),closed_doors=sum(x['kind']=='puerta_cerrada' for x in rows),complete_independent_doors=0,bridge_leaf_groups_independent=3,closed_doors_C=sum(x['grade']=='C' and x['kind']=='puerta_cerrada' for x in rows),closed_doors_D=sum(x['grade']=='D' and x['kind']=='puerta_cerrada' for x in rows),bridge_records=4)
(R/'DATOS/recuentos.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf8');print(json.dumps(summary,indent=2,ensure_ascii=False))
