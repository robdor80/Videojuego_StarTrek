"""Measured surfaces and explicit diagnostic body hypotheses, not a character rig."""
import bpy,sys,json,math,collections
import numpy as np
from pathlib import Path
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import load,Collision,ray
v,t,ids,obs=load('obj');tri=v[t];names=np.array([o['name'] for o in obs]);by={o['name']:i for i,o in enumerate(obs)};scale=1.1
doors=json.loads((R/'DATOS/puertas_medidas.json').read_text());functional=json.loads((R/'DATOS/preparacion_funcional.json').read_text())
for d in doors:
 tri[np.isin(names[ids],d['leafA'])]+=d['leafA_vector'];tri[np.isin(names[ids],d['leafB'])]+=d['leafB_vector']
tri*=scale
def bvh(q):return BVHTree.FromPolygons(q.reshape((-1,3)).tolist(),np.arange(len(q)*3).reshape((-1,3)).tolist(),all_triangles=True)
tree=bvh(tri)
groundmask=np.isin(ids,[i for i,o in enumerate(obs) if 'Voygray' in o['materials'] or o['name'] in ['Mesh_1856','Mesh_1787','Object_75']]);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);groundmask&=np.abs(cross[:,2])>.98*np.linalg.norm(cross,axis=1)
groundix=np.where(groundmask)[0];g=bvh(tri[groundmask]);cc=Collision(tri,names[ids])
def hit(b,p,d,limit=10,ix=None):
 loc,n,k,dist=b.ray_cast(p,d,limit)
 if loc is None:return None
 return dict(point=list(loc),distance=dist,object=str(names[ids[ix[k] if ix is not None else k]]))
def floor(x,y):return hit(g,(x,y,.9),(0,0,-1),2,groundix)
zones=[('CENTRO',0,-.7),('NAVEGACION_PASO',0,-4.4),('DELANTE_MANDO',0,0),('PASARELA_DERECHA',3.6,2.7),('POSTERIOR',1.191,6.08),('LATERAL_DER',5.7,.1),('LATERAL_IZQ',-5.7,.1),('TRAS_MANDO',0,2.0)]
zoneout=[]
for name,x,y in zones:
 x*=scale;y*=scale;f=floor(x,y)
 if not f:zoneout.append(dict(zone=name,floor=None));continue
 z=f['point'][2];first=hit(tree,(x,y,z+.01),(0,0,1),6);over=hit(tree,(x,y,z+1.80),(0,0,1),5)
 zoneout.append(dict(zone=name,xy_m=[x,y],floor=f,first_surface=first,overhead_from_1p80=over,overhead_clearance_m=over['point'][2]-z if over else None,standing=[dict(height=h,**cc.pose([x,y,z+.002],h,.35,.01)) for h in [1.6,1.75,1.8,1.9]]))
 print('ZONE',name,zoneout[-1]['overhead_clearance_m'],[(r['height'],r['clear']) for r in zoneout[-1]['standing']],flush=True)
seatnames={'NAVEGACION':['ChamferBox_22'],'LATERAL_DER':['ChamferBox_37'],'LATERAL_IZQ':['ChamferBox_38'],'MANDO_IZQ':['ChamferBox_27','ChamferBox_28','ChamferBox_29'],'MANDO_DER':['ChamferBox_34','ChamferBox_35','ChamferBox_36']}
seats=[]
screens=[]
for scr in functional['screens']:
 q=tri[ids==by[scr['object']]];c=q.reshape((-1,3)).mean(axis=0);screens.append(dict(object=scr['object'],center_m=c.tolist(),min_m=q.min(axis=(0,1)).tolist(),max_m=q.max(axis=(0,1)).tolist(),grade=scr['grade']))
for name,sn in seatnames.items():
 q=tri[np.isin(ids,[by[n] for n in sn])];st=bvh(q);lo=q.min(axis=(0,1));hi=q.max(axis=(0,1));cx,cy=(lo[:2]+hi[:2])/2
 # Command cushion incorporates a tall back: sample forward 35% of depth, not bbox maximum.
 if name.startswith('MANDO'):cy=lo[1]+.40*(hi[1]-lo[1])
 pts=[]
 for dx in [-.06,0,.06]:
  for dy in [-.06,0,.06]:
   p,normal,k,dist=st.ray_cast((cx+dx,cy+dy,hi[2]+.1),(0,0,-1),2)
   if p is not None:pts.append(list(p))
 if not pts:
  # Curved command cushion can miss a central 3x3 square. Retain the negative,
  # then scan the entire forward cushion footprint and report actual hits only.
  for xx in np.linspace(lo[0]+.01,hi[0]-.01,15):
   for yy in np.linspace(lo[1]+.01,lo[1]+.6*(hi[1]-lo[1]),15):
    p,normal,k,dist=st.ray_cast((float(xx),float(yy),float(hi[2]+.1)),(0,0,-1),2)
    if p is not None and p.z<1.20*scale:pts.append(list(p))
 assert pts,(name,'no measurable seat surface')
 z=float(np.median([p[2] for p in pts]));cx,cy=np.median(np.array(pts)[:,:2],axis=0);f=floor(cx,cy);fz=f['point'][2] if f else None
 nearby=sorted(screens,key=lambda x:np.linalg.norm(np.array(x['center_m'])[:2]-[cx,cy]))[:5]
 # Standing approach positions around each station. Surface tests include all seat/console parts.
 approaches=[]
 for dx,dy in [(0,-.75),(0,.75),(-.75,0),(.75,0)]:
  ff=floor(cx+dx,cy+dy)
  if ff:approaches.append(dict(xy=[cx+dx,cy+dy],floor=ff,result=cc.pose([cx+dx,cy+dy,ff['point'][2]+.002],1.9,.35,.01)))
 # Control proximity is measured to surface centers, no inferred hand operation.
 controls=[dict(**p,distance_xy_from_seat_m=float(np.linalg.norm(np.array(p['center_m'])[:2]-[cx,cy])),height_above_seat_m=p['center_m'][2]-z) for p in nearby]
 seats.append(dict(id=name,seat_object=sn,sample_points_m=pts,seat_sample_median_z=z,floor=f,seat_height_above_floor_m=z-fz if fz is not None else None,seat_surface_z_range=[min(p[2] for p in pts),max(p[2] for p in pts)],outer_seat_bbox_xy_m=(hi-lo)[:2].tolist(),approach_tests=approaches,nearest_screen_candidates=controls,grade='C',note='Seat top sampled by 9 rays; outer bbox is not usable cushion width/depth. No body rig, tissue contact or reach certification.'))
 print('SEAT',name,'height',seats[-1]['seat_height_above_floor_m'],'approach',sum(a['result']['clear'] for a in approaches),'/',len(approaches),flush=True)
# Actual stair/level cross-sections: BVH rays every 1cm, retain every support run.
sections=[]
for id,x,y0,y1 in [('AXIS_CENTRAL',0,-4.5,3.5),('ESCALON_DER',2.7,-3.9,3.1),('ESCALON_IZQ',-2.7,-3.9,3.1)]:
 samples=[]
 for y in np.arange(y0*scale,y1*scale+.005,.01):
  f=floor(x*scale,float(y));samples.append(dict(x=x*scale,y=float(y),z=f['point'][2] if f else None,object=f['object'] if f else None))
 runs=[]
 for p in samples:
  key=round(p['z'],3) if p['z'] is not None else None
  if not runs or key!=runs[-1]['z_m']:runs.append(dict(y_start=p['y'],y_end=p['y'],z_m=key,source=p['object']))
  else:runs[-1]['y_end']=p['y']
 for a,b in zip(runs,runs[1:]):
  if a['z_m'] is not None and b['z_m'] is not None:b['rise_from_previous_m']=b['z_m']-a['z_m']
 for run in runs:run['sampled_run_length_m']=run['y_end']-run['y_start']+.01
 sections.append(dict(id=id,x_m=x*scale,runs=runs,samples=samples,note='Straight diagnostic sections may cross furniture or voids; not complete stair treads or a walking route.'))
out=dict(scale=scale,method='All original triangles; full doors moved statically; floor candidates Voygray/Mesh_1856/Mesh_1787 horizontal faces; surface ray locations included.',zones=zoneout,seats=seats,screens=screens,level_sections=sections,independent_references=['https://www.osha.gov/etools/computer-workstations/components/chairs','https://www.nasa.gov/reference/4-0-physical-characteristics-and-capabilities-vol-2/','https://www.codigotecnico.org/pdf/Documentos/SUA/DBSUA.pdf'],limits='Geometric design review completed with explicit negatives. Human posture, control operation, comfort and disability access are not certified by these proxies.')
(R/'DATOS/ergonomia_detallada.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
