import json,hashlib,shutil,datetime,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]; A=R.parent; V2=A/'Voyager_VOY02_Laboratorio';V3=A/'Voyager_VOY03_Laboratorio'
for d in ['DATOS','ESCENAS','REFERENCIAS','CAPTURAS','ANIMACIONES','LOGS','PAQUETE']:(R/d).mkdir(exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
if __name__=='__main__':
 assert not (R/'DATOS/baseline.json').exists(),'No sobrescribir baseline'
 roots=[A/'Voyager_Puente_2026-10-21',V2,V3,Path(r'C:\Users\andro\Documents\StarTrek_3D\F07_Chair_AutoLab'),Path(r'C:\Users\andro\Documents\StarTrek_3D\Sutherland_ChairLab')]
 files=set(p for root in roots for p in root.rglob('*') if p.is_file())
 orig=json.loads((V2/'DATOS/entradas_antes.json').read_text())
 files.update(Path(x['source']) for x in orig)
 baseline=[]
 for p in sorted(files):
  st=p.stat();baseline.append(dict(path=str(p),bytes=st.st_size,mtime_ns=st.st_mtime_ns,sha256=sha(p)))
 (R/'DATOS/baseline.json').write_text(json.dumps(dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),roots=list(map(str,roots)),files=baseline),indent=2),encoding='utf8')
 print('BASELINE',len(baseline),sum(x['bytes'] for x in baseline),flush=True)
 copies=[(V3/'ESCENAS/VOY03_Circulacion.blend',R/'REFERENCIAS/VOY03_Circulacion.blend')]
 for n in ['puestos_revision.json','prototipo_conjunto.json','manifest_blender.json','obj_objetos.json','obj_geometria.npz','puente_abierto.npz']:
  copies.append((V3/'DATOS'/n,R/'REFERENCIAS'/n))
 copies.append((V3/'SCRIPTS/geom.py',R/'SCRIPTS/geom.py'))
 copies.append((roots[3]/'Reports/INFORME_FINAL_F07_CHAIR_01.md',R/'REFERENCIAS/SUTHERLAND_INFORME.md'))
 for root,label in [(V2,'VOY02'),(V3,'VOY03')]:
  for p in root.glob('*.md'):copies.append((p,R/'REFERENCIAS'/f'{label}_{p.name}'))
 for p,q in copies:shutil.copy2(p,q);assert sha(p)==sha(q)
 (R/'DATOS/copias.json').write_text(json.dumps([dict(source=str(p),copy=str(q),sha256=sha(q)) for p,q in copies],indent=2),encoding='utf8')
 print('COPIAS',len(copies),flush=True)
