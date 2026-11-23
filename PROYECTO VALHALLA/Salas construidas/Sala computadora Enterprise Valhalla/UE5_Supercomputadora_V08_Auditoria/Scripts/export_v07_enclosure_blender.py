"""Portable Blender work model from the exact authored UE scene, preserving materials."""
import argparse,json,sys,math
from pathlib import Path
import bpy
from mathutils import Matrix,Quaternion,Vector
p=argparse.ArgumentParser()
for n in ('geometry','doors','source-blend','output','report'):p.add_argument('--'+n,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);target=Path(a.output).resolve();assert not target.exists()
d=json.loads(Path(a.geometry).read_text());doors=json.loads(Path(a.doors).read_text());by_actor={r['actor']:r for r in doors}
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(Path(a.source_blend).resolve()),link=False) as (src,dst):dst.materials=sorted(src.materials)
originals=dst.materials;mats={};meshes={};groups={};animated=[];counts={}
def material(path):
 if path not in mats:
  name=path.rsplit('/',1)[-1].split('.')[0]
  if name.startswith('M_') and name[2:].isdigit():mats[path]=originals[int(name[2:])]
  elif path=='/Engine/EngineMaterials/WorldGridMaterial.WorldGridMaterial':
   mats[path]=bpy.data.materials.new('UE_Engine_WorldGrid_unused_base');mats[path].diffuse_color=(.5,.5,.5,1)
  else:raise AssertionError(path)
 return mats[path]
for key,part in d['meshes'].items():
 if not part['triangles']:continue
 mesh=bpy.data.meshes.new(key.rsplit('/',1)[-1]);mesh.from_pydata([(x/100,-y/100,z/100) for x,y,z in part['vertices']],[],[t['v'] for t in part['triangles']])
 for name in part['materials']:mesh.materials.append(material(name))
 uv=mesh.uv_layers.new(name='UVMap')
 for poly,tri in zip(mesh.polygons,part['triangles']):
  poly.material_index=tri['material'];poly.use_smooth=True
  for li,val in zip(poly.loop_indices,tri['uv']):uv.data[li].uv=val
 mesh.normals_split_custom_set([(n[0],-n[1],n[2]) for t in part['triangles'] for n in t['n']]);meshes[key]=mesh
C=Matrix.Diagonal((.01,-.01,.01,1))
for row in d['instances']:
 if row['mesh'] not in meshes:continue
 door=by_actor.get(row['actor']);name=row['mesh'].rsplit('/',1)[-1].split('.')[0]
 group='01_Arquitectura_conservada'
 if name.startswith('V07R01_Techo_'):group='02_Techo_general'
 elif name.startswith('V07R01_Suelo_'):group='03_Suelos_juntas'
 elif name.startswith('V07R01_Muro_'):group='04_Cierres_visibles_definitivos'
 elif name.startswith('V07R01_Faldones_'):group='05_Cerramiento_escaleras'
 elif door:
  group='06_Ocho_accesos_originales' if door['id'].startswith('V07_SRV_') else '07_Seis_accesos_MEM' if door['id'].startswith('MEM_') else '08_Accesos_futuros_bloqueados' if not door['constructed'] else '09_Acceso_principal_D01'
 if group not in groups:groups[group]=bpy.data.collections.new(group);bpy.context.scene.collection.children.link(groups[group])
 obj=bpy.data.objects.new((door['id']+'_' if door else name+'_')+row['component']+'_'+str(row['index']),meshes[row['mesh']]);groups[group].objects.link(obj)
 q=row['rotation'];T=Matrix.LocRotScale(Vector(row['location']),Quaternion((q[3],*q[:3])),Vector(row['scale']));obj.matrix_world=C@T@C.inverted()
 obj['UE_actor']=row['actor'];obj['UE_component']=row['component'];obj['UE_mesh']=row['mesh'];obj['UE_instance']=row['index']
 for slot,mat in zip(obj.material_slots,row.get('overrides',[])):
  if mat:slot.link='OBJECT';slot.material=material(mat)
 counts[group]=counts.get(group,0)+1
 if not door:continue
 for prop in ('id','constructed','locked','external'):obj['door_'+prop]=door[prop]
 obj['policy_note']='UE: set DestinationConstructed true and SecurityLocked false only after destination geometry is integrated and validated.'
 if row['component'] not in door['leaves']:continue
 leaf=door['leaves'][row['component']];closed=obj.location.copy();delta=Vector(leaf['open_world'])-Vector(leaf['closed_world']);opened=closed+Vector((delta.x/100,-delta.y/100,delta.z/100))
 for frame,position in ((1,closed),(60,opened),(120,closed)):
  obj.location=position;obj.keyframe_insert(data_path='location',frame=frame)
 animated.append(obj.name)
assert len(animated)==36,len(animated)
scene=bpy.context.scene;scene.frame_set(1);scene.frame_end=120;scene.unit_settings.system='METRIC'
scene['revision']='V07 Cerramientos R01; exact authored Unreal geometry; 18 paired mechanisms previewed at frames 1/60/120.'
scene['future_accesses']='D02, D03, D04 have working mechanisms; runtime access remains locked until destinations are constructed.'
scene['design_pending']='Two large exterior voids between room volumes and the curved corridor are retained for design review; stair apertures remain open.'
scene['preview_note']='Animation is a geometric preview; Unreal door policies remain authoritative. Frame 1 is authored closed state.'
bpy.ops.file.pack_all();target.parent.mkdir(parents=True,exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(target))
unpacked=[im.name for im in bpy.data.images if im.source=='FILE' and not im.packed_file]
report=dict(ok=not unpacked,objects=len(scene.objects),meshes=len(meshes),animated_leaves=len(animated),groups=counts,materials=len(mats),unpacked_images=unpacked)
Path(a.report).write_text(json.dumps(report,indent=2));print('BLENDER_R01',report,flush=True)
