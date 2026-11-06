import sys,json,math,time
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World,dense_xy
from sweepgeom import swept_distance,controls
controls_result=controls();route_data=json.loads((R/'DATOS/rutas_originales_candidatas.json').read_text());w=World();routes=[]
for r in route_data['routes']:
 if r['found']:routes.append(dict(id=r['id'],xy_path=r['xy_path'],scope='required_bridge_route'))
profiles=json.loads((R/'DATOS/perfiles_escaleras.json').read_text())['profiles']
for p in profiles:
 c=np.array(p['origin']);direction=np.array(p['up_axis']);xy=[(c+direction*u)[:2].tolist() for u in [-.85,.70]];routes.append(dict(id='ESCALERA_'+p['id'],xy_path=xy,scope='diagnostic_stair_flight'))
routes.append(dict(id='ESCALERA_NAV_CENTRAL',xy_path=[[0,-1.50],[0,-2.50]],scope='diagnostic_stair_flight'))
# Full VOY02 prototype is reused with original transforms; work frame is bridge frame.
proto=json.loads((R/'DATOS/prototipo_conjunto.json').read_text());data=np.load(R/'DATOS/prototipo_geometria.npz');T=np.array(proto['bridge_translation']);wf=World(data['triangles']-T,data['labels']);central=next(r for r in routes if r['id']=='CENTRO_A_PASARELA')['xy_path']
for r in proto['routes']:
 old=(np.array(r['routes'][0]['points'])-T)[:,:2].tolist();routes.append(dict(id='CENTRO_'+r['id'],xy_path=central+old,scope='full_center_network'));routes.append(dict(id='REGRESION_'+r['id'],xy_path=old,scope='VOY02_regression'))
def validate(world,route,height):
 xy=dense_xy(route['xy_path'],.01);states=[world.state(*p,h=height) for p in xy];fail=[dict(sample=i,**s) for i,s in enumerate(states) if not s['valid']];points=[s.get('foot') for s in states];step_fail=[];sweeps=[];bearing=[]
 q=world.tri[world.support_mask];terrain=BVHTree.FromPolygons(q.reshape(-1,3).tolist(),np.arange(len(q)*3).reshape(-1,3).tolist(),all_triangles=True)
 for i,s in enumerate(states):
  if not s['valid']:continue
  p=np.array(s['foot']);loc,n,k,dist=terrain.find_nearest(p+[0,0,.35]);up=(p[2]+.35-loc.z)/dist if dist else 0;bearing.append(dict(sample=i,gap_m=float(dist-.35),up_component=float(up),contact=list(loc),floor_z=s['floor']['z'],lift=s['lift_above_center_floor_m']))
  if not (.0025<=dist-.35<=.008 and up>.10):fail.append(dict(sample=i,reason='bearing_witness',gap=float(dist-.35),up=float(up)))
  if i and states[i-1].get('floor') and abs(s['floor']['z']-states[i-1]['floor']['z'])>.18001:step_fail.append(dict(sample=i,rise_m=s['floor']['z']-states[i-1]['floor']['z']))
 for i,(a,b) in enumerate(zip(points[:-1],points[1:])):
  if a is None or b is None:continue
  a=np.array(a);b=np.array(b);center=(a+b)/2;extent=.35+np.linalg.norm((b-a)[:2])/2+.005;ix=world.candidates(*center[:2],extent);lo=np.minimum(a,b);hi=np.maximum(a,b);ix=ix[(world.hi[ix,2]>=lo[2]-.01)&(world.lo[ix,2]<=hi[2]+height+.005)&(world.hi[ix,0]>=lo[0]-.36)&(world.lo[ix,0]<=hi[0]+.36)&(world.hi[ix,1]>=lo[1]-.36)&(world.lo[ix,1]<=hi[1]+.36)]
  if not len(ix):sweeps.append(dict(segment=i,clear=True,minimum_m=None));continue
  distance=swept_distance(world.tri[ix],a,b,height,.35);threshold=np.where(world.support_mask[ix],.0005,.003);bad=ix[distance<threshold-1e-7];sweeps.append(dict(segment=i,clear=not len(bad),minimum_m=float(distance.min()),blocks=sorted(set(world.labels[bad].tolist()))))
  if i%700==0:print('SWEEP_PROGRESS',route['id'],height,i,len(points),flush=True)
 bad_sweep=[s for s in sweeps if not s['clear']];passed=not fail and not step_fail and not bad_sweep
 return dict(id=route['id'],scope=route['scope'],height_m=height,radius_m=.35,classification='Superado sobre geometría original de trabajo' if passed else 'Resultado inconcluso' if not step_fail and not bad_sweep else 'Bloqueado por criterio de movimiento' if step_fail else 'Bloqueado por geometría',pass_test=passed,pose_samples=len(states),swept_intervals=len(sweeps),foot_points=points,floor_points=[s.get('floor',{}).get('z') for s in states],pose_or_support_failures=fail[:30],movement_failures=step_fail[:30],sweep_failures=bad_sweep[:30],minimum_swept_clearance_m=min((s['minimum_m'] for s in sweeps if s['minimum_m'] is not None),default=None),max_lift_above_center_floor_m=max((s.get('lift_above_center_floor_m',0) for s in states),default=0),bearing_min_up=min((x['up_component'] for x in bearing),default=None),bearing_gap_range_m=[min(x['gap_m'] for x in bearing),max(x['gap_m'] for x in bearing)] if bearing else None,bearing_witnesses=bearing[::max(1,len(bearing)//40)],forward='tested',reverse='same exact swept volume and reversed support/step order: geometrically certified under symmetric 180mm rise/drop criterion' if passed else 'not certified',geometry_modified=False)
out=[]
for route in routes:
 world=wf if route['scope'] in ['full_center_network','VOY02_regression'] else w
 for height in [1.6,1.75,1.9]:
  start=time.time();result=validate(world,route,height);out.append(result);print('VALIDATED',route['id'],height,result['pass_test'],'poses',result['pose_samples'],'sweep_fail',result['sweep_failures'][:1],'pose_fail',result['pose_or_support_failures'][:1],'motion',result['movement_failures'][:1],'seconds',time.time()-start,flush=True)
  (R/'DATOS/barridos_resultados_parcial.json').write_text(json.dumps(dict(controls=controls_result,results=out),indent=2,ensure_ascii=False),encoding='utf8')
(R/'DATOS/barridos_resultados.json').write_text(json.dumps(dict(controls=controls_result,method='For each 10mm XY interval, full translating vertical capsule axis sweeps a quad. Exact triangle/quad surface distances with edge/face crossing tests certify the entire linear interval. Contact support witnesses use the real lower hemisphere, 4mm geometric pad. No UE dynamics or gait certification. Reversal shares identical swept volume; not counted as an independent geometric experiment.',scale=1.1,geometry_modified=False,results=out),indent=2,ensure_ascii=False),encoding='utf8')
