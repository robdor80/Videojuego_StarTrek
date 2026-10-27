import bpy, json, hashlib, csv
from pathlib import Path
from mathutils import Vector
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'blender' / 'Miranda_Puente_Sutherland_Base.blend'
REPO = ROOT.parents[3]
GLB = REPO / 'assets/puentes/starfleet/USS Sutherland/star_trek_sutherland_bridge.glb'
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''): h.update(b)
    return h.hexdigest()
def bounds(o):
    if o.type != 'MESH': return None
    a = np.array([list(o.matrix_world @ v.co) for v in o.data.vertices])
    return {'min':a.min(0).tolist(), 'max':a.max(0).tolist(), 'dimensions':np.ptp(a,axis=0).tolist()}
objects=[]
arrays={}
for i,o in enumerate(bpy.data.objects):
    row={'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,
         'collections':[c.name for c in o.users_collection], 'location':list(o.location),
         'rotation_euler':list(o.rotation_euler),'scale':list(o.scale),
         'matrix_world':[list(r) for r in o.matrix_world], 'bounds_world_bu':bounds(o),
         'hide_viewport':o.hide_viewport,'hide_render':o.hide_render,'hide_get':o.hide_get(),
         'modifiers':[{'name':m.name,'type':m.type} for m in o.modifiers],
         'constraints':[{'name':c.name,'type':c.type} for c in o.constraints],
         'instances':o.instance_type,
         'materials':[s.material.name if s.material else None for s in o.material_slots]}
    if o.type=='MESH':
        row.update(vertices=len(o.data.vertices),polygons=len(o.data.polygons),mesh=o.data.name)
        o.data.calc_loop_triangles()
        arrays[f'v{i}']=np.array([list(o.matrix_world @ v.co) for v in o.data.vertices],dtype=np.float64)
        arrays[f't{i}']=np.array([list(t.vertices) for t in o.data.loop_triangles],dtype=np.int32)
        row['array_index']=i
    objects.append(row)
units=bpy.context.scene.unit_settings
info={'blender':bpy.app.version_string,'source':str(BASE),'glb':str(GLB),
      'source_sha256':sha(BASE),'glb_sha256':sha(GLB),
      'units':{'system':units.system,'scale_length':units.scale_length,'length_unit':units.length_unit},
      'collections':[{'name':c.name,'objects':len(c.objects),'hide_viewport':c.hide_viewport,'hide_render':c.hide_render} for c in bpy.data.collections],
      'objects':objects}
(ROOT/'datos/inventario.json').write_text(json.dumps(info,indent=2,ensure_ascii=False),encoding='utf-8')
np.savez_compressed(ROOT/'datos/geometria_mundial.npz',**arrays)
with (ROOT/'datos/inventario.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['objeto','tipo','padre','vertices','min_X_BU','min_Y_BU','min_Z_BU','max_X_BU','max_Y_BU','max_Z_BU','oculto_view','oculto_render'])
    for o in objects:
        b=o['bounds_world_bu']; w.writerow([o['name'],o['type'],o['parent'],o.get('vertices','')]+(b['min']+b['max'] if b else ['']*6)+[o['hide_get'],o['hide_render']])
print('UNITS',info['units'])
for o in objects:
    print(o['name'],o['type'],'parent=',o['parent'],'bounds=',o['bounds_world_bu'],'hidden=',o['hide_get'],o['hide_render'])
