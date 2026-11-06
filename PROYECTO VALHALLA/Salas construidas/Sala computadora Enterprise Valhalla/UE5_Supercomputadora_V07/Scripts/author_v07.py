"""UE Python, two separate invocations: VH_V07_STAGE=copy, then author.
Use a new project prepared by prepare_v07.py and a NEW VH_EVIDENCE_DIR each run.
VH_SOURCE_FILE is the generated manifest from export_doors_v07.py.
The resulting map is explicitly PARTIAL; successful authoring is not full coverage.
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
result = {'ok': False, 'v07_complete': False, 'inventory_exhaustive': False}
try:
    stage = os.environ['VH_V07_STAGE']
    target = '/Game/ValhallaV07/Maps/L_Supercomputadora_V07'
    if stage == 'copy':
        assert not u.EditorAssetLibrary.does_asset_exist(target), 'Never overwrite an existing delivery'
        world = u.EditorLoadingAndSavingUtils.load_map('/Game/Valhalla/Maps/L_Supercomputadora_V06_Quinn')
        assert u.EditorLoadingAndSavingUtils.save_map(world, target)
        result.update(ok=True, reopen_required=True)
    elif stage == 'author':
        world = u.EditorLoadingAndSavingUtils.load_map(target)
        u.VH06Tools.finish_compilation()
        result['build'] = json.loads(u.VHAutomaticDoorTools.build_door_extensions(os.environ['VH_SOURCE_FILE']))
        assert result['build']['ok'], result['build']
        result['collision'] = []
        for door in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
            if isinstance(door, u.VHAutomaticDoor) and str(door.door_id).startswith('V07_'):
                check = json.loads(u.VHAutomaticDoorTools.set_v07_leaf_collision_inset(door, 1.0 if str(door.door_id)=='V07_D02' else 3.2))
                assert check['ok']
                result['collision'].append({'id': str(door.door_id), 'result': check})
                door.reset_closed()
        assert u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level()
        result['map_check'] = json.loads(u.VH06Tools.map_check_snapshot())
        result['ok'] = result['map_check']['errors'] == 0 and result['map_check']['warnings'] == 0
        result['reopen_required'] = True
    else:
        raise ValueError('VH_V07_STAGE must be copy or author')
except Exception:
    result['error'] = traceback.format_exc()
    u.log_error(result['error'])
finally:
    (outdir/'author_v07.json').write_text(json.dumps(result, indent=2), encoding='utf8')
    u.SystemLibrary.quit_editor()
