"""Spatial accessibility screens, not building-code or wheelchair-motion certification."""
import sys,json,math
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import *
proto=json.loads((R/'DATOS/prototipo_conjunto.json').read_text());data=np.load(R/'DATOS/prototipo_geometria.npz');tri=data['triangles'];labels=data['labels'];cc=Collision(tri,labels)
def clip(poly,z,keepabove):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=a[2]>=z if keepabove else a[2]<=z;ib=b[2]>=z if keepabove else b[2]<=z
  if ia:out.append(a)
  if ia!=ib:out.append(a+(b-a)*((z-a[2])/(b[2]-a[2])))
 return out
def turn(p,radius=.75,height=1.35):
 p=np.array(p,float);lo=tri.min(axis=1);hi=tri.max(axis=1);sel=(hi[:,0]>=p[0]-radius)&(lo[:,0]<=p[0]+radius)&(hi[:,1]>=p[1]-radius)&(lo[:,1]<=p[1]+radius)&(hi[:,2]>p[2]+.025)&(lo[:,2]<p[2]+height);projected=[];labs=[]
 for q,l in zip(tri[sel],labels[sel]):
  poly=clip(list(q),p[2]+.025,True);poly=clip(poly,p[2]+height,False) if poly else []
  for i in range(1,len(poly)-1):
   qq=np.array([poly[0],poly[i],poly[i+1]]);qq[:,2]=0;projected.append(qq);labs.append(l)
 if projected:
  dist=np.sqrt(point_tri_sq([p[0],p[1],0],np.array(projected)));bad=dist<radius-1e-5;blocks=sorted(set(np.array(labs)[bad].tolist()))
 else:blocks=[]
 supports=[]
 for theta in np.arange(0,2*math.pi,math.pi/4):
  hit=ray(tri,[p[0]+radius*math.cos(theta),p[1]+radius*math.sin(theta),p[2]+.1],[0,0,-1],.2);supports.append(bool(hit and abs(hit['point'][2]-p[2])<=.01))
 return dict(center_m=p.tolist(),diameter_m=radius*2,vertical_envelope_m=height,clear=not blocks,blocking_objects=blocks,ring_support_hits=sum(supports),ring_probes=8,note='Vertical cylinder from foot+25mm to 1.35m; clipped triangle surfaces projected in XY. Eight support probes only. Not wheelchair kinematics or full solid containment.')
placements={p['id']:p for p in proto['placements']};room=np.array(placements['CAMAROTE_EXISTENTE']['translation']);hub=np.array(placements['CRUCE_CUATRO']['translation']);cab=np.array(placements['CABINA_TURBO']['translation']);turns=[]
for name,p in [('CRUCE',hub+[0,0,.002]),('CABINA',cab+[0,0,.002]),('CAMAROTE_CENTRO',room+[0,0,.002]),('CAMAROTE_JUNTO_CAMA',room+[.70,1.5,.002]),('CENTRO_PUENTE',np.array([0,-.7,.435856])*1.1+proto['bridge_translation']+[0,0,.002])]:turns.append(dict(id=name,**turn(p)))
# Actual free rays from the proxy bed edges toward room/furniture obstacles.
bed=next(p for p in proto['furniture_reference_only'] if p['id']=='REF_CAMA');center=np.array(bed['center']);size=np.array(bed['size']);context=tri[labels!='REF_CAMA'];sides=[]
for name,delta,direction in [('IZQUIERDA',[-size[0]/2-.001,0,0],[-1,0,0]),('DERECHA',[size[0]/2+.001,0,0],[1,0,0]),('PIES',[0,-size[1]/2-.001,0],[0,-1,0])]:
 hits=[]
 for z in [.10,.40,1.0,1.7]:
  p=center+delta;p[2]=room[2]+z;h=ray(context,p,direction,10);hits.append(dict(z_above_floor_m=z,free_ray_m=h['distance'] if h else None,label='Surface ray only; full transfer rectangle not certified'))
 sides.append(dict(side=name,probes=hits))
out=dict(turning_spaces=turns,bed_side_rays=sides,physical_accessibility_grade='E',reason='No continuous accessible route from central bridge, stair changes and narrow adaptive throat. Room clearances alone cannot certify disability access.',benchmark='CTE DB-SUA used only as human-scale design reference for 0.80m door, 1.50m turn, 0.90m bed transfer, 2.00m door height. No legal applicability to a game is asserted.',room_options=[dict(option='A_ADAPTAR_MESH4',grade='C',recommendation='Preferred spatial basis: existing shell, selected capsule route and floor/ceiling evidence; supply artistic fit, independent furniture, door and collision design.'),dict(option='B_FABRICAR_CON_MODULOS',grade='E',recommendation='Not fabricated in VOY-02; measured corridor interfaces can supply access, not proof of a complete room.'),dict(option='C_ESTANCIA_NUEVA',grade='E',recommendation='Artistically flexible; would require new room construction, UV/PBR, architecture and full spatial tests. No new production room created.')])
(R/'DATOS/accesibilidad_camarote.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8');print('TURN',[(x['id'],x['clear'],x['ring_support_hits'],x['blocking_objects']) for x in turns]);print('BED',sides)
