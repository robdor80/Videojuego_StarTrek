import json,hashlib,zipfile,shutil,csv,re,datetime,collections,sys
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
rows=read('DATOS/inventario_puertas_accesos.json');errors=[]
assert len(rows)==len(set(x['id'] for x in rows))==187
for x in rows:
 for k in ['capture','context_capture']:
  if not (R/x[k]).is_file():errors.append('missing '+x[k])
with (R/'DATOS/inventario_puertas_accesos.csv').open(encoding='utf-8-sig',newline='') as f:csvrows=list(csv.DictReader(f))
assert [x['id'] for x in rows]==[x['id'] for x in csvrows]
for x,c in zip(rows,csvrows):
 assert x['dimensional_group']==c['dimensional_group']
images=[]
for p in (R/'CAPTURAS').glob('*'):
 if p.suffix.lower() not in ['.png','.jpg']:continue
 with Image.open(p) as im:im.verify()
 images.append(dict(path=str(p.relative_to(R)),bytes=p.stat().st_size))
broken=[]
for p in list((R/'INFORMES').glob('*.md'))+[R/'README.md',R/'GALERIA.html']:
 content=p.read_text(encoding='utf8');links=re.findall(r'\]\(([^)]+)\)',content)+re.findall(r'(?:src|href)="([^"]+)"',content)
 for link in links:
  if '://' in link or link.startswith('#'):continue
  dest=(p.parent/link.split('#')[0]).resolve()
  if not dest.exists():broken.append(dict(file=str(p.relative_to(R)),link=link))
assert not broken,broken
assert not errors,errors
readback=read('VERIFICACION/escenas_readback.json');assert all(x['ok'] for x in readback)
integrity=[]
for name in ['originales_antes.json','referencias_antes.json']:
 for x in read('VERIFICACION/'+name):
  p=Path(x['path']);h=sha(p);s=p.stat();integrity.append(dict(path=str(p),sha256_before=x['sha256'],sha256_after=h,bytes=s.st_size,bytes_equal=h==x['sha256'],metadata_equal=(s.st_mtime_ns==x['mtime_ns'] and s.st_size==x['bytes']) if 'mtime_ns' in x else None))
assert all(x['bytes_equal'] for x in integrity)
(R/'VERIFICACION/integridad_final.json').write_text(json.dumps(dict(checked_at=datetime.datetime.now().astimezone().isoformat(),files=integrity,all_bytes_equal=True),indent=2,ensure_ascii=False),encoding='utf8')
valid=dict(ids=len(rows),csv_rows=len(csvrows),reports=len(list((R/'INFORMES').glob('*.md'))),images=len(images),images_bytes=sum(x['bytes'] for x in images),capture_refs_complete=True,broken_links=broken,scenes_ok=True,original_and_reference_hashes_checked=len(integrity),all_original_bytes_equal=True,ok=True)
(R/'VERIFICACION/validacion_local.json').write_text(json.dumps(valid,indent=2),encoding='utf8')
(R/'DATOS/capturas_archivos.json').write_text(json.dumps(images,indent=2),encoding='utf8')
# Hash manifest before ZIP creation. Self and future remote manifests are excluded by design.
files=[]
for folder in ['INFORMES','DATOS','SCRIPTS','REFERENCIAS','CAPTURAS']:
 files.extend(p for p in (R/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
files.extend([R/'README.md',R/'GALERIA.html']);files.extend(R/'ESCENAS'/f'VOY05A_{s}_Revision.blend' for s in ['coleccion','puente_obj']);files.extend(p for p in (R/'VERIFICACION').glob('*.json') if p.name not in ['entrega_manifest.json','paquetes_validacion.json'])
manifest=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(set(files))]
(R/'VERIFICACION/entrega_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
def chunks(paths,limit=88*1024*1024):
 bins=[];bucket=[];total=0
 for p in paths:
  if bucket and total+p.stat().st_size>limit:bins.append(bucket);bucket=[];total=0
  assert p.stat().st_size<99*1024*1024
  bucket.append(p);total+=p.stat().st_size
 if bucket:bins.append(bucket)
 return bins
groups=[]
docs=[p for folder in ['INFORMES','DATOS','SCRIPTS','REFERENCIAS','VERIFICACION'] for p in (R/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name not in ['paquetes_validacion.json']]+[R/'README.md',R/'GALERIA.html']
groups.append(('VOY05A_01_Informes_Datos_Scripts',docs))
for i,group in enumerate(chunks(sorted(R/p['path'] for p in images)),1):groups.append((f'VOY05A_02_{i:02}_Capturas',group))
groups.append(('VOY05A_03_Escenas_Auditoria',[R/'ESCENAS'/f'VOY05A_{s}_Revision.blend' for s in ['coleccion','puente_obj']]))
sources=sorted(p for p in (R/'FUENTES').rglob('*') if p.is_file())
for i,group in enumerate(chunks(sources),1):groups.append((f'VOY05A_04_{i:02}_Fuentes_Reproduccion',group))
results=[]
for name,paths in groups:
 p=R/'PAQUETE'/f'{name}.zip'
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for src in paths:z.write(src,src.relative_to(R).as_posix())
 assert p.stat().st_size<100*1024*1024
 verify=R/'VERIFICACION'/'EXTRACCION'/name;verify.mkdir(parents=True,exist_ok=True)
 checks=[]
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None;names=z.namelist();assert len(names)==len(set(names));assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names);z.extractall(verify)
  for src in paths:
   rel=src.relative_to(R);dest=verify/rel;checks.append(dict(path=rel.as_posix(),sha256=sha(src),extracted_equal=sha(src)==sha(dest)))
 assert all(x['extracted_equal'] for x in checks)
 results.append(dict(name=p.name,path=str(p),bytes=p.stat().st_size,sha256=sha(p),md5=hashlib.md5(p.read_bytes()).hexdigest(),members=checks,crc_ok=True,extraction_ok=True,under_100MiB=True))
(R/'VERIFICACION/paquetes_validacion.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf8')
(R/'PAQUETE/VOY05A_Paquetes_SHA256.txt').write_text('\n'.join(x['sha256']+'  '+x['name'] for x in results)+'\n',encoding='utf8')
print(json.dumps(valid,indent=2));print([(x['name'],round(x['bytes']/1048576,2),len(x['members'])) for x in results])
