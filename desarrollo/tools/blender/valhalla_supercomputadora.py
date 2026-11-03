"""Reconstrucción conservadora de los bancos Valhalla, Blender 5.2 / OpenSKP 1.3.

Ejecutar con Blender --background --factory-startup --python ESTE_ARCHIVO --
  --source-dir FUENTES --output-dir SALIDAS_NUEVAS --evidence-dir EVIDENCIAS
Requiere el lector OpenSKP previamente instalado. No instala dependencias.
Las salidas deben estar en una carpeta vacía, distinta de las fuentes.
"""
import argparse
import hashlib
import json
import os
import sys
import zipfile
from collections import Counter
from pathlib import Path

import bpy
import bmesh
import numpy as np
from mathutils import Matrix, Vector

ROOM = 'Sala computadora completa (con circulos vacios)'
SEMI = 'Semicirculo_computadora'
EXCLUDE = {'ROOT_MODEL', 'Component#200', 'Component#58', 'Component#202', 'Image'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def get_reader(evidence):
    version = f'{bpy.app.version[0]}.{bpy.app.version[1]}'
    base = Path(os.environ['APPDATA']) / 'Blender Foundation/Blender' / version / 'extensions/.local/lib'
    for site in base.glob('python*/site-packages'):
        sys.path.insert(0, str(site))
    # Factory startup may clean the extension's shared dependency environment.
    # Use only wheels already supplied with the installed extension, in isolation.
    wheels=base.parent.parent/'blender_org/openskp_import_export/wheels'
    isolated=evidence/'reader_dependencies'
    isolated.mkdir(exist_ok=True)
    tag=f'cp{sys.version_info.major}{sys.version_info.minor}'
    for wheel in wheels.glob('*.whl'):
        if 'py3-none-any' in wheel.name or f'{tag}-{tag}-win_amd64' in wheel.name:
            with zipfile.ZipFile(wheel) as archive:archive.extractall(isolated)
    sys.path.insert(0,str(isolated))
    sys.dont_write_bytecode=True
    import openskp
    return openskp


def recover_materials(skp_scene, evidence, prefix):
    """Match IDs AND colors, then restore only the original shader information."""
    log = []
    images = {}
    for index, original in enumerate(skp_scene.gltf_materials):
        material = bpy.data.materials.get(f'openskp_material_{index}')
        if material is None:
            raise ValueError(f'Material original ausente: {index}')
        pbr = original['pbrMetallicRoughness']
        color = pbr['baseColorFactor']
        if max(abs(a-b) for a,b in zip(material.diffuse_color,color)) > 1e-5:
            raise ValueError(f'Índice/color no corresponde: {material.name}')
        shader = next(n for n in material.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
        if shader.inputs['Base Color'].is_linked:
            raise ValueError('No sustituir conexiones existentes sin revisión')
        shader.inputs['Base Color'].default_value = (*color[:3], 1)
        shader.inputs['Alpha'].default_value = color[3]
        record = {'material': material.name, 'color': color, 'texture': None}
        ref = pbr.get('baseColorTexture')
        if ref:
            idx = ref['index']
            tex = skp_scene.textures[idx]
            if idx not in images:
                suffix = '.png' if tex.mime_type == 'image/png' else '.jpg'
                disk = evidence / f'{prefix}_original_texture_{idx}{suffix}'
                disk.write_bytes(tex.data)
                image = bpy.data.images.load(str(disk), check_existing=False)
                image.name = Path(tex.filename.replace('\\','/')).name
                image.pack()
                image.filepath = '//' + image.name
                images[idx] = image
            image = images[idx]
            node = material.node_tree.nodes.new('ShaderNodeTexImage')
            node.name = 'Imagen original recuperada de SketchUp'
            node.image = image
            material.node_tree.links.new(node.outputs['Color'], shader.inputs['Base Color'])
            if image.depth in (32,128):
                material.node_tree.links.new(node.outputs['Alpha'], shader.inputs['Alpha'])
            record['texture'] = image.name
        material.use_backface_culling = False
        if color[3] < 1 or (ref and images[ref['index']].depth in (32,128)):
            material.surface_render_method = 'DITHERED'
        log.append(record)
    return log


def placed():
    return [(i.object.original, i.matrix_world.copy())
            for i in bpy.context.evaluated_depsgraph_get().object_instances
            if i.object.type == 'MESH' and len(i.object.data.polygons)]


def coordinates(obj, matrix):
    return np.array([matrix @ v.co for v in obj.data.vertices])


def register_roof(source, target, flip):
    """Translation consensus followed by submillimetric nearest-point refinement."""
    source = np.unique(np.round(source,6),axis=0) * np.array([1,flip,1])
    target = np.unique(np.round(target,6),axis=0)
    differences = (target[:,None,:]-source[None,:,:]).reshape(-1,3)
    candidate = np.array(Counter(map(tuple,np.round(differences,3))).most_common(1)[0][0])
    distances = np.linalg.norm(source[:,None,:]+candidate-target[None,:,:],axis=2)
    nearest = distances.argmin(1)
    good = distances.min(1) < .003
    shift = np.median(target[nearest[good]]-source[good],axis=0)
    errors = np.linalg.norm(source+shift-target[nearest],axis=1)
    assert good.sum() >= 120, 'La arquitectura no admite esta alineación'
    return shift, {'matched':int(good.sum()),'source_points':len(source),
                   'max_matched_error_m':float(errors[good].max()),
                   'unmatched_points':source[~good].tolist()}


def mirrored_mesh(mesh, cache):
    if mesh.name not in cache:
        copy = mesh.copy()
        copy.name = mesh.name + '_Espejo_Normal_Corregida'
        copy.transform(Matrix.Diagonal((-1,1,1,1)))
        bm = bmesh.new(); bm.from_mesh(copy)
        bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
        bm.to_mesh(copy); bm.free(); copy.update()
        cache[mesh.name] = copy
    return cache[mesh.name]


def save(path):
    bpy.context.preferences.filepaths.save_version = 0
    bpy.context.view_layer.update()
    # Packed images are self-contained; avoid source-directory remapping on Save As.
    for image in bpy.data.images:
        if image.source=='FILE' and image.packed_file:
            image.filepath='//'+image.name
    bpy.ops.wm.save_as_mainfile(filepath=str(path), compress=True, relative_remap=False)


def frame_view(center, distance):
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type=='VIEW_3D':
                area.spaces.active.region_3d.view_location=center
                area.spaces.active.region_3d.view_distance=distance
                area.spaces.active.region_3d.view_rotation=Vector((1,-1,1)).to_track_quat('Z','Y')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-dir',required=True,type=Path)
    parser.add_argument('--output-dir',required=True,type=Path)
    parser.add_argument('--evidence-dir',required=True,type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    source=args.source_dir.resolve(); output=args.output_dir.resolve(); evidence=args.evidence_dir.resolve()
    if output == source or (output.exists() and any(output.iterdir())):
        raise ValueError('Se requiere una carpeta de salida nueva/vacía')
    output.mkdir(parents=True,exist_ok=True); evidence.mkdir(parents=True,exist_ok=True)
    originals={p.name:digest(p) for p in source.iterdir() if p.suffix.lower() in {'.blend','.skp'}}
    reader=get_reader(evidence)
    audit={'blender':bpy.app.version_string,'originals':originals,'materials':{},'alignment':[]}
    bpy.ops.wm.open_mainfile(filepath=str(source/(ROOM+'.blend')))
    room_roofs=[coordinates(o,m) for o,m in placed() if o.name=='Component#194']
    room_scene=reader.SkpFile.open(str(source/(ROOM+'.skp'))).build_instanced_scene()
    audit['materials']['room']=recover_materials(room_scene,evidence,'sala')
    save(output/'Sala_computadora_Materiales_Recuperados.blend')
    bpy.ops.wm.open_mainfile(filepath=str(source/(SEMI+'.blend')))
    semi_scene=reader.SkpFile.open(str(source/(SEMI+'.skp'))).build_instanced_scene()
    audit['materials']['semi']=recover_materials(semi_scene,evidence,'semicirculo')
    save(output/'Semicirculo_computadora_Materiales_Recuperados.blend')
    instances=placed()
    source_roof=next(coordinates(o,m) for o,m in instances if o.name=='Component#58')
    mirror_x=float(source_roof[:,0].min())
    banks=[(o,m) for o,m in instances if o.name not in EXCLUDE]
    points=np.concatenate([coordinates(o,m) for o,m in banks])
    center_y=float((points[:,1].min()+points[:,1].max())/2)
    center=Vector((mirror_x,center_y,.37))
    audit['bank_source_bounds']=[points.min(0).tolist(),points.max(0).tolist()]
    radial=np.linalg.norm(points[:,:2]-np.array(center[:2]),axis=1)
    audit['radial_envelope_m']={'inner_radius':float(radial.min()),'outer_radius':float(radial.max())}
    audit['mirror_plane_x']=mirror_x
    audit['master_origin']=list(center)
    for idx,target in enumerate(sorted(room_roofs,key=lambda a:a[:,1].max(),reverse=True)):
        flip=1 if idx==0 else -1
        shift,validation=register_roof(source_roof,target,flip)
        audit['alignment'].append({'flip_y':flip,'shift':shift.tolist(),'uniform_scale':1.0,**validation})
    # A new scene makes the deliverable independent of the original collection graph.
    scene=bpy.data.scenes.new('Bancos_Datos_Circulo_Maestro')
    bpy.context.window.scene=scene
    scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
    master=bpy.data.collections.new('VALHALLA_BANCOS_MAESTRO')
    scene.collection.children.link(master)
    halves=[]; cache={}; seen=set();duplicates=0
    reflection=Matrix.Diagonal((-1,1,1,1))
    world_reflection=Matrix.Translation((2*mirror_x,0,0))@reflection
    normalize=Matrix.Translation(-center)
    for side in ['A_Original','B_Espejo']:
        col=bpy.data.collections.new('Semicirculo_'+side);master.children.link(col);halves.append(col)
        for idx,(src,matrix) in enumerate(banks):
            key=(src.data.name,tuple(round(v,7) for row in matrix for v in row))
            if side=='A_Original':
                if key in seen:duplicates+=1;continue
                seen.add(key)
            elif key not in seen:continue
            final=normalize@(matrix if side=='A_Original' else world_reflection@matrix)
            data=src.data
            if final.determinant()<0:
                data=mirrored_mesh(src.data,cache);final=final@reflection
            obj=bpy.data.objects.new(f'Banco_{side}_{idx:04d}_{src.name}',data)
            col.objects.link(obj);obj.matrix_world=final
            obj['fuente_componente']=src.name;obj['fuente_instancia']=idx
    # Remove repeated placements on the mirrored side too, if source contained any.
    keys=set()
    for obj in list(halves[1].objects):
        key=(obj.data.name,tuple(round(v,7) for row in obj.matrix_world for v in row))
        if key in keys:bpy.data.objects.remove(obj,do_unlink=True)
        else:keys.add(key)
    audit['duplicate_source_placements_removed']=duplicates
    audit['bank_objects_per_circle']=len(halves[0].objects)+len(halves[1].objects)
    scene['origen_fuente']=SEMI+'.blend';scene['escala_uniforme']=1.0
    # Retain only the new scene, source datablocks used by its linked meshes survive.
    for other in list(bpy.data.scenes):
        if other!=scene:bpy.data.scenes.remove(other)
    frame_view((0,0,1.5),26)
    save(output/'Computadora_Circulo_Completo_V01.blend')
    scene.name='Bancos_Datos_Ajustados_Metros'
    scene['ajuste']='Escala 1:1; alineación por 125 vértices arquitectónicos; ejes Z-up'
    save(output/'Computadora_Circulo_Ajustado_V02.blend')
    bpy.ops.wm.open_mainfile(filepath=str(output/'Sala_computadora_Materiales_Recuperados.blend'))
    original_objects={o.name for o in bpy.context.scene.objects}
    with bpy.data.libraries.load(str(output/'Computadora_Circulo_Ajustado_V02.blend'),link=False) as (available,loaded):
        loaded.collections=['VALHALLA_BANCOS_MAESTRO']
    imported=loaded.collections[0]
    # Unlinked collections are absent from the depsgraph: matrix_world is stale.
    # These master meshes have no parents; their saved matrix_basis is authoritative.
    imported_items=[(obj,obj.matrix_basis.copy()) for obj in imported.all_objects]
    # Copies with local reflections avoid negative object transforms in both rooms.
    placements=bpy.data.collections.new('VALHALLA_BANCOS_INTEGRADOS')
    bpy.context.scene.collection.children.link(placements)
    flip_cache={}
    for idx,alignment in enumerate(audit['alignment']):
        col=bpy.data.collections.new(f'Banco_Circular_{idx+1:02d}');placements.children.link(col)
        transform=Matrix.Translation(Vector(alignment['shift']))@Matrix.Diagonal((1,alignment['flip_y'],1,1))@Matrix.Translation(center)
        for src,basis in imported_items:
            final=transform@basis;data=src.data
            if final.determinant()<0:data=mirrored_mesh(data,flip_cache);final=final@reflection
            obj=bpy.data.objects.new(f'C{idx+1:02d}_{src.name}',data);col.objects.link(obj);obj.matrix_world=final
            for key in src.keys():obj[key]=src[key]
    # The appended master is unlinked; delete only imported construction objects.
    for obj in list(imported.all_objects):bpy.data.objects.remove(obj,do_unlink=True)
    for child in list(imported.children):bpy.data.collections.remove(child)
    bpy.data.collections.remove(imported)
    assert original_objects <= {o.name for o in bpy.context.scene.objects}
    bpy.context.view_layer.update()
    inserted=[o for o in bpy.context.scene.objects if o.name.startswith(('C01_Banco','C02_Banco'))]
    zvalues=[]; vertex_cache={}
    for obj in inserted:
        if obj.data.name not in vertex_cache:
            values=np.empty(len(obj.data.vertices)*3)
            obj.data.vertices.foreach_get('co',values)
            vertex_cache[obj.data.name]=values.reshape(-1,3)
        row=np.array(obj.matrix_world)[2]
        z=vertex_cache[obj.data.name]@row[:3]+row[3]
        zvalues.extend((float(z.min()),float(z.max())))
    assert abs(min(zvalues)-.37)<1e-4 and abs(max(zvalues)-3.6863503)<1e-4, f'Altura integrada incorrecta: {min(zvalues)}, {max(zvalues)}'
    assert all(o.matrix_world.determinant()>0 for o in inserted), 'Espejo sin corregir'
    audit['integrated_z_bounds']=[min(zvalues),max(zvalues)]
    audit['original_scene_objects_preserved']=len(original_objects)
    audit['integrated_circles']=2
    bpy.context.scene['validacion_UE5']='Pendiente: colisiones, navegación y rendimiento dentro de Unreal Engine'
    bpy.context.scene['estado_geometrico']='PARCIAL: contactos paneles/estructura pendientes; consultar informe técnico'
    frame_view((30,-2.47,1.5),65)
    save(output/'Sala_Supercomputadora_Valhalla_Integrada_V03.blend')
    save(output/'Sala_Supercomputadora_Enterprise_G_FINAL.blend')
    for name,sha in originals.items():assert digest(source/name)==sha,'Original modificado'
    (evidence/'construccion.json').write_text(json.dumps(audit,indent=2),encoding='utf8')
    print('CONSTRUCCION_OK',json.dumps({k:v for k,v in audit.items() if k not in ['materials','originals']}),flush=True)


if __name__=='__main__':main()
