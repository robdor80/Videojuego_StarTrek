import pathlib,json,hashlib,shutil,csv,datetime
R=pathlib.Path(__file__).parent;P=R.parent/'Unreal'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
    return h.hexdigest()
audit=json.loads((R/'local_audit.json').read_text());diff=[]
for row in audit['manifest']:
    p=P/row['path']
    if not p.exists() or sha(p)!=row['sha256']:diff.append(row['path'])
assert not diff,diff
suite=json.loads((R/'Data/final_suite_verified.json').read_text());assert len(suite['results'])==3 and all(t['ok'] for t in suite['results']),suite
verify=json.loads((R/'saved_verification.json').read_text());assert verify['ok'],verify.get('error')
source=R.parents[2]/'blender/Miranda_Puente_Sutherland_PBR_Manual_01_Seis_Sillas_01.blend';snapshot=R/'Backups/Fuente_PBR_SeisSillas_20261029.blend';assert sha(source)==sha(snapshot)
assets=[{'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted((P/'Content/SutherlandPBR01').rglob('*')) if p.is_file()]
result=R/'Backups/Resultado_Validado_20261029';assert not result.exists();result.mkdir()
mapfile=P/'Content/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01.umap';shutil.copy2(mapfile,result/mapfile.name);assert sha(mapfile)==sha(result/mapfile.name)
out={'ok':True,'date':datetime.datetime.now().astimezone().isoformat(),'baseline_checked':len(audit['manifest']),'baseline_changes':diff,'source_sha256':sha(source),'source_matches_frozen_copy':True,'map_sha256':sha(mapfile),'new_assets':assets,'tests':suite['results'],'new_asset_count':len(assets),'mesh_count':175,'lights':16,'backups_verified':[]}
for p in (R/'Backups').rglob('*'):
    if p.is_file():out['backups_verified'].append({'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
(R/'final_integrity.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
with (R/'inventario_recursos.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(assets)
print('FINAL_INTEGRITY',out['baseline_checked'],out['baseline_changes'],out['new_asset_count'],out['tests'],out['map_sha256'])
report=f'''# USS Sutherland — auditoría de reanudación e integración PBR

29/10/2026, Europe/Madrid. Estado final guardado, reabierto y probado con GPU en UE 5.8.2 CL56702186. Blender 5.2.2 LTS.

## Qué existía al retomar la sesión

La inspección inicial fue de lectura: archivo de continuidad, estado Git, fechas de archivos, procesos, informes, manifiestos, registros y conversación anterior «Replicar las seis sillas operativas».

El turno interrumpido contiene las instrucciones de integración e iluminación, pero no contiene operaciones de integración ejecutadas. No se encontraron exportaciones nuevas del PBR, carpeta Content/SutherlandPBR01, mapa L_Sutherland_PBR_SeisSillas_01, pruebas nuevas ni proceso Unreal activo. Por tanto, no había una importación PBR parcial que repetir o sustituir. Blender seguía abierto.

Sí existían estos resultados anteriores, que se conservaron:

- Blender: Miranda_Puente_Sutherland_PBR_Manual_01_Seis_Sillas_01.blend y .blend1; seis puestos completos. Informe_Seis_Sillas_01.md, seis_sillas_manifest.json, seis_sillas_antes.json y seis_sillas_verificacion.json; cinco scripts seis_sillas y capturas. Las cinco sillas antiguas siguen recuperables en la colección oculta SS_Originales_5_Recuperables.
- Unreal, 27/10: integración de Ergonomía_03 en L_Sutherland_Playable01; 31 mallas visuales, ocho hojas y 51 grupos de colisión actualizados; 90 recursos derivados en F07COLL01/Ergonomia03. No era la nueva versión PBR de Blender del 29/10.
- Unreal, 28/10: reparación de BodySetup de ocho hojas, con 18/18 pruebas de puertas, tres ciclos por mecanismo, paso real de Quinn por D04 y reapertura. Las pruebas de Quinn del 27/10 eran 12/13, con el bloqueo D04 posteriormente corregido.
- Todos los Backups anteriores, incluidos BeforeIntegration, Puertas_20261028 y Resultado_validado; Scripts 01–19, Data, Logs, Config, Blueprints, C++ y binarios anteriores.

La auditoría verificó de nuevo el hash del mapa anterior y los ocho paquetes de hojas: todos coinciden con doors_20261028_final_integrity.json. El mapa histórico conserva SHA-256 cff10a2af8d8926d85951834d63b31117d0fe3420bb50007ae24ed8be9792d29.

## Qué estaba pendiente y se ha reanudado

Faltaban la exportación de la fuente actual, traducción de sus materiales, mapa independiente, nuevas sillas y plataformas, iluminación UE, colisiones para esa geometría y pruebas nuevas. Se trabajó únicamente en esos puntos, reutilizando el proyecto, Quinn, GameMode, ancla del capitán y cuatro mecanismos de puertas.

Durante la auditoría se detectó un guardado externo de Blender. Entre ambas lecturas solo cambió el grafo BLUE: geometría, imágenes y asignaciones de silla coinciden. Se congeló una copia independiente en Backups/Fuente_PBR_SeisSillas_20261029.blend. El archivo fuente actual y esa copia siguen coincidiendo: SHA-256 {out['source_sha256']}. Ningún script de esta intervención guarda un .blend original.

## Resultado y rutas

Proyecto: `{P / 'SutherlandPlayable01.uproject'}`.

Mapa nuevo: `/Game/SutherlandPBR01/Maps/L_Sutherland_PBR_SeisSillas_01`.

Archivo: `{mapfile}`.

Abrir `Abrir_Puente_PBR.cmd` en esta carpeta y pulsar Play. WASD y ratón para desplazarse; E cerca de la silla del capitán para sentarse/levantarse; Escape termina PIE. `Jugar_Puente_PBR.cmd` permite iniciar la misma versión como juego en ventana. Abrir solamente el .uproject mantiene el mapa de inicio histórico: seleccionar el mapa nuevo o usar el acceso indicado.

SHA-256 del mapa final: `{out['map_sha256']}`.

## Geometría, materiales e inventario

- 167 mallas estáticas y ocho visuales de hoja: 175 mallas visibles de fuente, conservando posiciones, orientación, escala, UV y asignaciones de cara. No se exportaron las 80 mallas ocultas de las cinco sillas recuperables, cámaras ni los dos objetos Light de Blender.
- Exactamente seis conjuntos laterales, 16 piezas por puesto: silla, pie cilíndrico y plataforma. La silla del capitán también se conserva. Las sillas antiguas no están duplicadas en el mapa nuevo. No se implementó movimiento de plataformas ni nuevos sistemas de sentarse laterales. Los mecanismos laterales históricos siguen disponibles en el mapa anterior.
- 36 imágenes fuente extraídas de sus datos originales, sin bake de luz ni regeneración de texturas. Los grafos UE reproducen color, mezclas, ajustes HSV, UV, metalicidad, rugosidad y normal de la fuente. Se conservan incluso las escalas UV muy pequeñas presentes en el Blender, sin corregirlas artísticamente. Los grafos originales de Blender permanecen intactos.
- LCARS, pantallas, inscripciones y superficies emisivas se conservan como elementos visuales. Sus materiales de presentación usan emisión/unlit según el grafo fuente; no aportan iluminación global al escenario.
- Cada hoja visual nueva conserva los materiales de sus caras y está adjunta al componente móvil correspondiente. El componente de hoja reparado conserva la colisión y permanece oculto visualmente. Los ocho visuales adjuntos usan el perfil NoCollision; así no duplican la colisión física.
- Se retiraron del mapa nuevo las visuales históricas y la fabricación de colisión anterior, sustituidas por colisión compleja estática sobre la geometría nueva. Esas operaciones no borran recursos del proyecto ni cambian el mapa anterior.
- Los cinco mamparos Plane.013_0, Plane.004_0, Plane.010_0, Plane.039_0 y Plane.011_0 bloquean Pawn y Camera e ignoran WorldDynamic para permitir que las hojas entren en sus alojamientos. Esto también afecta a futuros objetos WorldDynamic que se introduzcan frente a esos cinco mamparos; su respuesta es editable. No se cambió su geometría ni se desactivó la protección de Quinn.
- D01–D03 mantienen sus barreras y permisos por destino no construido. Se conserva la barrera histórica de la pantalla principal. D04 conserva su cabina existente. No hay viaje entre cubiertas.

Inventario exacto de los {len(assets)} archivos nuevos, tamaños y hashes: `inventario_recursos.csv` y `final_integrity.json`. Correspondencia fuente/actor/recurso: export.json, integration_result.json, leaf_visual_export.json, leaf_materials.json y saved_verification.json.

## Iluminación exclusivamente en Unreal

Diez RectLight blancas, Movable, de 900 lm; nueve distribuidas por el puente y una en D04. Seis PointLight blancas de relleno, Movable, de 250 lm, con radio de fuente de 100 cm y sombras desactivadas inicialmente. Las áreas principales tienen fuentes de 160 × 140 cm; la de D04, 100 × 100 cm. Exposición inicial fija EV100 3 en el PostProcessVolume del mapa.

Carpetas del Outliner: `Sutherland/Iluminacion/Blanca_Pruebas` y `Sutherland/Iluminacion/Relleno_Techo`. Seleccionar cada actor y editar Transform e intensidad, unidades, color, atenuación, tamaño/radio, sombras, visibilidad y demás comportamiento en Details. Todos son actores/componentes nativos editables; no hay valores de luz horneados en texturas ni un script que los restablezca durante Play.

`Force No Precomputed Lighting` está activo y la iluminación global está desactivada en el PostProcessVolume de este mapa para que las superficies emisivas no iluminen el puente. Esto no modifica los materiales para compensar luz. El proyecto histórico y sus configuraciones permanecen intactos. Los dos Light de Blender se excluyen expresamente. Las luces se crearon desde la API de UE5.

## Pruebas nuevas, realmente ejecutadas

Las tres pruebas finales se ejecutaron secuencialmente en PIE con render GPU D3D SM6, sobre el mapa guardado. `Data/final_suite_verified.json` registra el cierre; los datos detallados están en quinn_verified.json, doors_verified.json y stations_verified.json.

| Comprobación | Resultado |
| --- | --- |
| Quinn poseída, W, animación, E, sentado, obstrucción de salida, levantarse y recuperación de cápsula/locomoción | 13/13 |
| Ocho hojas con barrido completo y retorno; D01–D03 restringidas; tres aperturas/cierres automáticos D04; entrada/salida de cabina y sondas de cápsula | 18/18 |
| Spawn normal y suelo; circulación real con W por el pasillo frente a cada uno de los seis puestos | 8/8 |
| Reapertura independiente: geometría mundial de 175 mallas, seis conjuntos de 16 piezas, ocho visuales unidos, colisiones y 16 luces | Correcta |
| Hash de {len(audit['manifest'])} archivos preexistentes del proyecto, incluidas las hojas reparadas, mapa anterior, configuración, sistemas y binarios | Sin cambios |
| Fuente Blender frente a la copia congelada | Idéntica |

La geometría se cotejó en ambos sentidos con tolerancia de 0,005 cm. Las pruebas jugables usan el Quinn y PlayerController existentes. Las pruebas por puesto y de cabina disponen posiciones iniciales controladas antes de caminar: no se presentan como un recorrido continuo desde el spawn hasta todos los destinos. Las capturas finales de ambos lados y de la zona del capitán están en Capturas con sufijo _Verificada.png.

## Incidencias, reparaciones y límites

Los intentos fallidos se conservan con sus JSON/logs. Durante la integración se corrigieron diferencias de API Python de UE, la dimensión de salida UV exigida por el compilador y el perfil persistente NoCollision de los visuales de hoja. Las primeras pruebas identificaron el contacto de las hojas con los alojamientos; el ajuste de respuestas se validó después. Un guardado de luz encontró el mapa abierto por otro proceso de pruebas (error 32); se cerró ese proceso, se comprobó el estado anterior y se guardó de nuevo. No se perdió ni sustituyó el mapa histórico.

La carga GPU final no presenta errores de compilación de materiales ni avisos VSM. Las primeras cargas sí registraron la advertencia VSM de cola Non-Nanite observada también en el proyecto histórico; no se ha realizado un benchmark ni una conversión Nanite. La iluminación es una base blanca y suave para pruebas, ajustable en UE, no una aprobación artística definitiva. No se declara equivalencia píxel a píxel entre motores.

Quedan para revisión manual detallada las holguras corporales en cada consola, piernas bajo los puestos, apoyo de pies en poses sentadas y circulación exhaustiva por todos los bordes. No se exige ni se ha implementado sentarse en las seis sillas laterales o accionar sus plataformas. Las verificaciones de Blender se conservan como evidencia geométrica, separadas de las pruebas reales de Quinn.

## Recuperación y continuación

Todos los respaldos históricos se conservan. Esta carpeta añade Backups con la fuente congelada, mapa/configuración anteriores, materiales previos a la corrección UV y checkpoints del mapa nuevo. Backups/Resultado_Validado_20261029 contiene una copia verificada del mapa final; los assets asociados permanecen en Content/SutherlandPBR01 y sus hashes constan en el manifiesto.

Para abrir el resultado, usar los accesos indicados. No repetir export_pending.py, integrate_pending.py, finish_leaf_materials.py ni los scripts históricos 01, 07 o 15: ya hay resultados guardados; una continuación debe leer los manifiestos y verificar antes de editar. La restauración de un checkpoint del mapa debe hacerse con Unreal cerrado y manteniendo sus assets asociados. No se han borrado históricos ni realizado commits, push o PR.
'''
(R/'INFORME_REANUDACION_E_INTEGRACION_PBR.md').write_text(report,encoding='utf-8')
