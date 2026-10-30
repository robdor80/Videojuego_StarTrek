import unreal as u,pathlib,json,time,traceback,math
R=pathlib.Path(__file__).resolve().parent;MAP='/Game/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01';assert u.get_editor_subsystem(u.LevelEditorSubsystem).load_level(MAP)
S={'phase':'start','wall_start':time.monotonic(),'checks':[],'samples':[],'ok':False,'release':{}}
def write():
 (R/'Data/limited_runtime_check.json').write_text(json.dumps({k:v for k,v in S.items() if k not in ['world','pawn','seat','blocker','controller','door']},indent=2),encoding='utf-8')
def check(name,passed,**kw):S['checks'].append(dict(name=name,passed=bool(passed),**kw));write()
def tap(key):
 u.STPlayableTest.send_player_key(S['pawn'],key,True);S['release'][key]=u.GameplayStatics.get_time_seconds(S['world'])+.15
def phase(name):S['phase']=name;S['stage']=u.GameplayStatics.get_time_seconds(S['world']);write()
def state():
 p=S['pawn'];return {'phase':str(p.seat_phase),'runtime':p.runtime_state(),'position':list(p.get_actor_location().to_tuple()),'bones':{n:list(p.mesh.get_socket_location(n).to_tuple()) for n in ['pelvis','thigh_l','calf_l','foot_l','ball_l','thigh_r','calf_r','foot_r','ball_r','spine_05','head','hand_l','hand_r']},'mesh_origin':list(p.mesh.get_world_location().to_tuple())}
def finish(error=None):
 if error:S['error']=error
 S['ok']=not S.get('error') and all(c['passed'] for c in S['checks']);S['phase']='end';S['ended']=time.monotonic();write();u.EditorLevelLibrary.editor_end_play()
def tick(dt):
 try:
  if S['phase']=='end':
   if time.monotonic()-S['ended']>1:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_editor()
   return
  if time.monotonic()-S['wall_start']>90:raise RuntimeError('Gameplay rehearsal timeout')
  if S['phase']=='start':u.STPlayableTest.begin_playable_pie();S['phase']='world';return
  if S['phase']=='world':
   worlds=u.EditorLevelLibrary.get_pie_worlds(False)
   if not worlds:return
   w=worlds[0];p=u.GameplayStatics.get_player_character(w,0)
   if not p:return
   assert isinstance(p,u.STPlayableQuinn),str(type(p));seat=u.GameplayStatics.get_all_actors_of_class(w,u.STSeatAnchor)[0];pc=u.GameplayStatics.get_player_controller(w,0)
   S.update(world=w,pawn=p,seat=seat,controller=pc);check('Real PlayerController possesses the actual Quinn Character',p.get_controller()==pc,mesh=p.mesh.get_skeletal_mesh_asset().get_path_name(),viewport=u.STPlayableTest.viewport_info());pc.set_control_rotation(u.Rotator(pitch=0,yaw=-90,roll=0));phase('door_setup');return
  now=u.GameplayStatics.get_time_seconds(S['world']);elapsed=now-S['stage'];p=S['pawn'];seat=S['seat']
  for key,at in list(S['release'].items()):
   if now>=at:u.STPlayableTest.send_player_key(p,key,False);del S['release'][key]
  if S['phase']=='door_setup' and elapsed>.4:
   S['original_position']=list(p.get_actor_location().to_tuple());doors=u.GameplayStatics.get_all_actors_of_class(S['world'],u.STAutomaticDoor);S['door']=next(d for d in doors if str(d.door_id)=='DOOR_F07_004')
   p.character_movement.set_movement_mode(u.MovementMode.MOVE_NONE);p.set_actor_location(S['door'].get_actor_transform().transform_location(u.Vector(-180,0,110)),False,True)
   check('D01-D03 retain blocked destinations',all(not d.destination_constructed and not d.request_open(p) for d in doors if d!=S['door']))
   check('D04 accepts the actual Quinn without changing permissions',S['door'].request_open(p));phase('door_open')
  elif S['phase']=='door_open' and elapsed>1:
   check('D04 reaches full open through real Tick',S['door'].open_fraction>.999,fraction=S['door'].open_fraction);p.set_actor_location(u.Vector(*S['original_position']),False,True);p.character_movement.set_movement_mode(u.MovementMode.MOVE_WALKING);S['door'].request_close();phase('door_close')
  elif S['phase']=='door_close' and elapsed>2:
   check('D04 returns closed after Quinn leaves',S['door'].open_fraction<.001,fraction=S['door'].open_fraction);phase('settle')
  elif S['phase']=='settle' and elapsed>.4:
   S['walk_start']=list(p.get_actor_location().to_tuple());u.STPlayableTest.send_player_key(p,'W',True);phase('walking')
  elif S['phase']=='walking' and elapsed>1:
   u.STPlayableTest.send_player_key(p,'W',False);pos=list(p.get_actor_location().to_tuple());check('W drives real walking and floor holds',math.dist(pos,S['walk_start'])>80 and 'WALKING'in str(p.character_movement.movement_mode),start=S['walk_start'],end=pos,anim_class=p.mesh.get_editor_property('anim_class').get_path_name() if p.mesh.get_editor_property('anim_class') else None);phase('arrange_seat')
  elif S['phase']=='arrange_seat' and elapsed>.4:
   # Scenario arrangement only. This teleport is explicitly not claimed as
   # gameplay circulation or as part of the seat transition.
   p.set_actor_location(u.Vector(0,320,123),False,True);p.set_actor_rotation(u.Rotator(pitch=0,yaw=-90,roll=0),False);S['identity']=p.get_path_name();phase('prompt')
  elif S['phase']=='prompt' and elapsed>.5:
   check('E prompt available from valid approach',p.find_usable_seat()==seat,message=p.interaction_message,approach_clear=seat.approach_is_clear(p),exit_clear=seat.exit_is_clear(p));tap('E');phase('sitting')
  elif S['phase']=='sitting':
   if elapsed-S.get('last_sample',-1)>.12:S['samples'].append(dict(t=elapsed,**state()));S['last_sample']=elapsed;write()
   if str(p.seat_phase).endswith('Seated: 4>') or 'SEATED' in str(p.seat_phase).upper():
    check('E reaches seated state with same possessed Character','phase=4'in p.runtime_state() and S['identity']==p.get_path_name() and p.get_controller()==S['controller'],**state());phase('seated')
   elif elapsed>12:raise RuntimeError('Seat transition did not reach Seated: '+p.runtime_state())
  elif S['phase']=='seated' and elapsed>.7:
   pos=list(p.get_actor_location().to_tuple());S['seated_position']=pos;u.STPlayableTest.send_player_key(p,'W',True);phase('seated_no_walk')
  elif S['phase']=='seated_no_walk' and elapsed>.6:
   u.STPlayableTest.send_player_key(p,'W',False);check('Seated W cannot walk; capsule collision remains enabled',math.dist(S['seated_position'],list(p.get_actor_location().to_tuple()))<.1 and p.capsule_component.get_collision_enabled()!=u.CollisionEnabled.NO_COLLISION,**state())
   b=u.STAutomaticDoorTestLibrary.spawn_runtime_validation_pawn(S['world'],u.load_class(None,'/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C'),seat.exit.get_world_location());b.character_movement.set_movement_mode(u.MovementMode.MOVE_NONE);S['blocker']=b;phase('block_settle')
  elif S['phase']=='block_settle' and elapsed>.4:
   check('Exit obstruction is physically registered',not seat.exit_is_clear(p));tap('E');phase('blocked_exit')
  elif S['phase']=='blocked_exit' and elapsed>.6:
   check('Physical obstruction prevents unsafe standing','phase=4'in p.runtime_state() and not seat.exit_is_clear(p),message=p.interaction_message);S['blocker'].destroy_actor();phase('unblock')
  elif S['phase']=='unblock' and elapsed>.4:tap('E');S['last_sample']=-1;phase('standing')
  elif S['phase']=='standing':
   if elapsed-S.get('last_sample',-1)>.12:S['samples'].append(dict(t=elapsed,**state()));S['last_sample']=elapsed;write()
   if p.completed_sit_cycles>=1:
    check('E stands, restores full capsule, locomotion and ownership',p.capsule_component.get_scaled_capsule_radius()==35 and p.capsule_component.get_scaled_capsule_half_height()==90 and p.get_controller()==S['controller'] and 'WALKING'in str(p.character_movement.movement_mode),**state());S['walk_start']=list(p.get_actor_location().to_tuple());S['controller'].set_control_rotation(u.Rotator(pitch=0,yaw=90,roll=0));u.STPlayableTest.send_player_key(p,'W',True);phase('walk_recovered')
   elif elapsed>8:raise RuntimeError('Stand did not complete: '+p.runtime_state())
  elif S['phase']=='walk_recovered' and elapsed>1:
   u.STPlayableTest.send_player_key(p,'W',False);check('W movement works after stand',math.dist(S['walk_start'],list(p.get_actor_location().to_tuple()))>80,**state());finish()
 except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick)






