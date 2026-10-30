"""Read-only F07 inventory. Run with UE 5.8 PythonScript commandlet."""
import unreal as u
import json, pathlib, traceback

ROOT = pathlib.Path(u.Paths.project_dir()).resolve()
OUT = ROOT / 'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
OUT.mkdir(parents=True, exist_ok=True)
def write(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
def vec(v): return [v.x, v.y, v.z]
def safe(fn):
    try: return fn()
    except Exception as e: return {'error': str(e)}
def prop(o, n): return safe(lambda: str(o.get_editor_property(n)))

try:
    api={}
    for n in ['StaticMeshEditorSubsystem','EditorActorSubsystem','EditorLoadingAndSavingUtils',
              'ProceduralMeshLibrary','GeometryScript_AssetUtils','GeometryScript_MeshQueries',
              'GeometryScript_Collision','DynamicMesh','SystemLibrary','BodySetup','AggregateGeom']:
        c=getattr(u,n,None)
        api[n]={'doc': str(c.__doc__) if c else None,'members':dir(c) if c else []}
    write('api.json',api)
    world=u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/maps/L_F07_Sutherland_Test')
    actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
    smes=u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
    inventory={'engine':u.SystemLibrary.get_engine_version(),'actor_count':len(actors),'actors':[],'meshes':[]}
    meshes={}
    for a in actors:
        item={'name':a.get_name(),'label':a.get_actor_label(),'path':a.get_path_name(),
              'class':a.get_class().get_name(),'location':vec(a.get_actor_location()),
              'rotation':str(a.get_actor_rotation()),'scale':vec(a.get_actor_scale3d()),
              'bounds':safe(lambda:[vec(v) for v in a.get_actor_bounds(False)]),'components':[]}
        for c in a.get_components_by_class(u.PrimitiveComponent):
            ci={'name':c.get_name(),'class':c.get_class().get_name(),'transform':str(c.get_world_transform()),
                'enabled':str(c.get_collision_enabled()),'profile':str(c.get_collision_profile_name()),
                'object_type':str(c.get_collision_object_type()),'pawn_response':str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_PAWN))}
            if isinstance(c,u.StaticMeshComponent):
                m=c.static_mesh
                ci['mesh']=m.get_path_name() if m else None
                if m: meshes[m.get_path_name()]=m
            if isinstance(c,u.CapsuleComponent):
                ci['radius']=c.get_scaled_capsule_radius()
                ci['half_height']=c.get_scaled_capsule_half_height()
            item['components'].append(ci)
        inventory['actors'].append(item)
    assets=u.AssetRegistryHelpers.get_asset_registry().get_assets_by_path('/Game/star_trek_sutherland_bridge__2_/StaticMeshes',recursive=True)
    for ad in assets:
        m=ad.get_asset()
        if isinstance(m,u.StaticMesh): meshes[m.get_path_name()]=m
    for path,m in meshes.items():
        bs=m.get_editor_property('body_setup')
        d={'name':m.get_name(),'path':path,'bounds':str(m.get_bounds()),
           'complexity':prop(bs,'collision_trace_flag'),'double_sided':prop(bs,'double_sided_geometry'),
           'simple_count':safe(lambda:smes.get_simple_collision_count(m)),
           'convex_count':safe(lambda:smes.get_convex_collision_count(m)),
           'lods':m.get_num_lods(),'materials':[],
           'body_instance':prop(bs,'default_instance')}
        ag=bs.get_editor_property('agg_geom')
        d['aggregate']={n:prop(ag,n) for n in ['box_elems','sphere_elems','sphyl_elems','convex_elems']}
        for mat in m.get_editor_property('static_materials'):
            mi=mat.material_interface
            d['materials'].append({'slot':str(mat.material_slot_name),'material':mi.get_path_name() if mi else None})
        inventory['meshes'].append(d)
    inventory['dirty_content']=safe(lambda:[p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
    inventory['dirty_maps']=safe(lambda:[p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
    write('01_inventario_inicial.json',inventory)
    write('audit_status.json',{'ok':True})
except Exception:
    write('audit_status.json',{'ok':False,'traceback':traceback.format_exc()})
    raise
