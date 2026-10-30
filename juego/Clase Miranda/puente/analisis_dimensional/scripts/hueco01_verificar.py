import bpy,json,sys,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent))
from seis_sillas_comun import extra_snapshot
R=Path(__file__).resolve().parents[1]/'hueco_superior_01';m=json.loads((R/'reparacion_manifest.json').read_text(encoding='utf-8'));after=json.loads(json.dumps(extra_snapshot()));errors=[]
expected=m['snapshot_after']
for k in expected:
 if after[k]!=expected[k]:errors.append(k)
source=Path(m['source']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if sha(source)!=m['source_sha256']:errors.append('source_hash_changed_externally')
N=Vector((math.cos(math.radians(10)),math.sin(math.radians(10)),0));T=Vector((-N.y,N.x,0))
vs=[];fs=[]
for name in ['Plane.004_0','Plane.039_0']:
 o=bpy.data.objects[name];offset=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices);fs.extend(tuple(offset+i for i in p.vertices) for p in o.data.polygons)
tree=BVHTree.FromPolygons(vs,fs)
checks={}
for side,depth,direction in [('puente',-6.8,-N),('cabina',-7.6,N)]:
 rows=[]
 for i in range(33):
  s=-7.78+1.23*i/32
  for j in range(33):
   z=m['header_min_m']+.002+(3.88-m['header_min_m']-.002)*j/32;origin=T*s+N*depth+Vector((0,0,z));hit=tree.ray_cast(origin,direction,1)
   rows.append(hit[0] is not None and hit[1].dot(direction)<-.98)
 checks[side]={'rays':len(rows),'closed_with_outward_normal':sum(rows),'pass':all(rows)}
 if not all(rows):errors.append('closure_'+side)
o=bpy.data.objects['Plane.039_0'];zs=[(o.matrix_world@v.co).z for v in o.data.vertices];header=min(z for z in zs if 3.005<z<3.02)
if header<m['door_top_m']+.00049:errors.append('header_enters_door_envelope')
old=json.loads((R/'inspeccion.json').read_text(encoding='utf-8'))['objects']['Plane.039_0'];flip=[];zero=[]
for p in o.data.polygons:
 norm=(o.matrix_world.to_3x3().inverted().transposed()@p.normal).normalized();oldnorm=Vector(old['faces'][p.index]['normal_world'])
 if norm.dot(oldnorm)<.99:flip.append(p.index)
 if p.area<1e-12:zero.append(p.index)
if flip or zero:errors.append('normal_or_degenerate_face')
out={'ok':not errors,'errors':errors,'source_sha256_unchanged':sha(source)==m['source_sha256'],'output_sha256':sha(Path(bpy.data.filepath)),'snapshot_differences':errors,'objects':len(bpy.data.objects),'modified_objects':['Plane.039_0'],'created_objects':[],'six_chair_objects_and_meshes_unchanged':after['objects']==expected['objects'] and all(v==expected['meshes'][k] for k,v in after['meshes'].items() if k!=m['modified_mesh']),'materials_images_uv_assignments_unchanged':all(after[k]==expected[k] for k in ['materials','images','assignments_all','image_paths']),'closure_rays':checks,'door_clearance_m':header-m['door_top_m'],'flipped_faces':flip,'degenerate_faces':zero}
(R/'verificacion_reapertura.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print('VERIFY',json.dumps(out),flush=True)
