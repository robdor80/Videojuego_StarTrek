import unreal as u,json,pathlib,traceback,ast,runpy,hashlib
R=pathlib.Path(__file__).resolve().parents[1];D=R/'Data';P=R/'Unreal';out={'ok':False,'leaves':[]}
# Reuse the exact render/UV/material digest used before changing collision.
module=ast.parse((R/'Scripts/15_fix_door_collisions.py').read_text(encoding='utf-8-sig'));selected=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name in ['render_digest','positions']];exec(compile(ast.Module(body=selected,type_ignores=[]),str(__file__),'exec'))
try:
 fix=json.loads((D/'doors_20261028_fix.json').read_text());assert fix['ok'];A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem);assert L.load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
 doors={str(a.door_id):a for a in A.get_all_level_actors() if isinstance(a,u.STAutomaticDoor)}
 for row in fix['modified']:
  door=doors[row['door']];c=door.left_leaf if row['side']=='LeftLeaf' else door.right_leaf;m=c.static_mesh;assert m.get_path_name()==row['asset'];assert render_digest(m)==row['render_material_uv_digest']
  dm=u.DynamicMesh();u.GeometryScript_SceneUtils.copy_collision_meshes_from_object(c,dm,True);vs=positions(dm);lo=min(v.z for v in vs);hi=max(v.z for v in vs)
  assert abs(lo-row['collision_lower_world_z_cm'])<.001,(row['door'],row['side'],lo)
  body=next(x for x in json.loads(u.STCollisionReview.describe_actor(door))['components'] if x['component']==row['side']);assert body['convexes']==1 and body['boxes']==0 and body['collision_enabled_enum']==3
  out['leaves'].append({'door':row['door'],'side':row['side'],'render_material_uv_unchanged':True,'collision_bounds_z_cm':[lo,hi],'body':body})
 snap=runpy.run_path(str(R/'Scripts/05_connections.py'))['snapshot'](False);protected=json.loads((D/'connections_before.json').read_text());assert snap['chairs']==protected['chairs'];assert snap['visual_parents']==protected['visual_parents'];assert snap['quinn']==protected['quinn'];assert snap['game_mode']==protected['game_mode']
 out['six_chairs_quinn_references_unchanged']=True;out['map_unchanged']=hashlib.sha256((P/'Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap').read_bytes()).hexdigest()==fix['map_before_sha256'];assert out['map_unchanged'];out['ok']=len(out['leaves'])==8
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(D/'doors_20261028_saved_verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('DOORS_REOPEN_VERIFY',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
