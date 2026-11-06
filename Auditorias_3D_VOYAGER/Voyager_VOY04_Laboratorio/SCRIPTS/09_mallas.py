import sys,json,ast,collections,numpy as np
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import Env
parsed=ast.parse((R/'REFERENCIAS/VOY02_10_funcional.py').read_text());exec(compile(ast.Module(body=[x for x in parsed.body if isinstance(x,ast.FunctionDef) and x.name in ['tree','exact_overlap']],type_ignores=[]),'<SAT_VOY02>','exec'))
def classify(A,B,eps=.00001):
 na=np.cross(A[:,1]-A[:,0],A[:,2]-A[:,0]);nb=np.cross(B[:,1]-B[:,0],B[:,2]-B[:,0]);na/=np.maximum(np.linalg.norm(na,axis=1)[:,None],1e-20);nb/=np.maximum(np.linalg.norm(nb,axis=1)[:,None],1e-20);da=np.einsum('nvi,ni->nv',A-B[:,0,None,:],nb);db=np.einsum('nvi,ni->nv',B-A[:,0,None,:],na)
 return (da.min(1)<-eps)&(da.max(1)>eps)&(db.min(1)<-eps)&(db.max(1)>eps)
result=[]
for c in json.loads((R/'DATOS/ajustes_elegidos.json').read_text()):
 e=Env().adapted(c['drop'],.18).rail(.4);moving=e.tri[e.chair];mn=e.names[e.chair];fixed=e.tri[~e.chair];fn=e.names[~e.chair];lo=moving.min((0,1))-[.1,.5,.05];hi=moving.max((0,1))+[.1,.1,.05];near=np.all(fixed.max(1)>=lo,axis=1)&np.all(fixed.min(1)<=hi,axis=1);fixed=fixed[near];fn=fn[near];ft=tree(fixed);poses=[]
 for D in np.linspace(0,.4,81):
  q=moving+[0,-D,0];raw=tree(q).overlap(ft);pairs=[]
  # Reuse exact SAT on the small set of broadphase pairs, retaining original indices.
  if raw:
   a=np.array(raw);subA=q[a[:,0]];subB=fixed[a[:,1]]
   # SAT pair-wise, rather than cross product of candidate lists.
   ea=np.roll(subA,-1,1)-subA;eb=np.roll(subB,-1,1)-subB;na=np.cross(ea[:,0],ea[:,1]);nb=np.cross(eb[:,0],eb[:,1]);axes=[na,nb]+[np.cross(ea[:,i],eb[:,j]) for i in range(3) for j in range(3)]+[np.cross(na,ea[:,i]) for i in range(3)]+[np.cross(nb,eb[:,i]) for i in range(3)];keep=np.ones(len(a),bool)
   for ax in axes:
    le=np.linalg.norm(ax,axis=1);valid=le>1e-10;ax=np.divide(ax,le[:,None],out=np.zeros_like(ax),where=valid[:,None]);pa=np.einsum('nvi,ni->nv',subA,ax);pb=np.einsum('nvi,ni->nv',subB,ax);keep&=~(((pa.max(1)<pb.min(1)-1e-6)|(pb.max(1)<pa.min(1)-1e-6))&valid)
   pairs=a[keep]
  external=[];interfaces=[]
  if len(pairs):
   trans=classify(q[pairs[:,0]],fixed[pairs[:,1]])
   for name in sorted(set(fn[pairs[:,1]])):
    mask=fn[pairs[:,1]]==name;row=dict(object=str(name),pairs=int(mask.sum()),transverse=int((trans&mask).sum()),moving_parts=sorted(set(mn[pairs[mask,0]].tolist())))
    (interfaces if name=='VOY04_GUIA_NUEVA' and all(x=='VOY04_CARRO_NUEVO' for x in row['moving_parts']) else external).append(row)
  poses.append(dict(retreat=float(D),bvh_pairs=len(raw),pairs=len(pairs),external=external,mechanical_interface=interfaces))
 result.append(dict(H=c['H'],poses=poses,external_contact_poses=sum(bool(p['external']) for p in poses),external_transverse_poses=sum(any(x['transverse'] for x in p['external']) for p in poses),sampling_m=.005,continuous_sweep_certified=False));print('CHAIR_MESH',c['H'],result[-1]['external_contact_poses'],result[-1]['external_transverse_poses'],flush=True)
(R/'DATOS/interferencias_silla.json').write_text(json.dumps(result,indent=2))
# Topology, per object, welded only in diagnostic memory. No source geometry is repaired.
e=Env();top=[]
keys=set(sum([m['parts'] for m in json.loads((R/'DATOS/inventario_medidas.json').read_text())],[]))|{'Object_129','Object_126','Object_127','Plane_94','Plane_95'}
for key in sorted(keys):
 q=e.tri[e.names==key];_,ix=np.unique(np.round(q.reshape(-1,3)/1e-5).astype(np.int64),axis=0,return_inverse=True);tt=ix.reshape(-1,3);edges=np.sort(np.concatenate([tt[:,[0,1]],tt[:,[1,2]],tt[:,[2,0]]]),axis=1);edges=edges[edges[:,0]!=edges[:,1]];_,counts=np.unique(edges,axis=0,return_counts=True);top.append(dict(key=key,boundary_edges=int((counts==1).sum()),nonmanifold_edges=int((counts>2).sum()),closed_candidate=bool(len(counts) and np.all(counts==2))))
(R/'DATOS/topologia.json').write_text(json.dumps(top,indent=2));print('TOPOLOGY',len(top),flush=True)
