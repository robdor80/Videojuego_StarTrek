"""Auditoría de solo lectura. Blender 5.2.2; no guarda ni exporta la escena.

Ejecutar: blender.exe --background --factory-startup --disable-autoexec
  --python-exit-code 1 --python scripts/auditoria_voyager.py -- --root DIRECTORIO
Los nombres originales se conservan en JSON; normalized_name sólo facilita búsquedas.
"""
import argparse
import collections
import datetime
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import struct
import sys
import unicodedata

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def serial(v):
    if isinstance(v, (str, int, bool)) or v is None:
        return v
    if isinstance(v, float):
        return v if math.isfinite(v) else str(v)
    try:
        return [serial(x) for x in v]
    except TypeError:
        return str(v)


def norm(name):
    return re.sub(r"\s+", " ", "".join(c for c in name if not unicodedata.category(c).startswith('C'))).strip().casefold()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def bounds(coords):
    coords = list(coords)
    if not coords:
        return None
    lo = [min(v[i] for v in coords) for i in range(3)]
    hi = [max(v[i] for v in coords) for i in range(3)]
    return dict(min=lo, max=hi, dimensions=[hi[i]-lo[i] for i in range(3)], center=[(hi[i]+lo[i])/2 for i in range(3)])


def props(data):
    return {k: serial(data[k]) for k in data.keys()}


def object_info(o):
    result = dict(name=o.name, type=o.type, data=o.data.name if o.data else None,
        collections=[c.name for c in o.users_collection], parent=o.parent.name if o.parent else None,
        hide_viewport=o.hide_viewport, hide_render=o.hide_render, hide_get=o.hide_get(),
        visible_get=o.visible_get(), location=serial(o.location), rotation_euler=serial(o.rotation_euler),
        scale=serial(o.scale), matrix_world=serial(o.matrix_world), determinant=o.matrix_world.determinant(),
        properties=props(o), library=o.library.filepath if o.library else None,
        modifiers=[dict(name=m.name,type=m.type,show_viewport=m.show_viewport,show_render=m.show_render) for m in o.modifiers],
        constraints=[dict(name=c.name,type=c.type) for c in o.constraints],
        animation=bool(o.animation_data), material_slots=[s.material.name if s.material else None for s in o.material_slots])
    if o.type != 'MESH':
        return result
    m = o.data
    m.calc_loop_triangles()
    world = [o.matrix_world @ v.co for v in m.vertices]
    root = list(range(len(m.vertices)))
    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x
    edge_use = collections.Counter()
    degenerate = 0
    face_vertices=set()
    for e in m.edges:
        a,b = map(find, e.vertices)
        root[b] = a
    groups = collections.defaultdict(list)
    for i in range(len(world)):
        groups[find(i)].append(i)
    per_slot = {}
    island_faces = collections.Counter()
    for p in m.polygons:
        s = per_slot.setdefault(p.material_index, dict(faces=0,triangles=0,area_local=0.0,area_world=0.0,vertices=set(),normal_axes=collections.Counter()))
        s['faces'] += 1
        s['triangles'] += max(0,len(p.vertices)-2)
        s['area_local'] += p.area
        s['vertices'].update(p.vertices)
        face_vertices.update(p.vertices)
        n = o.matrix_world.to_3x3().inverted_safe().transposed() @ p.normal
        if n.length: n.normalize()
        axis = max(range(3),key=lambda i:abs(n[i]))
        s['normal_axes']['XYZ'[axis]+('+' if n[axis]>=0 else '-')] += 1
        if p.area < 1e-12: degenerate += 1
        for e in p.edge_keys: edge_use[tuple(sorted(e))] += 1
        if p.vertices: island_faces[find(p.vertices[0])] += 1
    for tri in m.loop_triangles:
        a,b,c = (world[i] for i in tri.vertices)
        per_slot[tri.material_index]['area_world'] += (b-a).cross(c-a).length/2
    slots = []
    for idx,s in sorted(per_slot.items()):
        s['bounds_world'] = bounds(world[i] for i in s.pop('vertices'))
        s['material_index'] = idx
        s['material'] = o.material_slots[idx].material.name if idx<len(o.material_slots) and o.material_slots[idx].material else None
        s['normal_axes'] = dict(s['normal_axes'])
        slots.append(s)
    islands = [dict(vertices=len(ids),faces=island_faces[r],bounds_world=bounds(world[i] for i in ids)) for r,ids in groups.items()]
    islands.sort(key=lambda x:x['faces'],reverse=True)
    uv=[]
    for layer in m.uv_layers:
        vals = [tuple(x.uv) for x in layer.data]
        uv.append(dict(name=layer.name,active_render=layer.active_render,loops=len(vals),
            bounds=[min(v[0] for v in vals),min(v[1] for v in vals),max(v[0] for v in vals),max(v[1] for v in vals)] if vals else None,
            nonfinite=sum(not all(math.isfinite(x) for x in v) for v in vals)))
    result['mesh']=dict(vertices=len(m.vertices),edges=len(m.edges),polygons=len(m.polygons),triangles=len(m.loop_triangles),
        bounds_world=bounds(world),bounds_local=bounds(v.co for v in m.vertices),bounds_surface_world=bounds(world[i] for i in face_vertices),material_faces=slots,
        uv_layers=uv,attributes=[dict(name=a.name,domain=a.domain,type=a.data_type) for a in m.attributes],
        shape_keys=bool(m.shape_keys),users=m.users,properties=props(m),
        boundary_edges=sum(v==1 for v in edge_use.values()),nonmanifold_edges_gt2=sum(v>2 for v in edge_use.values()),
        loose_edges=sum(edge_use[tuple(sorted(e.vertices))]==0 for e in m.edges),
        loose_vertices=len(m.vertices)-len(face_vertices),
        degenerate_polygons=degenerate,smooth_polygons=sum(p.use_smooth for p in m.polygons),
        connected_components=len(islands),components=islands)
    return result


def material_info(m):
    r=dict(name=m.name,normalized_name=norm(m.name),control_characters=[dict(index=i,code=hex(ord(c))) for i,c in enumerate(m.name) if unicodedata.category(c).startswith('C')],
        users=m.users,use_nodes=m.use_nodes,diffuse_color=serial(m.diffuse_color),metallic=m.metallic,roughness=m.roughness,
        specular_intensity=m.specular_intensity,surface_render_method=getattr(m,'surface_render_method',None),
        use_backface_culling=m.use_backface_culling,properties=props(m),nodes=[],links=[])
    if m.node_tree:
        outputs=[n for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL' and n.is_active_output]
        reach=set()
        def visit(n):
            if n.name in reach:return
            reach.add(n.name)
            for s in n.inputs:
                for link in s.links:visit(link.from_node)
        for n in outputs:visit(n)
        for n in m.node_tree.nodes:
            node=dict(name=n.name,type=n.bl_idname,label=n.label,mute=n.mute,reaches_active_output=n.name in reach,
                inputs=[dict(name=s.name,identifier=s.identifier,linked=s.is_linked,value=serial(s.default_value) if hasattr(s,'default_value') else None) for s in n.inputs])
            if hasattr(n,'image'):node['image']=n.image.name if n.image else None
            for key in ('uv_map','blend_type','operation','interpolation','extension','projection'):
                if hasattr(n,key):node[key]=getattr(n,key)
            if n.type=='GROUP':node['group']=n.node_tree.name if n.node_tree else None
            r['nodes'].append(node)
        r['links']=[dict(from_node=l.from_node.name,from_socket=l.from_socket.name,to_node=l.to_node.name,to_socket=l.to_socket.name,valid=l.is_valid) for l in m.node_tree.links]
    return r


def image_info(im, texture_files):
    resolved=bpy.path.abspath(im.filepath,library=im.library)
    basename=Path(im.filepath.replace('\\','/')).name.casefold()
    packed=[dict(filepath=p.filepath,bytes=p.packed_file.size,sha256=hashlib.sha256(p.packed_file.data).hexdigest()) for p in im.packed_files]
    matches=[str(p) for p in texture_files if p.name.casefold()==basename or p.name.casefold()==im.name.casefold()]
    try:
        pixels=len(im.pixels)
        sample=serial(im.pixels[:4]) if pixels else []
        error=None
    except Exception as e:
        pixels=0;sample=[];error=str(e)
    rename=re.sub(r'(?<=\d)\.(?=\d)', '_', basename)
    renamed=[str(p) for p in texture_files if p.name.casefold()==rename and rename!=basename]
    return dict(name=im.name,filepath=im.filepath,filepath_raw=im.filepath_raw,resolved_path=resolved,
        source=im.source,type=im.type,users=im.users,size=serial(im.size),channels=im.channels,depth=im.depth,
        colorspace=im.colorspace_settings.name,alpha_mode=im.alpha_mode,is_float=im.is_float,
        packed_files=packed,external_exists=Path(resolved).is_file() if resolved else False,
        local_basename_candidates=matches,renamed_basename_candidates=renamed,has_data=im.has_data,pixel_values=pixels,sample_rgba=sample,decode_error=error,
        status='nonfile_buffer' if im.source not in {'FILE','TILED','SEQUENCE','MOVIE'} else 'packed_decodable' if packed and pixels else 'external_decodable' if Path(resolved).is_file() and pixels else 'local_candidate_not_linked' if matches else 'renamed_candidate_not_linked' if renamed else 'missing_or_nonfile')


def decode_texture_files(files):
    """Decodificar copias temporales de imágenes sin reenlazar las originales."""
    result=[]
    for p in files:
        if p.suffix.casefold() not in {'.png','.jpg','.jpeg','.tif','.tiff','.tga','.bmp'}:continue
        temporary=None
        try:
            temporary=bpy.data.images.load(str(p),check_existing=False)
            size=list(temporary.size);count=len(temporary.pixels)
            result.append(dict(path=str(p),name=p.name,sha256=sha(p),size=size,channels=temporary.channels,
                depth=temporary.depth,pixel_values=count,decodable=bool(count and all(size)),error=None))
        except Exception as e:
            result.append(dict(path=str(p),name=p.name,decodable=False,error=str(e)))
        finally:
            if temporary is not None:bpy.data.images.remove(temporary)
    return result


def importer_readonly(path, object_names):
    """Únicamente rutinas lectoras del importador instalado; no se llama load/read/make_scene."""
    importer=Path(os.environ.get('APPDATA',''))/'Blender Foundation/Blender/5.2/extensions/blender_org/io_scene_max/import_max.py'
    r=dict(path=str(importer),available=importer.is_file(),nodes=[],errors=[])
    if not importer.is_file():return r
    r['sha256']=sha(importer)
    r['manifest']=(importer.parent/'blender_manifest.toml').read_text(encoding='utf-8')
    try:
        spec=importlib.util.spec_from_file_location('auditoria_max_reader',importer)
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        with mod.ImportMaxFile(str(path)) as maxfile:
            mod.read_class_data(maxfile,str(path));mod.read_config(maxfile,str(path))
            mod.read_directory(maxfile,str(path));mod.read_class_directory(maxfile,str(path))
            mod.SCENE_LIST=mod.read_chunks(maxfile,'Scene',mod.SceneChunk)
            mod.META_DATA=mod.read_chunks(maxfile,'FileAssetMetaData2',superId=11)
            def raw_geometry(msh, depth=0):
                if not msh or depth>8:return None
                if mod.get_guid(msh) in {0x2032,0x2033}:
                    refs=mod.get_references(msh)
                    return raw_geometry(refs[-1],depth+1) if refs else None
                poly=msh.get_first(0x08FE)
                if not poly:return None
                verts=[];faces=[];points=None
                vc=poly.get_first(0x0914);fc=poly.get_first(0x0912)
                if vc and fc:
                    verts=mod.get_point_array(vc.data);faces,_=mod.get_mesh_polys(fc.data)
                else:
                    for ch in poly.children:
                        if ch.types==0x0100:verts=mod.calc_point(ch.data)
                        elif ch.types==0x0118:faces.append(mod.get_face_chunks(ch)[0])
                        elif ch.types==0x011A:points=mod.calc_point_3d(ch)
                    if points is not None:faces.extend(p.points for p in points)
                nv=len(verts)//3
                return dict(vertices=nv,faces=len(faces),corners=sum(len(f) for f in faces),
                    face_lengths=dict(collections.Counter(len(f) for f in faces)),
                    repeated_vertex_faces=sum(len(set(f))!=len(f) for f in faces),
                    duplicate_vertex_sets_faces=len(faces)-len({tuple(sorted(f)) for f in faces}),
                    invalid_index_faces=sum(any(i<0 or i>=nv for i in f) for f in faces),
                    chunk_types=[hex(ch.types) for ch in poly.children],
                    unused_vertices=nv-len({i for f in faces for i in f}),
                    limitation='Conteo previo a mesh.validate según lector instalado; no verificación completa del formato MAX.')
            for chunk in mod.SCENE_LIST[0].children:
                namechunk=chunk.get_first(0x0962)
                if not namechunk:continue
                try:
                    name=mod.get_node_name(chunk).rstrip('\x00')
                    prs,msh,mat,lyr=mod.get_matrix_mesh_material(chunk)
                    parent=mod.get_node_parent(chunk)
                    node_record=dict(name=name,parent=mod.get_node_name(parent).rstrip('\x00') if parent else None,
                        class_name=mod.get_cls_name(msh) if msh else None, guid=hex(mod.get_guid(msh)),
                        super_id=hex(mod.get_super_id(msh)),source_transform=serial(mod.create_matrix(prs)) if prs else None,
                        importer_skips=mod.SKIPPABLE.get(mod.get_guid(msh)),
                        material_class=mod.get_cls_name(mat) if mat else None,
                        material_guid=hex(mod.get_guid(mat)) if mat else None,
                        material_name_reader=mod.get_material_name(mat) if mat else None,
                        present_in_blend=name in object_names)
                    if mod.get_super_id(msh)==0x10 and mod.get_guid(msh)!=0x1020 or mod.get_guid(msh) in {0x2032,0x2033}:
                        try:node_record['raw_geometry']=raw_geometry(msh)
                        except Exception as e:node_record['raw_geometry_error']=str(e)
                    r['nodes'].append(node_record)
                except Exception as e:r['errors'].append(dict(name=str(namechunk.data),error=str(e)))
        r['unmatched_blend_objects']=sorted(set(object_names)-{n['name'] for n in r['nodes']})
    except Exception as e:r['errors'].append(dict(error=str(e)))
    r['limitation']='Lectura parcial con código del importador instalado; nombres y clases, sin conversión de escena ni equivalencia de geometría/shaders.'
    return r


def mesh468_occlusion():
    """Rayos geométricos hacia +Z desde los centroides, máximo 5 cm.
    Excluye OBJ y Mesh468; no evalúa transparencia ni culling del material.
    """
    coords=[];tris=[];owners=[]
    for o in bpy.context.scene.objects:
        if o.type!='MESH' or o.name in {'Voyager Bridge','Mesh468'}:continue
        base=len(coords);coords.extend(o.matrix_world@v.co for v in o.data.vertices)
        o.data.calc_loop_triangles()
        for t in o.data.loop_triangles:
            tris.append(tuple(base+i for i in t.vertices));owners.append(o.name)
    bvh=BVHTree.FromPolygons(coords,tris,all_triangles=True)
    mesh=bpy.data.objects['Mesh468'];hits=collections.defaultdict(lambda:dict(triangles=0,area_world=0.,distances=[]))
    tested=0;area_total=0.
    for t in mesh.data.loop_triangles:
        vs=[mesh.matrix_world@mesh.data.vertices[i].co for i in t.vertices]
        center=sum(vs,Vector())/3;area=(vs[1]-vs[0]).cross(vs[2]-vs[0]).length/2
        tested+=1;area_total+=area
        loc,n,idx,dist=bvh.ray_cast(center+Vector((0,0,0.00001)),Vector((0,0,1)),0.05)
        if idx is not None:
            h=hits[owners[idx]];h['triangles']+=1;h['area_world']+=area;h['distances'].append(dist+0.00001)
    for h in hits.values():
        distances=h.pop('distances');h['distance_min']=min(distances);h['distance_max']=max(distances)
        h['area_fraction']=h['area_world']/area_total if area_total else None
    return dict(tested_triangles=tested,total_area_world=area_total,hit_objects=dict(hits),
        limitation='Muestreo de centroides; posible cobertura geométrica desde arriba, sin transparencia ni materiales; no calcula áreas de intersección exactas.')


def block_tree(text):
    """Parser de llaves con respeto a comillas; conserva claves repetidas y líneas."""
    root=dict(header='ROOT',line=1,lines=[],children=[])
    stack=[root];pending=None
    for lineno,line in enumerate(text.splitlines(),1):
        stripped=line.strip()
        if stripped=='{':
            b=dict(header=pending[0] if pending else '',line=pending[1] if pending else lineno,lines=[],children=[])
            if pending and stack[-1]['lines'] and stack[-1]['lines'][-1]['line']==pending[1]:stack[-1]['lines'].pop()
            stack[-1]['children'].append(b);stack.append(b);pending=None
        elif stripped=='}':
            if len(stack)==1:raise ValueError('MC6: cierre inesperado')
            stack.pop();pending=None
        elif stripped:
            stack[-1]['lines'].append(dict(line=lineno,text=stripped));pending=(stripped,lineno)
    if len(stack)!=1:raise ValueError('MC6: llaves sin cerrar')
    return root


def walk(tree):
    for ch in tree['children']:
        yield ch
        yield from walk(ch)


def mc6_info(path,files):
    text=path.read_text(encoding='cp1252')
    tree=block_tree(text)
    mats=[]
    for b in walk(tree):
        if not b['header'].startswith('material '):continue
        name=b['header'][9:].strip('"')
        inputs=[];maps=[];nodes=[]
        for sub in walk(b):
            vals={x['text'].split(None,1)[0]:x['text'].split(None,1)[1] if len(x['text'].split(None,1))>1 else '' for x in sub['lines']}
            if sub['header'].startswith('nodeInput '):inputs.append(dict(header=sub['header'],line=sub['line'],values=vals))
            if sub['header'].startswith('node '):nodes.append(dict(header=sub['header'],line=sub['line'],values=vals))
        for x in [*b['lines'],*(line for sub in walk(b) for line in sub['lines'])]:
            if re.search(r'\.(?:png|jpg|jpeg|tga|tif|tiff|bmp)',x['text'],re.I):
                raw=x['text'].split(None,1)[1].strip('"') if len(x['text'].split(None,1))>1 else x['text']
                basename=re.split(r'[:\\/]',raw)[-1].casefold()
                maps.append(dict(line=x['line'],text=x['text'],basename=basename,local_candidates=[str(f) for f in files if f.name.casefold()==basename]))
        mats.append(dict(name=name,normalized_name=norm(name),line=b['line'],properties=b['lines'],nodes=nodes,inputs=inputs,texture_references=maps))
    return dict(encoding='cp1252',materials=mats,material_count=len(mats),lines=len(text.splitlines()))


def max_info(path):
    """Inspección CFB/OLE y cadenas; nunca interpreta una escena MAX completa."""
    data=path.read_bytes();r=dict(bytes=len(data),signature=data[:16].hex(),streams=[],strings=[])
    if data[:8]!=bytes.fromhex('d0cf11e0a1b11ae1'):
        r['error']='No es contenedor CFB/OLE reconocido';return r
    ss=1<<struct.unpack_from('<H',data,30)[0]
    def sector(i):
        start=(i+1)*ss
        if start>=len(data):raise ValueError('sector CFB fuera de rango')
        # MAX puede acabar con un sector parcial: rellenar para recorrer FAT,
        # recortar cada stream a su longitud declarada y registrar esta condición.
        return data[start:start+ss].ljust(ss,b'\x00')
    dif=list(struct.unpack_from('<109I',data,76));next_dif,n_dif=struct.unpack_from('<II',data,68)
    for _ in range(n_dif):
        vals=struct.unpack('<%dI'%(ss//4),sector(next_dif));dif.extend(vals[:-1]);next_dif=vals[-1]
    fat=[]
    for s in dif:
        if s<0xFFFFFFFA:fat.extend(struct.unpack('<%dI'%(ss//4),sector(s)))
    def chain(start,table=fat,reader=sector):
        out=[];seen=set()
        while start<0xFFFFFFFA:
            if start in seen or start>=len(table):raise ValueError('cadena CFB inválida')
            seen.add(start);out.append(reader(start));start=table[start]
        return b''.join(out)
    directory=chain(struct.unpack_from('<I',data,48)[0]);entries=[]
    for off in range(0,len(directory)-127,128):
        e=directory[off:off+128];ln=struct.unpack_from('<H',e,64)[0]
        if e[66] and 2<=ln<=64:
            entries.append(dict(name=e[:ln-2].decode('utf-16le',errors='replace'),type=e[66],start=struct.unpack_from('<I',e,116)[0],bytes=struct.unpack_from('<Q',e,120)[0]))
    root=next(e for e in entries if e['type']==5)
    mini=chain(root['start'])[:root['bytes']]
    minifat_bytes=chain(struct.unpack_from('<I',data,60)[0]);minifat=list(struct.unpack('<%dI'%(len(minifat_bytes)//4),minifat_bytes))
    for e in entries:
        if e['type']!=2:continue
        raw=chain(e['start'],minifat,lambda i:mini[i*64:i*64+64])[:e['bytes']] if e['bytes']<4096 else chain(e['start'])[:e['bytes']]
        r['streams'].append(dict(name=e['name'],bytes=e['bytes'],sha256=hashlib.sha256(raw).hexdigest(),head_hex=raw[:24].hex()))
        found=[]
        for enc,pattern in [('ascii',rb'[\x20-\x7e]{5,}'),('utf16le',rb'(?:[\x20-\x7e]\x00){5,}')]:
            for m in re.finditer(pattern,raw):
                s=m.group().decode('ascii' if enc=='ascii' else 'utf-16le')
                if re.search(r'light|camera|objects:|vertices:|faces:|shapes:|geometry:|units|floor|glow|railing|chair|ceiling|door|console|bridge|chainsaw|\.png|\.jpg|\.tga|\.tif|autodesk|3ds|max|mental|vray',s,re.I):
                    found.append(dict(offset=m.start(),encoding=enc,text=s[:1000]))
        r['strings'].append(dict(stream=e['name'],hits=found))
    r['sector_size']=ss;r['partial_final_sector_bytes']=len(data)%ss
    r['limitation']='Sólo estructura CFB y cadenas legibles; no prueba de geometría, shading, luces ni animación. Sector final parcial rellenado con ceros sólo en memoria.'
    return r


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    root=args.root.resolve();originals=root/'originales';out=root/'informes';out.mkdir(exist_ok=True)
    files=sorted(p for p in originals.rglob('*') if p.is_file())
    before={str(p.relative_to(root)):dict(bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns,sha256=sha(p)) for p in files}
    blend=originals/'Voyager_Bridge_MAX_Trabajo.blend'
    if bpy.app.autoexec_fail:raise RuntimeError('autoexec_fail: '+bpy.app.autoexec_fail_message)
    bpy.ops.wm.open_mainfile(filepath=str(blend),use_scripts=False,load_ui=False)
    bpy.context.view_layer.update()
    print('AUDIT: escena abierta con use_scripts=False',flush=True)
    objects=[]
    for i,o in enumerate(bpy.data.objects):
        objects.append(object_info(o))
        if i%100==0:print('AUDIT objetos',i,flush=True)
    materials=[material_info(m) for m in bpy.data.materials]
    images=[image_info(im,files) for im in bpy.data.images]
    texture_files=decode_texture_files(files)
    poser=mc6_info(originals/'Voyager Bridge.mc6',files)
    old=[o for o in objects if o['name']=='Voyager Bridge']
    if len(old)!=1 or old[0]['type']!='MESH':raise RuntimeError('No se ha aislado la malla OBJ declarada por el usuario')
    max_objs=[o for o in objects if o['name']!='Voyager Bridge']
    assignments=collections.defaultdict(list)
    for o in objects:
        for slot in o.get('mesh',{}).get('material_faces',[]):
            if slot['material']:assignments[slot['material']].append(dict(object=o['name'],subset='legacy_OBJ' if o['name']=='Voyager Bridge' else 'MAX_candidate',**slot))
    for m in materials:
        m['assignments']=assignments[m['name']]
        candidates=[p for p in poser['materials'] if p['normalized_name']==m['normalized_name']]
        m['poser_exact_normalized_candidates']=[p['name'] for p in candidates]
    partial_max=importer_readonly(originals/'Voyager Bridge Max2011.max',[o['name'] for o in max_objs])
    occlusion=mesh468_occlusion()
    after={str(p.relative_to(root)):dict(bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns,sha256=sha(p)) for p in files}
    result=dict(schema_version=1,generated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        blender=dict(version=bpy.app.version_string,build_hash=bpy.app.build_hash.decode(),background=bpy.app.background,
            autoexec_preference=bpy.context.preferences.filepaths.use_scripts_auto_execute,open_use_scripts=False),
        input_manifest=before,integrity=dict(unchanged=before==after,after_manifest=after),
        scope=dict(legacy_OBJ=old[0]['name'],provenance='OBJ identificado por nombre exacto y declaración del usuario; el resto es candidato MAX hasta cotejo de nombres binarios.',
            global_counts=dict(objects=len(objects),meshes=sum(o['type']=='MESH' for o in objects),materials=len(materials),images=len(images)),
            max_candidate_counts=dict(objects=len(max_objs),meshes=sum(o['type']=='MESH' for o in max_objs))),
        scenes=[dict(name=s.name,objects=[o.name for o in s.objects],units=dict(system=s.unit_settings.system,scale_length=s.unit_settings.scale_length,length_unit=s.unit_settings.length_unit),
            engine=s.render.engine,world=s.world.name if s.world else None,frame=s.frame_current) for s in bpy.data.scenes],
        collections=[dict(name=c.name,objects=[o.name for o in c.objects],hide_viewport=c.hide_viewport,hide_render=c.hide_render,properties=props(c)) for c in bpy.data.collections],
        worlds=[dict(name=w.name,use_nodes=w.use_nodes,nodes=[dict(name=n.name,type=n.bl_idname,inputs=[dict(name=s.name,value=serial(s.default_value) if hasattr(s,'default_value') else None) for s in n.inputs]) for n in w.node_tree.nodes] if w.node_tree else []) for w in bpy.data.worlds],
        text_blocks=[dict(name=t.name,filepath=t.filepath,use_module=t.use_module,characters=len(t.as_string()),sha256=hashlib.sha256(t.as_string().encode()).hexdigest()) for t in bpy.data.texts],
        libraries=[l.filepath for l in bpy.data.libraries],objects=objects,materials=materials,images=images,
        texture_files=texture_files,poser=poser,max_binary=max_info(originals/'Voyager Bridge Max2011.max'),max_partial_reader=partial_max,
        mesh468_occlusion=occlusion,
        view_layers=[dict(name=v.name,objects=[dict(name=o.name,hide_get=o.hide_get(view_layer=v),visible_get=o.visible_get(view_layer=v)) for o in v.objects]) for v in bpy.context.scene.view_layers])
    sys.path.insert(0,str(root/'scripts'))
    from informe_auditoria import enrich, write_report
    enrich(result)
    write_report(result,root)
    (out/'auditoria_voyager.json').write_text(json.dumps(result,ensure_ascii=True,indent=2,allow_nan=False),encoding='utf-8')
    print('AUDIT finalizado; originales intactos:',before==after,flush=True)
    if before!=after:raise RuntimeError('Los originales han cambiado durante la auditoría')


if __name__=='__main__':
    main()
