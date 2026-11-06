import json,sys,math,csv
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from geom import ray
d=np.load(R/'DATOS/geometria.npz');V=d['vertices'];F=d['triangles'];I=d['object_ids'];tri=V[F];rows=json.loads((R/'DATOS/objetos.json').read_text());st=json.loads((R/'REFERENCIAS/puestos_revision.json').read_text())['stations'];by={r['key']:r for r in rows}
def dump(n,d):(R/'DATOS'/n).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
measures=[]
for s in st:
 keys=s['refined_parts'];rr=[by[k] for k in keys];ch=tri[np.isin(I,[r['index'] for r in rr])];p=np.array(s['seat_reference_m']);f=np.array([*s['forward_xy'],0.]);u=np.array([-f[1],f[0],0]);basis=np.array([u,f,[0,0,1]]).T
 cushions=[r for r in rr if r['key'].startswith('ChamferBox')];zmin=min(r['lo'][2] for r in cushions);seatc=[r for r in cushions if r['lo'][2]<zmin+.03];ci=np.isin(I,[r['index'] for r in seatc]);seat_hit=ray(tri[ci],[p[0],p[1],max(r['hi'][2] for r in seatc)+.01],[0,0,-1],.3);zs=seat_hit['point'][2];p[2]=zs
 # Reuse VOY03 support identity, and ray actual triangles (not chair base or console).
 support=set(['Mesh_1856','Object_75','Mesh_1968','Mesh_1848','Mesh_2121','Mesh_2122','Mesh_2123','Mesh_2124','Mesh_1739','Mesh_1740','Mesh_1755','Mesh_1807','Mesh_1808','Mesh_1809','Mesh_1810','Mesh_1811']+[r['key'] for r in rows if 'Voygray' in r['materials']]);si=np.where(np.isin(I,[r['index'] for r in rows if r['key'] in support]))[0];hit=ray(tri[si],[p[0],p[1],zs-.04],[0,0,-1],2)
 floorz=hit['point'][2] if hit else None
 bounds=(ch.reshape(-1,3)-p)@basis
 pieces=[]
 for r in rr:
  q=(tri[I==r['index']].reshape(-1,3)-p)@basis
  pieces.append(dict(**r,local_lo=q.min(0).tolist(),local_hi=q.max(0).tolist(),dimensions=(q.max(0)-q.min(0)).tolist()))
 # Nearby screen objects are candidates only, not semantic assignment by distance alone.
 screens=[]
 for r in rows:
  if any(m and ('scrn' in m.lower() or 'screen' in m.lower()) for m in r['materials']):
   q=tri[I==r['index']].reshape(-1,3);c=q.mean(0);l=(c-p)@basis
   if np.linalg.norm(c-p)<2.5:
    screens.append(dict(key=r['key'],name=r['name'],center=c.tolist(),local_center=l.tolist(),distance=float(np.linalg.norm(c-p)),materials=r['materials']))
 m=dict(id=s['id'],parts=keys,seat_point=p.tolist(),floor_m=floorz,floor_object=rows[int(I[si[hit['triangle']]])]['key'] if hit else None,seat_above_floor_m=zs-floorz if hit else None,seat_cushion_keys=[r['key'] for r in seatc],basis=basis.tolist(),forward=f.tolist(),right=u.tolist(),local_bounds=[bounds.min(0).tolist(),bounds.max(0).tolist()],dimensions=(bounds.max(0)-bounds.min(0)).tolist(),pieces=pieces,near_screens=sorted(screens,key=lambda x:x['distance']))
 measures.append(m);print(s['id'],'seat',p,'floor',floorz,'height',m['seat_above_floor_m'],'dims',m['dimensions'],'screens',[(x['key'],np.round(x['local_center'],3).tolist()) for x in m['near_screens'][:8]])
dump('inventario_medidas.json',measures)
with (R/'DATOS/medidas_sillas.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['id','ancho_m','fondo_m','alto_m','asiento_z_m','suelo_z_m','altura_asiento_m','suelo_objeto','piezas']);w.writerows([[m['id'],*m['dimensions'],m['seat_point'][2],m['floor_m'],m['seat_above_floor_m'],m['floor_object'],len(m['parts'])] for m in measures])
for m in measures:
 if m['id']=='NAVEGACION':
  p=np.array(m['seat_point']);b=np.array(m['basis']);print('NEAR_NAV')
  for r in rows:
   q=(tri[I==r['index']].reshape(-1,3)-p)@b
   if q[:,0].min()<.8 and q[:,0].max()>-.8 and q[:,1].min()<1.3 and q[:,1].max()>-.6 and q[:,2].min()<1.3 and q[:,2].max()>-.1:
    print(r['key'],np.round(q.min(0),3),np.round(q.max(0),3),r['materials'])
