"""Create a NEW safe rig with original frames and real Quinn.
Use VH_SOURCE_FILE from export_doors_v07.py and NEW VH_EVIDENCE_DIR.
Author in an authorized temporary copy; the approved validation map is portable.
"""
import json
import os
import traceback
from pathlib import Path
import unreal as u

outdir = Path(os.environ['VH_EVIDENCE_DIR']).resolve()
if outdir.exists() and any(outdir.iterdir()):
    raise RuntimeError('Use a new empty evidence directory')
outdir.mkdir(parents=True, exist_ok=True)
out = {'ok': False}
try:
    map_name = os.environ.get('VH_V07_RIG_MAP','/Game/VH07Test/L_DoorRig_WithFrames')
    assert map_name.startswith(('/Game/VH07Test/','/Game/ValhallaV07/Validation/')) and not u.EditorAssetLibrary.does_asset_exist(map_name)
    levels = u.get_editor_subsystem(u.LevelEditorSubsystem)
    assert levels.new_level(map_name)
    actors = u.get_editor_subsystem(u.EditorActorSubsystem)
    world = u.EditorLevelLibrary.get_editor_world()
    world.get_world_settings().set_editor_property('default_game_mode',u.EditorAssetLibrary.load_blueprint_class('/Game/ValhallaV06/Blueprints/BP_Valhalla_V06_GameMode'))
    floor = actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(2000,0,-20))
    floor.static_mesh_component.set_static_mesh(u.load_asset('/Engine/BasicShapes/Cube'))
    floor.set_actor_scale3d(u.Vector(70,30,.4))
    for location,scale in [((-1500,0,150),(.2,30,3)),((5500,0,150),(.2,30,3)),((2000,-1500,150),(70,.2,3)),((2000,1500,150),(70,.2,3))]:
        wall=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*location))
        wall.static_mesh_component.set_static_mesh(u.load_asset('/Engine/BasicShapes/Cube'))
        wall.set_actor_scale3d(u.Vector(*scale))
        wall.set_actor_label('Limite fisico del recinto de validacion')
    actors.spawn_actor_from_class(u.PlayerStart,u.Vector(-300,0,95))
    actors.spawn_actor_from_class(u.VH06Probe,u.Vector())
    sun = actors.spawn_actor_from_class(u.DirectionalLight,u.Vector(0,0,700),u.Rotator(pitch=-50))
    sun.get_component_by_class(u.DirectionalLightComponent).set_intensity(3)
    source = json.loads(Path(os.environ['VH_SOURCE_FILE']).read_text(encoding='utf8'))
    for i,row in enumerate(source['doors']):
        door = actors.spawn_actor_from_class(u.VHAutomaticDoor,u.Vector(i*1800,0,0))
        door.set_actor_label('Rig_'+row['id'])
        door.set_editor_property('door_id',u.Name('V07_'+row['id']))
        for j,key in enumerate(['left_leaf','right_leaf']):
            door.get_editor_property(key).set_static_mesh(u.load_asset('/Game/ValhallaV07/Meshes/'+row['id']+'_Leaf'+str(j)))
            door.set_editor_property('left_closed_location' if j==0 else 'right_closed_location',u.Vector(*row['leaves'][j]['closed']))
        for key,value in [('opening_width',row['width']),('opening_height',row['height']),('travel_distance',row['travel']),('proximity_depth',240.),('movement_duration',.8),('use_configured_travel',True),('left_travel',u.Vector(0,-row['travel'],0)),('right_travel',u.Vector(0,row['travel'],0)),('left_clearance_offset',u.Vector(20 if row['id']=='D04' else -20,0,0)),('right_clearance_offset',u.Vector(20 if row['id']=='D04' else -20,0,0))]:
            door.set_editor_property(key,value)
        frame = actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(i*1800+row['rig_frame_location'][0],row['rig_frame_location'][1],row['rig_frame_location'][2]),u.Rotator(roll=row['rig_frame_roll']))
        frame.static_mesh_component.set_static_mesh(u.load_asset(row['rig_frame_asset']))
        door.set_destination_constructed(True)
        door.set_security_locked(False)
        door.set_external_access_allowed(True)
        door.reset_closed()
    assert levels.save_current_level()
    out.update(ok=True, map=map_name, real_game_validation_required=True)
except Exception:
    out['error'] = traceback.format_exc()
    u.log_error(out['error'])
finally:
    (outdir/'rig_author_v07.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    u.SystemLibrary.quit_editor()
