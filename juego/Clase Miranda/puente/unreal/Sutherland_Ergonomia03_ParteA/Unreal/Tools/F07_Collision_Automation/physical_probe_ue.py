"""Temporary collision experiments in a fully initialized editor. No package saves."""
import unreal as u,json,pathlib,traceback,re
OUT=pathlib.Path(u.Paths.project_dir())/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
data={'saved':False,'tests':[]}
def hit_data(h):
    if h is None:return {'blocked':False}
    raw=h.export_text()
    found=re.search(r'PersistentLevel\.([^\.\'\"]+)\.',raw)
    actor=found.group(1) if found else None
    return {'blocked':True,'raw':raw,'actor':actor,
            'label':next((a.get_actor_label() for a in actors if a.get_name()==actor),None)}
try:
    u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/maps/L_F07_Sutherland_Test')
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
    a=next(a for a in actors if a.get_actor_label()=='Cylinder_002_0')
    c=a.get_component_by_class(u.StaticMeshComponent);m=c.static_mesh
    def sweep(name,start,end,r=35,hh=90):
        h=u.SystemLibrary.capsule_trace_single_by_profile(world,u.Vector(*start),u.Vector(*end),r,hh,'Pawn',False,[],u.DrawDebugTrace.NONE,True)
        data['tests'].append({'name':name,'start':start,'end':end,'radius':r,'half_height':hh,**hit_data(h)})
    def line(name,start,end):
        h=u.SystemLibrary.line_trace_single_by_profile(world,u.Vector(*start),u.Vector(*end),'Pawn',False,[],u.DrawDebugTrace.NONE,True)
        data['tests'].append({'name':name,'start':start,'end':end,**hit_data(h)})
    line('floor_control',[0,750,300],[0,750,-100])
    for enabled in [False,True]:
        c.set_collision_profile_name('BlockAll' if enabled else 'NoCollision')
        for side in [-1,1]:
            for x in [490,500,510,520,530,540,550]:
                sweep(('complex_on' if enabled else 'disabled')+f'_{side}_{x}',[side*x,110,92],[side*x,650,92])
        line('base_block_'+str(enabled),[540,373,88],[640,373,88])
    # Probe a simple representation using public GeometryScript collision setter.
    gs=u.GeometryScriptSimpleCollision()
    ag=u.KAggregateGeom()
    boxes=[]
    analysis=json.loads((OUT/'geometry_analysis.json').read_text(encoding='utf-8'))
    entry=next(x for x in analysis if x['name']=='Cylinder_002_0')
    t=c.get_world_transform()
    for i,it in enumerate(entry['islands']):
        center=t.inverse_transform_location(u.Vector(*it['center']))
        # This imported actor is uniformly scaled and rotated +90deg around X.
        dims=it['dims']; box=u.KBoxElem()
        box.set_editor_property('center',center)
        box.set_editor_property('x',dims[0]);box.set_editor_property('y',dims[2]);box.set_editor_property('z',dims[1])
        box.set_editor_property('name',f'F07_BASE_{i:02}')
        boxes.append(box)
    ag.set_editor_property('box_elems',boxes)
    m.get_editor_property('body_setup').set_editor_property('agg_geom',ag)
    gs=u.GeometryScript_Collision.get_simple_collision_from_static_mesh(m)
    m.get_editor_property('body_setup').set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX)
    u.GeometryScript_Collision.set_simple_collision_of_static_mesh(gs,m,u.GeometryScriptSetSimpleCollisionOptions())
    data['simple_shapes']=gs.get_simple_collision_shape_count()
    for side in [-1,1]:
        for x in [490,500,510,520,530,540,550]:sweep(f'boxes_{side}_{x}',[side*x,110,92],[side*x,650,92])
    line('base_block_boxes',[540,373,88],[640,373,88])
    data['ok']=True
except Exception:
    data['ok']=False;data['error']=traceback.format_exc()
(OUT/'physical_probe.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
