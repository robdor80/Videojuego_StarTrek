"""Independent read-only check after reopening the result; produces a full audit JSON."""
import bpy,json,sys,os,math
from pathlib import Path
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).parent))
from seis_sillas_comun import *
assert Path(bpy.data.filepath).resolve()==OUTPUT.resolve()
m=json.loads((ROOT/'datos'/'seis_sillas_manifest.json').read_text(encoding='utf-8'))
before=json.loads((ROOT/'datos'/'seis_sillas_antes.json').read_text(encoding='utf-8'))
# Disabled collections do not evaluate their objects on load. Enable only in memory
# to verify the archived world transforms, then restore the saved display flag.
archive=bpy.data.collections[m['archive_collection']]
archive_saved_hidden=(archive.hide_render,archive.hide_viewport)
archive.hide_viewport=False
bpy.context.view_layer.update()
after=json.loads(json.dumps(extra_snapshot()))
archive.hide_viewport=archive_saved_hidden[1]
bpy.context.view_layer.update()
expected_meshes={k:v for k,v in before['meshes'].items() if k not in m['removed_mesh_datablocks']}
expected_assignments={k:v for k,v in before['assignments_all'].items() if k not in m['removed_objects']}
errors=[]
def check(ok,label):
    if not ok:errors.append(label)
check(integrity.file_sha(ORIGINAL)==m['source_sha256'],'source_hash')
check(expected_meshes==after['meshes'],'all_retained_meshes_geometry_UV_normals_attributes')
check(expected_assignments=={k:after['assignments_all'][k] for k in expected_assignments},'original_material_assignments')
check(before['materials']==after['materials'],'all_material_graphs')
check(before['images']==after['images'],'all_packed_images')
check(before['image_paths']==after['image_paths'],'image_paths')
check(before['scene']==after['scene'],'scene_camera_world_engine_units')
changed=set(m['changed_existing_objects'])
existing_differences={}
for name,old in before['objects'].items():
    if name in m['removed_objects']:
        check(name not in after['objects'],'deleted_rail:'+name)
        continue
    new=after['objects'][name]
    differences=[k for k in old if old[k]!=new[k]]
    if differences:existing_differences[name]=differences
    allowed={'collections'} if name in changed else set()
    if name=='Cilindro':allowed|={'world','local','basis','location'}
    check(set(differences)<=allowed,'unexpected_change:'+name+':'+str(differences))
for name,old in before['collections'].items():
    new=after['collections'][name]
    expected=dict(old);expected['objects']=[n for n in old['objects'] if n not in changed and n not in m['removed_objects']]
    check(new==expected,'original_collection:'+name)
archive=bpy.data.collections[m['archive_collection']]
check(all(archive_saved_hidden),'archive_hidden')
source=[bpy.data.objects[n] for n in m['master_meshes']]
chair_names=set(n for n in before['objects'] if PATTERN.fullmatch(n))
new_names={n for s in m['stations'] for n in s['mapping'].values()}
ignored=chair_names|new_names|set(m['master_meshes'])
environment=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name not in ignored and not o.hide_render and not o.hide_viewport]
trees={o.name:bvh(o) for o in environment}
bbs={o.name:bounds([o]) for o in environment}
all_stations=[{'station':'P01_Maestra','meshes':source,'mapping':{o.name:o.name for o in source},'yaw':0.0}]
for s in m['stations']:
    mapping=s['mapping'];delta=Matrix(s['delta_world'])
    for src,dst in mapping.items():
        a=bpy.data.objects[src];b=bpy.data.objects[dst]
        err=max(abs(b.matrix_world[i][j]-(delta@a.matrix_world)[i][j]) for i in range(4) for j in range(4))
        check(err<2e-5,'replica_matrix:'+dst)
        check(a.data==b.data,'linked_geometry:'+dst)
        check(after['objects'][src]['modifiers']==after['objects'][dst]['modifiers'],'replica_modifiers:'+dst)
        if a.type=='MESH':
            check(integrity.material_assignment(a)==integrity.material_assignment(b),'replica_materials:'+dst)
            check((a.dimensions-b.dimensions).length<2e-5,'replica_dimensions:'+dst)
        check(b.parent.name==mapping.get(a.parent.name,s['group_empty']) if a.parent else b.parent.name==s['group_empty'],'replica_parent:'+dst)
    oldcol=bpy.data.collections[s['archive_subcollection']]
    check(sorted(o.name for o in oldcol.objects)==sorted(s['old_objects']),'originals_preserved:'+s['station'])
    all_stations.append({'station':s['station'],'meshes':[bpy.data.objects[mapping[n]] for n in m['master_meshes']],
                         'mapping':mapping,'yaw':s['relative_yaw_deg']})
stations=[]
for s in all_stations:
    meshes=s['meshes'];bb=bounds(meshes);collisions=[]
    for a in meshes:
        ab=bounds([a]);at=bvh(a)
        for e in environment:
            eb=bbs[e.name]
            if any(ab[1][i]<eb[0][i]-1e-6 or eb[1][i]<ab[0][i]-1e-6 for i in range(3)):continue
            hits=at.overlap(trees[e.name])
            if hits:collisions.append({'chair_component':a.name,'environment':e.name,'intersecting_face_pairs':len(hits)})
    platform=bpy.data.objects[s['mapping']['Floor_aiWireframe1_0']]
    foot=bpy.data.objects[s['mapping']['Cilindro']]
    fb=bounds([foot]);pb=bounds([platform]);floor_samples=[]
    for x,y in [(pb[0][0],pb[0][1]),(pb[1][0],pb[0][1]),(pb[1][0],pb[1][1]),(pb[0][0],pb[1][1]),tuple(foot.matrix_world.translation[:2])]:
        floor_samples.append(floor_at(x,y))
    floor_z=max(p[2] for p in floor_samples)
    check(bb[0][2]>=floor_z-2e-5,'floor_penetration:'+s['station'])
    platform_top=bvh(platform).ray_cast(Vector((foot.matrix_world.translation.x,foot.matrix_world.translation.y,.2)),Vector((0,0,-1)),.5)[0]
    gap=None if platform_top is None else fb[0][2]-platform_top.z
    check(gap is not None and abs(gap)<2e-5,'foot_platform_contact:'+s['station'])
    floor_contacts=[c for c in collisions if c['environment']=='Circle_0' and bb[0][2]>=floor_z-2e-5]
    collisions=[c for c in collisions if c not in floor_contacts]
    check(not collisions,'environment_intersection:'+s['station'])
    stations.append({'station':s['station'],'yaw_relative_deg':s['yaw'],'bounds_m':bb,'dimensions_world_m':dimensions(meshes),
        'mesh_count':len(meshes),'floor_samples_m':floor_samples,'minimum_ground_clearance_m':bb[0][2]-floor_z,
        'foot_to_platform_gap_at_axis_m':gap,'environment_surface_intersections':collisions,'floor_surface_contacts_within_tolerance':floor_contacts})
missing=[im.name for im in bpy.data.images if im.source=='FILE' and not im.packed_file and not len(im.packed_files) and not os.path.isfile(bpy.path.abspath(im.filepath))]
check(not missing,'missing_external_images')
report={'ok':not errors,'errors':errors,'input_sha256':m['source_sha256'],'output_sha256':integrity.file_sha(OUTPUT),
    'original_objects':len(before['objects']),'result_objects':len(after['objects']),
    'retained_mesh_datablocks_unchanged':expected_meshes==after['meshes'],
    'materials_unchanged':before['materials']==after['materials'],'images_unchanged':before['images']==after['images'],
    'missing_images':missing,'existing_object_differences':existing_differences,'stations':stations,
    'collision_method':'Evaluated world-space BVH triangle surface overlap against every visible environment mesh; floor rays at four platform corners and axis. Intended internal assembly overlaps excluded. Does not certify ergonomics or watertight solid containment.',
    'removed_objects':m['removed_objects'],'removed_mesh_datablocks':m['removed_mesh_datablocks']}
(ROOT/'datos'/'seis_sillas_verificacion.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
print('VERIFIED',json.dumps({k:report[k] for k in ['ok','errors','retained_mesh_datablocks_unchanged','materials_unchanged','images_unchanged','missing_images']}))
for s in stations:print('STATION',s['station'],'DIMS',s['dimensions_world_m'],'GAP',s['foot_to_platform_gap_at_axis_m'],'COLLISIONS',s['environment_surface_intersections'])
