import unreal as u,pathlib,json,traceback,math,hashlib,ast
R=pathlib.Path(__file__).parent;P=R.parent/'Unreal';E=u.EditorAssetLibrary;T=u.AssetToolsHelpers.get_asset_tools();A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem);ML=u.MaterialEditingLibrary
BASE='/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01';DEST='/Game/SutherlandPBR01';MAP=DEST+'/Maps/L_Sutherland_PBR_SeisSillas_01'
out={'ok':False,'materials':[],'objects':[],'lights':[],'removed_from_new_map_only':[]}
plan=json.loads((R/'export.json').read_text(encoding='utf-8'));assert plan['ok']
def save(): (R/'integration_progress.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
def import_file(file,folder,name,options=None):
    if E.does_asset_exist(folder+'/'+name):return E.load_asset(folder+'/'+name)
    task=u.AssetImportTask();task.filename=file;task.destination_path=folder;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=False
    if options:task.options=options
    T.import_asset_tasks([task]);obj=E.load_asset(folder+'/'+name);assert obj,('import failed',name,task.imported_object_paths);return obj
def expr(mat,cls,**kwargs):
    n=ML.create_material_expression(mat,cls)
    for k,v in kwargs.items():n.set_editor_property(k,v)
    return n
def connect(a,b,pin):assert ML.connect_material_expressions(a,'',b,pin),(a,b,pin)
def custom(mat,code,args,vector=True):
    n=expr(mat,u.MaterialExpressionCustom,code=code,output_type=u.CustomMaterialOutputType.CMOT_FLOAT3 if vector else u.CustomMaterialOutputType.CMOT_FLOAT1)
    ins=[]
    for name,x in args.items():
        ci=u.CustomInput();ci.set_editor_property('input_name',name);ins.append(ci)
    n.set_editor_property('inputs',ins)
    for name,x in args.items():connect(x,n,name)
    return n
textures={}
def build(mat,r,normal=False,scalar=False):
    op=r['op']
    if op=='constant':
        v=r['value']
        if isinstance(v,list):return expr(mat,u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*v[:3],1))
        return expr(mat,u.MaterialExpressionConstant,r=float(v))
    if op=='texture':
        tr=r['texture'];isnormal=normal;key=tr['name']+('_Normal' if isnormal else '')
        if key not in textures:
            tex=import_file(tr['file'],DEST+'/Textures',key);tex.set_editor_property('srgb',tr['colorspace']=='sRGB' and not isnormal)
            tex.set_editor_property('compression_settings',u.TextureCompressionSettings.TC_NORMALMAP if isnormal else u.TextureCompressionSettings.TC_DEFAULT)
            if isnormal:tex.set_editor_property('flip_green_channel',True)
            E.save_loaded_asset(tex);textures[key]=tex
        node=expr(mat,u.MaterialExpressionTextureSample,texture=textures[key],sampler_type=u.MaterialSamplerType.SAMPLERTYPE_NORMAL if isnormal else (u.MaterialSamplerType.SAMPLERTYPE_COLOR if tr['colorspace']=='sRGB' else u.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR))
        s=r['uv']['scale'];t=r['uv']['location'];uv=expr(mat,u.MaterialExpressionTextureCoordinate)
        uvn=custom(mat,f'return float2(UV.x*{s[0]:.10f}+{t[0]:.10f},UV.y*{s[1]:.10f}+{1-s[1]-t[1]:.10f});',{'UV':uv});uvn.set_editor_property('output_type',u.CustomMaterialOutputType.CMOT_FLOAT2)
        connect(uvn,node,'UVs')
        if scalar:return custom(mat,'return dot(C,float3(0.2126,0.7152,0.0722));',{'C':node},False)
        return node
    if op=='normal':return custom(mat,f'return normalize(lerp(float3(0,0,1),N,{r["strength"]:.10f}));',{'N':build(mat,r['color'],True)})
    if op=='math':
        assert r['mode']=='ADD'
        return custom(mat,'return '+('saturate(A+B)' if r['clamp'] else 'A+B')+';',{'A':build(mat,r['a'],scalar=True),'B':build(mat,r['b'],scalar=True)},False)
    if op=='mix':
        assert r['mode'] in ['MULTIPLY','MIX']
        code='lerp(A,A*B,F)' if r['mode']=='MULTIPLY' else 'lerp(A,B,F)'
        if r['clamp']:code='saturate('+code+')'
        return custom(mat,'return '+code+';',{'A':build(mat,r['a']),'B':build(mat,r['b']),'F':build(mat,r['factor'])})
    if op=='hsv':
        code='''float4 K=float4(0,-1.0/3.0,2.0/3.0,-1);float4 p=lerp(float4(C.bg,K.wz),float4(C.gb,K.xy),step(C.b,C.g));float4 q=lerp(float4(p.xyw,C.r),float4(C.r,p.yzx),step(p.x,C.r));float d=q.x-min(q.w,q.y);float e=1e-10;float3 hsv=float3(abs(q.z+(q.w-q.y)/(6*d+e)),d/(q.x+e),q.x);'''
        code+=f'hsv.x=frac(hsv.x+{r["hue"]-.5:.10f});hsv.y=saturate(hsv.y*{r["saturation"]:.10f});hsv.z*={r["value"]:.10f};'
        code+='float3 rgb=hsv.z*lerp(float3(1,1,1),saturate(abs(frac(hsv.xxx+float3(0,2.0/3.0,1.0/3.0))*6-3)-1),hsv.y);'
        code+=f'return lerp(C,rgb,{r["factor"]:.10f});'
        return custom(mat,code,{'C':build(mat,r['color'])})
    raise RuntimeError(op)
try:
    existing_map=E.does_asset_exist(MAP)
    if existing_map:
        prior=json.loads((R/'integration_result.json').read_text());assert not prior['ok'] and not prior['lights'],'Existing result requires verification'
        assert L.load_level(MAP)
        assert not any(a.get_actor_label().startswith('PBR_') for a in A.get_all_level_actors()),'Partial saved integration: inspect instead'
    assert L.load_level(BASE)
    mats={}
    for name,r in plan['materials'].items():
        path=DEST+'/Materials/'+r['name'];mat=E.load_asset(path)
        if not mat:
            mat=T.create_asset(r['name'],DEST+'/Materials',u.Material,u.MaterialFactoryNew());mat.set_editor_property('two_sided',False)
            if r['kind']=='visual_emissive':
                mat.set_editor_property('shading_model',u.MaterialShadingModel.MSM_UNLIT);n=build(mat,r['channels']['Emission']);n=custom(mat,f'return C*{r["strength"]:.10f};',{'C':n});assert ML.connect_material_property(n,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
            else:
                for k,v in r['channels'].items():
                    prop={'Base Color':u.MaterialProperty.MP_BASE_COLOR,'Roughness':u.MaterialProperty.MP_ROUGHNESS,'Metallic':u.MaterialProperty.MP_METALLIC,'Normal':u.MaterialProperty.MP_NORMAL}[k]
                    assert ML.connect_material_property(build(mat,v,scalar=k in ['Roughness','Metallic']),'',prop)
            ML.layout_material_expressions(mat);ML.recompile_material(mat);E.save_loaded_asset(mat)
        mats[name]=mat;out['materials'].append({'source':name,'asset':mat.get_path_name(),'source_hash':r['source_hash']});save()
    opt=u.FbxImportUI();opt.automated_import_should_detect_type=False;opt.import_mesh=True;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.import_materials=False;opt.import_textures=False
    md=opt.static_mesh_import_data;md.combine_meshes=True;md.auto_generate_collision=False;md.generate_lightmap_u_vs=False;md.convert_scene=True;md.convert_scene_unit=True;md.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
    world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();u.SystemLibrary.execute_console_command(world,'Interchange.FeatureFlags.Import.FBX 0')
    import re
    def norm(s):return re.sub('[^a-zA-Z0-9_]+','_',s).strip('_').lower()
    matlookup={norm(k):v for k,v in mats.items()};meshes={}
    for row in plan['objects']:
        mesh=import_file(row['file'],DEST+'/Meshes',row['asset'],opt)
        for i,slot in enumerate(mesh.get_editor_property('static_materials')):
            key=norm(str(slot.get_editor_property('imported_material_slot_name')))
            if key in matlookup:mesh.set_material(i,matlookup[key])
            else:assert key in ['none','defaultmaterial','material',''],(row['source'],key)
        mesh.get_editor_property('body_setup').set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);E.save_loaded_asset(mesh);meshes[row['source']]=mesh
    # Duplicate only after imports have completed. Existing level is never saved.
    if not existing_map:assert E.duplicate_asset(BASE,MAP)
    assert L.load_level(MAP)
    previous=list(A.get_all_level_actors());seat=next(a for a in previous if isinstance(a,u.STSeatAnchor));oldseat=[a.get_actor_label() for a in seat.chair_collision_actors if a]
    # Replace original bridge presentation and its obsolete collision fabrication
    # in this new map. Door mechanisms, their corrected leaves, guards and Quinn stay.
    for a in previous:
        label=a.get_actor_label()
        if label.startswith(('VIS_','SM_COLL_')) or isinstance(a,u.STSlidingChair) or isinstance(a,u.Light):
            out['removed_from_new_map_only'].append(label);A.destroy_actor(a)
    created={}
    for row in plan['objects']:
        a=A.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*row['position_cm']));a.set_actor_label('PBR_'+row['source']);a.set_folder_path('Sutherland/PBR/Sillas' if row['source'].startswith(('SS_','Mesh.58','Mesh.59','Mesh.60','Cilindro','Floor_')) else 'Sutherland/PBR/Puente')
        c=a.static_mesh_component;c.set_static_mesh(meshes[row['source']]);c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS);c.set_collision_profile_name('BlockAll');c.set_mobility(u.ComponentMobility.STATIC)
        created[row['source']]=a
        center,ext=a.get_actor_bounds(False);expected=row['bounds_cm'];error=max(abs(v-q) for vv,qq in [(center-ext,u.Vector(*expected[0])),(center+ext,u.Vector(*expected[1]))] for v,q in zip(vv.to_tuple(),qq.to_tuple()))
        assert error<.05,(row['source'],'bounds mismatch',error)
        out['objects'].append({'source':row['source'],'actor':a.get_actor_label(),'asset':meshes[row['source']].get_path_name(),'bounds_error_cm':error});save()
    seat.chair_collision_actors=[created[n] for n in ['Mesh.453_0','Sphere.001_0','Cube.002_0','Cylinder_0','Cube_0']]
    assert seat.chair_collision_actors,'Captain seat collision references missing'
    # Preserve repaired collision and animation of leaves; only assign equivalent
    # source PBR and original text texture in this duplicated map.
    for d in [a for a in A.get_all_level_actors() if isinstance(a,u.STAutomaticDoor)]:
        for c in [d.left_leaf,d.right_leaf]:c.set_material(0,mats['PBR_Puertas'])
    # Dynamic UE-only illumination. No emissive GI or static lighting data.
    ws=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world().get_world_settings();ws.set_editor_property('force_no_precomputed_lighting',True)
    for pp in [a for a in A.get_all_level_actors() if isinstance(a,u.PostProcessVolume)]:
        settings=pp.settings
        settings.set_editor_property('override_dynamic_global_illumination_method',True);settings.set_editor_property('dynamic_global_illumination_method',u.DynamicGlobalIlluminationMethod.NONE)
        settings.set_editor_property('override_auto_exposure_min_brightness',True);settings.set_editor_property('override_auto_exposure_max_brightness',True);settings.set_editor_property('auto_exposure_min_brightness',2.0);settings.set_editor_property('auto_exposure_max_brightness',2.0)
        pp.settings=settings
    # Large white area lights, separated by zones, fully editable native actors.
    positions=[(-330,-60,280),(330,-60,280),(-330,210,280),(330,210,280),(-330,470,280),(330,470,280),(0,50,280),(0,330,280),(0,600,280)]
    for i,pos in enumerate(positions):
        a=A.spawn_actor_from_class(u.RectLight,u.Vector(*pos),u.Rotator(pitch=-90,yaw=0,roll=0));a.set_actor_label(f'Sutherland_Luz_Blanca_{i+1:02d}');a.set_folder_path('Sutherland/Iluminacion/Blanca_Pruebas')
        c=a.get_component_by_class(u.RectLightComponent);c.set_mobility(u.ComponentMobility.MOVABLE);c.set_editor_property('intensity_units',u.LightUnits.LUMENS);c.set_intensity(1600);c.set_light_color(u.LinearColor(1,1,1,1));c.set_editor_property('source_width',160.0);c.set_editor_property('source_height',140.0);c.set_attenuation_radius(650)
        out['lights'].append({'actor':a.get_actor_label(),'position_cm':pos,'lumens':1600,'type':'RectLight','mobility':'Movable','color':[1,1,1],'source_cm':[160,140]})
    assert L.save_current_level();out['map']=MAP;out['ok']=True;save()
except Exception:out['error']=traceback.format_exc();save();u.log_error(out['error'])
(R/'integration_result.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('PBR_INTEGRATION',out['ok'],out.get('error'),flush=True);u.SystemLibrary.quit_editor()
