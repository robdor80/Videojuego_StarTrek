from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'Data';P=R/'Unreal';B=R/'Backups/Puertas_20261028'
def read(name):return json.loads((D/name).read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(4*1024*1024),b''):h.update(c)
 return h.hexdigest()
fix=read('doors_20261028_fix.json');tests=read('doors_20261028_validation.json');repeat=read('doors_20261028_repeat_validation.json');saved=read('doors_20261028_saved_verification.json')
assert all(x['ok'] for x in [fix,tests,repeat,saved])
previous=read('final_integrity.json');manifest=read('copy_manifest.json');source=Path(read('copy_verified.json')['source'])/'Unreal'
allowed={Path(x['package']).relative_to(R).as_posix():x for x in fix['modified']}
out={'ok':False,'date':'2026-10-28 Europe/Madrid','scope':'Doors only','source_checked':0,'blends_checked':0,'working_baseline_checked':0,'derived_checked':0,'modified_assets':[],'unexpected_changes':[]}
for row in manifest:
 path=source/row['path'];out['source_checked']+=1
 if not path.exists() or sha(path)!=row['sha256']:out['unexpected_changes'].append({'original':str(path)})
 if row['path'].split('/')[0] not in ['Saved','Intermediate','DerivedDataCache'] and '/Intermediate/' not in row['path']:
  path=P/row['path'];expected=fix['map_before_sha256'] if row['path']=='Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap' else row['sha256'];out['working_baseline_checked']+=1
  if not path.exists() or sha(path)!=expected:out['unexpected_changes'].append({'working':str(path)})
for row in previous['derived_assets']:
 path=R/row['path'];h=sha(path);out['derived_checked']+=1
 if row['path'] in allowed:
  f=allowed[row['path']];assert h==f['after_sha256'];assert sha(Path(f['backup']))==f['before_sha256'];out['modified_assets'].append({'path':row['path'],'before':f['before_sha256'],'after':h,'render_uv_material_unchanged':True})
 elif h!=row['sha256']:out['unexpected_changes'].append({'derived':row['path']})
for p,h in read('original_blend_hashes.json').items():
 out['blends_checked']+=1
 if sha(Path(p))!=h:out['unexpected_changes'].append({'original_blend':p})
assert not out['unexpected_changes'],out['unexpected_changes'];assert len(out['modified_assets'])==8
mp=P/'Content/SutherlandPlayable01/Maps/L_Sutherland_Playable01.umap';out['map_sha256']=sha(mp);assert out['map_sha256']==fix['map_before_sha256']
final=B/'Resultado_validado'
for row in fix['modified']:
 src=Path(row['package']);dest=final/'Content'/src.relative_to(P/'Content');dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():shutil.copy2(src,dest)
 assert sha(src)==sha(dest)
dest=final/mp.name
if not dest.exists():shutil.copy2(mp,dest)
assert sha(mp)==sha(dest)
out['ok']=True;(D/'doors_20261028_final_integrity.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
for src,name in [(R/'CONTINUAR_AQUI.md','CONTINUAR_AQUI_ANTES.md'),(D/'STATUS.json','STATUS_ANTES.json')]:
 if not (B/name).exists():shutil.copy2(src,B/name)
rows='\n'.join('| '+x['door'].removeprefix('DOOR_F07_')+' | '+str(x['floor_cm'])+' | '+str(x['collision_lower_world_z_cm'])+' | Dos hojas; 3 ciclos mecánicos correctos |' for x in fix['modified'] if x['side']=='LeftLeaf')
report=f'''# USS Sutherland — Corrección exclusiva de puertas

28/10/2026, Europe/Madrid. **Intervención de puertas terminada y verificada tras reabrir.** No se han iniciado otras fases ni continuado la auditoría general de integración.

## Proyecto utilizado

`{P/'SutherlandPlayable01.uproject'}`

Mapa: `/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01`. Se reutilizó la misma copia de trabajo, derivada de VISUAL_02. No se creó otro proyecto.

## Causa y reparación

Las colisiones importadas de las hojas incluían la parte visual oculta bajo el suelo. En D02 y D04 llegaban a Z=-2,3589 cm. En ejecución, el barrido de D04 comenzaba penetrando `SM_COLL_Circle_0_05` y `SM_COLL_P03G_D04_RightLowerReturn_01`: el código existente recibía un impacto y dejaba la puerta obstruida. No faltaban el Blueprint, los permisos ni la solicitud de Quinn.

Se recortó **solo la colisión inferior de las ocho hojas**, hasta 0,2 cm sobre su suelo local (0,3 cm en D04, cuyo suelo de cabina está a 0,1 cm). Se retuvo un hull convexo por hoja y su extremo superior. La parte dibujada bajo el suelo permanece intacta. No se movieron ni reescalaron las hojas, no se importó de nuevo el puente y no se cambiaron suelo, retornos, marcos o colisiones generales.

| Puerta UE | Suelo Z, cm | Límite inferior del collider Z, cm | Resultado mecánico |
|---|---:|---:|---|
{rows}

Se modificaron únicamente los `BodySetup` de ocho StaticMesh ya usados por `LeftLeaf` y `RightLeaf` de `P03FG_D001`–`P03FG_D004`, en `/Game/F07COLL01/Ergonomia03/Leaves/`. Rutas y hashes exactos: `Data/doors_20261028_fix.json` y `doors_20261028_final_integrity.json`.

## Mecanismos reutilizados

Blueprint conservado: `/Game/F07P03FG/Blueprints/BP_ST_AutomaticDoor_Sutherland`.
Clase/plugin conservados: `STAutomaticDoor` / `STAutomaticDoors`, de VISUAL_02. Se reutilizan las dos hojas, sus posiciones cerradas, recorridos, sensores de aproximación/ocupación, intención de paso, autorización, apertura, cierre y protecciones existentes.

**Cero cambios en Blueprints, código C++, binarios o configuración de Quinn.** No se creó un nuevo mecanismo. Los perfiles de colisión y los componentes móviles originales se mantienen.

## Pruebas realmente ejecutadas

- Diagnóstico en PIE, con barridos reales de las hojas: contacto inicial contra suelo y retorno inferior identificado. `doors_20261028_runtime_diagnosis.json`. Los contactos de D01/D03 recogidos en ese diagnóstico preliminar se produjeron por un error del guion al acumular la referencia de posición; no se utilizan como prueba de fallo de sus guías. La validación posterior usa copias de coordenadas y el recorrido correcto.
- Las ocho hojas completaron recorrido horizontal en sentidos opuestos y retorno, con barridos activos y sin impactos contra marcos. Se verificaron tanto posición de cierre como desplazamiento del collider unido a la hoja, tolerancia 0,001 cm.
- **Tres ciclos mecánicos consecutivos para cada una de las cuatro puertas**, ambas hojas: 12 rondas de mecanismo / 24 ciclos de hoja, sin bloqueos ni deriva. `doors_20261028_repeat_validation.json`: 3/3 comprobaciones y todas las rondas correctas.
- **Quinn real y poseído** activó D04 por aproximación desde el puente, caminando con la entrada W a través de su PlayerController. D04 abrió por completo y cerró automáticamente en **tres ciclos consecutivos**. `doors_20261028_validation.json`: 18/18 comprobaciones.
- Quinn entró caminando en la cabina existente y regresó al puente; se verificó apoyo en el suelo de cabina. Solo la posición inicial del escenario se preparó de forma controlada; no se presenta esta prueba como auditoría completa de circulación.
- Tres carriles de sonda de cápsula (Y=-25, 0, +25 cm) contra las hojas: bloquean cerradas y dejan paso abiertas. Se repitió durante los ciclos; no quedó la antigua barrera de hoja en la posición cerrada.
- Reapertura en otro proceso: ocho hulls correctos, perfiles activos y límites inferiores nuevos. Digest de vértices, índices, normales, tangentes, UV y materiales **idéntico** al anterior en las ocho mallas visibles. `doors_20261028_saved_verification.json`.

## Seguridad y límites

D04 es la puerta con cabina disponible y apertura automática validada con Quinn. D01–D03 conservan los tres bloqueos de destino no construido; sus mecanismos se probaron de forma controlada, sin habilitar circulación ni cambiar los permisos guardados. No se ha inventado suelo, habitación, corredor o destino. No hay transporte entre cubiertas.

Esta intervención no certifica todas las colisiones del puente, ergonomía o rendimiento. Pies suspendidos y la incidencia VSM quedan como antecedentes sin intervenir. Las seis sillas laterales, el capitán, las consolas, las cámaras y demás sistemas permanecen como estaban.

## Protección y recuperación

- Antes de modificar: respaldo del mapa y de cada uno de los ocho paquetes, con SHA-256, en `{B}`.
- Resultado validado, ocho paquetes y mapa de referencia: `{final}`.
- Mapa activo sin cambios: SHA-256 `{out['map_sha256']}`.
- Rehash final de {out['source_checked']} archivos del proyecto histórico y {out['blends_checked']} Blender originales: sin diferencias.
- Verificados {out['working_baseline_checked']} archivos previos no regenerables de la copia y los 90 assets derivados. Únicas modificaciones de assets: **las ocho hojas autorizadas**; los otros 82 derivados y el contenido previo del proyecto permanecen intactos.
- Las seis sillas (15 piezas móviles cada una), actores visuales adjuntos, Quinn y GameMode coinciden con la línea base al reabrir. La silla del capitán y sus marcadores no se cambiaron en esta intervención; el mapa es idéntico.
- Sin commit, push, PR, borrado de históricos ni cambios en proyectos originales.

## Reanudación

Abrir `Abrir_Editor.cmd` o el .uproject indicado. `Jugar_Standalone.cmd` inicia el juego normal. No repetir `15_fix_door_collisions.py`: se protege frente a una segunda aplicación. Los datos válidos son los cuatro JSON de fix, validation, repeat_validation y saved_verification, todos con `ok=true`; los intentos preliminares se conservan por separado.

Para restaurar, cerrar Unreal y recuperar **solo los ocho paquetes de hojas** desde el respaldo anterior o desde Resultado_validado, manteniendo sus rutas Content en esta copia de trabajo. El mapa no necesita restauración para esta corrección, pues no cambió.

La intervención termina aquí. Cualquier continuación de integración o fases posteriores requiere una nueva instrucción; no se inicia automáticamente.
'''
(R/'INFORME_PUERTAS_20261028.md').write_text(report,encoding='utf-8')
(R/'CONTINUAR_AQUI.md').write_text(f'''# USS Sutherland — último estado guardado

28/10/2026, Europe/Madrid. **Corrección exclusiva de puertas terminada. No continuar con otros trabajos automáticamente.**

Proyecto: `{P/'SutherlandPlayable01.uproject'}`.
Mapa: `/Game/SutherlandPlayable01/Maps/L_Sutherland_Playable01`.

El bloqueo D04 registrado el 27/10 queda resuelto: los colliders de las hojas penetraban el suelo/retorno inferior. Se corrigieron únicamente los BodySetup de las ocho hojas, sin cambiar mallas visibles, UV, materiales, actores o código. El mapa conserva exactamente su SHA-256 anterior.

## Estado validado

- Ocho hojas / cuatro mecanismos: tres ciclos mecánicos consecutivos por puerta, sin impactos o deriva y con sus colliders acompañando el movimiento.
- D04: tres aperturas automáticas por aproximación real de Quinn desde el puente, tres cierres automáticos y entrada/salida de la cabina existente.
- D01–D03: mecanismos preparados, acceso bloqueado por destinos no construidos. No desbloquear ni permitir caída al vacío.
- Sondas de cápsula: hojas cerradas bloquean; abiertas dejan los tres carriles comprobados libres.
- Reapertura y digest de geometría visible, normales, tangentes, UV y materiales de ocho hojas: sin cambios.
- Seis sillas laterales, capitán, consolas, Quinn y resto del puente intactos en esta intervención.

## Evidencia y recuperación

Leer `INFORME_PUERTAS_20261028.md`.
Datos actuales:
- `Data/doors_20261028_fix.json`: ocho paquetes modificados, todos respaldados.
- `Data/doors_20261028_validation.json`: 18/18 comprobaciones.
- `Data/doors_20261028_repeat_validation.json`: tres rondas por cada puerta.
- `Data/doors_20261028_saved_verification.json`: ocho hojas reabiertas correctamente.
- `Data/doors_20261028_final_integrity.json`: originales intactos; cambios limitados a ocho hojas.

Respaldos anteriores: `{B}`.
Resultado validado recuperable: `{final}`.
Mapa activo: SHA-256 `{out['map_sha256']}`.

Abrir con `Abrir_Editor.cmd`, jugar con `Jugar_Standalone.cmd`. No repetir la importación del puente ni aplicar otra vez el script 15. Si una interrupción obliga a recuperar, cerrar Unreal y restaurar únicamente los ocho paquetes de hojas, manteniendo las rutas de Content; conservar ambos respaldos.

El informe de Parte A del 27/10 se conserva como histórico. No se han realizado hoy las fases B, C, D o E, ni se está declarando completada otra fase distinta a esta corrección de puertas. Pies suspendidos, ergonomía y VSM permanecen fuera de alcance.
''',encoding='utf-8')
status=read('STATUS.json');status['previous_status_20261027']=dict(status);status['status']='DOORS_FIXED_OTHER_WORK_NOT_ASSESSED';status['doors_correction_complete']=True;status['doors_validation_passed']=18;status['doors_validation_total']=18;status['doors_three_mechanical_cycles_per_door']=True;status['map_sha256']=out['map_sha256'];status['current_report']='INFORME_PUERTAS_20261028.md'
(D/'STATUS.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
print('DOORS_CLOSED_OK',out['source_checked'],out['blends_checked'],out['working_baseline_checked'],len(out['modified_assets']),flush=True)
