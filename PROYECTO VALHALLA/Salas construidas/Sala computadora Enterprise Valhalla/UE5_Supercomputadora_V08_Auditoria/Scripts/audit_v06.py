"""UE Python: reopen V06, audit actual RHI resources and list independent packages.
Use VH_EVIDENCE_DIR with a new authorized empty directory. NullRHI is not valid.
"""
import collections,json,os
from pathlib import Path
import unreal as u

outdir=Path(os.environ['VH_EVIDENCE_DIR']).resolve()
if outdir.exists() and any(outdir.iterdir()):raise RuntimeError('Use new empty evidence directory')
outdir.mkdir(parents=True,exist_ok=True)
try:
    w=u.EditorLoadingAndSavingUtils.load_map('/Game/Valhalla/Maps/L_Supercomputadora_V06_Quinn');u.VH06Tools.finish_compilation()
    actors=u.get_editor_subsystem(u.EditorActorSubsystem)
    out={'map_check':json.loads(u.VH06Tools.map_check_snapshot()),'material_resources':json.loads(u.VH06Tools.material_resource_snapshot()),'winding':json.loads(u.VH06Tools.audit_winding()),'world_game_mode':w.get_world_settings().get_editor_property('default_game_mode').get_path_name()}
    out['static_instances']=sum(c.get_instance_count() for a in actors.get_all_level_actors() for c in a.get_components_by_class(u.InstancedStaticMeshComponent))
    out['boundaries']=[a.get_actor_label() for a in actors.get_all_level_actors() if 'V06_VISIBLE_BOUNDARY' in [str(t) for t in a.tags]]
    out['technical_lights_and_exposure']=[a.get_actor_label() for a in actors.get_all_level_actors() if 'V06_PROVISIONAL_LIGHT' in [str(t) for t in a.tags]]
    reg=u.AssetRegistryHelpers.get_asset_registry();reg.scan_paths_synchronous(['/Game'],True)
    opts=u.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True,include_searchable_names=False,include_soft_management_references=False,include_hard_management_references=False)
    roots=['/Game/Valhalla/Maps/L_Supercomputadora_V06_Quinn']+[x.split('.')[0] for x in u.EditorAssetLibrary.list_assets('/Game/Valhalla/Meshes',True,False)]+[x.split('.')[0] for x in u.EditorAssetLibrary.list_assets('/Game/Valhalla/Materials',True,False)]
    queue=collections.deque(roots);seen=set()
    while queue:
        key=queue.popleft()
        if key in seen or not key.startswith('/Game/'):continue
        seen.add(key)
        for dep in reg.get_dependencies(key,opts):
            name=str(dep)
            if name.startswith('/Game/') and name not in seen:queue.append(name)
    content=Path(u.Paths.project_content_dir());missing=[]
    for package in sorted(seen):
        f=content/package.removeprefix('/Game/')
        if not f.with_suffix('.uasset').is_file() and not f.with_suffix('.umap').is_file():missing.append(package)
    out['asset_packages']=sorted(seen);out['missing_game_packages']=missing
    out['ok']=out['map_check']['errors']==0 and out['map_check']['warnings']==0 and out['map_check']['materials_missing_flag']==0 and out['material_resources'].get('ok',False) and not missing and out['static_instances']==16302 and len(out['boundaries'])==14
    (outdir/'audit_v06.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    if not out['ok']:raise RuntimeError('V06 audit failed; inspect audit_v06.json')
finally:u.SystemLibrary.quit_editor()
