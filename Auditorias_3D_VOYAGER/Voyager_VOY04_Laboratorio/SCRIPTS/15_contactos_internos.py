import ast,json,sys,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import Env
from mathutils.bvhtree import BVHTree
p=ast.parse((R/'SCRIPTS/09_mallas.py').read_text());q=ast.parse((R/'REFERENCIAS/VOY02_10_funcional.py').read_text());exec(compile(ast.Module(body=[x for x in q.body if isinstance(x,ast.FunctionDef) and x.name in ['tree','exact_overlap']]+[x for x in p.body if isinstance(x,ast.FunctionDef) and x.name=='classify'],type_ignores=[]),'<SAT>','exec'))
out=[];orientation=[]
for m in json.loads((R/'DATOS/inventario_medidas.json').read_text()):
 e=Env(m['id']);pairs=[];pieces={key:e.tri[e.names==key] for key in m['parts']}
 for i,key in enumerate(m['parts']):
  for other in m['parts'][i+1:]:
   A=pieces[key];B=pieces[other]
   if np.any(A.max((0,1))<B.min((0,1))-.000001) or np.any(B.max((0,1))<A.min((0,1))-.000001):continue
   pp,_=exact_overlap(A,B)
   if pp:
    ix=np.array(pp);t=classify(A[ix[:,0]],B[ix[:,1]]);pairs.append(dict(a=key,b=other,contact_pairs=len(pp),transverse_pairs=int(t.sum())))
 out.append(dict(id=m['id'],contacting_object_pairs=pairs,interpretation='Surface contacts and transverse crossings; not a solid penetration volume and not proof of a movable joint.'))
 if m['id']=='NAVEGACION':back='Layer__3'
 elif m['id']=='LATERAL_DER':back='Layer__4'
 elif m['id']=='LATERAL_IZQ':back='Layer__5'
 else:back='ChamferBox_25' if m['id']=='MANDO_IZQ' else 'ChamferBox_32'
 rr=next(x for x in m['pieces'] if x['key']==back);bc=(np.array(rr['lo'])+rr['hi'])/2;f=np.array(m['seat_point'])-bc;f[2]=0;f/=np.linalg.norm(f);angle=float(np.degrees(np.arccos(np.clip(np.dot(f,m['forward']),-1,1))));orientation.append(dict(id=m['id'],reference_basis_forward=m['forward'],independent_seat_minus_back_forward=f.tolist(),difference_deg=angle,basis_note='Coordinate frame retained for comparability, not a hinge axis inferred from object origin.'))
 print('INTERNAL',m['id'],len(pairs),flush=True)
(R/'DATOS/contactos_internos_originales.json').write_text(json.dumps(out,indent=2));(R/'DATOS/orientacion_contraste.json').write_text(json.dumps(orientation,indent=2))
