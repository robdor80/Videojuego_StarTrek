from pathlib import Path
import json,hashlib,shutil,csv
R=Path(__file__).resolve().parents[1];D=R/'Data'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def read(n):return json.loads((D/n).read_text(encoding='utf-8-sig'))
copy=read('copy_verified.json');manifest=read('copy_manifest.json');source=Path(copy['source'])/'Unreal'
integrity={'ok':False,'original_project_files_checked':0,'original_project_differences':[],'original_blends_checked':0,'original_blend_differences':[],'work_baseline_content_differences':[]}
for row in manifest:
 p=source/row['path'];h=sha(p) if p.exists() else None;integrity['original_project_files_checked']+=1
 if h!=row['sha256']:integrity['original_project_differences'].append(row['path'])
 if row['path'].split('/')[0] not in ['Saved','Intermediate','DerivedDataCache'] and '/Intermediate/' not in row['path']:
  p=R/'Unreal'/row['path'];h=sha(p) if p.exists() else None
  if h!=row['sha256']:integrity['work_baseline_content_differences'].append(row['path'])
for path,h in read('original_blend_hashes.json').items():
 integrity['original_blends_checked']+=1
 if sha(Path(path))!=h:integrity['original_blend_differences'].append(path)
integrity['ok']=not integrity['original_project_differences'] and not integrity['original_blend_differences']
assert integrity['ok'],'Original integrity difference: preserve and report'
mp=R/'Unreal/Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap'
integrity['saved_map_sha256']=sha(mp)
backup=R/'Backups/L_Sutherland_Ergonomia03_Bloqueo_D04.umap'
if not backup.exists():shutil.copy2(mp,backup)
assert sha(backup)==sha(mp)
new_assets=[]
for p in (R/'Unreal/Content/F07COLL01/Ergonomia03').rglob('*.uasset'):new_assets.append({'path':p.relative_to(R).as_posix(),'size':p.stat().st_size,'sha256':sha(p)})
integrity['derived_assets']=new_assets
(D/'final_integrity.json').write_text(json.dumps(integrity,indent=2),encoding='utf-8')
integration=read('integration.json');verified=read('saved_verification.json');runtime=read('limited_runtime_check.json');primitives=read('primitive_collision_inventory.json');plan=read('export_meshes.json')
assert integration['ok'] and verified['ok'] and primitives['ok']
passed=sum(c['passed'] for c in runtime['checks']);failed=[c for c in runtime['checks'] if not c['passed']]
chairs=integration['chair_checks'];assert chairs['all_pass'] and len(chairs['chairs'])==6
with (D/'mallas_actualizadas.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f);writer.writerow(['tipo','actor','componente','fuente','antes','despues'])
 for typ,key in [('visual','visual'),('colision_dependiente','collisions'),('hoja_puerta','doors')]:
  for x in integration[key]:writer.writerow([typ,x['actor'],x.get('component',''),next((v['source'] for v in plan['visual'] if 'VIS_'+v['actor_source']==x['actor']),''),x['before'],x['after']])
report=f'''# USS Sutherland — Parte A: estado recuperable con bloqueo D04

Fecha: 27/10/2026, Europe/Madrid. **PARTE A INCOMPLETA: D04 no supera la apertura jugable.**
Se detiene la integración funcional en este punto. No se ha eliminado, movido ni rebajado ninguna silla lateral para resolver problemas.

## Base elegida y proyecto

- Base: **SUTHERLAND_VISUAL_02**. Recuperación física: `{copy['source']}`.
- Proyecto de trabajo único: `{R/'Unreal/SutherlandPlayable01.uproject'}`.
- Nivel: `/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01`.
- UE5.8.2 CL56702186 y Blender 5.2.2 LTS comprobados en los logs.
- Las antiguas rutas Documents/StarTrek_3D/PLAYABLE_01 y VISUAL_02 ya no existen. Se localizaron respaldos de reorganización y se leyó su documentación.
- El mapa de VISUAL_02 recuperado coincide con su hash histórico verificado `935938535e566b9187cd58fe8aa86a16be97a53a4d978a5be53e85a64ad7b417`.
- PLAYABLE_01 es el antecesor funcional. VISUAL_02 conserva sus sistemas y su mejora visual. INTEGRACION_FINAL_01 fue contrastada en el rescate TABULA RASA: había retirado las seis sillas y 84 actores visuales; no se adoptó esa retirada. Los laboratorios experimentales no se incorporaron.
- Copia física: {copy['files']} archivos, {copy['bytes']:,} bytes, verificados por SHA-256 antes de intervenir. Los originales permanecen separados y no se guardó sobre ellos.

## Etapas

| Etapa | Estado |
|---|---|
| A.1 Recuperar base | Verificada |
| A.2 Copia protegida | Verificada |
| A.3 Integrar geometría | Guardada y reabierta; 39 mallas visuales comprobadas |
| A.4 Conservar funcionamiento | Seis sillas y Quinn superan comprobaciones limitadas; D04 bloquea el cierre |
| A.5 Recuperación/documentación | Guardada, con estado anterior y estado integrado disponibles |

## Geometría, referencias y materiales

Se han actualizado **31 mallas visuales**, **ocho hojas móviles** y **51 grupos de colisión dependientes**, conservando los actores originales y sus nombres/referencias. Se importaron {len(new_assets)} assets derivados en `/Game/F07COLL01/Ergonomia03`; las mallas anteriores permanecen disponibles dentro de la misma copia. No hay otro proyecto ni nivel sustitutivo.

Las dos consolas centrales, agrupadas en Ergonomia_03, se exportaron en las 18 partes que espera VISUAL_02. Se comprobó la correspondencia de la topología antes de repartirlas. Las demás piezas actualizadas son los cinco objetos del capitán, paneles/carcasa/pantallas laterales, marcos y paneles interiores del turbo. Lista exacta de actores, assets anteriores y nuevos: `Data/mallas_actualizadas.csv`, `export_meshes.json` e `integration.json`.

Se mantuvieron los pivotes y transformaciones de los actores; la adaptación se exportó desde las coordenadas de Ergonomia_03. No se aplicó escala global. Los vértices guardados de las 31 visuales y ocho hojas se cotejaron en ambos sentidos con tolerancia 0,005 cm. Las ocho colisiones de hoja fueron extraídas del motor al reabrir: sus límites verticales coinciden con la geometría nueva dentro de 0,05 cm; no conservan los antiguos 391 cm.

Los materiales PBR originales se reasignaron por nombre importado y por correspondencia de cara con el Blender de VISUAL_02. Los nombres básicos del Blender Ergonomia_03 no sustituyeron esos grafos. UV de la geometría exportada conservados. No se regeneraron texturas ni se simplificaron materiales. Luces, cámara, TSR, Lumen y VSM permanecen heredados. La inspección GPU mostró el puente texturizado; no certifica aprobación artística ni equivalencia con Blender.

## Condición obligatoria: seis sillas laterales y capitán

Hay exactamente **Chair01–Chair06**, cada una con base fija, MovingRig y **15 componentes móviles**, además de la silla del capitán. Sus propiedades, mallas, materiales, transformaciones y actores visuales adjuntos coinciden con la línea base guardada. Ninguna silla lateral se importó de nuevo, se duplicó, se eliminó, se trasladó o cambió de altura.

Las seis completaron un ciclo nativo Toggle/AdvanceChair con barridos reales: recorrido 57 cm, retorno 0 cm de error, bases fijas y ninguna obstrucción. Detalles individuales en `Data/integration.json/ chair_checks`. La reapertura confirmó las conexiones y posiciones guardadas.

**Límite heredado comprobado:** VISUAL_02 contiene un solo STSeatAnchor con clips Sit/Seated/Stand, correspondiente al capitán. Los seis laterales tienen desplazamiento, ocupación y detección de obstrucción mediante STSlidingChair. No se encontraron seis sistemas de animación de sentarse/levantarse laterales que pudieran recuperarse; no se inventaron ni reconstruyeron en esta Parte A.

## Quinn y comprobación jugable limitada

Se conserva STPlayableQuinn, SKM_Quinn_Simple, ABP_Unarmed, controlador, controles y cámara. Escala de malla 1, cápsula radio 35 / semialtura 90 cm. Se preserva la referencia corporal histórica de **177,3 cm**; no se redimensionó a Quinn.

Los cinco marcadores de pose sentada del capitán se bajaron 14,8 cm para acompañar el sillón aceptado; Approach y Exit quedaron sobre el suelo original. Los tres clips y la lista de actores de colisión del asiento permanecen iguales.

Prueba GPU limitada, reutilizada del guion de VISUAL_02: **{passed}/{len(runtime['checks'])} comprobaciones superadas**. Se verificaron posesión real, caminar con W y animación, interacción E, sentado con bloqueo de caminar, protección frente a salida ocupada, levantarse, cápsula y locomoción recuperadas. No se afirma circulación completa del puente ni prueba exhaustiva.

## Bloqueo D04 — no declarar completada la Parte A

Resultado fallido literal: `{failed}`.

D04 acepta la solicitud de Quinn y conserva los permisos/destino construidos, pero su fracción de apertura no alcanza 1 durante Tick. El mecanismo no queda validado como funcional con las mallas/colisiones nuevas. No se ha diagnosticado qué componente impide el movimiento; no se atribuye una causa exacta sin un barrido de contacto.

Se conserva el código, Blueprint, configuración, geometría y mapa anterior de VISUAL_02. No se ha forzado la apertura, desactivado colisiones, inventado una habitación ni cambiado destinos/permisos. D01–D03 siguen bloqueadas por destino no construido; D04 sigue siendo la única que tiene cabina. No hay viaje entre cubiertas.

**Siguiente intervención necesaria para cerrar A.4:** diagnosticar únicamente los contactos de las hojas D04 con las mallas y colisiones nuevas y contrastar con el estado anterior conservado. Si no se puede conciliar sin cambiar la geometría aprobada o los mecanismos de forma segura, conservar ambos y consultar la decisión concreta. No modificar sillas laterales ni emprender la Parte B para ocultar este bloqueo.

## Inventario de colisiones

- {len(primitives['after'])} componentes primitivos inventariados: perfiles, canales Pawn/Camera, transformaciones, cajas, sensores y mallas; `Data/primitive_collision_inventory.json`.
- 330 actores técnicos SM_COLL presentes en la base y en la copia integrada.
- **279** permanecen idénticos al reabrir.
- **51** grupos afectados se adaptaron reutilizando cada hull anterior y su correspondencia con la superficie fuente. No se reemplazó la arquitectura general. Se conserva el número de formas por grupo; las cajas afectadas pueden quedar representadas como hulls UCX tras deformarlas. Esta representación y el ajuste superficial requieren revisión dirigida en B; no equivalen a certificar todas las paredes/objetos.
- Las tres barreras de destinos no construidos se conservaron y redujeron en altura; no mantienen el antiguo límite superior. Los sensores de puerta acompañan la nueva altura de paso. Las ocho hojas conservan un hull convexo cada una.
- La incidencia **pies suspendidos** permanece abierta hasta verificar expresamente apoyo y ergonomía. Completar la animación no demuestra su resolución.

## Incidencias técnicas conservadas

Los primeros intentos de guion encontraron una propiedad FBX inexistente y una suposición incorrecta sobre el perfil Custom de las visuales; se corrigió el guion sin guardar el nivel de esos intentos. Se conservan JSON/logs. El comprobador histórico de sillas se quedó esperando FinishAllCompilation; no se declaró aprobado. Se sustituyó por seis ciclos reales limitados, que sí produjeron resultados explícitos. Los procesos detenidos no tenían una escritura de mapa activa; se comprobó el hash original antes del guardado válido.

Los intentos de juego con NullRHI no completaron una prueba válida. El lanzamiento ExecCmds inicial tampoco transmitió el nombre de guion por las comillas de la ruta; se ejecutó desde la consola de la ventana real y se obtuvo el resultado GPU de 13 comprobaciones. Los datos incompletos se conservan separados y no se presentan como éxitos.

VSM Non-Nanite Marking Job Queue overflow, diferencias visuales heredadas y ergonomía de pies siguen documentados. No se hizo benchmark nuevo ni conversión Nanite.

## Integridad y recuperación

Hash del mapa integrado guardado: `{integrity['saved_map_sha256']}`.

Rehash final: **{integrity['original_project_files_checked']}/{copy['files']} archivos del proyecto fuente y {integrity['original_blends_checked']} Blender originales sin diferencias**. `Data/final_integrity.json` conserva resultados y SHA-256 de todos los assets derivados. Cambios en archivos previos de la copia fuera de cachés: `{integrity['work_baseline_content_differences']}`. No hubo commit, push, pull request ni modificación de los originales.

- Estado original funcional: `Backups/BeforeIntegration/L_Sutherland_Playable01.umap`, con las mallas antiguas todavía disponibles en sus rutas /Game originales.
- Estado integrado con bloqueo D04: `Backups/L_Sutherland_Ergonomia03_Bloqueo_D04.umap`, idéntico por SHA-256 al mapa activo.
- Estado intermedio anterior al ajuste de barreras: `Backups/L_Sutherland_Playable01_BeforeGuardAdaptation.umap`.
- Instrucciones operativas: `CONTINUAR_AQUI.md`. No repetir 01_prepare ni 07_integrate sobre este estado; 07 se protege frente a un segundo ajuste de marcadores.

## Pendientes posteriores

Antes de cerrar Parte A: resolver/verificar D04 conservando ambos estados y las seis sillas.

Parte B: revisión sistemática de paredes/objetos, superficies adaptadas, circulación y colisiones. Parte C: revisión visual/ergonómica completa, apoyo de pies, cámaras y ajuste futuro de alturas de seis sillas únicamente cuando se autorice. No se ejecutaron esas fases.
'''
(R/'INFORME_PARTE_A.md').write_text(report,encoding='utf-8')
checkpoint=R/'CONTINUAR_AQUI.md';hist=R/'HISTORIAL_ETAPAS.md'
if not hist.exists():shutil.copy2(checkpoint,hist)
checkpoint.write_text(f'''# CONTINUAR AQUÍ — USS Sutherland Ergonomia_03 Parte A

27/10/2026, Europe/Madrid. **PARTE A INCOMPLETA. Pausa técnica segura por bloqueo D04.**

## Estado guardado

Proyecto único: `{R/'Unreal/SutherlandPlayable01.uproject'}`.
Mapa: `/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01`.
Base recuperada: VISUAL_02, `{copy['source']}`.

A.1 y A.2 verificadas. A.3 guardada y reabierta: 31 visuales, ocho hojas, 51 grupos físicos adaptados. A.4 parcial: seis mecanismos laterales aprobados, Quinn y capitán aprobados en comprobación limitada; D04 acepta acceso pero no abre completamente. A.5 documentada y recuperable.

**Condición protegida:** exactamente seis sillas laterales Chair01–06 (15 piezas móviles cada una) más capitán. Posiciones/alturas laterales y componentes originales preservados. Seis ciclos reales 57 cm ida/retorno0 aprobados. No duplicar/importar/eliminar sillas. Solo el capitán tenía anclaje de animación para sentarse en VISUAL_02; no inventar seis sistemas laterales ausentes.

## Punto exacto de reanudación

Leer `INFORME_PARTE_A.md`, `Data/limited_runtime_check.json` (12/13, falla apertura D04), `Data/integration.json`, `Data/saved_verification.json` y `Data/primitive_collision_inventory.json`.

No reimportar el puente ni reconstruir mecanismos. Diagnosticar **solo D04**: comparar hoja visual/collider nuevo y contactos contra el estado anterior. Conservar destinos/permisos. D01–D03 siguen bloqueadas. No aplicar un arreglo que cambie la geometría aprobada o las seis sillas; documentar y consultar si esa fuera la única salida segura. Hasta entonces no declarar completada A.

Para abrir la copia: `Abrir_Editor.cmd`. Para arrancar juego normal: `Jugar_Standalone.cmd` (D04 sigue sin validarse; no confundir con una entrega funcional cerrada). Controles heredados WASD, ratón, Shift, Espacio y E para el capitán.

Verificación guardada de solo lectura, opcional tras cerrar Unreal:
```powershell
& 'C:/Program Files/Epic Games/UE_5.8/Engine/Binaries/Win64/UnrealEditor-Cmd.exe' '{(R/'Unreal/SutherlandPlayable01.uproject').as_posix()}' -run=pythonscript -script='{(R/'Scripts/08_verify_saved.py').as_posix()}' -unattended -nop4 -nosplash -NullRHI
```
Las rutas de script deben usar `/`; `\\03` fue interpretado como escape en un intento inicial. No ejecutar pruebas de juego con NullRHI. Si se reanuda una prueba asíncrona, usar la consola de Unreal `py "ruta del guion"`; no usar el guion de integración otra vez.

## Ambos estados conservados

- `Backups/BeforeIntegration/L_Sutherland_Playable01.umap`: original VISUAL_02, hash 935938535e566b9187cd58fe8aa86a16be97a53a4d978a5be53e85a64ad7b417. Las mallas antiguas siguen en Content, no fueron sobrescritas.
- `Backups/L_Sutherland_Ergonomia03_Bloqueo_D04.umap`: estado integrado activo, hash {integrity['saved_map_sha256']}.
- Fuente completa VISUAL_02 fuera de esta copia, intacta.

Para recuperar un mapa, cerrar el editor y copiar el respaldo elegido sobre **el mapa de ESTA copia de trabajo**, manteniendo la ruta y nombre `Unreal/Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap`. Conservar antes el otro estado. No abrir el respaldo como si fuera un nuevo proyecto ni sobrescribir el proyecto fuente.

## Integridad y límites

`Data/final_integrity.json`: {copy['files']} archivos fuente y {integrity['original_blends_checked']} Blender originales sin diferencias. Único proyecto de trabajo. No commit/push/PR. Sin borrado manual de cachés ni temporales.

Pies suspendidos y VSM abiertos. Las colisiones generales y la ergonomía de sillas son Partes B/C, pendientes. El historial técnico está en `HISTORIAL_ETAPAS.md` y Logs; los intentos incompletos no cuentan como pruebas aprobadas.
''',encoding='utf-8')
for filename,extra in [('Abrir_Editor.cmd',''),('Jugar_Standalone.cmd',' -game -windowed')]:
 (R/filename).write_text('@echo off\r\nstart "" "C:\\Program Files\\Epic Games\\UE_5.8\\Engine\\Binaries\\Win64\\UnrealEditor.exe" "%~dp0Unreal\\SutherlandPlayable01.uproject"'+extra+'\r\n',encoding='ascii')
(D/'STATUS.json').write_text(json.dumps({'part_a_complete':False,'status':'BLOCKED_D04_OPENING','safe_checkpoint':True,'six_lateral_chairs_preserved':True,'six_chair_mechanisms_tested':True,'runtime_passed':passed,'runtime_total':len(runtime['checks']),'map_sha256':integrity['saved_map_sha256'],'original_integrity_ok':True},indent=2),encoding='utf-8')
print('CHECKPOINT_WRITTEN',integrity['ok'],'ORIGINALS',integrity['original_project_files_checked'],integrity['original_blends_checked'],'DERIVED',len(new_assets),'RUNTIME',passed,len(runtime['checks']),'WORK_DIFFERENCES',integrity['work_baseline_content_differences'],flush=True)
