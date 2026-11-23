import sys,json,csv,collections
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World
from geom import capsule_distance
w=World();profiles=json.loads((R/'DATOS/perfiles_escaleras.json').read_text())['profiles'];out=[];topo=json.loads((R/'DATOS/topografia_objetos.json').read_text());lookup={o['name']:o for o in topo['objects']}
for p in profiles:
 c=np.array(p['origin']);u=np.array(p['up_axis']);v=np.array(p['lateral_axis']);rows=[]
 for t in np.arange(-.6,.701,.002):
  xy=(c+u*t)[:2];f=w.floor(*xy);rows.append(dict(u_m=float(t),z_m=f['z'] if f else None,object=f['object'] if f else None))
 transitions=[];last=None
 for row in rows:
  key=round(row['z_m'],4) if row['z_m'] is not None else None
  if key!=last:
   transitions.append(row);last=key
 useful=[r for r in transitions if r['z_m'] is not None];risers=[]
 for a,b in zip(useful,useful[1:]):
  if b['z_m']-a['z_m']>.01:risers.append(dict(position_u_m=b['u_m'],riser_m=b['z_m']-a['z_m'],from_object=a['object'],to_object=b['object']))
 widthtests=[]
 for t in [0,p['between_tread_centers_m'],.55]:
  states=[(off,w.state(*(c+u*t+v*off)[:2])) for off in np.arange(-.8,.801,.01)];valid=[off for off,s in states if s['valid']];center=min(range(len(states)),key=lambda j:abs(states[j][0]));lo=hi=center
  while lo>0 and states[lo-1][1]['valid']:lo-=1
  while hi<len(states)-1 and states[hi+1][1]['valid']:hi+=1
  widthtests.append(dict(u_m=t,capsule_center_span_m=[states[lo][0],states[hi][0]],center_span_width_m=states[hi][0]-states[lo][0],swept_capsule_total_width_m=states[hi][0]-states[lo][0]+.7,grid_m=.01,interpretation='Contiguous free lateral centre positions at this cross section, not a global corridor width.'))
 headroom=[]
 for t in np.linspace(-.5,.6,23):
  xy=(c+u*t)[:2];s=w.state(*xy);ix=w.candidates(*xy,.001);ix=ix[(w.lo[ix,0]<=xy[0])&(w.hi[ix,0]>=xy[0])&(w.lo[ix,1]<=xy[1])&(w.hi[ix,1]>=xy[1])];tr=w.tri[ix];a=tr[:,0];ab=tr[:,1]-a;ac=tr[:,2]-a;cr=np.cross(ab,ac);den=cr[:,2];z=a[:,2]-np.divide(cr[:,0]*(xy[0]-a[:,0])+cr[:,1]*(xy[1]-a[:,1]),den,out=np.full(len(ix),1e9),where=np.abs(den)>1e-12);pt=np.column_stack([np.full(len(z),xy[0]),np.full(len(z),xy[1]),z]);crosses=[]
  from geom import point_tri_sq
  for j in range(len(ix)):
   if z[j]>s['foot'][2]+.25 and point_tri_sq(pt[j],tr[j:j+1])[0]<1e-12:crosses.append(float(z[j]-s['foot'][2]))
  headroom.append(min(crosses) if crosses else None)
 out.append(dict(id=p['id'],origin=c.tolist(),up_axis=u.tolist(),transitions=transitions,risers=risers,tread_depth_axis_m=p['between_tread_centers_m'],width_cross_sections=widthtests,min_vertical_headroom_centerline_m=min([h for h in headroom if h is not None],default=None),profile=rows))
nav=[]
for y in np.arange(-3.0,-1.19,.002):
 f=w.floor(0,y);nav.append(dict(y_m=float(y),z_m=f['z'] if f else None,object=f['object'] if f else None))
nt=[];last=None
for row in nav:
 key=round(row['z_m'],4) if row['z_m'] is not None else None
 if key!=last:nt.append(row);last=key
names=['Mesh_1856','Mesh_1859','Mesh_1860','Mesh_1861','Mesh_1862','Mesh_1863','Mesh_2121','Mesh_2122','Mesh_2123','Mesh_2124','Mesh_1968','Mesh_1848','Mesh_1739','Mesh_1740','Mesh_1755','Mesh_1807','Mesh_1808','Mesh_1809','Mesh_1810','Mesh_1811','Mesh_1787','Mesh_1788','Mesh_2096','Mesh_1944']
details=[]
for n in names:
 ix=np.where(w.labels==n)[0];t=w.tri[ix];rounded=np.round(t,6);canonical=np.array([sorted(map(tuple,a)) for a in rounded]);_,counts=np.unique(canonical.reshape(len(t),-1),axis=0,return_counts=True);edges=np.concatenate([rounded[:,[0,1]],rounded[:,[1,2]],rounded[:,[2,0]]]);canon=np.array([sorted(map(tuple,e)) for e in edges]);_,ec=np.unique(canon.reshape(len(edges),-1),axis=0,return_counts=True);details.append(dict(name=n,bounds=[w.lo[ix].min(axis=0).tolist(),w.hi[ix].max(axis=0).tolist()],triangles=len(ix),duplicate_triangle_excess_at_1um=int(np.sum(counts-1)),boundary_edges_at_1um=int(np.sum(ec==1)),nonmanifold_edges_at_1um=int(np.sum(ec>2)),levels=lookup[n]['levels'] if n in lookup else [],role='console, obstacle, not floor' if n in ['Mesh_1787','Mesh_1788'] else 'obstacle' if n in ['Mesh_2096','Mesh_1944'] else 'floor or stair, preserve entire geometry'))
result=dict(frame='bridge A; metres; imported +90deg X correction retained; scale1.10',lateral_flights=out,navigation_centerline_transitions=nt,objects=details,topology_note='Topology is geometric edge counting after 1um rounding; seams and double-sided panels may be intentional. No automatic repairs.',seam=dict(objects=['AD_PUENTE','PASILLO_PRINCIPAL'],y_m=8.420256090164186,physical_gap_measured_m=0,numeric_problem='float32 BVH misses coincident edge; same triangle double precision ray succeeds.'))
(R/'DATOS/mediciones_finales.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
with (R/'DATOS/escalones_medidos.csv').open('w',newline='',encoding='utf-8-sig') as f:
 wr=csv.DictWriter(f,fieldnames=['flight','number','riser_m','tread_depth_axis_m','position_u_m','from_object','to_object']);wr.writeheader()
 for p in out:
  for i,s in enumerate(p['risers']):wr.writerow(dict(flight=p['id'],number=i+1,tread_depth_axis_m=p['tread_depth_axis_m'],**s))
print('MEASURED',[(p['id'],len(p['risers']),p['min_vertical_headroom_centerline_m'],p['width_cross_sections']) for p in out],flush=True)
