from pathlib import Path
import hashlib,json,ast,struct
R=Path(__file__).resolve().parents[1];D=R/'Data';out={'ok':False,'date':'2026-10-28 Europe/Madrid','errors':[],'source_files_checked':0,'working_files_checked':0,'derived_assets_checked':0,'blend_files_checked':0}
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def check(p,h,category):
 if not p.is_file():out['errors'].append({'category':category,'path':str(p),'error':'missing'});return
 if sha(p)!=h:out['errors'].append({'category':category,'path':str(p),'error':'hash mismatch'})
 if p.suffix.lower() in ['.uasset','.umap']:
  with p.open('rb') as f:assert struct.unpack('<I',f.read(4))[0]==0x9e2a83c1,('Invalid package tag',str(p))
previous=read(D/'final_integrity.json');source=Path(read(D/'copy_verified.json')['source'])/'Unreal';manifest=read(D/'copy_manifest.json')
for row in manifest:
 check(source/row['path'],row['sha256'],'original_project');out['source_files_checked']+=1
 if row['path'].split('/')[0] not in ['Saved','Intermediate','DerivedDataCache'] and '/Intermediate/' not in row['path']:
  if row['path']=='Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap':continue
  check(R/'Unreal'/row['path'],row['sha256'],'working_original_asset');out['working_files_checked']+=1
for row in previous['derived_assets']:
 check(R/row['path'],row['sha256'],'derived_asset');out['derived_assets_checked']+=1
for p,h in read(D/'original_blend_hashes.json').items():check(Path(p),h,'original_blend');out['blend_files_checked']+=1
mp=R/'Unreal/Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap';check(mp,previous['saved_map_sha256'],'saved_map');out['recovered_map_sha256']=sha(mp)
check(R/'Backups/L_Sutherland_Ergonomia03_Bloqueo_D04.umap',previous['saved_map_sha256'],'recovery_map')
out['json_files_checked']=[]
for p in D.glob('*.json'):
 try:read(p);out['json_files_checked'].append(p.name)
 except Exception as e:out['errors'].append({'path':str(p),'error':str(e)})
for p in (R/'Scripts').glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
out['ok']=not out['errors'];(D/'resume_20261028_integrity.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out),flush=True)
assert out['ok'],'Recover state before launching editor'
