"""Only read UE assets/CDOs and export evidence outside the Unreal project."""
import unreal as u,pathlib,json,traceback
R=pathlib.Path(__file__).resolve().parents[1]/'ergonomia_correderas_01';R.mkdir(exist_ok=True)
out={'ok':False,'exports':[]}
try:
 c=u.get_default_object(u.STPlayableQuinn);mesh=c.mesh.get_skeletal_mesh_asset()
 out['capsule']={'radius_cm':c.capsule_component.get_unscaled_capsule_radius(),'half_height_cm':c.capsule_component.get_unscaled_capsule_half_height(),'scale':list(c.capsule_component.get_editor_property('relative_scale3d').to_tuple())}
 out['mesh']={'path':mesh.get_path_name(),'skeleton':mesh.skeleton.get_path_name(),'relative_location':list(c.mesh.get_editor_property('relative_location').to_tuple()),'relative_rotation':list(c.mesh.get_editor_property('relative_rotation').to_tuple()),'relative_scale':list(c.mesh.get_editor_property('relative_scale3d').to_tuple())}
 out['api']={n:str(getattr(u,n).__doc__)[:20000] for n in ['SkeletalMeshExporterFBX','AnimSequenceExporterFBX','FbxExportOption','AnimationLibrary','AnimationBlueprintLibrary'] if hasattr(u,n)}
 for obj,name in [(mesh,'Quinn_Referencia'),(u.load_asset('/Game/SutherlandPlayable01/Animations/A_Captain_Seated_Authored'),'Quinn_PoseSentada_Referencia')]:
  assert obj;task=u.AssetExportTask();task.object=obj;task.filename=str(R/(name+'.fbx'));assert not pathlib.Path(task.filename).exists();task.automated=True;task.prompt=False;task.replace_identical=False
  task.options=u.FbxExportOption();task.options.set_editor_property('export_morph_targets',False)
  out['exports'].append({'object':obj.get_path_name(),'file':task.filename,'ok':u.Exporter.run_asset_export_task(task),'errors':list(task.errors)})
 out['ok']=all(x['ok'] for x in out['exports'])
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(R/'quinn_ue_lectura.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('READ_QUINN',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
