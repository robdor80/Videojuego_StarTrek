import bpy,bmesh,json,sys,math,hashlib,collections
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
args=sys.argv[sys.argv.index('--')+1:];label=args[0];source=Path(args[1])
if source.suffix.lower()=='.blend':bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
elif source.suffix.lower()=='.obj':
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=str(source),use_split_objects=True,use_split_groups=True,validate_meshes=True,forward_axis='NEGATIVE_Z',up_axis='Y')
else:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(source))
def vec(v):return [float(x) for x in v]
def bounds(ob):
    pts=[ob.matrix_world@Vector(c) for c in ob.bound_box]
    lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
    return {'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]}
objects=[];meshes=[];materials=[];images=[]
for me in bpy.data.meshes:
    me.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(me)
    bnd=sum(e.is_boundary for e in bm.edges);non=sum(not e.is_manifold for e in bm.edges)
    loose=sum(e.is_wire for e in bm.edges);badwind=sum(e.is_manifold and not e.is_contiguous for e in bm.edges)
    parent=list(range(len(me.vertices)))
    def find(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    for e in me.edges:
        a,b=map(find,e.vertices);parent[b]=a
    comps=collections.Counter(find(v.index) for v in me.vertices)
    uv=[]
    for layer in me.uv_layers:
        coords=[x.uv[:] for x in layer.data];d=0;uvtri=[]
        for t in me.loop_triangles:
            a,b,c=[Vector(coords[i]) for i in t.loops]
            if abs((b-a).cross(c-a))<1e-12:d+=1
            uvtri.append(tuple(sorted(tuple(round(v,6) for v in coords[i]) for i in t.loops)))
        uv.append({'name':layer.name,'min':[min((c[i] for c in coords),default=0) for i in range(2)],'max':[max((c[i] for c in coords),default=0) for i in range(2)],'degenerate_uv_triangles':d,'exact_repeated_uv_triangles':sum(n-1 for n in collections.Counter(uvtri).values() if n>1)})
    # Seam-welded diagnostic in memory only, no write back.
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
    welded={'vertices':len(bm.verts),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'inconsistent_winding_edges':sum(e.is_manifold and not e.is_contiguous for e in bm.edges)}
    bm.free()
    geometry_hash=hashlib.sha256(repr(([(round(v.co.x,6),round(v.co.y,6),round(v.co.z,6)) for v in me.vertices],[tuple(p.vertices) for p in me.polygons])).encode()).hexdigest()
    meshes.append({'name':me.name,'users':me.users,'vertices':len(me.vertices),'edges':len(me.edges),'faces':len(me.polygons),'triangles':len(me.loop_triangles),'zero_area_triangles':sum(t.area<1e-10 for t in me.loop_triangles),'nonfinite_vertices':sum(not all(math.isfinite(x) for x in v.co) for v in me.vertices),'boundary_edges':bnd,'nonmanifold_edges':non,'wire_edges':loose,'inconsistent_winding_edges':badwind,'connected_components':len(comps),'largest_components':comps.most_common(10),'uv':uv,'color_attributes':[a.name for a in me.color_attributes],'welded_diagnostic':welded,'geometry_hash':geometry_hash})
for ob in bpy.data.objects:
    row={'name':ob.name,'type':ob.type,'parent':ob.parent.name if ob.parent else None,'data':ob.data.name if ob.data else None,'collections':[c.name for c in ob.users_collection],'location':vec(ob.location),'rotation_euler':vec(ob.rotation_euler),'scale':vec(ob.scale),'world_matrix':[vec(row) for row in ob.matrix_world],'world_origin':vec(ob.matrix_world.translation),'hide_render':ob.hide_render,'hide_viewport':ob.hide_viewport,'visible_get':ob.visible_get(),'modifiers':[{'name':m.name,'type':m.type} for m in ob.modifiers],'materials':[m.name if m else None for m in ob.data.materials] if ob.type=='MESH' else []}
    if ob.type=='MESH':row['bounds']=bounds(ob)
    objects.append(row)
for mat in bpy.data.materials:
    row={'name':mat.name,'users':mat.users,'diffuse_color':vec(mat.diffuse_color),'use_nodes':mat.use_nodes,'nodes':[],'links':[]}
    if mat.node_tree:
        for n in mat.node_tree.nodes:
            inputs={}
            for s in n.inputs:
                if hasattr(s,'default_value'):
                    val=s.default_value
                    try:val=list(val)
                    except TypeError:pass
                    if isinstance(val,(str,int,float,list,bool)):inputs[s.name]={'value':val,'linked':s.is_linked}
            row['nodes'].append({'name':n.name,'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None,'inputs':inputs})
        row['links']=[{'from':l.from_node.name,'out':l.from_socket.name,'to':l.to_node.name,'in':l.to_socket.name} for l in mat.node_tree.links]
    materials.append(row)
for im in bpy.data.images:
    p=bpy.path.abspath(im.filepath)
    images.append({'name':im.name,'source':im.source,'filepath':im.filepath,'absolute_path':p,'external_exists':Path(p).exists() if p else False,'size':list(im.size),'packed':bool(im.packed_file),'has_data':im.has_data})
active=[o for o in objects if o['type']=='MESH' and o['visible_get']]
lo=[min((o['bounds']['min'][i] for o in active),default=0) for i in range(3)];hi=[max((o['bounds']['max'][i] for o in active),default=0) for i in range(3)]
out={'label':label,'source_copy':str(source),'blender_version':bpy.app.version_string,'scenes':[{'name':s.name,'objects':len(s.objects),'units':{'system':s.unit_settings.system,'scale_length':s.unit_settings.scale_length,'length_unit':s.unit_settings.length_unit}} for s in bpy.data.scenes],'collections':[{'name':c.name,'objects':len(c.objects),'hide_render':c.hide_render,'hide_viewport':c.hide_viewport} for c in bpy.data.collections],'world_bounds_visible':{'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]},'objects':objects,'meshes':meshes,'materials':materials,'images':images,'libraries':[l.filepath for l in bpy.data.libraries],'actions':[a.name for a in bpy.data.actions]}
(R/'DATOS'/f'blender_{label}.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print('AUDIT_COMPLETE',label,len(objects),len(meshes),sum(m['triangles'] for m in meshes),out['world_bounds_visible'],flush=True)
