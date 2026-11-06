import bpy,bmesh,json,math,hashlib,sys,shutil
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World
world=World();results=json.loads((R/'DATOS/barridos_resultados.json').read_text())['results'];assert len(results)==39 and all(r['pass_test'] for r in results)
assert all(r['certified'] for r in json.loads((R/'DATOS/apoyo_continuo.json').read_text())['results'])
archive=R/'CAPTURAS/REVISION_A1_NO_VALIDADA';archive.mkdir(exist_ok=True)
for f in (R/'CAPTURAS').glob('B*.png'):
 if int(f.stem[1:3])>11:continue # Later evidence is not part of the initial camera/path revision.
 if not (archive/f.name).exists():shutil.copy2(f,archive/f.name)
proto=json.loads((R/'DATOS/prototipo_conjunto.json').read_text());T=Vector(proto['bridge_translation'])
bpy.ops.wm.open_mainfile(filepath=str(R/'REFERENCIAS/VOY02/VOY02_Laboratorio.blend'),load_ui=False,use_scripts=False)
source=bpy.data.scenes['G_INTERIORES_CONECTADOS'];old_human_helpers=[o.name for o in source.objects if o.name.startswith('PUENTE_AL_') and any(x in o.name for x in ['_TORSO','_PELVIS','_PIERNA'])];geometry=[o for o in source.objects if o.type=='MESH' and o.get('VOY02_TIPO') in ['GEOMETRIA_EXISTENTE_COPIADA','GEOMETRIA_NUEVA_SOLO_PRUEBA'] and o.name not in old_human_helpers]
def fingerprint(o):
 h=hashlib.sha256();v=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',v);h.update(v.tobytes());h.update(np.array(o.matrix_world,dtype=np.float64).tobytes());h.update(str([(tuple(p.vertices),p.material_index) for p in o.data.polygons]).encode());return h.hexdigest()
before={o.name:fingerprint(o) for o in geometry};parents=set()
for o in geometry:
 p=o.parent
 while p:parents.add(p);p=p.parent
scenes=[]
for name in ['01_REFERENCIA_ORIGINAL','02_DIAGNOSTICO','03_EXPERIMENTO_A_SIN_CAMBIOS','04_RECORRIDOS_COMPLETOS']:
 s=bpy.data.scenes.new(name);s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
 for o in geometry+list(parents):s.collection.objects.link(o)
 s['VOY03_ESCALA_PUENTE']=1.1;s['VOY03_ORIENTACION']='OBJ +90 X heredado VOY02';s['VOY03_CAMBIOS_ARQUITECTURA']=0
 s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=2000;s.render.resolution_y=1450;s.render.resolution_percentage=100;s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new(name+'_WORLD');s.world.color=(.12,.12,.12);s.view_settings.view_transform='Standard';scenes.append(s)
bpy.context.window.scene=scenes[0]
for s in list(bpy.data.scenes):
 if s not in scenes:bpy.data.scenes.remove(s)
def mat(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=color;return m
colors=[mat('VOY03_VERDE',(.06,.85,.25,1)),mat('VOY03_AZUL',(.1,.4,1,1)),mat('VOY03_AMARILLO',(1,.75,.05,1)),mat('VOY03_ROJO',(.95,.08,.06,1))]
def line(s,name,points,material,width=.023):
 cv=bpy.data.curves.new(name,'CURVE');cv.dimensions='3D';cv.bevel_depth=width;cv.bevel_resolution=2;sp=cv.splines.new('POLY');sp.points.add(len(points)-1)
 for p,co in zip(sp.points,points):p.co=(*co,1)
 ob=bpy.data.objects.new(name,cv);s.collection.objects.link(ob);cv.materials.append(material);ob['VOY03_TIPO']='EVIDENCIA_NO_COLISION';return ob
for j,r in enumerate(x for x in results if x['height_m']==1.9):
 points=[(Vector(p)+T+Vector((0,0,.025)))[:] for p in r['foot_points']]
 if r['scope']=='required_bridge_route':line(scenes[2],r['id'],points,colors[j%3])
 if r['scope']=='full_center_network':line(scenes[3],r['id'],points,colors[j%2])
 if r['scope']=='diagnostic_stair_flight':line(scenes[1],r['id'],points,colors[2])
def capsule(s,name,p,h,material):
 vs=[];fs=[];n=32;r=.35
 # bottom hemisphere includes equator, followed by top hemisphere equator.
 for center,angles in [(r,np.linspace(-math.pi/2,0,9)),(h-r,np.linspace(0,math.pi/2,9))]:
  for angle in angles:
   for a in np.linspace(0,2*math.pi,n,endpoint=False):vs.append((r*math.cos(angle)*math.cos(a),r*math.cos(angle)*math.sin(a),center+r*math.sin(angle)))
 for k in range(17):
  for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(material);o=bpy.data.objects.new(name,me);s.collection.objects.link(o);o.location=Vector(p)+T;o['VOY03_TIPO']='CAPSULA_REFERENCIA_NO_COLISION';o['height_m']=h;o['radius_m']=r;return o
p=world.state(4.0,.05)['foot'];caps=[]
for h,m in zip([1.6,1.75,1.9],colors):
 o=capsule(scenes[1],f'CAPSULA_{h:.2f}',p,h,m);o.hide_render=h!=1.9;o.hide_viewport=h!=1.9;caps.append(o)
after={o.name:fingerprint(o) for o in geometry};assert before==after
manifest=dict(file=str(R/'ESCENAS/VOY03_Circulacion.blend'),scenes=[s.name for s in scenes],source_geometry_objects=len(geometry),source_existing_objects=sum(o.get('VOY02_TIPO')=='GEOMETRIA_EXISTENTE_COPIADA' for o in geometry),excluded_previous_diagnostic_mannequin_parts=old_human_helpers,architecture_fingerprints=before,source_to_copy_equal=before==after,translation_A_to_G=list(T),scale=1.1,geometry_changes=[],hypothesis='Option A only: original VOY02 work geometry unchanged. Paths and capsules are diagnostic helpers, not collision surfaces.',source_objects=[dict(object=o.name,source=o.get('VOY02_ORIGEN'),instance=o.get('VOY02_INSTANCE'),matrix_world=[list(v) for v in o.matrix_world],fingerprint=before[o.name]) for o in geometry])
# Camera saved with each scene for easy inspection.
def camera(s,name,at,aim,scale):
 cd=bpy.data.cameras.new(name);c=bpy.data.objects.new(name,cd);s.collection.objects.link(c);c.location=Vector(at)+T;c.rotation_euler=(Vector(aim)+T-c.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO' if scale else 'PERSP';cd.ortho_scale=scale or 10;cd.lens=32;cd.clip_start=.005;cd.clip_end=1000;s.camera=c;return c
for s in scenes:camera(s,'CAMARA_'+s.name,(24,-23,29) if s==scenes[3] else (14,-18,18),(0,8,0) if s==scenes[3] else (0,3,0),43 if s==scenes[3] else 28)
bpy.context.window.scene=scenes[3];bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=manifest['file'],compress=True);(R/'DATOS/manifest_blender.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8');print('SAVED',manifest['file'],len(geometry),flush=True)
# Cutaway is a render-only duplicate, made AFTER saving the intact laboratory.
cutscene=bpy.data.scenes.new('TEMP_CAPTURAS');cutscene.render.engine='BLENDER_WORKBENCH';cutscene.render.resolution_x=2000;cutscene.render.resolution_y=1450;cutscene.render.resolution_percentage=100;cutscene.display.shading.color_type='MATERIAL';cutscene.display.shading.show_cavity=True;cutscene.display.shading.show_shadows=True;cutscene.view_settings.view_transform='Standard';cutscene.world=scenes[0].world
copies=[]
for o in geometry:
 c=o.copy();c.data=o.data.copy();c.parent=None;c.matrix_world=o.matrix_world;cutscene.collection.objects.link(c);c.hide_render=False
 bm=bmesh.new();bm.from_mesh(c.data);bm.transform(c.matrix_world);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,2.35+T.z),plane_no=(0,0,1),clear_outer=True);bm.transform(c.matrix_world.inverted());bm.to_mesh(c.data);bm.free();copies.append(c)
helpers=[]
def shot(name,at,aim,scale=None,sceneidx=None,bridgeonly=False,capheight=None):
 for h in helpers:cutscene.collection.objects.unlink(h)
 helpers.clear()
 if sceneidx is not None:
  for o in scenes[sceneidx].objects:
   if o.get('VOY03_TIPO') in ['EVIDENCIA_NO_COLISION','CAPSULA_REFERENCIA_NO_COLISION']:
    cutscene.collection.objects.link(o);helpers.append(o);o.hide_viewport=False;o.hide_render=o.get('height_m') is not None and o.get('height_m')!=capheight
 for c,o in zip(copies,geometry):c.hide_render=bridgeonly and not str(o.get('VOY02_ORIGEN','')).startswith('OBJ:')
 if scale and at[2]>15 and abs(at[0]-aim[0])<.001 and abs(at[1]-aim[1])<.001:
  bounds=[c.matrix_world@Vector(v)-T for c in copies if not c.hide_render for v in c.bound_box];lo=np.min(np.array(bounds),axis=0);hi=np.max(np.array(bounds),axis=0);cx,cy=(lo[:2]+hi[:2])/2;at=(cx,cy,at[2]);aim=(cx,cy,0);scale=max(hi[0]-lo[0],(hi[1]-lo[1])*2000/1450)*1.10
 camera(cutscene,name,at,aim,scale);cutscene.render.filepath=str(R/'CAPTURAS'/f'{name}.png');bpy.ops.render.render(write_still=True,scene=cutscene.name);print('SHOT',name,flush=True)
shot('B01_planta_rutas_original',(0,0,22),(0,0,0),17,2,True)
shot('B02_niveles_lateral',(15,0,1.0),(0,0,.9),15,1,True)
shot('B03_escalera_derecha_apoyo',(5.9,-1.9,2.7),(4.1,.1,.5),None,1,True)
shot('B04_escalera_izquierda_apoyo',(-5.9,-1.9,2.7),(-4.1,.1,.5),None,1,True)
shot('B05_navegacion_ruta',(0,-.2,2.9),(0,-2.5,.2),None,2,True)
for h in [1.6,1.75,1.9]:shot(f'B06_capsula_{h:.2f}',(5.0,-.65,2.8),(4.0,.05,1.1),3.8,1,True,h)
shot('B07_red_completa_planta',(0,10,40),(0,10,0),40,3)
shot('B08_red_completa_axonometrica',(24,-23,29),(0,8,0),43,3)
shot('B09_union_posterior',(3.8,4.2,3.5),(1.31,7.4,1),None,3)
shot('B10_puestos_mando',(0,-3.4,3.0),(0,0,.7),None,2,True)
shot('B11_planta_original_completa',(0,0,22),(0,0,0),21,None,True)
# Do not save the render cutaway back over the intact laboratory.
