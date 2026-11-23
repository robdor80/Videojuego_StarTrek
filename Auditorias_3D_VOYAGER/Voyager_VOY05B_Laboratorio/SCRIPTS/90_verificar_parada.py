"""Read-only checkpoint validation; writes only verification outputs in this lab."""
import json,hashlib,ast,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1]
A=R.parent/'Voyager_VOY05A_Laboratorio'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def verify(rows):
 out=[]
 for x in rows:
  p=Path(x['path']);actual=sha(p) if p.is_file() else None
  out.append(dict(path=str(p),expected=x['sha256'],actual=actual,ok=actual==x['sha256']))
 return out
baseline=json.loads((R/'VERIFICACION/VOY05A_inicio.json').read_text(encoding='utf8'))
old=json.loads((A/'VERIFICACION/originales_antes.json').read_text(encoding='utf8'))
originals=verify(old);prior=verify(baseline)
parsed=[]
for p in sorted((R/'DATOS').glob('*.json')):
 data=json.loads(p.read_text(encoding='utf8'));parsed.append(dict(file=str(p.relative_to(R)),bytes=p.stat().st_size,records=len(data),ok=True))
scripts=[]
for p in sorted((R/'SCRIPTS').glob('*.py')):
 ast.parse(p.read_text(encoding='utf8'));scripts.append(dict(file=str(p.relative_to(R)),syntax_ok=True))
copies=[]
for folder in ['INFORMES','DATOS','REFERENCIAS']:
 for p in (R/'FUENTES/VOY05A'/folder).rglob('*'):
  if p.is_file():
   src=A/folder/p.relative_to(R/'FUENTES/VOY05A'/folder)
   copies.append(dict(file=str(p.relative_to(R)),ok=sha(p)==sha(src)))
for p in (R/'FUENTES/PUENTE').rglob('*'):
 if p.is_file():
  src=A/'FUENTES/PUENTE'/p.relative_to(R/'FUENTES/PUENTE')
  copies.append(dict(file=str(p.relative_to(R)),ok=sha(p)==sha(src)))
for p in (R/'FUENTES').glob('*.blend'):
 copies.append(dict(file=str(p.relative_to(R)),ok=sha(p)==sha(A/'ESCENAS'/p.name)))
dump=dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),originals=originals,VOY05A=prior,parsed_json=parsed,scripts=scripts,copies=copies,all_ok=all(x['ok'] for x in originals+prior+copies))
(R/'VERIFICACION/parada_integridad.json').write_text(json.dumps(dump,indent=2),encoding='utf8')
assert dump['all_ok']
print(json.dumps(dict(all_ok=dump['all_ok'],originals=len(originals),VOY05A_files=len(prior),copies=len(copies),parsed_json=len(parsed),scripts=len(scripts)),indent=2))
