"""Author only in a new isolated copy; then reopen before running audit_scene.py.

Required process environment: VH_SOURCE_FILE, VH_EVIDENCE_DIR.
The evidence directory must be new and comply with the repository's AGENTS.md.
"""
import json, os, pathlib, traceback
import unreal as u

evidence=pathlib.Path(os.environ['VH_EVIDENCE_DIR']).resolve()
evidence.mkdir(parents=True,exist_ok=False)
result={'ok':False}
try:
    source=pathlib.Path(os.environ['VH_SOURCE_FILE']).resolve()
    assert not u.EditorAssetLibrary.does_asset_exist('/Game/Valhalla/Meshes/SM_000'), 'Use a new project copy; never overwrite an authored scene'
    levels=u.get_editor_subsystem(u.LevelEditorSubsystem)
    assert levels.new_level('/Game/Valhalla/Maps/L_Supercomputadora_V05')
    result['build']=json.loads(u.VHAutomaticDoorTools.build_scene(str(source),'/Game/Valhalla'))
    assert result['build']['ok']
    door=next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a,u.VHAutomaticDoor))
    result['collision']=json.loads(u.VHAutomaticDoorTools.set_floor_clearance(door,.2))
    assert result['collision']['ok']
    assert levels.save_current_level()
    result.update(ok=True,reopen_required=True)
except Exception:
    result['error']=traceback.format_exc()
    u.log_error(result['error'])
(evidence/'authoring.json').write_text(json.dumps(result,indent=2),encoding='utf8')
u.SystemLibrary.quit_editor()
