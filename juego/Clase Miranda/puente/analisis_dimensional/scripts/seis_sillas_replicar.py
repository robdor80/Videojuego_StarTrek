"""Reproducible bounded replication; refuses to overwrite source or existing output.
Run: blender --background <original.blend> --python <this script> --disable-autoexec
"""
import bpy, json, sys, os, hashlib, math
from pathlib import Path
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).parent))
from seis_sillas_comun import *

assert Path(bpy.data.filepath).resolve()==ORIGINAL.resolve()
assert not OUTPUT.exists(),f'Refusing to overwrite {OUTPUT}'
source_sha=integrity.file_sha(ORIGINAL)
baseline=extra_snapshot()
(ROOT/'datos'/'seis_sillas_antes.json').write_text(json.dumps(baseline,ensure_ascii=False),encoding='utf-8')
chair=chair_group(MASTER_ANCHOR)
assert len(chair)==14 and not any(o.name.startswith(('Mesh.587_0','Mesh.595_0')) for o in chair)
platform=bpy.data.objects['Floor_aiWireframe1_0'];foot=bpy.data.objects['Cilindro']
source_mesh=chair+[platform,foot]
source_objects=with_parents(source_mesh)
assert len(source_objects)==31
assert not any(o.constraints or o.modifiers or o.animation_data for o in source_objects)
plans=[]
for station,anchor in TARGETS:
    old=chair_group(anchor);assert len(old)==16
    oldobjs=with_parents(old);assert len(oldobjs)==32
    delta=rigid_delta(MASTER_ANCHOR,anchor)
    plans.append((station,anchor,old,oldobjs,delta))

def collection(name,parent):
    c=bpy.data.collections.new(name);parent.children.link(c);return c
def move(objects,dest):
    for o in objects:
        for c in list(o.users_collection):c.objects.unlink(o)
        dest.objects.link(o)
top=collection('SS_Sillas_Operativas_Seis_01',bpy.context.scene.collection)
master_col=collection('P01_Maestra_Xpos_Y-5.51422',top)
archive=collection('SS_Originales_5_Recuperables',bpy.context.scene.collection)
archive.hide_viewport=True;archive.hide_render=True

# Correct only the manual foot's vertical placement, preserving geometry and scale.
# Base rests on the installed platform's top, which is flat under the column.
foot_before=[list(r) for r in foot.matrix_world]
foot_bounds=bounds([foot]);platform_bounds=bounds([platform])
platform_axis_hit=bvh(platform).ray_cast(Vector((foot.matrix_world.translation.x,foot.matrix_world.translation.y,.2)),Vector((0,0,-1)),.5)[0]
assert platform_axis_hit is not None
dz=platform_axis_hit.z-foot_bounds[0][2]
assert 0<dz<.05
foot.location.z+=dz
bpy.context.view_layer.update()
move(source_objects,master_col)
manifest={'input':str(ORIGINAL),'output':str(OUTPUT),'source_sha256':source_sha,'blender':bpy.app.version_string,
 'master_anchor':MASTER_ANCHOR,'master_collection':master_col.name,
 'master_meshes':[o.name for o in source_mesh],'master_objects':[o.name for o in source_objects],
 'master_foot_adjustment':{'dz_m':dz,'world_before':foot_before,'world_after':[list(r) for r in foot.matrix_world]},
 'archive_collection':archive.name,'stations':[],
 'removed_rails':['FloorRail01_aiWireframe1_0','FloorRail02_aiWireframe1_0'],
 'removed_objects':['FloorRail01_aiWireframe1_0','FloorRail02_aiWireframe1_0','FloorRail01','FloorRail02'],
 'removed_mesh_datablocks':[],
 'notes':['Loose imported FloorRail objects at world origin removed per explicit user instruction, including their exclusive empty parents.',
          'Installed platform retains its modeled guide grooves; no functioning slide/rail mechanism is inferred.',
          'Source foot vertical adjustment is applied equally to all six sets; no mesh, material, or scale edits.']}
source_world={o:o.matrix_world.copy() for o in source_objects}
for station,anchor,old,oldobjs,delta in plans:
    restore=collection('Original_'+station,archive);move(oldobjs,restore)
    dest=collection(station,top)
    root=bpy.data.objects.new('SS_'+station,None);dest.objects.link(root)
    root.empty_display_type='PLAIN_AXES';root.empty_display_size=.18
    # Group empty is an identity grouping node; copied parent matrices carry the rigid placement.
    copies={}
    for o in source_objects:
        cp=o.copy();cp.name='SS_'+station+'__'+o.name;dest.objects.link(cp);copies[o]=cp
    for o,cp in copies.items():
        cp.parent=copies.get(o.parent,root)
        cp.matrix_parent_inverse=o.matrix_parent_inverse.copy() if o.parent in copies else Matrix.Identity(4)
        if o.parent not in copies:cp.matrix_world=delta@source_world[o]
        else:cp.matrix_basis=o.matrix_basis.copy()
    bpy.context.view_layer.update()
    for o,cp in copies.items():
        err=max(abs(cp.matrix_world[i][j]-(delta@source_world[o])[i][j]) for i in range(4) for j in range(4))
        assert err<2e-5,(o.name,err)
        if o.type=='MESH':assert cp.data==o.data
    meshes=[copies[o] for o in source_mesh]
    manifest['stations'].append({'station':station,'target_anchor':anchor,'old_meshes':[o.name for o in old],
        'old_objects':[o.name for o in oldobjs],'archive_subcollection':restore.name,'collection':dest.name,
        'group_empty':root.name,'mapping':{o.name:cp.name for o,cp in copies.items()},
        'delta_world':[list(r) for r in delta],
        'target_origin_m':list(bpy.data.objects[anchor].matrix_world.translation),
        'relative_yaw_deg':math.degrees(math.atan2(delta[1][0],delta[0][0])),
        'bounds_m':bounds(meshes),'dimensions_world_m':dimensions(meshes)})
manifest['master_bounds_m']=bounds(source_mesh)
manifest['master_dimensions_world_m']=dimensions(source_mesh)
manifest['changed_existing_objects']=sorted([o.name for o in source_objects]+[o.name for p in plans for o in p[3]])
for name in manifest['removed_objects']:
    o=bpy.data.objects[name]
    if o.type=='EMPTY':assert not o.children
    data=o.data
    bpy.data.objects.remove(o,do_unlink=True)
    if isinstance(data,bpy.types.Mesh) and data.users==0:
        manifest['removed_mesh_datablocks'].append(data.name)
        bpy.data.meshes.remove(data)
manifest_path=ROOT/'datos'/'seis_sillas_manifest.json'
manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
# Keep all embedded image data and existing relative paths (output is in the same directory).
bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT),check_existing=True,relative_remap=False)
assert integrity.file_sha(ORIGINAL)==source_sha,'Original changed'
print('SAVED',OUTPUT,'MASTER_MESHES',len(source_mesh),'REPLICAS',len(plans),'FOOT_DZ',dz)
