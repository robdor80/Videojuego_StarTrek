"""Read-only source measurements; all outputs are analysis evidence."""
import bpy,json,sys,hashlib,math
import numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'ergonomia_correderas_01';R.mkdir(exist_ok=True)
if bpy.context.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.update()
manifest=json.loads((ROOT/'datos/seis_sillas_manifest.json').read_text(encoding='utf-8'))
stations=[{'id':'P01','mapping':{n:n for n in manifest['master_meshes']}}]+[{'id':f'P{i+2:02d}','mapping':s['mapping']} for i,s in enumerate(manifest['stations'])]
data={'source':bpy.data.filepath,'source_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'objects':{},'stations':stations}
arrays={};dg=bpy.context.evaluated_depsgraph_get()
for o in bpy.context.scene.objects:
 if o.type!='MESH' or not o.visible_get() or o.hide_render:continue
 ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles()
 verts=np.array([list(o.matrix_world@v.co) for v in me.vertices],dtype=np.float64)*100
 tris=np.array([list(t.vertices) for t in me.loop_triangles],dtype=np.int32)
 key=f'O{len(data["objects"]):03d}';arrays[key+'_v']=verts;arrays[key+'_t']=tris
 data['objects'][o.name]={'key':key,'bounds_cm':[verts.min(0).tolist(),verts.max(0).tolist()],'origin_cm':list(o.matrix_world.translation*100),'matrix':[list(x) for x in o.matrix_world],'materials':[s.material.name if s.material else None for s in o.material_slots],'tri_materials':[t.material_index for t in me.loop_triangles],'triangles':len(tris),'vertices':len(verts)}
 ev.to_mesh_clear()
for s in stations:
 mapping=s['mapping'];anchor=bpy.data.objects[mapping['Mesh.589_0.002']];foot=bpy.data.objects[mapping['Cilindro']];platform=bpy.data.objects[mapping['Floor_aiWireframe1_0']]
 names=[mapping[n] for n in manifest['master_meshes']];s['objects']=names;s['moving_objects']=[n for n in names if n!=platform.name];s['fixed_platform']=platform.name
 s['anchor_cm']=list(anchor.matrix_world.translation*100);s['cylinder_center_cm']=data['objects'][foot.name]['origin_cm'];s['forward_world']=[1 if s['anchor_cm'][0]>0 else -1,0,0]
 s['seat_bounds_cm']=data['objects'][anchor.name]['bounds_cm'];s['platform_bounds_cm']=data['objects'][platform.name]['bounds_cm'];s['foot_bounds_cm']=data['objects'][foot.name]['bounds_cm']
 data['stations'][int(s['id'][1:])-1]=s
np.savez_compressed(R/'geometria_fuente_cm.npz',**arrays)
(R/'mediciones_blender.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
print('MEASURED',len(data['objects']),'objects')
for s in stations:print(s['id'],'SEAT',s['seat_bounds_cm'],'PLATFORM',s['platform_bounds_cm'],'FOOT',s['foot_bounds_cm'])
