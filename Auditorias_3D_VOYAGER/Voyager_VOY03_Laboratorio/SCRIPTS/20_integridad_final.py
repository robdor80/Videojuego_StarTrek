from pathlib import Path
import json,hashlib,datetime,collections
R=Path(__file__).resolve().parents[1];assert R.name=='Voyager_VOY03_Laboratorio'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
b=json.loads((R/'DATOS/baseline_protegido.json').read_text());rows=[]
for i,x in enumerate(b['protected']):
 p=Path(x['path']);actual=sha(p) if p.is_file() else None;rows.append(dict(group=x['group'],path=x['path'],sha256_before=x['sha256'],sha256_after=actual,unchanged=actual==x['sha256']))
 if i%500==0:print('HASH_PROGRESS',i,len(b['protected']),flush=True)
refs=[]
for x in b['reference_copies']+json.loads((R/'DATOS/copias_visuales_referencia.json').read_text())['copied_relevant_captures']:
 p=Path(x['copy']);h=sha(p);refs.append(dict(path=str(p),expected=x['sha256'],actual=h,unchanged=h==x['sha256']))
result=dict(time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),protected_entries=len(rows),unique_protected_files=len(set(x['path'] for x in rows)),groups=dict(collections.Counter(x['group'] for x in rows)),all_protected_unchanged=all(x['unchanged'] for x in rows),reference_copies_unchanged=all(x['unchanged'] for x in refs),reference_copies=refs,protected=rows,other_projects='No operations were performed on Sutherland, Unreal or CoreRPG. This is not a global disk hash claim.')
(R/'DATOS/integridad_final.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8');print('FINAL_INTEGRITY',result['protected_entries'],result['groups'],result['all_protected_unchanged'],result['reference_copies_unchanged'],flush=True);assert result['all_protected_unchanged'] and result['reference_copies_unchanged']
