import sys,json,itertools,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import *
e=Env();floor=.0233257818-e.P[2];out=[]
for H in [1.6,1.75,1.9]:
 c=next(x for x in json.loads((R/'DATOS/ajustes_elegidos.json').read_text()) if x['H']==H)
 for x,y in itertools.product([-.9,-.6,-.4,0.],[0.,.35,.5,.65]):
  hip=[x,y,floor+.53*H];ankles=[[x+s*.055*H,y,floor+.045*H] for s in [-1,1]];b=make_body(H,hip,ankles);r=e.test(b,chair_delta=(0,0,-c['drop']));out.append(dict(H=H,x=x,y=y,**r))
 print(H,[(r['x'],r['y'],r['clear'],[(a['part'],a['objects']) for a in r['interferences']]) for r in out if r['H']==H],flush=True)
(R/'DATOS/sondeo_aproximacion.json').write_text(json.dumps(out,indent=2))
