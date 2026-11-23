"""Add only the two approved V07 safety closures in an isolated project copy.

Requires a NEW VH_EVIDENCE_DIR. Never run authoring on the preserved delivery.
Does not change doors, original architecture, stairs, materials or V06 closures.
The saved map uses only existing /Game materials and the engine cube.
"""
import hashlib
import json
import os
import traceback
from pathlib import Path

import unreal as u

MAP = '/Game/ValhallaV07/Maps/L_Supercomputadora_V07'
TAG = 'V07_CLOSURE_VISIBLE_BOUNDARY'


def preserved_snapshot(actors):
    """Compare authored properties, not transient editor object addresses."""
    def transform(t):
        return [[t.translation.x, t.translation.y, t.translation.z],
                [t.rotation.x, t.rotation.y, t.rotation.z, t.rotation.w],
                [t.scale3d.x, t.scale3d.y, t.scale3d.z]]

    def mesh_state(c):
        return [c.static_mesh.get_path_name(), str(c.get_collision_enabled()),
                [m.get_path_name() if m else None for m in c.get_materials()]]

    rows = []
    for actor in actors.get_all_level_actors():
        if isinstance(actor, u.VHAutomaticDoor):
            props = {}
            for key in ('door_id', 'destination_constructed', 'security_locked', 'external_access_allowed',
                        'use_configured_travel', 'left_closed_location', 'right_closed_location',
                        'left_travel', 'right_travel', 'left_clearance_offset', 'right_clearance_offset',
                        'travel_distance', 'clearance_fraction', 'opening_width', 'opening_height',
                        'movement_duration', 'close_delay', 'proximity_depth', 'open_fraction'):
                value = actor.get_editor_property(key)
                props[key] = [value.x, value.y, value.z] if isinstance(value, u.Vector) else str(value)
            rows.append(('door', actor.get_actor_label(), transform(actor.get_actor_transform()), props,
                         mesh_state(actor.left_leaf), mesh_state(actor.right_leaf)))
        for component in actor.get_components_by_class(u.InstancedStaticMeshComponent):
            rows.append(('architecture', actor.get_actor_label(), component.get_name(), mesh_state(component),
                         [transform(component.get_instance_transform(i, world_space=True))
                          for i in range(component.get_instance_count())]))
        if 'V06_VISIBLE_BOUNDARY' in [str(t) for t in actor.tags]:
            rows.append(('boundary', actor.get_actor_label(), transform(actor.get_actor_transform()),
                         mesh_state(actor.static_mesh_component)))
    return hashlib.sha256(json.dumps(sorted(rows)).encode('utf8')).hexdigest()


outdir = Path(os.environ['VH_EVIDENCE_DIR']).resolve()
if outdir.exists() and any(outdir.iterdir()):
    raise RuntimeError('Use a new empty evidence directory')
outdir.mkdir(parents=True, exist_ok=True)
out = {'ok': False}
try:
    world = u.EditorLoadingAndSavingUtils.load_map(MAP)
    u.VH06Tools.finish_compilation()
    actors = u.get_editor_subsystem(u.EditorActorSubsystem)
    assert not any(TAG in [str(t) for t in a.tags] for a in actors.get_all_level_actors()), 'Closures already exist'
    before = preserved_snapshot(actors)
    cube = u.load_asset('/Engine/BasicShapes/Cube')
    blue = u.load_asset('/Game/Valhalla/Materials/M_061')
    white = u.load_asset('/Game/Valhalla/Materials/M_099')
    assert cube and blue and white
    out['closures'] = []
    for row in json.loads(Path(__file__).with_name('v07_closures.json').read_text(encoding='utf8')):
        x, y = row['center_xy']
        rotation = u.Rotator(pitch=0, yaw=row['yaw_deg'], roll=0)
        for header in (False, True):
            z = row['bottom_cm'] + (row['height_cm'] - 4 if header else row['height_cm'] / 2)
            actor = actors.spawn_actor_from_class(u.StaticMeshActor, u.Vector(x, y, z), rotation)
            actor.set_actor_label('V07_' + row['id'] + ('_Remate' if header else ''))
            actor.set_editor_property('tags', [u.Name(TAG), u.Name(row['id'])])
            c = actor.static_mesh_component
            c.set_static_mesh(cube)
            c.set_material(0, white if header else blue)
            c.set_collision_profile_name('BlockAll')
            actor.set_actor_scale3d(u.Vector(.14 if header else row['thickness_cm']/100,
                                             row['width_cm']/100, .08 if header else row['height_cm']/100))
        out['closures'].append(row)
    after = preserved_snapshot(actors)
    out['preserved_before'] = before
    out['preserved_after'] = after
    assert before == after, 'Existing authored actors changed'
    assert actors and u.EditorLoadingAndSavingUtils.save_map(world, MAP)
    out['map_check'] = json.loads(u.VH06Tools.map_check_snapshot())
    out['ok'] = out['map_check']['errors'] == 0 and out['map_check']['warnings'] == 0
except Exception:
    out['error'] = traceback.format_exc()
    u.log_error(out['error'])
finally:
    (outdir/'author_v07_closure.json').write_text(json.dumps(out, indent=2), encoding='utf8')
    u.SystemLibrary.quit_editor()
