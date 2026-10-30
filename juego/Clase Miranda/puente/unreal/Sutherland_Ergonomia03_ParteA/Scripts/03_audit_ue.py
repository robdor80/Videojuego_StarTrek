import unreal as u,pathlib,json,traceback
R=pathlib.Path(__file__).resolve().parents[1];assert pathlib.Path(u.Paths.project_dir()).resolve()==R/'Unreal'
A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem)
out={'ok':False}
def prop(o,k):
 try:
  v=o.get_editor_property(k)
  if isinstance(v,(float,int,bool,str)):return v
  if hasattr(v,'to_tuple'):return list(v.to_tuple())
  return str(v)
 except Exception:return None
try:
 assert json.loads((R/'Data/copy_verified.json').read_text())['ok']
 assert L.load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
 out['actors']=[]
 for a in A.get_all_level_actors():
  c,e=a.get_actor_bounds(False);row={'label':a.get_actor_label(),'name':a.get_name(),'class':a.get_class().get_path_name(),'location':list(a.get_actor_location().to_tuple()),'rotation':list(a.get_actor_rotation().to_tuple()),'scale':list(a.get_actor_scale3d().to_tuple()),'tags':[str(t) for t in a.tags],'bounds_center':list(c.to_tuple()),'bounds_extent':list(e.to_tuple()),'parent':a.get_attach_parent_actor().get_actor_label() if a.get_attach_parent_actor() else None,'components':[]}
  for comp in a.get_components_by_class(u.StaticMeshComponent):
   m=comp.static_mesh;c,e,_=u.SystemLibrary.get_component_bounds(comp)
   row['components'].append({'name':comp.get_name(),'mesh':m.get_path_name() if m else None,'visible':comp.is_visible(),'location':list(comp.get_world_location().to_tuple()),'rotation':list(comp.get_world_rotation().to_tuple()),'relative_location':prop(comp,'relative_location'),'relative_scale3d':prop(comp,'relative_scale3d'),'collision':str(comp.get_collision_enabled()),'profile':str(comp.get_collision_profile_name()),'materials':[x.get_path_name() if x else None for x in comp.get_materials()],'bounds_center':list(c.to_tuple()),'bounds_extent':list(e.to_tuple()),'body_trace_flag':prop(m.get_editor_property('body_setup'),'collision_trace_flag') if m and m.get_editor_property('body_setup') else None})
  if isinstance(a,u.STAutomaticDoor):row['door']={k:prop(a,k) for k in ['door_id','left_closed_location','right_closed_location','travel_distance','opening_width','opening_height','movement_duration','close_delay','destination_constructed','security_locked','external_access_allowed','use_passage_intent']}
  if isinstance(a,u.STSeatAnchor):row['seat']={k:prop(a,k) for k in ['interaction_distance','interaction_enabled','sit_animation','stand_animation','chair_collision_actors']}
  out['actors'].append(row)
 out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(R/'Data/ue_before.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('AUDIT',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
