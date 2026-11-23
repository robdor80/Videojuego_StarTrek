import json,sys,math,csv,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import *;from importlib import import_module
kin=import_module('06_cinematica');results=[];poses=[]
search=json.loads((R/'DATOS/busqueda_recorrido.json').read_text())
for H in [1.6,1.75,1.9]:
 c=next(x for x in kin.CONFIG if x['H']==H);D=max(min(x['D'] for x in search if x['H']==hh and not x['failed_samples']) for hh in [1.6,1.75,1.9]);e=Env().adapted(c['drop'],.18).rail(D);fail=[];seq=[]
 # Empty pullback, approach/sit/work/stand/exit, then empty return.
 for frame in range(1,302):
  u=(frame-1)/30.
  if u<1:
   b,s=kin.posture(H,0,D);s['retreat']=D*u;s['phase']='retirada_vacia'
  elif u>9:
   b,s=kin.posture(H,8,D);s['retreat']=D*(10-u);s['phase']='retorno_vacio'
  else:b,s=kin.posture(H,u-1,D)
  r=e.test(b,chair_delta=(0,-s['retreat'],0));seq.append(dict(frame=frame,u=u,state=s,body=serial(b)))
  if not r['clear']:fail.append(dict(frame=frame,u=u,**r))
 summary=dict(H=H,D=D,drop=c['drop'],backshift=.18,samples=301,failed_samples=len(fail),failures=fail,complete_sampled_body_clear=not fail,interpolation_continuously_certified=False)
 results.append(summary);poses.append(dict(H=H,config=summary,poses=seq));print('DENSE',H,D,len(fail),flush=True)
(R/'DATOS/trayectorias.json').write_text(json.dumps(poses,indent=2));(R/'DATOS/resultados_cinematica.json').write_text(json.dumps(results,indent=2))
with (R/'DATOS/recorridos.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['altura_m','frame','fase','retirada_m','descenso_m','cadera_x','cadera_y','cadera_z'])
 for seq in poses:
  for p in seq['poses']:w.writerow([seq['H'],p['frame'],p['state']['phase'],p['state']['retreat'],p['state']['drop'],*p['body']['joints']['hip']])
