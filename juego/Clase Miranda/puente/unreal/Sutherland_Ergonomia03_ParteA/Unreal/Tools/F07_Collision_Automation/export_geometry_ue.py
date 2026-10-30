import unreal as u
import json, pathlib, traceback
ROOT=pathlib.Path(u.Paths.project_dir()).resolve()
OUT=ROOT/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
def vec(v): return [v.x,v.y,v.z]
def write(n,d): (OUT/n).write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8')
try:
    docs={}
    for c,names in [(u.ProceduralMeshLibrary,['get_section_from_static_mesh']),
                    (u.GeometryScript_AssetUtils,['copy_mesh_from_static_mesh']),
                    (u.GeometryScript_MeshQueries,['get_all_vertex_positions','get_all_triangle_indices']),
                    (u.SystemLibrary,['capsule_trace_single_by_profile','line_trace_single_by_profile']),
                    (u.Transform,['transform_location','inverse_transform_location'])]:
        for n in names: docs[c.__name__+'.'+n]=str(getattr(c,n).__doc__)
    write('method_docs.json',docs)
    u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/maps/L_F07_Sutherland_Test')
    actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
    result={'instances':[],'meshes':{},'errors':[]}
    for a in actors:
        for c in a.get_components_by_class(u.StaticMeshComponent):
            m=c.static_mesh
            if not m: continue
            t=c.get_world_transform()
            path=m.get_path_name()
            result['instances'].append({'actor':a.get_name(),'label':a.get_actor_label(),'mesh':path,
                'translation':vec(t.translation),'rotation':[t.rotation.x,t.rotation.y,t.rotation.z,t.rotation.w],
                'scale':vec(t.scale3d),'bounds':[vec(v) for v in a.get_actor_bounds(False)],
                'enabled':str(c.get_collision_enabled()),'profile':str(c.get_collision_profile_name())})
            if path in result['meshes']: continue
            bs=m.get_editor_property('body_setup'); ag=bs.get_editor_property('agg_geom')
            md={'sections':[], 'primitives':{n:len(ag.get_editor_property(n)) for n in ['box_elems','sphere_elems','sphyl_elems','convex_elems']}}
            for sec in range(m.get_num_sections(0)):
                vv,tt,nn,uv,tan=u.ProceduralMeshLibrary.get_section_from_static_mesh(m,0,sec)
                md['sections'].append({'vertices':[vec(v) for v in vv],'triangles':list(tt)})
            result['meshes'][path]=md
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    ws=world.get_world_settings()
    result['world_game_mode']=str(ws.get_editor_property('default_game_mode'))
    result['default_game_mode']=str(u.GameMapsSettings.get_game_maps_settings().get_editor_property('global_default_game_mode')) if hasattr(u,'GameMapsSettings') else None
    result['pawn_defaults']={}
    for cl in [u.DefaultPawn,u.Character,u.GameModeBase]:
        cd=u.get_default_object(cl)
        result['pawn_defaults'][cl.__name__]={'properties':str(cd)}
        if isinstance(cd,u.Pawn):
            result['pawn_defaults'][cl.__name__]['components']=[str(x) for x in cd.get_components_by_class(u.PrimitiveComponent)]
    result['floor_trace']=str(u.SystemLibrary.line_trace_single_by_profile(world,u.Vector(0,750,300),u.Vector(0,750,-100),'Pawn',False,[],u.DrawDebugTrace.NONE,True))
    write('geometria.json',result)
    write('geometry_status.json',{'ok':True})
except Exception:
    write('geometry_status.json',{'ok':False,'traceback':traceback.format_exc()})
    raise
