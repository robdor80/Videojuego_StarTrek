import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def object_state(o):
    s={'type':o.type,'parent':o.parent.name if o.parent else None,'matrix_world':[list(r) for r in o.matrix_world],
       'matrix_basis':[list(r) for r in o.matrix_basis],'matrix_parent_inverse':[list(r) for r in o.matrix_parent_inverse],
       'materials':[slot.material.name if slot.material else None for slot in o.material_slots],
       'data':o.data.name if o.data else None,'modifiers':[(m.name,m.type) for m in o.modifiers],
       'constraints':[(c.name,c.type) for c in o.constraints]}
    if o.type=='MESH':
        me=o.data
        s.update(vertices=[list(v.co) for v in me.vertices],edges=[list(e.vertices) for e in me.edges],
                 polygons=[{'v':list(p.vertices),'mat':p.material_index,'smooth':p.use_smooth} for p in me.polygons],
                 uv={uv.name:[list(x.uv) for x in uv.data] for uv in me.uv_layers},
                 attributes=[(a.name,a.domain,a.data_type) for a in me.attributes])
    return s
def material_state(m):
    return {'name':m.name,'diffuse':list(m.diffuse_color),'nodes':[
        {'name':n.name,'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None,
         'inputs':[(i.name,list(i.default_value) if hasattr(i.default_value,'__iter__') else str(i.default_value)) for i in n.inputs if hasattr(i,'default_value')]}
        for n in m.node_tree.nodes] if m.node_tree else [],
        'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links] if m.node_tree else []}
def inspect():
    states={o.name:object_state(o) for o in bpy.data.objects}
    out={'source':bpy.data.filepath,'version':bpy.app.version_string,
         'units':{'system':bpy.context.scene.unit_settings.system,'scale_length':bpy.context.scene.unit_settings.scale_length},
         'protected_sha256':{str(p):sha(p) for p in (ROOT.parent/'blender').glob('*.blend')},
         'objects':{},'states':states,
         'material_hashes':{m.name:digest(material_state(m)) for m in bpy.data.materials},
         'images':{i.name:{'path':i.filepath,'size':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images}}
    for o in bpy.data.objects:
        if o.type!='MESH':continue
        vs=[list(o.matrix_world@v.co) for v in o.data.vertices]
        row={'world_vertices':vs,'polygons':states[o.name]['polygons'],'uv':states[o.name]['uv'],
             'bounds':[list(map(min,zip(*vs))),list(map(max,zip(*vs)))],
             'materials':states[o.name]['materials'],'users':o.data.users}
        out['objects'][o.name]=row
        if o.name.startswith('Plane.') or o.name.startswith('Circle'):
            sides=[]
            for sign in [-1,1]:
                v=[v for v in vs if v[0]*sign>0]
                if v:sides.append((sign,[round(min(a[i] for a in v),4) for i in range(3)],[round(max(a[i] for a in v),4) for i in range(3)]))
            print(o.name,row['materials'],len(vs),sides)
    (ROOT/'datos/ergonomia02_inspeccion.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print('INSPECCION_OK',len(states),out['units'])
if __name__=='__main__':inspect()
