import numpy as np,json,collections,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'HERRAMIENTAS'))
from scipy.spatial import cKDTree
def points(label):
 z=np.load(R/'DATOS'/f'{label}_geometria.npz');return z['vertices'][np.unique(z['triangles'])]
def distances(a,b):
 aa=cKDTree(b).query(a)[0];bb=cKDTree(a).query(b)[0];return dict(a_to_b_max=float(aa.max()),b_to_a_max=float(bb.max()),a_to_b_median=float(np.median(aa)),b_to_a_median=float(np.median(bb)),a_points=len(a),b_points=len(b),method='bidirectional nearest vertices; not surface Hausdorff or UV equality')
out={}
for label in ['coleccion_glb','puente_blend','puente_glb','puente_max','puente_max_desktop']:
 source='coleccion' if label=='coleccion_glb' else 'puente_obj';a=points(source);b=points(label)
 if label.startswith('puente_max'):
  a=a*1.50813535+np.array([-.11236,1.875563,-.466607]);out[label]=dict(transform='MAX = OBJ * 1.50813535 + (-0.11236,1.875563,-0.466607), hypothesis from VOY02, rechecked now',**distances(a,b))
 else:out[label]=distances(a,b)
rows=json.loads((R/'DATOS/inventario_puertas_accesos.json').read_text());groups=collections.defaultdict(list)
for x in rows:
 e=x.get('front_surface_envelope');w=e['width'] if e else x['width'];h=e['height'] if e else x['height'];key=(x['kind'],None if w is None else round(w,3),None if h is None else round(h,3));groups[key].append(x['id'])
dim=[]
for i,(key,ix) in enumerate(sorted(groups.items(),key=lambda x:str(x[0])),1):
 code=f'GD_{i:02}';dim.append(dict(id=code,kind=key[0],width=key[1],height=key[2],members=ix,meaning='dimensional envelope at 1 mm; NOT complete geometry identity'))
 for x in rows:
  if x['id'] in ix:x['dimensional_group']=code
# Source component fingerprints only detect identical translation-normalized vertex clouds.
objects=json.loads((R/'DATOS/coleccion_auditoria.json').read_text())['objects'];exact=collections.defaultdict(list)
for o in objects:exact[o['fingerprint_translation_only']].append(o['object'])
out['native_exact_translation_duplicates']=[x for x in exact.values() if len(x)>1]
out['identity_limit']='Rotation/reflection, UV and material identity are not implied by a point cloud or dimensional match.'
(R/'DATOS/contraste_formatos_actual.json').write_text(json.dumps(out,indent=2),encoding='utf8');(R/'DATOS/grupos_dimensionales.json').write_text(json.dumps(dim,indent=2,ensure_ascii=False),encoding='utf8')
(R/'DATOS/inventario_puertas_accesos.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
summary=json.loads((R/'DATOS/recuentos.json').read_text());summary['dimensional_groups']=len(dim);(R/'DATOS/recuentos.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
print(json.dumps(out,indent=2));print('grupos dimensionales',len(dim))
