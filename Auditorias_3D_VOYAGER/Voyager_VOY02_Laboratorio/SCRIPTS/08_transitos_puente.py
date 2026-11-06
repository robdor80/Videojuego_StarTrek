from geom import *
import heapq,sys
v,t,ids,obs=load('obj');tri=v[t];names=np.array([o['name'] for o in obs]);doors=json.loads((R/'DATOS/puertas_medidas.json').read_text());scale=float(sys.argv[1]) if len(sys.argv)>1 else 1.1
for d in doors:
 tri[np.isin(names[ids],d['leafA'])]+=d['leafA_vector'];tri[np.isin(names[ids],d['leafB'])]+=d['leafB_vector']
cc=Collision(tri,names[ids]);floorids=[i for i,o in enumerate(obs) if 'Voygray'in o['materials'] or o['name'] in ['Mesh_1856','Mesh_1787']];gr=tri[np.isin(ids,floorids)];cross=np.cross(gr[:,1]-gr[:,0],gr[:,2]-gr[:,0]);gr=gr[np.abs(cross[:,2])>.98*np.linalg.norm(cross,axis=1)]
step=.15;xs=np.arange(-6.45,6.46,step);ys=np.arange(-5.7,6.46,step);grid={};blocked=[]
for ix,x in enumerate(xs):
 for iy,y in enumerate(ys):
  f=floor(gr,x,y,start=.76,limit=1.)
  if not f:continue
  p=[x,y,f['point'][2]+.002];r=cc.pose(p,height=1.9/scale,radius=.35/scale,margin=.01/scale)
  if r['clear']:grid[ix,iy]=p
  elif len(blocked)<120:blocked.append({'point':p,'blocks':r['blocking_objects']})
def route(a,b):
 start=min(grid,key=lambda k:np.linalg.norm(np.array(grid[k][:2])-a));end=min(grid,key=lambda k:np.linalg.norm(np.array(grid[k][:2])-b));queue=[(0,start)];dist={start:0};prev={}
 while queue:
  cost,k=heapq.heappop(queue)
  if k==end:break
  if cost>dist[k]:continue
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   n=(k[0]+dx,k[1]+dy)
   if n not in grid or abs(grid[n][2]-grid[k][2])*scale>.31:continue
   nc=cost+float(np.linalg.norm(np.array(grid[n])-grid[k]))
   if nc<dist.get(n,math.inf):dist[n]=nc;prev[n]=k;heapq.heappush(queue,(nc,n))
 if end not in dist:return {'found':False,'start':grid[start],'goal':grid[end]}
 path=[end]
 while path[-1]!=start:path.append(prev[path[-1]])
 path=path[::-1];points=[grid[k] for k in path];res=cc.path(points,height=1.9/scale,radius=.35/scale,spacing=.025,margin=.01/scale);return {'found':True,'length_obj':dist[end],'points':points,'refined_capsule_test':res,'elevation_changes':sorted(set(round(p[2],4) for p in points)),'note':'Grid search is geometric, not Recast; any large floor step and dynamics remain separate issues.'}
routes=[{'id':'pasarela_al_posterior',**route([3.6,2.7],[1.191,6.08])},{'id':'centro_al_posterior',**route([0,-.7],[1.191,6.08])},{'id':'navegacion_al_lateral',**route([0,-4.4],[5.9,.18])}]
out={'scale':scale,'capsule_real_m':{'height':1.9,'radius':.35},'grid_spacing_obj':step,'standable_nodes':len(grid),'nodes':[p for p in grid.values()],'blocked_examples':blocked,'routes':routes}
suffix='' if abs(scale-1.1)<1e-8 else '_'+str(scale).replace('.','p')
(R/'DATOS'/f'transitos_puente{suffix}.json').write_text(json.dumps(out,indent=2),encoding='utf8')
for r in routes:print(r['id'],r['found'],r.get('length_obj'),r.get('refined_capsule_test',{}).get('clear'),r.get('elevation_changes'))
print('NODES',len(grid))
