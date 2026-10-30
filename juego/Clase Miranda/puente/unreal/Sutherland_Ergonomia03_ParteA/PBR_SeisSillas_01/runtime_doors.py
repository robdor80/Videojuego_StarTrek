import unreal as u,pathlib,json,time,traceback,math
R=pathlib.Path(__file__).resolve().parent;D=R/'Data';S={'ok':False,'phase':'start','started':time.monotonic(),'mechanical':[],'cycles':[],'checks':[]};V={}
assert u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01')
def save():(D/'doors_pbr_validation.json').write_text(json.dumps(S,indent=2),encoding='utf-8')
def check(name,passed,**data):S['checks'].append({'name':name,'pass':bool(passed),**data});save();assert passed,name
def phase(name):S['phase']=name;S['stage']=u.GameplayStatics.get_time_seconds(V['world']);save()
def input_w(on):u.STPlayableTest.send_player_key(V['pawn'],'W',on)
def face(reverse=False):V['controller'].set_control_rotation(u.Rotator(pitch=0,yaw=V['door'].get_actor_rotation().yaw+(180 if reverse else 0),roll=0))
def local():return V['door'].get_actor_transform().inverse_transform_location(V['pawn'].get_actor_location())
def collision_center(c):
 dm=u.DynamicMesh();u.GeometryScript_SceneUtils.copy_collision_meshes_from_object(c,dm,True);p=u.GeometryScript_List.convert_vector_list_to_array(u.GeometryScript_MeshQueries.get_all_vertex_positions(dm,False)[1]);return sum(p,u.Vector())/len(p)
def hit_info(h):
 b=h.to_tuple();return {'blocking':b[0],'initial_overlap':b[1],'time':b[2],'actor':b[9].get_actor_label() if b[9] else None,'component':b[10].get_name() if b[10] else None}
def mechanical(door):
 row={'id':str(door.door_id),'leaves':[]};door.reset_closed()
 for side,c in [('LeftLeaf',door.left_leaf),('RightLeaf',door.right_leaf)]:
  b=c.get_editor_property('relative_location');closed=u.Vector(b.x,b.y,b.z);origin=c.get_world_location();cc=collision_center(c);sign=-1 if side=='LeftLeaf' else 1;lr={'side':side,'hits':[]}
  try:
   for passnum in range(2):
    for i in range(1,121):
     fraction=i/120. if passnum==0 else 1-i/120.;target=closed+u.Vector(0,sign*door.travel_distance*fraction,0);h=c.set_relative_location(target,True,False);hi=hit_info(h)
     if hi['blocking']:lr['hits'].append({'pass':passnum,'fraction':fraction,**hi});break
    if passnum==0:
     expected=door.get_actor_transform().transform_direction(u.Vector(0,sign*door.travel_distance,0));actual=c.get_world_location()-origin;delta=collision_center(c)-cc;lr['travel_error_cm']=(actual-expected).length();lr['collision_follow_error_cm']=(delta-expected).length()
    if lr['hits']:break
   lr['closed_error_cm']=(c.get_editor_property('relative_location')-closed).length();lr['pass']=not lr['hits'] and max(lr.get('travel_error_cm',1e9),lr.get('collision_follow_error_cm',1e9),lr['closed_error_cm'])<.001
  finally:door.reset_closed()
  row['leaves'].append(lr)
 row['pass']=all(x['pass'] for x in row['leaves']);return row
def barrier(opened):
 door=V['door'];t=door.get_actor_transform();rows=[]
 for y in [-25,0,25]:
  p=json.loads(u.STCollisionReview.probe(V['world'],t.transform_location(u.Vector(-120,y,110)),t.transform_location(u.Vector(120,y,110)),35,90,door,False));rows.append({'lane_y':y,'probe':p})
 check('Leaf collision passage '+('open' if opened else 'closed'),all(x['probe']['hit']!=opened for x in rows),probes=rows)
def finish(error=None):
 try:
  if 'pawn' in V:input_w(False)
 except:pass
 if error:S['error']=error
 S['ok']=not S.get('error') and len(S['cycles'])==3 and all(c['pass'] for c in S['checks']) and all(x['pass'] for x in S['mechanical']);S['phase']='done';S['ended']=time.monotonic();save();u.EditorLevelLibrary.editor_end_play()
def tick(dt):
 try:
  if S['phase']=='done':
   if time.monotonic()-S['ended']>1:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_editor()
   return
  if time.monotonic()-S['started']>140:raise RuntimeError('Bounded doors-only validation timeout')
  if S['phase']=='start':u.STPlayableTest.begin_playable_pie();S['phase']='world';save();return
  if S['phase']=='world':
   worlds=u.EditorLevelLibrary.get_pie_worlds(False)
   if not worlds:return
   w=worlds[0];p=u.GameplayStatics.get_player_character(w,0)
   if not p or u.GameplayStatics.get_time_seconds(w)<.5:return
   V.update(world=w,pawn=p,controller=u.GameplayStatics.get_player_controller(w,0));check('Actual possessed Quinn',isinstance(p,u.STPlayableQuinn) and p.get_controller()==V['controller'])
   doors=sorted(u.GameplayStatics.get_all_actors_of_class(w,u.STAutomaticDoor),key=lambda a:str(a.door_id));V['door']=next(a for a in doors if str(a.door_id)=='DOOR_F07_004')
   for door in doors:S['mechanical'].append(mechanical(door));save()
   check('Eight leaves sweep full opposite travel and return',len(doors)==4 and all(x['pass'] for x in S['mechanical']))
   check('D01-D03 retain destination safety',all(not d.destination_constructed and d.security_locked and not d.request_open(p) for d in doors if d!=V['door']))
   barrier(False);p.set_actor_location(V['door'].get_actor_transform().transform_location(u.Vector(-300,0,92)),False,True);V['cycle']=1;phase('settle');return
  w=V['world'];p=V['pawn'];door=V['door'];now=u.GameplayStatics.get_time_seconds(w);elapsed=now-S['stage']
  if elapsed>15:raise RuntimeError('Door validation phase timeout: '+S['phase']+' fraction='+str(door.open_fraction)+' state='+str(door.door_state))
  if S['phase']=='settle' and elapsed>.5:face();input_w(True);phase('approach')
  elif S['phase']=='approach':
   if local().x>-110:input_w(False);phase('opening')
  elif S['phase']=='opening':
   if door.open_fraction>.999:
    check('Automatic Quinn approach opens D04 cycle '+str(V['cycle']),True,fraction=door.open_fraction,player_local=list(local().to_tuple()));barrier(True)
    if V['cycle']==1:face();input_w(True);phase('enter_cabin')
    else:face(True);input_w(True);phase('retreat')
  elif S['phase']=='enter_cabin' and local().x>80:
   input_w(False);check('Quinn walks into existing cabin',True,position=list(p.get_actor_location().to_tuple()),movement=str(p.character_movement.movement_mode));phase('cabin')
  elif S['phase']=='cabin' and elapsed>.4:
   check('Cabin floor supports Quinn',u.MovementMode.MOVE_WALKING==p.character_movement.movement_mode and abs(p.character_movement.velocity.z)<1,local=list(local().to_tuple()));face(True);input_w(True);phase('retreat')
  elif S['phase']=='retreat' and local().x<-300:input_w(False);phase('closing')
  elif S['phase']=='closing' and door.open_fraction<.001:
   check('Automatic D04 closure cycle '+str(V['cycle']),True,fraction=door.open_fraction);barrier(False);S['cycles'].append({'cycle':V['cycle'],'automatic_open':True,'automatic_close':True,'cabina_access':V['cycle']==1});save()
   if V['cycle']==3:finish()
   else:V['cycle']+=1;face();input_w(True);phase('approach')
 except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick);save()
