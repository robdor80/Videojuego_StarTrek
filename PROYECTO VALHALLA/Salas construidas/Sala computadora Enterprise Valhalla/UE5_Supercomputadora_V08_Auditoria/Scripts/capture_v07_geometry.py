"""UE editor: export immutable source geometry; refuses an existing output file.

VH_GEOMETRY_FILE: new JSON path; VH_GEOMETRY_MAP: optional source map override.
"""
import os
import unreal as u

try:
    world=u.EditorLoadingAndSavingUtils.load_map(os.environ.get('VH_GEOMETRY_MAP','/Game/ValhallaV07/Maps/L_Supercomputadora_V07'))
    assert world
    u.VH06Tools.finish_compilation()
    assert u.VHAutomaticDoorTools.export_v07_geometry(os.environ['VH_GEOMETRY_FILE'])
finally:
    u.SystemLibrary.quit_editor()
