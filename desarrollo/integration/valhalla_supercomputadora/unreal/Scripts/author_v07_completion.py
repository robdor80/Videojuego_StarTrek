"""Author a NEW functional V07 map in a copied project, keeping its source map.

VH_COMPLETION_MANIFEST: output of build_v07_memory_geometry.py.
VH_EVIDENCE_DIR: a new empty directory for the result.
"""
import hashlib
import json
import math
import os
import traceback
from pathlib import Path
import unreal as u

SOURCE='/Game/ValhallaV07/Maps/L_Supercomputadora_V07'
TARGET='/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional'


def add_stair_caps(actors):
    """Upper hoods leave every stair tread and vertical connection clear below 379.635."""
    assert not any('V07_STAIR_CAP' in [str(t) for t in a.tags] for a in actors.get_all_level_actors())
    cube=u.load_asset('/Engine/BasicShapes/Cube');white=u.load_asset('/Game/Valhalla/Materials/M_099')
    for north in (False,True):
        lo,hi=(561.16,902.15) if north else (-407.4,-66.41)
        boxes=[((3132,lo,610),(3425,hi,622)),
               ((3128,lo,379.635),(3132,hi,610)),
               ((3425,lo,379.635),(3429,hi,610)),
               ((3132,lo-4,542.3),(3425,lo,610)),
               ((3132,hi,542.3),(3425,hi+4,610))]
        for index,(a,b) in enumerate(boxes):
            pos=[(a[k]+b[k])/2 for k in range(3)]
            actor=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*pos))
            actor.set_actor_label('V07_TechoEscalera_'+('Norte' if north else 'Sur')+'_'+str(index))
            actor.set_editor_property('tags',[u.Name('V07_STAIR_CAP')])
            actor.static_mesh_component.set_static_mesh(cube);actor.static_mesh_component.set_material(0,white)
            actor.static_mesh_component.set_collision_profile_name('BlockAll')
            actor.set_actor_scale3d(u.Vector(*[(b[k]-a[k])/100 for k in range(3)]))


def add_memory_service_lights(actors,doors):
    """Four small technical fills make the enclosed service destinations inspectable."""
    assert not any('V07_COMPLETION_LIGHT' in [str(t) for t in a.tags] for a in actors.get_all_level_actors())
    for row in doors:
        if row['id'] in ('MEM_C03','MEM_C06'):continue
        angle=math.radians(row['yaw']);x,y,z=row['root']
        actor=actors.spawn_actor_from_class(u.PointLight,u.Vector(x+220*math.cos(angle),y+220*math.sin(angle),z+220))
        actor.set_actor_label('V07_TECH_'+row['id']);actor.set_editor_property('tags',[u.Name('V07_COMPLETION_LIGHT')])
        component=actor.get_component_by_class(u.PointLightComponent)
        component.set_mobility(u.ComponentMobility.MOVABLE);component.set_editor_property('intensity_units',u.LightUnits.LUMENS)
        component.set_intensity(600);component.set_attenuation_radius(400);component.set_cast_shadows(False)


def select_primary_directional_light(actors):
    components=[a.get_component_by_class(u.DirectionalLightComponent) for a in actors.get_all_level_actors() if isinstance(a,u.DirectionalLight)]
    if not components:return
    primary=max(components,key=lambda c:c.get_editor_property('intensity'))
    for component in components:component.set_editor_property('forward_shading_priority',1 if component==primary else 0)


def protected(actors):
    def transform(a):
        t=a.get_actor_transform();q=t.rotation
        return [[t.translation.x,t.translation.y,t.translation.z],[q.x,q.y,q.z,q.w],
                [t.scale3d.x,t.scale3d.y,t.scale3d.z]]
    rows=[]
    for a in actors.get_all_level_actors():
        tags=[str(t) for t in a.tags]
        if isinstance(a,u.VHAutomaticDoor) and not str(a.door_id).startswith('MEM_'):
            props={}
            for key in ('door_id','destination_constructed','security_locked','external_access_allowed',
                        'left_closed_location','right_closed_location','left_travel','right_travel',
                        'left_clearance_offset','right_clearance_offset','opening_width','opening_height',
                        'movement_duration','close_delay','travel_distance','use_configured_travel'):
                value=a.get_editor_property(key)
                props[key]=[value.x,value.y,value.z] if isinstance(value,u.Vector) else str(value)
            rows.append([a.get_actor_label(),transform(a),props,
                         a.left_leaf.static_mesh.get_path_name(),a.right_leaf.static_mesh.get_path_name()])
        elif 'V06_VISIBLE_BOUNDARY' in tags or 'V07_CLOSURE_VISIBLE_BOUNDARY' in tags:
            rows.append([a.get_actor_label(),transform(a),
                         a.static_mesh_component.static_mesh.get_path_name(),
                         str(a.static_mesh_component.get_collision_profile_name())])
    return hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest()


def main():
    path=Path(os.environ['VH_EVIDENCE_DIR']).resolve()
    path.mkdir(parents=True,exist_ok=False)
    result={'ok':False}
    try:
        assert not u.EditorAssetLibrary.does_asset_exist(TARGET),'Never overwrite a completed map'
        data=json.loads(Path(os.environ['VH_COMPLETION_MANIFEST']).read_text())
        assert len(data['doors'])==6
        world=u.EditorLoadingAndSavingUtils.load_map(SOURCE)
        u.VH06Tools.finish_compilation()
        actors=u.get_editor_subsystem(u.EditorActorSubsystem)
        before=protected(actors)
        result['geometry']=json.loads(u.VHAutomaticDoorTools.build_v07_completion(os.environ['VH_COMPLETION_MANIFEST']))
        assert result['geometry']['ok'],result['geometry']
        cube=u.load_asset('/Engine/BasicShapes/Cube')
        blue=u.load_asset('/Game/Valhalla/Materials/M_061')
        for row in data['doors']:
            door=actors.spawn_actor_from_class(u.VHAutomaticDoor,u.Vector(*row['root']),u.Rotator(yaw=row['yaw']))
            door.set_actor_label(row['id']+' - acceso de servicio al nucleo')
            door.set_editor_property('tags',[u.Name('V07_COMPLETION_DOOR')])
            door.set_editor_property('door_id',u.Name(row['id']))
            for key,value in dict(opening_width=180.,opening_height=230.,travel_distance=100.,
                                  movement_duration=.8,close_delay=1.5,proximity_depth=180.,
                                  use_configured_travel=True,use_passage_intent=False).items():
                door.set_editor_property(key,value)
            for left,component in ((True,door.left_leaf),(False,door.right_leaf)):
                component.set_static_mesh(cube)
                component.set_material(0,blue)
                component.set_relative_scale3d(u.Vector(.06,.896,2.292))
                prefix='left' if left else 'right'
                door.set_editor_property(prefix+'_closed_location',u.Vector(0,-45 if left else 45,115))
                door.set_editor_property(prefix+'_travel',u.Vector(0,-100 if left else 100,0))
                door.set_editor_property(prefix+'_clearance_offset',u.Vector(-35,0,0))
            door.set_destination_constructed(True);door.set_security_locked(False)
            door.set_external_access_allowed(True);door.reset_closed()
        add_stair_caps(actors)
        add_memory_service_lights(actors,data['doors'])
        select_primary_directional_light(actors)
        after=protected(actors)
        result.update(protected_before=before,protected_after=after)
        assert before==after,'D01-D04 or V06/V07 safety closures changed'
        assert u.EditorLoadingAndSavingUtils.save_map(world,TARGET)
        result['map_check']=json.loads(u.VH06Tools.map_check_snapshot())
        assert result['map_check']['errors']==0 and result['map_check']['warnings']==0
        result.update(ok=True,map=TARGET,metrics=data['metrics'])
    except Exception:
        result['error']=traceback.format_exc();u.log_error(result['error'])
    finally:
        (path/'author_completion.json').write_text(json.dumps(result,indent=2),encoding='utf8')
        u.SystemLibrary.quit_editor()


if __name__=='__main__':main()
