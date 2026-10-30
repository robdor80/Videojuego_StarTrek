import unreal as u,json,pathlib,traceback
OUT=pathlib.Path(u.Paths.project_dir())/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
data={}
def get(fn):
    try:return fn()
    except Exception as e:return {'error':str(e)}
u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/maps/L_F07_Sutherland_Test')
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
gm=u.get_default_object(world.get_world_settings().get_editor_property('default_game_mode'))
pc=gm.get_editor_property('default_pawn_class');pawn=u.get_default_object(pc)
data['pawn_class']=pc.get_path_name()
cap=pawn.get_component_by_class(u.CapsuleComponent)
data['capsule']={'radius':cap.get_scaled_capsule_radius(),'half_height':cap.get_scaled_capsule_half_height()}
move=pawn.get_component_by_class(u.CharacterMovementComponent)
data['movement']={n:get(lambda n=n:str(move.get_editor_property(n))) for n in ['max_step_height','walkable_floor_angle','max_walk_speed','can_walk_off_ledges']}
data['capsule_profile']=str(cap.get_collision_profile_name())
data['collision_class_names']=[n for n in dir(u) if 'GeometryScript' in n and 'Collision' in n]
for cl in ['GeometryScript_Collision','GeometryScriptSimpleCollision','KAggregateGeom','KBoxElem','HitResult']:
    c=getattr(u,cl,None);data[cl]={'doc':str(c.__doc__) if c else None,'members':dir(c) if c else []}
if hasattr(u,'GeometryScript_Collision'):
    for n in ['set_simple_collision_of_static_mesh','get_simple_collision_from_static_mesh','set_static_mesh_collision_from_mesh']:
        data[n]=str(getattr(u.GeometryScript_Collision,n).__doc__)
data['tests']=[]
for start,end in [([0,750,300],[0,750,-100]),([0,750,98],[0,750,90]),([0,100,300],[0,100,-100])]:
    hit=u.SystemLibrary.line_trace_single_by_profile(world,u.Vector(*start),u.Vector(*end),'Pawn',False,[],u.DrawDebugTrace.NONE,True)
    data['tests'].append({'start':start,'end':end,'hit':{n:get(lambda n=n:str(hit.get_editor_property(n))) for n in ['blocking_hit','start_penetrating','distance','time','location','impact_point','normal','component','hit_object_handle']}})
(OUT/'probe.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
