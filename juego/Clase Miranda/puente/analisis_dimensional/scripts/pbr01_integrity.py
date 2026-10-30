"""Read-only signatures shared by the bounded PBR transfer and reopening check."""
import bpy, hashlib, json, re, collections
import numpy as np

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def file_sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''): h.update(block)
    return h.hexdigest()

def value(x):
    if isinstance(x,(str,int,float,bool)) or x is None: return x
    if isinstance(x,bpy.types.ID): return {'id':x.name,'type':x.bl_rna.identifier}
    try: return [value(v) for v in x]
    except TypeError: return str(x)

def settings(x,depth=0):
    result={}
    for p in x.bl_rna.properties:
        k=p.identifier
        if k in {'rna_type','id_data','name','type'}: continue
        try:
            v=getattr(x,k)
            if p.type in {'BOOLEAN','INT','FLOAT','STRING','ENUM'}: result[k]=value(v)
            elif p.type=='POINTER' and isinstance(v,bpy.types.ID): result[k]=value(v)
            elif p.type=='POINTER' and v is not None and depth<2: result[k]=settings(v,depth+1)
        except (AttributeError,TypeError,ValueError): pass
    return result

def image_record(im):
    packed=list(im.packed_files)
    hashes=[hashlib.sha256(bytes(p.packed_file.data)).hexdigest() for p in packed]
    if not hashes and im.packed_file: hashes=[hashlib.sha256(bytes(im.packed_file.data)).hexdigest()]
    return {'source':im.source,'size':list(im.size),'colorspace':im.colorspace_settings.name,
            'alpha_mode':im.alpha_mode,'packed_sha256':hashes}

def graph_record(mat):
    def tree_record(tree):
        nodes=[]
        for n in sorted(tree.nodes,key=lambda x:x.name):
            row={'name':n.name,'type':n.bl_idname,'settings':settings(n),
                 'inputs':[(s.identifier,value(s.default_value)) for s in n.inputs if hasattr(s,'default_value')],
                 'outputs':[(s.identifier,value(s.default_value)) for s in n.outputs if hasattr(s,'default_value')]}
            # ID names may gain suffixes during append. Compare the actual embedded images instead.
            row['settings'].pop('image',None); row['settings'].pop('node_tree',None)
            if n.type=='TEX_IMAGE' and n.image: row['image']=image_record(n.image)
            if n.type=='GROUP' and n.node_tree: row['group']=tree_record(n.node_tree)
            if hasattr(n,'color_ramp'):
                row['ramp']={'interpolation':n.color_ramp.interpolation,'color_mode':n.color_ramp.color_mode,
                             'elements':[(e.position,list(e.color)) for e in n.color_ramp.elements]}
            if hasattr(n,'mapping'):
                row['curves']=[[(list(p.location),p.handle_type) for p in c.points] for c in n.mapping.curves]
            nodes.append(row)
        return {'nodes':nodes,'links':sorted((l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in tree.links)}
    return {'surface_render_method':mat.surface_render_method,'diffuse_color':list(mat.diffuse_color),
            'metallic':mat.metallic,'roughness':mat.roughness,'use_nodes':mat.use_nodes,
            'tree':tree_record(mat.node_tree) if mat.node_tree else None}

def graph_hash(mat): return digest(graph_record(mat))

def array_hash(seq,prop,width,dtype):
    a=np.empty(len(seq)*width,dtype=dtype)
    seq.foreach_get(prop,a)
    return hashlib.sha256(a.tobytes()).hexdigest()

def mesh_geometry(m):
    attrs=[]
    for a in m.attributes:
        if a.name=='material_index': continue
        if not len(a.data): attrs.append((a.name,a.domain,a.data_type,0)); continue
        p=next((k for k in ['vector','color','value'] if hasattr(a.data[0],k)),None)
        assert p is not None, (m.name,a.name,a.data_type)
        v=getattr(a.data[0],p); width=len(v) if hasattr(v,'__len__') else 1
        dtype=np.float32 if a.data_type in {'FLOAT','FLOAT2','FLOAT_VECTOR','FLOAT_COLOR','BYTE_COLOR','QUATERNION','FLOAT4X4'} else np.int32
        attrs.append((a.name,a.domain,a.data_type,array_hash(a.data,p,width,dtype)))
    return {'vertices':len(m.vertices),'edges':len(m.edges),'faces':len(m.polygons),'loops':len(m.loops),
            'co':array_hash(m.vertices,'co',3,np.float32),'edge_vertices':array_hash(m.edges,'vertices',2,np.int32),
            'loop_vertices':array_hash(m.loops,'vertex_index',1,np.int32),
            'loop_edges':array_hash(m.loops,'edge_index',1,np.int32),
            'polygon_ranges':[(p.loop_start,p.loop_total,p.use_smooth) for p in m.polygons],
            'attributes':sorted(attrs),
            'uv':[(l.name,l.active_render,l.active_clone,array_hash(l.data,'uv',2,np.float32)) for l in m.uv_layers],
            'uv_active':m.uv_layers.active_index,'custom_normals':m.has_custom_normals,
            'shape_keys':None if not m.shape_keys else digest([(k.name,[list(p.co) for p in k.data]) for k in m.shape_keys.key_blocks])}

def material_assignment(o):
    return {'slots':[(s.link,s.material.name if s.material else None) for s in o.material_slots],
            'faces':[p.material_index for p in o.data.polygons]}

def protected_chair(name):
    return bool(re.fullmatch(r'Mesh\.(58[7-9]|59\d|60[0-2])_0(?:\.\d+)?',name)) or name in {'Sphere.001_0','Cube.002_0','Cylinder_0','Cube_0','Mesh.453_0'}

def snapshot():
    result={'objects':{},'meshes':{},'chair_assignments':{},'materials':{},'images':{}}
    for o in bpy.data.objects:
        result['objects'][o.name]={'type':o.type,'data':o.data.name if o.data else None,
          'parent':o.parent.name if o.parent else None,'parent_type':o.parent_type,'parent_bone':o.parent_bone,
          'world':value(o.matrix_world),'local':value(o.matrix_local),'basis':value(o.matrix_basis),
          'parent_inverse':value(o.matrix_parent_inverse),'location':value(o.location),'rotation_mode':o.rotation_mode,
          'rotation_euler':value(o.rotation_euler),'rotation_quaternion':value(o.rotation_quaternion),
          'scale':value(o.scale),'delta_location':value(o.delta_location),'delta_rotation_euler':value(o.delta_rotation_euler),
          'delta_rotation_quaternion':value(o.delta_rotation_quaternion),'delta_scale':value(o.delta_scale),'dimensions':value(o.dimensions),
          'collections':sorted(c.name for c in o.users_collection),'hidden':(o.hide_viewport,o.hide_render,o.hide_get()),
          'modifiers':[(m.name,m.type,settings(m)) for m in o.modifiers],
          'constraints':[(c.name,c.type,settings(c)) for c in o.constraints]}
        if o.type=='MESH':
            if o.data.name not in result['meshes']: result['meshes'][o.data.name]=mesh_geometry(o.data)
            if protected_chair(o.name): result['chair_assignments'][o.name]=material_assignment(o)
    for m in bpy.data.materials: result['materials'][m.name]=graph_hash(m)
    for im in bpy.data.images: result['images'][im.name]=image_record(im)
    return result

def face_materials(o):
    return [o.material_slots[p.material_index].material.name if p.material_index<len(o.material_slots) and o.material_slots[p.material_index].material else None for p in o.data.polygons]

def mapping_record(o):
    return {'vertices':len(o.data.vertices),'polys':[list(p.vertices) for p in o.data.polygons],
            'uv':[[list(l.data[i].uv) for i in range(len(l.data))] for l in o.data.uv_layers],
            'uv_names':[l.name for l in o.data.uv_layers],
            'loop_ranges':[(p.loop_start,p.loop_total) for p in o.data.polygons],
            'materials':face_materials(o),
            'world_x':[float((o.matrix_world@v.co).x) for v in o.data.vertices]}

def compact_plans(plans):
    result=[]
    for plan in plans:
        grouped=collections.defaultdict(list)
        for a in plan['assignments']:
            grouped[(a['source_object'],a['from'],a['to'])].append((a['face'],a['source_face']))
        groups=[]
        for (source,old,new),pairs in grouped.items():
            ranges=[]
            for i,j in sorted(pairs):
                if ranges and i==ranges[-1][0]+ranges[-1][2] and j==ranges[-1][1]+ranges[-1][2]: ranges[-1][2]+=1
                else:ranges.append([i,j,1])
            groups.append({'source_object':source,'from':old,'to':new,'ranges':ranges})
        result.append({'object':plan['object'],'method':plan['method'],'groups':groups})
    return result

def expand_assignments(plan):
    if 'assignments' in plan:return plan['assignments']
    return [{'face':i+k,'source_object':g['source_object'],'source_face':j+k,'from':g['from'],'to':g['to']}
            for g in plan['groups'] for i,j,count in g['ranges'] for k in range(count)]
