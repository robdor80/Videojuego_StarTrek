import json,sys,shutil,numpy as np
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from bodygeom import *;from importlib import import_module
k=import_module('06_cinematica')
for name in ['trayectorias','resultados_cinematica']:
 src=R/'DATOS'/f'{name}.json';dest=R/'DATOS'/f'{name}_A1_FALLO_GUIA.json';assert not dest.exists();shutil.copy2(src,dest)
seqs=json.loads((R/'DATOS/trayectorias.json').read_text());results=[]
for seq in seqs:
 H=seq['H'];cfg=seq['config'];e=Env().adapted(cfg['drop'],cfg['backshift']).rail(cfg['D']);affected={p['frame'] for p in seq['poses'] if 'aproximacion' in p['state']['phase']};fail=[f for f in cfg['failures'] if f['frame'] not in affected]
 for p in seq['poses']:
  if p['frame'] not in affected:continue
  b,state=k.posture(H,p['u']-1,cfg['D']);r=e.test(b,chair_delta=(0,-state['retreat'],0));p['body']=serial(b);p['state']=state
  if not r['clear']:fail.append(dict(frame=p['frame'],u=p['u'],**r))
 cfg.update(failed_samples=len(fail),failures=fail,complete_sampled_body_clear=not fail,rechecked_step_frames=len(affected),adaptation='A2: explicit foot lift over proposed guide; retains A1 failures');results.append(cfg);print('CORRECCION_GUIA',H,len(affected),len(fail),flush=True)
(R/'DATOS/trayectorias.json').write_text(json.dumps(seqs,indent=2));(R/'DATOS/resultados_cinematica.json').write_text(json.dumps(results,indent=2))
