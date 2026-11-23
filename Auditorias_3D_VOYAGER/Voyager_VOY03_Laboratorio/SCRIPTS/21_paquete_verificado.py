from pathlib import Path
import json,hashlib,zipfile,ast,re,math,datetime
from PIL import Image
R=Path(__file__).resolve().parents[1];assert R.name=='Voyager_VOY03_Laboratorio';P=R/'PAQUETE';P.mkdir(exist_ok=True)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
read=lambda n:json.loads((R/'DATOS'/n).read_text(encoding='utf8'))
reports=sorted(R.glob('0[0-8]_*.md'));assert len(reports)==9
broken=[]
for f in reports+[R/'README.md']:
 text=f.read_text(encoding='utf8');assert len(text)>1500
 for dest in re.findall(r'\]\(([^)]+)\)',text):
  if '://' in dest or dest.startswith('#'):continue
  if not (f.parent/dest.split('#')[0]).exists():broken.append(dict(file=f.name,target=dest))
assert not broken,broken
scripts=list((R/'SCRIPTS').glob('*.py'))
for f in scripts:ast.parse(f.read_text(encoding='utf8'),filename=str(f))
results=read('barridos_resultados.json');support=read('apoyo_continuo.json');metric=read('resumen_metricas.json');contrast=read('contraste_VOY03.json');integrity=read('integridad_final.json');manifest=read('manifest_blender.json')
assert len(results['results'])==39 and all(r['pass_test'] for r in results['results'])
assert len(support['results'])==13
assert all(r['certified'] for r in support['results']) and support['upward_contact_component_bound']==.5
assert {(r['id'],r['height_m']) for r in results['results']}=={(r['id'],h) for r in support['results'] for h in [1.6,1.75,1.9]}
assert contrast['all_geometry_matches'] and contrast['file_unchanged'] and contrast['scene_names_match'] and len(contrast['objects'])==645 and len(contrast['scenes'])==4
assert sha(R/'ESCENAS/VOY03_Circulacion.blend')==contrast['sha256']
assert integrity['all_protected_unchanged'] and integrity['reference_copies_unchanged'] and integrity['protected_entries']==2762
assert manifest['source_to_copy_equal'] and not manifest['geometry_changes'] and len(manifest['architecture_fingerprints'])==645
for r in results['results']:
 assert r['radius_m']==.35 and not r['geometry_modified'] and not r['pose_or_support_failures'] and not r['movement_failures'] and not r['sweep_failures']
 json.dumps(r,allow_nan=False)
images=[]
for f in R.rglob('*.png'):
 if 'PAQUETE' in f.relative_to(R).parts:continue
 with Image.open(f) as im:im.verify()
 images.append(str(f.relative_to(R)))
check=dict(reports=len(reports),scripts_parsed=len(scripts),broken_report_links=broken,images_verified=len(images),cases_passed=39,continuous_support_routes=13,geometry_components_matched=645,scenes=4,protected_unchanged=2762,reference_copies_unchanged=len(integrity['reference_copies']),all_passed=True)
(R/'DATOS/validacion_entrega.json').write_text(json.dumps(check,indent=2,ensure_ascii=False),encoding='utf8')
state=dict(status='COMPLETADA',scope='VOY03 geometric circulation only',time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),geometry_modified=False,originals_unchanged=True,protected_hash_entries=2762,all_routes_passed=True,heights_m=[1.6,1.75,1.9],radius_m=.35,pose_samples=metric['pose_samples_total'],swept_intervals=metric['swept_intervals_total'],blend_file=str(R/'ESCENAS/VOY03_Circulacion.blend'),blend_sha256=contrast['sha256'],ue_executed=False,voy04_started=False,git_operations=False,remaining='Real CharacterMovement, collisions, dynamics, gait, doors and NavMesh require a future authorized phase.')
(R/'DATOS/estado_final_VOY03.json').write_text(json.dumps(state,indent=2,ensure_ascii=False),encoding='utf8')
excluded_reference=R/'REFERENCIAS/VOY02/VOY02_Laboratorio.blend'
files=sorted(p for p in R.rglob('*') if p.is_file() and 'PAQUETE' not in p.relative_to(R).parts and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.blend1','.blend2'] and p!=excluded_reference and p.name!='MANIFIESTO_SHA256.json')
entries=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
manifestpath=R/'MANIFIESTO_SHA256.json';manifestpath.write_text(json.dumps(dict(entries=entries,excluded_reference_blend=str(excluded_reference),excluded_reference_blend_sha256=sha(excluded_reference),note='Manifest excludes its own hash. ZIP CRC and every manifest entry SHA256 were checked after creation.'),indent=2,ensure_ascii=False),encoding='utf8')
zpath=P/'VOY03_Entrega.zip'
with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for p in files+[manifestpath]:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None;assert len(z.namelist())==len(entries)+1;assert len(z.namelist())==len(set(z.namelist()))
 for e in entries:
  assert '..' not in Path(e['path']).parts and not Path(e['path']).is_absolute()
  h=hashlib.sha256()
  with z.open(e['path']) as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
  assert h.hexdigest()==e['sha256'],e['path']
 assert json.loads(z.read('MANIFIESTO_SHA256.json'))['entries']==entries
zipcheck=dict(file=str(zpath),bytes=zpath.stat().st_size,sha256=sha(zpath),crc_all_passed=True,all_manifest_hashes_match=True,entries=len(entries)+1,contains_nine_reports=True,contains_final_blend=True,contains_scripts_data_images_logs=True,external_reference_blend=str(excluded_reference),delivery_checks=check)
(P/'verificacion_zip.json').write_text(json.dumps(zipcheck,indent=2,ensure_ascii=False),encoding='utf8');(P/'VOY03_Entrega.zip.sha256').write_text(zipcheck['sha256']+'  VOY03_Entrega.zip\n',encoding='ascii');print(json.dumps(zipcheck,indent=2,ensure_ascii=False),flush=True)
