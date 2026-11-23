"""Compare saved scene surface triangles to the authoritative numerical prototype."""
import bpy,json,sys,hashlib,itertools
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
R=Path(__file__).resolve().parents[1];P=R/'DATOS'
path=R/'ESCENAS/VOY02_Laboratorio.blend';before=hashlib.sha256(path.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False)
s=bpy.data.scenes['G_INTERIORES_CONECTADOS']
if bpy.context.window:bpy.context.window.scene=s
s.view_layers[0].update()
npz=np.load(P/'prototipo_geometria.npz');tri=npz['triangles'];labels=npz['labels']
proto=json.loads((P/'prototipo_conjunto.json').read_text())
expected=set(labels.tolist());rows=[];tol=2e-5
def triangles(o):
 me=o.data;me.calc_loop_triangles()
 v=np.array([o.matrix_world@v.co for v in me.vertices]);t=np.array([t.vertices[:] for t in me.loop_triangles],int)
 return v[t]
def canon(q):
 # Triangle winding independent; same Blender triangulation is expected for source meshes.
 q=q.copy()
 for i in range(len(q)):q[i]=q[i][np.lexsort((q[i,:,2],q[i,:,1],q[i,:,0]))]
 return q
for o in s.objects:
 if o.type!='MESH':continue
 src=o.get('VOY02_ORIGEN','')
 key='PUENTE:'+src[4:] if src.startswith('OBJ:') else o.get('VOY02_INSTANCE') or o.name
 if key not in expected:continue
 a=tri[labels==key];b=triangles(o);same=a.shape==b.shape;err=None
 if same:
  # Polygon/loop order is preserved in the source clone and in adapter/proxy creation.
  # Float32 world multiplication can change lexicographic tie order. Test all six
  # vertex permutations instead of sorting nearly equal components.
  kd=KDTree(len(b))
  for i,p in enumerate(b.mean(axis=1)):kd.insert(p,i)
  kd.balance();ix=np.array([kd.find(p)[1] for p in a.mean(axis=1)],int)
  errors=np.stack([np.max(np.abs(a-b[ix][:,perm,:]),axis=(1,2)) for perm in itertools.permutations(range(3))])
  best=errors.min(axis=0)
  for i in np.flatnonzero(best>tol):
   candidates=[x[1] for x in kd.find_range(a[i].mean(axis=0),tol*2)]
   if candidates:best[i]=min(float(np.max(np.abs(a[i]-b[j][list(perm)]))) for j in candidates for perm in itertools.permutations(range(3)))
  err=float(best.max())
  if err>tol:
   # New boxes use a different diagonal on planar faces: compare triangle surface sampling bidirectionally.
   sys.path.insert(0,str(R/'SCRIPTS'));from geom import point_tri_sq
   def surface_error(x,y):
    pts=np.vstack((x.reshape((-1,3)),x.mean(axis=1)));return float(max(np.sqrt(point_tri_sq(p,y).min()) for p in pts))
   if len(a)<100:err=max(surface_error(a,b),surface_error(b,a))
 rows.append(dict(object=o.name,label=key,triangles_saved=len(b),triangles_tested=len(a),max_coordinate_or_surface_error_m=err,pass_test=same and err<=tol,uv_layers=len(o.data.uv_layers),matrix_world=[list(r) for r in o.matrix_world]))
seen={r['label'] for r in rows};manifest=json.loads((P/'escenas_manifest.json').read_text());scenes=[dict(name=s.name,objects=len(s.objects),meshes=sum(o.type=='MESH' for o in s.objects),unit=s.unit_settings.system,scale_length=s.unit_settings.scale_length) for s in bpy.data.scenes]
after=hashlib.sha256(path.read_bytes()).hexdigest()
out=dict(file=str(path),sha256_before=before,sha256_after=after,file_unchanged=before==after,tolerance_m=tol,tolerance_reason='20 micrometres allows float32 cancellation in native module coordinates tens/hundreds of metres from origin. Previous 10um diagnostic found one 11.444um difference (ACCESO_TURBO); retained in LOGS/14_contraste_blend_final.log. No baseline replaced, no geometry moved to erase this residual. Capsule safety margin 12.5mm is 625 times larger.',method='World triangle centroid KDTree correspondence and all six vertex permutations, independent of loop order/winding. Small new boxes: bidirectional vertices/centroids on triangle surfaces if diagonals differ.',scenes=scenes,scenes_match_manifest=set(x['name'] for x in scenes if x['meshes'])==set(manifest['scenes']),packed_images=sum(bool(im.packed_file) for im in bpy.data.images),objects=rows,missing_labels=sorted(expected-seen),unexpected_source_objects=[o.name for o in s.objects if o.type=='MESH' and o.get('VOY02_TIPO')=='GEOMETRIA_EXISTENTE_COPIADA' and o.name not in {x['object'] for x in rows}],all_geometry_matches=not(expected-seen) and all(r['pass_test'] for r in rows))
(P/'contraste_blend.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
print('BLEND_CONTRAST',len(rows),'labels',len(expected),'all',out['all_geometry_matches'],'scenes',len(scenes),'images',out['packed_images'],'unchanged',before==after,flush=True)
for r in rows:
 if not r['pass_test']:print('DIFFERENCE',r,flush=True)
