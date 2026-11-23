import json, hashlib, shutil, zipfile, datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for d in ['INFORMES','DATOS','CAPTURAS','ESCENAS','SCRIPTS','PAQUETE','VERIFICACION','FUENTES','REFERENCIAS','LOGS']:(R/d).mkdir(parents=True,exist_ok=True)
bridge=Path(r'C:\Users\andro\Desktop\Nueva carpeta\TrekmeshesEU_Chainsaw_USSVoyagerBridge_OBJ')
coll=Path(r'C:\Users\andro\Documents\GitHub\3D Star Trek\assets\otros\corridor\Star Trek Voyager Collection\voyager\coleccion_de_pasillos_voyager')
recovery=Path(r'C:\Users\andro\Documents\Voyager_Bridge_Recovery\originales')
old=R.parent/'Voyager_VOY02_Laboratorio'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
sources=[]
for root,label in [(bridge,'PUENTE'),(coll,'COLECCION'),(recovery,'RECOVERY')]:
 for p in sorted(root.rglob('*')):
  if p.is_file():
   s=p.stat();sources.append(dict(path=str(p),group=label,bytes=s.st_size,mtime_ns=s.st_mtime_ns,sha256=sha(p)))
   if p.suffix.lower() in ['.obj','.mtl','.blend','.glb','.jpg','.png','.tga','.tif']:
    dest=R/'FUENTES'/label/p.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():shutil.copy2(p,dest)
    assert sha(dest)==sources[-1]['sha256']
refs=[]
for phase in ['Voyager_Puente_2026-10-21','Voyager_VOY02_Laboratorio','Voyager_VOY03_Laboratorio','Voyager_VOY04_Laboratorio']:
 base=R.parent/phase
 for p in sorted(base.glob('*.md')):
  dest=R/'REFERENCIAS'/phase/p.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);refs.append(dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size))
for p in sorted(Path(r'C:\Users\andro\Documents\StarTrek_3D\F07_P03FG_DoorLab').rglob('*.md')):
 if 'Backups' in p.parts:continue
 dest=R/'REFERENCIAS'/'SUTHERLAND'/p.name;shutil.copy2(p,dest) if dest.parent.exists() else (dest.parent.mkdir(parents=True),shutil.copy2(p,dest));refs.append(dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size))
for name in ['puertas_medidas.json','carreras_investigacion.json','interfaces_modulos.json','clasificacion_modulos.json','correspondencias_max_obj.json']:
 p=old/'DATOS'/name;dest=R/'REFERENCIAS'/name;shutil.copy2(p,dest);refs.append(dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size))
(R/'VERIFICACION/originales_antes.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf8')
(R/'VERIFICACION/referencias_antes.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf8')
print('Fuentes protegidas',len(sources),'Referencias',len(refs),flush=True)
