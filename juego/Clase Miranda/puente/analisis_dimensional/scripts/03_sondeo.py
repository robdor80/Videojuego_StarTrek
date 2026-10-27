import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
trees={}
for o in bpy.data.objects:
    if o.type=='MESH':
        trees[o.name]=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
def ray(origin,direction,limit=100):
    hits=[];d=Vector(direction)
    for n,t in trees.items():
        start=Vector(origin);total=0
        for _ in range(50):
            p,no,face,dist=t.ray_cast(start,d,limit-total)
            if p is None:break
            total+=(p-start).length
            hits.append({'object':n,'point':[round(x,6) for x in p],'normal':[round(x,5) for x in no],'distance':round(total,6),'face':face})
            start=p+d*0.0001;total+=0.0001
    return sorted(hits,key=lambda h:h['distance'])
probes={}
points={'central':(0,-5.5),'capitan':(0,-1.8),'podio_libre':(0,-3),'lateral_d':(5.3,-3.7),'puesto_d':(4.7,-3.7),'pasillo_d':(3.7,-3.7),'posterior':(0,-8.5),'frontal':(0,0.6),'turbo_centro':(-8.12772,-8.71576),'acceso_turbo':(-6.05,-8.33),'puerta_lateral_d':(5.7,-8.33),'puerta_frontal_d':(5.5,0.87)}
for n,(x,y) in points.items():probes[n]=ray((x,y,-0.5),(0,0,1),10)
for z in [0.1,0.7,1.5,1.773,2.5,3,3.8,4,4.5]:
    probes[f'puerta_turbo_z{z}']=ray((-8.12772,-8.33,z),(1,0,0),4)
    probes[f'puerta_frontal_z{z}']=ray((5.5,-2,z),(0,1,0),5)
    probes[f'puerta_lateral_z{z}']=ray((4,-8.33,z),(1,0,0),4)
    probes[f'turbo_ejeX_z{z}']=ray((-8.12772,-8.71576,z),(-1,0,0),4)+ray((-8.12772,-8.71576,z),(1,0,0),4)
    probes[f'turbo_ejeY_z{z}']=ray((-8.12772,-8.71576,z),(0,-1,0),4)+ray((-8.12772,-8.71576,z),(0,1,0),4)
(ROOT/'datos/sondeos.json').write_text(json.dumps(probes,indent=2),encoding='utf-8')
names=['Circle_0','Circle.001_0','Plane.001_0','Plane.017_0','Plane.018_0','Plane.019_0','Plane.039_0','Plane.026_0','Plane.030_0','Plane.034_0','Plane.007_0','Plane.004_0','Plane.005_0','Plane.028_0','Plane.040_0','Plane.041_0','Plane.042_0','Cube.002_0','Cube_0','Mesh.453_0']
faces={}
for name in names:
    o=bpy.data.objects[name]
    faces[name]=[{'face':p.index,'vertices':[[round(c,6) for c in o.matrix_world@o.data.vertices[i].co] for i in p.vertices]} for p in o.data.polygons]
(ROOT/'datos/caras_relevantes.json').write_text(json.dumps(faces,indent=2),encoding='utf-8')
for n,hs in probes.items():
    if n in points:print(n,[(h['object'],h['point']) for h in hs])
