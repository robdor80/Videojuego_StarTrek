"""UE editor: reopen, test ten mechanisms and sample floors/ceilings/passages.

VH_EVIDENCE_DIR must name a new directory. Tests do not save policy changes.
"""
import json
import os
import traceback
from collections import deque
from pathlib import Path
import unreal as u


def main():
    outdir=Path(os.environ['VH_EVIDENCE_DIR']);outdir.mkdir(parents=True,exist_ok=False)
    out={'ok':False}
    try:
        world=u.EditorLoadingAndSavingUtils.load_map('/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional')
        u.VH06Tools.finish_compilation()
        actors=u.get_editor_subsystem(u.EditorActorSubsystem)
        doors=[a for a in actors.get_all_level_actors() if isinstance(a,u.VHAutomaticDoor)]
        out['doors']=[]
        for door in doors:
            policy=[door.destination_constructed,door.security_locked,door.external_access_allowed]
            try:
                door.set_destination_constructed(True);door.set_security_locked(False);door.set_external_access_allowed(True);door.reset_closed()
                checks=json.loads(u.VHAutomaticDoorTools.run_checks(door))
                out['doors'].append(dict(id=str(door.door_id),checks=checks,authored_policy=policy))
            finally:
                door.set_destination_constructed(policy[0]);door.set_security_locked(policy[1]);door.set_external_access_allowed(policy[2]);door.reset_closed()
        out['surfaces']=[];segments=[];rays=[]
        def ray(point,z1,z2,identity):
            rays.append(dict(id=identity,start=[point.x,point.y,point.z+z1],end=[point.x,point.y,point.z+z2]))
        for door in doors:
            if not str(door.door_id).startswith('MEM_'):continue
            transform=door.get_actor_transform()
            # Move both leaves to their real open positions for independent capsule sweeps.
            door.left_leaf.set_relative_location(door.leaf_location_at_fraction(True,1),False,True)
            door.right_leaf.set_relative_location(door.leaf_location_at_fraction(False,1),False,True)
            start=transform.transform_location(u.Vector(-140,0,0))
            end=transform.transform_location(u.Vector(340,0,0))
            segments.append(dict(id=str(door.door_id),start=[start.x,start.y,start.z],end=[end.x,end.y,end.z]))
            for x in (-100,0,80,180,280,340):
                for y in (-45,0,45):
                    p=transform.transform_location(u.Vector(x,y,0))
                    sample=dict(id=str(door.door_id),local=[x,y],hits=[])
                    for ceiling in (False,True):
                        z1,z2=(170,600) if ceiling else (10,-50)
                        identity=f'{door.door_id}_{x}_{y}_{ceiling}'
                        ray(p,z1,z2,identity)
                        sample['hits'].append(dict(ceiling=ceiling,ray_id=identity))
                    out['surfaces'].append(sample)
        plan=json.loads(Path(__file__).with_name('v07_validation_plan.json').read_text())
        for case in plan['cases']:
            if not case['name'].startswith(('ruta_','escalera_')):continue
            for index,pos in enumerate([case['start']]+case['points']):
                ray(u.Vector(*pos),180,1200,f'main_{case["name"]}_{index}')
        traces=json.loads(u.VHAutomaticDoorTools.trace_v07_surfaces(json.dumps(dict(rays=rays))))['rays']
        indexed={r['id']:r for r in traces}
        out['main_headroom']=[r for r in traces if r['id'].startswith('main_')]
        connected={r['id'] for r in json.loads(Path(__file__).with_name('v07_memory_accesses.json').read_text(encoding='utf-8-sig')) if r.get('connects_existing_corridor',False)}
        for sample in out['surfaces']:
            for hit in sample['hits']:
                result=indexed[hit['ray_id']]
                hit.update(result)
                clearance=200 if sample['id'] in connected and sample['local'][0]>200 else 225
                hit['ok']=result['hit'] and (result['z']>=37+clearance if hit['ceiling'] else abs(result['z']-37)<.1)
            sample['ok']=all(h['ok'] for h in sample['hits'])
        out['passages']=json.loads(u.VH06Tools.probe_segments(json.dumps(dict(segments=segments))))
        barriers=[]
        for identity,x,y,z in [('B08',3353.18,-60,37),('B09',3353.18,561.15857,-305.635)]:
            for dx in (-10,0,10):
                for side in (-1,1):
                    barriers.append(dict(id=identity,dx=dx,side=side,start=[x+dx,y+100*side,z],end=[x+dx,y-100*side,z]))
        out['safety_barriers']=json.loads(u.VH06Tools.probe_segments(json.dumps(dict(segments=barriers))))['segments']
        for d in doors:d.reset_closed()
        out['map_check']=json.loads(u.VH06Tools.map_check_snapshot())
        out['materials']=json.loads(u.VH06Tools.material_resource_snapshot())
        directions=[a.get_component_by_class(u.DirectionalLightComponent) for a in actors.get_all_level_actors() if isinstance(a,u.DirectionalLight)]
        out['directional_priorities']=[dict(intensity=c.get_editor_property('intensity'),priority=c.get_editor_property('forward_shading_priority')) for c in directions]
        top=max(r['priority'] for r in out['directional_priorities'])
        out['primary_directional_unique']=sum(r['priority']==top for r in out['directional_priorities'])==1
        out['service_light_count']=sum('V07_COMPLETION_LIGHT' in [str(t) for t in a.tags] for a in actors.get_all_level_actors())
        winding=json.loads(u.VH06Tools.audit_winding())
        out['new_surface_winding']=[r for r in winding['meshes'] if '/Completion/' in r['mesh'] and not r['mesh'].split('.')[-1].endswith('_Architecture')]
        registry=u.AssetRegistryHelpers.get_asset_registry();registry.scan_paths_synchronous(['/Game'],True)
        options=u.AssetRegistryDependencyOptions(include_soft_package_references=True,include_hard_package_references=True,
            include_searchable_names=False,include_soft_management_references=False,include_hard_management_references=False)
        queue=deque(['/Game/ValhallaV07/Maps/L_Supercomputadora_V07_Funcional']);seen=set()
        while queue:
            name=queue.popleft()
            if name in seen or not name.startswith('/Game/'):continue
            seen.add(name);queue.extend(str(x) for x in registry.get_dependencies(name,options))
        content=Path(u.Paths.project_content_dir())
        out['missing_packages']=[]
        for name in sorted(seen):
            path=content/name.removeprefix('/Game/')
            if not path.with_suffix('.uasset').is_file() and not path.with_suffix('.umap').is_file():out['missing_packages'].append(name)
        out['package_count']=len(seen)
        out['test_package_dependencies']=[n for n in seen if n.startswith('/Game/VH07Test/')]
        out['ok']=(len(doors)==10 and all(d['checks']['all_pass'] for d in out['doors'])
                   and all(s['ok'] for s in out['surfaces'])
                   and all(not s['blocked'] for s in out['passages']['segments'])
                   and all(r['hit'] for r in out['main_headroom'])
                   and out['map_check']['errors']==0 and out['map_check']['warnings']==0
                   and out['materials'].get('ok',False))
        out['ok'] &= not out['missing_packages'] and not out['test_package_dependencies']
        out['ok'] &= all(r['cross_dot_normal_positive']==0 for r in out['new_surface_winding'])
        out['ok'] &= all(r['blocked'] and not r['penetrating'] for r in out['safety_barriers'])
        out['ok'] &= out['primary_directional_unique'] and out['service_light_count']==4
    except Exception:
        out['error']=traceback.format_exc();u.log_error(out['error'])
    finally:
        (outdir/'check_completion.json').write_text(json.dumps(out,indent=2),encoding='utf8')
        u.SystemLibrary.quit_editor()


if __name__=='__main__':main()
