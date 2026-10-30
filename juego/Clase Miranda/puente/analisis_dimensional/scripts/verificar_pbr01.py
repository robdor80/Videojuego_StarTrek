"""Independent fresh-process reopening and integrity check. Never saves a blend."""
import bpy,sys,json,collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pbr01_integrity import *
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'datos/pbr01_manifest.json').read_text(encoding='utf-8'))
ORIGINAL=Path(manifest['original']);OUTPUT=Path(manifest['output'])
bpy.ops.wm.open_mainfile(filepath=str(ORIGINAL),load_ui=False)
before=snapshot()
old_faces={o.name:face_materials(o) for o in bpy.data.objects if o.type=='MESH'}
old_slots={o.name:material_assignment(o)['slots'] for o in bpy.data.objects if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=str(OUTPUT),load_ui=False)
after=snapshot()
checks={'objects_identical':before['objects']==after['objects'],
        'meshes_uv_custom_normals_identical':before['meshes']==after['meshes'],
        'all_101_chair_parts_and_material_assignments_identical':before['chair_assignments']==after['chair_assignments'],
        'all_original_material_graphs_identical':all(after['materials'].get(n)==h for n,h in before['materials'].items()),
        'all_original_images_identical':all(after['images'].get(n)==v for n,v in before['images'].items()),
        'source_and_original_files_unchanged':all(file_sha(p)==h for p,h in manifest['original_sha256'].items()),
        'output_sha256_matches_saved':file_sha(OUTPUT)==manifest['output_sha256'],
        'recovered_graphs_complete':all(after['materials'][manifest['material_datablocks'][n]]==h for n,h in manifest['source_graphs'].items()),
        'gray_variant_absent':'PBR_Paneles_Prueba_Gris' not in after['materials'],
        'baseline_reproducible':all(digest(before[k])==h for k,h in manifest['baseline_digests'].items())}
expected={n:list(mats) for n,mats in old_faces.items()}
for p in manifest['plans']:
    for a in expand_assignments(p): expected[p['object']][a['face']]=manifest['material_datablocks'][a['to']]
actual={o.name:face_materials(o) for o in bpy.data.objects if o.type=='MESH'}
checks['only_manifest_faces_reassigned']=expected==actual
checks['original_slots_preserved']=all(material_assignment(bpy.data.objects[n])['slots'][:len(slots)]==slots for n,slots in old_slots.items())
lcars={'turbolcar','lcardtype','lcarkey','lcarsdisplay','lcarsdisplay.001'}
lcars_faces=sum(m in lcars for mats in old_faces.values() for m in mats)
checks['all_lcars_faces_unchanged']=all(actual[n][i]==m for n,mats in old_faces.items() for i,m in enumerate(mats) if m in lcars)
blue_counts={}
for sign,label in [(-1,'left'),(1,'right')]:
    o=bpy.data.objects['Editable Mesh_Mat.004_0'];counts=collections.Counter()
    for p,m in zip(o.data.polygons,actual[o.name]):
        if all((o.matrix_world@o.data.vertices[v].co).x*sign>0 for v in p.vertices):counts[m]+=1
    blue_counts[label]=dict(counts)
checks['both_blue_strips_original_emission']=all(c.get('Luz_Azul_Suave_Consola',0)>0 and sum(c.values())==18 for c in blue_counts.values()) and checks['only_manifest_faces_reassigned']
used_materials={s.material for o in bpy.data.objects if o.type=='MESH' for s in o.material_slots if s.material}
used_images=set()
def images(tree):
    for n in tree.nodes:
        if n.type=='TEX_IMAGE' and n.image:used_images.add(n.image)
        if n.type=='GROUP' and n.node_tree:images(n.node_tree)
for m in used_materials:
    if m.node_tree:images(m.node_tree)
dependencies=[]
for im in sorted(used_images,key=lambda x:x.name):
    packed=bool(im.packed_file or len(im.packed_files));path=Path(bpy.path.abspath(im.filepath)) if im.filepath else None
    dependencies.append({'image':im.name,'packed':packed,'size':list(im.size),'available':packed or bool(path and path.is_file()),'source':im.source,'colorspace':im.colorspace_settings.name})
checks['all_used_images_available']=all(d['available'] and min(d['size'])>0 for d in dependencies)
checks['all_used_images_packed']=all(d['packed'] for d in dependencies)
checks['no_linked_blend_dependencies']=len(bpy.data.libraries)==0
doors={}
for n in ['Plane.001_0','Plane.017_0','Plane.018_0','Plane.019_0']:
    o=bpy.data.objects[n];a=np.array([list(o.matrix_world@v.co) for v in o.data.vertices])*100
    doors[n]={'dimensions_cm':np.ptp(a,axis=0).tolist(),'materials':dict(collections.Counter(actual[n]))}
result={'ok':all(checks.values()),'checks':checks,'counts':manifest['counts'],
        'objects_after':len(after['objects']),'protected_lcars_faces':lcars_faces,'blue_strips':blue_counts,
        'doors':doors,'dependencies':dependencies,'packed_used_images':sum(d['packed'] for d in dependencies),
        'geometry_object_hashes':{k:digest(after[k]) for k in ['objects','meshes','chair_assignments']},
        'per_mesh_geometry_sha256':{n:digest(v) for n,v in after['meshes'].items()},
        'visual_check':manifest.get('visual_check','pending light Blender UI check; no aesthetic approval claimed')}
(R/'datos/pbr01_verificacion.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in {'dependencies','per_mesh_geometry_sha256'}},ensure_ascii=False),flush=True)
assert result['ok'], 'Reopening integrity check failed; see JSON'
