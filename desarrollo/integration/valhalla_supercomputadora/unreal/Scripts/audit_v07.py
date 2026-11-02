"""Reopen the PARTIAL V07 map with a real RHI. Results are technical checks,
not certification that the still-open architectural inventory is complete.
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
out = {'ok': False, 'v07_complete': False, 'inventory_exhaustive': False}
try:
    map_name = '/Game/ValhallaV07/Maps/L_Supercomputadora_V07'
    world = u.EditorLoadingAndSavingUtils.load_map(map_name)
    u.VH06Tools.finish_compilation()
    actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
    out['map_check'] = json.loads(u.VH06Tools.map_check_snapshot())
    out['material_resources'] = json.loads(u.VH06Tools.material_resource_snapshot())
    out['static_instances'] = sum(c.get_instance_count() for a in actors for c in a.get_components_by_class(u.InstancedStaticMeshComponent))
    out['boundaries'] = [a.get_actor_label() for a in actors if 'V06_VISIBLE_BOUNDARY' in [str(t) for t in a.tags]]
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
    out['ok'] = ids == {'VALHALLA_SC_EXTERIOR_D01','V07_D02','V07_D03','V07_D04'} and safe and out['static_instances'] == 16299 and len(out['boundaries']) == 14 and not missing and out['validation_map_exists'] and not out['unexpected_test_dependencies'] and '/Game/ValhallaV06/Blueprints/BP_Valhalla_V06_GameMode' in out['game_mode'] and out['map_check']['errors'] == 0 and out['map_check']['warnings'] == 0 and out['material_resources'].get('ok',False)
except Exception:
    out['error'] = traceback.format_exc()
    u.log_error(out['error'])
finally:
    (outdir/'audit_v07.json').write_text(json.dumps(out, indent=2), encoding='utf8')
    u.SystemLibrary.quit_editor()
