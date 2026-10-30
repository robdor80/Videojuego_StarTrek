"""Keep walkable wall collision while allowing existing WorldDynamic leaves in their pockets."""
import unreal as u,pathlib,json,shutil,traceback
R=pathlib.Path(__file__).parent;P=R.parent/'Unreal';out={'ok':False,'walls':[]}
try:
    source=P/'Content/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01.umap';backup=R/'Backups/L_PBR_AntesColisionAlojamientos.umap'
    if not backup.exists():shutil.copy2(source,backup)
    L=u.get_editor_subsystem(u.LevelEditorSubsystem);A=u.get_editor_subsystem(u.EditorActorSubsystem);assert L.load_level('/Game/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01')
    actors={a.get_actor_label():a for a in A.get_all_level_actors()}
    response=actors['PBR_Plane.013_0'].static_mesh_component.get_collision_response_to_channel(u.CollisionChannel.ECC_PAWN)
    enum=type(response);out['response_type']=str(enum);out['response_values']=dir(enum)
    ignore=getattr(enum,next(k for k in dir(enum) if 'IGNORE' in k.upper()))
    block=getattr(enum,next(k for k in dir(enum) if 'BLOCK' in k.upper()))
    for n in ['Plane.013_0','Plane.004_0','Plane.010_0','Plane.039_0','Plane.011_0']:
        a=actors['PBR_'+n];c=a.static_mesh_component;c.set_collision_response_to_channel(u.CollisionChannel.ECC_WORLD_DYNAMIC,ignore)
        assert c.get_collision_response_to_channel(u.CollisionChannel.ECC_PAWN)==block
        assert c.get_collision_response_to_channel(u.CollisionChannel.ECC_CAMERA)==block
        out['walls'].append({'actor':a.get_actor_label(),'WorldDynamic':'Ignore','Pawn':'Block','Camera':'Block','geometry_changed':False})
    assert L.save_current_level();out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(R/'leaf_pockets.json').write_text(json.dumps(out,indent=2));print('LEAF_POCKETS',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
