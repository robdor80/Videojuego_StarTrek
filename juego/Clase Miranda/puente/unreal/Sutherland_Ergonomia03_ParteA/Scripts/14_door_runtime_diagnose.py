import unreal as u,json,pathlib,time,traceback
R=pathlib.Path(__file__).resolve().parents[1];D=R/'Data';S={'ok':False,'phase':'start','started':time.monotonic(),'doors':[]}
assert u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
def save():(D/'doors_20261028_runtime_diagnosis.json').write_text(json.dumps(S,indent=2),encoding='utf-8')
def finish(error=None):
 if error:S['error']=error
 S['phase']='done';S['ended']=time.monotonic();save();u.EditorLevelLibrary.editor_end_play()
def hitrow(h):
 b=h.to_tuple();a=b[9];c=b[10]
 return {'blocking':b[0],'initial_overlap':b[1],'time':b[2],'distance_cm':b[3],'impact':list(b[5].to_tuple()),'normal':list(b[7].to_tuple()),'actor':a.get_actor_label() if a else None,'component':c.get_name() if c else None,'mesh':c.static_mesh.get_path_name() if isinstance(c,u.StaticMeshComponent) and c.static_mesh else None}
def tick(dt):
 try:
  if S['phase']=='done':
   if time.monotonic()-S['ended']>1:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_editor()
   return
  if time.monotonic()-S['started']>70:raise RuntimeError('Door diagnostic bounded timeout')
  if S['phase']=='start':u.STPlayableTest.begin_playable_pie();S['phase']='world';save();return
  worlds=u.EditorLevelLibrary.get_pie_worlds(False)
  if not worlds:return
  w=worlds[0]
  if u.GameplayStatics.get_time_seconds(w)<.5:return
  doors=sorted(u.GameplayStatics.get_all_actors_of_class(w,u.STAutomaticDoor),key=lambda x:str(x.door_id))
  for door in doors:
   door.reset_closed();row={'id':str(door.door_id),'leaves':[]}
   for side,c in [('LeftLeaf',door.left_leaf),('RightLeaf',door.right_leaf)]:
    closed=c.get_editor_property('relative_location');lr={'side':side,'mesh':c.static_mesh.get_path_name(),'samples':[]}
    try:
     for i in range(1,121):
      target=closed+u.Vector(0,(-1 if side=='LeftLeaf' else 1)*door.travel_distance*i/120.,0);h=c.set_relative_location(target,True,False);v=hitrow(h)
      if v['blocking'] or i in [1,30,60,90,120]:lr['samples'].append({'step':i,'target':list(target.to_tuple()),'actual':list(c.get_editor_property('relative_location').to_tuple()),'hit':v})
      if v['blocking']:break
    finally:door.reset_closed()
    row['leaves'].append(lr)
   S['doors'].append(row);save()
  S['ok']=len(S['doors'])==4;finish()
 except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick);save()

