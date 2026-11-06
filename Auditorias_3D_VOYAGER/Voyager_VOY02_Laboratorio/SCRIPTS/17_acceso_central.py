"""Refined grid with fixed requested endpoints, component diagnostics and exact surfaces.
Negative is limited to this grid; no inference of absolute impossibility or UE walking.
"""
import sys,json,math,heapq,collections
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import *
v,t,ids,obs=load('obj');tri=v[t];names=np.array([o['name'] for o in obs]);doors=json.loads((R/'DATOS/puertas_medidas.json').read_text());scale=1.1
for d in doors:
 tri[np.isin(names[ids],d['leafA'])]+=d['leafA_vector'];tri[np.isin(names[ids],d['leafB'])]+=d['leafB_vector']
tri*=scale;cc=Collision(tri,names[ids]);gm=np.isin(ids,[i for i,o in enumerate(obs) if 'Voygray' in o['materials'] or o['name'] in ['Mesh_1856','Mesh_1787','Object_75']]);cross=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);gm&=np.abs(cross[:,2])>.98*np.linalg.norm(cross,axis=1);q=tri[gm];ground=BVHTree.FromPolygons(q.reshape((-1,3)).tolist(),np.arange(len(q)*3).reshape((-1,3)).tolist(),all_triangles=True)
step=.10;xs=np.arange(-7.1,7.11,step);ys=np.arange(-6.3,7.12,step);out=[]
for height in [1.6,1.9]:
 grid={};blocked=[];floors={}
 for ix,x in enumerate(xs):
  for iy,y in enumerate(ys):
   p,n,k,dist=ground.ray_cast((float(x),float(y),.9),(0,0,-1),2)
   if p is None:continue
   foot=[float(x),float(y),float(p.z+.002)];floors[ix,iy]=foot;r=cc.pose(foot,height,.35,.01)
   if r['clear']:grid[ix,iy]=foot
   else:blocked.append(dict(foot=foot,objects=r['blocking_objects']))
  if ix%30==0:print('GRID_PROGRESS',height,ix,len(xs),'clear',len(grid),flush=True)
 components={};groups=[]
 for key in grid:
  if key in components:continue
  cid=len(groups);queue=[key];components[key]=cid;group=[]
  while queue:
   k=queue.pop();group.append(k)
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    nn=k[0]+dx,k[1]+dy
    if nn in grid and nn not in components and abs(grid[nn][2]-grid[k][2])<=.31:components[nn]=cid;queue.append(nn)
  groups.append(group)
 routes=[]
 for name,a,b in [('CENTRO_A_POSTERIOR',[0,-.7],[1.191,6.08]),('NAVEGACION_A_POSTERIOR',[0,-4.4],[1.191,6.08]),('PASARELA_A_POSTERIOR',[3.6,2.7],[1.191,6.08])]:
  a=np.array(a)*scale;b=np.array(b)*scale;start=min(grid,key=lambda k:np.linalg.norm(np.array(grid[k][:2])-a));end=min(grid,key=lambda k:np.linalg.norm(np.array(grid[k][:2])-b));sa=float(np.linalg.norm(np.array(grid[start][:2])-a));sb=float(np.linalg.norm(np.array(grid[end][:2])-b));found=components[start]==components[end] and max(sa,sb)<=.20
  result=dict(id=name,requested_start_xy_m=a.tolist(),requested_goal_xy_m=b.tolist(),start_m=grid[start],goal_m=grid[end],start_adjustment_m=sa,goal_adjustment_m=sb,allowed_endpoint_adjustment_m=.20,start_component=components[start],goal_component=components[end],optimistic_grid_route_found=found)
  if found:
   queue=[start];prev={start:None}
   for k in queue:
    if k==end:break
    for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
     nn=k[0]+dx,k[1]+dy
     if nn in grid and nn not in prev and abs(grid[nn][2]-grid[k][2])<=.31:prev[nn]=k;queue.append(nn)
   keys=[end]
   while prev[keys[-1]] is not None:keys.append(prev[keys[-1]])
   points=[grid[k] for k in keys[::-1]];result['capsule_refined']=cc.path(points,height,.35,.025,.0125);result['support']=support_path(tri,points)
  else:
   # Closest pair of nodes across endpoint components, not an assumed door/path.
   aa=np.array([grid[k] for k in groups[components[start]]]);bb=np.array([grid[k] for k in groups[components[end]]]);best=(math.inf,None,None)
   for p in aa:
    ds=np.linalg.norm(bb-p,axis=1);j=int(ds.argmin())
    if ds[j]<best[0]:best=float(ds[j]),p,bb[j]
   dist,p,q=best;result['closest_component_gap_m']=dist;result['gap_endpoints']=[p.tolist(),q.tolist()];result['gap_straight_diagnostic']=cc.path([p,q],height,.35,.025,.01)
  routes.append(result);print('ACCESS',height,name,'found',found,'shifts',sa,sb,'gap',result.get('closest_component_gap_m'),'refined',result.get('capsule_refined',{}).get('clear'),flush=True)
 out.append(dict(height_m=height,radius_m=.35,grid_spacing_m=step,max_neighbor_level_difference_m=.31,free_nodes=len(grid),components=[dict(id=i,nodes=len(g)) for i,g in enumerate(groups)],nodes=[dict(foot=grid[k],component=components[k]) for k in grid],blocked_nodes=blocked,routes=routes))
(R/'DATOS/acceso_central_revision.json').write_text(json.dumps(dict(scale=scale,tests=out,method='0.10m real grid, geometric capsule distance on complete triangles; endpoints fixed within 0.20m and adjustments reported; optimistic four-neighbor level allowance 0.31m is not a stair solver; found routes rechecked every 25mm and five support rays.',conclusion='Any failed route remains E for gameplay access. A disconnected finite grid is not a proof of topological impossibility; capsule stair dynamics and UE CharacterMovement remain separate.'),indent=2,ensure_ascii=False),encoding='utf8')
