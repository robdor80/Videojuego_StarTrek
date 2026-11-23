import bpy,bmesh,json,math,sys,os
from pathlib import Path
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'ESCENAS/VOY02_Laboratorio.blend'),load_ui=False,use_scripts=False)
only={x.strip() for x in os.environ.get('VOY02_ONLY','').split(',') if x.strip()}
manifest=[m for m in json.loads((R/'DATOS/capturas_manifest.json').read_text()) if m['file'][:-4] not in only] if only else []
def active(name):
 s=bpy.data.scenes[name]
 if bpy.context.window:bpy.context.window.scene=s
 s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1700;s.render.resolution_y=1150;s.render.resolution_percentage=100;s.display.shading.color_type='MATERIAL';s.display.shading.light='STUDIO';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.view_settings.view_transform='Standard'
 return s
def cut(s,z,axis=2,side=1):
 for o in list(s.objects):
  if o.type!='MESH' or o.hide_render:continue
  if o.get('VOY02_TIPO') not in ['GEOMETRIA_EXISTENTE_COPIADA','GEOMETRIA_NUEVA_SOLO_PRUEBA']:continue
  # Reference silhouettes and furniture are never geometry sources for architectural sections.
  if any(k in o.name for k in ['TORSO','PIERNA','PELVIS','CABEZA','REF_CAMA','REF_ESCRITORIO','REF_ARMARIO']):continue
  o.data=o.data.copy();bm=bmesh.new();bm.from_mesh(o.data);bm.transform(o.matrix_world);normal=Vector((0,0,0));normal[axis]=side;point=Vector((0,0,0));point[axis]=z
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=point,plane_no=normal,clear_outer=True,clear_inner=False);bm.transform(o.matrix_world.inverted());bm.to_mesh(o.data);bm.free();o.data.update()
 s.view_layers[0].update()
def shot(s,name,title,direction=(1,-1,.8),subset=None,position=None,target=None,orthoscale=None,note=''):
 if only and name not in only:return
 if bpy.context.window:bpy.context.window.scene=s
 old_resolution=(s.render.resolution_x,s.render.resolution_y)
 if name=='G02_conjunto_planta':s.render.resolution_x=1300;s.render.resolution_y=2000
 if name=='D02_planta_camarote':s.render.resolution_x=1300;s.render.resolution_y=1600
 hidden=[]
 if subset is not None:
  for o in s.objects:
   if o.type in {'MESH','FONT'} and not o.hide_render and not subset(o):hidden.append(o);o.hide_render=True
 s.view_layers[0].update();obs=[o for o in s.objects if o.type=='MESH' and not o.hide_render and len(o.data.vertices)]
 if not obs:print('EMPTY_SHOT',name,flush=True);return
 pts=[o.matrix_world@Vector(p) for o in obs for p in o.bound_box]
 if name=='E04_sillas_grupos':pts += [o.matrix_world@Vector(p) for o in s.objects if o.type=='FONT' and not o.hide_render for p in o.bound_box]
 lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);center=(lo+hi)/2;radius=max((p-center).length for p in pts)
 camdata=bpy.data.cameras.new(name+'_Camera');cam=bpy.data.objects.new(name+'_Camera',camdata);s.collection.objects.link(cam);s.camera=cam
 cam.location=Vector(position) if position is not None else center+Vector(direction).normalized()*radius*3;aim=Vector(target) if target is not None else center;cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='PERSP' if position is not None and orthoscale is None else 'ORTHO';camdata.sensor_fit='HORIZONTAL';camdata.lens=24;camdata.clip_start=.01;camdata.clip_end=10000
 frame_bounds=None
 if camdata.type=='ORTHO':
  # Project actual object bounds onto camera right/up; explicitly fit horizontal sensor.
  q=cam.rotation_euler.to_quaternion().inverted();pp=[q@(p-center) for p in pts]
  left,right=min(p.x for p in pp),max(p.x for p in pp);bottom,top=min(p.y for p in pp),max(p.y for p in pp)
  shift=cam.rotation_euler.to_quaternion()@Vector(((left+right)/2,(bottom+top)/2,0));cam.location+=shift;aim+=shift
  aspect=s.render.resolution_x/s.render.resolution_y
  camdata.ortho_scale=orthoscale or max(right-left,(top-bottom)*aspect)*1.12
  s.view_layers[0].update();ndc=[world_to_camera_view(s,cam,p) for p in pts]
  frame_bounds={'xmin':min(p.x for p in ndc),'xmax':max(p.x for p in ndc),'ymin':min(p.y for p in ndc),'ymax':max(p.y for p in ndc)}
  assert min(frame_bounds.values())>=0 and max(frame_bounds.values())<=1,(name,frame_bounds)
 s.render.filepath=str(R/'CAPTURAS'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=s.name)
 manifest.append({'file':name+'.png','scene':s.name,'title':title,'note':note,'camera':list(cam.location),'target':list(aim),'ortho_scale':camdata.ortho_scale if camdata.type=='ORTHO' else None,'engine':'Workbench / material diffuse','source_scene_preserved_full':True,'projected_mesh_bounds':frame_bounds,'temporarily_hidden_neighbors':len(hidden),'visible_meshes':len(obs)})
 for o in hidden:o.hide_render=False
 s.render.resolution_x,s.render.resolution_y=old_resolution
 print('SHOT',name,flush=True)
A=active('A_ESCALA_HUMANA_110');shot(A,'A01_puente_completo','Puente completo; escala experimental 1.10')
cut(A,3.0);shot(A,'A02_puente_humanos','Referencias 1.60 / 1.75 / 1.90 m; arquitectura a 1.10',note='Corte horizontal Z=3.00 m solo para captura; no se guarda sobre el laboratorio.')
shot(A,'A03_planta_acotada','Planta de puente: envolvente 14.465 x 14.312 m',(0,0,1),note='Corte Z=3.00 m; envolvente exterior, no anchura útil de pasos.')
cut(A,0,axis=1,side=-1);shot(A,'A04_seccion_alturas','Alturas de personas y niveles del puente',(0,-1,.02),note='Sección adicional Y=0; referencias humanas completas conservadas.')
A0=active('A_COMPARACION_ESCALAS');shot(A0,'A05_escalas_comparadas','Mismo acceso y referencia de 1.90 m: escalas 1.00 / 1.10 / 1.15 / 1.508',(0,-1,.15),note='Fragmentos de acceso reales; no demuestra ergonomía del puente completo.')
B=active('B_PASILLOS_UNIONES');shot(B,'B00_catalogo_ensayos','Siete ensamblajes reales, alineados por anclas de extremos',(0,0,1))
cut(B,2.3)
cases=json.loads((R/'DATOS/ensamblajes_pruebas.json').read_text())
for case in cases:
 cid=case['id'];pred=lambda o,cid=cid:o.get('VOY02_CASO')==cid or o.name.startswith('PERSONA_'+cid)
 shot(B,cid+'_planta',cid+': unión geométrica y referencia humana',(0,0,1),subset=pred,note='Corte Z=2.30 m. Color por módulo; no se reparan molduras en esta prueba.')
 shot(B,cid+'_perspectiva',cid+': perfiles existentes y continuidad de suelo',(1,-1,.8),subset=pred,note='Corte Z=2.30 m. Medidas y discrepancias registradas en ensamblajes_pruebas.json.')
C=active('C_UNION_PUENTE_PASILLO');cut(C,2.3);shot(C,'C01_puente_pasillo','Puente → adaptador experimental → pasillo → cruce',(1,-1,1),note='Corte Z=2.30 m; puertas en pose abierta estática, sin mecanismo certificado.')
rear=next(d for d in json.loads((R/'DATOS/prototipo_conjunto.json').read_text())['bridge_door_openings'] if d['id']=='D_POST')
rear_names={'OBJ:'+n for n in rear['leafA']+rear['leafB']+['Mesh_1832','Mesh_1833','hallwayfloor_1']}
shot(C,'C02_detalle_adaptador','Acceso posterior: adaptador naranja construido solo para laboratorio',(1,-1,1),subset=lambda o:o.name.split('.')[0]=='AD_PUENTE' or o.get('VOY02_INSTANCE')=='PASILLO_PRINCIPAL' or o.get('VOY02_ORIGEN') in rear_names,note='Contexto posterior aislado solo para captura. Paredes/techo del adaptador retranqueados 0.14m; carrera de puertas sin certificar.')
D=active('D_CAMAROTE_ENSAYO');shot(D,'D01_interior_camarote','Habitación existente con cama, escritorio y armario de referencia',position=(-2.5,-2.8,1.65),target=(.4,1.5,.9),note='Envolvente completa; volúmenes verdes nuevos, sin diseño artístico final.')
cut(D,2.30);shot(D,'D02_planta_camarote','Maqueta de camarote y conexión al pasillo',(0,0,1),note='Envolvente Group4 / Mesh4, corte Z=2.30 m; mobiliario verde solo para comprobar espacio.')
shot(D,'D03_camarote_perspectiva','Volumen caminable, entrada y mobiliario de prueba',(1,-1,1),note='Corte Z=2.30 m. Los objetos no son muebles definitivos.')
E=active('E_PUERTAS_CARRERA_PRUEBA')
for frame,name in [(1,'E01_puertas_cerradas'),(25,'E02_puertas_intermedias'),(49,'E03_puertas_abiertas')]:
 E.frame_set(frame);E.view_layers[0].update();shot(E,name,'Tres puertas: '+str(frame)+' / ensayo geométrico',(1,-1,.65),note='Las poses intermedias tienen nuevos contactos detectados; apertura final no certifica bolsillos ni mecanismo.')
Es=active('E_SILLAS_GRUPOS');shot(Es,'E04_sillas_grupos','Cinco agrupaciones revisadas: 8 / 31 / 31 / 11 / 11 piezas',(1,-1,.9),note='Grupos semánticos corregidos; los giros históricos corresponden a agrupaciones anteriores. Articulación y sentado sin validar.')
G=active('G_INTERIORES_CONECTADOS');shot(G,'G01_conjunto_completo','Conjunto experimental completo, sin cortes',(1,-1,1))
cut(G,2.30);shot(G,'G02_conjunto_planta','Puente + pasillos + turbolift + camarote',(0,0,1),note='Corte Z=2.30 m; rojo/naranja: adaptadores de prueba. No valida el tránsito de todo el puente.')
shot(G,'G03_conjunto_perspectiva','Conexiones de laboratorio verificadas en recorridos seleccionados',(1,-1,1),note='Corte Z=2.30 m. Se conservan los problemas del modelo y se documentan las zonas no demostradas.')
shot(G,'G04_cruce_y_turbolift','Cruce y transición a cabina de turbolift',(1,-1,1),subset=lambda o:o.name in ['CRUCE_CUATRO','ACCESO_TURBO','CABINA_TURBO','AD_RAMAL_TURBO','AD_GARGANTA_TURBO'],note='Ramal aislado, corte Z=2.30 m. Solo cabina y acceso estáticos; no implementa ascensor.')
(R/'DATOS/capturas_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
print('CAPTURAS_COMPLETADAS',len(manifest),flush=True)
