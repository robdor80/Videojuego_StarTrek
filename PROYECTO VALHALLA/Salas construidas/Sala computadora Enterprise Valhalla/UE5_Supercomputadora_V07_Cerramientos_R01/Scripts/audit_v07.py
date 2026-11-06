"""Reopen the V07 practical delivery with a real RHI. Technical checks do not
replace the independent final review or the user's personal play acceptance.
VH_EVIDENCE_DIR must be a new authorized temporary directory.
"""
import collections
import json
import os
import traceback
from pathlib import Path
import unreal as u

outdir = Path(os.environ['VH_EVIDENCE_DIR']).resolve()
if outdir.exists() and any(outdir.iterdir()):
    raise RuntimeError('Use a new empty evidence directory')
outdir.mkdir(parents=True, exist_ok=True)
out = {'ok': False, 'formal_closure_pending': True}
try:
    map_name = '/Game/ValhallaV07/Maps/L_Supercomputadora_V07'
    world = u.EditorLoadingAndSavingUtils.load_map(map_name)
    u.VH06Tools.finish_compilation()
    actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
    out['map_check'] = json.loads(u.VH06Tools.map_check_snapshot())
    out['material_resources'] = json.loads(u.VH06Tools.material_resource_snapshot())
    out['static_instances'] = sum(c.get_instance_count() for a in actors for c in a.get_components_by_class(u.InstancedStaticMeshComponent))
    out['boundaries'] = [a.get_actor_label() for a in actors if 'V06_VISIBLE_BOUNDARY' in [str(t) for t in a.tags]]
    out['closure_boundaries'] = [a.get_actor_label() for a in actors if 'V07_CLOSURE_VISIBLE_BOUNDARY' in [str(t) for t in a.tags]]
    out['closure_geometry'] = []
    closure_ok = True
    for row in json.loads(Path(__file__).with_name('v07_closures.json').read_text(encoding='utf8')):
        matches = [a for a in actors if a.get_actor_label() == 'V07_' + row['id']]
        valid = len(matches) == 1
        if valid:
            actor = matches[0]; pos = actor.get_actor_location(); scale = actor.get_actor_scale3d()
            valid = (abs(pos.x-row['center_xy'][0]) < .01 and abs(pos.y-row['center_xy'][1]) < .01
                     and abs(pos.z-row['bottom_cm']-row['height_cm']/2) < .01
                     and abs(scale.x-row['thickness_cm']/100) < .001
                     and abs(scale.y-row['width_cm']/100) < .001
                     and abs(scale.z-row['height_cm']/100) < .001
                     and abs(actor.get_actor_rotation().yaw-row['yaw_deg']) < .01
                     and str(actor.static_mesh_component.get_collision_profile_name()) == 'BlockAll'
                     and actor.static_mesh_component.static_mesh.get_path_name() == '/Engine/BasicShapes/Cube.Cube')
        out['closure_geometry'].append({'id': row['id'], 'valid': valid})
        closure_ok &= valid
    out['doors'] = []
    for a in actors:
        if isinstance(a, u.VHAutomaticDoor):
            out['doors'].append({'id': str(a.door_id), 'position_cm': [a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z], 'yaw': a.get_actor_rotation().yaw,
                                 'constructed': a.destination_constructed, 'locked': a.security_locked,
                                 'external_access_allowed': a.external_access_allowed, 'fraction': a.open_fraction, 'clearance_offset_x_cm': a.left_clearance_offset.x,
                                 'left_mesh': a.left_leaf.static_mesh.get_path_name(), 'right_mesh': a.right_leaf.static_mesh.get_path_name()})
    registry = u.AssetRegistryHelpers.get_asset_registry()
    registry.scan_paths_synchronous(['/Game'], True)
    options = u.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True,
                                               include_searchable_names=False, include_soft_management_references=False,
                                               include_hard_management_references=False)
    validation_map='/Game/ValhallaV07/Validation/L_V07_Puertas_Validacion'
    out['validation_map_exists']=u.EditorAssetLibrary.does_asset_exist(validation_map)
    queue = collections.deque([map_name,validation_map]); seen = set()
    while queue:
        name = queue.popleft()
        if name in seen or not name.startswith('/Game/'):
            continue
        seen.add(name)
        queue.extend(str(x) for x in registry.get_dependencies(name, options))
    content = Path(u.Paths.project_content_dir()); missing = []
    for name in sorted(seen):
        path = content/name.removeprefix('/Game/')
        if not path.with_suffix('.uasset').is_file() and not path.with_suffix('.umap').is_file():
            missing.append(name)
    out['packages'] = sorted(seen); out['missing_packages'] = missing
    out['unexpected_test_dependencies']=[x for x in seen if x.startswith('/Game/VH07Test/')]
    out['game_mode']=world.get_world_settings().get_editor_property('default_game_mode').get_path_name()
    ids = {r['id'] for r in out['doors']}
    safe = all(not r['constructed'] and r['locked'] and r['fraction'] == 0 for r in out['doors'] if r['id'].startswith('V07_'))
    expected_closures = {'V07_' + r['id'] + suffix
                         for r in json.loads(Path(__file__).with_name('v07_closures.json').read_text(encoding='utf8'))
                         for suffix in ('', '_Remate')}
    out['ok'] = ids == {'VALHALLA_SC_EXTERIOR_D01','V07_D02','V07_D03','V07_D04'} and safe and out['static_instances'] == 16299 and len(out['boundaries']) == 14 and set(out['closure_boundaries']) == expected_closures and closure_ok and not missing and out['validation_map_exists'] and not out['unexpected_test_dependencies'] and '/Game/ValhallaV06/Blueprints/BP_Valhalla_V06_GameMode' in out['game_mode'] and out['map_check']['errors'] == 0 and out['map_check']['warnings'] == 0 and out['material_resources'].get('ok',False)
except Exception:
    out['error'] = traceback.format_exc()
    u.log_error(out['error'])
finally:
    (outdir/'audit_v07.json').write_text(json.dumps(out, indent=2), encoding='utf8')
    u.SystemLibrary.quit_editor()
