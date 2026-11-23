import numpy as np,math,json,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1];EPS=1e-12
def load(label):
 d=np.load(R/'DATOS'/f'{label}_geometria.npz');return d['vertices'],d['triangles'],d['object_ids'],json.loads((R/'DATOS'/f'{label}_objetos.json').read_text(encoding='utf8'))
def dot(a,b):return np.einsum('...i,...i->...',a,b)
def ray(tri,p,d,limit=100):
 p=np.asarray(p,float);d=np.asarray(d,float);e1=tri[:,1]-tri[:,0];e2=tri[:,2]-tri[:,0];h=np.cross(d,e2);det=dot(e1,h);valid=np.abs(det)>EPS;inv=np.divide(1,det,out=np.zeros_like(det),where=valid);s=p-tri[:,0];u=dot(s,h)*inv;q=np.cross(s,e1);v=dot(d,q)*inv;dist=dot(e2,q)*inv;valid&=(u>=-1e-7)&(v>=-1e-7)&(u+v<=1+1e-7)&(dist>1e-6)&(dist<=limit)
 if not valid.any():return None
 ds=np.where(valid,dist,np.inf);k=int(ds.argmin());return {'distance':float(ds[k]),'point':(p+d*ds[k]).tolist(),'triangle':k}
def floor(tri,x,y,start=.9,limit=10):return ray(tri,[x,y,start],[0,0,-1],limit)
def segment_point_sq(p,a,b):
 ab=b-a;u=np.clip(dot(p-a,ab)/np.maximum(dot(ab,ab),EPS),0,1);q=a+ab*u[:,None];return dot(p-q,p-q)
def point_tri_sq(p,tri):
 a,b,c=tri[:,0],tri[:,1],tri[:,2];ab=b-a;ac=c-a;n=np.cross(ab,ac);nn=dot(n,n);dist=dot(p-a,n);proj=p-n*(dist/np.maximum(nn,EPS))[:,None];v=proj-a;aa=dot(ab,ab);bb=dot(ac,ac);cc=dot(ab,ac);va=dot(v,ab);vb=dot(v,ac);den=aa*bb-cc*cc;u=(bb*va-cc*vb)/np.maximum(den,EPS);w=(aa*vb-cc*va)/np.maximum(den,EPS);inside=(u>=0)&(w>=0)&(u+w<=1)&(nn>EPS)
 edges=np.minimum.reduce([segment_point_sq(p,a,b),segment_point_sq(p,b,c),segment_point_sq(p,c,a)])
 return np.where(inside,dist*dist/np.maximum(nn,EPS),edges)
def segment_segment_sq(p,q,a,b):
 # Closest distance between finite segments, including parallel/degenerate cases.
 u=q-p;v=b-a;w=p-a;aa=float(dot(u,u));bb=dot(u,v);cc=dot(v,v);dd=dot(u,w);ee=dot(v,w);den=aa*cc-bb*bb
 s=np.clip(np.divide(bb*ee-cc*dd,den,out=np.zeros_like(den),where=np.abs(den)>EPS),0,1);t=np.divide(bb*s+ee,cc,out=np.zeros_like(cc),where=cc>EPS)
 s=np.where(t<0,np.clip(-dd/max(aa,EPS),0,1),s);s=np.where(t>1,np.clip((bb-dd)/max(aa,EPS),0,1),s);t=np.clip(t,0,1)
 delta=w+s[:,None]*u-t[:,None]*v;return dot(delta,delta)
def capsule_distance(tri,foot,height=1.8,radius=.35):
 foot=np.asarray(foot,float);p=foot+[0,0,radius];q=foot+[0,0,height-radius]
 ds=np.minimum(point_tri_sq(p,tri),point_tri_sq(q,tri))
 for i,j in [(0,1),(1,2),(2,0)]:ds=np.minimum(ds,segment_segment_sq(p,q,tri[:,i],tri[:,j]))
 # Segment-plane crossings whose barycentric coordinates are within the triangle.
 a=tri[:,0];ab=tri[:,1]-a;ac=tri[:,2]-a;n=np.cross(ab,ac);den=dot(n,q-p);u=np.divide(dot(n,a-p),den,out=np.full(len(tri),-1.),where=np.abs(den)>EPS);hit=p+u[:,None]*(q-p);nn=dot(n,n);c0=dot(np.cross(tri[:,1]-tri[:,0],hit-tri[:,0]),n);c1=dot(np.cross(tri[:,2]-tri[:,1],hit-tri[:,1]),n);c2=dot(np.cross(tri[:,0]-tri[:,2],hit-tri[:,2]),n);cross=(u>=0)&(u<=1)&(c0>=-1e-10)&(c1>=-1e-10)&(c2>=-1e-10)&(nn>EPS)
 return np.sqrt(np.maximum(np.where(cross,0,ds),0))
class Collision:
 def __init__(self,tri,ids=None,cell=.5):
  self.tri=np.asarray(tri,float);self.ids=ids;self.lo=self.tri.min(axis=1);self.hi=self.tri.max(axis=1);self.cell=cell;self.grid=collections.defaultdict(list)
  for k,(lo,hi) in enumerate(zip(self.lo,self.hi)):
   a=np.floor(lo[:2]/cell).astype(int);b=np.floor(hi[:2]/cell).astype(int)
   for x in range(a[0],b[0]+1):
    for y in range(a[1],b[1]+1):self.grid[x,y].append(k)
 def pose(self,foot,height=1.8,radius=.35,margin=0):
  p=np.asarray(foot,float);extent=radius+margin;lo=np.floor((p[:2]-extent)/self.cell).astype(int);hi=np.floor((p[:2]+extent)/self.cell).astype(int);cand=set()
  for x in range(lo[0],hi[0]+1):
   for y in range(lo[1],hi[1]+1):cand.update(self.grid.get((x,y),[]))
  if not cand:return {'clear':True,'min_clearance':None,'candidate_triangles':0,'blocking_objects':[]}
  ix=np.array(list(cand),int);sel=(self.hi[ix,2]>p[2]+.002)&(self.lo[ix,2]<p[2]+height+margin)&(self.hi[ix,0]>p[0]-extent)&(self.lo[ix,0]<p[0]+extent)&(self.hi[ix,1]>p[1]-extent)&(self.lo[ix,1]<p[1]+extent);ix=ix[sel]
  if not len(ix):return {'clear':True,'min_clearance':None,'candidate_triangles':0,'blocking_objects':[]}
  ds=capsule_distance(self.tri[ix],p,height,radius)-radius;blocked=ix[ds<margin-1e-5];return {'clear':not len(blocked),'min_clearance':float(ds.min()),'candidate_triangles':len(ix),'blocking_objects':list(sorted(set(str(self.ids[k]) for k in blocked)))[:15] if self.ids is not None else [],'blocking_triangles':len(blocked)}
 def path(self,points,height=1.8,radius=.35,spacing=.025,margin=.0125):
  samples=[]
  for a,b in zip(points[:-1],points[1:]):
   a=np.array(a,float);b=np.array(b,float);n=max(1,int(math.ceil(np.linalg.norm(b-a)/spacing)));samples.extend(a+(b-a)*u for u in np.linspace(0,1,n,endpoint=False))
  samples.append(np.array(points[-1],float));results=[self.pose(p,height,radius,margin) for p in samples];bad=[{'sample':i,'foot':samples[i].tolist(),**r} for i,r in enumerate(results) if not r['clear']];return {'height':height,'radius':radius,'spacing_max':spacing,'margin':margin,'samples':len(samples),'clear_samples':sum(r['clear'] for r in results),'clear':not bad,'minimum_clearance':min((r['min_clearance'] for r in results if r['min_clearance'] is not None),default=None),'failures':bad[:12],'points':[list(map(float,p)) for p in points],'method':'exact segment-triangle distance on broadphase candidates; discrete translation poses; support surfaces below foot+2mm excluded; not CharacterMovement'}
def transform(tri,yaw=0,translation=(0,0,0),scale=1):
 c=math.cos(yaw);s=math.sin(yaw);rot=np.array([[c,-s,0],[s,c,0],[0,0,1]]);return (tri*scale)@rot.T+translation
def section_segments(tri,axis,plane):
 segments=[]
 for t in tri:
  ds=t[:,axis]-plane;pts=[]
  if ds.min()>0 or ds.max()<0:continue
  for i,j in [(0,1),(1,2),(2,0)]:
   if abs(ds[i])<1e-8:pts.append(t[i])
   if ds[i]*ds[j]<0:pts.append(t[i]+(t[j]-t[i])*(-ds[i])/(ds[j]-ds[i]))
  if len(pts)>=2:
   p=np.unique(np.round(pts,8),axis=0)
   if len(p)>=2:segments.append([p[0].tolist(),p[-1].tolist()])
 return segments
def self_test():
 wall=np.array([[[0,-3,-1],[0,3,-1],[0,0,4]]],float)
 assert abs(capsule_distance(wall,[.5,0,0])[0]-.5)<1e-9
 assert abs(capsule_distance(wall,[.2,0,0])[0]-.2)<1e-9
 assert capsule_distance(wall,[0,0,0])[0]<1e-9
 floortri=np.array([[[-2,-2,0],[2,-2,0],[0,2,0]]],float)
 assert abs(capsule_distance(floortri,[0,0,0])[0]-.35)<1e-9
 roof=floortri+np.array([0,0,1.7]);assert abs(capsule_distance(roof,[0,0,0])[0]-.25)<1e-9
 return {'analytic_cases':5,'passed':5}
def support_path(tri,points,spacing=.05,disk=.20):
 samples=[]
 for a,b in zip(points[:-1],points[1:]):
  a=np.array(a,float);b=np.array(b,float);n=max(1,int(math.ceil(np.linalg.norm(b-a)/spacing)));samples.extend(a+(b-a)*u for u in np.linspace(0,1,n,endpoint=False))
 samples.append(np.array(points[-1],float));fail=[];count=0;maxerr=0
 # Up/down-facing triangles are candidates; normals orientation alone does not define support.
 cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);mask=np.abs(cross[:,2])>.99*np.linalg.norm(cross,axis=1);q=tri[mask]
 for k,p in enumerate(samples):
  for dx,dy in [(0,0),(disk,0),(-disk,0),(0,disk),(0,-disk)]:
   count+=1;hit=ray(q,[p[0]+dx,p[1]+dy,p[2]+.10],[0,0,-1],.2);err=abs(hit['point'][2]-p[2]) if hit else None
   if err is None or err>.01:
    if len(fail)<15:fail.append({'sample':k,'point':p.tolist(),'foot_offset':[dx,dy],'floor_error':err})
   elif err>maxerr:maxerr=err
 return {'samples':len(samples),'support_probes':count,'disk_probe_radius':disk,'spacing':spacing,'clear':not fail,'maximum_accepted_floor_error_m':maxerr,'failures':fail,'note':'Five supports per pose; not a full continuous contact or CharacterMovement solver.'}
