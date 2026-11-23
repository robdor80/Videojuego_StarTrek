import sys,json,math,heapq
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World,dense_xy
w=World();old=json.loads((R/'DATOS/busqueda_original.json').read_text());step=old['grid_spacing_m'];targets=old['targets'];grid={}
for p in old['nodes']:
 s=w.state(*p[:2])
 if s['valid']:
  k=round((p[0]+6.9)/step),round((p[1]+5.1)/step);grid[k]=dict(foot=s['foot'],floor=s['floor'])
def edgeof(p,keys,xy):
 a=np.array(xy[:-1]);b=np.array(xy[1:]);ab=b-a;t=np.clip(np.einsum('ij,ij->i',np.array(p)-a,ab)/np.maximum(np.einsum('ij,ij->i',ab,ab),1e-14),0,1);ds=np.linalg.norm(a+ab*t[:,None]-p,axis=1);i=int(ds.argmin());return (keys[i],keys[i+1]) if i<len(keys)-1 else (None,None)
results=[]
for original in old['routes']:
 name=original['id'];a,b=name.split('_A_');aa=np.array(targets[a]);bb=np.array(targets[b]);ka=min(grid,key=lambda k:np.linalg.norm(np.array(grid[k]['foot'][:2])-aa));kb=min(grid,key=lambda k:np.linalg.norm(np.array(grid[k]['foot'][:2])-bb));blocked=set();rejected=[]
 for attempt in range(60):
  queue=[(0,ka)];dist={ka:0};prev={}
  while queue:
   cost,k=heapq.heappop(queue)
   if cost!=dist[k]:continue
   if k==kb:break
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
    n=k[0]+dx,k[1]+dy
    if n not in grid or frozenset((k,n)) in blocked or abs(grid[n]['floor']['z']-grid[k]['floor']['z'])>.18:continue
    nc=cost+float(np.linalg.norm(np.array(grid[n]['foot'])-grid[k]['foot']))
    if nc<dist.get(n,math.inf):dist[n]=nc;prev[n]=k;heapq.heappush(queue,(nc,n))
  if kb not in dist:result=dict(id=name,found=False,rejected=rejected);break
  keys=[kb]
  while keys[-1]!=ka:keys.append(prev[keys[-1]])
  keys=keys[::-1];xy=[grid[k]['foot'][:2] for k in keys];xy[0]=targets[a];xy[-1]=targets[b];dense=dense_xy(xy,.01);states=[w.state(*p) for p in dense];bad=[i for i,s in enumerate(states) if not s['valid']];steps=[i for i in range(len(states)-1) if states[i].get('floor') and states[i+1].get('floor') and abs(states[i+1]['floor']['z']-states[i]['floor']['z'])>.18]
  if not bad and not steps:
   result=dict(id=name,found=True,xy_path=xy,dense_xy=dense,foot_path=[s['foot'] for s in states],floor_sequence=[dict(xy=dense[i],floor=s['floor'],lift=s['lift_above_center_floor_m']) for i,s in enumerate(states)],rejected=rejected,attempts=attempt+1,geometry_modified=False);break
  kk=bad[0] if bad else steps[0];p=dense[kk];edge=edgeof(p,keys,xy);key=frozenset(edge)
  rejected.append(dict(point=p,reason=states[kk].get('reason') if bad else 'floor_step_gt_180mm',blocks=states[kk].get('blocks'),edge=[list(x) if x else None for x in edge]));blocked.add(key)
  print('REJECT_EDGE',name,attempt,rejected[-1],flush=True)
 else:result=dict(id=name,found=False,reason='replan_limit',rejected=rejected)
 results.append(result);print('FINAL_ROUTE',name,result['found'],result.get('attempts'),len(result.get('dense_xy',[])),flush=True)
(R/'DATOS/rutas_originales_candidatas.json').write_text(json.dumps(dict(targets=targets,scale=1.1,radius=.35,max_floor_rise_m=.18,method='Original geometry. Finite grid candidates with lazy rejection of edges whose 10mm refinement collides or jumps >180mm. No whole geometry edits; exact swept proof follows separately.',routes=results),indent=2,ensure_ascii=False),encoding='utf8')
