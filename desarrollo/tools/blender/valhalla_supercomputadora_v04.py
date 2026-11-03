"""Apply an explicitly reviewed local frame-fitting plan to a new Blender file.

Blender --background --factory-startup --python THIS_FILE --
  --input V03.blend --plan reviewed.json --output V04.blend --evidence-dir NEW_DIR

The JSON plan supplies input_sha256, clearance_m, and groups of operations with
object, expected_component, planes (unit world normal and offset), and max_cut_m.
Only closed, single-material structural frames may be trimmed. Existing source
meshes, architectural objects, UVs on surviving faces and materials are retained.
This tool neither reconstructs the room nor certifies Unreal Engine navigation.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
import bmesh
import numpy as np
from mathutils import Vector


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mesh_digest(mesh):
    h=hashlib.sha256()
    for vertex in mesh.vertices:h.update(np.asarray(vertex.co,dtype='<f4').tobytes())
    for edge in mesh.edges:h.update(np.asarray(edge.vertices,dtype='<i4').tobytes())
    for polygon in mesh.polygons:
        h.update(np.asarray(list(polygon.vertices)+[polygon.material_index,int(polygon.use_smooth)],dtype='<i4').tobytes())
    for layer in mesh.uv_layers:
        h.update(layer.name.encode())
        for value in layer.data:h.update(np.asarray(value.uv,dtype='<f4').tobytes())
    h.update(json.dumps([m.name if m else None for m in mesh.materials]).encode())
    return h.hexdigest()


def object_state(obj):
    return {'data':obj.data.name if obj.data else None,
            'matrix_basis':[list(row) for row in obj.matrix_basis],
            'parent':obj.parent.name if obj.parent else None,
            'collections':sorted(c.name for c in obj.users_collection),
            'instance_collection':obj.instance_collection.name if obj.instance_collection else None}


def fit_frame(obj,operation,clearance):
    if obj.get('fuente_componente')!=operation['expected_component'] or operation['expected_component']!='Component#34':
        raise ValueError('This reviewed operation is limited to Component#34 structural frames')
    if obj.parent or obj.modifiers or obj.data.has_custom_normals or len(obj.data.materials)!=1:
        raise ValueError('Unsupported frame data; inspect rather than simplify it automatically')
    original=obj.data
    mesh=original.copy();mesh.name=original.name+'_V04_Ajuste_Local'
    bm=bmesh.new();bm.from_mesh(mesh);bm.transform(obj.matrix_world)
    # Source stores face seams as duplicate vertices. Weld only this private copy;
    # loop UV layers survive the weld and the subsequent BMesh clipping operation.
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    if not all(e.is_manifold for e in bm.edges):
        bm.free();raise ValueError('Refuse trimming an originally open/nonmanifold component')
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    before_volume=abs(bm.calc_volume(signed=True));cuts=[]
    for plane in operation['planes']:
        n=Vector(plane['normal']);d=float(plane['offset'])+clearance
        if abs(n.length-1)>1e-6:raise ValueError('Plane normal must be unit length')
        depth=max(0,max(d-n.dot(v.co) for v in bm.verts))
        if depth>operation['max_cut_m'] or depth<=0:
            raise ValueError(f'Unreviewed cutting depth: {depth}')
        result=bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),
                                      dist=1e-7,plane_co=n*d,plane_no=n,clear_inner=True,clear_outer=False)
        border=[e for e in result['geom_cut'] if isinstance(e,bmesh.types.BMEdge) and e.is_boundary]
        if border:
            caps=bmesh.ops.holes_fill(bm,edges=border,sides=0)['faces']
            for f in caps:
                f.material_index=0;f.smooth=False
                # A flat structural cut gets a local planar UV projection. All
                # surviving original face UVs are interpolated by bisect_plane.
                tangent=n.orthogonal().normalized();bitangent=n.cross(tangent)
                for layer in bm.loops.layers.uv.values():
                    for loop in f.loops:loop[layer].uv=(loop.vert.co.dot(tangent),loop.vert.co.dot(bitangent))
        cuts.append({'normal':list(n),'offset_with_clearance_m':d,'cut_depth_m':depth})
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    if not all(e.is_manifold for e in bm.edges):raise ValueError('Cut did not retain a closed frame')
    after_volume=abs(bm.calc_volume(signed=True))
    if not 0.9<after_volume/before_volume<1:raise ValueError('Unexpected volume loss')
    for plane in operation['planes']:
        n=Vector(plane['normal']);d=float(plane['offset'])+clearance
        if min(n.dot(v.co)-d for v in bm.verts)<-5e-6:raise ValueError('Frame still crosses its reviewed plane')
    bm.transform(obj.matrix_world.inverted());bm.to_mesh(mesh);bm.free();mesh.update()
    obj.data=mesh
    return {'object':obj.name,'old_mesh':original.name,'new_mesh':mesh.name,
            'before_volume_m3':before_volume,'after_volume_m3':after_volume,
            'removed_fraction':1-after_volume/before_volume,'cuts':cuts}


def main():
    parser=argparse.ArgumentParser()
    for name in ['input','plan','output','evidence-dir']:parser.add_argument('--'+name,required=True,type=Path)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    source=args.input.resolve();output=args.output.resolve();evidence=args.evidence_dir.resolve()
    if output.exists() or output==source:raise ValueError('Output must be a new file')
    if evidence.exists() and any(evidence.iterdir()):raise ValueError('Evidence directory must be new/empty')
    plan=json.loads(args.plan.read_text(encoding='utf-8-sig'))
    if digest(source)!=plan['input_sha256'].lower():raise ValueError('Input hash differs from reviewed plan')
    if not 0<plan['clearance_m']<=.0002:raise ValueError('Unreviewed clearance')
    operations=[op for group in plan['groups'] for op in group['operations']]
    if len({op['object'] for op in operations})!=len(operations):raise ValueError('Repeated frame operation')
    evidence.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene
    objects={o.name:object_state(o) for o in bpy.data.objects}
    original_meshes={m.name:mesh_digest(m) for m in bpy.data.meshes}
    file_images={im.name:digest_bytes(im.packed_file.data) for im in bpy.data.images if im.source=='FILE' and im.packed_file}
    material_names=sorted(m.name for m in bpy.data.materials)
    protected={f.name:digest(f) for f in output.parent.iterdir() if f.is_file() and f.suffix.lower() in {'.blend','.skp'}} if output.parent.exists() else {}
    report={'input_sha256':digest(source),'plan_sha256':digest(args.plan),'groups':[]}
    for group in plan['groups']:
        changes=[fit_frame(bpy.data.objects[op['object']],op,plan['clearance_m']) for op in group['operations']]
        report['groups'].append({'id':group['id'],'changes':changes})
        print('GROUP_FITTED',group['id'],len(changes),flush=True)
    changed={op['object'] for op in operations}
    assert set(objects)==set(bpy.data.objects.keys())
    for name,state in objects.items():
        actual=object_state(bpy.data.objects[name]);expected=dict(state)
        if name in changed:expected['data']=actual['data']
        assert actual==expected,('Object changed unexpectedly',name)
    assert all(mesh_digest(bpy.data.meshes[name])==sha for name,sha in original_meshes.items())
    assert sorted(m.name for m in bpy.data.materials)==material_names
    assert {im.name:digest_bytes(im.packed_file.data) for im in bpy.data.images if im.source=='FILE' and im.packed_file}==file_images
    total_changed=int(scene.get('v04_objetos_ajustados',0))+len(changed)
    scene['estado_geometrico']=f'V04 PARCIAL: ajustes locales de {total_changed} montantes; interferencias heredadas y puertas pendientes'
    scene['validacion_UE5']='Pendiente; capsula provisional de referencia 0.70 m x 1.80 m'
    scene['v04_objetos_ajustados']=total_changed
    bpy.context.preferences.filepaths.save_version=0
    output.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output),compress=True,relative_remap=False)
    assert digest(source)==plan['input_sha256'].lower()
    assert all(digest(output.parent/name)==sha for name,sha in protected.items())
    report.update(output_sha256=digest(output),original_meshes_preserved=len(original_meshes),
                  objects_preserved=len(objects),changed_objects=sorted(changed),
                  packed_images=file_images,protected_files=protected)
    (evidence/'aplicacion.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    print('V04_SAVED',output.name,report['output_sha256'],flush=True)


def digest_bytes(data):
    return hashlib.sha256(bytes(data)).hexdigest()


if __name__=='__main__':main()
