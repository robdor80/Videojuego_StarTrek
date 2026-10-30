"""Controlled scenario arrangement followed by real Quinn movement at each aisle."""
import unreal as u,pathlib,json,time,traceback,math
R=pathlib.Path(__file__).parent;(R/'Capturas').mkdir(exist_ok=True)
S={'ok':False,'phase':'start','checks':[],'stations':[],'started':time.monotonic()};V={}
places=[(1,340,551.422),(2,340,372.934),(3,340,173.943),(4,-340,180.778),(5,-340,359.266),(6,-340,558.256)]
assert u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01')
def save(): (R/'Data/stations_runtime.json').write_text(json.dumps(S,indent=2))
def check(n,p,**kw):S['checks'].append({'name':n,'pass':bool(p),**kw});save()
def phase(n):S['phase']=n;S['stage']=u.GameplayStatics.get_time_seconds(V['world']);save()
def finish(err=None):
    if err:S['error']=err
    if 'pawn' in V:u.STPlayableTest.send_player_key(V['pawn'],'W',False)
    S['ok']=not S.get('error') and len(S['stations'])==6 and all(c['pass'] for c in S['checks']);S['phase']='done';S['ended']=time.monotonic();save();u.EditorLevelLibrary.editor_end_play()
def tick(dt):
    try:
        if S['phase']=='done':
            if time.monotonic()-S['ended']>1:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_editor()
            return
        if time.monotonic()-S['started']>100:raise RuntimeError('Station validation timeout')
        if S['phase']=='start':u.STPlayableTest.begin_playable_pie();S['phase']='world';return
        if S['phase']=='world':
            worlds=u.EditorLevelLibrary.get_pie_worlds(False)
            if not worlds:return
            p=u.GameplayStatics.get_player_character(worlds[0],0)
            if not p:return
            V.update(world=worlds[0],pawn=p,pc=u.GameplayStatics.get_player_controller(worlds[0],0),index=0)
            check('Possessed Quinn in PBR map',isinstance(p,u.STPlayableQuinn) and p.get_controller()==V['pc']);phase('spawn_settle');return
        p=V['pawn'];now=u.GameplayStatics.get_time_seconds(V['world']);elapsed=now-S['stage']
        if S['phase']=='spawn_settle' and elapsed>.5:
            check('Normal Play spawn supported by floor',p.character_movement.movement_mode==u.MovementMode.MOVE_WALKING,position=list(p.get_actor_location().to_tuple()));phase('arrange')
        elif S['phase']=='arrange':
            i,x,y=places[V['index']];p.set_actor_location(u.Vector(x,y+90,92),False,True);p.character_movement.set_movement_mode(u.MovementMode.MOVE_WALKING);V['pc'].set_control_rotation(u.Rotator(pitch=0,yaw=-90,roll=0));phase('settle')
        elif S['phase']=='settle' and elapsed>.35:
            V['start']=list(p.get_actor_location().to_tuple());u.STPlayableTest.send_player_key(p,'W',True);phase('walk')
        elif S['phase']=='walk' and elapsed>1.0:
            u.STPlayableTest.send_player_key(p,'W',False);pos=list(p.get_actor_location().to_tuple());passed=math.dist(V['start'],pos)>140 and p.character_movement.movement_mode==u.MovementMode.MOVE_WALKING and abs(pos[2]-V['start'][2])<3
            check('Walk aisle beside station P%02d'%places[V['index']][0],passed,start=V['start'],end=pos);S['stations'].append({'station':places[V['index']][0],'passed':passed});V['index']+=1;phase('arrange' if V['index']<6 else 'view_east')
        elif S['phase']=='view_east':
            p.set_actor_location(u.Vector(150,360,92),False,True);V['pc'].set_control_rotation(u.Rotator(pitch=-8,yaw=0,roll=0));phase('capture_east')
        elif S['phase']=='capture_east' and elapsed>1:
            u.STPlayableTest.screenshot(str(R/'Capturas/Quinn_TresSillas_Xpositivo.png'));phase('view_west')
        elif S['phase']=='view_west' and elapsed>.4:
            p.set_actor_location(u.Vector(-150,360,92),False,True);V['pc'].set_control_rotation(u.Rotator(pitch=-8,yaw=180,roll=0));phase('capture_west')
        elif S['phase']=='capture_west' and elapsed>1:
            u.STPlayableTest.screenshot(str(R/'Capturas/Quinn_TresSillas_Xnegativo.png'));phase('view_overview')
        elif S['phase']=='view_overview' and elapsed>.4:
            p.set_actor_location(u.Vector(0,650,92),False,True);V['pc'].set_control_rotation(u.Rotator(pitch=-10,yaw=-90,roll=0));phase('capture_overview')
        elif S['phase']=='capture_overview' and elapsed>1:
            u.STPlayableTest.screenshot(str(R/'Capturas/Quinn_Puente_PBR.png'));phase('finish')
        elif S['phase']=='finish' and elapsed>.5:finish()
    except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick);save()
