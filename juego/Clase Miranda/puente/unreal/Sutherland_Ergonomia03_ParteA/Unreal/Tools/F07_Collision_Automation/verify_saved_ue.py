"""Reload and test saved physics without rebuilding or saving any asset."""
import pathlib,unreal
VERIFY_ONLY=True
script=pathlib.Path(unreal.Paths.project_dir())/'Tools/F07_Collision_Automation/apply_plan_ue.py'
exec(compile(script.read_text(encoding='utf-8'),str(script),'exec'),globals())
