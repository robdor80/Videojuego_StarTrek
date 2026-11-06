import csv,json,hashlib,shutil,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1];V2=R.parent/'Voyager_VOY02_Laboratorio';V1=R.parent/'Voyager_Puente_2026-10-21'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
for d in ['DATOS','ESCENAS','REFERENCIAS/VOY02','CAPTURAS','LAMINAS','LOGS','PAQUETE']: (R/d).mkdir(parents=True,exist_ok=True)
out=R/'DATOS/baseline_protegido.json';assert not out.exists(),'Baseline exists; do not replace'
rows=[]
for label,root in [('VOY01',V1),('VOY02',V2)]:
 for p in sorted(root.rglob('*')):
  if p.is_file():rows.append(dict(group=label,path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
original=json.loads((V2/'DATOS/entradas_antes.json').read_text())
for x in original:
 p=Path(x['source']);h=sha(p);assert h==x['sha256'],str(p);rows.append(dict(group='ORIGINAL_REGISTRADO',path=str(p),bytes=p.stat().st_size,sha256=h))
copies=[]
needed=['obj_geometria.npz','obj_objetos.json','prototipo_geometria.npz','prototipo_conjunto.json','puertas_medidas.json','acceso_central_revision.json','ergonomia_detallada.json','puestos_revision.json','secciones_niveles.csv','pruebas_rutas.csv','transitos_puente.json','contraste_blend.json','escenas_manifest.json']
for n in needed:
 src=V2/'DATOS'/n;dest=R/'DATOS'/n;assert not dest.exists();shutil.copy2(src,dest);assert sha(src)==sha(dest);copies.append(dict(source=str(src),copy=str(dest),sha256=sha(src)))
for src in sorted(V2.glob('*.md'))+[V2/'SCRIPTS/17_acceso_central.py',V2/'SCRIPTS/geom.py',V2/'ESCENAS/VOY02_Laboratorio.blend']:
 dest=R/'REFERENCIAS/VOY02'/src.name;assert not dest.exists();shutil.copy2(src,dest);copies.append(dict(source=str(src),copy=str(dest),sha256=sha(dest)))
shutil.copy2(V2/'SCRIPTS/geom.py',R/'SCRIPTS/geom.py')
out.write_text(json.dumps(dict(time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),protected=rows,reference_copies=copies,source_blend_expected=json.loads((V2/'DATOS/estado_final.json').read_text())['blend']['sha256']),indent=2,ensure_ascii=False),encoding='utf8')
assert sha(R/'REFERENCIAS/VOY02/VOY02_Laboratorio.blend')==json.loads((V2/'DATOS/estado_final.json').read_text())['blend']['sha256']
print('BASELINE',len(rows),'COPY_FILES',len(copies),'VOY02_BLEND_MATCH',True,flush=True)
