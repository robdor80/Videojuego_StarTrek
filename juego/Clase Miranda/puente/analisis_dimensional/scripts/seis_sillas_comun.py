"""Explicit selection, world geometry and non-destructive validation helpers."""
import bpy, math, re, sys
from pathlib import Path
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent))
import pbr01_integrity as integrity

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL=ROOT.parent/'blender'/'Miranda_Puente_Sutherland_PBR_Manual_01.blend'
OUTPUT=ORIGINAL.with_stem(ORIGINAL.stem+'_Seis_Sillas_01')
MASTER_ANCHOR='Mesh.589_0.002'
TARGETS=[('P02_Xpos_Y-3.72934','Mesh.589_0.001'),('P03_Xpos_Y-1.73943','Mesh.589_0'),
         ('P04_Xneg_Y-1.80778','Mesh.589_0.003'),('P05_Xneg_Y-3.59266','Mesh.589_0.004'),
         ('P06_Xneg_Y-5.58256','Mesh.589_0.005')]
PATTERN=re.compile(r'Mesh\.(?:58[7-9]|59\d|60[0-2])_0(?:\.\d+)?$')
def chair_group(anchor):
    anchor=bpy.data.objects[anchor]
    return sorted([o for o in bpy.data.objects if o.type=='MESH' and PATTERN.fullmatch(o.name)
                   and (o.matrix_world.translation-anchor.matrix_world.translation).length<.001],key=lambda o:o.name)
def with_parents(meshes):
    parents={o.parent for o in meshes if o.parent}
    assert all(p.type=='EMPTY' and all(c in meshes for c in p.children) for p in parents)
    return sorted(parents,key=lambda o:o.name)+meshes
def bounds(objects):
    vs=[o.matrix_world@Vector(v) for o in objects if o.type=='MESH' for v in o.bound_box]
    return [[min(v[i] for v in vs) for i in range(3)],[max(v[i] for v in vs) for i in range(3)]]
def dimensions(objects):
    b=bounds(objects);return [b[1][i]-b[0][i] for i in range(3)]
def rigid_delta(source,target):
    s=bpy.data.objects[source].matrix_world;t=bpy.data.objects[target].matrix_world
    sl,sq,ss=s.decompose();tl,tq,ts=t.decompose()
    assert (ss-ts).length<1e-6 and s.determinant()>0 and t.determinant()>0
    rot=tq@sq.inverted()
    return Matrix.Translation(tl)@rot.to_matrix().to_4x4()@Matrix.Translation(-sl)
def bvh(o):
    dg=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dg);me=ev.to_mesh()
    vs=[ev.matrix_world@v.co for v in me.vertices];fs=[tuple(p.vertices) for p in me.polygons]
    result=BVHTree.FromPolygons(vs,fs,all_triangles=False,epsilon=0.0)
    ev.to_mesh_clear();return result
def floor_at(x,y):
    hit=bvh(bpy.data.objects['Circle_0']).ray_cast(Vector((x,y,.25)),Vector((0,0,-1)),1)
    assert hit[0] is not None, (x,y,'no floor')
    return list(hit[0])
def extra_snapshot():
    s=integrity.snapshot()
    s['assignments_all']={o.name:integrity.material_assignment(o) for o in bpy.data.objects if o.type=='MESH'}
    s['image_paths']={im.name:im.filepath for im in bpy.data.images}
    s['collections']={c.name:{'objects':sorted(o.name for o in c.objects),'children':sorted(ch.name for ch in c.children),
                            'hide_viewport':c.hide_viewport,'hide_render':c.hide_render} for c in bpy.data.collections}
    sc=bpy.context.scene
    s['scene']={'camera':sc.camera.name if sc.camera else None,'engine':sc.render.engine,
        'unit_system':sc.unit_settings.system,'unit_scale':sc.unit_settings.scale_length,
        'world':sc.world.name if sc.world else None}
    return s
