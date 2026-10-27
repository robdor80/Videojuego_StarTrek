import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'datos/inventario.json').read_text(encoding='utf-8'))
expected=json.loads((ROOT/'datos/verificacion_en_memoria.json').read_text(encoding='utf-8'))['fingerprints']
def fingerprint(o):
    q={'type':o.type,'parent':o.parent.name if o.parent else None,'matrix':[list(r) for r in o.matrix_world],
       'materials':[s.material.name if s.material else None for s in o.material_slots]}
    if o.type=='MESH':q.update(vertices=[list(v.co) for v in o.data.vertices],polygons=[list(p.vertices) for p in o.data.polygons])
    return hashlib.sha256(json.dumps(q,sort_keys=True).encode()).hexdigest()
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
diff=[n for n,fp in expected.items() if n not in bpy.data.objects or fingerprint(bpy.data.objects[n])!=fp]
refs=json.loads((ROOT/'datos/referencias.json').read_text(encoding='utf-8'))
head_checks=[]
for ref in refs:
    head=bpy.data.objects['REF_'+ref['id']+'_cabeza']
    top=max((head.matrix_world@Vector(c)).z for c in head.bound_box)*100
    head_checks.append({'id':ref['id'],'height_cm':top-ref['feet_world_cm'][2],'error_cm':top-ref['head_top_world_cm']})
check={'analysis_file':bpy.data.filepath,'base_sha256':sha(d['source']),'glb_sha256':sha(d['glb']),
       'base_unchanged':sha(d['source'])==d['source_sha256'],'glb_unchanged':sha(d['glb'])==d['glb_sha256'],
       'original_objects_checked':len(expected),'original_objects_changed':diff,'references_checked':head_checks,
       'units':{'system':bpy.context.scene.unit_settings.system,'scale_length':bpy.context.scene.unit_settings.scale_length},
       'passed':not diff and sha(d['source'])==d['source_sha256'] and sha(d['glb'])==d['glb_sha256'] and all(abs(c['error_cm'])<.001 for c in head_checks)}
(ROOT/'datos/verificacion_final.json').write_text(json.dumps(check,indent=2),encoding='utf-8')
print(json.dumps(check,indent=2))
assert check['passed']
