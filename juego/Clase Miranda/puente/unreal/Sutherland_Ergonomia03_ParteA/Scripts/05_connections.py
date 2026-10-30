import unreal as u,json,pathlib,traceback
R=pathlib.Path(__file__).resolve().parents[1]
assert pathlib.Path(u.Paths.project_dir()).resolve()==R/'Unreal'
A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem)
def value(v):
 if v is None or isinstance(v,(float,int,bool,str)):return v
 if hasattr(v,'get_path_name'):return v.get_path_name()
 if hasattr(v,'to_tuple'):return list(v.to_tuple())
 try:return [value(x) for x in v]
 except:return str(v)
def tr(c):return {'location':value(c.get_world_location()),'rotation':value(c.get_world_rotation()),'scale':value(c.get_world_scale())}
def snapshot(load=True):
 out={'ok':False,'chairs':[],'seats':[],'doors':[],'collision_inventory':[],'visual_parents':[]}
 if load:assert L.load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
 actors=list(A.get_all_level_actors())
 for a in actors:
  if isinstance(a,u.STSlidingChair):
   row={'name':a.get_name(),'label':a.get_actor_label(),'class':a.get_class().get_path_name(),'location':value(a.get_actor_location()),'rotation':value(a.get_actor_rotation()),'scale':value(a.get_actor_scale3d()),'properties':{k:value(a.get_editor_property(k)) for k in ['chair_id','stroke_cm','movement_duration','retracted_local_position','local_travel_direction','chair_state','fraction']},'fixed_base':value(a.fixed_base),'moving_rig':value(a.moving_rig),'moving_parts':[]}
   for c in a.moving_parts:row['moving_parts'].append({'name':c.get_name(),'mesh':value(c.static_mesh),'transform':tr(c),'materials':value(c.get_materials()),'collision':str(c.get_collision_enabled()),'profile':str(c.get_collision_profile_name())})
   out['chairs'].append(row)
  if isinstance(a,u.STSeatAnchor):out['seats'].append({'name':a.get_name(),'location':value(a.get_actor_location()),'animations':{k:value(a.get_editor_property(k)) for k in ['sit_animation','seated_animation','stand_animation']},'collision_actors':value(a.chair_collision_actors),'markers':{k:tr(a.get_editor_property(k)) for k in ['approach','seated_capsule','pelvis','back','left_foot','right_foot','exit']}})
  if isinstance(a,u.STAutomaticDoor):out['doors'].append({'label':a.get_actor_label(),'body':json.loads(u.STCollisionReview.describe_actor(a))})
  if a.get_actor_label().startswith('SM_COLL_'):out['collision_inventory'].append(json.loads(u.STCollisionReview.describe_actor(a)))
  parent=a.get_attach_parent_actor()
  if parent and isinstance(parent,u.STSlidingChair):out['visual_parents'].append({'name':a.get_name(),'label':a.get_actor_label(),'parent':parent.get_name(),'location':value(a.get_actor_location()),'rotation':value(a.get_actor_rotation()),'scale':value(a.get_actor_scale3d()),'meshes':[value(c.static_mesh) for c in a.get_components_by_class(u.StaticMeshComponent)]})
 out['game_mode']=value(u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world().get_world_settings().default_game_mode)
 default=u.get_default_object(u.STPlayableQuinn)
 out['quinn']={'class':default.get_class().get_path_name(),'skeletal_mesh':value(default.mesh.skeletal_mesh),'mesh_scale':value(default.mesh.get_editor_property('relative_scale3d')),'mesh_location':value(default.mesh.get_editor_property('relative_location')),'anim_class':value(default.mesh.anim_class),'capsule_half_height':default.capsule_component.get_unscaled_capsule_half_height(),'capsule_radius':default.capsule_component.get_unscaled_capsule_radius()}
 out['ok']=len(out['chairs'])==6 and len(out['seats'])==1 and all(len(c['moving_parts'])==15 for c in out['chairs'])
 return out
if __name__=='__main__':
 try:out=snapshot()
 except Exception:out={'ok':False,'error':traceback.format_exc()}
 (R/'Data/connections_before.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 print('CONNECTIONS',out.get('ok'),out.get('error'));u.SystemLibrary.quit_editor()

