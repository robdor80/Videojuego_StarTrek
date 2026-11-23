from pathlib import Path
import json,hashlib,shutil,html
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];V2=R.parent/'Voyager_VOY02_Laboratorio';dest=R/'REFERENCIAS/VOY02/CAPTURAS';dest.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# A presentation rebuild once archived three later figures along with the old B
# shots. Remove only those byte-identical duplicates; no negative result is lost.
cleanlog=R/'DATOS/depuracion_catalogo.json';clean=json.loads(cleanlog.read_text()) if cleanlog.exists() else []
for n in ['B12_niveles_suelos_aislados.png','B13_escalones_apoyos_aislados.png','B14_bloqueo_diagonal_Mesh2096.png']:
 p=R/'CAPTURAS/REVISION_A1_NO_VALIDADA'/n;final=R/'CAPTURAS'/n
 if p.exists():
  assert p.resolve().is_relative_to((R/'CAPTURAS/REVISION_A1_NO_VALIDADA').resolve()) and sha(p)==sha(final)
  clean.append(dict(duplicate_path=str(p),retained_path=str(final),sha256=sha(final),reason='Later final evidence accidentally duplicated into initial revision archive; byte-identical copy only.'))
  p.unlink()
cleanlog.write_text(json.dumps(clean,indent=2,ensure_ascii=False),encoding='utf8')
names=['A01_puente_completo.png','A02_puente_humanos.png','A03_planta_acotada.png','A04_seccion_alturas.png','C01_puente_pasillo.png','C02_detalle_adaptador.png','G01_conjunto_completo.png','G02_conjunto_planta.png','G03_conjunto_perspectiva.png','G04_cruce_y_turbolift.png'];copies=[]
for n in names:
 s=V2/'CAPTURAS'/n;p=dest/n
 if not p.exists():shutil.copy2(s,p)
 assert sha(s)==sha(p);copies.append(dict(source=str(s),copy=str(p),sha256=sha(p)))
(R/'DATOS/copias_visuales_referencia.json').write_text(json.dumps(dict(source_capture_count=33,copied_relevant_captures=copies,remaining='All33 remain intact in VOY02, protected by baseline.'),indent=2,ensure_ascii=False),encoding='utf8')
notes={
 'B01_planta_rutas_original':'Rutas finales sobre el puente completo; recorte de techo solo para visualización.',
 'B02_niveles_lateral':'Vista lateral exterior ocluida: no usar para interpretar niveles; sustituida por B12 y secciones.',
 'B03_escalera_derecha_apoyo':'Escalera derecha y trayectoria de diagnóstico; todos los objetos se conservan en las pruebas.',
 'B04_escalera_izquierda_apoyo':'Escalera izquierda y trayectoria de diagnóstico.',
 'B05_navegacion_ruta':'Área de navegación y rutas finales; aproximación al puesto, no postura sentada.',
 'B07_red_completa_planta':'Recorridos finales centro–turbolift y centro–camarote; ensamblaje heredado.',
 'B08_red_completa_axonometrica':'Vista general del recorrido sobre la red existente, puertas abiertas.',
 'B09_union_posterior':'Conexión posterior y adaptador R1, sin nueva modificación.',
 'B10_puestos_mando':'Aproximaciones finales a sillones izquierdo y derecho, sin uso de asiento.',
 'B11_planta_original_completa':'Planta de referencia sin rutas añadidas; encuadre completo corregido.',
 'B12_niveles_suelos_aislados':'Suelos reales aislados para ver niveles; color diagnóstico. Arquitectura restante omitida solo en esta captura, presente en todos los ensayos.',
 'B13_escalones_apoyos_aislados':'Detalle de apoyos reales de la escalera, aislados y coloreados solo para lectura.',
 'B14_bloqueo_diagonal_Mesh2096':'Resultado negativo: cápsula de radio35cm en la diagonal descartada; obstáculo Mesh_2096 no eliminado.',
 'A04_escalones_aislados':'Diagnóstico inicial: Mesh_1856 aislada. Muestra marcos/narices, NO la escalera entera.',
 '01_superficies_originales':'Selección inicial por material: inventario incompleto, no representa huecos físicos acreditados.',
 'QA_contacto_inicial':'Contacto de QA inicial; incluye encuadres rechazados y ruta sin certificado continuo.',
 '02_planta_soportes_y_rutas':'Inventario corregido de apoyos reales y seis rutas validadas. No certifica toda la planta.',
 '03_seccion_derecha':'Perfil medido de la escalera derecha a 2mm, contrahuellas y huella.',
 '03_seccion_izquierda':'Perfil medido de la escalera izquierda a 2mm.',
 '04_seccion_navegacion':'Sección real de rejillas/marcos y apoyos de navegación.',
 '05_atajo_descartado_y_ruta_final':'Comparación de trayectoria; misma arquitectura. El rojo queda rechazado por falta de apoyo vertical.',
 '06_tres_alturas':'Mismo punto, radio35cm constante, alturas160/175/190cm.',
 '07_comparativa_sin_reparacion':'Antes/después del método; la arquitectura no se ha reparado.'}
rows=[]
for folder in ['CAPTURAS','LAMINAS','REFERENCIAS/VOY02/CAPTURAS']:
 for p in sorted((R/folder).rglob('*.png')):
  if p.stem=='QA_contacto_final':continue # Contact sheet is generated after this catalog; avoid embedding itself.
  with Image.open(p) as im:
   im.verify()
  with Image.open(p) as im:dimensions=list(im.size);extrema=im.convert('RGB').getextrema()
  rejected='REVISION_A1_NO_VALIDADA' in str(p) or p.stem in ['B02_niveles_lateral','01_superficies_originales','QA_contacto_inicial']
  group='Descartados / diagnósticos iniciales' if rejected else 'Referencia VOY02' if folder.startswith('REFERENCIAS') else 'Capturas originales de diagnóstico' if p.stem.startswith('A') else 'Evidencia final'
  caption=notes.get(p.stem,'Cápsula de referencia '+p.stem[-4:]+' m, radio0,35m; mismo punto crítico.' if p.stem.startswith('B06') else p.stem.replace('_',' '))
  if 'REVISION_A1_NO_VALIDADA' in str(p):caption='RECHAZADA como evidencia final: encuadre inicial / candidato sin certificado continuo. Conservada por trazabilidad.'
  rows.append(dict(path=p.relative_to(R).as_posix(),dimensions=dimensions,sha256=sha(p),group=group,selected_final=group=='Evidencia final',caption=caption,nonempty=any(a!=b for a,b in extrema)))
(R/'DATOS/capturas_qa.json').write_text(json.dumps(dict(images=rows,visual_review='Contact sheets plus individual plans, sections, capsule views, full assembly and negative obstacle reviewed. B02 is explicitly not used for level evidence.',all_readable=all(r['nonempty'] for r in rows)),indent=2,ensure_ascii=False),encoding='utf8')
css='body{font:17px system-ui;background:#f1f4f7;color:#172c40;margin:0 auto;max-width:1500px;padding:24px}a{color:#1260b5}h1{font-size:30px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:20px}figure{margin:0;background:white;padding:14px;border:1px solid #d1dae3;border-radius:8px}img{width:100%;height:auto}figcaption{padding:12px 0;line-height:1.5}small{color:#586574}summary{cursor:pointer;font-size:22px;padding:20px}h2{margin-top:45px}'
body=['<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>VOY-03 — Galería técnica</title><style>'+css+'</style><h1>VOY-03 · Galería técnica</h1><p><b>COMPLETADA, alcance geométrico.</b> Opción A: misma arquitectura, recorridos verificados con radio35cm y tres alturas. Unreal pendiente. <a href="README.md">Índice y escenas</a> · <a href="00_RESUMEN_EJECUTIVO.md">Resumen</a></p><p>Las capturas con techo recortado o superficies aisladas sirven para leer la geometría. Las pruebas utilizan todas las mallas y no omiten obstáculos. Abrir cualquier imagen para ver su resolución original.</p>']
for group in ['Evidencia final','Capturas originales de diagnóstico','Referencia VOY02','Descartados / diagnósticos iniciales']:
 if group=='Descartados / diagnósticos iniciales':body.append('<details><summary>Descartados y diagnósticos iniciales (no son aprobados finales)</summary>')
 else:body.append('<h2>'+group+'</h2>')
 body.append('<div class="grid">')
 for row in rows:
  if row['group']!=group:continue
  p=html.escape(row['path']);caption=html.escape(row['caption']);body.append(f'<figure><a href="{p}"><img loading="lazy" src="{p}" alt="{caption}"></a><figcaption>{caption}<br><small>{p} · {row["dimensions"][0]} × {row["dimensions"][1]} px</small></figcaption></figure>')
 body.append('</div>')
 if group=='Descartados / diagnósticos iniciales':body.append('</details>')
body.append('</html>');(R/'GALERIA.html').write_text('\n'.join(body),encoding='utf8')
final=[r for r in rows if r['selected_final']];cols=4;thumbw,thumbh=360,315;im=Image.new('RGB',(cols*thumbw,((len(final)+cols-1)//cols)*thumbh),'white');draw=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16)
for i,row in enumerate(final):
 p=R/row['path'];small=Image.open(p).convert('RGB');small.thumbnail((350,265));x=i%cols*thumbw;y=i//cols*thumbh;im.paste(small,(x,y));draw.text((x+5,y+270),p.stem[:36],fill='#172c40',font=font)
im.save(R/'LAMINAS/QA_contacto_final.png');print('GALLERY',len(rows),'FINAL',len(final),'COPIES',len(copies),flush=True)
