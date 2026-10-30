"""Export only visible mesh geometry and original texture bytes, never scene lighting."""
import bpy,json,re,sys,hashlib,shutil
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).parent; X=R/'Exports';X.mkdir(exist_ok=True)
sys.path.insert(0,str(R.parents[2]/'analisis_dimensional/scripts'))
import pbr01_integrity as I
audit=json.loads((R/'blender_audit.json').read_text(encoding='utf-8'))
assert I.file_sha(bpy.data.filepath)==audit['sha256']
assert not (R/'export.json').exists(),'Export already complete; inspect instead'
def safe(s):return re.sub('[^a-zA-Z0-9_]+','_',s).strip('_')
images={};materials={}
def image(im):
    if im.name in images:return images[im.name]
    name='T_'+safe(im.name);p=X/(name+Path(im.filepath).suffix)
    if not p.suffix or p.suffix.lower() not in ['.png','.jpg','.jpeg','.tga','.bmp','.exr']:p=X/(name+'.png')
    if im.packed_file:p.write_bytes(bytes(im.packed_file.data))
    else:shutil.copyfile(bpy.path.abspath(im.filepath),p)
    rec={'name':name,'file':str(p),'colorspace':im.colorspace_settings.name,'sha256':I.file_sha(p)}
    images[im.name]=rec;return rec
def socket(s):
    if not s.is_linked:
        v=s.default_value
        return {'op':'constant','value':list(v) if hasattr(v,'__len__') and not isinstance(v,str) else v}
    l=s.links[0];n=l.from_node
    if n.type=='TEX_IMAGE':
        uv={'scale':[1,1,1],'location':[0,0,0]}
        if n.inputs['Vector'].is_linked:
            mn=n.inputs['Vector'].links[0].from_node
            if mn.type=='MAPPING':
                assert max(abs(v) for v in mn.inputs['Rotation'].default_value)<1e-6
                uv={'scale':list(mn.inputs['Scale'].default_value),'location':list(mn.inputs['Location'].default_value)}
            else:assert mn.type=='TEX_COORD'
        return {'op':'texture','texture':image(n.image),'uv':uv,'output':l.from_socket.name}
    if n.type=='MIX':
        assert n.data_type=='RGBA'
        return {'op':'mix','mode':n.blend_type,'factor':socket(n.inputs[0]),'a':socket(n.inputs[6]),'b':socket(n.inputs[7]),'clamp':n.clamp_result}
    if n.type=='HUE_SAT':return {'op':'hsv','color':socket(n.inputs['Color']),**{k.lower():n.inputs[k].default_value for k in ['Hue','Saturation','Value','Factor']}}
    if n.type=='NORMAL_MAP':return {'op':'normal','color':socket(n.inputs['Color']),'strength':n.inputs['Strength'].default_value}
    if n.type=='MATH':return {'op':'math','mode':n.operation,'a':socket(n.inputs[0]),'b':socket(n.inputs[1]),'clamp':n.use_clamp}
    raise RuntimeError(('Unsupported shader node; no approximation',n.name,n.type))
visible=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.visible_get() and not o.hide_render]
used={s.material for o in visible for s in o.material_slots if s.material}
for m in sorted(used,key=lambda m:m.name):
    nodes=m.node_tree.nodes;ps=[n for n in nodes if n.type=='BSDF_PRINCIPLED'];em=[n for n in nodes if n.type=='EMISSION']
    rec={'name':'M_'+safe(m.name),'source_hash':I.graph_hash(m),'source':m.name}
    if ps:
        p=ps[-1];rec['kind']='pbr';rec['channels']={k:socket(p.inputs[k]) for k in ['Base Color','Metallic','Roughness']}
        if p.inputs['Normal'].is_linked:rec['channels']['Normal']=socket(p.inputs['Normal'])
    else:
        assert em,m.name
        rec['kind']='visual_emissive';rec['channels']={'Emission':socket(em[0].inputs['Color'])};rec['strength']=em[0].inputs['Strength'].default_value
    materials[m.name]=rec
rows=[];dg=bpy.context.evaluated_depsgraph_get()
doors={'Plane.001_0','Plane.017_0','Plane.018_0','Plane.019_0'}
for o in visible:
    if o.name in doors:continue
    name='SM_PBR_'+safe(o.name);p=X/(name+'.fbx');assert not p.exists(),p
    evaluated=o.evaluated_get(dg);mesh=bpy.data.meshes.new_from_object(evaluated,depsgraph=dg,preserve_all_data_layers=True)
    mesh.transform(o.matrix_world)
    pts=[v.co.copy() for v in mesh.vertices];lo=Vector(tuple(min(v[i] for v in pts) for i in range(3)));hi=Vector(tuple(max(v[i] for v in pts) for i in range(3)));pivot=(lo+hi)/2
    mesh.transform(Matrix.Translation(-pivot));obj=bpy.data.objects.new(name,mesh);bpy.context.scene.collection.objects.link(obj)
    bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
    bpy.ops.export_scene.fbx(filepath=str(p),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_NONE',use_mesh_modifiers=False,mesh_smooth_type='FACE',use_tspace=True,bake_anim=False,path_mode='STRIP')
    rows.append({'source':o.name,'asset':name,'file':str(p),'position_cm':[pivot.x*100,-pivot.y*100,pivot.z*100],'bounds_cm':[[lo.x*100,-hi.y*100,lo.z*100],[hi.x*100,-lo.y*100,hi.z*100]],'materials':[s.material.name if s.material else None for s in o.material_slots],'points_cm':[[v.x*100,-v.y*100,v.z*100] for v in pts],'triangles':sum(len(f.vertices)-2 for f in mesh.polygons)})
    bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
out={'ok':True,'source_hash':audit['sha256'],'objects':rows,'materials':materials,'images':images,'excluded_lights':audit['lights'],'excluded_hidden_meshes':[o['name'] for o in audit['objects'] if not o['visible']],'doors_reuse_existing_mechanisms':sorted(doors),'lighting_baked':False}
(R/'export.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
assert I.file_sha(bpy.data.filepath)==audit['sha256']
print('PBR_EXPORT_OK',len(rows),len(materials),len(images),flush=True)
