import pathlib,json,hashlib,datetime,shutil
R=pathlib.Path(__file__).parent; P=R.parent/'Unreal'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()
manifest=[]
for folder in ['Content','Config','Source','Plugins','Binaries']:
    for p in sorted((P/folder).rglob('*')):
        if p.is_file():manifest.append({'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
for p in P.glob('*.uproject'):manifest.append({'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
doors=json.loads((R.parent/'Data/doors_20261028_final_integrity.json').read_text())
checks=[{'path':x['path'],'matches':sha(R.parent/x['path'])==x['after']} for x in doors['modified_assets']]
mapfile=P/'Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap'
checks.append({'path':str(mapfile),'matches':sha(mapfile)==doors['map_sha256']})
backup=R/'Backups';backup.mkdir(exist_ok=False)
for p in [mapfile,P/'SutherlandPlayable01.uproject',*list((P/'Config').glob('*.ini'))]:
    d=backup/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);assert sha(p)==sha(d)
out={'time':datetime.datetime.now().astimezone().isoformat(),'historical_checks':checks,'manifest':manifest,'all_historical_checks_pass':all(c['matches'] for c in checks),'previous_pbr_target_exists':(P/'Content/SutherlandPBR01').exists()}
(R/'local_audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('LOCAL_AUDIT',len(manifest),checks,'PBR_EXISTS',out['previous_pbr_target_exists'])
