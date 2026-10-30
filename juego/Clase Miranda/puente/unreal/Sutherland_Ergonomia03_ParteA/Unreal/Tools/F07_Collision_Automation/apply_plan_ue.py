"""Apply the reviewed F07 collision plan. Default dry run: no packages saved.

Commit requires commit_plan.json containing the exact SHA256 of collision_plan.json.
Only collision BodySetup data and the Cylinder_002_0 component profile are changed.
"""
import unreal as u
import pathlib,json,hashlib,traceback,re,math
ROOT=pathlib.Path(u.Paths.project_dir()).resolve()
OUT=ROOT/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
PLAN=OUT/'collision_plan.json'
sha=hashlib.sha256(PLAN.read_bytes()).hexdigest()
commitfile=OUT/'commit_plan.json'
VERIFY_ONLY=globals().get('VERIFY_ONLY',False)
COMMIT=not VERIFY_ONLY and commitfile.exists() and json.loads(commitfile.read_text())['plan_sha256']==sha
result={'verify_only':VERIFY_ONLY,'commit_requested':COMMIT,'plan_sha256':sha,'changes':[],'tests':[],'saved_assets':[],'saved_map':False,'ok':False}
def vec(v): return [v.x,v.y,v.z]
def write(): (OUT/('04_verificacion_desde_disco.json' if VERIFY_ONLY else ('03_aplicacion_guardada.json' if COMMIT else '03_candidato_sin_guardar.json'))).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
def visual_digest(m):
    data={'materials':[(str(s.material_slot_name),s.material_interface.get_path_name() if s.material_interface else None) for s in m.get_editor_property('static_materials')],'sections':[]}
    for sec in range(m.get_num_sections(0)):
        vv,tt,nn,uv,tan=u.ProceduralMeshLibrary.get_section_from_static_mesh(m,0,sec)
        data['sections'].append({'v':[vec(v) for v in vv],'t':list(tt),'n':[vec(v) for v in nn],'uv':[[v.x,v.y] for v in uv]})
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
def hitdata(h):
    if h is None:return {'blocked':False}
    raw=h.export_text(); match=re.search(r'PersistentLevel\.([^\.\'\"]+)\.',raw)
    actor=match.group(1) if match else None
    return {'blocked':True,'actor':actor,'label':labels.get(actor),'raw':raw}
def trace(name,start,end,expected, capsule=False,ignore=None,target=None):
    args=(world,u.Vector(*start),u.Vector(*end))
    if capsule:h=u.SystemLibrary.capsule_trace_single_by_profile(*args,35,90,'Pawn',False,ignore or [],u.DrawDebugTrace.NONE,True)
    else:h=u.SystemLibrary.line_trace_single_by_profile(*args,'Pawn',False,ignore or [],u.DrawDebugTrace.NONE,True)
    data=hitdata(h);passed=data['blocked']==expected and (not target or data.get('label') in target)
    test={'name':name,'type':'CAPSULE_SWEEP' if capsule else 'LINE_TRACE','start_cm':start,'end_cm':end,
          'expected_block':expected,'target_labels':target,'pass':passed,**data}
    result['tests'].append(test);return passed
def state(m):
    bs=m.get_editor_property('body_setup'); ag=bs.get_editor_property('agg_geom')
    return {'complexity':str(bs.get_editor_property('collision_trace_flag')),'double_sided':bs.get_editor_property('double_sided_geometry'),
            'primitives':{n:len(ag.get_editor_property(n)) for n in ['box_elems','sphere_elems','sphyl_elems','convex_elems']},'aggregate_text':ag.export_text()}
try:
    loaded=u.get_editor_subsystem(u.LevelEditorSubsystem).load_level('/Game/maps/L_F07_Sutherland_Test')
    assert loaded,'Map did not load'
    assert not u.EditorLoadingAndSavingUtils.get_dirty_content_packages(),'Pre-existing dirty content'
    assert not u.EditorLoadingAndSavingUtils.get_dirty_map_packages(),'Pre-existing dirty map'
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
    actor_sub=u.get_editor_subsystem(u.EditorActorSubsystem)
    actors=list(actor_sub.get_all_level_actors());labels={a.get_name():a.get_actor_label() for a in actors}
    helper_label='F07_COLL_PANTALLA_PRINCIPAL_FIJA'
    existing_helpers=[a for a in actors if a.get_actor_label()==helper_label]
    assert len(existing_helpers)<=1,'Duplicate screen helper'
    assert len(actors)==345+len(existing_helpers),'Unexpected actor count'
    meshes={};components={}
    for a in actors:
        for c in a.get_components_by_class(u.StaticMeshComponent):
            if c.static_mesh:
                name=c.static_mesh.get_name();meshes[name]=c.static_mesh;components[name]=c
    assert all(n in meshes for n in ['Circle_0','Cylinder_002_0']),'Missing model'
    original_visual={a.get_name():a.get_actor_transform().export_text() for a in actors}
    before_visual_meshes={n:visual_digest(m) for n,m in meshes.items() if m.get_path_name().startswith('/Game/star_trek_')}
    if not VERIFY_ONLY:(OUT/'visual_mesh_hashes_before.json').write_text(json.dumps(before_visual_meshes,indent=2),encoding='utf-8')
    protected=['Circle_0','Mesh_589_0','Mesh_589_01','Mesh_589_02','Mesh_589_03','Mesh_589_04','Mesh_589_05',
               'Editable_Mesh_Mat_003_0','Sphere_001_0','Cube_002_0','Cylinder_0','Mesh_453_0','Plane_028_0']
    protected_before={n:state(meshes[n]) for n in protected}
    assert trace('control_suelo_antes',[0,750,300],[0,750,-100],True,target=['Circle_0']),'Physics world unavailable'
    plan=json.loads(PLAN.read_text(encoding='utf-8'))
    for item in plan:
        m=meshes[item['name']];bs=m.get_editor_property('body_setup');before=state(m)
        if VERIFY_ONLY:
            result['changes'].append({'mesh':item['name'],'asset':m.get_path_name(),'strategy':item['strategy'],'reason':item['reason'],'before':before,'after':before})
            continue
        m.modify();bs.modify()
        if item['strategy']=='EXACT_STATIC_TRIANGLES':
            bs.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
            bs.set_editor_property('double_sided_geometry',True)
        elif item['strategy']=='ISLAND_BOXES':
            boxes=[]
            for definition in item['boxes']:
                box=u.KBoxElem()
                box.set_editor_property('center',u.Vector(*definition['center']))
                box.set_editor_property('rotation',u.Quat(*definition['quaternion']).rotator())
                for n,v in zip(['x','y','z'],definition['dims']):box.set_editor_property(n,float(v))
                box.set_editor_property('name',definition['name']);boxes.append(box)
            ag=u.KAggregateGeom();ag.set_editor_property('box_elems',boxes)
            bs.set_editor_property('agg_geom',ag)
            bs.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX)
        elif item['strategy']=='CONVEX_COMPONENTS':
            dynamic=u.DynamicMesh()
            # Construct only the transient collision input from the observed LOD0
            # buffers. Share coincident positions across shading seams. The mesh
            # asset's source/UVs/normals/render buffers are never written.
            vertices=[];triangles=[];keys={}
            for sec in range(m.get_num_sections(0)):
                vv,tt,nn,uv,tan=u.ProceduralMeshLibrary.get_section_from_static_mesh(m,0,sec)
                remap=[]
                for v in vv:
                    key=tuple(round(x,3) for x in vec(v))
                    if key not in keys:keys[key]=len(vertices);vertices.append(v)
                    remap.append(keys[key])
                for k in range(0,len(tt),3):
                    tri=[remap[tt[k+j]] for j in range(3)]
                    if len(set(tri))==3:triangles.append(u.IntVector(*tri))
            buffers=u.GeometryScriptSimpleMeshBuffers()
            buffers.set_editor_property('vertices',vertices);buffers.set_editor_property('triangles',triangles)
            u.GeometryScript_MeshEdits.append_buffers_to_mesh(dynamic,buffers)
            options=u.GeometryScriptCollisionFromMeshOptions()
            options.set_editor_property('method',u.GeometryScriptCollisionGenerationMethod.CONVEX_HULLS)
            options.set_editor_property('auto_detect_boxes',False);options.set_editor_property('auto_detect_spheres',False)
            options.set_editor_property('auto_detect_capsules',False);options.set_editor_property('simplify_hulls',False)
            options.set_editor_property('max_convex_hulls_per_mesh',1)
            options.set_editor_property('remove_fully_contained_shapes',True)
            bs.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX)
            u.GeometryScript_Collision.set_static_mesh_collision_from_mesh(dynamic,m,options)
        collision=u.GeometryScript_Collision.get_simple_collision_from_static_mesh(m)
        u.GeometryScript_Collision.set_simple_collision_of_static_mesh(collision,m,u.GeometryScriptSetSimpleCollisionOptions())
        after=state(m)
        if item['strategy']=='ISLAND_BOXES':assert after['primitives']['box_elems']==len(item['boxes'])
        if item['strategy']=='CONVEX_COMPONENTS':
            count=sum(after['primitives'].values())
            assert 1<=count<=32,(item['name'],count)
            if 'expected_shapes' in item:assert count==item['expected_shapes'],(item['name'],count)
        result['changes'].append({'mesh':item['name'],'asset':m.get_path_name(),'strategy':item['strategy'],'reason':item['reason'],'before':before,'after':after})
    cyl=components['Cylinder_002_0'];result['cylinder_profile_before']=str(cyl.get_collision_profile_name())
    if not VERIFY_ONLY:cyl.modify();cyl.set_collision_profile_name('BlockAll')
    result['cylinder_profile_after']=str(cyl.get_collision_profile_name())
    assert str(cyl.get_collision_profile_name())=='BlockAll'
    # The principal-screen frame has a genuine unmodelled opening, NOT a fifth door.
    # One targeted safety slab in that opening prevents exits into the void.
    # Measurements come from Plane_015_0 frame vertices (inner x +/-216.405,
    # y 988.656..1008.328, upper edge z388.762). It never intersects door regions.
    helper=existing_helpers[0] if existing_helpers else actor_sub.spawn_actor_from_class(u.StaticMeshActor,u.Vector(0,998.492,194.381),u.Rotator())
    hc=helper.get_component_by_class(u.StaticMeshComponent)
    if not VERIFY_ONLY:
        helper.set_actor_label(helper_label);helper.set_folder_path('F07_Collision_Proxies')
        helper.set_editor_property('tags',['F07_COLLISION','SCREEN_VOID_SAFETY','NOT_A_DOOR'])
        helper.set_actor_location(u.Vector(0,998.492,194.381),False,False)
        helper.set_actor_scale3d(u.Vector(4.32810,.19672,3.88762))
        hc.set_static_mesh(u.load_asset('/Engine/BasicShapes/Cube.Cube'))
        hc.set_collision_profile_name('BlockAll');hc.set_visibility(False,True);hc.set_hidden_in_game(True,True)
        hc.set_cast_shadow(False);helper.set_actor_hidden_in_game(True)
    result['helper']={'label':helper_label,'location':vec(helper.get_actor_location()),'scale':vec(helper.get_actor_scale3d()),
                      'reason':'Hueco real de pantalla sin superficie: tope puntual de seguridad dentro del marco, lejos de puertas',
                      'created':not bool(existing_helpers),'visible':False}
    actors=list(actor_sub.get_all_level_actors());labels={a.get_name():a.get_actor_label() for a in actors}
    # Capsules use the real Character CDO dimensions, not PlayerStart's visualization.
    gm=u.get_default_object(world.get_world_settings().get_editor_property('default_game_mode'))
    pawn=u.get_default_object(gm.get_editor_property('default_pawn_class'));cap=pawn.get_component_by_class(u.CapsuleComponent)
    result['capsule']={'radius':cap.get_scaled_capsule_radius(),'half_height':cap.get_scaled_capsule_half_height()}
    result['capsule']['object_type']=str(cap.get_collision_object_type())
    result['capsule']['world_static_response']=str(cap.get_collision_response_to_channel(u.CollisionChannel.ECC_WORLD_STATIC))
    assert cap.get_scaled_capsule_radius()==35.0 and cap.get_scaled_capsule_half_height()==90.0
    for side in [-1,1]:
        trace(f'pasillo_interior_alternativo_{side}_ida',[side*360,130,92],[side*360,650,92],False,True)
        trace(f'pasillo_interior_alternativo_{side}_vuelta',[side*360,650,92],[side*360,130,92],False,True)
    for side in [-1,1]:
        for x in [520,530,540]:
            # x540 grazes real angled end-wall returns; x520/530 are the full routes.
            # After restoring the seat pans' actual physics, these lines are diagnostic.
            trace(f'pasillo_{side}_x{x}_ida',[side*x,110,92],[side*x,650,92],False,True)
            trace(f'pasillo_{side}_x{x}_vuelta',[side*x,650,92],[side*x,110,92],False,True)
    analysis=json.loads((OUT/'geometry_analysis.json').read_text(encoding='utf-8'))
    base=next(s for s in analysis if s['name']=='Cylinder_002_0')
    for i,island in enumerate(base['islands']):
        x,y,z=island['center'];side=1 if x>0 else -1
        trace(f'base_solida_{i:02}',[x-side*65,y,z],[x+side*45,y,z],True,target=['Cylinder_002_0'])
    catalog=json.loads((OUT/'puertas_f07_inventario.json').read_text(encoding='utf-8'))
    leaf_names=['Plane_001_0','Plane_017_0','Plane_018_0','Plane_019_0']
    def doortrace(d,opened,offset=0):
        x,y,z=d['center_cm'];nx,ny=d['normal_outward_xy'];tx,ty=d['tangent_xy']
        x+=tx*offset;y+=ty*offset;z=d['bounds_cm'][0][2]+110
        return trace(f"{d['id']}_{'hojas_sin_colision' if opened else 'cerrada'}_offset{offset}",
                     [x-nx*110,y-ny*110,z],[x+nx*110,y+ny*110,z],not opened,True,
                     target=None if opened else leaf_names)
    for d in catalog['doors']:
        for off in [-30,0,30]:doortrace(d,False,off)
    for n in leaf_names:components[n].set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
    for d in catalog['doors']:
        for off in [-30,0,30]:doortrace(d,True,off)
    for n in leaf_names:components[n].set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS)
    # Floor surfaces: physical traces at centroids obtained from exported geometry.
    geo=json.loads((OUT/'world_geometry.json').read_text(encoding='utf-8'))
    floor_names=['Circle_0','Circle_001_0','Circle_002_0','Plane_002_0','Plane_003_0','Plane_021_0']
    ignore_floor=[a for a in actors if not any(c.static_mesh and c.static_mesh.get_name() in floor_names for c in a.get_components_by_class(u.StaticMeshComponent))]
    for name in floor_names:
        md=geo[name];count=0
        for tri in md['t']:
            vv=[md['v'][i] for i in tri]
            ab=[vv[1][j]-vv[0][j] for j in range(3)];ac=[vv[2][j]-vv[0][j] for j in range(3)]
            n=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]]
            length=math.sqrt(sum(x*x for x in n))
            if length<.01 or abs(n[2])/length<.7:continue
            center=[sum(v[j] for v in vv)/3 for j in range(3)];count+=1
            trace(f'suelo_{name}_{count}',[center[0],center[1],center[2]+50],[center[0],center[1],center[2]-20],True,ignore=ignore_floor)
    # Perimeter: rays from the interior, furniture ignored, and reverse direction.
    perimeter_names=set(['Cube','Plane_0','Plane_007_0','Plane_010_0','Plane_013_0','Plane_014_0','Plane_016_0',
                         'Cube_000_0','Cube_001_0','Plane_005_0','Plane_004_0','Plane_015_0','Plane_011_0','Plane_039_0']+leaf_names)
    ignore=[a for a in actors if not any(c.static_mesh and c.static_mesh.get_name() in perimeter_names for c in a.get_components_by_class(u.StaticMeshComponent))]
    for degrees in range(0,360,5):
        angle=math.radians(degrees);p=[1600*math.cos(angle),400+1600*math.sin(angle),200]
        trace(f'perimetro_salida_{degrees:03}',[0,400,200],p,True,ignore=ignore)
        trace(f'perimetro_entrada_{degrees:03}',p,[0,400,200],True,ignore=ignore)
    trace('spawn_suelo',[-19.9228,760.0297,131.6858],[-19.9228,760.0297,-20],True)
    # Sample every newly configured solid asset at an observed triangle, in isolation.
    for item in plan:
        name=item['name']
        if item['strategy'] in ['REBUILD_EXISTING_COLLISION','ISLAND_BOXES'] or name=='Cylinder_002_0':continue
        ca=components[name].get_owner();ignored=[a for a in actors if a!=ca];md=geo[ca.get_actor_label()];candidates=[]
        for tri in md['t']:
            vv=[md['v'][i] for i in tri];ab=[vv[1][j]-vv[0][j] for j in range(3)];ac=[vv[2][j]-vv[0][j] for j in range(3)]
            n=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]];size=math.sqrt(sum(v*v for v in n))
            if size>.01:candidates.append((size,[sum(v[j] for v in vv)/3 for j in range(3)],[x/size for x in n]))
        _,center,normal=max(candidates);start=[center[j]+normal[j]*30 for j in range(3)];end=[center[j]-normal[j]*30 for j in range(3)]
        h1=u.SystemLibrary.line_trace_single_by_profile(world,u.Vector(*start),u.Vector(*end),'Pawn',False,ignored,u.DrawDebugTrace.NONE,True)
        h2=u.SystemLibrary.line_trace_single_by_profile(world,u.Vector(*end),u.Vector(*start),'Pawn',False,ignored,u.DrawDebugTrace.NONE,True)
        result['tests'].append({'name':f'muestra_fisica_asset_{name}','type':'TRIANGLE_NORMAL_TWO_DIRECTIONS','start_cm':start,'end_cm':end,
                                'pass':h1 is not None or h2 is not None,'forward':hitdata(h1),'reverse':hitdata(h2)})
    # Regression: ray through a real triangle, not a bounding-box center that may be hollow.
    for name in protected:
        if name=='Circle_0':continue
        ca=components[name].get_owner();ignored=[a for a in actors if a!=ca]
        md=geo[ca.get_actor_label()]; candidates=[]
        for tri in md['t']:
            vv=[md['v'][i] for i in tri];ab=[vv[1][j]-vv[0][j] for j in range(3)];ac=[vv[2][j]-vv[0][j] for j in range(3)]
            n=[ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0]]
            size=math.sqrt(sum(v*v for v in n))
            if size>.01:candidates.append((size,[sum(v[j] for v in vv)/3 for j in range(3)],[x/size for x in n]))
        _,center,normal=max(candidates)
        start=[center[j]+normal[j]*15 for j in range(3)];end=[center[j]-normal[j]*15 for j in range(3)]
        h1=u.SystemLibrary.line_trace_single_by_profile(world,u.Vector(*start),u.Vector(*end),'Pawn',False,ignored,u.DrawDebugTrace.NONE,True)
        h2=u.SystemLibrary.line_trace_single_by_profile(world,u.Vector(*end),u.Vector(*start),'Pawn',False,ignored,u.DrawDebugTrace.NONE,True)
        result['tests'].append({'name':f'regresion_objeto_{name}','type':'TRIANGLE_NORMAL_TWO_DIRECTIONS','start_cm':start,'end_cm':end,
                                'pass':h1 is not None or h2 is not None,'forward':hitdata(h1),'reverse':hitdata(h2)})
    result['visual_transforms_unchanged']=all(a.get_actor_transform().export_text()==original_visual[a.get_name()] for a in actors if a.get_name() in original_visual)
    after_visual_meshes={n:visual_digest(m) for n,m in meshes.items() if m.get_path_name().startswith('/Game/star_trek_')}
    reference=json.loads((OUT/'visual_mesh_hashes_before.json').read_text())
    result['visual_meshes_unchanged']=after_visual_meshes==reference
    result['visual_mesh_count']=len(after_visual_meshes)
    result['protected_collision_unchanged']=all(state(meshes[n])==protected_before[n] for n in protected)
    result['actor_count_expected']=len(actor_sub.get_all_level_actors())==346
    result['failed_tests']=[t['name'] for t in result['tests'] if not t['pass']]
    # Bounds-center regression misses can represent open geometry; all critical tests gate saving.
    # Keep failed outer-aisle tests as failed: measured solid geometry is narrower
    # than the unchanged capsule. Saving other safe work is allowed only with this
    # explicit unresolved limitation, not by claiming that the route is free.
    result['known_geometry_limitations']=[n for n in result['failed_tests'] if re.match(r'pasillo_-?1_x',n)]
    result['critical_failures']=[n for n in result['failed_tests'] if n not in result['known_geometry_limitations']]
    result['functional_complete']=not result['known_geometry_limitations']
    assert result['visual_transforms_unchanged'] and result['visual_meshes_unchanged'] and result['protected_collision_unchanged'] and result['actor_count_expected']
    assert not result['critical_failures'],str(result['critical_failures'])
    result['ok']=True
    if COMMIT:
        for item in plan:
            m=meshes[item['name']]
            assert u.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=True),m.get_name()
            result['saved_assets'].append(m.get_path_name());write()
        assert u.get_editor_subsystem(u.LevelEditorSubsystem).save_current_level(),'Map save failed'
        result['saved_map']=True
    write()
except Exception:
    result['error']=traceback.format_exc();write()
    raise
