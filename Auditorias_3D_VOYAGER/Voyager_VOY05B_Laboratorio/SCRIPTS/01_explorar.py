import bpy,json,collections
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1]
def load(n):bpy.ops.wm.open_mainfile(filepath=str(R/'FUENTES'/n),load_ui=False,use_scripts=False)
def verts(o):return np.array([o.matrix_world@v.co for v in o.data.vertices],float)
load('VOY05A_Puente_Original_Inspeccion.blend')
c=np.array([1.1911309957504272,6.38205099105835,.7122955561927033]);basis=np.array([[0,1,0],[-1,0,0],[0,0,1]],float)
out=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 v=(verts(o)-c)@basis.T;lo=v.min(0);hi=v.max(0)
 if np.all(hi>[-.35,-1.4,-.2]) and np.all(lo<[.35,1.4,2.4]):
  out.append(dict(object=o.name,lo=lo.tolist(),hi=hi.tolist(),vertices=len(v),faces=len(o.data.polygons),materials=[m.name if m else None for m in o.data.materials]))
(R/'DATOS/BR03_contexto_exploracion.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print('BR03 nearby',json.dumps(out),flush=True)
print('images',json.dumps([dict(name=i.name,path=i.filepath,packed=bool(i.packed_file),size=list(i.size)) for i in bpy.data.images]),flush=True)
load('VOY05A_Coleccion_Original_Inspeccion.blend')
for name in ['Mesh4','Mesh5','Mesh6','Mesh9','Mesh11','Mesh81','Mesh12','Mesh13','Mesh18']:
 o=bpy.data.objects[name];v=verts(o);m=o.data;m.calc_loop_triangles();t=np.array([x.vertices[:] for x in m.loop_triangles]);tr=v[t];lo=v.min(0);hi=v.max(0)
 n=np.cross(tr[:,1]-tr[:,0],tr[:,2]-tr[:,0]);area=np.linalg.norm(n,axis=1)/2;n=np.divide(n,2*area[:,None],out=np.zeros_like(n),where=area[:,None]>1e-12)
 print('ROOM',name,'bounds',lo,hi,'faces',len(m.polygons),'horizontal',[(z,float(area[(abs(n[:,2])>.99)&(abs(tr.mean(1)[:,2]-z)<.01)].sum())) for z in sorted(set(np.round(tr.mean(1)[abs(n[:,2])>.99,2],3)))],flush=True)
