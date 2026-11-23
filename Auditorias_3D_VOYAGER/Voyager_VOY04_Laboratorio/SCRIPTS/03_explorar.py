import sys,json,itertools,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import Env,make_body,serial
e=Env();out=[]
for H in [1.6,1.75,1.9]:
 for retreat,drop,lean in itertools.product([0,.1,.2,.3],[0,.1,.18],[0,.15]):
  hip=np.array([0,-.15-retreat,.043*H+.003-drop]);footz=hip[2]-.245*H-.045*H
  # Horizontal thigh, vertical shin, feet located relative to actual seat and floor.
  ankles=[[s*.055*H,hip[1]+.245*H,hip[2]-.245*H] for s in [-1,1]];b=make_body(H,hip,ankles,lean);r=e.test(b,chair_delta=(0,-retreat,-drop));out.append(dict(H=H,retreat=retreat,drop=drop,lean=lean,foot_sole_above_floor_m=footz-e.floor,**r))
 # Baseline artifact retains the failure.
 hip=[0,-.15,.043*H+.003];ankles=[[s*.055*H,-.15+.245*H,hip[2]-.245*H] for s in [-1,1]]
 b=make_body(H,hip,ankles);(R/'DATOS'/f'original_{H:.2f}.json').write_text(json.dumps(dict(body=serial(b),test=e.test(b,details=True)),indent=2))
(R/'DATOS/exploracion_posturas.json').write_text(json.dumps(out,indent=2));
for H in [1.6,1.75,1.9]:
 print('HEIGHT',H,flush=True)
 for r in sorted([x for x in out if x['H']==H],key=lambda x:(len(x['interferences'])+len(x['invalid_ik']),-x['minimum_clearance_m']))[:8]:print(r,flush=True)
