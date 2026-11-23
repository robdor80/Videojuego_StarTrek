from geom import *
from math import atan2,pi
vv,tt,oi,ob=load('modulos');interfaces=json.loads((R/'DATOS/interfaces_modulos.json').read_text());by={x['name']:x for x in interfaces};mesh={o['name']:vv[tt[oi==k]]+np.array(by[o['name']]['normalize_translation']) for k,o in enumerate(ob)}
def rot(a):return np.array([[math.cos(a),-math.sin(a),0],[math.sin(a),math.cos(a),0],[0,0,1]])
def placement(name,meshname,yaw=0,translation=(0,0,0)):
 return {'id':name,'source':meshname,'yaw':yaw,'translation':list(map(float,translation)),'original_to_canonical':by[meshname]['normalize_translation']}
def port(place,code):
 p=next(x for x in by[place['source']]['ports'] if x['code']==code);rr=rot(place['yaw']);return {**p,'world_point':(rr@p['point']+place['translation']).tolist(),'world_normal':(rr@p['normal']).tolist()}
def attach(A,acode,bname,bmesh,bcode,gap=0):
 a=port(A,acode);b=next(x for x in by[bmesh]['ports'] if x['code']==bcode);normal=-np.array(a['world_normal']);yaw=atan2(normal[1],normal[0])-atan2(b['normal'][1],b['normal'][0]);pos=np.array(a['world_point'])+np.array(a['world_normal'])*gap-rot(yaw)@b['point'];return placement(bname,bmesh,yaw,pos)
def placed(p):return transform(mesh[p['source']],p['yaw'],p['translation'])
def profile_points(segments,axis,tan,p):
 # Convert actual sectional edges to transverse-height samples at 10mm maximum spacing.
 out=[]
 for a,b in segments:
  a=np.array(a);b=np.array(b);n=max(1,int(np.ceil(np.linalg.norm(b-a)/.01)))
  out.extend(a+(b-a)*u for u in np.linspace(0,1,n+1))
 return np.array(out) if out else np.empty((0,3))
def compare(A,acode,B,bcode):
 a=port(A,acode);b=port(B,bcode);p=np.array(a['world_point']);n=np.array(a['world_normal']);tan=np.array([-n[1],n[0],0]);ta=placed(A);tb=placed(B);both=np.vstack([ta,tb]);floorprobes=[]
 for lateral in [-.9,0,.9]:
  for d in [-.02,-.005,.005,.02]:
   q=p+tan*lateral+n*d;hit=floor(both,q[0],q[1],start=p[2]+.5,limit=1);floorprobes.append({'offset_normal':d,'lateral':lateral,'hit':bool(hit),'floor_error':hit['point'][2]-p[2] if hit else None})
 segsets=[]
 for pl,pp in [(A,a),(B,b)]:
  pts=profile_points(pp['section_segments'],None,None,None);pts=pts@rot(pl['yaw']).T+pl['translation'];segsets.append(np.column_stack([(pts-p)@tan,pts[:,2]-p[2]]) if len(pts) else np.empty((0,2)))
 haus=None
 if all(len(s) for s in segsets):
  values=[]
  for s1,s2 in [segsets,segsets[::-1]]:
   maxd=0
   for chunk in np.array_split(s1,max(1,len(s1)//200)):
    ds=np.linalg.norm(chunk[:,None,:]-s2[None,:,:],axis=2);maxd=max(maxd,float(ds.min(axis=1).max()))
   values.append(maxd)
  haus=max(values)
 w1=a['width_z040_100_170_220'];w2=b['width_z040_100_170_220'];dw=max((abs(x-y) for x,y in zip(w1,w2) if x is not None and y is not None),default=None);h1=a['ceiling_z'];h2=b['ceiling_z'];dh=abs(h1-h2) if h1 is not None and h2 is not None else None;anchor=float(np.linalg.norm(np.array(a['world_point'])-b['world_point']));normerr=float(np.linalg.norm(np.array(a['world_normal'])+b['world_normal']));support=all(f['hit'] and abs(f['floor_error'])<.002 for f in floorprobes)
 classification='A' if anchor<1e-5 and normerr<1e-5 and support and haus is not None and haus<.015 else ('B' if support and (dw or 0)<.25 else 'C')
 return {'a':A['id'],'a_port':acode,'b':B['id'],'b_port':bcode,'anchor_residual_m':anchor,'normal_residual':normerr,'floor_delta_m':abs(a['world_point'][2]-b['world_point'][2]),'width_delta_m':dw,'ceiling_delta_m':dh,'profile_sampled_hausdorff_m':haus,'profile_sampling_m':.01,'floor_probes':floorprobes,'floor_continuous_sampled':support,'grade_geometric_interface':classification,'method':'opposing actual interface anchors + section profiles at 2mm inside + floor samples; no unmeasured visual-fit acceptance'}
cases=[]
def case(name,spec):
 ps=[];joins=[]
 for name_,source,prev,pa,pb in spec:
  p=placement(name_,source) if prev is None else attach(next(x for x in ps if x['id']==prev),pa,name_,source,pb)
  ps.append(p)
  if prev is not None:joins.append(compare(next(x for x in ps if x['id']==prev),pa,p,pb))
 # A polyline through exact module center and interface points. Turn is inside the measured module, not diagonal through outside walls.
 route=[]
 for k,p in enumerate(ps):
  if k==0:
   start=port(p,'Y-')['world_point'];route.append((np.array(start)+[0,.35,.002]).tolist())
  route.append((np.array(p['translation'])+[0,0,.002]).tolist())
  if k<len(ps)-1:route.append((np.array(joins[k]['floor_probes'][0].get('dummy',p['translation']))+[0,0,.002]).tolist()) if False else None
 route.append((np.array(ps[-1]['translation'])+[0,0,.002]).tolist())
 geometry=np.vstack([placed(p) for p in ps]);labels=np.concatenate([np.full(len(placed(p)),p['id']) for p in ps]);cc=Collision(geometry,labels);results=[cc.path(route,height=h,radius=.35,spacing=.025,margin=.0125) for h in [1.6,1.75,1.9]]
 support=support_path(geometry,route)
 cases.append({'id':name,'placements':ps,'joins':joins,'routes':results,'floor_support':support,'note':'Route uses centers; endpoint remains inside last module. Doors in side recesses stay as source geometry.'})
case('B01_CORTO_LARGO',[('corto','Mesh12',None,None,None),('largo','Mesh13','corto','Y+','Y-')])
case('B02_DOS_RECTOS_CURVA',[('largo','Mesh13',None,None,None),('curva','Mesh41','largo','Y+','Y-'),('salida','Mesh18','curva','X+','Y-')])
case('B03_RECTA_T',[('recto','Mesh18',None,None,None),('T','Mesh40','recto','Y+','Y-'),('ramal','Mesh18','T','X+','Y-')])
case('B04_CUATRO_VIAS',[('recto','Mesh18',None,None,None),('cruce','Mesh38','recto','Y+','Y-'),('este','Mesh18','cruce','X+','Y-')])
case('B05_MODULO_PUERTAS',[('recto','Mesh18',None,None,None),('puertas','Mesh14','recto','Y+','Y-')])
case('B06_TURBOLIFT',[('recto','Mesh18',None,None,None),('acceso','Mesh37','recto','Y+','Y-'),('cabina','Mesh17','acceso','Y+','Y-')])
case('B07_RESIDENCIAL',[('recto','Mesh18',None,None,None),('residencial','Mesh57','recto','Y+','Y-')])
(R/'DATOS/ensamblajes_pruebas.json').write_text(json.dumps(cases,indent=2),encoding='utf8')
for c in cases:print(c['id'],'JOINS',[(j['grade_geometric_interface'],round(j['width_delta_m'] or 0,4),round(j['profile_sampled_hausdorff_m'] or 0,4),j['floor_continuous_sampled']) for j in c['joins']],'CAPS',[(p['height'],p['clear'],p['minimum_clearance']) for p in c['routes']],'SUPPORT',c['floor_support']['clear'])
