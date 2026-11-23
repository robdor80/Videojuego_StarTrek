import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[1];P=R/'DATOS'
proto=json.loads((P/'prototipo_conjunto.json').read_text());cases=json.loads((P/'ensamblajes_pruebas.json').read_text());interfaces={p['name']:p for p in json.loads((P/'interfaces_modulos.json').read_text())};functional=json.loads((P/'preparacion_funcional.json').read_text());meta=json.loads((P/'obj_objetos.json').read_text());by={o['name']:o for o in meta};transits=json.loads((P/'transitos_puente.json').read_text());manifest=[]
if (P/'puestos_revision.json').exists():
 revised_groups={x['id']:x['refined_parts'] for x in json.loads((P/'puestos_revision.json').read_text())['stations']}
 for ch in functional['chairs']:
  ch['parts']=revised_groups[ch['id']];ch['note']='Revised semantic group only; old motion results do not validate this revised assembly.'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
with bpy.data.libraries.load(str(R/'FUENTES/OBJ/puente_base_importado.blend'),link=False) as (src,dst):dst.objects=list(src.objects)
objtemplates={o.name:o for o in dst.objects if o and o.type=='MESH'}
# Preserve the import basis in shared laboratory mesh coordinates before clone_obj
# resets object matrices. Source cache is loaded in memory only and never saved.
for template in objtemplates.values():
 template.data.transform(template.matrix_world);template.data.update();template.matrix_world=Matrix.Identity(4)
oldset=set(bpy.data.objects)
with bpy.data.libraries.load(str(R/'FUENTES/COLECCION/coleccion_original.blend'),link=False) as (src,dst):dst.objects=[n for n in src.objects if n.startswith('Mesh')]
native={o.name:o for o in dst.objects if o and o.type=='MESH'}
native_world={o['name']:Matrix(o['world_matrix']) for o in json.loads((R.parent/'Voyager_Puente_2026-10-21/DATOS/blender_blend.json').read_text())['objects'] if o['type']=='MESH'}
palette=[(.25,.45,.75,1),(.25,.65,.55,1),(.6,.45,.75,1),(.65,.65,.3,1),(.4,.7,.8,1),(.8,.4,.4,1)]
def mat(name,color):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.diffuse_color=color;return m
orange=mat('LAB_ADAPTADOR_NUEVO',(.95,.42,.08,1));green=mat('LAB_MOBILIARIO_REFERENCIA',(.28,.65,.34,1));humanm=mat('LAB_REFERENCIA_HUMANA',(.15,.45,.85,1));whitem=mat('LAB_TEXTO',(.95,.95,.95,1));red=mat('LAB_INCIDENCIA',(.8,.12,.10,1))
def scene(name):
 s=bpy.data.scenes.new(name);s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.world=bpy.data.worlds.new(name+'_World');s.world.color=(.05,.05,.05);s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1700;s.render.resolution_y=1150;s.render.resolution_percentage=100;s.display.shading.light='STUDIO';s.display.shading.studio_light='paint.sl';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.view_settings.view_transform='Standard';s.render.image_settings.file_format='PNG';s['VOY02_ESTADO']='LABORATORIO_EXPERIMENTAL_NO_PRODUCCION';return s
def coll(s,name):c=bpy.data.collections.new(s.name+'__'+name);s.collection.children.link(c);return c
def empty(c,name,at=(0,0,0),kind='ROOT'):
 o=bpy.data.objects.new(name,None);o.location=at;o.empty_display_type='ARROWS';o.empty_display_size=.25;o['VOY02_TIPO']=kind;c.objects.link(o);return o
def text(c,name,body,p,size=.22):
 cv=bpy.data.curves.new(name,'FONT');cv.body=body;cv.size=size;cv.align_x='CENTER';o=bpy.data.objects.new(name,cv);c.objects.link(o);o.location=p;o.data.materials.append(whitem);o['VOY02_TIPO']='ROTULO_DIAGNOSTICO';return o
def mesh(c,name,vertices,faces,material=orange):
 me=bpy.data.meshes.new(name);me.from_pydata(vertices,[],faces);me.update();o=bpy.data.objects.new(name,me);c.objects.link(o);me.materials.append(material);o['VOY02_TIPO']='GEOMETRIA_NUEVA_SOLO_PRUEBA';return o
def triangles(c,name,tri,material=orange):
 vs=[p for t in tri for p in t];fs=[(i,i+1,i+2) for i in range(0,len(vs),3)];return mesh(c,name,vs,fs,material)
def cube(c,name,center,size,material=green):
 x,y,z=[v/2 for v in size];vs=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)];fs=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];o=mesh(c,name,vs,fs,material);o.location=center;return o
def capsule(c,name,foot,height,radius=.35,wire=True):
 rings=[]
 for theta in [-math.pi/2,-math.pi/3,-math.pi/6,0]:rings.append((radius+radius*math.sin(theta),max(.0001,radius*math.cos(theta))))
 for theta in [0,math.pi/6,math.pi/3,math.pi/2]:rings.append((height-radius+radius*math.sin(theta),max(.0001,radius*math.cos(theta))))
 vs=[(rr*math.cos(2*math.pi*j/20),rr*math.sin(2*math.pi*j/20),zz) for zz,rr in rings for j in range(20)];fs=[]
 for i in range(len(rings)-1):
  for j in range(20):a=i*20+j;b=i*20+(j+1)%20;fs.append((a,b,b+20,a+20))
 o=mesh(c,name,vs,fs,humanm);o.location=foot;o['VOY02_TIPO']='CAPSULA_HIPOTESIS';o['height_m']=height;o['radius_m']=radius
 if wire:o.display_type='WIRE';o.hide_render=True
 return o
def human(c,name,foot,height):
 # Simple silhouette kept within the .70m diameter capsule. No production anatomy or rig.
 x,y,z=foot;cap=capsule(c,name+'_CAPSULA',foot,height);cube(c,name+'_TORSO',(x,y,z+height*.64),(.40,.23,height*.28),humanm);cube(c,name+'_PELVIS',(x,y,z+height*.44),(.30,.20,height*.13),humanm)
 for dx in [-.10,.10]:cube(c,name+'_PIERNA'+str(dx),(x+dx,y,z+height*.22),(.12,.13,height*.42),humanm)
 # UV sphere via direct latitudes; overall reference reaches exactly declared H.
 rr=.115;zz=z+height-rr;vs=[];fs=[]
 for i in range(9):
  ph=-math.pi/2+math.pi*i/8
  for j in range(16):a=2*math.pi*j/16;vs.append((x+rr*math.cos(ph)*math.cos(a),y+rr*math.cos(ph)*math.sin(a),zz+rr*math.sin(ph)))
 for i in range(8):
  for j in range(16):a=i*16+j;b=i*16+(j+1)%16;fs.append((a,b,b+16,a+16))
 o=mesh(c,name+'_CABEZA',vs,fs,humanm);o['VOY02_TIPO']='REFERENCIA_HUMANA';text(c,name+'_H',f'{height:.2f} m',(x,y,z+height+.12),.19);return cap
def clone_obj(template,c,name,matrix,source,case=None):
 o=template.copy();o.data=template.data;o.animation_data_clear();o.parent=None;o.matrix_world=matrix;o.name=name;c.objects.link(o);o.hide_render=False;o.hide_viewport=False;o['VOY02_TIPO']='GEOMETRIA_EXISTENTE_COPIADA';o['VOY02_ORIGEN']=source
 if case:o['VOY02_CASO']=case
 return o
def bridge(s,scale=1.,translation=(0,0,0),doors_open=False):
 groups={x:coll(s,x) for x in ['ARQUITECTURA','SUELOS_ESCALONES','CONSOLAS','PANTALLAS','SILLAS','PUERTAS','TECHO_LUCES']};instances={};chairparts={n:ch['id'] for ch in functional['chairs'] for n in ch['parts']};screenparts={p['object'] for p in functional['screens']};doorparts={n:d['id'] for d in proto['bridge_door_openings'] for n in d['leafA']+d['leafB']}
 root=empty(s.collection,s.name+'_PUENTE_ROOT',translation);root.scale=(scale,)*3;root['VOY02_ESCALA']=scale
 for name,template in objtemplates.items():
  row=by[name];mats=' '.join(row['materials']).lower()
  category='SILLAS' if name in chairparts else 'PUERTAS' if name in doorparts else 'PANTALLAS' if name in screenparts else 'SUELOS_ESCALONES' if 'voygray'in mats or name in ['Mesh_1856','Mesh_1787'] else 'TECHO_LUCES' if name in ['Mainroof_1','centerlight_1','centerlights_2','blackinset_1','centerinset_1','lightssupport_1','lightsring_3','strudextends_1','Centerpiece_1'] or row['bounds_min'][2]>2.65 else 'CONSOLAS' if 'dimgray'in mats else 'ARQUITECTURA'
  ob=clone_obj(template,groups[category],s.name+'__'+name,Matrix.Identity(4),'OBJ:'+name);ob.parent=root;ob.matrix_parent_inverse=Matrix.Identity(4)
  if doors_open:
   for d in proto['bridge_door_openings']:
    if name in d['leafA']:ob.location=Vector(d['leafA_vector'])
    if name in d['leafB']:ob.location=Vector(d['leafB_vector'])
  instances[name]=ob
 return root,instances,groups
def module(c,p,extra=(0,0,0),case=None,color_index=0):
 src=p['source'];yaw=p['yaw'];M=Matrix.Translation(Vector(p['translation'])+Vector(extra))@Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(Vector(p['original_to_canonical']))@native_world[src];o=clone_obj(native[src],c,p['id'],M,'COLECCION:'+src,case)
 # Object display material is explicitly diagnostic; native materials remain available in source copy.
 o.data=o.data.copy();o.data.materials.clear();o.data.materials.append(mat('LAB_MODULO_'+p['id'],palette[color_index%len(palette)]))
 for poly in o.data.polygons:poly.material_index=0
 o['VOY02_MATERIAL']='COLOR_DIAGNOSTICO_NO_ARTISTICO'
 o['VOY02_INSTANCE']=p['id']
 for pp in interfaces[src]['ports']:
  if pp['open_candidate']:
   wp=Matrix.Translation(Vector(p['translation'])+Vector(extra))@Matrix.Rotation(yaw,4,'Z')@Vector(pp['point']);an=empty(c,p['id']+'_ANCLA_'+pp['code'],wp,'ANCLA_MEDIDA');an['VOY02_NORMAL_LOCAL']=pp['normal']
 return o
# A — original and proposed working scale, shared source mesh datablocks.
A=scene('A_ESCALA_HUMANA_110');_,ab,ag=bridge(A,1.1);refs=coll(A,'REFERENCIAS_HUMANAS')
nodes=transits['nodes'];placements_h=[]
for h,target in [(1.6,[-1.6,-4.3]),(1.75,[0,-.75]),(1.9,[3.6,2.7])]:
 p=min(nodes,key=lambda p:(p[0]-target[0])**2+(p[1]-target[1])**2);wp=[x*1.1 for x in p];human(refs,'H_'+str(h),wp,h);placements_h.append({'height_m':h,'foot':wp,'scale_bridge':1.1})
text(refs,'AVISO_ESCALA','ESCALA DE TRABAJO 1.10 - NO DEFINITIVA',(0,-7.0,.02),.30)
for name,p0,p1,label in [('ANCHO',(-7.23,-6.85,.01),(7.23,-6.85,.01),'Envolvente X = 14.465 m'),('ALTO',(-7.8,-7.,.01),(-7.8,7.,.01),'Y = 14.312 m')]:
 text(refs,name,label,((p0[0]+p1[0])/2,(p0[1]+p1[1])/2,.02),.25)
A0=scene('A_COMPARACION_ESCALAS');ac=coll(A0,'FRAGMENTOS_MEDIDOS');d=next(x for x in proto['bridge_door_openings'] if x['id']=='D_DER');center=Vector(d['center']);candidate=['Mesh_1841','Object_82']+d['leafA']+d['leafB']
for k,sc in enumerate([1.0,1.1,1.15,1.50813535]):
 offset=Vector((k*4.0,0,0));root=empty(ac,'ESCALA_'+str(sc),offset);root.scale=(sc,)*3
 for name in candidate:
  if name not in objtemplates:continue
  o=clone_obj(objtemplates[name],ac,'COMPARA_'+str(k)+'_'+name,Matrix.Identity(4),'OBJ:'+name);o.parent=root;o.location=-center
  if name in d['leafA']:o.location+=Vector(d['leafA_vector'])
  if name in d['leafB']:o.location+=Vector(d['leafB_vector'])
 human(ac,'H190_'+str(k),offset+Vector((0,-.25,0)),1.90);text(ac,'SCALE_LABEL_'+str(k),f'OBJ x {sc:.4f}',offset+Vector((0,-1.2,.01)),.24)
# B — every requested raw joint, without silently repairing source trim.
B=scene('B_PASILLOS_UNIONES');bc=coll(B,'MODULOS_ALINEADOS');case_offsets={}
for k,case in enumerate(cases):
 extra=Vector(((k%2)*19,(k//2)*12,0));case_offsets[case['id']]=list(extra)
 for j,p in enumerate(case['placements']):module(bc,p,extra,case['id'],j)
 text(bc,'LABEL_'+case['id'],case['id'],extra+Vector((0,-3,.01)),.3)
 for q in case['routes'][2]['points'][::max(1,len(case['routes'][2]['points'])//3)]:capsule(bc,case['id']+'_CAPS',Vector(q)+extra,1.9)
 human(bc,'PERSONA_'+case['id'],Vector(case['routes'][2]['points'][-1])+extra,1.9)
# G — full experimental connected network.
G=scene('G_INTERIORES_CONECTADOS');gr,gb,gg=bridge(G,proto['scale_bridge'],proto['bridge_translation'],True);gc=coll(G,'MODULOS_EXISTENTES');ga=coll(G,'ADAPTADORES_NUEVOS');gf=coll(G,'MOBILIARIO_SOLO_REFERENCIA');gh=coll(G,'HUMANOS_Y_RECORRIDOS')
for k,p in enumerate(proto['placements']):module(gc,p,color_index=k)
for a in proto['adapters']:o=triangles(ga,a['id'],a['triangles']);o['VOY02_ORIGEN']='NUEVO_ADAPTADOR_NO_FINAL'
for p in proto['furniture_reference_only']:cube(gf,p['id'],p['center'],p['size'])
for k,test in enumerate(proto['routes']):
 route=test['routes'][2]['points'];positions=[route[0],route[len(route)//2],route[-1]]
 for j,p in enumerate(positions):human(gh,test['id']+'_'+str(j),p,1.90)
text(gh,'AVISO_G','PROTOTIPO EXPERIMENTAL - ADAPTADORES NARANJA - MOBILIARIO VERDE',(-1,-15,.02),.35)
# C and D share geometry datablocks but independent objects; no duplicate source meshes.
C=scene('C_UNION_PUENTE_PASILLO');cr,cb,cg=bridge(C,proto['scale_bridge'],proto['bridge_translation'],True);cc=coll(C,'PRIMERA_CONEXION')
for p in proto['placements'][:2]:module(cc,p,color_index=0)
for a in proto['adapters'][:2]:triangles(cc,a['id'],a['triangles'])
human(cc,'PERSONA_ACCESO',[0,.8,.002],1.9)
D=scene('D_CAMAROTE_ENSAYO');dc=coll(D,'ENVOLVENTE_EXISTENTE');df=coll(D,'MOBILIARIO_REFERENCIA');da=coll(D,'ADAPTACION_PASILLO');dh=coll(D,'PERSONAS')
room=next(p for p in proto['placements'] if p['id']=='CAMAROTE_EXISTENTE');offset=-Vector(room['translation']);module(dc,room,offset,color_index=2)
for p in proto['furniture_reference_only']:cube(df,p['id'],Vector(p['center'])+offset,p['size'])
for a in proto['adapters']:
 if a['id']=='AD_CAMAROTE':triangles(da,a['id'],[[list(Vector(v)+offset) for v in tri] for tri in a['triangles']])
for p in proto['placements']:
 if p['id']=='PASILLO_CAMAROTE':module(da,p,offset,color_index=1)
human(dh,'PERSONA_CAMAROTE',[0,0,.002],1.9);human(dh,'PERSONA_CAMA',[.7,1.5,.002],1.75);text(dh,'LABEL_D','ENVOLVENTE EXISTENTE / VOLUMENES VERDES NUEVOS',(-.5,-5,.02),.25)
# E — actual complete door assemblies, movable roots with measurable trial pivots.
E=scene('E_PUERTAS_CARRERA_PRUEBA');ec=coll(E,'MECANISMOS_NO_VALIDADOS');E.frame_start=1;E.frame_end=97
for k,d in enumerate(proto['bridge_door_openings']):
 cen=Vector(d['center']);off=Vector((k*5,0,0));near=[]
 for row in meta:
  lo=Vector(row['bounds_min']);hi=Vector(row['bounds_max']);c=(lo+hi)/2
  if (c-cen).length<1.5 and row['name']not in d['leafA']+d['leafB']:near.append(row['name'])
 for name in near:clone_obj(objtemplates[name],ec,f'{d["id"]}_FIJO_{name}',Matrix.Translation(off-cen*1.1)@Matrix.Scale(1.1,4),'OBJ:'+name)
 for side,parts,vec in [('A',d['leafA'],d['leafA_vector']),('B',d['leafB'],d['leafB_vector'])]:
  root=empty(ec,d['id']+'_HOJA_'+side,off);root['VOY02_CARRERA_M']=d['stroke_obj_units']*1.1
  for name in parts:
   o=clone_obj(objtemplates[name],ec,d['id']+'_MOVIL_'+name,Matrix.Identity(4),'OBJ:'+name);o.parent=root;o.scale=(1.1,)*3;o.location=-cen*1.1
  root.location=off;root.keyframe_insert(data_path='location',frame=1);root.location=off+Vector(vec)*1.1;root.keyframe_insert(data_path='location',frame=49);root.location=off;root.keyframe_insert(data_path='location',frame=97)
 text(ec,'DOOR_LABEL_'+d['id'],d['id']+' - CONTACTOS EN POSICIONES INTERMEDIAS',off+Vector((0,-1.5,0)),.22)
E.frame_set(49)
Es=scene('E_SILLAS_GRUPOS');sc=coll(Es,'GRUPOS_PROPUESTOS')
for k,ch in enumerate(functional['chairs']):
 center=Vector(ch['pivot_candidate']);target=Vector(((k%3)*3.2,(k//3)*3.2,0));root=empty(sc,ch['id']+'_PIVOTE_PRUEBA',target)
 for name in ch['parts']:
  o=clone_obj(objtemplates[name],sc,ch['id']+'_'+name,Matrix.Identity(4),'OBJ:'+name);o.parent=root;o.location=-center;o.location.z-=min(by[n]['bounds_min'][2] for n in ch['parts'])-center.z
 text(sc,'LABEL_'+ch['id'],ch['id']+' / GRADO C',target+Vector((0,-1.0,0)),.22)
# Set viewport and pack source images without changing pixels or shader values.
textures={p.name.lower():p for p in (R/'FUENTES/OBJ/VOYBRIDGETEX-1/Textures').glob('*') if p.is_file()}
packed=0
for im in bpy.data.images:
 if im.source!='FILE':continue
 name=Path(im.filepath.replace('\\','/')).name.lower();candidate=textures.get(name)
 if candidate:
  im.filepath=str(candidate)
  if not im.packed_file:im.pack()
  packed+=1
for s in [A,A0,B,C,D,E,Es,G]:
 s['VOY02_CAPSULA_RADIO_M']=.35;s['VOY02_NO_UE5_VALIDADO']=True
 for area in s.collection.all_objects:
  pass
manifest={'main_file':str(R/'ESCENAS/VOY02_Laboratorio.blend'),'scenes':[s.name for s in [A,A0,B,C,D,E,Es,G]],'case_offsets':case_offsets,'human_references':placements_h,'packed_images':packed,'source_geometry_shared_datablocks':True,'prototype_scale':1.1,'warning':'Scenes are technical laboratory only; door intermediate collisions remain and central bridge circulation not demonstrated.'}
(P/'escenas_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
if bpy.context.window:bpy.context.window.scene=G
for unused_scene in list(bpy.data.scenes):
 if unused_scene.name=='Scene' and not unused_scene.objects:bpy.data.scenes.remove(unused_scene)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'ESCENAS/VOY02_Laboratorio.blend'))
print('LAB_SAVED',manifest['scenes'],'PACKED',packed,flush=True)
