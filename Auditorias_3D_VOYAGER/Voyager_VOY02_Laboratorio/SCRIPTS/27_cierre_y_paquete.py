"""Final independent checks and shareable package; never rewrites original baselines."""
import csv,datetime,hashlib,json,re,zipfile,ast
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'DATOS';package=R/'PAQUETE';package.mkdir(exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def write(n,d):(P/n).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf8')
baseline=json.loads((P/'entradas_antes.json').read_text());sources=[]
for x in baseline:
 source=Path(x['source']);q=Path(x['copy']) if x.get('copy') else None;sources.append(dict(source=str(source),sha256=sha(source),expected_sha256=x['sha256'],original_matches=sha(source)==x['sha256'],copy=str(q) if q else None,copy_matches=not q or sha(q)==x['sha256']))
assert all(x['original_matches'] and x['copy_matches'] for x in sources)
write('integridad_fuentes_final.json',dict(originals_checked=len(sources),copies_checked=sum(bool(x['copy']) for x in sources),all_match=True,scope='Recorded VOY-02 sources/copies only. Sutherland and UE projects were not written by this work; this is not a full computer/repository hash.',sources=sources))
old=list(csv.DictReader((R/'TRASPASO/INVENTARIO_ARCHIVOS.csv').open(encoding='utf-8-sig')));changes=[]
for x in old:
 p=R/x['relative_path'];now=sha(p) if p.is_file() else None
 if now!=x['sha256']:changes.append(dict(file=x['relative_path'],before_sha256=x['sha256'],after_sha256=now,exists=p.is_file()))
assert all(not x['file'].startswith('FUENTES/') for x in changes)
write('cambios_desde_parada.json',dict(baseline_preserved='TRASPASO/INVENTARIO_ARCHIVOS.csv',original_file_count=len(old),changed_existing_files=changes,new_paths=[p.relative_to(R).as_posix() for p in sorted(R.rglob('*')) if p.is_file() and p.relative_to(R).as_posix() not in {x['relative_path'] for x in old} and p.parent!=package],explanation='Derived laboratory blend, scripts, renders and prototype data intentionally revised. Baselines/original resources not replaced. Backups and superseded results retained in TRASPASO.'))
blend=R/'ESCENAS/VOY02_Laboratorio.blend';contrast=read('contraste_blend.json');assert contrast['all_geometry_matches'] and contrast['scenes_match_manifest'] and contrast['packed_images']==49 and len(contrast['scenes'])==8;assert contrast['sha256_after']==sha(blend),'Final saved file differs from contrasted file'
assert all(x['uv_layers']>=1 for x in contrast['objects'] if x['label'].startswith('PUENTE:'))
proto=read('prototipo_conjunto.json');assert proto.get('adapter_revision');assert all(r['clear'] for t in proto['routes'] for r in t['routes']);assert all(t['support']['clear'] for t in proto['routes'])
ad=next(a for a in read('encuentros_adaptadores.json')['adapters'] if a['id']=='AD_PUENTE');assert not any(x['transverse'] for x in ad['contacts'])
formats=[]
for p in list(P.glob('*.json'))+list(P.glob('*.npz'))+list((R/'CAPTURAS').glob('*.png')):
 if p.suffix=='.json':json.loads(p.read_text(encoding='utf8'))
 elif p.suffix=='.npz':
  with zipfile.ZipFile(p) as z:assert z.testzip() is None
 else:
  with Image.open(p) as im:im.verify()
 formats.append(p.relative_to(R).as_posix())
manifest=read('capturas_manifest.json');assert len(manifest)==33 and len({x['file'] for x in manifest})==33;assert all((R/'CAPTURAS'/x['file']).is_file() for x in manifest);assert all(x.get('bounds_pass') is not False for x in read('capturas_qa.json'))
scripts=list((R/'SCRIPTS').glob('*.py'))
for p in scripts:ast.parse(p.read_text(encoding='utf8'),filename=str(p))
reports=sorted(R.glob('[0-9][0-9]_*.md'));assert len(reports)==9
(R/'VERIFICACION_ENTREGA.md').write_text('''# Verificar la entrega VOY-02

El ZIP contiene MANIFIESTO_ENTREGA.json con ruta, tamaño y SHA-256 de cada archivo de contenido. El propio manifiesto no se incluye a sí mismo en esa lista. La comprobación del ZIP vuelve a leer cada entrada y contrasta todos esos hashes, además de revisar el CRC.

PAQUETE/COMPROBACION_ZIP.json y PAQUETE/VOY02_ENTREGA.sha256.txt permanecen al lado del ZIP en el laboratorio local. Contienen el hash del ZIP completo y el resultado real de comprobación. No se incluyen dentro del ZIP para evitar una dependencia circular de su propio hash.

Los nueve informes, tablas, capturas y galería pueden leerse tras extraer la carpeta. Repetir ensayos de geometría requiere los archivos grandes locales listados en README, excluidos del paquete. Los originales y baselines no deben reconstruirse ni sobrescribirse para ejecutar una verificación.

Los JSON de TRASPASO y los logs anteriores son historia conservada. El estado de cierre está en DATOS/estado_final.json y los informes finales; un resultado anterior negativo o sustituido no debe confundirse con la versión final sin leer el informe 08.
''',encoding='utf8')
broken=[]
for p in reports+[R/'README.md']:
 for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  if re.match(r'^(https?:|#)',link):continue
  target=(p.parent/link.split('#')[0]).resolve()
  if not target.exists() and target!=P/'estado_final.json':broken.append(dict(file=p.name,link=link))
assert not broken,broken
state=dict(date_context='21/10/2026 Europe/Madrid',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),laboratory=str(R),status='VOY-02 evaluation complete; production approval and future systems not claimed',reports=[p.name for p in reports],blend=dict(path=str(blend),sha256=sha(blend),scenes=8,packed_images=49,prototype_components_compared=len(contrast['objects']),all_match=True,tolerance_m=contrast['tolerance_m'],max_error_m=max(x['max_coordinate_or_surface_error_m'] or 0 for x in contrast['objects'])),captures=33,analytical_plates=len(list((R/'LAMINAS').glob('L*.png'))),contact_sheets=len(list((R/'LAMINAS').glob('CONTACTO*'))),csv_tables=len(list(P.glob('*.csv'))),json_data_files=len(list(P.glob('*.json'))),sources_originals=115,sources_copies=106,all_sources_match=True,scene_review='Eight scenes reopened and inventoried; G surfaces exhaustively compared to tested prototype. Other scenes share corrected OBJ datablocks; no claim of independent full physical testing of every scene.',routes=[dict(id=t['id'],tests=[dict(height=r['height'],samples=r['samples'],clear=r['clear']) for r in t['routes']],support=t['support']['clear']) for t in proto['routes']],adapter_revision=proto['adapter_revision'],final_adapter_transverse_contacts=sum(x['transverse'] for x in ad['contacts']),format_files_checked=len(formats),python_scripts_parsed=len(scripts),broken_report_links=broken,not_certified=['continuous central/navigation bridge access','door pockets and continuous motion','human rig/posture/sit-stand/controls','continuous disability access','UE CharacterMovement/NavMesh/physics/FPS/Lumen','artistic restoration/production integration'],no_original_models_modified=True,no_sutherland_or_ue_project_modified=True,no_publication_or_git_mutation=True)
write('estado_final.json',state)
assert (P/'estado_final.json').is_file()
(R/'LOGS/27_verificaciones_previas.log').write_text(json.dumps(dict(sources='115/115 originals and 106/106 copies match',scenes=8,prototype_components='645/645 within declared tolerance',capsule_routes='6/6 pass after adapter revision, with 2/2 support paths',captures=33,python_syntax='all parsed',report_links='all local targets exist',format_files_checked=len(formats),note='ZIP CRC/content hash results are recorded after construction in external PAQUETE/COMPROBACION_ZIP.json.'),indent=2),encoding='utf8')
files=[]
files+=reports+[R/'README.md',R/'VERIFICACION_ENTREGA.md',R/'GALERIA.html']
for folder,patterns in [('DATOS',['*.json','*.csv']),('CAPTURAS',['*.png']),('LAMINAS',['*.png','*.jpg']),('SCRIPTS',['*.py']),('LOGS',['*.log']),('REFERENCIAS',['*.md','*.json']),('TRASPASO',['*.md','*.json','*.csv','*.py'])]:
 for pattern in patterns:files+=list((R/folder).glob(pattern))
files=sorted(set(files));entries=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
delivery_manifest=R/'MANIFIESTO_ENTREGA.json';delivery_manifest.write_text(json.dumps(dict(scope='Reports, tables, diagnostic images, scripts, logs and continuity documents. Geometry NPZ, Blender files, original textures and large backups excluded; see README.',files=entries),indent=2,ensure_ascii=False),encoding='utf8')
zip_path=package/'VOY02_ENTREGA.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[delivery_manifest]:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(set(z.namelist()))==len(entries)+1
 bad=[x['path'] for x in entries if hashlib.sha256(z.read(x['path'])).hexdigest()!=x['sha256']]
 assert not bad,bad
 inside=json.loads(z.read('MANIFIESTO_ENTREGA.json'));assert inside['files']==entries
checksum=sha(zip_path);check=dict(path=str(zip_path),bytes=zip_path.stat().st_size,MiB=zip_path.stat().st_size/1048576,sha256=checksum,entries=len(entries)+1,reports=9,CRC_ok=True,all_content_hashes_match=True,content_hashes_checked=len(entries),manifest_sha256=sha(delivery_manifest),originals_and_copies_still_match=True,excluded_large_files_listed_in='README.md')
(package/'COMPROBACION_ZIP.json').write_text(json.dumps(check,indent=2,ensure_ascii=False),encoding='utf8');(package/'VOY02_ENTREGA.sha256.txt').write_text(checksum+'  VOY02_ENTREGA.zip\n',encoding='utf8')
print(json.dumps(check,ensure_ascii=False),flush=True)
