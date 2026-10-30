"""Preserve each source face material, with visual children on repaired collision leaves."""
import unreal as u,json,pathlib,re,shutil,traceback
R=pathlib.Path(__file__).parent;P=R.parent/'Unreal';E=u.EditorAssetLibrary;T=u.AssetToolsHelpers.get_asset_tools();A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem);out={'ok':False,'leaves':[]}
try:
    mapfile=P/'Content/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01.umap';b=R/'Backups/L_PBR_AntesMaterialesHojas.umap';assert not b.exists();shutil.copy2(mapfile,b)
    assert L.load_level('/Game/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01');actors={a.get_actor_label():a for a in A.get_all_level_actors()}
    plan=json.loads((R/'export.json').read_text(encoding='utf-8'));rows=json.loads((R/'leaf_visual_export.json').read_text());world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();u.SystemLibrary.execute_console_command(world,'Interchange.FeatureFlags.Import.FBX 0')
    def norm(s):return re.sub('[^a-zA-Z0-9_]+','_',s).strip('_').lower()
    mats={norm(k):E.load_asset('/Game/SutherlandPBR01/Materials/'+v['name']) for k,v in plan['materials'].items()}
    for row in rows:
        assert row['asset'] not in actors
        task=u.AssetImportTask();task.filename=row['file'];task.destination_path='/Game/SutherlandPBR01/Meshes';task.destination_name=row['asset'];task.automated=True;task.save=True;task.replace_existing=False
        opt=u.FbxImportUI();opt.automated_import_should_detect_type=False;opt.import_mesh=True;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.import_materials=False;opt.import_textures=False;md=opt.static_mesh_import_data;md.combine_meshes=True;md.auto_generate_collision=False;md.generate_lightmap_u_vs=False;md.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS;task.options=opt;T.import_asset_tasks([task])
        mesh=E.load_asset(task.destination_path+'/'+row['asset']);assert mesh
        for i,s in enumerate(mesh.get_editor_property('static_materials')):
            key=norm(str(s.get_editor_property('imported_material_slot_name')));assert key in mats,key;mesh.set_material(i,mats[key])
        E.save_loaded_asset(mesh);d=actors[row['door']];leaf=d.left_leaf if row['component']=='LeftLeaf' else d.right_leaf
        a=A.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*row['position_cm']));a.set_actor_label(row['asset']);a.set_folder_path('Sutherland/PBR/Puertas');c=a.static_mesh_component;c.set_mobility(u.ComponentMobility.MOVABLE);c.set_static_mesh(mesh);c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
        assert a.attach_to_component(leaf,'',u.AttachmentRule.KEEP_WORLD,u.AttachmentRule.KEEP_WORLD,u.AttachmentRule.KEEP_WORLD,False)
        leaf.set_visibility(False,False)
        out['leaves'].append({'actor':a.get_actor_label(),'door':row['door'],'parent_component':row['component'],'materials':[m.get_path_name() for m in c.get_materials()],'collision_reused':leaf.static_mesh.get_path_name()})
    a=A.spawn_actor_from_class(u.RectLight,u.Vector(-810,870,260),u.Rotator(pitch=-90,yaw=0,roll=0));a.set_actor_label('Sutherland_Luz_Blanca_Turbo_D04');a.set_folder_path('Sutherland/Iluminacion/Blanca_Pruebas');c=a.get_component_by_class(u.RectLightComponent);c.set_mobility(u.ComponentMobility.MOVABLE);c.set_editor_property('intensity_units',u.LightUnits.LUMENS);c.set_intensity(900);c.set_light_color(u.LinearColor(1,1,1,1));c.set_editor_property('source_width',100.0);c.set_editor_property('source_height',100.0);c.set_attenuation_radius(400)
    assert L.save_current_level();out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(R/'leaf_materials.json').write_text(json.dumps(out,indent=2));print('LEAF_MATERIALS',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
