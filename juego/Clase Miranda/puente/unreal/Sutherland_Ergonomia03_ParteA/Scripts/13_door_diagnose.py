import unreal as u,json,pathlib,traceback
R=pathlib.Path(__file__).resolve().parents[1];D=R/'Data';out={'ok':False,'doors':[]}
assert pathlib.Path(u.Paths.project_dir()).resolve()==R/'Unreal'
try:
 A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem);assert L.load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
 baseline={a['label']:a for a in json.loads((D/'ue_before.json').read_text())['actors']}
 objects=[getattr(u.ObjectTypeQuery,'OBJECT_TYPE_QUERY'+str(i)) for i in range(1,7)]
 for door in sorted([a for a in A.get_all_level_actors() if isinstance(a,u.STAutomaticDoor)],key=lambda a:str(a.door_id)):
  row={'id':str(door.door_id),'label':door.get_actor_label(),'class':door.get_class().get_path_name(),'travel':door.travel_distance,'opening_height':door.opening_height,'destination_constructed':door.destination_constructed,'locked':door.security_locked,'leaves':[]}
  for side,c in [('LeftLeaf',door.left_leaf),('RightLeaf',door.right_leaf)]:
   original=c.static_mesh;leaf={'component':side,'mesh':original.get_path_name(),'location':list(c.get_world_location().to_tuple()),'variants':[]}
   oldpath=next(x['mesh'] for x in baseline[door.get_actor_label()]['components'] if x['name']==side)
   try:
    for name,path in [('integrated',original.get_path_name()),('historical_leaf_memory_only',oldpath)]:
     c.set_static_mesh(u.EditorAssetLibrary.load_asset(path));variant={'name':name,'mesh':path,'overlaps':[]}
     for fraction in [0.,.001,.01,.5,1.]:
      t=c.get_world_transform();delta=door.get_actor_transform().transform_direction(u.Vector(0,(-1 if side=='LeftLeaf' else 1)*door.travel_distance*fraction,0));t.translation=c.get_world_location()+delta
      result=u.SystemLibrary.component_overlap_components(c,t,objects,None,[door]);components=result[1] if isinstance(result,tuple) else result
      hits=[]
      for hit in components or []:
       if hit.get_collision_response_to_channel(u.CollisionChannel.ECC_WORLD_DYNAMIC)!=u.CollisionResponse.ECR_BLOCK:continue
       owner=hit.get_owner();hits.append({'actor':owner.get_actor_label(),'component':hit.get_name(),'class':hit.get_class().get_path_name(),'profile':str(hit.get_collision_profile_name()),'mesh':hit.static_mesh.get_path_name() if isinstance(hit,u.StaticMeshComponent) and hit.static_mesh else None})
      variant['overlaps'].append({'fraction':fraction,'blocking_candidates':hits})
     leaf['variants'].append(variant)
   finally:c.set_static_mesh(original)
   row['leaves'].append(leaf)
  out['doors'].append(row)
 out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(D/'doors_20261028_diagnosis.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('DOOR_DIAGNOSIS',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()

