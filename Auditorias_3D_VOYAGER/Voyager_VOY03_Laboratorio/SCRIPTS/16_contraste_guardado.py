"""New VOY03 saved-file comparison, including every collision component.
No old-stage checks or source-file mutations. Float tolerance inherited and
kept explicit; the capsule margins and results are not inferred from this test.
"""
import bpy,json,sys,hashlib,itertools
import numpy as np
from pathlib import Path
from mathutils.kdtree import KDTree
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'SCRIPTS'));from geom import point_tri_sq
path=R/'ESCENAS/VOY03_Circulacion.blend';before=hashlib.sha256(path.read_bytes()).hexdigest();manifest=json.loads((R/'DATOS/manifest_blender.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);s=bpy.data.scenes['04_RECORRIDOS_COMPLETOS'];bpy.context.window.scene=s;s.view_layers[0].update();data=np.load(R/'DATOS/prototipo_geometria.npz');tri=data['triangles'];labels=data['labels'];expected=set(labels.tolist());rows=[];tol=2e-5
def fingerprint(o):
 h=hashlib.sha256();v=np.empty(len(o.data.vertices)*3,np.float32);o.data.vertices.foreach_get('co',v);h.update(v.tobytes());h.update(np.array(o.matrix_world,dtype=np.float64).tobytes());h.update(str([(tuple(p.vertices),p.material_index) for p in o.data.polygons]).encode());return h.hexdigest()
for o in s.objects:
 if o.name not in manifest['architecture_fingerprints']:continue
 me=o.data;me.calc_loop_triangles();v=np.array([o.matrix_world@p.co for p in me.vertices]);b=v[np.array([t.vertices[:] for t in me.loop_triangles],int)];src=o.get('VOY02_ORIGEN','');key='PUENTE:'+src[4:] if src.startswith('OBJ:') else o.get('VOY02_INSTANCE') or o.name
 assert key in expected,(o.name,key)
 a=tri[labels==key];same=a.shape==b.shape;err=None
 if same:
  kd=KDTree(len(b))
  for i,p in enumerate(b.mean(axis=1)):kd.insert(p,i)
  kd.balance();ix=np.array([kd.find(p)[1] for p in a.mean(axis=1)],int);errors=np.stack([np.max(np.abs(a-b[ix][:,perm,:]),axis=(1,2)) for perm in itertools.permutations(range(3))]);best=errors.min(axis=0)
  for i in np.flatnonzero(best>tol):
   candidates=[x[1] for x in kd.find_range(a[i].mean(axis=0),tol*2)]
   if candidates:best[i]=min(float(np.max(np.abs(a[i]-b[j][list(perm)]))) for j in candidates for perm in itertools.permutations(range(3)))
  err=float(best.max())
  if err>tol and len(a)<100:
   def surf(x,y):return float(max(np.sqrt(point_tri_sq(p,y).min()) for p in np.vstack((x.reshape(-1,3),x.mean(axis=1)))))
   err=max(surf(a,b),surf(b,a))
 rows.append(dict(object=o.name,label=key,triangles=len(b),error_m=err,pass_test=same and err<=tol,fingerprint_matches_source=fingerprint(o)==manifest['architecture_fingerprints'][o.name]))
scene_checks=[]
for sc in bpy.data.scenes:
 scene_checks.append(dict(name=sc.name,geometry_objects=sum(o.name in manifest['architecture_fingerprints'] for o in sc.objects),all_fingerprints_match=all(fingerprint(o)==manifest['architecture_fingerprints'][o.name] for o in sc.objects if o.name in manifest['architecture_fingerprints'])))
missing=sorted(expected-set(r['label'] for r in rows));after=hashlib.sha256(path.read_bytes()).hexdigest();out=dict(file=str(path),sha256=after,file_unchanged=before==after,tolerance_m=tol,reason='20um accounts for float world transforms of native library coordinates; actual maximum reported per object.',objects=rows,missing_labels=missing,scenes=scene_checks,scene_names_match=set(s.name for s in bpy.data.scenes)==set(manifest['scenes']),packed_images=sum(bool(im.packed_file) for im in bpy.data.images),all_geometry_matches=not missing and all(r['pass_test'] and r['fingerprint_matches_source'] for r in rows) and all(s['all_fingerprints_match'] and s['geometry_objects']==645 for s in scene_checks))
(R/'DATOS/contraste_VOY03.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8');print('SAVED_GEOMETRY',len(rows),out['all_geometry_matches'],'MAX_ERROR',max(r['error_m'] for r in rows),'SCENES',scene_checks,flush=True);assert out['all_geometry_matches'] and out['file_unchanged'] and out['scene_names_match']
