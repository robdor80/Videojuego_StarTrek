"""Local surface contacts at every prototype adapter, including constructive overlaps."""
import ast,sys,json,collections
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from geom import *
for file,functions in [('10_funcional.py',['tree','exact_overlap']),('16_investigar_carreras.py',['classify'])]:
 p=ast.parse((R/'SCRIPTS'/file).read_text());exec(compile(ast.Module(body=[x for x in p.body if isinstance(x,ast.FunctionDef) and x.name in functions],type_ignores=[]),file,'exec'))
data=np.load(R/'DATOS/prototipo_geometria.npz');tri=data['triangles'];labels=data['labels'];proto=json.loads((R/'DATOS/prototipo_conjunto.json').read_text());out=[]
for a in proto['adapters']:
 moving=labels==a['id'];q=tri[moving];fixed=tri[~moving];fn=labels[~moving];lo=q.min(axis=(0,1))-.001;hi=q.max(axis=(0,1))+.001;near=(fixed.max(axis=1)>=lo).all(axis=1)&(fixed.min(axis=1)<=hi).all(axis=1);fixed=fixed[near];fn=fn[near];pairs,broad=exact_overlap(q,fixed);details=[]
 if pairs:
  ix=np.array(pairs);trans,cop,depth=classify(q[ix[:,0]],fixed[ix[:,1]])
  for name in sorted(set(fn[ix[:,1]])):
   sel=fn[ix[:,1]]==name;details.append(dict(object=str(name),pairs=int(sel.sum()),transverse=int((trans&sel).sum()),coplanar=int((cop&sel).sum()),other=int((~(trans|cop)&sel).sum()),maximum_plane_crossing_m=float(depth[sel].max())))
 out.append(dict(id=a['id'],surface_pairs=len(pairs),contacts=details,grade='C',interpretation='Structural ends overlap/contact by construction; selected walking surface tests are separate. These counts do not approve moldings, watertight volumes or manufacturing clearance.'))
 print('ADAPTER_CONTACTS',a['id'],details,flush=True)
(R/'DATOS/encuentros_adaptadores.json').write_text(json.dumps(dict(adapters=out,analytic_capsule_controls=self_test(),method='All prototype triangles with BVH/SAT and same transverse/coplanar classification as door investigation. No architecture removed. Interior containment not solved.'),indent=2,ensure_ascii=False),encoding='utf8')
