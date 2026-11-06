import bpy,json,hashlib
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=[]
for label in ['coleccion','puente_obj']:
 path=R/'ESCENAS'/f'VOY05A_{label}_Revision.blend';bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False)
 a=json.loads((R/'DATOS'/f'{label}_auditoria.json').read_text())['objects'];z=np.load(R/'DATOS'/f'{label}_geometria.npz');v=z['vertices'];t=z['triangles'];ids=z['object_ids'];checks=[]
 base=0
 for i,source in enumerate(a):
  o=bpy.data.objects[source['object']];m=o.data;m.calc_loop_triangles();vv=np.array([o.matrix_world@p.co for p in m.vertices]);tt=np.array([p.vertices[:] for p in m.loop_triangles]);orig=v[base:base+len(vv)];tri=t[ids==i]-base;err=float(abs(vv-orig).max())
  checks.append(dict(object=o.name,vertices_equal=bool(np.array_equal(vv,orig)),max_world_vertex_error=err,triangles_equal=bool(np.array_equal(tt,tri)),materials_equal=[x.name if x else None for x in m.materials]==source['materials'],uv_names_equal=[x.name for x in m.uv_layers]==source['uv_layers'],animation_present=bool(o.animation_data)))
  base+=len(vv)
 # Compare every UV coordinate and material face assignment with the copied source blend/import.
 snapshot={o.name:dict(uv={uv.name:np.array([l.uv[:] for l in uv.data]) for uv in o.data.uv_layers},material=np.array([p.material_index for p in o.data.polygons])) for o in bpy.data.objects if o.type=='MESH'}
 images=[dict(name=im.name,packed=bool(im.packed_file),path=im.filepath) for im in bpy.data.images if im.source=='FILE'];result=dict(scene=str(path),objects=len(checks),checks=checks,geometry_equal=all(x['vertices_equal'] and x['triangles_equal'] for x in checks),materials_equal=all(x['materials_equal'] for x in checks),images=images,linked_libraries=[x.filepath for x in bpy.data.libraries])
 if label=='coleccion':bpy.ops.wm.open_mainfile(filepath=str(R/'FUENTES/COLECCION/star-trek-voyager-collection/source/StarTrekVoyagerCollection.blend'),load_ui=False,use_scripts=False)
 else:
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.wm.obj_import(filepath=str(R/'FUENTES/PUENTE/Voyager Bridge.obj'),use_split_objects=True,use_split_groups=True,validate_meshes=True,forward_axis='NEGATIVE_Z',up_axis='Y')
 uvchecks=[]
 for name,snap in snapshot.items():
  m=bpy.data.objects[name].data;uvchecks.append(dict(object=name,all_uv_coordinates_equal=all(np.array_equal(np.array([l.uv[:] for l in m.uv_layers[uvname].data]),values) for uvname,values in snap['uv'].items()),polygon_materials_equal=np.array_equal(np.array([p.material_index for p in m.polygons]),snap['material'])))
 result['uv_checks']=uvchecks;result['uv_and_material_assignments_equal']=all(x['all_uv_coordinates_equal'] and x['polygon_materials_equal'] for x in uvchecks);result['ok']=bool(result['geometry_equal'] and result['materials_equal'] and result['uv_and_material_assignments_equal'] and not result['linked_libraries']);out.append(result);print('READBACK',label,result['ok'],flush=True)
(R/'VERIFICACION/escenas_readback.json').write_text(json.dumps(out,indent=2,default=lambda x:x.item()),encoding='utf8')
