import unreal as u,json,pathlib,traceback
R=pathlib.Path(__file__).parent
out={'ok':False}
try:
    A=u.get_editor_subsystem(u.EditorActorSubsystem);L=u.get_editor_subsystem(u.LevelEditorSubsystem)
    assert L.load_level('/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01')
    out['actors']=[]
    for a in A.get_all_level_actors():
        row={'label':a.get_actor_label(),'class':a.get_class().get_name(),'position':list(a.get_actor_location().to_tuple()),'components':[]}
        for c in a.get_components_by_class(u.StaticMeshComponent):
            row['components'].append({'name':c.get_name(),'mesh':c.static_mesh.get_path_name() if c.static_mesh else None,'visible':c.is_visible(),'collision':str(c.get_collision_enabled()),'materials':[m.get_name() if m else None for m in c.get_materials()]})
        out['actors'].append(row)
    out['api']={n:str(getattr(u,n).__doc__)[:12000] for n in ['InterchangeManager','InterchangeGenericAssetsPipeline','InterchangeGenericMeshPipeline','InterchangeGenericScenesPipeline','RectLightComponent','MaterialExpressionTextureSample','EditorLevelLibrary'] if hasattr(u,n)}
    out['ok']=True
except Exception:out['error']=traceback.format_exc()
(R/'ue_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('PBR_AUDIT',out['ok'],out.get('error'),flush=True)
u.SystemLibrary.quit_editor()
