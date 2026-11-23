import json, hashlib, shutil, datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1]
A=R.parent/'Voyager_VOY05A_Laboratorio'
for d in ['INFORMES','DATOS','CAPTURAS','ESCENAS','SCRIPTS','FUENTES','VERIFICACION','LOGS','PAQUETES']:(R/d).mkdir(parents=True,exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def check(rows):
 out=[]
 for x in rows:
  p=Path(x['path']);actual=sha(p) if p.is_file() else None
  out.append(dict(path=str(p),expected=x['sha256'],actual=actual,ok=actual==x['sha256']))
 return out
old=json.loads((A/'VERIFICACION/originales_antes.json').read_text(encoding='utf8'))
checks=check(old)
(R/'VERIFICACION/originales_inicio.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
assert all(x['ok'] for x in checks),'Originales distintos de baseline A; revisar'
baseline=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(A.rglob('*')) if p.is_file()]
(R/'VERIFICACION/VOY05A_inicio.json').write_text(json.dumps(baseline,indent=2),encoding='utf8')
for folder in ['INFORMES','DATOS','REFERENCIAS']:
 dst=R/'FUENTES'/'VOY05A'/folder
 if not dst.exists():shutil.copytree(A/folder,dst)
for name in ['VOY05A_Puente_Original_Inspeccion.blend','VOY05A_Coleccion_Original_Inspeccion.blend']:
 shutil.copy2(A/'ESCENAS'/name,R/'FUENTES'/name)
shutil.copytree(A/'FUENTES/PUENTE',R/'FUENTES/PUENTE',dirs_exist_ok=True)
print(json.dumps(dict(originales=len(checks),originales_ok=all(x['ok'] for x in checks),archivos_A=len(baseline)),indent=2))
