import sys,json,math,heapq,collections,time
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World,dense_xy
w=World();targets={'CENTRO':[0,-.77],'NAVEGACION':[-.8,-2.90],'MANDO_IZQ':[-1.43,-.22],'MANDO_DER':[1.43,-.22],'PASARELA':[3.96,2.97],'POSTERIOR':[1.191*1.1,6.08*1.1]}
for name,xy in targets.items():print('TARGET',name,w.state(*xy),flush=True)
step=.10;xs=np.arange(-6.9,6.91,step);ys=np.arange(-5.1,7.11,step);grid={};rejections=collections.Counter();start=time.time()
for i,x in enumerate(xs):
 for j,y in enumerate(ys):
  s=w.state(float(x),float(y))
  if s['valid']:grid[i,j]=s
  else:rejections[s['reason']]+=1
 if i%25==0:print('GRID',i,len(xs),'free',len(grid),'elapsed',time.time()-start,flush=True)
def route(a,b):
 aa=np.array(targets[a]);bb=np.array(targets[b]);ka=min(grid,key=lambda k:np.linalg.norm(np.array(grid[k]['foot'][:2])-aa));kb=min(grid,key=lambda k:np.linalg.norm(np.array(grid[k]['foot'][:2])-bb));queue=[(0,ka)];dist={ka:0};prev={};found=False
 while queue:
  cost,k=heapq.heappop(queue)
  if cost!=dist[k]:continue
  if k==kb:found=True;break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
   n=k[0]+dx,k[1]+dy
   if n not in grid or abs(grid[n]['floor']['z']-grid[k]['floor']['z'])>.18:continue
   length=np.linalg.norm(np.array(grid[n]['foot'])-grid[k]['foot']);nc=cost+float(length)
   if nc<dist.get(n,math.inf):dist[n]=nc;prev[n]=k;heapq.heappush(queue,(nc,n))
 out=dict(id=a+'_A_'+b,start_requested=targets[a],end_requested=targets[b],start=grid[ka]['foot'],end=grid[kb]['foot'],adjustments=[float(np.linalg.norm(np.array(grid[ka]['foot'][:2])-aa)),float(np.linalg.norm(np.array(grid[kb]['foot'][:2])-bb))],found=found)
 if found:
  keys=[kb]
  while keys[-1]!=ka:keys.append(prev[keys[-1]])
  xy=[targets[a]]+[grid[k]['foot'][:2] for k in keys[::-1]]+[targets[b]];dense=dense_xy(xy,.01);states=[w.state(*p) for p in dense];out['xy_path']=xy;out['foot_path']=[s.get('foot') for s in states];out['state_failures']=[dict(sample=i,**s) for i,s in enumerate(states) if not s['valid']][:30];out['max_raw_floor_step_m']=max(abs(states[i+1].get('floor',{}).get('z',0)-states[i].get('floor',{}).get('z',0)) for i in range(len(states)-1));out['dense_clear']=not out['state_failures'] and out['max_raw_floor_step_m']<=.18;out['ground_objects']=sorted(set(s['floor']['object'] for s in states if s.get('floor')))
 return out
routes=[]
for a,b in [('CENTRO','PASARELA'),('CENTRO','NAVEGACION'),('NAVEGACION','PASARELA'),('CENTRO','MANDO_IZQ'),('CENTRO','MANDO_DER'),('PASARELA','POSTERIOR')]:
 r=route(a,b);routes.append(r);print('ROUTE',r['id'],r['found'],r.get('dense_clear'),r.get('state_failures',[])[:1],flush=True)
(R/'DATOS/busqueda_original.json').write_text(json.dumps(dict(scale=1.1,reference_radius=.35,search_height=1.9,grid_spacing_m=step,floor_step_limit_m=.18,lift_limit_m=.20,support_mesh_additions=['Mesh_1968','Mesh_1848','Mesh_2121','Mesh_2122','Mesh_2123','Mesh_2124'],excluded_old_floor_candidate='Mesh_1787: console/front trim; not accepted as walking surface',free_nodes=len(grid),rejections=dict(rejections),nodes=[s['foot'] for s in grid.values()],targets=targets,routes=routes,note='Terrain lower-sphere envelope on measured horizontal surfaces; not a dynamics solver. Search is only candidate generation; full sweeps/support validation remain separate.'),indent=2,ensure_ascii=False),encoding='utf8')
