"""Read source without saving; inventory evaluated geometry and material graphs."""
import bpy,sys,json,hashlib
from pathlib import Path
R=Path(__file__).parent
sys.path.insert(0,str(R.parents[2]/'analisis_dimensional/scripts'))
import pbr01_integrity as I
def val(v):
    try:return list(v)
    except TypeError:return v
out={'source':bpy.data.filepath,'sha256':I.file_sha(bpy.data.filepath),'objects':[], 'materials':{},'lights':[]}
for o in bpy.context.scene.objects:
    if o.type=='LIGHT':out['lights'].append(o.name)
    if o.type!='MESH':continue
    out['objects'].append({'name':o.name,'visible':o.visible_get(),'render':not o.hide_render,'collections':[c.name for c in o.users_collection],'matrix':[list(v) for v in o.matrix_world], 'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'materials':[s.material.name if s.material else None for s in o.material_slots]})
for m in bpy.data.materials:
    out['materials'][m.name]={'hash':I.graph_hash(m),'nodes':[],'links':[]}
    if not m.node_tree:continue
    for n in m.node_tree.nodes:
        out['materials'][m.name]['nodes'].append({'name':n.name,'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None,'image_path':bpy.path.abspath(n.image.filepath) if n.type=='TEX_IMAGE' and n.image else None,'inputs':{s.name:val(s.default_value) for s in n.inputs if hasattr(s,'default_value')}})
    out['materials'][m.name]['links']=[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]
out['snapshot']=I.snapshot()
(R/'blender_audit.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('AUDIT',len(out['objects']),sum(o['visible'] for o in out['objects']),len(out['materials']),out['lights'])
