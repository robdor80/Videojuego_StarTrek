"""Distinguish transverse surface crossings from coplanar/tangent contacts.
No surfaces are removed and no mechanism is certified by a clean discrete pose.
"""
import ast,sys,json,collections
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import *
# Reuse exactly the prior SAT functions without rerunning its top-level tests.
parsed=ast.parse((R/'SCRIPTS/10_funcional.py').read_text())
exec(compile(ast.Module(body=[x for x in parsed.body if isinstance(x,ast.FunctionDef) and x.name in ['tree','exact_overlap']],type_ignores=[]),'<SAT_prior>','exec'))
v,t,ids,obs=load('obj');alltri=v[t];names=np.array([o['name'] for o in obs]);doorrows=json.loads((R/'DATOS/puertas_medidas.json').read_text());out=[]
def classify(A,B,eps=1e-5):
 na=np.cross(A[:,1]-A[:,0],A[:,2]-A[:,0]);nb=np.cross(B[:,1]-B[:,0],B[:,2]-B[:,0]);na/=np.maximum(np.linalg.norm(na,axis=1)[:,None],1e-20);nb/=np.maximum(np.linalg.norm(nb,axis=1)[:,None],1e-20)
 da=np.einsum('nvi,ni->nv',A-B[:,0,None,:],nb);db=np.einsum('nvi,ni->nv',B-A[:,0,None,:],na)
 transverse=(da.min(axis=1)<-eps)&(da.max(axis=1)>eps)&(db.min(axis=1)<-eps)&(db.max(axis=1)>eps)
 coplanar=(np.abs(da).max(axis=1)<=eps)&(np.abs(db).max(axis=1)<=eps)
 return transverse,coplanar,np.minimum(np.maximum(0,np.minimum(-da.min(axis=1),da.max(axis=1))),np.maximum(0,np.minimum(-db.min(axis=1),db.max(axis=1))))
for d in doorrows:
 ma=np.isin(names[ids],d['leafA']);mb=np.isin(names[ids],d['leafB']);moving=ma|mb;A=alltri[ma];B=alltri[mb];fixed=alltri[~moving];fn=names[ids][~moving]
 lo=np.vstack([A.reshape((-1,3)),B.reshape((-1,3))]).min(axis=0)-1;hi=np.vstack([A.reshape((-1,3)),B.reshape((-1,3))]).max(axis=0)+1;near=(fixed.max(axis=1)>=lo).all(axis=1)&(fixed.min(axis=1)<=hi).all(axis=1);fixed=fixed[near];fn=fn[near]
 base=set(exact_overlap(np.vstack([A,B]),fixed)[0]);poses=[]
 def pose(f,offset=np.zeros(3)):
  q=np.vstack([A+np.array(d['leafA_vector'])*f,B+np.array(d['leafB_vector'])*f])+offset;pairs=set(exact_overlap(q,fixed)[0]);new=sorted(pairs-base)
  result=dict(fraction=float(f),all_pairs=len(pairs),new_pairs=len(new),coplanar=0,transverse=0,other_touch_or_edge=0,by_object=[])
  if new:
   ix=np.array(new,int);trans,cop,depth=classify(q[ix[:,0]],fixed[ix[:,1]],eps=1e-5/1.1);result.update(transverse=int(trans.sum()),coplanar=int(cop.sum()),other_touch_or_edge=int((~(trans|cop)).sum()))
   for name in sorted(set(fn[ix[:,1]])):
    sel=fn[ix[:,1]]==name;pts=q[ix[sel,0]].reshape((-1,3));result['by_object'].append(dict(object=str(name),pairs=int(sel.sum()),transverse=int((trans&sel).sum()),coplanar=int((cop&sel).sum()),max_two_sided_plane_crossing_depth_m=float(depth[sel].max()*1.1),moving_z_range_above_sill_m=((np.array([pts[:,2].min(),pts[:,2].max()])-d['center'][2])*1.1).tolist()))
  return result
 for f in np.linspace(0,1,21):poses.append(pose(f))
 variants=[]
 # Diagnostic only: offset full leaf pair normal to the door or above the floor.
 for mode,offset in [('NORMAL_OUT_10MM',np.array(d['normal'])*.010/1.1),('NORMAL_OUT_30MM',np.array(d['normal'])*.030/1.1),('NORMAL_IN_10MM',-np.array(d['normal'])*.010/1.1),('NORMAL_IN_30MM',-np.array(d['normal'])*.030/1.1),('LIFT_2MM',np.array([0,0,.002/1.1])),('LIFT_10MM',np.array([0,0,.010/1.1]))]:
  pp=[pose(f,offset) for f in [0,.25,.5,.75,1]];variants.append(dict(id=mode,offset_m=(offset*1.1).tolist(),poses=pp,all_sampled_surface_contacts_clear=all(p['all_pairs']==0 for p in pp)))
 # Surface topology diagnostics for the obstacle mesh, welded at 10um.
 topology=[]
 for name in sorted({x['object'] for p in poses for x in p['by_object']}):
  q=alltri[names[ids]==name];vv,ix=np.unique(np.round(q.reshape((-1,3))/1e-5).astype(np.int64),axis=0,return_inverse=True);tt=ix.reshape((-1,3));edges=np.sort(np.concatenate([tt[:,[0,1]],tt[:,[1,2]],tt[:,[2,0]]]),axis=1);edges=edges[edges[:,0]!=edges[:,1]];_,counts=np.unique(edges,axis=0,return_counts=True)
  topology.append(dict(object=name,boundary_edges=int((counts==1).sum()),nonmanifold_edges=int((counts>2).sum()),closed_two_manifold_candidate=bool(len(counts) and np.all(counts==2)),note='Triangle-edge weld at 10um; closed topology alone does not prove an empty pocket.'))
 out.append(dict(id=d['id'],scale=1.1,stroke_m=d['stroke_obj_units']*1.1,poses=poses,variants=variants,obstacle_topology=topology,pocket_certified=False,grade='C',conclusion='Investigated. Preserve floor contacts and transverse intersections separately; rebuild local guides/pockets in a later functional prototype. No tested offset is applied to the saved scene.'))
 print('DOOR_REVIEW',d['id'],'transverse_peak',max(p['transverse'] for p in poses),'coplanar_peak',max(p['coplanar'] for p in poses),'clean_variants',[v['id'] for v in variants if v['all_sampled_surface_contacts_clear']],flush=True)
(R/'DATOS/carreras_investigacion.json').write_text(json.dumps(dict(method='Prior BVH + 17-axis SAT; 21 static fractions; transverse test requires vertices on both sides of both planes beyond 10um. Depth is a plane crossing witness, not a solid penetration depth. Offset variants use 5 fractions only.',doors=out,no_original_or_scene_geometry_modified=True),indent=2,ensure_ascii=False),encoding='utf8')
