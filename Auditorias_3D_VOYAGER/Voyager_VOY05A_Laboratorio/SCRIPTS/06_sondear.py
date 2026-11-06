import json,collections,math
import numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def ray(tri,p,d,limit=100):
 p=np.asarray(p,float);d=np.asarray(d,float);e1=tri[:,1]-tri[:,0];e2=tri[:,2]-tri[:,0];h=np.cross(d,e2);det=np.einsum('ij,ij->i',e1,h);valid=np.abs(det)>1e-12;inv=np.divide(1,det,out=np.zeros_like(det),where=valid);s=p-tri[:,0];u=np.einsum('ij,ij->i',s,h)*inv;q=np.cross(s,e1);vv=q@d*inv;dist=np.einsum('ij,ij->i',e2,q)*inv;valid&=(u>=-1e-7)&(vv>=-1e-7)&(u+vv<=1+1e-7)&(dist>1e-6)&(dist<=limit)
 if not valid.any():return None
 ds=np.where(valid,dist,np.inf);k=int(ds.argmin());return dict(distance=float(ds[k]),point=(p+d*ds[k]).tolist(),triangle=k)
def geometry(label):
 z=np.load(R/'DATOS'/f'{label}_geometria.npz');a=json.loads((R/'DATOS'/f'{label}_auditoria.json').read_text());return z['vertices'][z['triangles']],z['object_ids'],a
def ports():
 tri,ids,a=geometry('coleccion');rows=[];surfaces=[]
 for i,o in enumerate(a['objects']):
  tr=tri[ids==i];lo=tr.min((0,1));hi=tr.max((0,1));c=(lo+hi)/2;floor=ray(tr,[*c[:2],lo[2]+min((hi[2]-lo[2])*.5,1.)],[0,0,-1],3);fz=floor['point'][2] if floor else lo[2]
  for ax,side,code in [(0,-1,'XM'),(0,1,'XP'),(1,-1,'YM'),(1,1,'YP')]:
   normal=np.eye(3)[ax]*side;tangent=np.array([-normal[1],normal[0],0]);p=c.copy();p[ax]=lo[ax] if side<0 else hi[ax];p[2]=fz;inside=p-normal*.08;fr=ray(tr,inside+[0,0,.65],[0,0,-1],2);fl=fr['point'][2] if fr else None
   block=[];widths=[]
   for z in [.4,1,1.7,2.2]:
    aa=p-normal*.06+[0,0,z];block.append(ray(tr,aa,normal,.12) is not None);aa=inside+[0,0,z];l=ray(tr,aa,-tangent,12);r=ray(tr,aa,tangent,12);widths.append(l['distance']+r['distance'] if l and r else None)
   ceil=ray(tr,inside+[0,0,1.5],[0,0,1],5)
   candidate=not any(block[:3]) and fl is not None and abs(fl-fz)<.05 and all(w is not None and w>=.65 for w in widths[:3])
   rows.append(dict(id=f'P_{o["object"]}_{code}',object=o['object'],code=code,point=p.tolist(),normal=normal.tolist(),tangent=tangent.tolist(),floor_z=fl,ceiling_z=ceil['point'][2] if ceil else None,widths_z040_100_170_220=widths,blocked_z040_100_170_220=block,open_candidate=bool(candidate),method='fresh four cardinal centerline rays; candidate not exhaustive for off-center or diagonal ports'))
  # Coplanar vertical surfaces, grouped by orientation and plane. Diagnostic candidates, not semantic doors.
  n=np.cross(tr[:,1]-tr[:,0],tr[:,2]-tr[:,0]);areas=np.linalg.norm(n,axis=1)/2;n=np.divide(n,2*areas[:,None],out=np.zeros_like(n),where=areas[:,None]>1e-12);groups=collections.defaultdict(list)
  for j,nn in enumerate(n):
   if abs(nn[2])>.001 or areas[j]<1e-7:continue
   if nn[np.argmax(np.abs(nn))]<0:nn=-nn
   plane=tr[j,0]@nn;key=(*np.round(nn,4),round(plane,4));groups[key].append(j)
  for key,ix in groups.items():
   nn=np.array(key[:3]);tangent=np.array([-nn[1],nn[0],0]);pv=tr[ix].reshape(-1,3);u=pv@tangent;zz=pv[:,2];w=float(np.ptp(u));h=float(np.ptp(zz));area=float(areas[ix].sum())
   if .35<w<3.3 and .45<h<3.5 and area>.1:
    surfaces.append(dict(id=f'S_{o["object"]}_{len(surfaces):04}',object=o['object'],normal=nn.tolist(),plane=key[3],tangent=tangent.tolist(),u_min=float(u.min()),u_max=float(u.max()),z_min=float(zz.min()),z_max=float(zz.max()),width=w,height=h,area=area,triangles=ix,center=(nn*key[3]+tangent*(u.min()+u.max())/2+[0,0,(zz.min()+zz.max())/2]).tolist()))
 (R/'DATOS/puertos_sondeo_actual.json').write_text(json.dumps(rows,indent=2),encoding='utf8');(R/'DATOS/superficies_candidatas.json').write_text(json.dumps(surfaces,indent=2),encoding='utf8')
 print('PUERTOS',sum(x['open_candidate'] for x in rows),'SUPERFICIES',len(surfaces))
 for o in ['Mesh3','Mesh4','Mesh5','Mesh6','Mesh7','Mesh9','Mesh10','Mesh11','Mesh14','Mesh27','Mesh28','Mesh53','Mesh55','Mesh93','Mesh103']:
  print(o,[(s['id'],[round(x,4) for x in s['normal']],round(s['plane'],4),round(s['width'],4),round(s['height'],4),round(s['area'],4)) for s in surfaces if s['object']==o])
if __name__=='__main__':ports()
