"""Read-only recovery audit; writes a new report, never rewrites the stop baseline."""
import csv, datetime, hashlib, json, zipfile
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
rows=list(csv.DictReader((R/'TRASPASO/INVENTARIO_ARCHIVOS.csv').open(encoding='utf-8-sig')))
inventory=[dict(path=x['relative_path'],exists=(R/x['relative_path']).is_file(),matches=(R/x['relative_path']).is_file() and sha(R/x['relative_path'])==x['sha256']) for x in rows]
base=json.loads((R/'DATOS/entradas_antes.json').read_text())
sources=[dict(source=x['source'],matches=Path(x['source']).is_file() and sha(Path(x['source']))==x['sha256'],copy_matches=not x.get('copy') or (Path(x['copy']).is_file() and sha(Path(x['copy']))==x['sha256'])) for x in base]
formats=[]
for p in list((R/'DATOS').glob('*'))+list((R/'CAPTURAS').glob('*.png')):
 if p.suffix not in ('.json','.npz','.png'):continue
 try:
  if p.suffix=='.json':json.loads(p.read_text())
  elif p.suffix=='.npz':
   with zipfile.ZipFile(p) as z:assert z.testzip() is None
  else:
   with Image.open(p) as im:im.verify()
  formats.append(dict(path=p.relative_to(R).as_posix(),readable=True))
 except Exception as e:formats.append(dict(path=str(p),readable=False,error=str(e)))
result=dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(),baseline='TRASPASO/INVENTARIO_ARCHIVOS.csv (unchanged)',inventory=inventory,sources=sources,formats=formats,all_inventory_match=all(x['matches'] for x in inventory),all_originals_match=all(x['matches'] for x in sources),all_copies_match=all(x['copy_matches'] for x in sources))
assert all(result[k] for k in ['all_inventory_match','all_originals_match','all_copies_match'])
(R/'DATOS/reanudacion_integridad.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
# Preserve the render revision being superseded; no source meshes or blend duplicated.
archive=R/'TRASPASO/CAPTURAS_Y_SCRIPT_ANTES_CORRECCION.zip'
if not archive.exists():
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in [R/'SCRIPTS/12_capturas.py',R/'DATOS/capturas_manifest.json']+list((R/'CAPTURAS').glob('*.png')):z.write(p,p.relative_to(R).as_posix())
print(json.dumps({k:v for k,v in result.items() if k.startswith('all_')}),'files',len(inventory),'sources',len(sources),'formats',len(formats),flush=True)
