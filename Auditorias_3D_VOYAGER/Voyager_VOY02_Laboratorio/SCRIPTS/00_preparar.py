import json,hashlib,shutil,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for n in ['FUENTES/OBJ','FUENTES/COLECCION','FUENTES/MAX','REFERENCIAS','DATOS','ESCENAS','CAPTURAS','LOGS','PAQUETE']: (R/n).mkdir(parents=True,exist_ok=True)
V1=R.parent/'Voyager_Puente_2026-10-21';src=Path(r'C:\Users\andro\Desktop\Nueva carpeta\TrekmeshesEU_Chainsaw_USSVoyagerBridge_OBJ');col=Path(r'C:\Users\andro\Documents\GitHub\3D Star Trek\assets\otros\corridor\Star Trek Voyager Collection\voyager\coleccion_de_pasillos_voyager\star-trek-voyager-collection\source\StarTrekVoyagerCollection.blend');mx=Path(r'C:\Users\andro\Documents\Voyager_Bridge_Recovery\originales\Voyager_Bridge_MAX_Trabajo.blend')
inputs=[(src/'Voyager Bridge.obj',R/'FUENTES/OBJ/Voyager Bridge.obj'),(src/'VoyagerB.Mtl',R/'FUENTES/OBJ/VoyagerB.Mtl'),(col,R/'FUENTES/COLECCION/coleccion_original.blend'),(mx,R/'FUENTES/MAX/puente_max_conversion.blend')]
inputs.extend((p,R/'FUENTES/OBJ'/p.relative_to(src)) for p in (src/'VOYBRIDGETEX-1').rglob('*') if p.is_file())
manifest=[]
for s,t in inputs:
 st=s.stat();h=hashlib.sha256(s.read_bytes()).hexdigest();t.parent.mkdir(parents=True,exist_ok=True)
 if not t.exists():shutil.copy2(s,t)
 assert hashlib.sha256(t.read_bytes()).hexdigest()==h
 manifest.append({'source':str(s),'copy':str(t),'bytes':st.st_size,'mtime_ns':st.st_mtime_ns,'sha256':h})
for p in sorted(V1.glob('0[1-9]_*.md')):
 t=R/'REFERENCIAS'/p.name
 if not t.exists():shutil.copy2(p,t)
manifest.extend({'source':str(p),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':'VOY01 report read-only'} for p in sorted(V1.glob('0[1-9]_*.md')))
(R/'DATOS/entradas_antes.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
(R/'REFERENCIAS/PR32.json').write_text(json.dumps({'url':'https://github.com/robdor80/Videojuego_StarTrek/pull/32','read_ref':'docs/voyager-3d-audit','head_sha':'c3a5a0885f39ecdc0d6acaaf7057b6817282efe4','state_at_start':'open / draft / not merged','mode':'read only; no new publication authorized in VOY02'},indent=2),encoding='utf8')
print('COPIAS_VERIFICADAS',len(inputs),'INFORMES_REFERENCIA',9)
