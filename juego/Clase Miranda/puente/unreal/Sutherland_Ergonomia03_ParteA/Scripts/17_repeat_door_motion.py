from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'Scripts/16_validate_doors.py').read_text(encoding='utf-8-sig').split('\ndef tick(dt):')[0]
source=source.replace('doors_20261028_validation.json','doors_20261028_repeat_validation.json').replace("len(S['cycles'])==3","S.get('mechanisms_only',False)")
exec(compile(source,str(__file__),'exec'))
def tick(dt):
 try:
  if S['phase']=='done':
   if time.monotonic()-S['ended']>1:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_editor()
   return
  if time.monotonic()-S['started']>70:raise RuntimeError('Bounded repeated mechanism check timeout')
  if S['phase']=='start':u.STPlayableTest.begin_playable_pie();S['phase']='world';save();return
  worlds=u.EditorLevelLibrary.get_pie_worlds(False)
  if not worlds or u.GameplayStatics.get_time_seconds(worlds[0])<.5:return
  w=worlds[0];p=u.GameplayStatics.get_player_character(w,0);V.update(world=w,pawn=p,controller=u.GameplayStatics.get_player_controller(w,0));check('Quinn and controlled test world present',isinstance(p,u.STPlayableQuinn))
  doors=sorted(u.GameplayStatics.get_all_actors_of_class(w,u.STAutomaticDoor),key=lambda a:str(a.door_id))
  for iteration in range(3):
   for door in doors:
    row=mechanical(door);row['round']=iteration+1;S['mechanical'].append(row);save()
  check('All four mechanisms complete three consecutive swept round trips',len(S['mechanical'])==12 and all(r['pass'] for r in S['mechanical']))
  check('Unbuilt destinations never unlocked',all(not d.destination_constructed and d.security_locked and not d.request_open(p) for d in doors if str(d.door_id)!='DOOR_F07_004'))
  S['mechanisms_only']=True;finish()
 except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick);save()
