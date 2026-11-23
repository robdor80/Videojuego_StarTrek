import json,hashlib,zipfile,collections,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
manifest=json.loads((R/'VERIFICACION/entrega_manifest.json').read_text())
for x in manifest:
 p=R/x['path'];x['sha256']=sha(p);x['bytes']=p.stat().st_size
(R/'VERIFICACION/entrega_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf8')
# Content-level duplicate check: retain original-path provenance, never delete a source or evidence view.
groups=collections.defaultdict(list)
for x in manifest:groups[x['sha256']].append(x['path'])
duplicates=[dict(sha256=k,paths=v,decision='conservar: misma geometria vista simetrica / documento de fases distintas; no se cuentan como instancias nuevas') for k,v in groups.items() if len(v)>1]
(R/'VERIFICACION/duplicados_contenido.json').write_text(json.dumps(dict(groups=duplicates,accidental_archive_member_names=0,policy='No se borran vistas simetricas ni referencias de diferentes fases; un ID de acceso solo aparece una vez en el inventario'),indent=2,ensure_ascii=False),encoding='utf8')
# Rebuild only package 1 with the reproducible all-view catalogue script, preserving its member list.
zip1=R/'PAQUETE/VOY05A_01_Informes_Datos_Scripts.zip'
with zipfile.ZipFile(zip1) as z:names=z.namelist()
for p in [R/'SCRIPTS/16_cierre_local.py',R/'VERIFICACION/duplicados_contenido.json']:
 if p.relative_to(R).as_posix() not in names:names.append(p.relative_to(R).as_posix())
with zipfile.ZipFile(zip1,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name in names:z.write(R/name,name)
checks=[]
with zipfile.ZipFile(zip1) as z:
 assert z.testzip() is None;assert len(z.namelist())==len(set(z.namelist()));dest=R/'VERIFICACION/EXTRACCION/VOY05A_01_Informes_Datos_Scripts';z.extractall(dest)
 for name in z.namelist():checks.append(dict(path=name,sha256=sha(R/name),extracted_equal=sha(R/name)==sha(dest/name)))
assert all(x['extracted_equal'] for x in checks)
packages=json.loads((R/'VERIFICACION/paquetes_validacion.json').read_text());p=packages[0];p.update(bytes=zip1.stat().st_size,sha256=sha(zip1),md5=hashlib.md5(zip1.read_bytes()).hexdigest(),members=checks)
(R/'VERIFICACION/paquetes_validacion.json').write_text(json.dumps(packages,indent=2,ensure_ascii=False),encoding='utf8');(R/'PAQUETE/VOY05A_Paquetes_SHA256.txt').write_text('\n'.join(x['sha256']+'  '+x['name'] for x in packages)+'\n',encoding='utf8')
# Post-package closure is separate to avoid putting a ZIP's own checksum inside itself.
closure=R/'PAQUETE/VOY05A_05_Cierre_Verificaciones.zip'
extra=[R/'VERIFICACION/paquetes_validacion.json',R/'VERIFICACION/duplicados_contenido.json',R/'PAQUETE/VOY05A_Paquetes_SHA256.txt',R/'VERIFICACION/validacion_local.json',R/'VERIFICACION/integridad_final.json',R/'VERIFICACION/escenas_readback.json']
with zipfile.ZipFile(closure,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in extra:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(closure) as z:
 assert z.testzip() is None
 for p in extra:assert hashlib.sha256(z.read(p.relative_to(R).as_posix())).hexdigest()==sha(p)
print(json.dumps(dict(package1_bytes=zip1.stat().st_size,package1_sha256=sha(zip1),closure_bytes=closure.stat().st_size,closure_sha256=sha(closure),duplicate_groups=len(duplicates)),indent=2))
