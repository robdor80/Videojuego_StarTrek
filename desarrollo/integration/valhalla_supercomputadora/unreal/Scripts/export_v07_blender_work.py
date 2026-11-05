"""Blender: recreate a linked work copy from the final Unreal geometry export.

The Unreal project remains authoritative for collision, triggers and gameplay.
Packed V04E materials are read without changing the original Blender file.
"""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Matrix,Quaternion,Vector


def main():
    parser=argparse.ArgumentParser()
    for name in ('geometry','source-blend','completion','output'):parser.add_argument('--'+name,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    target=Path(args.output).resolve();assert not target.exists()
    data=json.loads(Path(args.geometry).read_text(encoding='utf8'))
    completion=json.loads(Path(args.completion).read_text(encoding='utf8'))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(Path(args.source_blend).resolve()),link=False) as (source,destination):
        destination.materials=sorted(source.materials)
    originals=destination.materials
    mats={}
    def material(path):
        if path not in mats:
            name=path.rsplit('/',1)[-1].split('.')[0]
            if name.startswith('M_') and name[2:].isdigit() and int(name[2:])<len(originals):
                mats[path]=originals[int(name[2:])]
            else:mats[path]=bpy.data.materials.new(name)
        return mats[path]
    meshes={}
    for key,part in data['meshes'].items():
        mesh=bpy.data.meshes.new(key)
        mesh.from_pydata([(p[0]/100,-p[1]/100,p[2]/100) for p in part['vertices']],[],
                         [t['v'] for t in part['triangles']])
        for name in part['materials']:mesh.materials.append(material(name))
        uv=mesh.uv_layers.new(name='UVMap')
        for poly,tri in zip(mesh.polygons,part['triangles']):
            poly.material_index=tri['material']
            for li,val in zip(poly.loop_indices,tri['uv']):uv.data[li].uv=val
        for poly in mesh.polygons:poly.use_smooth=True
        mesh.normals_split_custom_set([(n[0],-n[1],n[2]) for t in part['triangles'] for n in t['n']])
        meshes[key]=mesh
    conversion=Matrix.Diagonal((.01,-.01,.01,1))
    groups={}
    animated=0
    for row in data['instances']:
        key=row['actor']
        if key not in groups:
            groups[key]=bpy.data.collections.new(key);bpy.context.scene.collection.children.link(groups[key])
        obj=bpy.data.objects.new(row['component']+'_'+str(row['index']),meshes[row['mesh']]);groups[key].objects.link(obj)
        q=row['rotation'];matrix=Matrix.LocRotScale(Vector(row['location']),Quaternion((q[3],*q[:3])),Vector(row['scale']))
        obj.matrix_world=conversion@matrix@conversion.inverted()
        for slot,mat in zip(obj.material_slots,row.get('overrides',[])):
            if mat:slot.link='OBJECT';slot.material=material(mat)
        if row['component'] not in ('LeftLeaf','RightLeaf'):continue
        closest=min(completion['doors'],key=lambda d:(Vector(d['root'])-Vector(row['location'])).length)
        if (Vector(closest['root'])-Vector(row['location'])).length>150:continue
        obj.name=closest['id']+'_'+row['component']
        left=row['component']=='LeftLeaf'
        delta=Matrix.Rotation(math.radians(closest['yaw']),3,'Z')@Vector((-35,-100 if left else 100,0))
        closed=obj.location.copy();opened=closed+Vector((delta.x/100,-delta.y/100,delta.z/100))
        for frame,position in ((1,closed),(60,opened),(120,closed)):
            obj.location=position;obj.keyframe_insert(data_path='location',frame=frame)
        animated+=1
    assert animated==12,animated
    bpy.context.scene.frame_set(1);bpy.context.scene.frame_end=120
    bpy.context.scene['V07']='Final Unreal work copy; six doors animated for visual inspection. Runtime uses AVHAutomaticDoor.'
    bpy.ops.file.pack_all()
    target.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target))
    print('WORK_COPY',len(data['instances']),'linked placements;',animated,'animated leaves;',len(mats),'materials',flush=True)


if __name__=='__main__':main()
