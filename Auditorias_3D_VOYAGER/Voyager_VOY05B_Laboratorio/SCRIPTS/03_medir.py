import sys,math,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from comun import *
from mathutils.bvhtree import BVHTree
def geometry(obs):
 vv=[];tt=[];labels=[];base=0
 for o in obs:
  v=world(o);o.data.calc_loop_triangles();t=np.array([p.vertices[:] for p in o.data.loop_triangles],int).reshape(-1,3)
  vv.extend(v);tt.extend(t+base);labels.extend([o.name]*len(t));base+=len(v)
 return np.array(vv),np.array(tt),labels
def ray(b,p,d,limit):
 loc,n,idx,dist=b.ray_cast(Vector(p),Vector(d),limit)
 return None if loc is None else dict(point=list(loc),normal=list(n),triangle=idx,distance=dist)
inv=json.loads((R/'FUENTES/VOY05A/DATOS/inventario_puertas_accesos.json').read_text(encoding='utf8'))
bpy.ops.wm.open_mainfile(filepath=str(R/'FUENTES/VOY05A_Puente_Original_Inspeccion.blend'),load_ui=False,use_scripts=False)
leaves=set(n for x in inv if x['id'] in ['BR_01','BR_02','BR_03'] for n in x['objects'])
v,t,labs=geometry([o for o in bpy.context.scene.objects if o.type=='MESH' and o.name not in leaves]);bvh=BVHTree.FromPolygons(v,t,all_triangles=True)
out=[]
for x in [x for x in inv if x['id'].startswith('BR_')]:
 c=np.array(x['center_world']);c[2]=x['floor_z'];n=np.array(x['normal_world']);n[2]=0;n/=np.linalg.norm(n);u=np.cross([0,0,1],n)
 widths=[];heights=[];support=[];block=[]
 for depth in np.linspace(-.16,.16,33):
  for h in np.linspace(.02,1.77,176):
   p=c+n*depth+[0,0,h];a=ray(bvh,p,-u,1.5);bb=ray(bvh,p,u,1.5)
   widths.append(dict(depth=float(depth),z=float(h),width=(a['distance']+bb['distance']) if a and bb else None,left_object=labs[a['triangle']] if a else None,right_object=labs[bb['triangle']] if bb else None))
  for yy in np.linspace(-.37,.37,75):
   p=c+n*depth+u*yy+[0,0,.5];a=ray(bvh,p,[0,0,1],3);bb=ray(bvh,p,[0,0,-1],1)
   heights.append(dict(depth=float(depth),y=float(yy),ceiling_relative=a['point'][2]-c[2] if a else None,ceiling_object=labs[a['triangle']] if a else None))
   support.append(dict(depth=float(depth),y=float(yy),floor_relative=bb['point'][2]-c[2] if bb else None,object=labs[bb['triangle']] if bb else None))
 for yy in np.linspace(-.34,.34,35):
  for h in np.linspace(.04,1.72,85):
   p=c-n*.18+u*yy+[0,0,h];a=ray(bvh,p,n,.36)
   if a:block.append(dict(y=float(yy),z=float(h),object=labs[a['triangle']],point=a['point']))
 ls=[]
 for leaf in x.get('leaf_dimensions') or []:
  pts=np.vstack([world(bpy.data.objects[nm]) for nm in leaf['objects']]);q=(pts-c)@np.array([n,u,[0,0,1]]).T
  ls.append(dict(objects=leaf['objects'],local_min=q.min(0).tolist(),local_max=q.max(0).tolist(),dimensions=np.ptp(q,axis=0).tolist()))
 row=dict(id=x['id'],root=c.tolist(),normal=n.tolist(),tangent=u.tolist(),widths=widths,heights=heights,support=support,transverse_hits=block,leaves=ls,method='static BVH rays; 10 mm depth steps, 10 mm height steps, 10 mm lateral steps; no continuous sweep or collision certification')
 out.append(row)
 print(x['id'],'W min',min((w['width'] for w in widths if w['width'] is not None),default=None),'H center',[(p['depth'],p['ceiling_relative']) for p in heights if abs(p['y'])<1e-6][::8],'transverse',len(block),flush=True)
dump('DATOS/puente_medicion_repetida.json',out)
# Static cavity reservation: no object displacement or animation. SAT of triangles and AABBs.
c=np.array([1.1911309957504272,6.38205099105835,.7122955561927033]);B=np.array([[0,1,0],[-1,0,0],[0,0,1]])
tri=((v-c)@B.T)[t]
def sat_box(tri,lo,hi):
 center=(lo+hi)/2;half=(hi-lo)/2;tr=tri-center
 valid=np.all(tr.max(1)>=-half-1e-8,axis=1)&np.all(tr.min(1)<=half+1e-8,axis=1)
 ix=np.flatnonzero(valid);a=tr[ix];edges=np.stack([a[:,1]-a[:,0],a[:,2]-a[:,1],a[:,0]-a[:,2]],axis=1)
 axes=[np.cross(edges[:,0],edges[:,1])]
 for j in range(3):
  for k in range(3):axes.append(np.cross(edges[:,j],np.eye(3)[k]))
 keep=np.ones(len(ix),bool)
 for ax in axes:
  pp=np.einsum('tvc,tc->tv',a,ax);rad=np.abs(ax)@half
  keep&=(pp.min(1)<=rad+1e-10)&(pp.max(1)>=-rad-1e-10)
 return ix[keep]
cav=[]
for side in [-1,1]:
 for margin in [0,.01]:
  lo=np.array([-.021255-margin,.37915 if side>0 else -.79777,0+margin]);hi=np.array([.021255+margin,.79777 if side>0 else -.37915,1.775577+margin])
  ix=sat_box(tri,lo,hi);counts=collections.Counter(labs[j] for j in ix)
  cav.append(dict(side=side,margin=margin,local_min=lo.tolist(),local_max=hi.tolist(),intersecting_triangles=dict(counts),total=len(ix),method='triangle/AABB SAT of static proposed reservation; boundary contact included; box is conservative envelope, not a displaced leaf'))
dump('DATOS/BR03_reservas_cavidad.json',cav)
print('CAV',json.dumps(cav),flush=True)
bpy.ops.wm.open_mainfile(filepath=str(R/'FUENTES/VOY05A_Coleccion_Original_Inspeccion.blend'),load_ui=False,use_scripts=False)
rooms=[]
for name in ['Mesh4','Mesh5','Mesh6','Mesh9','Mesh11','Mesh81','Mesh12','Mesh13','Mesh18']:
 o=bpy.data.objects[name];v,t,l=geometry([o]);tr=v[t];lo=v.min(0);hi=v.max(0);center=(lo+hi)/2;b=BVHTree.FromPolygons(v,t,all_triangles=True)
 n=np.cross(tr[:,1]-tr[:,0],tr[:,2]-tr[:,0]);areas=np.linalg.norm(n,axis=1)/2;n=np.divide(n,2*areas[:,None],out=np.zeros_like(n),where=areas[:,None]>1e-12)
 # Weld only for diagnostic topology, without modifying source.
 _,wi=np.unique(np.round(v/1e-5).astype(np.int64),axis=0,return_inverse=True)
 edges=collections.Counter(tuple(sorted((int(wi[a]),int(wi[bb])))) for f in o.data.polygons for a,bb in zip(f.vertices,list(f.vertices[1:])+[f.vertices[0]]) if wi[a]!=wi[bb])
 floors=[];ceil=[];grid=[]
 for xx in np.linspace(lo[0]+.02,hi[0]-.02,41):
  for yy in np.linspace(lo[1]+.02,hi[1]-.02,41):
   pp=[xx,yy,lo[2]+1.3];f=ray(b,pp,[0,0,-1],1.5);ce=ray(b,pp,[0,0,1],5)
   if f and abs(f['normal'][2])>.9:floors.append(f['point'][2])
   if ce and abs(ce['normal'][2])>.9:ceil.append(ce['point'][2])
   grid.append(dict(x=float(xx),y=float(yy),floor_z=f['point'][2] if f else None,floor_normal=f['normal'] if f else None,ceiling_z=ce['point'][2] if ce else None,ceiling_normal=ce['normal'] if ce else None,headroom=ce['point'][2]-f['point'][2] if f and ce else None))
 horizontal=[]
 for z in sorted(set(np.round(tr.mean(1)[abs(n[:,2])>.99,2],3))):
  ix=(abs(n[:,2])>.99)&(abs(tr.mean(1)[:,2]-z)<.0006)
  horizontal.append(dict(z=float(z),area=float(areas[ix].sum()),up_area=float(areas[ix&(n[:,2]>0)].sum()),down_area=float(areas[ix&(n[:,2]<0)].sum())))
 record=dict(object=name,vertices=len(v),polygons=len(o.data.polygons),triangles=len(t),bounds_min=lo.tolist(),bounds_max=hi.tolist(),dimensions=(hi-lo).tolist(),boundary_edges_weld10um=sum(z==1 for z in edges.values()),nonmanifold_edges_weld10um=sum(z!=2 for z in edges.values()),horizontal_surfaces=horizontal,grid=grid,grid_note='41x41 bounding rectangle, ray origin bottom+1.3m; coverage is not walkability; steps/furniture may be hit',ports=[x for x in inv if x['objects']==[name]])
 rooms.append(record);print('SPACE',name,'boundary',record['boundary_edges_weld10um'],'floorgrid',len(floors),'ceilgrid',len(ceil),'surfaces',horizontal,flush=True)
dump('DATOS/espacios_medidos.json',rooms)
