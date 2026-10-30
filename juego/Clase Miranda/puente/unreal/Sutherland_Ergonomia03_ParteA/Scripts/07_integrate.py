import unreal as u,pathlib,json,traceback,shutil,re,runpy,math,faulthandler
R=pathlib.Path(__file__).resolve().parents[1];D=R/'Data';P=R/'Unreal'
assert pathlib.Path(u.Paths.project_dir()).resolve()==P
E=u.EditorAssetLibrary;A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem);T=u.AssetToolsHelpers.get_asset_tools()
MAP='/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01';DEST='/Game/F07COLL01/Ergonomia03'
out={'ok':False,'visual':[],'collisions':[],'doors':[],'captain_marker_changes':[]}
def norm(s):return re.sub('[^a-zA-Z0-9_]+','_',s).strip('_').lower()
def import_mesh(row,folder,name,collision):
 task=u.AssetImportTask();task.filename=row['file'];task.destination_path=folder;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=True
 opt=u.FbxImportUI();opt.automated_import_should_detect_type=False;opt.import_mesh=True;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.import_materials=False;opt.import_textures=False
 md=opt.static_mesh_import_data;md.combine_meshes=True;md.auto_generate_collision=False;md.one_convex_hull_per_ucx=True;md.generate_lightmap_u_vs=False;md.convert_scene=True;md.convert_scene_unit=True;md.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS;task.options=opt
 T.import_asset_tasks([task]);mesh=E.load_asset(folder+'/'+name);assert mesh,('Import failed',folder,name)
 return mesh
def points(c):
 m=c.static_mesh;wt=c.get_world_transform();p=[]
 for i in range(m.get_num_sections(0)):
  vv,_,_,_,_=u.ProceduralMeshLibrary.get_section_from_static_mesh(m,0,i);p.extend([list(wt.transform_location(v).to_tuple()) for v in vv])
 return p
def compare(expected,actual,tol=.005):
 def bucket(a):return tuple(math.floor(x/tol) for x in a)
 def distance(a,b):return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
 def direction(a,b):
  bins={}
  for p in b:bins.setdefault(bucket(p),[]).append(p)
  worst=0
  for p in a:
   k=bucket(p);near=[q for x in [-1,0,1] for y in [-1,0,1] for z in [-1,0,1] for q in bins.get((k[0]+x,k[1]+y,k[2]+z),[])];v=min((distance(p,q) for q in near),default=1e9);worst=max(worst,v)
  return worst
 assert expected and actual,'No geometry to compare'
 err=max(direction(expected,actual),direction(actual,expected));assert err<tol,('Geometry mismatch cm',err)
 return err
def focused_chair_check():
 result={'all_pass':False,'chairs':[],'method':'Six retained native Toggle/AdvanceChair round trips with real sweeps; no global FinishAllCompilation wait.'}
 for chair in sorted([a for a in A.get_all_level_actors() if isinstance(a,u.STSlidingChair)],key=lambda a:a.chair_id):
  start=chair.moving_rig.get_world_location();fixed=chair.fixed_base.get_world_location();row={'id':chair.chair_id,'components':len(chair.moving_parts)}
  row['toggle_extend_accepted']=chair.toggle()
  for i in range(122):chair.advance_chair(chair.movement_duration/120.)
  row['extended_fraction']=chair.fraction;row['travel_cm']=(chair.moving_rig.get_world_location()-start).length();row['obstruction_forward']=chair.last_obstruction
  if chair.fraction<.9999 or abs(row['travel_cm']-chair.stroke_cm)>.001:
   row['pass']=False;result['chairs'].append(row);chair.reset_retracted();return result
  row['toggle_retract_accepted']=chair.toggle()
  for i in range(122):chair.advance_chair(chair.movement_duration/120.)
  row['return_error_cm']=(chair.moving_rig.get_world_location()-start).length();row['fixed_base_error_cm']=(chair.fixed_base.get_world_location()-fixed).length();row['obstruction_return']=chair.last_obstruction
  row['pass']=row['toggle_extend_accepted'] and row['toggle_retract_accepted'] and row['components']==15 and chair.fraction<.0001 and row['return_error_cm']<.001 and row['fixed_base_error_cm']<.001
  result['chairs'].append(row);chair.reset_retracted()
  if not row['pass']:return result
 result['all_pass']=len(result['chairs'])==6 and all(x['pass'] for x in result['chairs']);return result
try:
 if (D/'integration.json').exists():assert not json.loads((D/'integration.json').read_text()).get('ok'),'Already integrated; verify only'
 plan=json.loads((D/'export_meshes.json').read_text());proxy=json.loads((D/'collision_proxy_update.json').read_text());assert plan['ok'] and proxy['ok']
 protected=json.loads((D/'connections_before.json').read_text());assert protected['ok'];assert L.load_level(MAP)
 backup=R/'Backups/BeforeIntegration';backup.mkdir(exist_ok=True);source=P/'Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap'
 if not (backup/source.name).exists():shutil.copy2(source,backup/source.name)
 actors={a.get_actor_label():a for a in A.get_all_level_actors()};world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();u.SystemLibrary.execute_console_command(world,'Interchange.FeatureFlags.Import.FBX 0')
 mats={norm(x['name']):E.load_asset('/Game/SutherlandPlayable01/Materials/'+x['asset']) for x in json.loads((D/'reference_visual_export.json').read_text())['materials']}
 for row in plan['visual']:
  actor=actors['VIS_'+row['actor_source']];c=actor.static_mesh_component;before=c.static_mesh.get_path_name();mesh=import_mesh(row,DEST+'/Visual',before.rsplit('.',1)[-1],False)
  c.set_static_mesh(mesh)
  for i,slot in enumerate(mesh.get_editor_property('static_materials')):
   key=norm(str(slot.get_editor_property('imported_material_slot_name')));assert key in mats and mats[key],('Unresolved original PBR',row['actor_source'],key);mesh.set_material(i,mats[key]);c.set_material(i,mats[key])
  # Keep the existing custom collision responses on the visual component.
  err=compare(row['expected_world_cm'],points(c));E.save_loaded_asset(mesh);out['visual'].append({'actor':actor.get_actor_label(),'before':before,'after':mesh.get_path_name(),'max_vertex_error_cm':err})
  print('UPDATED_VISUAL',len(out['visual']),flush=True)
 expected_shapes={x['actor']:x['reused_shapes'] for x in proxy['collision_groups']}
 for row in plan['collisions']:
  actor=actors[row['actor']];c=actor.static_mesh_component;oldmesh=c.static_mesh;profile=c.get_collision_profile_name();enabled=c.get_collision_enabled();oldflag=oldmesh.get_editor_property('body_setup').get_editor_property('collision_trace_flag')
  mesh=import_mesh(row,DEST+'/Collision','ERG_'+row['actor'],True);mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',oldflag);c.set_static_mesh(mesh);c.set_collision_profile_name(profile);c.set_collision_enabled(enabled)
  desc=json.loads(u.STCollisionReview.describe_actor(actor));body=desc['components'][0];count=body['boxes']+body['convexes']+body['spheres']+body['capsules'];assert count==expected_shapes[row['actor']],('Hull loss',row['actor'],count,expected_shapes[row['actor']])
  E.save_loaded_asset(mesh);out['collisions'].append({'actor':row['actor'],'before':oldmesh.get_path_name(),'after':mesh.get_path_name(),'retained_shape_count':count,'body':desc})
 for row in plan['doors']:
  actor=actors[row['actor']];c=actor.left_leaf if row['component']=='LeftLeaf' else actor.right_leaf;mesh=import_mesh(row,DEST+'/Leaves',row['asset_name'],True);oldflag=c.static_mesh.get_editor_property('body_setup').get_editor_property('collision_trace_flag');mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',oldflag);c.set_static_mesh(mesh)
  for i in range(mesh.get_num_sections(0)):
   mat=E.load_asset(row['materials'][0]);assert mat;mesh.set_material(i,mat);c.set_material(i,mat)
  err=compare(row['expected_world_cm'],points(c));E.save_loaded_asset(mesh);out['doors'].append({'actor':row['actor'],'component':row['component'],'before':row['old_asset'],'after':mesh.get_path_name(),'max_vertex_error_cm':err})
 for actor in [a for a in actors.values() if isinstance(a,u.STAutomaticDoor)]:
  floor=60. if str(actor.door_id) in ['DOOR_F07_001','DOOR_F07_003'] else 0.
  top=floor+(300.135 if str(actor.door_id)=='DOOR_F07_004' else 300.)
  actor.opening_height=top-actor.get_actor_location().z;actor.reset_closed()
  desc=json.loads(u.STCollisionReview.describe_actor(actor));assert all(c['convexes']==1 and c['boxes']==0 for c in desc['components']),('Door hull loss',actor.get_actor_label())
 # Adapt only the captain's seated pose markers to the accepted -14.8cm chair.
 # Entry/exit points remain at the original walkable floor.
 seat=next(a for a in actors.values() if isinstance(a,u.STSeatAnchor))
 for key in ['seated_capsule','pelvis','back','left_foot','right_foot']:
  c=seat.get_editor_property(key);before=list(c.get_world_location().to_tuple());loc=c.get_editor_property('relative_location');loc.z-=14.8;c.set_editor_property('relative_location',loc);out['captain_marker_changes'].append({'marker':key,'before':before,'after':list(c.get_world_location().to_tuple())})
 snapshot=runpy.run_path(str(R/'Scripts/05_connections.py'))['snapshot'];after=snapshot(False)
 assert after['ok'];assert protected['chairs']==after['chairs'],'Mandatory six chairs changed';assert protected['visual_parents']==after['visual_parents'],'Chair visuals changed';assert protected['quinn']==after['quinn'];assert protected['game_mode']==after['game_mode'];assert protected['seats'][0]['animations']==after['seats'][0]['animations'];assert protected['seats'][0]['collision_actors']==after['seats'][0]['collision_actors']
 # One focused inherited chair check. On a new conflict, leave the map unsaved
 # and record it; never remove/move a chair to force success.
 (D/'integration_inprogress.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
 print('BEGIN_FOCUSED_CHAIR_CHECK',flush=True)
 trace=(R/'Logs/native_wait_trace.log').open('w');faulthandler.dump_traceback_later(45,file=trace)
 out['chair_checks']=focused_chair_check();faulthandler.cancel_dump_traceback_later();trace.close()
 print('END_FOCUSED_CHAIR_CHECK',out['chair_checks'].get('passed'),out['chair_checks'].get('total'),flush=True)
 assert out['chair_checks'].get('all_pass',False),'Chair conflict: stop without saving level'
 assert L.save_current_level();E.save_directory(DEST,only_if_is_dirty=True,recursive=True)
 out['connections_after']=after;out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(D/'integration.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('INTEGRATION_RESULT',out['ok'],out.get('error'),flush=True);u.SystemLibrary.quit_editor()


