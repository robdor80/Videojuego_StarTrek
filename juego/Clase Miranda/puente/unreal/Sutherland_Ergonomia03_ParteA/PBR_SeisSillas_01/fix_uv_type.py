import unreal as u,pathlib,json,shutil,traceback
R=pathlib.Path(__file__).parent;P=R.parent/'Unreal';E=u.EditorAssetLibrary;out={'ok':False,'changed':[]}
try:
    plan=json.loads((R/'export.json').read_text(encoding='utf-8'))
    for recipe in plan['materials'].values():
        path='/Game/SutherlandPBR01/Materials/'+recipe['name'];mat=E.load_asset(path);assert mat
        matches=[]
        for i in range(64):
            n=u.find_object(None,mat.get_path_name()+':MaterialExpressionCustom_'+str(i))
            if not n:continue
            code=n.get_editor_property('code')
            if code.startswith('return float3(UV.x'):
                matches.append(n)
        if not matches:continue
        original=P/('Content/SutherlandPBR01/Materials/'+recipe['name']+'.uasset');backup=R/'Backups/Materiales_AntesCorreccionUV'/original.name;backup.parent.mkdir(exist_ok=True);assert not backup.exists();shutil.copy2(original,backup)
        for n in matches:
            code=n.get_editor_property('code').replace('float3(UV.x','float2(UV.x').replace(',0);',');');n.set_editor_property('code',code);n.set_editor_property('output_type',u.CustomMaterialOutputType.CMOT_FLOAT2)
        u.MaterialEditingLibrary.recompile_material(mat);E.save_loaded_asset(mat);out['changed'].append({'asset':path,'uv_nodes':len(matches)})
    assert out['changed'];out['ok']=True
except Exception:out['error']=traceback.format_exc();u.log_error(out['error'])
(R/'uv_repair.json').write_text(json.dumps(out,indent=2));print('UV_REPAIR',out['ok'],out.get('error'));u.SystemLibrary.quit_editor()
