import sys,json,collections
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'))
from walkgeom import World,dense_xy
from geom import Collision
w=World();routes=json.loads((R/'DATOS/rutas_originales_candidatas.json').read_text())['routes'];rows=[]
for r in routes:
 xy=dense_xy(r['xy_path'],.01);blocked=[];hits=collections.Counter()
 for i,p in enumerate(xy):
  f=w.floor(*p)
  if not f:continue
  # Deliberately reproduces fixed foot 2mm above selected centre floor.
  result=w.raw_pose([*p,f['z']+.002]);
  if not result['clear']:blocked.append(i);hits.update(result['blocks'])
 rows.append(dict(id=r['id'],samples=len(xy),fixed_foot_blocked_samples=len(blocked),first_blocked_samples=blocked[:30],obstacles=hits.most_common(15),meaning='Negative control: no stair solver, same mesh, same 10mm samples; not a new routing failure.'))
(R/'DATOS/comparacion_algoritmos.json').write_text(json.dumps(dict(results=rows,notes='VOY02 coarse graph was not a physical step-up solver. This control isolates that restriction at 10mm. Material selection, diagonal edge and float robustness errors are separately documented.'),indent=2,ensure_ascii=False),encoding='utf8')
print(rows,flush=True)
