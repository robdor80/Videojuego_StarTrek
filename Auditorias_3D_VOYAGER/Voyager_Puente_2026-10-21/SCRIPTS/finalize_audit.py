import json,hashlib,csv,re,collections
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];D=R/'DATOS';C=R/'CAPTURAS'
before=json.loads((D/'inventario_archivos.json').read_text(encoding='utf8'));checks=[]
for f in before['files']:
 p=Path(f['path']);now={'path':str(p),'exists':p.is_file()}
 if p.is_file():
  st=p.stat();now.update(bytes=st.st_size,mtime_ns=st.st_mtime_ns,sha256=hashlib.sha256(p.read_bytes()).hexdigest());now['unchanged']=all(now[k]==f[k] for k in ['bytes','mtime_ns','sha256'])
 else:now['unchanged']=False
 checks.append(now)
result={'scope':'230 located input files from inventory; not an entire-computer snapshot','files_checked':len(checks),'unchanged':sum(c['unchanged'] for c in checks),'differences':[c for c in checks if not c['unchanged']],'checks':checks}
(D/'integridad_final.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
# Material/geometry contact sheets. Existing rendered pixels only.
fontpath=Path(r'C:\Windows\Fonts\arial.ttf');font=ImageFont.truetype(str(fontpath),22) if fontpath.exists() else ImageFont.load_default()
def sheet(name,items):
 out=Image.new('RGB',(1600,640),'#303030');d=ImageDraw.Draw(out)
 for k,(file,title,subtitle) in enumerate(items):
  im=Image.open(C/file).convert('RGB');im.thumbnail((790,540));x=k*800;out.paste(im,(x+(800-im.width)//2,60));d.text((x+12,10),title,font=font,fill='white');d.text((x+12,603),subtitle,font=font,fill='white')
 out.save(C/name)
sheet('comparativa_puentes.png',[('glb_09_puente_corte_z250.png','Coleccion: puente esquematico sin texturas','Corte temporal Z > 2,50 m; escala de vista independiente'),('obj_texturizado_corte_perspectiva.png','Puente detallado: shaders y texturas existentes','Corte temporal Z > 2,50 m; luces de diagnostico')])
sheet('comparativa_suelo_conversion.png',[('recovery_03_corte_z260.png','Conversion MAX: superficies de suelo incompletas','OBJ heredado excluido; corte Z > 2,60 m'),('obj_texturizado_corte_planta.png','Familia OBJ: suelo mas completo','Corte Z > 2,50 m; no certifica colisiones')])
special={
 'comparativa_puentes.png':'Comparación principal de familias. Cámaras y escalas independientes; dos cortes temporales.',
 'comparativa_suelo_conversion.png':'Comparación de fuentes: el MAX convertido no conserva todas las superficies del suelo.',
 'texturas_embebidas_OBJ.png':'49 imágenes reales extraídas en memoria del GLB; lámina reducida, no nuevos mapas de textura.',
 'catalogo_grupos.png':'Bloques secundarios anónimos de la colección, color de material Workbench; no son habitaciones restauradas.',
 'obj_texturizado_interior.png':'Interior completo, sin corte, luz diagnóstica exterior: ausencia de emisión y oscuridad real de este ensayo.',
 'obj_texturizado_interior_luz_diagnostico.png':'Mismo interior con luz puntual temporal para inspección; shaders originales intactos.',
 'glb_05_puente_mobiliario_aislado.png':'La selección por jerarquía contiene barandillas y soportes, no sillas; el nombre de selección no acredita mobiliario.',
 'blend_05_puente_mobiliario_aislado.png':'La selección por jerarquía contiene barandillas y soportes, no sillas; ver informe de arquitectura.',
}
rows=[];bad=[]
for p in sorted(C.glob('*.png')):
 try:
  with Image.open(p) as im:im.load();width,height=im.size
 except Exception as e:bad.append({'path':str(p),'error':str(e)});continue
 desc=special.get(p.name)
 if not desc:
  if 'corte'in p.name:desc='Corte de diagnóstico: omite caras altas en memoria. No muestra el cerramiento completo.'
  elif 'grupo'in p.name:desc='Grupo secundario aislado; geometría y color difuso originales.'
  elif 'puerta'in p.name:desc='Puertas/marcos aislados; la disposición de catálogo no es ensamblaje certificado.'
  elif 'sillon'in p.name or 'consolas'in p.name:desc='Piezas aisladas de Recovery, mostradas por geometría y color de material.'
  elif 'catalogo'in p.name:desc='Conjunto completo desplegado en catálogo; no representa una cubierta ensamblada.'
  elif 'superior'in p.name or 'completo'in p.name:desc='Vista completa de la selección original; los elementos residuales pueden ampliar el encuadre.'
  else:desc='Vista de diagnóstico de la selección original; consultar manifiesto de objetos/cámara.'
  if p.name.startswith(('blend_','glb_','recovery_')):desc+=' Workbench no evalúa texturas; comparar con renders obj_texturizado y lámina de imágenes.'
 rows.append({'file':p.name,'width':width,'height':height,'description':desc,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(D/'capturas_verificadas.json').write_text(json.dumps({'images':rows,'decode_errors':bad},indent=2,ensure_ascii=False),encoding='utf8')
index='# Catálogo visual de diagnóstico\n\nTodas las imágenes proceden de Blender o de píxeles reales de imágenes incluidas. No se han generado texturas ni restaurado materiales. Las cámaras/luces son de inspección. Los cortes omiten caras por encima de una cota y pueden abrir paredes que sí existen. Workbench muestra color difuso de material, no mapas; los renders `obj_texturizado` sí evalúan los shaders originales.\n\n'
index+='## Vistas recomendadas\n\n'
for n in ['comparativa_puentes.png','comparativa_suelo_conversion.png','obj_texturizado_interior_luz_diagnostico.png','texturas_embebidas_OBJ.png','glb_06_pasillos.png','glb_07_turbolift.png']:
 index+=f'[{n}]({n})\n\n'
index+='## Índice completo\n\n| Imagen | Resolución | Alcance |\n|---|---|---|\n'
index+='\n'.join(f"| [{x['file']}]({x['file']}) | {x['width']} × {x['height']} | {x['description']} |" for x in rows)+'\n'
(C/'INDICE.md').write_text(index,encoding='utf8')
summary=R/'01_RESUMEN_EJECUTIVO.md';s=summary.read_text(encoding='utf8').split('\nVerificación final:')[0];s+=f'\nVerificación final: **{result["unchanged"]}/{result["files_checked"]} archivos de entrada sin cambios de SHA-256, tamaño y mtime_ns**; **{len(rows)} PNG decodificados**, {len(bad)} errores de imagen. Este alcance no representa un snapshot completo de todos los proyectos del ordenador.\n';summary.write_text(s,encoding='utf8')
# Verify deliverables and all referenced local capture names.
missing=[]
for p in R.glob('*.md'):
 for n in re.findall(r'CAPTURAS/([a-zA-Z0-9_]+\.png)',p.read_text(encoding='utf8')):
  if not (C/n).exists():missing.append(n)
expected=['01_RESUMEN_EJECUTIVO.md','02_INVENTARIO.md','03_GEOMETRIA.md','04_MATERIALES_TEXTURAS.md','05_INTERACTIVIDAD.md','06_MODULOS_ADICIONALES.md','07_COMPARATIVA_VERSIONES.md','08_PLAN_FUTURO.md']
qa={'expected_reports':len(expected),'reports_present_nonempty':sum((R/n).exists() and (R/n).stat().st_size>300 for n in expected),'png_count':len(rows),'png_decode_errors':bad,'missing_capture_references':missing,'input_integrity_ok':not result['differences']}
(D/'verificacion_entrega.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False),encoding='utf8');print(json.dumps(qa,indent=2));assert qa['reports_present_nonempty']==8 and not bad and not missing and qa['input_integrity_ok']
