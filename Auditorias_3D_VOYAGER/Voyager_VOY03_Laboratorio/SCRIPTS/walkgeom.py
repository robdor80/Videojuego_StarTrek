"""VOY03 terrain-aware capsule geometry. Does not mutate VOY02 or implement UE physics."""
import sys,json,math,collections
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1]
from geom import Collision,point_tri_sq,capsule_distance,segment_segment_sq,dot
EXTRA_FLOORS=['Mesh_1968','Mesh_1848','Mesh_2121','Mesh_2122','Mesh_2123','Mesh_2124','Mesh_1739','Mesh_1740','Mesh_1755','Mesh_1807','Mesh_1808','Mesh_1809','Mesh_1810','Mesh_1811']
class World:
 def __init__(self,tri=None,labels=None,additions=None):
  data=np.load(R/'DATOS/puente_abierto.npz');self.tri=data['triangles'] if tri is None else np.asarray(tri,float);self.labels=data['labels'] if labels is None else np.asarray(labels)
  meta=json.loads((R/'DATOS/obj_objetos.json').read_text());floor_names=[o['name'] for o in meta if 'Voygray'in o['materials']]+['Mesh_1856','Object_75']+EXTRA_FLOORS
  self.support_names=set(floor_names);self.support_mask=np.array([str(n).removeprefix('PUENTE:') in self.support_names or str(n).startswith('VOY03_SUELO') or str(n).startswith('AD_') or str(n) in ['PASILLO_PRINCIPAL','CRUCE_CUATRO','ACCESO_TURBO','CABINA_TURBO','PASILLO_CAMAROTE','CAMAROTE_EXISTENTE'] for n in self.labels]);cross=np.cross(self.tri[:,1]-self.tri[:,0],self.tri[:,2]-self.tri[:,0]);length=np.linalg.norm(cross,axis=1);self.flat=self.support_mask&(np.abs(cross[:,2])>.999*length)&(length>1e-10)
  self.cc=Collision(self.tri,self.labels);self.lo=self.cc.lo;self.hi=self.cc.hi;self.floor_ix=np.where(self.flat)[0];q=self.tri[self.flat];self.bvh=BVHTree.FromPolygons(q.reshape(-1,3).tolist(),np.arange(len(q)*3).reshape(-1,3).tolist(),all_triangles=True)
  q=self.tri[self.support_mask];self.terrain=BVHTree.FromPolygons(q.reshape(-1,3).tolist(),np.arange(len(q)*3).reshape(-1,3).tolist(),all_triangles=True)
 def candidates(self,x,y,r=.36):
  lo=np.floor((np.array([x,y])-r)/self.cc.cell).astype(int);hi=np.floor((np.array([x,y])+r)/self.cc.cell).astype(int);cand=set()
  for i in range(lo[0],hi[0]+1):
   for j in range(lo[1],hi[1]+1):cand.update(self.cc.grid.get((i,j),[]))
  return np.array(list(cand),int)
 def floor(self,x,y,start=1.05):
  p,n,k,d=self.bvh.ray_cast((float(x),float(y),start),(0,0,-1),2)
  if p is not None:return dict(z=float(p.z),point=list(p),triangle=int(self.floor_ix[k]),object=str(self.labels[self.floor_ix[k]]),method='BVH')
  # A float BVH may miss exactly shared edges. Intersect the SAME triangles in
  # double precision; no floor extension or bridging of physical gaps is added.
  ix=self.candidates(x,y,.00001);ix=ix[self.flat[ix]]
  if not len(ix):return None
  t=self.tri[ix];a=t[:,0];ab=t[:,1]-a;ac=t[:,2]-a
  cross2=lambda u,v:u[:,0]*v[:,1]-u[:,1]*v[:,0]
  v=np.array([x,y])-a[:,:2];den=cross2(ab[:,:2],ac[:,:2]);u=np.divide(cross2(v,ac[:,:2]),den,out=np.full(len(ix),-1.),where=np.abs(den)>1e-20);v2=np.divide(cross2(ab[:,:2],v),den,out=np.full(len(ix),-1.),where=np.abs(den)>1e-20)
  z=a[:,2]+u*ab[:,2]+v2*ac[:,2];valid=(u>=-1e-10)&(v2>=-1e-10)&(u+v2<=1+1e-10)&(z<=start)&(z>=start-2)
  if not valid.any():return None
  j=np.where(valid)[0][z[valid].argmax()];k=int(ix[j]);z=float(z[j]);return dict(z=z,point=[x,y,z],triangle=k,object=str(self.labels[k]),method='double_precision_same_triangle')
 def state(self,x,y,h=1.9,r=.35):
  floor=self.floor(x,y)
  if floor is None:return dict(valid=False,reason='no_center_support',xy=[x,y])
  ix=self.candidates(x,y,r+.006);gi=ix[self.flat[ix] & (self.hi[ix,2]>=floor['z']-.01) & (self.lo[ix,2]<floor['z']+.37)]
  q=self.tri[gi].copy();q[:,:,2]=0;rho2=point_tri_sq([x,y,0],q);inside=rho2<r*r
  gi=gi[inside];rho2=rho2[inside]
  if not len(gi):return dict(valid=False,reason='no_bearing')
  envelope=self.hi[gi,2]-r+np.sqrt(np.maximum(0,r*r-rho2));k=int(envelope.argmax());footz=float(envelope[k]+.004)
  # The dark nosing can project ahead of the tread. Resolve the lower hemisphere
  # against all measured stair surfaces, not just the horizontal tread triangles.
  ti=ix[self.support_mask[ix] & (self.hi[ix,2]>=floor['z']-.01) & (self.lo[ix,2]<floor['z']+.50)]
  def gap(z):return float(np.sqrt(point_tri_sq([x,y,z+r],self.tri[ti])).min()-r)
  if len(ti) and gap(footz)<.004:
   low=footz;high=float(max(footz,self.hi[ti,2].max()+.004))
   for iteration in range(17):
    middle=(low+high)/2
    if gap(middle)<.004:low=middle
    else:high=middle
   footz=high
  if footz-floor['z']>r+.01:return dict(valid=False,reason='bearing_outside_lower_hemisphere',floor=floor,lift=footz-floor['z'])
  foot=np.array([x,y,footz]);near=(self.hi[ix,2]>footz-.001)&(self.lo[ix,2]<footz+h+.005)&(self.hi[ix,0]>x-r-.005)&(self.lo[ix,0]<x+r+.005)&(self.hi[ix,1]>y-r-.005)&(self.lo[ix,1]<y+r+.005);ci=ix[near];ds=capsule_distance(self.tri[ci],foot,h,r)-r;threshold=np.where(self.support_mask[ci],.001,.005);bad=ci[ds<threshold-1e-6]
  loc,n,ti,dist=self.terrain.find_nearest(foot+[0,0,r]);up=(footz+r-loc.z)/dist if dist else 0
  return dict(valid=not len(bad) and up>=.50,foot=foot.tolist(),floor=floor,lift_above_center_floor_m=footz-floor['z'],bearing_up=float(up),bearing_object=str(self.labels[gi[k]]),bearing_triangle=int(gi[k]),clearance_min_m=float(ds.min()) if len(ds) else None,blocks=sorted(set(self.labels[bad].tolist())),reason='geometry' if len(bad) else 'lateral_bearing_not_support' if up<.50 else 'clear')
 def raw_pose(self,p,h=1.9,r=.35):
  p=np.array(p,float);ix=self.candidates(*p[:2],r+.01);ix=ix[(self.hi[ix,2]>p[2]-.001)&(self.lo[ix,2]<p[2]+h+.005)];ds=capsule_distance(self.tri[ix],p,h,r)-r
  return dict(clear=bool(np.all(ds>=np.where(self.support_mask[ix],.0005,.003)-1e-6)),min_clearance=float(ds.min()) if len(ds) else None,blocks=sorted(set(self.labels[ix[ds<-.00001]].tolist())))
def dense_xy(points,spacing=.01):
 out=[]
 for a,b in zip(points[:-1],points[1:]):
  a=np.array(a)[:2];b=np.array(b)[:2];n=max(1,math.ceil(np.linalg.norm(b-a)/spacing));out.extend((a+(b-a)*u).tolist() for u in np.linspace(0,1,n,endpoint=False))
 return out+[list(points[-1][:2])]
