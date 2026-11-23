import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from geom import *
from mathutils.bvhtree import BVHTree
v,t,ids,obs=load('obj');tri=v[t];names=np.array([o['name'] for o in obs]);doors=json.loads((R/'DATOS/puertas_medidas.json').read_text());by={o['name']:o for o in obs}
def tree(q):return BVHTree.FromPolygons(q.reshape((-1,3)).tolist(),np.arange(len(q)*3).reshape((-1,3)).tolist(),all_triangles=True,epsilon=0)
def exact_overlap(a,b):
 # AABB overlap from Blender BVH, then SAT axes, including in-plane axes for coplanar triangles.
 pairs=tree(a).overlap(tree(b));real=[]
 for start in range(0,len(pairs),4000):
  part=np.array(pairs[start:start+4000],int)
  if not len(part):continue
  A=a[part[:,0]];B=b[part[:,1]];ea=np.roll(A,-1,axis=1)-A;eb=np.roll(B,-1,axis=1)-B;na=np.cross(ea[:,0],ea[:,1]);nb=np.cross(eb[:,0],eb[:,1]);axes=[na,nb]+[np.cross(ea[:,i],eb[:,j]) for i in range(3) for j in range(3)]+[np.cross(na,ea[:,i]) for i in range(3)]+[np.cross(nb,eb[:,i]) for i in range(3)];keep=np.ones(len(A),bool)
  for ax in axes:
   length=np.linalg.norm(ax,axis=1);valid=length>1e-10;ax=np.divide(ax,length[:,None],out=np.zeros_like(ax),where=valid[:,None]);pa=np.einsum('nvi,ni->nv',A,ax);pb=np.einsum('nvi,ni->nv',B,ax);separated=(pa.max(axis=1)<pb.min(axis=1)-1e-6)|(pb.max(axis=1)<pa.min(axis=1)-1e-6);keep&=~(separated&valid)
  real.extend(tuple(map(int,p)) for p in part[keep])
 return real,len(pairs)
door_tests=[]
for d in doors:
 ma=np.isin(names[ids],d['leafA']);mb=np.isin(names[ids],d['leafB']);moving=ma|mb;fixed=tri[~moving];fixednames=names[ids][~moving];A=tri[ma];B=tri[mb];lo=np.vstack([A.reshape((-1,3)),B.reshape((-1,3))]).min(axis=0)-1;hi=np.vstack([A.reshape((-1,3)),B.reshape((-1,3))]).max(axis=0)+1;near=(fixed.max(axis=1)>=lo).all(axis=1)&(fixed.min(axis=1)<=hi).all(axis=1);fixed=fixed[near];fixednames=fixednames[near];poses=[]
 baseline=None
 for f in [0,.25,.5,.75,1]:
  q=np.vstack([A+np.array(d['leafA_vector'])*f,B+np.array(d['leafB_vector'])*f]);pairs,broad=exact_overlap(q,fixed);pairset=set(pairs)
  if baseline is None:baseline=pairset
  novel=pairset-baseline;poses.append({'fraction':f,'bvh_pairs':broad,'triangle_intersections_or_contacts':len(pairset),'new_pairs_vs_closed':len(novel),'objects_new_contacts':sorted(set(str(fixednames[j]) for i,j in novel)),'method':'BVH broadphase + 17-axis triangle SAT, 1um separation tolerance; contacts included, no swept continuous solver'})
 closed=Collision(tri,names[ids]).pose(d['center'],height=1.9/1.1,radius=.35/1.1);door_tests.append({'id':d['id'],'closed_capsule_blocked_control':not closed['clear'],'poses':poses,'pocket_verified':not any(p['new_pairs_vs_closed'] for p in poses),'grade':'B' if not any(p['new_pairs_vs_closed'] for p in poses) else 'C'})
 print('DOOR_MOTION',d['id'],[(p['fraction'],p['new_pairs_vs_closed'],p['objects_new_contacts'][:4]) for p in poses],flush=True)
# Functional chair grouping uses explicit OBJ part families and spatial clusters. Does not transfer unverified MAX chair transforms.
stations=[('NAVEGACION',np.array([0,-2.67,.021205])),('LATERAL_DER',np.array([4.75,-2.7,.297639])),('LATERAL_IZQ',np.array([-4.18,-2.53,.297639]))]
chairgroups={k:[] for k,p in stations};allowed_objects={f'Object_{k}' for k in [75,76,77,120,121,122,123,124,125,126,127,128,129]}
for o in obs:
 if not (o['name'].startswith(('MSB','ChamferBox_','Layer__')) or o['name']in allowed_objects):continue
 c=(np.array(o['bounds_min'])+o['bounds_max'])/2;k,p=min(stations,key=lambda pair:np.linalg.norm(c[:2]-pair[1][:2]));
 if np.linalg.norm(c[:2]-p[:2])<1.2:chairgroups[k].append(o['name'])
chairgroups['MANDO_IZQ']=['Box_6','Box_7','Armrest_5','Armrest_6'];chairgroups['MANDO_DER']=['Box_8','Box_9','Armrest_7','Armrest_8']
chairs=[]
for group,parts in chairgroups.items():
 mask=np.isin(names[ids],parts);q=tri[mask];fixed=tri[~mask];fn=names[ids][~mask];lo=q.min(axis=(0,1))-.25;hi=q.max(axis=(0,1))+.25;near=(fixed.max(axis=1)>=lo).all(axis=1)&(fixed.min(axis=1)<=hi).all(axis=1);context=fixed[near];cn=fn[near];pivot=(q.min(axis=(0,1))+q.max(axis=(0,1)))/2;poses=[];base=None
 for mode,yaw,offset in [('ORIGEN',0,[0,0,0]),('GIRO_10_GRADOS',math.radians(10),[0,0,0]),('DESPLAZAMIENTO_10CM',0,[0,-.10/1.1,0])]:
  pose=transform(q-pivot,yaw,translation=pivot+offset);pairs,broad=exact_overlap(pose,context);pairs=set(pairs)
  if base is None:base=pairs
  new=pairs-base;poses.append({'mode':mode,'new_contact_pairs':len(new),'objects_new_contacts':sorted(set(str(cn[j]) for i,j in new)),'contacts_total':len(pairs)})
 low=[n for n in parts if by[n]['bounds_max'][2]<(min(by[n]['bounds_min'][2] for n in parts)+.18)];chairs.append({'id':group,'parts':parts,'part_count':len(parts),'pivot_candidate':pivot.tolist(),'fixed_base_candidates':low,'poses':poses,'grade':'B' if not any(p['new_contact_pairs'] for p in poses[1:]) else 'C','note':'Rigid assembly trials only; base/seat articulation, occupied pose and continuous sweep not certified.'});print('CHAIR',group,len(parts),[(p['mode'],p['new_contact_pairs']) for p in poses],flush=True)
screens=[]
for k,o in enumerate(obs):
 mats=list(o['materials']);screenm=[m for m in mats if m.lower().startswith('scrn') or m.lower()=='mainscreen']
 if not screenm:continue
 points=np.unique(tri[ids==k].reshape((-1,3)),axis=0);mean=points.mean(axis=0);_,_,vh=np.linalg.svd(points-mean,full_matrices=False);dist=(points-mean)@vh[-1];planar=float(np.abs(dist).max());screens.append({'object':o['name'],'materials':mats,'triangles':o['triangles'],'planarity_max_error_m':planar,'already_independent_object':len(screenm)==len(mats),'grade':'A' if planar<.001 and len(screenm)==len(mats) else 'B','normal_candidate':vh[-1].tolist(),'future':'Preserve UV0; independent output surface may host interaction, no UI implemented.'})
out={'doors':door_tests,'chairs':chairs,'screens':screens,'motion_tests_are_discrete':True,'no_blueprints_no_NPC':True}
(R/'DATOS/preparacion_funcional.json').write_text(json.dumps(out,indent=2),encoding='utf8');print('SCREENS',len(screens),collections.Counter(s['grade'] for s in screens),flush=True)
