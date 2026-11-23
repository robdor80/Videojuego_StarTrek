# Permanent authoring recipe for a NEW copy; all evidence is explicitly external.
import os,json,traceback
from pathlib import Path
import unreal as u
SOURCE='/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional'
TARGET='/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Corregida'

def main():
 out=Path(os.environ['VH_EVIDENCE_DIR']).resolve();out.mkdir(parents=True,exist_ok=False)
 result={'ok':False}
 try:
  assert not u.EditorAssetLibrary.does_asset_exist(TARGET),'Never overwrite a corrected delivery'
  w=u.EditorLoadingAndSavingUtils.load_map(SOURCE);actors=u.get_editor_subsystem(u.EditorActorSubsystem)
  assert u.EditorLoadingAndSavingUtils.save_map(w,TARGET)
  inner_path=os.environ['VH_INNER_DOORS_MANIFEST'];pockets_path=os.environ['VH_INNER_POCKETS_MANIFEST']
  inner=json.loads(Path(inner_path).read_text());pockets=json.loads(Path(pockets_path).read_text())
  assert len(inner['doors'])==8 and all(r['surface_area_error_cm2']<.01 for r in inner['doors'])
  direct=[]
  for r in pockets['direct_replacements']:
   source=r['source'];found=[a for a in actors.get_all_level_actors() if a.get_name()==source['actor']];assert len(found)==1
   actor=found[0];component=actor.get_component_by_class(u.StaticMeshComponent)
   assert component.static_mesh.get_path_name()==source['mesh']
   location=actor.get_actor_location();scale=actor.get_actor_scale3d();rotation=actor.get_actor_rotation()
   assert all(abs(v)<.000001 for v in (location.x,location.y,location.z))
   assert all(abs(v-1)<.000001 for v in (scale.x,scale.y,scale.z))
   assert abs(rotation.yaw)+abs(rotation.roll)+abs(rotation.pitch)<.000001
   direct.append((actor,r['target']))
  result['doors']=json.loads(u.VHAutomaticDoorTools.build_door_extensions(inner_path));assert result['doors']['ok']
  result['pockets']=json.loads(u.VHAutomaticDoorTools.build_v07_completion(pockets_path));assert result['pockets']['ok']
  for actor,target in direct:
   generated=[a for a in actors.get_all_level_actors() if a.get_actor_label()==target];assert len(generated)==1
   actor.static_mesh_component.set_static_mesh(generated[0].static_mesh_component.static_mesh)
   actors.destroy_actor(generated[0])
  for door in actors.get_all_level_actors():
   if not isinstance(door,u.VHAutomaticDoor):continue
   identity=str(door.door_id)
   if identity.startswith('MEM_'):
    door.set_editor_property('left_clearance_offset',u.Vector());door.set_editor_property('right_clearance_offset',u.Vector())
   if identity.startswith(('MEM_','V07_SRV_')):
    door.set_editor_property('proximity_depth',600.);door.set_editor_property('use_passage_intent',True)
    if identity.startswith('V07_SRV_'):door.set_editor_property('path_clearance',1.)
    door.set_destination_constructed(True);door.set_security_locked(False);door.set_external_access_allowed(True);door.reset_closed()
  cube=u.load_asset('/Engine/BasicShapes/Cube');blue=u.load_asset('/Game/Valhalla/Materials/M_061');white=u.load_asset('/Game/Valhalla/Materials/M_099')
  for identity,x,y,yaw,width in [('B10_R1_Extremo_Radial',2268.4833,-2485.,90,102),('B11_R2_Extremo_Radial',2268.4833,2979.75,90,102),('B12_R2_Extremo_Este',3318.,1926.18515,0,160)]:
   a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x,y,37+332.635/2),u.Rotator(yaw=yaw));a.set_actor_label('V07C_'+identity+' - limite de cubierta construida');a.set_editor_property('tags',[u.Name('V07C_SAFE_TERMINAL'),u.Name(identity)]);a.static_mesh_component.set_static_mesh(cube);a.static_mesh_component.set_material(0,blue);a.static_mesh_component.set_collision_profile_name('BlockAll');a.set_actor_scale3d(u.Vector(.08,width/100,3.32635))
  for identity,x,y,sx,sy in [('B10',2268.4833,-2475.5,1.02,.31),('B11',2268.4833,2970.25,1.02,.31),('B12',3312.,1926.18515,.28,1.6)]:
   a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x,y,33));a.set_actor_label('V07C_'+identity+'_Relleno_de_junta_terminal');a.set_editor_property('tags',[u.Name('V07C_SAFE_TERMINAL')]);a.static_mesh_component.set_static_mesh(cube);a.static_mesh_component.set_material(0,white);a.static_mesh_component.set_collision_profile_name('BlockAll');a.set_actor_scale3d(u.Vector(sx,sy,.08))
  assert u.EditorLoadingAndSavingUtils.save_map(w,TARGET)
  result['map_check']=json.loads(u.VH06Tools.map_check_snapshot());assert result['map_check']['errors']==0 and result['map_check']['warnings']==0
  result['ok']=True
 except Exception:result['error']=traceback.format_exc();u.log_error(result['error'])
 (out/'author_correction.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 u.SystemLibrary.quit_editor()
if __name__=='__main__':main()
