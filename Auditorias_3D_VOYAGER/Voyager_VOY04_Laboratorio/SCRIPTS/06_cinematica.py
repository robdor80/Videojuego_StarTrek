import json,sys,math,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import *
CONFIG=json.loads((R/'DATOS/ajustes_elegidos.json').read_text())
def control_targets(H):
 out=[]
 for side,n,d in [(-1,[.0512874021326899,-.41714875410930163,.9073899488794975],.03300586345665679),(1,[-.037632226431561916,-.4186059003315652,.9073879631896178],.03272133206405911)]:
  n=np.array(n);x=side*.16;y=.405;z=(d-n[0]*x-n[1]*y)/n[2];out.append(np.array([x,y,z])+n*(.018*H+.002))
 return out
def posture(H,u,D=.5,backshift=.18):
 c=next(x for x in CONFIG if x['H']==H);hy=c['hip_y'];drop=c['drop'];floor=.0233257818-.6298899146742544;seat_hip=floor+.290*H;standing=floor+.53*H
 # 0-1 approach from port, 1-2 sit, 2-3 glide occupied, 3-4 place hands/work.
 u=max(0,min(8,u));v=u if u<=4 else 8-u;retreat=D
 if v<1:
  t=v;x=-.65*(1-t);hip=np.array([x,hy+.245*H-D,standing]);ankles=[]
  for side in [-1,1]:
   footx=x+side*.055*H;step=.040*float(np.clip((.087-abs(footx))/.035,0,1));ankles.append([footx,hip[1],floor+.045*H+step])
  lean=0.;phase='aproximacion_paso_sobre_guia'
 elif v<2:
  t=v-1;hip=np.array([0,hy+.245*H*(1-t)-D,standing+(seat_hip-standing)*t]);ankles=[[s*.055*H,hy+.245*H-D,floor+.045*H] for s in [-1,1]];lean=.30*math.sin(math.pi*t);phase='sentarse'
 elif v<3:
  t=v-2;retreat=D*(1-t);hip=np.array([0,hy-retreat,seat_hip]);ankles=[[s*.055*H,hip[1]+.245*H,floor+.045*H+.035*math.sin(math.pi*t)] for s in [-1,1]];lean=0.;phase='traslacion_ocupada'
 else:
  t=v-3;retreat=0.;hip=np.array([0,hy,seat_hip]);ankles=[[s*.055*H,hy+.245*H,floor+.045*H] for s in [-1,1]];lean=0.;phase='manos_trabajo'
 # Retract hands during access; blend to screen only after chair is in working pose.
 hands=[hip+np.array([s*.13*H,-.03,.04*H]) for s in [-1,1]]
 if v>=3:
  t=v-3;hands=[(1-t)*h+t*target+np.array([0,0,.16*math.sin(math.pi*t)]) for h,target in zip(hands,control_targets(H))]
 b=make_body(H,hip,ankles,lean,hands)
 return b,dict(retreat=retreat,drop=drop,backshift=backshift,phase=phase if u<=4 else 'salida_'+phase)
if __name__=='__main__':
 out=[]
 for H in [1.6,1.75,1.9]:
  c=next(x for x in CONFIG if x['H']==H);e=Env().adapted(c['drop'],.18)
  for D in [.2,.3,.4,.5,.6]:
   fail=[]
   for u in np.linspace(0,4,49):
    b,s=posture(H,u,D);r=e.test(b,chair_delta=(0,-s['retreat'],0))
    if not r['clear']:fail.append(dict(u=float(u),phase=s['phase'],**r))
   q=dict(H=H,D=D,failed_samples=len(fail),failures=fail);out.append(q);print('PATH',H,D,len(fail),[(x['u'],[(a['part'],a['objects']) for a in x['interferences']],x['invalid_ik']) for x in fail[:3]],flush=True)
 (R/'DATOS/busqueda_recorrido.json').write_text(json.dumps(out,indent=2))
