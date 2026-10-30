import unreal as u,pathlib,json,traceback,shutil,runpy
R=pathlib.Path(__file__).resolve().parents[1];D=R/'Data';out={'ok':False,'guard_changes':[]}
try:
 L=u.get_editor_subsystem(u.LevelEditorSubsystem);A=u.get_editor_subsystem(u.EditorActorSubsystem);assert L.load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
 actors=list(A.get_all_level_actors());doors={str(a.door_id):a for a in actors if isinstance(a,u.STAutomaticDoor)}
 def inventory():
  result=[]
  for a in A.get_all_level_actors():
   for c in a.get_components_by_class(u.PrimitiveComponent):
    row={'actor':a.get_actor_label(),'actor_name':a.get_name(),'component':c.get_name(),'class':c.get_class().get_path_name(),'collision':str(c.get_collision_enabled()),'profile':str(c.get_collision_profile_name()),'object_type':str(c.get_collision_object_type()),'Pawn':str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_PAWN)),'Camera':str(c.get_collision_response_to_channel(u.CollisionChannel.ECC_CAMERA)),'location':list(c.get_world_location().to_tuple()),'rotation':list(c.get_world_rotation().to_tuple()),'scale':list(c.get_world_scale().to_tuple())}
    if isinstance(c,u.BoxComponent):row['box_extent']=list(c.get_unscaled_box_extent().to_tuple())
    result.append(row)
  return result
 out['before']=inventory()
 source=R/'Unreal/Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap';backup=R/'Backups/L_Sutherland_Playable01_BeforeGuardAdaptation.umap'
 if not backup.exists():shutil.copy2(source,backup)
 for door_id,door in doors.items():
  if door.destination_constructed:continue
  guard=next(a for a in actors if 'FG_Guard_'+door_id in [str(t) for t in a.tags]);boxes=guard.get_components_by_class(u.BoxComponent);assert len(boxes)==1;box=boxes[0]
  low=-door.get_actor_location().z-10;high=door.opening_height+10;before={'location':list(box.get_world_location().to_tuple()),'extent':list(box.get_unscaled_box_extent().to_tuple())}
  extent=box.get_unscaled_box_extent();extent.z=(high-low)/2;box.set_box_extent(extent,False);box.set_world_location(door.get_actor_transform().transform_location(u.Vector(-100,0,(high+low)/2)),False,False)
  out['guard_changes'].append({'actor':guard.get_actor_label(),'door':door_id,'before':before,'after':{'location':list(box.get_world_location().to_tuple()),'extent':list(box.get_unscaled_box_extent().to_tuple())},'reason':'Keep destination guard, adapt only old height to reduced doorway.'})
 assert len(out['guard_changes'])==3;out['after']=inventory()
 changed={x['actor'] for x in out['guard_changes']};old={(x['actor_name'],x['component']):x for x in out['before']}
 for x in out['after']:
  if x['actor'] not in changed:assert x==old[(x['actor_name'],x['component'])],('Unrelated primitive changed',x['actor'])
 snap=runpy.run_path(str(R/'Scripts/05_connections.py'))['snapshot'](False);before=json.loads((D/'connections_before.json').read_text());assert snap['chairs']==before['chairs'];assert snap['visual_parents']==before['visual_parents'];assert L.save_current_level();out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(D/'primitive_collision_inventory.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('GUARDS_INVENTORY',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
