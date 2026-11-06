import bpy, json, sys, hashlib, collections, math
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
sources={
 'coleccion':R/'FUENTES/COLECCION/star-trek-voyager-collection/source/StarTrekVoyagerCollection.blend',
 'coleccion_glb':R/'FUENTES/COLECCION/star_trek_voyager_collection.glb',
 'puente_obj':R/'FUENTES/PUENTE/Voyager Bridge.obj',
 'puente_blend':R/'FUENTES/PUENTE/Voyager_Bridge_Trabajo.blend',
 'puente_max':R/'FUENTES/RECOVERY/Voyager_Bridge_MAX_Trabajo.blend',
 'puente_glb':R/'FUENTES/PUENTE/Voyager_Bridge_Trabajo.glb',
 'puente_max_desktop':R/'FUENTES/PUENTE/Voyager_Bridge_MAX_Trabajo.blend'}
def load(label):
 p=sources[label];bpy.ops.wm.read_factory_settings(use_empty=True)
 if p.suffix=='.blend':bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
 elif p.suffix=='.glb':bpy.ops.import_scene.gltf(filepath=str(p))
 else:bpy.ops.wm.obj_import(filepath=str(p),use_split_objects=True,use_split_groups=True,validate_meshes=True,forward_axis='NEGATIVE_Z',up_axis='Y')
 return p
def audit(label):
 p=load(label);rows=[];vv=[];tt=[];oid=[];mats=[];base=0
 for o in sorted(bpy.data.objects,key=lambda x:x.name):
  if o.type!='MESH':continue
  m=o.data;m.calc_loop_triangles();v=np.array([o.matrix_world@x.co for x in m.vertices],float).reshape(-1,3);t=np.array([x.vertices[:] for x in m.loop_triangles],int).reshape(-1,3)
  if not len(v):continue
  mi=[x.material_index for x in m.loop_triangles];slots=[x.name if x else None for x in m.materials]
  edges=collections.Counter(tuple(sorted((a,b))) for f in m.polygons for a,b in zip(f.vertices, list(f.vertices[1:])+[f.vertices[0]]))
  # Diagnostic weld does not modify the scene. It distinguishes OBJ/UV vertex splits from topology.
  weld=np.round(v/1e-5).astype(np.int64);_,wi=np.unique(weld,axis=0,return_inverse=True);we=collections.Counter(tuple(sorted((int(wi[a]),int(wi[b])))) for f in m.polygons for a,b in zip(f.vertices,list(f.vertices[1:])+[f.vertices[0]]) if wi[a]!=wi[b])
  centered=np.round(v-v.mean(0),5);order=np.lexsort(centered.T);finger=hashlib.sha256(centered[order].tobytes()).hexdigest()
  rows.append(dict(object=o.name,mesh=m.name,parent=o.parent.name if o.parent else None,scenes=[s.name for s in bpy.data.scenes if o.name in s.objects],collections=[c.name for c in o.users_collection],matrix_world=[list(x) for x in o.matrix_world],location=list(o.location),rotation_mode=o.rotation_mode,rotation_euler=list(o.rotation_euler),scale=list(o.scale),origin_world=list(o.matrix_world.translation),vertices=len(v),polygons=len(m.polygons),triangles=len(t),bounds_min=v.min(0).tolist(),bounds_max=v.max(0).tolist(),materials=slots,uv_layers=[x.name for x in m.uv_layers],material_triangles=dict(collections.Counter(slots[i] if i<len(slots) else 'NONE' for i in mi)),boundary_edges=sum(n==1 for n in edges.values()),nonmanifold_edges=sum(n!=2 for n in edges.values()),weld_10um_boundary=sum(n==1 for n in we.values()),weld_10um_nonmanifold=sum(n!=2 for n in we.values()),fingerprint_translation_only=finger,modifiers=[dict(name=x.name,type=x.type) for x in o.modifiers],animation=bool(o.animation_data)))
  vv.append(v);tt.append(t+base);oid.extend([len(rows)-1]*len(t));mats.extend(mi);base+=len(v)
 np.savez_compressed(R/'DATOS'/f'{label}_geometria.npz',vertices=np.vstack(vv),triangles=np.vstack(tt),object_ids=np.array(oid),material_ids=np.array(mats))
 metadata=dict(label=label,path=str(p),blender=bpy.app.version_string,unit_system=bpy.context.scene.unit_settings.system,scale_length=bpy.context.scene.unit_settings.scale_length,scenes=[s.name for s in bpy.data.scenes],objects=rows,images=[dict(name=x.name,path=x.filepath,packed=bool(x.packed_file),size=list(x.size)) for x in bpy.data.images])
 (R/'DATOS'/f'{label}_auditoria.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding='utf8');print('AUDIT',label,len(rows),flush=True)
 if label=='puente_obj':bpy.ops.wm.save_as_mainfile(filepath=str(R/'ESCENAS/VOY05A_Puente_Original_Inspeccion.blend'),compress=True)
 if label=='coleccion':bpy.ops.wm.save_as_mainfile(filepath=str(R/'ESCENAS/VOY05A_Coleccion_Original_Inspeccion.blend'),compress=True)
def camera(scene,center,direction,span,aspect):
 c=bpy.data.cameras.new('VOY05A_CAM');o=bpy.data.objects.new('VOY05A_CAM',c);scene.collection.objects.link(o);o.location=Vector(center)+Vector(direction).normalized()*span*3;o.rotation_euler=(Vector(center)-o.location).to_track_quat('-Z','Y').to_euler();c.type='ORTHO';c.ortho_scale=span;c.clip_start=.001;c.clip_end=2000;scene.camera=o
 return o
def setup(scene):
 if not scene.world:scene.world=bpy.data.worlds.new('VOY05A_WORLD')
 scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=640;scene.render.resolution_y=520;scene.render.resolution_percentage=100
 scene.display.shading.light='STUDIO';scene.display.shading.studiolight_rotate_z=.4;scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True;scene.display.shading.cavity_type='BOTH';scene.display.shading.show_specular_highlight=True;scene.display.shading.background_type='WORLD';scene.world.color=(.07,.07,.07);scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard'
def catalog():
 load('coleccion');scene=bpy.context.scene;setup(scene);obs=[o for o in scene.objects if o.type=='MESH']
 for o in obs:o.hide_render=True
 for o in sorted(obs,key=lambda x:x.name):
  o.hide_render=False;v=np.array([o.matrix_world@x.co for x in o.data.vertices]);lo=v.min(0);hi=v.max(0);center=(lo+hi)/2;span=float(max(hi-lo)*1.5)
  for suffix,dr in [('ISO',(1,-1,.85)),('TOP',(0,0,1)),('BACK',(-1,1,.7)),('FRONT',(-1,-1,.35))]:
   cam=camera(scene,center,dr,span,640/520);scene.render.filepath=str(R/'CAPTURAS'/f'CAT_{o.name}_{suffix}.png');bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True)
  # Section is generated in a disposable mesh; original object data remain untouched.
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data);bm.transform(o.matrix_world)
  cut=float(lo[2]+min(1.8,(hi[2]-lo[2])*.62));bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00001,plane_co=(0,0,cut),plane_no=(0,0,1),clear_outer=True,clear_inner=False)
  m=bpy.data.meshes.new('TEMP_SECTION');bm.to_mesh(m);bm.free();tmp=bpy.data.objects.new('TEMP_SECTION',m);scene.collection.objects.link(tmp)
  for mat in o.data.materials:m.materials.append(mat)
  o.hide_render=True;cam=camera(scene,center,(0,0,1),span,640/520);scene.render.filepath=str(R/'CAPTURAS'/f'CAT_{o.name}_CUT.png');bpy.ops.render.render(write_still=True);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.objects.remove(tmp,do_unlink=True);bpy.data.meshes.remove(m)
  print('CATALOG',o.name,flush=True)
args=sys.argv[sys.argv.index('--')+1:]
if args==['catalogo']:catalog()
else:
 for label in args:audit(label)
