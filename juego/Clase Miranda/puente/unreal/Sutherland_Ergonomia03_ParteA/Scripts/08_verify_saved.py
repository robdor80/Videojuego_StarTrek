import unreal as u,json,pathlib,runpy,traceback,math
R=pathlib.Path(__file__).resolve().parents[1];D=R/'Data';out={'ok':False,'geometry':[],'door_collision_bounds':[]}
try:
 assert json.loads((D/'integration.json').read_text())['ok']
 lib=runpy.run_path(str(R/'Scripts/05_connections.py'));after=lib['snapshot']();out['connections']=after;assert after['ok']
 before=json.loads((D/'connections_before.json').read_text());assert before['chairs']==after['chairs'],'Six chair connection state changed after save';assert before['visual_parents']==after['visual_parents'];assert before['quinn']==after['quinn'];assert before['game_mode']==after['game_mode'];assert before['seats'][0]['animations']==after['seats'][0]['animations'];assert before['seats'][0]['collision_actors']==after['seats'][0]['collision_actors']
 A=u.get_editor_subsystem(u.EditorActorSubsystem);actors={a.get_actor_label():a for a in A.get_all_level_actors()};plan=json.loads((D/'export_meshes.json').read_text());baseline={a['label']:a for a in json.loads((D/'ue_before.json').read_text())['actors']}
 def vertices(c):
  pts=[]
  for i in range(c.static_mesh.get_num_sections(0)):
   vv,_,_,_,_=u.ProceduralMeshLibrary.get_section_from_static_mesh(c.static_mesh,0,i);pts.extend([list(c.get_world_transform().transform_location(v).to_tuple()) for v in vv])
  return pts
 def error(expected,actual):
  tolerance=.005
  def one(a,b):
   bins={}
   for p in b:bins.setdefault(tuple(math.floor(x/tolerance) for x in p),[]).append(p)
   worst=0
   for p in a:
    k=tuple(math.floor(x/tolerance) for x in p);near=[q for x in [-1,0,1] for y in [-1,0,1] for z in [-1,0,1] for q in bins.get((k[0]+x,k[1]+y,k[2]+z),[])];worst=max(worst,min((math.dist(p,q) for q in near),default=1e9))
   return worst
  assert expected and actual;v=max(one(expected,actual),one(actual,expected));assert v<tolerance,('Saved geometry mismatch',v);return v
 for row in plan['visual']:
  a=actors['VIS_'+row['actor_source']];c=a.static_mesh_component;out['geometry'].append({'actor':a.get_actor_label(),'mesh':c.static_mesh.get_path_name(),'error_cm':error(row['expected_world_cm'],vertices(c))})
 for row in plan['doors']:
  a=actors[row['actor']];c=a.left_leaf if row['component']=='LeftLeaf' else a.right_leaf;out['geometry'].append({'actor':row['actor'],'component':row['component'],'error_cm':error(row['expected_world_cm'],vertices(c))})
  dm=u.DynamicMesh();u.GeometryScript_SceneUtils.copy_collision_meshes_from_object(c,dm,True);vv=u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm,False)[1]);zs=[v.z for v in vv];expected=row['expected_world_cm'];maxz=max(p[2] for p in expected);minz=min(p[2] for p in expected)
  assert abs(max(zs)-maxz)<.05 and abs(min(zs)-minz)<.05,('Stale door collision height',row['actor'],row['component'],min(zs),max(zs),minz,maxz)
  out['door_collision_bounds'].append({'actor':row['actor'],'component':row['component'],'collision_z_cm':[min(zs),max(zs)],'render_z_cm':[minz,maxz]})
 doors=[a for a in actors.values() if isinstance(a,u.STAutomaticDoor)]
 for a in doors:
  b=baseline[a.get_actor_label()];assert list(a.get_actor_location().to_tuple())==b['location'];assert list(a.get_actor_rotation().to_tuple())==b['rotation'];assert a.travel_distance==b['door']['travel_distance'];assert a.destination_constructed==b['door']['destination_constructed'];assert a.security_locked==b['door']['security_locked'];assert a.external_access_allowed==b['door']['external_access_allowed']
 out['door_policy_preserved']=len(doors)==4;assert out['door_policy_preserved']
 affected={r['actor'] for r in plan['collisions']};bodies={r['actor']:r for r in before['collision_inventory']};out['untouched_collision_actors']=[]
 for row in after['collision_inventory']:
  if row['actor'] not in affected:
   assert row==bodies[row['actor']],('Unrelated collision changed',row['actor']);out['untouched_collision_actors'].append(row['actor'])
 if (D/'primitive_collision_inventory.json').exists():
  guards=json.loads((D/'primitive_collision_inventory.json').read_text());assert guards['ok'];out['guards_reopened']=[]
  for g in guards['guard_changes']:
   guard=actors[g['actor']];box=guard.get_components_by_class(u.BoxComponent)[0];assert list(box.get_unscaled_box_extent().to_tuple())==g['after']['extent'];assert math.dist(list(box.get_world_location().to_tuple()),g['after']['location'])<.001;out['guards_reopened'].append(g['actor'])
 out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(D/'saved_verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('SAVED_VERIFICATION',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
