import unreal as u,json,pathlib,traceback,re,math
OUT=pathlib.Path(u.Paths.project_dir())/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
data={'saved':False,'tests':[]}
try:
    u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/maps/L_F07_Sutherland_Test')
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    actors=list(u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors())
    a=next(a for a in actors if a.get_actor_label()=='Mesh_589_0');c=a.get_component_by_class(u.StaticMeshComponent);m=c.static_mesh
    data['component']={n:str(c.get_editor_property(n)) for n in ['body_instance','mobility']}
    data['mesh']={n:str(m.get_editor_property(n)) for n in ['lod_for_collision','complex_collision_mesh','body_setup']}
    g=json.loads((OUT/'world_geometry.json').read_text());md=g['Mesh_589_0']
    def trace(n,start,end,capsule=False,ignore=None,complex=False):
        args=[world,u.Vector(*start),u.Vector(*end)]
        if capsule:hit=u.SystemLibrary.capsule_trace_single_by_profile(*args,35,90,'Pawn',complex,ignore or [],u.DrawDebugTrace.NONE,True)
        else:hit=u.SystemLibrary.line_trace_single_by_profile(*args,'Pawn',complex,ignore or [],u.DrawDebugTrace.NONE,True)
        data['tests'].append({'name':n,'start':start,'end':end,'blocked':hit is not None,'raw':hit.export_text() if hit else None})
    for stage in ['original','refresh']:
        if stage=='refresh':
            collision=u.GeometryScript_Collision.get_simple_collision_from_static_mesh(m)
            u.GeometryScript_Collision.set_simple_collision_of_static_mesh(collision,m,u.GeometryScriptSetSimpleCollisionOptions())
        for ignore in [False,True]:
            ignored=[x for x in actors if x!=a] if ignore else []
            for z in [74,92,120]:trace(f'{stage}_capsule_ignore{ignore}_z{z}',[350,174,z],[600,174,z],True,ignored)
            for num,tri in enumerate(md['t']):
                if num>30:break
                vv=[md['v'][i] for i in tri];ab=[vv[1][j]-vv[0][j] for j in range(3)];ac=[vv[2][j]-vv[0][j] for j in range(3)]
                nn=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]];mag=math.sqrt(sum(x*x for x in nn))
                if mag<1e-5:continue
                center=[sum(v[j] for v in vv)/3 for j in range(3)];normal=[n/mag for n in nn]
                start=[center[j]+normal[j]*10 for j in range(3)];end=[center[j]-normal[j]*10 for j in range(3)]
                trace(f'{stage}_tri_{num}_ignore{ignore}_forward',start,end,ignore=ignored)
                trace(f'{stage}_tri_{num}_ignore{ignore}_back',end,start,ignore=ignored)
    data['ok']=True
except Exception:data['ok']=False;data['error']=traceback.format_exc()
(OUT/'chair_probe.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
