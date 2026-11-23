import json,collections,sys
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];label=sys.argv[1] if len(sys.argv)>1 else 'coleccion';data=np.load(R/'DATOS'/f'{label}_geometria.npz');tri=data['vertices'][data['triangles']];ids=data['object_ids'];obs=json.loads((R/'DATOS'/f'{label}_auditoria.json').read_text())['objects'];out=[]
if label=='puente_obj':ids=np.zeros(len(tri),int);obs=[{'object':'PUENTE_AGREGADO'}]
for i,o in enumerate(obs):
 tr=tri[ids==i];p,wi=np.unique(np.round(tr.reshape(-1,3)/1e-5).astype(np.int64),axis=0,return_inverse=True);p=p*1e-5;wt=wi.reshape(-1,3);edges=collections.Counter(tuple(sorted((int(a),int(b)))) for f in wt for a,b in zip(f,np.roll(f,-1)) if a!=b);boundary=[e for e,n in edges.items() if n==1];adj=collections.defaultdict(set)
 for a,b in boundary:adj[a].add(b);adj[b].add(a)
 seen=set();parts=[]
 for a in sorted(adj):
  if a in seen:continue
  queue=[a];seen.add(a);ix=[]
  while queue:
   b=queue.pop();ix.append(b)
   for c in adj[b]:
    if c not in seen:seen.add(c);queue.append(c)
  pp=p[ix];lo=pp.min(0);hi=pp.max(0);center=(lo+hi)/2;mean=pp.mean(0);_,sv,vh=np.linalg.svd(pp-mean,full_matrices=False);normal=vh[-1];normal[abs(normal)<1e-6]=0
  if normal[np.argmax(abs(normal))]<0:normal=-normal
  tangent=np.cross([0,0,1],normal);tangent/=max(np.linalg.norm(tangent),1e-12);width=float(np.ptp(pp@tangent));height=float(np.ptp(pp[:,2]));planarity=float(abs((pp-mean)@normal).max());degs=collections.Counter(len(adj[x]) for x in ix)
  segments=[[p[a].tolist(),p[b].tolist()] for a,b in boundary if a in set(ix)]
  parts.append(dict(id=f'L_{o["object"]}_{len(parts):02}',object=o['object'],vertices=len(ix),degrees=dict(degs),lo=lo.tolist(),hi=hi.tolist(),points=pp.tolist(),segments=segments,center=center.tolist(),normal=normal.tolist(),tangent=tangent.tolist(),width=width,height=height,plane_error=planarity,vertical=abs(normal[2])<.05,cycle=all(len(adj[x])==2 for x in ix)))
 out.extend(parts)
(R/'DATOS'/('bordes_abiertos.json' if label=='coleccion' else 'bordes_'+label+'.json')).write_text(json.dumps(out,indent=2,default=lambda x:x.item()),encoding='utf8')
for o in obs:
 loops=[x for x in out if x['object']==o['object'] and x['height']>.4 and (label!='puente_obj' or (x['height']>1.2 and x['width']>.5 and x['width']<4 and x['height']<3 and x['plane_error']<.03 and x['vertical']))]
 print(o['object'],[(x['id'],x['vertices'],round(x['width'],4),round(x['height'],4),[round(y,4) for y in x['normal']],round(x['plane_error'],5),round(x['lo'][2],4),x['cycle']) for x in loops])
