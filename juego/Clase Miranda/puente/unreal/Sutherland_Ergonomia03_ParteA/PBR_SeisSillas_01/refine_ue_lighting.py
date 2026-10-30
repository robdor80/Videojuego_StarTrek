import unreal as u,pathlib,json,shutil,traceback
R=pathlib.Path(__file__).parent;P=R.parent/'Unreal';out={'ok':False}
try:
    m=P/'Content/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01.umap';b=R/'Backups/L_PBR_AntesRevisionLuzSuave.umap'
    if not b.exists():shutil.copy2(m,b)
    else:assert m.read_bytes()==b.read_bytes(),'Saved map has advanced; inspect first'
    A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem);assert L.load_level('/Game/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01')
    for a in A.get_all_level_actors():
        if a.get_actor_label().startswith('SM_PBR_P03FG_'):a.static_mesh_component.set_collision_profile_name('NoCollision')
        if isinstance(a,u.RectLight):a.get_component_by_class(u.RectLightComponent).set_intensity(900)
        if isinstance(a,u.PostProcessVolume):
            settings=a.settings;settings.set_editor_property('auto_exposure_min_brightness',3.0);settings.set_editor_property('auto_exposure_max_brightness',3.0);a.settings=settings
    for i,pos in enumerate([(-330,40,300),(330,40,300),(-330,420,320),(330,420,320),(0,640,340),(-810,870,250)]):
        a=A.spawn_actor_from_class(u.PointLight,u.Vector(*pos));a.set_actor_label(f'Sutherland_Relleno_Suave_{i+1:02d}');a.set_folder_path('Sutherland/Iluminacion/Relleno_Techo');c=a.get_component_by_class(u.PointLightComponent);c.set_mobility(u.ComponentMobility.MOVABLE);c.set_editor_property('intensity_units',u.LightUnits.LUMENS);c.set_intensity(250);c.set_light_color(u.LinearColor(1,1,1,1));c.set_editor_property('source_radius',100.0);c.set_editor_property('soft_source_radius',100.0);c.set_attenuation_radius(650);c.set_cast_shadows(False)
    assert L.save_current_level();out['ok']=True;out['rect_lights']=10;out['rect_lumens']=900;out['point_fills']=6;out['point_lumens']=250;out['exposure_EV100']=3
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(R/'lighting_refinement.json').write_text(json.dumps(out,indent=2));print('LIGHTING',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
