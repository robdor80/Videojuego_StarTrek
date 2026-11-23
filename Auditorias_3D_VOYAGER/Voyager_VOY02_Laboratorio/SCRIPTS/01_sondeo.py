import bpy,json,sys,math,collections
import numpy as np
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
def save_meshes(label):
 rows=[];vv=[];tt=[];ids=[];norm=[];mi=[];mnames=[]
 for ob in sorted((o for o in bpy.context.scene.objects if o.type=='MESH'),key=lambda o:o.name):
  me=ob.data;me.calc_loop_triangles();v=np.array([ob.matrix_world@x.co for x in me.vertices],dtype=np.float64).reshape((-1,3));t=np.array([x.vertices[:] for x in me.loop_triangles],dtype=np.int32).reshape((-1,3));base=sum(len(a) for a in vv);k=len(rows)
  vv.append(v);tt.append(t+base);ids.extend([k]*len(t));n=np.cross(v[t[:,1]]-v[t[:,0]],v[t[:,2]]-v[t[:,0]]) if len(t) else np.empty((0,3));norm.append(n)
  slots=[m.name if m else 'NONE' for m in me.materials];counter=collections.Counter(slots[t.material_index] if t.material_index<len(slots) else 'NONE' for t in me.loop_triangles)
  used=np.unique(t) if len(t) else np.array([],dtype=int);pv=v[used] if len(used) else v
  rows.append({'name':ob.name,'parent':ob.parent.name if ob.parent else None,'vertices':len(v),'triangles':len(t),'bounds_min':pv.min(axis=0).tolist() if len(pv) else [0]*3,'bounds_max':pv.max(axis=0).tolist() if len(pv) else [0]*3,'materials':dict(counter),'origin':list(ob.matrix_world.translation),'scale':list(ob.scale)})
 np.savez_compressed(R/'DATOS'/f'{label}_geometria.npz',vertices=np.vstack(vv),triangles=np.vstack(tt),object_ids=np.array(ids,dtype=np.int32),cross_normals=np.vstack(norm))
 (R/'DATOS'/f'{label}_objetos.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
 print(label,len(rows),sum(r['triangles'] for r in rows),flush=True)
requested=sys.argv[sys.argv.index('--')+1:] if '--'in sys.argv else ['obj','modulos','max']
if 'obj'in requested:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.wm.obj_import(filepath=str(R/'FUENTES/OBJ/Voyager Bridge.obj'),use_split_objects=True,use_split_groups=True,validate_meshes=True,forward_axis='NEGATIVE_Z',up_axis='Y');save_meshes('obj')
 for ob in bpy.context.scene.objects:ob['VOY02_ORIGEN']='OBJ_ORIGINAL_COPIA'
 bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
 bpy.ops.wm.save_as_mainfile(filepath=str(R/'FUENTES/OBJ/puente_base_importado.blend'))
if 'modulos'in requested:
 bpy.ops.wm.open_mainfile(filepath=str(R/'FUENTES/COLECCION/coleccion_original.blend'),load_ui=False,use_scripts=False);save_meshes('modulos')
if 'max'in requested:
 bpy.ops.wm.open_mainfile(filepath=str(R/'FUENTES/MAX/puente_max_conversion.blend'),load_ui=False,use_scripts=False);save_meshes('max')
