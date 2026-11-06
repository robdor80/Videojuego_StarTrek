import sys,json,csv,collections,math
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import *
v,t,ids,obs=load('obj');tri=v[t]*1.1;names=np.array([o['name'] for o in obs]);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);area=np.linalg.norm(cross,axis=1)/2;n=np.divide(cross,2*area[:,None],out=np.zeros_like(cross),where=area[:,None]>1e-12)
floor_names=[o['name'] for o in obs if 'Voygray'in o['materials']]+['Mesh_1856','Mesh_1787','Object_75']
rows=[];plots=[]
for k,o in enumerate(obs):
 lo=np.array(o['bounds_min'])*1.1;hi=np.array(o['bounds_max'])*1.1
 if hi[2]<0 or lo[2]>1.6:continue
 sel=ids==k;count=int(sel.sum());flat=sel&(np.abs(n[:,2])>.999)&(area>1e-10);levels=[]
 for z in sorted(set(np.round(tri[flat].mean(axis=1)[:,2],3))):
  mask=flat&(np.abs(tri.mean(axis=1)[:,2]-z)<.00051);q=tri[mask]
  levels.append(dict(z_m=float(z),area_m2=float(area[mask].sum()),triangles=int(mask.sum()),min_m=q.min(axis=(0,1)).tolist(),max_m=q.max(axis=(0,1)).tolist(),up=int((n[mask,2]>0).sum()),down=int((n[mask,2]<0).sum())))
 if o['name'] in floor_names:
  plots.extend(dict(object=o['name'],z=float(q.mean(axis=0)[2]),points=q.tolist()) for q in tri[flat] if q.mean(axis=0)[2]<.9)
 rows.append(dict(name=o['name'],floor_candidate=o['name'] in floor_names,bounds=[lo.tolist(),hi.tolist()],triangles=count,degenerate_area_below_1e10=int((sel&(area<1e-10)).sum()),levels=levels,materials=o['materials']))
step=next(x for x in rows if x['name']=='Mesh_1856');print('STEP_LEVELS',json.dumps(step['levels']),flush=True)
# Welded geometry diagnostics, never deletes surfaces; count exact/coincident/near-degenerate.
steptri=tri[ids==names.tolist().index('Mesh_1856')];qv=np.round(steptri.reshape((-1,3))/1e-6).astype(np.int64);_,ix=np.unique(qv,axis=0,return_inverse=True);edges=np.sort(np.concatenate([ix.reshape(-1,3)[:,[0,1]],ix.reshape(-1,3)[:,[1,2]],ix.reshape(-1,3)[:,[2,0]]]),axis=1);_,counts=np.unique(edges,axis=0,return_counts=True)
faces=np.sort(ix.reshape(-1,3),axis=1);_,fc=np.unique(faces,axis=0,return_counts=True)
(R/'DATOS/topografia_objetos.json').write_text(json.dumps(dict(scale=1.1,frame='VOY02 A bridge frame, metres, no rear-origin translation',objects=rows,step_topology=dict(boundary_edges=int((counts==1).sum()),nonmanifold_edges=int((counts>2).sum()),duplicate_triangle_excess=int((fc-1).sum()),note='Welded at 1um for counting; original geometry retained.'),floor_names=floor_names),indent=2,ensure_ascii=False),encoding='utf8')
(R/'DATOS/planos_soporte_plot.json').write_text(json.dumps(plots),encoding='utf8')
np.savez_compressed(R/'DATOS/puente_abierto.npz',triangles=tri,labels=names[ids],normals=n,area=area)
# Explicit complete source door poses from VOY02, all leaves present.
ds=json.loads((R/'DATOS/puertas_medidas.json').read_text())
for d in ds:
 tri[np.isin(names[ids],d['leafA'])]+=np.array(d['leafA_vector'])*1.1;tri[np.isin(names[ids],d['leafB'])]+=np.array(d['leafB_vector'])*1.1
np.savez_compressed(R/'DATOS/puente_abierto.npz',triangles=tri,labels=names[ids],normals=n,area=area)
