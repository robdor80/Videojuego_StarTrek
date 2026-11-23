"""UE Python: author V06 only in a new independent copy prepared by prepare_v06.py.
Set VH_EVIDENCE_DIR to a new authorized output directory; run with a real RHI.
"""
import json,os,traceback
from pathlib import Path
import unreal as u

MAP='/Game/Valhalla/Maps/L_Supercomputadora_V06_Quinn'
BASE='/Game/Valhalla/Maps/L_Supercomputadora_V05'
SCRIPTS=Path(__file__).resolve().parent

def main():
    evidence=Path(os.environ['VH_EVIDENCE_DIR']).resolve()
    if evidence.exists() and any(evidence.iterdir()):raise RuntimeError('Use a new empty evidence directory')
    evidence.mkdir(parents=True,exist_ok=True)
    assert not u.EditorAssetLibrary.does_asset_exist(MAP),'Never overwrite V06 or an existing delivery'
    w=u.EditorLoadingAndSavingUtils.load_map(BASE);u.VH06Tools.finish_compilation()
    actors=u.get_editor_subsystem(u.EditorActorSubsystem);tools=u.AssetToolsHelpers.get_asset_tools()
    placed=sum(c.get_instance_count() for a in actors.get_all_level_actors() for c in a.get_components_by_class(u.InstancedStaticMeshComponent));assert placed==16302
    result={'map_check_before':json.loads(u.VH06Tools.map_check_snapshot())}
    result['material_correction']=json.loads(u.VH06Tools.correct_instanced_material_usage());assert result['material_correction']['ok']
    result['winding_correction']=json.loads(u.VH06Tools.correct_winding());assert result['winding_correction']['ok']
    result['stair_collision']=[];references=[]
    for actor in actors.get_all_level_actors():
        if isinstance(actor,u.VHFunctionalProbe):actors.destroy_actor(actor);continue
        if isinstance(actor,u.PlayerStart):actor.set_actor_label('V06 Inicio Quinn - D01')
        for c in actor.get_components_by_class(u.InstancedStaticMeshComponent):
            name=c.get_name()
            if name in ['InstancedStaticMeshComponent_47','InstancedStaticMeshComponent_170']:
                entry=json.loads(u.VH06Tools.set_stair_collision(c.static_mesh));assert entry['render_mesh_untouched'];result['stair_collision'].append(entry)
            if name in ['InstancedStaticMeshComponent_165','InstancedStaticMeshComponent_166','InstancedStaticMeshComponent_167','InstancedStaticMeshComponent_168']:
                references.append({'component':name,'instances':c.get_instance_count(),'mesh':c.static_mesh.get_path_name()});c.set_visibility(False);c.set_hidden_in_game(True);c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION);c.set_editor_property('component_tags',[u.Name('V06_REFERENCE_NANCY_NOT_GAMEPLAY')])
        for c in actor.get_components_by_class(u.LightComponent):c.set_cast_shadows(False)
    assert len(result['stair_collision'])==2 and sum(x['instances'] for x in references)==8
    result['reference_scale_figures']=references
    result['floor_faces']=json.loads(u.VH06Tools.correct_floor_faces());assert all(x['positions_uv_materials_unchanged'] for x in result['floor_faces']['corrections'])
    bp=tools.duplicate_asset('BP_Valhalla_Quinn','/Game/ValhallaV06/Blueprints',u.load_asset('/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter'));u.BlueprintEditorLibrary.compile_blueprint(bp);u.EditorAssetLibrary.save_loaded_asset(bp)
    quinn=u.EditorAssetLibrary.load_blueprint_class('/Game/ValhallaV06/Blueprints/BP_Valhalla_Quinn')
    probe=actors.spawn_actor_from_class(quinn,u.Vector(-100000,0,1000));capsule=probe.get_component_by_class(u.CapsuleComponent);assert capsule.get_unscaled_capsule_radius()==35 and capsule.get_unscaled_capsule_half_height()==90;actors.destroy_actor(probe)
    factory=u.BlueprintFactory();factory.set_editor_property('parent_class',u.GameModeBase);gm=tools.create_asset('BP_Valhalla_V06_GameMode','/Game/ValhallaV06/Blueprints',None,factory);u.BlueprintEditorLibrary.compile_blueprint(gm);gmclass=u.EditorAssetLibrary.load_blueprint_class('/Game/ValhallaV06/Blueprints/BP_Valhalla_V06_GameMode');default=u.get_default_object(gmclass);default.set_editor_property('default_pawn_class',quinn);default.set_editor_property('player_controller_class',u.EditorAssetLibrary.load_blueprint_class('/Game/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController'));u.EditorAssetLibrary.save_loaded_asset(gm);w.get_world_settings().set_editor_property('default_game_mode',gmclass)
    door=next(x for x in actors.get_all_level_actors() if isinstance(x,u.VHAutomaticDoor));door.set_editor_property('proximity_depth',240.0);door.reset_closed()
    actors.spawn_actor_from_class(u.VH06Probe,u.Vector())
    for row in json.loads((SCRIPTS/'v06_lighting.json').read_text(encoding='utf8')):
        actor=actors.spawn_actor_from_class(u.PointLight,u.Vector(*row['location_cm']));actor.set_actor_label(row['actor']);actor.set_editor_property('tags',[u.Name('V06_PROVISIONAL_LIGHT')]);c=actor.get_component_by_class(u.PointLightComponent);c.set_mobility(u.ComponentMobility.MOVABLE);c.set_editor_property('intensity_units',u.LightUnits.LUMENS);c.set_intensity(row['lumens']);c.set_attenuation_radius(row['radius_cm']);c.set_cast_shadows(False)
    sun=actors.spawn_actor_from_class(u.DirectionalLight,u.Vector(0,0,700),u.Rotator(pitch=-25,yaw=0,roll=-65));sun.set_actor_label('V06_TECH_UniformFill');sun.set_editor_property('tags',[u.Name('V06_PROVISIONAL_LIGHT')]);c=sun.get_component_by_class(u.DirectionalLightComponent);c.set_mobility(u.ComponentMobility.MOVABLE);c.set_intensity(2);c.set_cast_shadows(False)
    pp=actors.spawn_actor_from_class(u.PostProcessVolume,u.Vector());pp.set_actor_label('V06_TECH_FixedExposure');pp.set_editor_property('tags',[u.Name('V06_PROVISIONAL_LIGHT')]);pp.set_editor_property('unbound',True);settings=pp.get_editor_property('settings')
    for key,value in [('override_auto_exposure_method',True),('auto_exposure_method',u.AutoExposureMethod.AEM_MANUAL),('override_auto_exposure_bias',True),('auto_exposure_bias',-1.5),('override_auto_exposure_apply_physical_camera_exposure',True),('auto_exposure_apply_physical_camera_exposure',False),('override_bloom_intensity',True),('bloom_intensity',.1),('override_motion_blur_amount',True),('motion_blur_amount',0.0)]:settings.set_editor_property(key,value)
    pp.set_editor_property('settings',settings)
    cube=u.load_asset('/Engine/BasicShapes/Cube');blue=u.load_asset('/Game/Valhalla/Materials/M_061');white=u.load_asset('/Game/Valhalla/Materials/M_099')
    for row in json.loads((SCRIPTS/'v06_boundaries.json').read_text(encoding='utf8')):
        x,y=row['center_xy'];rotation=u.Rotator(pitch=0,yaw=row['yaw_deg'],roll=0)
        actor=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x,y,row['bottom_cm']+row['height_cm']/2),rotation);actor.set_actor_label('V06_'+row['id']);actor.set_editor_property('tags',[u.Name('V06_VISIBLE_BOUNDARY'),u.Name(row['id'])]);c=actor.static_mesh_component;c.set_static_mesh(cube);c.set_material(0,blue);c.set_collision_profile_name('BlockAll');actor.set_actor_scale3d(u.Vector(row['thickness_cm']/100,row['width_cm']/100,row['height_cm']/100))
        header=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x,y,row['bottom_cm']+row['height_cm']-4),rotation);header.set_actor_label('V06_'+row['id']+'_Remate');header.set_editor_property('tags',[u.Name('V06_VISIBLE_BOUNDARY')]);header.static_mesh_component.set_static_mesh(cube);header.static_mesh_component.set_material(0,white);header.set_actor_scale3d(u.Vector(.14,row['width_cm']/100,.08))
    u.VH06Tools.finish_compilation();assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
    result['ok']=True
    (evidence/'author_v06.json').write_text(json.dumps(result,indent=2),encoding='utf8')
try:main()
except Exception:u.log_error(traceback.format_exc());raise
finally:u.SystemLibrary.quit_editor()
