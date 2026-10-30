import pathlib,json,math,csv
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
g=json.loads((OUT/'geometria.json').read_text(encoding='utf-8'))
inv=json.loads((OUT/'01_inventario_inicial.json').read_text(encoding='utf-8'))
stats=json.loads((OUT/'geometry_analysis.json').read_text(encoding='utf-8'))
world=json.loads((OUT/'world_geometry.json').read_text(encoding='utf-8'))
def quat(R):
    # Rotation matrix -> quaternion, robust for 180-degree rotations.
    K=np.array([[R[0,0]-R[1,1]-R[2,2],R[1,0]+R[0,1],R[2,0]+R[0,2],R[2,1]-R[1,2]],
                [R[1,0]+R[0,1],R[1,1]-R[0,0]-R[2,2],R[2,1]+R[1,2],R[0,2]-R[2,0]],
                [R[2,0]+R[0,2],R[2,1]+R[1,2],R[2,2]-R[0,0]-R[1,1],R[1,0]-R[0,1]],
                [R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1],R.trace()]])/3
    val,v=np.linalg.eigh(K); q=v[:,-1]
    return q.tolist()
def local_mesh(path):
    vv=[];tt=[]
    for s in g['meshes'][path]['sections']:
        tt.extend((np.array(s['triangles']).reshape(-1,3)+len(vv)).tolist()); vv.extend(s['vertices'])
    return np.array(vv),np.array(tt)
def fitted_boxes(name):
    entry=next(s for s in stats if s['name']==name)
    instance=next(i for i in g['instances'] if i['label']==name)
    v,t=local_mesh(instance['mesh']); boxes=[]
    for idx,island in enumerate(entry['islands']):
        pts=np.unique(np.round(v[t[island['triangle_indices']].ravel()],5),axis=0)
        vals,R=np.linalg.eigh(np.cov(pts.T))
        if np.linalg.det(R)<0:R[:,0]*=-1
        pp=pts@R; mn=pp.min(axis=0);mx=pp.max(axis=0)
        boxes.append({'name':f'F07_{name}_{idx:02}','center':(((mn+mx)/2)@R.T).tolist(),
                      'dims':np.maximum(mx-mn,.1).tolist(),'quaternion':quat(R),
                      'world_min':island['min'],'world_max':island['max']})
    return boxes
doors=[]
spec=[('F07_D01_IZQ_TRAS_ESCALERA',1,['Plane_001_0','Plane_017_0'],[2],False),
      ('F07_D02_IZQ_FRENTE_DERECHA',1,['Plane_018_0','Plane_019_0'],[2],False),
      ('F07_D03_DER_FRENTE_IZQUIERDA',-1,['Plane_001_0','Plane_017_0'],[4],False),
      ('F07_D04_TURBOASCENSOR_INTERIOR',-1,['Plane_018_0','Plane_019_0'],[1,4,5],True)]
for num,(human,sign,names,imgs,turbo) in enumerate(spec,1):
    parts=[]; pts=[]
    for name in names:
        entry=next(s for s in stats if s['name']==name)
        island=next(it for it in entry['islands'] if it['center'][0]*sign>0)
        p=np.array(world[name]['v'])[np.array(world[name]['t'])[island['triangle_indices']].ravel()]
        pts.extend(p.tolist()); parts.append({'actor':world[name]['actor'],'mesh':world[name]['mesh'],'bounds':[island['min'],island['max']],
                                              'triangle_indices':island['triangle_indices'],'shared_with_opposite_door':True})
    pts=np.array(pts);center=(pts.min(axis=0)+pts.max(axis=0))/2
    xy=pts[:,:2];val,axes=np.linalg.eigh(np.cov(xy.T)); tangent=axes[:,-1]
    if tangent[1]<0:tangent=-tangent
    normal=np.array([tangent[1],-tangent[0]])*sign
    width=float(np.ptp(xy@tangent));height=float(np.ptp(pts[:,2]))
    door={'id':f'DOOR_F07_{num:03}','human_id':human,'map':'/Game/maps/L_F07_Sutherland_Test',
          'center_cm':center.tolist(),'normal_outward_xy':normal.tolist(),'tangent_xy':tangent.tolist(),
          'measured_leaf_envelope_width_cm':width,'measured_leaf_envelope_height_cm':height,
          'bounds_cm':[pts.min(axis=0).tolist(),pts.max(axis=0).tolist()],
          'capsule_diameter_cm':70,'capsule_height_cm':180,'parts':parts,
          'frame_assets':['Plane_004_0','Plane_011_0','Plane_039_0'] if turbo else (['Plane_004_0','Plane_011_0'] if num==2 else ['Plane_001_0 (hojas, no marco)','Plane_013_0','Plane_005_0']),
          'destination':'CABINA_TURBOASCENSOR_EXISTENTE' if turbo else 'DESTINO_NO_CONSTRUIDO',
          'reference_images':imgs,'confidence':'ALTA en geometria; emparejamiento verbal D02/D03 contradicho por coordenadas',
          'separability':'Cada asset contiene una hoja en dos accesos opuestos; no son componentes animables por puerta',
          'status':'REQUIERE SEPARACION EN BLENDER','collision_preparation':'Dos cajas por asset compartido, una por isla; nunca una caja que una ambos lados',
          'future_motion':'Hipotesis: bipartida a lo largo de tangent_xy, dos sentidos; validar bolsillos y pivotes',
          'closed_test':'PENDIENTE','open_test':'PENDIENTE','frame_void_dimensions':'Vano funcional pendiente de medicion por barrido; envolvente de hojas no equivale a hueco libre'}
    doors.append(door)
catalog={'known_doors':4,'matched':4,'orientation':{'forward':'+Y, pantalla en y=1000; capitan en y=163','left':'+X','right':'-X'},
         'discrepancy':'D01 y D03 se enfrentan atras; D02 y D04 se enfrentan delante. D02 y D03 no comparten coordenada longitudinal.',
         'additional_candidates':[{'mesh':'Plane_027_0','note':'Panel gris en extremo exterior de cabina, 190x281 cm; no acreditado como puerta. Revisar en fase de separacion; no sumado a las cuatro moradas.'}],
         'doors':doors}
for filename in ['puertas_f07_inventario.json','PUERTAS_SUTHERLAND_F07.json']:(OUT/filename).write_text(json.dumps(catalog,indent=2,ensure_ascii=False),encoding='utf-8')
md=['# Puertas Sutherland F07 — conciliación geométrica 4/4','',
    'Identificadas mediante material `door`, ocho islas de hojas, cuatro accesos y volumen de cabina. Unidades: cm de mundo UE.',
    'Frente +Y, izquierda del Capitán +X, derecha -X. Se conserva el inventario humano y se registra la discrepancia del emparejamiento.',
    '', '| ID | Centro XYZ | Assets de hojas | Destino | Estado |','|---|---|---|---|---|']
for d in doors:md.append('| '+d['id']+' / '+d['human_id']+' | '+str([round(v,1) for v in d['center_cm']])+' | '+', '.join(p['mesh'].split('.')[-1] for p in d['parts'])+' | '+d['destination']+' | REQUIERE SEPARACIÓN EN BLENDER |')
md+=['','## Discrepancias y límites','',catalog['discrepancy'],'',
     'Cada una de las cuatro mallas de hojas contiene dos islas distantes de lados opuestos. Ocho hojas en cuatro accesos. No hay actor animable independiente por puerta. Se preparan colisiones por isla sin separar ni modificar geometría visual.',
     'El ancho medido es la envolvente de hojas, no una certificación del vano. Los barridos con hojas desactivadas verificarán que los nuevos muros no sellan el centro del acceso.',
     'Panel gris Plane_027_0 en el extremo exterior de la cabina: candidato para revisión humana, no una quinta puerta confirmada.',
     'La pared posterior no se interpreta como puerta. No se han añadido corredores, destinos ni animaciones.',
     '', 'Ver `puertas_f07_inventario.json`, `plano_geometria_z100.png` y resultados físicos finales.']
for n in ['PUERTAS_F07_CONCILIACION_4_DE_4.md','PUERTAS_SUTHERLAND_F07.md']:(OUT/n).write_text('\n'.join(md)+'\n',encoding='utf-8')
fixed=['Plane_0','Plane_002_0','Plane_003_0','Plane_007_0','Plane_009_0','Plane_010_0','Plane_013_0','Plane_014_0','Plane_016_0',
       'Circle_001_0','Circle_002_0','Cube_000_0','Cube_001_0','Plane_005_0','Plane_004_0','Plane_015_0','Plane_011_0',
       'Plane_008_0','Editable_Mesh_Mat_004_0','Editable_Mesh_Mat_005_0','Editable_Mesh_Mat_006_0','Editable_Mesh_Mat_007_0',
       'Editable_Mesh_Mat_008_0','Editable_Mesh_Mat_009_0','Editable_Mesh_Mat_010_0','Editable_Mesh_Mat_011_0',
       'Plane_038_0','Plane_033_0','Plane_030_0','Plane_027_0','Plane_029_0','Plane_026_0','Plane_025_0','Plane_024_0','Plane_023_0','Plane_021_0','Plane_039_0']
plan=[]
for name in fixed:
    plan.append({'name':name,'strategy':'EXACT_STATIC_TRIANGLES','reason':'Arquitectura estatica, suelo/escalon o consola identificada; conservar huecos y concavidades exactos','double_sided':True})
for name in ['Plane_001_0','Plane_017_0','Plane_018_0','Plane_019_0']:
    plan.append({'name':name,'strategy':'ISLAND_BOXES','boxes':fitted_boxes(name),'reason':'Hojas cerradas: una caja ajustada por hoja/isla, separadas de muros fijos'})
plan.append({'name':'Cylinder_002_0','strategy':'CONVEX_COMPONENTS','expected_shapes':18,
             'reason':'18 bases desconectadas; convexos por componente conservando contorno cilindrico. Restaurar BlockAll; el hueco geometrico real mide 59.9-61.0 cm frente a capsula de 70 cm'})
for name in ['Mesh_589_0','Mesh_589_01','Mesh_589_02','Mesh_589_03','Mesh_589_04','Mesh_589_05']:
    plan.append({'name':name,'strategy':'REBUILD_EXISTING_COLLISION','reason':'Prueba fisica demuestra datos de colision obsoletos: regenerar sin cambiar complexity, geometria ni transform'})
for m in inv['meshes']:
    if m['name'].startswith(('Mesh_587_','Mesh_588_','Mesh_591_','Mesh_598_','Mesh_600_','Mesh_601_','Mesh_602_')):
        plan.append({'name':m['name'],'strategy':'CONVEX_COMPONENTS','reason':'Parte solida identificada de silla lateral: base, respaldo, apoyo o soporte. Convexo por componente, sin unir muebles distantes'})
(OUT/'collision_plan.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False),encoding='utf-8')
rows=[]
for m in inv['meshes']:
    name=m['name']; item=next((x for x in plan if x['name']==name),None)
    protected='COMPLEX_AS_SIMPLE' in m['complexity'] and name!='Cylinder_002_0'
    category='DECORACION_O_MECANISMO' if name.startswith('Mesh_') else 'DECORACION_ALTA'
    if protected:category='PREVIAMENTE_PROBADO'
    if item:category='PUERTAS' if name in ['Plane_001_0','Plane_017_0','Plane_018_0','Plane_019_0'] else ('BASES_CONSOLA' if name=='Cylinder_002_0' else 'ARQUITECTURA_O_CONSOLA')
    if name.startswith(('Mesh_587','Mesh_591','Mesh_588','Mesh_598','Mesh_600','Mesh_601','Mesh_602')):category='ASIENTO_PARTE_SOLIDA'
    rows.append({'mesh':name,'category':category,'before':m['complexity'],'strategy':item['strategy'] if item else 'PRESERVAR',
                 'status':'PLANIFICADO' if item else ('PRESERVADO_VALIDACION_PREVIA' if protected else ('PENDIENTE' if 'PENDIENTE' in category else 'SIN_COLISION_NUEVA'))})
with (OUT/'02_matriz_colisiones.csv').open('w',newline='',encoding='utf-8-sig') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print('Doors',len(doors),'Plan',len(plan),'protected',sum(r['category']=='PREVIAMENTE_PROBADO' for r in rows))
