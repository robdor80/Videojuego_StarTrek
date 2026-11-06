"""Read-only saved-scene audit. Required: VH_SOURCE_FILE, VH_EVIDENCE_DIR."""
import json, os, pathlib, traceback
import unreal as u

evidence=pathlib.Path(os.environ['VH_EVIDENCE_DIR']).resolve()
evidence.mkdir(parents=True,exist_ok=False)
result={'ok':False}
try:
    assert u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/Valhalla/Maps/L_Supercomputadora_V05')
    door=next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a,u.VHAutomaticDoor))
    result['import']=json.loads(u.VHAutomaticDoorTools.audit_imported_scene(str(pathlib.Path(os.environ['VH_SOURCE_FILE']).resolve()),'/Game/Valhalla'))
    result['functional']=json.loads(u.VHAutomaticDoorTools.run_checks(door))
    result['ok']=result['import']['ok'] and result['functional']['all_pass']
except Exception:
    result['error']=traceback.format_exc()
    u.log_error(result['error'])
(evidence/'audit.json').write_text(json.dumps(result,indent=2),encoding='utf8')
u.SystemLibrary.quit_editor()
