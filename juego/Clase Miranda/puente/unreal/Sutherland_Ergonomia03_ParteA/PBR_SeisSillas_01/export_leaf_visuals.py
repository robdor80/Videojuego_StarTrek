import bpy,bmesh,json,pathlib,re
from mathutils import Vector,Matrix
R=pathlib.Path(__file__).parent;old=json.loads((R.parent/'Data/export_meshes.json').read_text());out=[]
for d in old['doors']:
    o=bpy.data.objects[d['source']];mesh=o.data.copy();mesh.transform(o.matrix_world)
    expected=d['expected_world_cm'];sign=1 if sum(v[0] for v in expected)>0 else -1
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.x*sign<=0],context='VERTS');bm.to_mesh(mesh);bm.free()
    points=[v.co.copy() for v in mesh.vertices];pivot=sum(points,Vector())/len(points);mesh.transform(Matrix.Translation(-pivot))
    name='SM_PBR_'+d['actor']+'_'+d['component'];path=R/'Exports'/(name+'.fbx');assert not path.exists()
    obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj);bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
    bpy.ops.export_scene.fbx(filepath=str(path),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_NONE',use_mesh_modifiers=False,mesh_smooth_type='FACE',use_tspace=True,bake_anim=False,path_mode='STRIP')
    out.append({'door':d['actor'],'component':d['component'],'source':d['source'],'asset':name,'file':str(path),'position_cm':[pivot.x*100,-pivot.y*100,pivot.z*100],'points_cm':[[v.x*100,-v.y*100,v.z*100] for v in points]})
    bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
(R/'leaf_visual_export.json').write_text(json.dumps(out,indent=2));print('LEAF_VISUALS',len(out))
