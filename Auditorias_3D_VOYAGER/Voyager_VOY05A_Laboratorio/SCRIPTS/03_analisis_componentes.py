import json,collections,hashlib
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1]
data=np.load(R/'DATOS/coleccion_geometria.npz');v=data['vertices'];t=data['triangles'];ids=data['object_ids'];mat=data['material_ids'];a=json.loads((R/'DATOS/coleccion_auditoria.json').read_text());out=[]
for i,o in enumerate(a['objects']):
 tri=t[ids==i];verts=np.unique(tri);p=v[verts];lo=p.min(0);hi=p.max(0)
 # Weld at 10 micrometres in world coordinates, then connected components.
 _,wi=np.unique(np.round(p/1e-5).astype(np.int64),axis=0,return_inverse=True);parents=list(range(max(wi)+1));local=np.searchsorted(verts,tri);wt=wi[local]
 def root(x):
  while parents[x]!=x:parents[x]=parents[parents[x]];x=parents[x]
  return x
 def union(x,y):
  x=root(x);y=root(y)
  if x!=y:parents[y]=x
 for x,y,z in wt:union(x,y);union(x,z)
 labels=np.array([root(x) for x in wi]);groups=collections.defaultdict(list)
 for k,label in enumerate(labels):groups[label].append(k)
 components=[]
 for k,ix in enumerate(sorted(groups.values(),key=lambda x:-len(x))):
  pp=p[ix];components.append(dict(index=k,vertices=len(ix),lo=pp.min(0).tolist(),hi=pp.max(0).tolist(),size=np.ptp(pp,axis=0).tolist(),center=((pp.min(0)+pp.max(0))/2).tolist()))
 out.append(dict(object=o['object'],components=components))
(R/'DATOS/coleccion_componentes.json').write_text(json.dumps(out,indent=2),encoding='utf8')
for o in out:
 if o['object'] in ['Mesh14','Mesh25','Mesh26','Mesh27','Mesh28','Mesh51','Mesh53','Mesh54','Mesh55','Mesh57','Mesh93']:
  print(o['object'],len(o['components']),[(x['index'],x['vertices'],[round(y,4) for y in x['size']],[round(y,4) for y in x['center']]) for x in o['components'] if x['vertices']>5])
