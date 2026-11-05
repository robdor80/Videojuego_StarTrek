"""Blender background: localized construction from an immutable UE V07 export.

--geometry exported.json --accesses v07_memory_accesses.json --output new-directory
No source assets are overwritten. Output contains a reproducible import manifest
and a Blender work file with linked source meshes and the six new modules.
Coordinates in the manifest are UE centimetres; Blender uses metres, Y reversed.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Quaternion, Vector


def half(poly, axis, value, less):
    """Clip corner records (position, UV, normal) with interpolated attributes."""
    out = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        da = a[axis] - value
        db = b[axis] - value
        ina = da <= 1e-7 if less else da >= -1e-7
        inb = db <= 1e-7 if less else db >= -1e-7
        if ina:
            out.append(a)
        if ina != inb:
            out.append(a + (b - a) * (da / (da - db)))
    return out


def subtract_box(poly, bounds):
    outside = []
    inside = poly
    for axis, lo, hi in bounds:
        for value, less in ((lo, False), (hi, True)):
            if not inside:
                return outside, False
            piece = half(inside, axis, value, not less)
            if len(piece) >= 3:
                outside.append(piece)
            inside = half(inside, axis, value, less)
    return outside, len(inside) >= 3


def area(poly):
    return sum(np.linalg.norm(np.cross(poly[i][:3]-poly[0][:3],
                                       poly[i+1][:3]-poly[0][:3]))/2
               for i in range(1, len(poly)-1))


def new_part(name):
    return dict(name=name, vertices=[], triangles=[], materials=[])


def emit(part, poly, material, to_world=None, orient_for_unreal=False):
    if len(poly) < 3 or area(poly) < 1e-5:
        return
    if material not in part['materials']:
        part['materials'].append(material)
    slot = part['materials'].index(material)
    for i in range(1, len(poly)-1):
        corners = [poly[0], poly[i], poly[i+1]]
        if orient_for_unreal:
            cross=np.cross(corners[1][:3]-corners[0][:3],corners[2][:3]-corners[0][:3])
            if np.dot(cross,sum(c[5:8] for c in corners))>0:corners[1],corners[2]=corners[2],corners[1]
        indices, normals, uvs = [], [], []
        for corner in corners:
            p, n = corner[:3], corner[5:8]
            if to_world:
                p = np.array(to_world @ Vector(p))
                n = np.array(to_world.to_3x3() @ Vector(n))
            n = n / max(np.linalg.norm(n), 1e-9)
            indices.append(len(part['vertices']))
            part['vertices'].append(p.tolist())
            normals.append(n.tolist())
            uvs.append(corner[3:5].tolist())
        part['triangles'].append(dict(v=indices, n=normals, uv=uvs, material=slot))


def cube(part, lo, hi, mat, transform):
    pts = np.array([[hi[k] if i & (1 << k) else lo[k] for k in range(3)] for i in range(8)])
    for ids in ((0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)):
        n = np.cross(pts[ids[1]]-pts[ids[0]], pts[ids[2]]-pts[ids[0]])
        n /= np.linalg.norm(n)
        poly = [np.r_[pts[j], uv, n] for j, uv in zip(ids, ((0,0),(1,0),(1,1),(0,1)))]
        emit(part, poly, mat, transform,orient_for_unreal=True)



def complementary_surface(coverage,depth=400):
    import shapely
    from shapely.geometry import Polygon
    rectangle=Polygon(((-70,-90),(depth,-90),(depth,90),(-70,90)))
    existing=[Polygon(tri) for tri in coverage if Polygon(tri).area>.01]
    missing=rectangle.difference(shapely.union_all(existing,grid_size=.001))
    return [list(np.array(t.exterior.coords)[:-1]) for t in shapely.constrained_delaunay_triangles(missing).geoms]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--geometry',required=True)
    parser.add_argument('--accesses',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--dependency-dir',help='Optional directory containing Shapely for fast surface union')
    parser.add_argument('--source-blend',help='Optional V04E original, read only, to recover its packed materials')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if args.dependency_dir:sys.path.insert(0,args.dependency_dir)
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=False)
    data=json.loads(Path(args.geometry).read_text(encoding='utf-8-sig'))
    doors=json.loads(Path(args.accesses).read_text(encoding='utf-8-sig'))
    white='/Game/Valhalla/Materials/M_099.M_099'
    blue='/Game/Valhalla/Materials/M_061.M_061'
    manifest=dict(schema=1,remove=[],parts=[],doors=[],metrics=[])
    frames=[]
    for d in doors:
        yaw=math.radians(d['outward_yaw']); x,y,_=d['wall_face_center_cm']
        t=Matrix.Translation((x,y,37)) @ Matrix.Rotation(yaw,4,'Z')
        frames.append((t,t.inverted()))
        root=t@Vector((-20,0,0))
        manifest['doors'].append(dict(id=d['id'],root=list(root),yaw=d['outward_yaw']))
    # World-space source arrays are evaluated once; all unaffected instances remain linked.
    sources=[]
    for row in data['instances']:
        mesh=data['meshes'][row['mesh']]
        q=row['rotation']; t=Matrix.LocRotScale(Vector(row['location']),Quaternion((q[3],*q[:3])),Vector(row['scale']))
        v=np.array(mesh['vertices']); m=np.array(t)
        world=v@m[:3,:3].T+m[:3,3]
        sources.append((row,mesh,t,world))
    replacements=[new_part(d['id']+'_Architecture') for d in doors]
    horizontal=[[] for _ in doors]
    removed=0
    for row,mesh,t,world in sources:
        # Direct mesh actors include D01-D04 and the authored safety closures.
        # They are displayed in the work copy but never partitioned as architecture.
        if row['index']<0:continue
        changed=False;part=None;new_polys=[]
        # Accesses are disjoint; a source placement may span several accesses.
        candidates=[]
        for j,(frame,inv) in enumerate(frames):
            m=np.array(inv);local=world@m[:3,:3].T+m[:3,3]
            lo=local.min(0);hi=local.max(0)
            if all(lo[k]<[410,195,320][k] and hi[k]>[-75,-195,-10][k] for k in range(3)):
                candidates.append((j,local))
        if not candidates: continue
        normal_matrix=np.array(t.to_3x3().inverted().transposed())
        polys=[]
        for tr in mesh['triangles']:
            normals=np.array(tr['n'])@normal_matrix.T
            poly=[np.r_[world[v],uv,n] for v,uv,n in zip(tr['v'],tr['uv'],normals)]
            polys.append((poly,mesh['materials'][tr['material']]))
        for j,local in candidates:
            frame,inv=frames[j];m=np.array(inv)
            next_polys=[]
            for poly,mat in polys:
                lp=[np.r_[np.array(inv@Vector(c[:3])),c[3:5],m[:3,:3]@c[5:8]] for c in poly]
                z=[c[2] for c in lp]
                if max(z)-min(z)<.02 and (abs(z[0])<.05 or abs(z[0]-312.635)<.05):
                    horizontal[j].append((z[0],[c[:2] for c in lp]))
                pieces=[lp]
                for bounds in (((0,-70,doors[j].get('depth_cm',400)),(1,-90,90),(2,.05,312.58)),
                               ((0,-65,-15),(1,-190,190),(2,.05,230))):
                    keep=[]
                    for piece in pieces:
                        result,cut=subtract_box(piece,bounds)
                        if cut and area(piece)-sum(area(p) for p in result)>1e-4:changed=True
                        keep.extend(result)
                    pieces=keep
                for piece in pieces:
                    wp=[np.r_[np.array(frame@Vector(c[:3])),c[3:5],np.array(frame.to_3x3())@c[5:8]] for c in piece]
                    next_polys.append((wp,mat))
            polys=next_polys
        if changed:
            manifest['remove'].append(row);removed+=1
            for poly,mat in polys:emit(replacements[candidates[0][0]],poly,mat)
    manifest['parts'] += [p for p in replacements if p['triangles']]
    print('PORTALS',removed,'placements; constructing complementary surfaces',flush=True)
    for j,d in enumerate(doors):
        frame,_=frames[j];shell=new_part(d['id']+'_Enclosure')
        depth=d.get('depth_cm',400);connected=d.get('connects_existing_corridor',False)
        side_end=depth if connected else depth+8
        # Two sides, back and lintel. The entry and door pockets remain unobstructed.
        cube(shell,(0,-98,0),(side_end,-90,312.635),blue,frame)
        cube(shell,(0,90,0),(side_end,98,312.635),blue,frame)
        if not connected:cube(shell,(depth,-90,0),(depth+8,90,312.635),blue,frame)
        cube(shell,(-10,-90,230),(0,90,312.635),white,frame)
        manifest['parts'].append(shell)
        metrics=dict(id=d['id'],floor_area_cm2=0,ceiling_area_cm2=0)
        for ceiling,z in ((False,0),(True,312.635)):
            coverage=[tri for height,tri in horizontal[j] if abs(height-z)<.05]
            pieces=complementary_surface(coverage,depth)
            part=new_part(d['id']+('_Ceiling' if ceiling else '_Floor'))
            for poly in pieces:
                corners=[np.r_[p,z, p/100, (0,0,-1 if ceiling else 1)] for p in poly]
                if ceiling:corners.reverse()
                emit(part,corners,white,frame,orient_for_unreal=True)
                metrics['ceiling_area_cm2' if ceiling else 'floor_area_cm2']+=area(corners)
            if part['triangles']:manifest['parts'].append(part)
        manifest['metrics'].append(metrics)
    manifest['materials']=sorted({m for p in manifest['parts'] for m in p['materials']})
    (out/'completion.json').write_text(json.dumps(manifest,separators=(',',':')),encoding='utf8')
    # A work copy of the actual UE geometry. Linked meshes preserve batching semantics.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    originals=[]
    if args.source_blend:
        with bpy.data.libraries.load(str(Path(args.source_blend).resolve()),link=False) as (source,target):
            target.materials=sorted(source.materials)
        originals=target.materials
    materials={}
    for m in {v for mesh in data['meshes'].values() for v in mesh['materials']}:
        name=m.rsplit('/',1)[-1].split('.')[0]
        index=int(name[2:]) if name.startswith('M_') and name[2:].isdigit() else -1
        material=originals[index] if 0<=index<len(originals) else bpy.data.materials.new(m)
        if not originals:material.diffuse_color=(.65,.69,.73,1)
        materials[m]=material
    def blender_mesh(part,name):
        mesh=bpy.data.meshes.new(name)
        mesh.from_pydata([(v[0]/100,-v[1]/100,v[2]/100) for v in part['vertices']],[],[t['v'] for t in part['triangles']])
        for mat in part['materials']:mesh.materials.append(materials[mat])
        for poly,tr in zip(mesh.polygons,part['triangles']):poly.material_index=tr['material']
        uv=mesh.uv_layers.new(name='UVMap')
        for poly,tr in zip(mesh.polygons,part['triangles']):
            for li,val in zip(poly.loop_indices,tr['uv']):uv.data[li].uv=val
        for poly in mesh.polygons:poly.use_smooth=True
        mesh.normals_split_custom_set([(n[0],-n[1],n[2]) for t in part['triangles'] for n in t['n']])
        return mesh
    meshes={key:blender_mesh(mesh,key) for key,mesh in data['meshes'].items()}
    removed_ids={(r['actor'],r['component'],r['index']) for r in manifest['remove']}
    convert=Matrix.Diagonal((.01,-.01,.01,1))
    source_collection=bpy.data.collections.new('V07_Arquitectura_conservada');bpy.context.scene.collection.children.link(source_collection)
    for row,mesh,t,world in sources:
        if (row['actor'],row['component'],row['index']) in removed_ids:continue
        obj=bpy.data.objects.new(row['component']+'_'+str(row['index']),meshes[row['mesh']]);source_collection.objects.link(obj)
        obj.matrix_world=convert@t@convert.inverted()
    additions=bpy.data.collections.new('V07_Seis_accesos_funcionales');bpy.context.scene.collection.children.link(additions)
    for part in manifest['parts']:
        obj=bpy.data.objects.new(part['name'],blender_mesh(part,part['name']));additions.objects.link(obj)
    for d in manifest['doors']:
        for sign in (-1,1):
            bpy.ops.mesh.primitive_cube_add(size=1)
            obj=bpy.context.object;obj.name=d['id']+('_LeftLeaf' if sign<0 else '_RightLeaf')
            t=Matrix.Translation(d['root'])@Matrix.Rotation(math.radians(d['yaw']),4,'Z')
            for f,x,y in ((1,0,sign*45),(60,-35,sign*145)):
                p=t@Vector((x,y,115));obj.location=(p.x/100,-p.y/100,p.z/100);obj.keyframe_insert(data_path='location',frame=f)
            obj.rotation_euler.z=-math.radians(d['yaw']);obj.dimensions=(.06,.896,2.292);obj.data.materials.append(materials[blue])
    bpy.context.scene.frame_set(1);bpy.context.scene['source_geometry']=Path(args.geometry).name
    bpy.context.scene['note']='V07 work copy. Runtime doors and original D01-D04 remain in the Unreal project.'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'Sala_Supercomputadora_V07_Funcional.blend'))
    print('COMPLETION',removed,'source instances replaced;',len(manifest['parts']),'parts;',manifest['metrics'],flush=True)


if __name__=='__main__':main()
