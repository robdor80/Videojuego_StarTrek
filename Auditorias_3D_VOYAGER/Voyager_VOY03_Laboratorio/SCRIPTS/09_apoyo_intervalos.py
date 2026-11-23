"""Continuous bearing certificate: distance to a convex triangle is convex.
If both ends of an interval lie <= radius+8mm from one real triangle,
the entire interval does too. Require that triangle below both sphere centres.
Subdivide the actual linear trajectory if the supporting triangle changes.
This is a capsule terrain envelope, not a human foot or gait simulation.
"""
import sys,json,time
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World
from geom import point_tri_sq
w=World();proto=json.loads((R/'DATOS/prototipo_conjunto.json').read_text());d=np.load(R/'DATOS/prototipo_geometria.npz');wf=World(d['triangles']-np.array(proto['bridge_translation']),d['labels']);data=json.loads((R/'DATOS/barridos_resultados.json').read_text());out=[]
def certify(world,p,q,depth=0):
 p=np.array(p);q=np.array(q);a=p+[0,0,.35];b=q+[0,0,.35];ix=world.candidates(*((a+b)/2)[:2],.38);ix=ix[world.support_mask[ix] & (world.hi[ix,2]<=min(a[2],b[2])-.179)&(world.hi[ix,2]>=min(p[2],q[2])-.02)]
 if len(ix):
  ds=np.maximum(point_tri_sq(a,world.tri[ix]),point_tri_sq(b,world.tri[ix]));k=int(ds.argmin())
  if ds[k]<=(.358)**2:return True,depth,float(np.sqrt(ds[k])-.35)
 if depth==10:return False,depth,None
 mid=(p+q)/2;l=certify(world,p,mid,depth+1);r=certify(world,mid,q,depth+1)
 return l[0] and r[0],max(l[1],r[1]),max([v for v in [l[2],r[2]] if v is not None],default=None)
for route in data['results']:
 if route['height_m']!=1.9:continue # Foot trajectories identical for all three heights; checked below.
 world=wf if route['scope'] in ['full_center_network','VOY02_regression'] else w;points=route['foot_points'];tests=[certify(world,a,b) if a is not None and b is not None else (False,0,None) for a,b in zip(points[:-1],points[1:])];same=all(r['foot_points']==points for r in data['results'] if r['id']==route['id']);row=dict(id=route['id'],certified=all(t[0] for t in tests) and same,intervals=len(tests),failed_intervals=[i for i,t in enumerate(tests) if not t[0]],max_subdivision_depth=max(t[1] for t in tests),maximum_bearing_distance_above_radius_m=max((t[2] for t in tests if t[2] is not None),default=None),same_trajectory_all_heights=same);out.append(row);print(row,flush=True)
(R/'DATOS/apoyo_continuo.json').write_text(json.dumps(dict(method=__doc__,radius_m=.35,padding_bound_m=.008,upward_contact_component_bound=.50,vertical_separation_bound_m=.179,results=out),indent=2,ensure_ascii=False),encoding='utf8')
