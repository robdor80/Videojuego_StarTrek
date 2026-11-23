"""Articulated capsule mannequin. Proportions are explicit lab assumptions, not percentiles."""
import numpy as np,math,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import point_tri_sq,segment_segment_sq,dot,Collision,ray
def segment_tri(p,q,tri):
 ds=np.minimum(point_tri_sq(p,tri),point_tri_sq(q,tri))
 for i,j in [(0,1),(1,2),(2,0)]:ds=np.minimum(ds,segment_segment_sq(p,q,tri[:,i],tri[:,j]))
 a=tri[:,0];ab=tri[:,1]-a;ac=tri[:,2]-a;n=np.cross(ab,ac);den=dot(n,q-p);u=np.divide(dot(n,a-p),den,out=np.full(len(tri),-1.),where=np.abs(den)>1e-12);hit=p+u[:,None]*(q-p);nn=dot(n,n)
 cross=(u>=0)&(u<=1)&(nn>1e-12)
 for i,j in [(0,1),(1,2),(2,0)]:cross&=dot(np.cross(tri[:,j]-tri[:,i],hit-tri[:,i]),n)>=-1e-12
 return np.sqrt(np.maximum(np.where(cross,0,ds),0))
def ik(a,b,l1,l2,bend):
 d=b-a;D=np.linalg.norm(d)
 if D>l1+l2+1e-8 or D<abs(l1-l2)-1e-8:return None
 n=d/max(D,1e-12);x=(l1*l1-l2*l2+D*D)/(2*max(D,1e-12));h=math.sqrt(max(0,l1*l1-x*x));v=np.array(bend,float);v-=n*np.dot(v,n);v/=max(np.linalg.norm(v),1e-12);return a+n*x+v*h
def make_body(H,hip,ankles,lean=0,hands=None,yaw=0):
 # Diagnostic coordinates x along stored lateral axis, y forward, z up.
 # This legacy basis has determinant -1: do not infer nautical port/starboard from +/- labels.
 hip=np.array(hip,float);up=np.array([0,math.sin(lean),math.cos(lean)]);front=np.array([0,math.cos(lean),-math.sin(lean)]);right=np.array([1.,0,0]);parts=[];joints={'hip':hip.tolist()};bad=[]
 def add(n,a,b,r):parts.append(dict(name=n,p=np.array(a,float),q=np.array(b,float),r=float(r)))
 hw=.055*H;pelr=.043*H;add('PELVIS',hip-right*hw,hip+right*hw,pelr)
 waist=hip+up*.10*H;shoulder=hip+up*.288*H
 # Three overlapping capsules form a trunk with a shoulder breadth ~0.23H.
 for side in [-1,0,1]:add('TORSO_'+str(side),waist+right*side*.044*H,shoulder+right*side*.060*H,.055*H)
 neck=hip+up*.33*H;head=hip+up*.407*H;add('CUELLO',shoulder,neck,.032*H);add('CABEZA',head,head,.063*H)
 for side in [-1,1]:
  hh=hip+right*side*hw;ankle=np.array(ankles[0 if side<0 else 1],float);knee=ik(hh,ankle,.245*H,.245*H,[0,1,0])
  if knee is None:bad.append('pierna_'+str(side));continue
  add('MUSLO_'+str(side),hh,knee,.043*H);add('PANTORRILLA_'+str(side),knee,ankle,.029*H)
  foot=ankle-np.array([0,0,.018*H]);add('PIE_'+str(side),foot-np.array([0,.025*H,0]),foot+np.array([0,.080*H,0]),.027*H)
  sh=shoulder+right*side*.094*H
  hand=np.array(hands[0 if side<0 else 1],float) if hands is not None else hip+right*side*.13*H+front*.13*H+up*.035*H
  wrist=hand-front*.035*H;elbow=ik(sh,wrist,.186*H,.146*H,[side,0,-.4])
  if elbow is None:bad.append('brazo_'+str(side));continue
  add('BRAZO_'+str(side),sh,elbow,.023*H);add('ANTEBRAZO_'+str(side),elbow,wrist,.020*H);add('MANO_'+str(side),wrist,hand,.018*H)
  joints['knee_'+str(side)]=knee.tolist();joints['ankle_'+str(side)]=ankle.tolist();joints['shoulder_'+str(side)]=sh.tolist();joints['elbow_'+str(side)]=elbow.tolist();joints['hand_'+str(side)]=hand.tolist()
 if yaw:
  c=math.cos(yaw);s=math.sin(yaw);rot=np.array([[c,-s,0],[s,c,0],[0,0,1.]])
  for part in parts:
   part['p']=hip+rot@(part['p']-hip);part['q']=hip+rot@(part['q']-hip)
  joints={k:(hip+rot@(np.array(v)-hip)).tolist() for k,v in joints.items()}
 return dict(height=H,parts=parts,joints=joints,invalid_ik=bad)
class Env:
 def __init__(self,station='NAVEGACION'):
  d=np.load(R/'DATOS/geometria.npz');rows=json.loads((R/'DATOS/objetos.json').read_text());self.rows=rows;self.I=d['object_ids'];self.m=next(m for m in json.loads((R/'DATOS/inventario_medidas.json').read_text()) if m['id']==station);self.P=np.array(self.m['seat_point']);self.B=np.array(self.m['basis']);self.tri=(d['vertices'][d['triangles']]-self.P)@self.B;self.names=np.array([rows[k]['key'] for k in self.I]);self.chair=np.isin(self.names,self.m['parts']);self.floor=self.m['floor_m']-self.P[2];self.cc=Collision(self.tri,self.names);self.lo=self.cc.lo;self.hi=self.cc.hi
 def candidates(self,p,q,r):
  lo=np.minimum(p,q)-r-.004;hi=np.maximum(p,q)+r+.004
  a=np.floor(lo[:2]/self.cc.cell).astype(int);b=np.floor(hi[:2]/self.cc.cell).astype(int);cand=set()
  for x in range(a[0],b[0]+1):
   for y in range(a[1],b[1]+1):cand.update(self.cc.grid.get((x,y),[]))
  ix=np.array(list(cand),int)
  return ix[np.all(self.hi[ix]>=lo,axis=1)&np.all(self.lo[ix]<=hi,axis=1)]
 def test(self,body,chair_delta=(0,0,0),include_chair=True,details=False):
  out=[];worst=1.;mins={};delta=np.array(chair_delta);world=self.tri.copy() if np.any(delta) else self.tri
  if np.any(delta):world[self.chair]+=delta
  for pt in body['parts']:
   p=pt['p'];q=pt['q'];r=pt['r'];ix=self.candidates(p,q,r)
   if np.any(delta):
    ix=ix[~self.chair[ix]];ch=np.where(self.chair)[0];sel=np.all(world[ch].max(1)>=np.minimum(p,q)-r-.004,axis=1)&np.all(world[ch].min(1)<=np.maximum(p,q)+r+.004,axis=1);ix=np.r_[ix,ch[sel]]
   if not include_chair:ix=ix[~self.chair[ix]]
   if not len(ix):continue
   ds=segment_tri(p,q,world[ix])-r;mins[pt['name']]=float(ds.min());worst=min(worst,float(ds.min()));bad=ix[ds<-.002]
   if len(bad):out.append(dict(part=pt['name'],objects=sorted(set(self.names[bad].tolist())),clearance_m=float(ds.min()),triangles=bad.tolist() if details else len(bad)))
  return dict(clear=not out and not body['invalid_ik'],invalid_ik=body['invalid_ik'],minimum_clearance_m=worst,interferences=out,minima=mins)
 def adapted(self,drop,backshift=0):
  self.tri[self.chair,:,2]-=drop
  back=np.isin(self.names,['Object_76','Layer__3','MSB_30192','MSB_30193']);self.tri[back,:,1]+=backshift
  # Rebuild sleeve length locally: keep bottom at original bridge elevation, upper end below lowered seat.
  pole=self.names=='MSB_30191';z=self.tri[pole,:,2];lo=z.min();hi=z.max();bottom=.0483257818-self.P[2];top=-drop-.080
  self.tri[pole,:,2]=bottom+(z-lo)*(top-bottom)/(hi-lo)
  self.cc=Collision(self.tri,self.names);self.lo=self.cc.lo;self.hi=self.cc.hi
  return self
 def rail(self,D):
  floor=.0233257818-self.P[2]
  for name,lo,hi,moving in [('VOY04_GUIA_NUEVA',[-.035,-D-.08,floor+.001],[.035,.08,floor+.009],False),('VOY04_CARRO_NUEVO',[-.075,-.08,floor+.009],[.075,.08,floor+.025],True)]:
   vs=np.array([[x,y,z] for x in [lo[0],hi[0]] for y in [lo[1],hi[1]] for z in [lo[2],hi[2]]]);faces=np.array([[0,4,6],[0,6,2],[1,3,7],[1,7,5],[0,1,5],[0,5,4],[2,6,7],[2,7,3],[0,2,3],[0,3,1],[4,5,7],[4,7,6]])
   self.tri=np.concatenate([self.tri,vs[faces]]);self.names=np.concatenate([self.names,[name]*12]);self.chair=np.concatenate([self.chair,[moving]*12])
  self.cc=Collision(self.tri,self.names);self.lo=self.cc.lo;self.hi=self.cc.hi;return self
def serial(body):return dict(height=body['height'],joints=body['joints'],invalid_ik=body['invalid_ik'],parts=[dict(name=p['name'],p=p['p'].tolist(),q=p['q'].tolist(),r=p['r']) for p in body['parts']])
