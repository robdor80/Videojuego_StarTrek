import sys,json,itertools
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import Env,make_body,serial
e=Env();out=[];chosen=[];floor=.0233257818-e.P[2]
for H in [1.6,1.75,1.9]:
 for retreat,hy,lean in itertools.product([0,.05,.10,.15,.2],[-.08,-.04,0.],[0,.10,.20]):
  # Feet on measured bridge floor; horizontal thighs and vertical shins, fixed segment lengths.
  z=floor+.290*H;hip=np.array([0,hy-retreat,z]);ankles=[[s*.055*H,hip[1]+.245*H,floor+.045*H] for s in [-1,1]];drop=.043*H+.004-z
  hands=[[s*.16,.355,.265] for s in [-1,1]];b=make_body(H,hip,ankles,lean,hands);r=e.test(b,chair_delta=(0,-retreat,-drop));out.append(dict(H=H,retreat=retreat,hip_y=hy,lean=lean,drop=drop,**r))
 for r in sorted([x for x in out if x['H']==H],key=lambda x:(len(x['interferences'])+len(x['invalid_ik']),x['retreat'],abs(x['hip_y']+.04),x['lean']))[:5]:print(r,flush=True)
 valid=[x for x in out if x['H']==H and x['clear']]
 if valid:
  r=sorted(valid,key=lambda x:(x['retreat'],abs(x['hip_y']+.04),x['lean']))[0];chosen.append(r)
 print('VALID',H,len(valid),flush=True)
(R/'DATOS/ajustes_busqueda.json').write_text(json.dumps(out,indent=2));(R/'DATOS/ajustes_elegidos.json').write_text(json.dumps(chosen,indent=2))
