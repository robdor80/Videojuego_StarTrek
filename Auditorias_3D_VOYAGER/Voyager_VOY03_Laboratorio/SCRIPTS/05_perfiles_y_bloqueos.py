import sys,json,math,csv
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World
w=World();meta=json.loads((R/'DATOS/obj_objetos.json').read_text());source={o['name']:o for o in meta};profiles=[]
for side,n1,n2 in [('DERECHA','Mesh_1860','Mesh_1862'),('IZQUIERDA','Mesh_1861','Mesh_1863')]:
 center=lambda n:(np.array(source[n]['bounds_min'])+source[n]['bounds_max'])*.55
 c1=center(n1);c2=center(n2);direction=c2-c1;direction[2]=0;run=np.linalg.norm(direction);direction/=run;lateral=np.array([-direction[1],direction[0],0]);rows=[]
 for u in np.arange(-.9,.91,.005):
  p=c1+direction*u;s=w.state(*p[:2]);f=w.floor(*p[:2]);rows.append(dict(u_m=float(u),xy=p[:2].tolist(),floor=f,state=s))
 profiles.append(dict(id=side,origin=c1.tolist(),up_axis=direction.tolist(),lateral_axis=lateral.tolist(),between_tread_centers_m=run,rows=rows))
 print('PROFILE',side,'origin',c1,'axis',direction,'run',run,flush=True)
 prev=None
 for row in rows:
  state=row['state'];key=(row['floor']['object'] if row['floor'] else None,round(row['floor']['z'],4) if row['floor'] else None,state['valid'],tuple(state.get('blocks',[])),state.get('reason'))
  if key!=prev:print(round(row['u_m'],3),key,flush=True);prev=key
nav=[]
for x in [-1.9,-1.7,-1.5,-1.3,-.8,0,.8,1.3,1.5,1.7,1.9]:
 for y in [-3.2,-2.9,-2.6,-2.4,-2.2,-2.0,-1.8,-1.6]:
  s=w.state(x,y)
  nav.append(dict(x=x,y=y,**s))
print('NAV_FREE',[(p['x'],p['y'],p.get('floor',{}).get('z')) for p in nav if p['valid']],flush=True)
(R/'DATOS/perfiles_escaleras.json').write_text(json.dumps(dict(profiles=profiles,navigation_probes=nav),indent=2,ensure_ascii=False),encoding='utf8')
