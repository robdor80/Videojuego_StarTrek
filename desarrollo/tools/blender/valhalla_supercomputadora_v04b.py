"""Prepare the measured two-leaf doorway on a new copy of the verified V04.

Blender --background --factory-startup --python-exit-code 1 --python THIS_FILE --
  --input V04.blend --output NEW_V04B.blend --evidence-dir NEW_DIRECTORY

Creates a private slotted copy of the two Component#120 doorway linings. The
original lining, door meshes, materials and UVs are retained. Door instances gain
linear diagnostic poses: frame 1 original, 20 closed with 4 mm centre seam, 60 open.
This is geometric preparation, not a UE5 door controller or mechanical approval.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

# Dynamic imports must not place experimental bytecode beside permanent sources.
sys.dont_write_bytecode=True

import bpy
import bmesh
import numpy as np
from mathutils import Matrix, Vector

INPUT_SHA256='e4dbf7a0b835fe0ad2f51500ca801b5a3c914069816885a2e8f551466fe27568'
LEAVES=('Component_435035','Component_435936')
LININGS=('Component_431089','Component_431089.001')
SLOT_CLEARANCE=.002
RETRACTION_CLEARANCE=.010
CENTRE_SEAM=.004


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def placed(instancer):
    items=[(i.object.original,i.matrix_world.copy()) for i in bpy.context.evaluated_depsgraph_get().object_instances
           if i.parent and i.parent.name==instancer and i.object.type=='MESH']
    if len(items)!=1:raise ValueError(f'Expected one mesh in {instancer}')
    obj,matrix=items[0];mesh=obj.data
    v=np.empty(len(mesh.vertices)*3);mesh.vertices.foreach_get('co',v)
    m=np.array(matrix);v=v.reshape(-1,3)@m[:3,:3].T+m[:3,3]
    return obj,matrix,v


def slotted_mesh(original,world,low,high):
    if original.has_custom_normals:raise ValueError('Review custom frame normals before clipping')
    parts=[]
    for keep_left,bound in [(True,low),(False,high)]:
        bm=bmesh.new();bm.from_mesh(original);bm.transform(world)
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
            dist=1e-7,plane_co=(bound,0,0),plane_no=(1,0,0),
            clear_outer=keep_left,clear_inner=not keep_left)
        bm.transform(world.inverted())
        part=bpy.data.meshes.new('V04B_TEMP_own_cut_half');bm.to_mesh(part);bm.free();parts.append(part)
    combined=bmesh.new()
    for part in parts:combined.from_mesh(part)
    result=original.copy();result.name='V04B_Revestimiento_Puerta_Ranura'
    combined.to_mesh(result);combined.free();result.update()
    for part in parts:bpy.data.meshes.remove(part)
    original.calc_loop_triangles();result.calc_loop_triangles()
    old_area=sum(t.area for t in original.loop_triangles);new_area=sum(t.area for t in result.loop_triangles)
    if not .05<1-new_area/old_area<.20:raise ValueError('Unreviewed lining area change')
    vertices=np.array([world@v.co for v in result.vertices])
    for tri in result.loop_triangles:
        x=vertices[list(tri.vertices),0]
        if not (x.max()<=low+5e-6 or x.min()>=high-5e-6):raise ValueError('Triangle bridges the measured slot')
    return result,{'original_area_m2':old_area,'slotted_area_m2':new_area,'removed_fraction':1-new_area/old_area}


def linear_keys(obj,poses):
    if obj.animation_data:raise ValueError('Do not overwrite existing animation')
    for frame,location in poses.items():
        obj.location=location;obj.keyframe_insert(data_path='location',frame=frame,group='V04B_Puerta_Diagnostico')
    action=obj.animation_data.action
    curves=[]
    if hasattr(action,'fcurves'):curves=list(action.fcurves)
    else:
        for layer in action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:curves.extend(bag.fcurves)
    if len(curves)!=3:raise ValueError('Unexpected location animation layout')
    for curve in curves:
        for key in curve.keyframe_points:key.interpolation='LINEAR'


def verify_translation_sweep(scene):
    """Conservative sufficient proof for this fixed input: no swept triangle box
    overlaps any fixed triangle box. A possible overlap is rejected for review,
    never accepted merely because a few sampled poses are clear.
    """
    scene.frame_set(20);bpy.context.view_layer.update();closed=[placed(name) for name in LEAVES]
    scene.frame_set(60);bpy.context.view_layer.update();opened=[placed(name) for name in LEAVES]
    sweeps=[]
    for (obj,_,start),(_,_,end) in zip(closed,opened):
        velocity=end[0]-start[0]
        if np.max(abs(end-start-velocity))>1e-5:raise ValueError('Door motion is not pure translation')
        obj.data.calc_loop_triangles();indices=np.array([tuple(t.vertices) for t in obj.data.loop_triangles]);tri=start[indices]
        low=np.minimum(tri,tri+velocity).min(1);high=np.maximum(tri,tri+velocity).max(1)
        sweeps.append((low,high))
    gap=float(closed[0][2][:,1].min()-closed[1][2][:,1].max())
    if gap<CENTRE_SEAM-1e-5:raise ValueError('Leaves overlap at closure')
    if not (opened[0][2][:,1].min()>closed[0][2][:,1].min() and opened[1][2][:,1].max()<closed[1][2][:,1].max()):
        raise ValueError('Leaf motions do not monotonically separate')
    envelope_low=np.min([x[0].min(0) for x in sweeps],axis=0);envelope_high=np.max([x[1].max(0) for x in sweeps],axis=0)
    floor=min(float(c[2][:,2].min()) for c in closed);fixed_meshes=0;fixed_triangles=0
    for item in bpy.context.evaluated_depsgraph_get().object_instances:
        if item.object.type!='MESH' or not len(item.object.data.polygons):continue
        if item.parent and item.parent.name in LEAVES:continue
        matrix=item.matrix_world.copy();box=np.array([matrix@Vector(v) for v in item.object.bound_box])
        if np.any(box.max(0)<envelope_low-1e-6) or np.any(box.min(0)>envelope_high+1e-6):continue
        mesh=item.object.data;mesh.calc_loop_triangles();v=np.array([matrix@v.co for v in mesh.vertices]);tri=v[np.array([tuple(t.vertices) for t in mesh.loop_triangles])]
        tri=tri[tri[:,:,2].max(1)>floor+1e-5]
        if not len(tri):continue
        fixed_meshes+=1;fixed_triangles+=len(tri);lo=tri.min(1);hi=tri.max(1)
        for low,high in sweeps:
            for a,b in zip(low,high):
                if np.any(((hi>=a-1e-6)&(lo<=b+1e-6)).all(1)):
                    raise ValueError(f'Possible swept triangle collision with {item.object.name}; review before saving')
    scene.frame_set(1);bpy.context.view_layer.update()
    return {'method':'Conservative swept triangle AABBs over complete linear closed-to-open translations; zero candidate box overlaps. Surface separation only, floor support below base + 0.010 mm excluded.',
            'fixed_mesh_placements_checked':fixed_meshes,'fixed_triangles_checked':fixed_triangles,
            'possible_triangle_overlap_pairs':0,'minimum_leaf_pair_y_gap_m':gap}


def main():
    parser=argparse.ArgumentParser()
    for name in ['input','output','evidence-dir']:parser.add_argument('--'+name,required=True,type=Path)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);source=args.input.resolve();output=args.output.resolve();evidence=args.evidence_dir.resolve()
    if sha(source)!=INPUT_SHA256:raise ValueError('Expected the reviewed, intact V04 input')
    if output.exists() or output==source:raise ValueError('Output must be a new file')
    if evidence.exists() and any(evidence.iterdir()):raise ValueError('Evidence directory must be new/empty')
    evidence.mkdir(parents=True,exist_ok=True)
    spec=importlib.util.spec_from_file_location('v04_helpers',Path(__file__).with_name('valhalla_supercomputadora_v04.py'))
    helpers=importlib.util.module_from_spec(spec);spec.loader.exec_module(helpers)
    bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
    original_meshes={m.name:helpers.mesh_digest(m) for m in bpy.data.meshes}
    states={o.name:helpers.object_state(o) for o in bpy.data.objects}
    materials=sorted(m.name for m in bpy.data.materials)
    images={im.name:hashlib.sha256(bytes(im.packed_file.data)).hexdigest() for im in bpy.data.images if im.source=='FILE' and im.packed_file}
    leaves=[placed(name) for name in LEAVES];linings=[placed(name) for name in LININGS]
    bounds=[(v.min(0),v.max(0)) for _,_,v in leaves]
    if max(abs(bounds[0][0][0]-bounds[1][0][0]),abs(bounds[0][1][0]-bounds[1][1][0]))>1e-5:
        raise ValueError('Leaf thicknesses are not aligned')
    low=min(b[0][0] for b in bounds)-SLOT_CLEARANCE;high=max(b[1][0] for b in bounds)+SLOT_CLEARANCE
    old_collection=bpy.data.objects[LININGS[0]].instance_collection
    if any(bpy.data.objects[name].instance_collection!=old_collection for name in LININGS):raise ValueError('Lining instances differ')
    if len(old_collection.objects)!=1 or old_collection.children:raise ValueError('Unexpected lining assembly')
    old_obj,world,_=linings[0]
    # Both lining placements have the same X coordinates; the private local slot
    # must map to the same world slab through the reflected southern instance.
    for _,matrix,_ in linings:
        if abs(matrix[0][0]-world[0][0])>1e-6 or abs(matrix[0][3]-world[0][3])>1e-6:
            raise ValueError('Review non-equivalent lining transforms')
    private,cut_info=slotted_mesh(old_obj.data,world,low,high)
    collection=bpy.data.collections.new('V04B_Revestimiento_Ranurado')
    replacement=old_obj.copy();replacement.data=private;replacement.name='V04B_Revestimiento_Puerta_120';collection.objects.link(replacement)
    for name in LININGS:bpy.data.objects[name].instance_collection=collection
    north_jamb=float(linings[0][2][:,1].max());south_jamb=float(linings[1][2][:,1].min());centre=(north_jamb+south_jamb)/2
    translations=[{'original':0.,'closed':centre+CENTRE_SEAM/2-float(bounds[0][0][1]),'open':north_jamb+RETRACTION_CLEARANCE-float(bounds[0][0][1])},
                  {'original':0.,'closed':centre-CENTRE_SEAM/2-float(bounds[1][1][1]),'open':south_jamb-RETRACTION_CLEARANCE-float(bounds[1][1][1])}]
    pose_records=[]
    for name,travel in zip(LEAVES,translations):
        obj=bpy.data.objects[name]
        if obj.parent:raise ValueError('Review parent-space door motion')
        original_location=obj.location.copy();poses={frame:original_location+Vector((0,travel[label],0)) for frame,label in [(1,'original'),(20,'closed'),(60,'open')]}
        linear_keys(obj,poses);pose_records.append({'instance':name,'translation_y_m':travel,'locations':{str(k):list(v) for k,v in poses.items()}})
    scene.frame_start=1;scene.frame_end=60
    for label,frame in [('V04B_ORIGINAL_REFERENCIA',1),('V04B_CERRADA_DIAGNOSTICO_4mm',20),('V04B_ABIERTA_DIAGNOSTICO',60)]:scene.timeline_markers.new(label,frame=frame)
    sweep_info=verify_translation_sweep(scene)
    scene.frame_set(1);bpy.context.view_layer.update()
    for name,state in states.items():
        expected=dict(state)
        if name in LININGS:expected['instance_collection']=collection.name
        assert helpers.object_state(bpy.data.objects[name])==expected,name
    assert all(helpers.mesh_digest(bpy.data.meshes[n])==s for n,s in original_meshes.items())
    assert sorted(m.name for m in bpy.data.materials)==materials
    assert {im.name:hashlib.sha256(bytes(im.packed_file.data)).hexdigest() for im in bpy.data.images if im.source=='FILE' and im.packed_file}==images
    scene['estado_geometrico']='V04B PARCIAL: ranuras locales y barridos lineales de puerta comprobados; 128 cruces de bancos y validación UE5 pendientes'
    scene['V04B_estado_original_frame']=1;scene['V04B_estado_cerrado_frame']=20;scene['V04B_estado_abierto_frame']=60
    scene['validacion_UE5']='Pendiente: control, colisiones, seguridad y navegación; cápsula provisional 0.70 x 1.80 m'
    bpy.context.preferences.filepaths.save_version=0;output.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output),compress=True,relative_remap=False)
    report={'input_sha256':INPUT_SHA256,'output_sha256':sha(output),'output_bytes':output.stat().st_size,
            'slot_world_x_m':[low,high],'slot_width_m':high-low,'side_clearance_m':SLOT_CLEARANCE,
            'lining_depth_x_m':float(linings[0][2][:,0].max()-linings[0][2][:,0].min()),
            'jamb_y_m':[south_jamb,north_jamb],'portal_width_m':north_jamb-south_jamb,
            'poses':pose_records,'cut':cut_info,'sweep_validation':sweep_info,'original_mesh_blocks_preserved':len(original_meshes),
            'original_objects_preserved':len(states),'new_object':replacement.name,'new_collection':collection.name,
            'new_mesh':private.name,'original_materials_preserved':len(materials),'packed_images':images,
            'warning':'Geometric preparation only. Functional approval requires independent swept-surface validation and UE5 checks; original frame 1 has the original 0.33 m opening, not an airtight closed state.'}
    (evidence/'preparacion_v04b.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    assert sha(source)==INPUT_SHA256
    print('V04B_PREPARED',json.dumps(report),flush=True)


if __name__=='__main__':main()
