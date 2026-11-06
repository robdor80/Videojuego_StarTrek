import sys,json
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World
from geom import point_tri_sq
w=World();route=json.loads((R/'DATOS/barridos_resultados.json').read_text())['results'][2];q=w.tri[w.support_mask];ix=np.where(w.support_mask)[0];bvh=BVHTree.FromPolygons(q.reshape(-1,3).tolist(),np.arange(len(q)*3).reshape(-1,3).tolist(),all_triangles=True)
for i in [363,364,365,395]:
 for u in [0,.5,1]:
  p=np.array(route['foot_points'][i])*(1-u)+np.array(route['foot_points'][i+1])*u;c=p+[0,0,.35];loc,n,k,dist=bvh.find_nearest(c);j=ix[k];print('SUPPORT',i,u,'p',p,'gap',dist-.35,'up',(c[2]-loc.z)/dist,'name',w.labels[j],'triZ',w.lo[j,2],w.hi[j,2], 'center',c[2])
profiles=json.loads((R/'DATOS/perfiles_escaleras.json').read_text())['profiles']
for pr in profiles:
 vals=[]
 for row in pr['rows']:
  if not row['state']['valid']:continue
  c=np.array(row['state']['foot'])+[0,0,.35];loc,n,k,dist=bvh.find_nearest(c);vals.append((c[2]-loc.z)/dist)
 print('STAIR_UP',pr['id'],min(vals))
