import sys,json
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World
from geom import capsule_distance,point_tri_sq,segment_segment_sq
from sweepgeom import swept_distance,intersects
results=json.loads((R/'DATOS/barridos_resultados.json').read_text())['results'];route=next(r for r in results if r['id']=='CENTRO_A_PASARELA');w=World();i=route['sweep_failures'][0]['segment'];p=np.array(route['foot_points'][i]);q=np.array(route['foot_points'][i+1]);ix=np.where(w.labels=='Mesh_1944')[0];d=swept_distance(w.tri[ix],p,q);bad=ix[d<0];print('SEGMENT',i,p,q,'BAD',len(bad))
for k in bad[:5]:
 t=w.tri[k:k+1];print('TRI',int(k),t.tolist(),'POSE',capsule_distance(t,p,1.6,.35)-.35,capsule_distance(t,q,1.6,.35)-.35)
 corners=np.array([p+[0,0,.35],p+[0,0,1.25],q+[0,0,1.25],q+[0,0,.35]])
 for a,b in [(0,1),(1,2),(2,3),(3,0)]:print('EDGEQUAD',a,b,intersects(corners[a],corners[b],t))
 for ids in [(0,1,2),(0,2,3)]:
  qt=corners[list(ids)][None]
  for j in range(3):print('EDGETRI',ids,j,intersects(t[0,j],t[0,(j+1)%3],qt),'DIST',point_tri_sq(t[0,j],qt))
proto=json.loads((R/'DATOS/prototipo_conjunto.json').read_text());data=np.load(R/'DATOS/prototipo_geometria.npz');T=np.array(proto['bridge_translation']);wf=World(data['triangles']-T,data['labels']);x,y=1.3102440953254701,8.420256090164186
for dx,dy in [(0,0),(0,1e-6),(0,-1e-6),(1e-6,0),(-1e-6,0),(0,1e-5),(0,-1e-5)]:print('SEAM',dx,dy,wf.floor(x+dx,y+dy))
for label in ['AD_PUENTE','PASILLO_PRINCIPAL']:
 ix=np.where((wf.labels==label)&wf.flat)[0];print('SEAM_GEOM',label,len(ix),wf.lo[ix].min(axis=0).tolist() if len(ix) else None,wf.hi[ix].max(axis=0).tolist() if len(ix) else None)
