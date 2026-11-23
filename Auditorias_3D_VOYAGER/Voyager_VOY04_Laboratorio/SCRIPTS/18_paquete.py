import csv,json,hashlib,zipfile,datetime,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'DATOS'/n).read_text(encoding='utf8'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
 return h.hexdigest()
assert load('integridad_final.json')['pass_check']
assert load('verificacion_animacion_visual.json')['pass_check']
assert load('recursos_guardados.json')['packed_bytes_SHA256_equal']
assert not load('verificacion_copias_blender.json')['bad']
assert all(x['all_sampled_geometry_pass'] for x in load('verificacion_animacion_guardada.json'))
assert len(list(R.glob('[0-9][0-9]_*.md')))==10
meta=load('manifest_blender.json');erg=load('ergonomia_resultados.json');ver=load('verificacion_animacion_guardada.json')
with (R/'DATOS/pivotes_jerarquias.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['escena','objeto','fuente','padre','pivote_mundo_x','pivote_mundo_y','pivote_mundo_z','error_recentrado_m','matriz_referencia_json'])
 for ch in meta['chairs']:
  for p in ch['parts']:w.writerow([ch['scene'],p['object'],p['key'],p['parent'],*p['origin_after'],p['pivot_world_error_m'],json.dumps(p['matrix_after'])])
with (R/'DATOS/resultados_por_altura.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['altura_m','descenso_asiento_m','asiento_sobre_suelo_pies_m','carrera_m','avance_respaldo_m','gap_espalda_m','mirada_deg','poses','subfotogramas','fallos_subfotograma','error_rig_m','resultado'])
 for e,v in zip(erg,ver):w.writerow([e['H'],e['seat_drop_m'],e['adapted_seat_height_over_local_foot_floor_m'],e['travel_m'],e['back_shift_m'],e['backrest_min_capsule_gap_m'],e['look_down_to_center_deg'],v['poses_compared'],v['midpoints_tested'],len(v['midpoint_failures']),v['max_axis_endpoint_error_m'],'GEOMETRIA_MUESTREADA_POSITIVA_CON_RESERVAS'])
with (R/'DATOS/interferencias.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['version','altura_m','frame','miembro','objetos','clearance_m','nota'])
 for H in [1.6,1.75,1.9]:
  data=load(f'original_{H:.2f}.json')
  for b in data['test']['interferences']:w.writerow(['ORIGINAL',H,1,b['part'],';'.join(b['objects']),b['clearance_m'],'Pose original rechazada'])
 for version,file in [('A1_GUIA','resultados_cinematica_A1_FALLO_GUIA.json'),('A3_MANOS','resultados_cinematica_A3_FALLO_MANOS.json')]:
  for s in load(file):
   for failure in s['failures']:
    for b in failure['interferences']:w.writerow([version,s['H'],failure['frame'],b['part'],';'.join(b['objects']),b['clearance_m'],'Trayectoria rechazada'])
 for H in [1.6,1.75,1.9]:w.writerow(['FINAL',H,'1..301 + 300 medios','','',None,'Sin cruces principales >2mm en las muestras, no barrido continuo'])
mods=[dict(H=e['H'],seat_translation_z_m=-e['seat_drop_m'],backrest_forward_m=e['back_shift_m'],chair_retreat_m=e['travel_m'],original_geometry_changed_in_reference=False,experimental_piece_remapped='MSB_30191 vertical extent',new_mechanisms=['VOY04_GUIA_NUEVA','VOY04_CARRO_NUEVO'],console_geometry_changed=False,remaining=['Dorsal support gap','Head/reading for tall mannequin','Gait/biomechanics','Real mechanical design','Continuous collision','Unreal']) for e in erg]
(R/'DATOS/modificaciones_experimentales.json').write_text(json.dumps(mods,indent=2),encoding='utf8')
baseline=load('baseline.json');changed_meta=[]
for x in baseline['files']:
 p=Path(x['path']);st=p.stat() if p.exists() else None
 if st is None or st.st_size!=x['bytes'] or st.st_mtime_ns!=x['mtime_ns']:changed_meta.append(str(p))
assert not changed_meta,changed_meta
(R/'DATOS/integridad_metadata_cierre.json').write_text(json.dumps(dict(full_hash_reread='integridad_final.json',files_rechecked=len(baseline['files']),metadata_unchanged=not changed_meta,changed=changed_meta),indent=2))
report=dict(classification='COMPLETADA CON RESERVAS',date='2026-10-22',reports=10,reference_seats=5,chair_objects=92,main_scenes=8,source_OBJ_objects=630,source_scene_geometry=645,copy_checks=1184,heights=[1.6,1.75,1.9],animation_poses=1803,chair_poses=243,continuous_collision_certified=False,physics_certified=False,Unreal_opened=False,GitHub_writes=False,VOY05_started=False,main_blend=str(R/'ESCENAS/VOY04_Laboratorio.blend'),failures_blend=str(R/'ESCENAS/VOY04_Fallos_y_Comparativa.blend'),protected_files=len(baseline['files']),intact=True,visual_check=load('verificacion_animacion_visual.json'))
(R/'DATOS/validacion_entrega.json').write_text(json.dumps(report,indent=2),encoding='utf8')
# Portable package includes complete animated GIF/WebP. Large Blender files and PNG frame sequence remain on MSI.
files=sorted([p for p in R.glob('*.md')]+[R/'GALERIA.html']+[p for p in (R/'DATOS').rglob('*') if p.is_file()]+[p for p in (R/'SCRIPTS').glob('*.py')]+[p for p in (R/'LOGS').glob('*.log') if p.name!='18_paquete.log']+[p for p in (R/'CAPTURAS').glob('*.png')]+[p for p in (R/'ANIMACIONES').glob('*') if p.suffix in ['.gif','.webp']]+[p for p in (R/'REFERENCIAS').glob('*') if p.suffix in ['.md','.json','.py']])
hashes=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
local_blends=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in (R/'ESCENAS').glob('*.blend')]+[dict(path=str(R/'REFERENCIAS/VOY03_Circulacion.blend'),sha256=sha(R/'REFERENCIAS/VOY03_Circulacion.blend'))]
manifest=R/'MANIFIESTO_SHA256.json';manifest.write_text(json.dumps(dict(classification='COMPLETADA CON RESERVAS',files=hashes,large_Blender_files_on_MSI=local_blends,raw_PNG_sequence_on_MSI=str(R/'ANIMACIONES'),portable_animation_files=['ANIMACIONES/VOY04_Ciclo_175.gif','ANIMACIONES/VOY04_Ciclo_175.webp'],scope='Documentary package. ZIP CRC/SHA is stored externally to avoid self-reference.'),indent=2,ensure_ascii=False),encoding='utf8');files.append(manifest)
dest=R/'PAQUETE/VOY04_Entrega.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for p in files:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 entries=[dict(path=i.filename,CRC32=f'{i.CRC:08x}',bytes=i.file_size,compressed_bytes=i.compress_size) for i in z.infolist()]
 for item in hashes:
  assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256'],item['path']
h=sha(dest);(R/'PAQUETE/VOY04_Entrega.zip.sha256').write_text(h+'  VOY04_Entrega.zip\n',encoding='ascii');verification=dict(zip=str(dest),bytes=dest.stat().st_size,sha256=h,CRC_test='PASS',all_entry_SHA256_match_manifest=True,entries=len(entries),entry_CRC32=entries,large_files=local_blends)
(R/'PAQUETE/verificacion_zip.json').write_text(json.dumps(verification,indent=2,ensure_ascii=False),encoding='utf8')
print('ZIP',str(dest),'MB',round(dest.stat().st_size/1e6,2),'ENTRIES',len(entries),'CRC_PASS','SHA256',h,flush=True)
