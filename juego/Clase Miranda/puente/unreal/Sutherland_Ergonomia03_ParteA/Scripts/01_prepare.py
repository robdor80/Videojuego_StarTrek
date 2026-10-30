from pathlib import Path
import hashlib,json,shutil,time
R=Path(__file__).resolve().parents[1]
REPO=R.parents[4]
SOURCE=Path(r'C:\Users\andro\ST_ORG_01_FASE_3C_09\2026-10-25_02-17-38\RECUPERACION\P-e4252915fcf5')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
for n in ['Data','Logs','Exports','Backups']: (R/n).mkdir(exist_ok=True)
checkpoint=R/'CONTINUAR_AQUI.md'
checkpoint.write_text('''# Sutherland Ergonomia_03 — Parte A
27/10/2026, Europe/Madrid. Copia protegida única.
Etapa A.1: seleccionada VISUAL_02 recuperada de ST_ORG_01_FASE_3C_09/RECUPERACION/P-e4252915fcf5.
Motivo: conserva Quinn, capitán, cuatro puertas, colisiones y los seis mecanismos laterales que INTEGRACION_FINAL_01 retiró.
La entrega final posterior se ha inspeccionado como referencia, no se promueven sus retiradas sobre esta base.
Etapa A.2: copia y comprobación SHA-256 EN CURSO. No abrir Unreal hasta Data/copy_verified.json ok=true.
Reanudación: python Scripts/01_prepare.py; comprueba cada archivo existente antes de copiar; no sobrescribe diferencias.
No modificar originales. No commit/push/PR. D04 histórica operativa; D01–D03 sin destinos. Pies suspendidos y VSM abiertos.
''',encoding='utf-8')
blends=R.parents[1]/'blender'
originals={str(p):sha(p) for p in blends.glob('*.blend*')}
(R/'Data/original_blend_hashes.json').write_text(json.dumps(originals,indent=2),encoding='utf-8')
critical='Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap'
assert sha(SOURCE/'Unreal'/critical)=='935938535e566b9187cd58fe8aa86a16be97a53a4d978a5be53e85a64ad7b417','VISUAL_02 saved map does not match historical verified version'
manifest=[]
for i,p in enumerate((SOURCE/'Unreal').rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(SOURCE/'Unreal');dest=R/'Unreal'/rel;h=sha(p)
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():assert sha(dest)==h,('Existing different file; do not overwrite',str(dest))
 else:shutil.copy2(p,dest)
 assert sha(dest)==h,str(dest)
 manifest.append({'path':rel.as_posix(),'size':p.stat().st_size,'sha256':h})
 if len(manifest)%400==0:print('COPIED_VERIFIED',len(manifest),flush=True)
(R/'Data/copy_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for n in ['visual_export.json','V02_baseline_audit.json','playable_setup.json']:
 shutil.copy2(SOURCE/'Data'/n,R/'Data'/('reference_'+n))
(R/'Data/copy_verified.json').write_text(json.dumps({'ok':True,'source':str(SOURCE),'files':len(manifest),'bytes':sum(x['size'] for x in manifest),'map_hash':sha(SOURCE/'Unreal'/critical)},indent=2),encoding='utf-8')
checkpoint.write_text(checkpoint.read_text(encoding='utf-8').replace('copia y comprobación SHA-256 EN CURSO','copia y comprobación SHA-256 COMPLETADAS').replace('No abrir Unreal hasta Data/copy_verified.json ok=true.','Ver Data/copy_verified.json y copy_manifest.json. Siguiente: auditoría Blender y nivel UE, sin guardar originales.'),encoding='utf-8')
print('COPY_OK',len(manifest),flush=True)
