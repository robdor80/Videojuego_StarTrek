import unreal as u,json,pathlib,traceback,ast,math
R=pathlib.Path(__file__).parent;E=u.EditorAssetLibrary;A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem)
out={'ok':False,'objects':[]}
try:
    assert L.load_level('/Game/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01')
    plan=json.loads((R/'export.json').read_text(encoding='utf-8'));actors={a.get_actor_label():a for a in A.get_all_level_actors()}
    # Reuse an already validated bidirectional world-vertex comparison.
    source=ast.parse((R.parent/'Scripts/07_integrate.py').read_text(encoding='utf-8-sig'));selected=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in ['compare','points']];exec(compile(ast.Module(body=selected,type_ignores=[]),str(__file__),'exec'))
    for row in plan['objects']:
        a=actors['PBR_'+row['source']];c=a.static_mesh_component;err=compare(row['points_cm'],points(c),.005)
        assert c.get_collision_enabled()==u.CollisionEnabled.QUERY_AND_PHYSICS
        assert c.static_mesh.get_editor_property('body_setup').get_editor_property('collision_trace_flag')==u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE
        out['objects'].append({'source':row['source'],'world_vertex_error_cm':err,'materials':[m.get_path_name() if m else None for m in c.get_materials()]})
    assert len(out['objects'])==167
    out['chair_components']={}
    for i in range(1,7):
        names=[row['source'] for row in plan['objects']]
        if i==1:names=[n for n in names if n.startswith(('Mesh.58','Mesh.59','Mesh.60')) or n in ['Cilindro','Floor_aiWireframe1_0']]
        else:names=[n for n in names if n.startswith(f'SS_P{i:02d}_')]
        out['chair_components'][f'P{i:02d}']=len(names)
    assert all(v==16 for v in out['chair_components'].values()),out['chair_components']
    out['old_visual_actor_count']=sum(a.startswith(('VIS_','SM_COLL_')) for a in actors);assert out['old_visual_actor_count']==0
    doors=[a for a in actors.values() if isinstance(a,u.STAutomaticDoor)];assert len(doors)==4
    out['doors']=[{'id':str(d.door_id),'destination_constructed':d.destination_constructed,'leaves':[c.static_mesh.get_path_name() for c in [d.left_leaf,d.right_leaf]]} for d in doors]
    out['leaf_visuals']=[]
    for row in json.loads((R/'leaf_visual_export.json').read_text()):
        a=actors[row['asset']];c=a.static_mesh_component;err=compare(row['points_cm'],points(c),.005);assert c.get_collision_enabled()==u.CollisionEnabled.NO_COLLISION
        door=actors[row['door']];leaf=door.left_leaf if row['component']=='LeftLeaf' else door.right_leaf
        assert not leaf.is_visible() and c.is_visible();assert a.get_attach_parent_actor()==door
        out['leaf_visuals'].append({'actor':row['asset'],'error_cm':err,'materials':[m.get_path_name() for m in c.get_materials()]})
    lights=[a for a in actors.values() if isinstance(a,u.Light)];assert len(lights)==16
    out['lights']=[]
    for a in lights:
        c=a.get_component_by_class(u.LightComponent);assert c and c.mobility==u.ComponentMobility.MOVABLE
        out['lights'].append({'label':a.get_actor_label(),'intensity':c.intensity,'folder':str(a.get_folder_path()),'mobility':str(c.mobility)})
    seat=next(a for a in actors.values() if isinstance(a,u.STSeatAnchor));assert len(seat.chair_collision_actors)==5
    out['captain_collision_references']=[a.get_actor_label() for a in seat.chair_collision_actors]
    out['world_no_precomputed_lighting']=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world().get_world_settings().get_editor_property('force_no_precomputed_lighting');assert out['world_no_precomputed_lighting']
    out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(R/'saved_verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('PBR_SAVED_VERIFY',out['ok'],out.get('error'),flush=True);u.SystemLibrary.quit_editor()
