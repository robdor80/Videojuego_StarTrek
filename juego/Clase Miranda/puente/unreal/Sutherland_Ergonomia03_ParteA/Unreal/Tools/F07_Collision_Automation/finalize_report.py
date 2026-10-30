"""Generate local evidence, file manifests and the human review report."""
import pathlib,json,hashlib,csv,datetime,collections,shutil
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=ROOT/'Saved/F07_Sutherland_Audit/Codex_Full_Bridge'
TOOLS=ROOT/'Tools/F07_Collision_Automation'
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8-sig'))
def save(n,d): (OUT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False),encoding='utf-8')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def md(n,s): (OUT/n).write_text(s.strip()+'\n',encoding='utf-8')
backup=pathlib.Path((TOOLS/'backup_path.txt').read_text(encoding='utf-8-sig').strip())
manifest=json.loads((backup/'manifest.json').read_text(encoding='utf-8-sig'))
commit=read('03_aplicacion_guardada.json');verify=read('04_verificacion_desde_disco.json');rerun=read('03_candidato_sin_guardar.json')
assert commit['ok'] and commit['saved_map'] and len(commit['saved_assets'])==90
assert verify['ok'] and not verify['critical_failures'] and not verify['functional_complete']
assert rerun['ok'] and not rerun['saved_assets'] and not rerun['helper']['created']
assert sum(sum(c['after']['primitives'].values()) for c in rerun['changes'])==74
changes=[]
for row in manifest:
    p=ROOT/row['path'];before=row['sha256'].lower();after=digest(p)
    assert digest(backup/row['path'])==before,'Backup changed: '+row['path']
    if before!=after:changes.append({'relative_path':row['path'],'before_sha256':before,'after_sha256':after,'before_size':row['size'],'after_size':p.stat().st_size})
expected={'Content/maps/L_F07_Sutherland_Test.umap'}
expected.update('Content/star_trek_sutherland_bridge__2_/StaticMeshes/'+c['mesh']+'.uasset' for c in commit['changes'])
assert {r['relative_path'].replace('\\','/') for r in changes}==expected
save('rollback_manifest.json',{'project_root':str(ROOT),'backup_root':str(backup),'files':changes})
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))
started=datetime.datetime.fromtimestamp((TOOLS/'audit_ue.py').stat().st_mtime,tz=now.tzinfo)
duration=round((now-started).total_seconds()/60,1)
total=len(verify['tests']);passed=sum(t['pass'] for t in verify['tests'])
strategies=collections.Counter(c['strategy'] for c in commit['changes'])
primitive=collections.Counter()
for c in commit['changes']:primitive.update(c['after']['primitives'])
summary={'date_madrid':now.isoformat(),'duration_minutes_from_first_script':duration,'engine':'5.8.2-56702186',
         'map':'/Game/maps/L_F07_Sutherland_Test','actors_initial':345,'actors_final':346,
         'sutherland_meshes':170,'sutherland_components':170,'mesh_assets_saved':90,'map_files_saved':1,
         'mesh_files_unchanged':80,'previously_validated_configurations_preserved':13,'previously_validated_files_untouched':7,
         'previously_validated_seat_files_rebuilt_with_identical_configuration':6,'strategies':dict(strategies),
         'asset_primitives':dict(primitive),'new_helper_actors':1,'tests_total':total,'tests_passed':passed,'tests_failed':total-passed,
         'unresolved_failures':verify['known_geometry_limitations'],'functional_complete':False,
         'all_170_visual_mesh_hashes_unchanged':verify['visual_meshes_unchanged'],'original_transforms_unchanged':verify['visual_transforms_unchanged'],
         'backup_root':str(backup),'backup_verified_files':len(manifest),'changed_content_files':len(changes),
         'verdict':'CONFIGURACIÓN PARCIALMENTE COMPLETADA — VER PENDIENTES.'}
save('RESUMEN_VERIFICABLE.json',summary)
save('04_pruebas.json',{'summary':summary,'source':'04_verificacion_desde_disco.json','tests':verify['tests']})
# Complete collision matrix, including the objects that intentionally retain no new collision.
inv=read('01_inventario_inicial.json');geometry=read('geometria.json')
plan={c['mesh']:c for c in commit['changes']};states={c['mesh']:c['after'] for c in verify['changes']}
floors={'Circle_0','Circle_001_0','Circle_002_0','Plane_002_0','Plane_003_0','Plane_021_0'}
captain={'Sphere_001_0','Cube_002_0','Cylinder_0','Mesh_453_0','Cube_0'}
doorset={'Plane_001_0','Plane_017_0','Plane_018_0','Plane_019_0'}
rows=[]
for m in inv['meshes']:
    n=m['name'];p=plan.get(n);category='TECHO_LUZ_O_DECORACION_ALTA';reason='Elemento alto o acabado; no se añade colisión en esta fase a pie; salto/encuentros altos pendientes'
    if n.startswith('Mesh_'):category='MECANISMO_O_DETALLE_ASIENTO';reason='Mecanismo/detalle pequeño; la silla queda cubierta por sus piezas sólidas principales'
    if n in captain:category='SILLON_CAPITAN';reason='Configuración previa preservada; Cube_0 es acabado sobre cuerpos existentes'
    if n in floors:category='SUELO_ESCALON_TARIMA';reason='Superficie de apoyo'
    if n=='Plane_028_0':category='BARANDILLA';reason='Configuración previa preservada'
    if n.startswith('Mesh_58') or n.startswith(('Mesh_591','Mesh_598','Mesh_600','Mesh_601','Mesh_602')):category='ASIENTO_SOLIDO'
    if n in doorset:category='HOJAS_PUERTA_COMPARTIDAS'
    elif n=='Cylinder_002_0' or n=='Plane_008_0':category='CONSOLA_LATERAL'
    elif n.startswith('Editable_Mesh_Mat_0') and n not in ['Editable_Mesh_Mat_026_0']:category='CONSOLA_INDEPENDIENTE'
    elif p and p['strategy']=='EXACT_STATIC_TRIANGLES' and n not in floors:category='MAMPARO_MARCO_O_CABINA'
    if n in ['Plane_040_0','Plane_041_0','Plane_042_0','Plane_047_0','Editable_Mesh_Mat_026_0']:
        category='DISPLAY_O_ACABADO';reason='Superficie visual/LCARS; cuerpos de consola y mamparos aportan bloqueo principal'
    if p:reason=p['reason']
    st=states.get(n); before_counts=geometry['meshes'][m['path']]['primitives']
    rows.append({'mesh':n,'asset':m['path'],'area':category,'strategy':p['strategy'] if p else 'PRESERVAR',
                 'complexity_before':m['complexity'],'complexity_after':st['complexity'] if st else m['complexity'],
                 'simple_before':sum(before_counts.values()),'simple_after':sum(st['primitives'].values()) if st else sum(before_counts.values()),
                 'file_changed':bool(p),'reason':reason,'human_play':'PENDIENTE'})
with (OUT/'02_matriz_colisiones.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
# Repair the initial inventory's commandlet-only count error with directly measured aggregate counts.
for m in inv['meshes']:
    counts=geometry['meshes'][m['path']]['primitives'];m['simple_count_commandlet_note']=m['simple_count']
    m['simple_count']=sum(counts.values());m['convex_count']=counts['convex_elems'];m['primitives']=counts
inv['count_note']='Recuentos de AggregateGeom obtenidos por API pública; StaticMeshEditorSubsystem no existía en commandlet inicial.'
save('01_inventario_inicial.json',inv)
catalog=read('puertas_f07_inventario.json')
for door in catalog['doors']:
    cases=[t for t in verify['tests'] if t['name'].startswith(door['id']+'_')]
    door['closed_test']='PRUEBA FISICA AUTOMATICA OK: 3 barridos bloquean las hojas'
    door['open_test']='PRUEBA FISICA AUTOMATICA OK: 3 barridos libres con colisión de hojas retirada temporalmente; estado cerrado restaurado'
    door['test_cases']=[t['name'] for t in cases]
    door['frame_fixed_configured']=True;door['fixed_collision_center_passage_clear']=all(t['pass'] for t in cases)
    door['full_leaf_motion_pockets_verified']=False
    if door['id'] in ['DOOR_F07_001','DOOR_F07_003']:door['frame_assets']=['Plane_013_0 (candidato geométrico)','Plane_005_0 (mamparo adyacente)','Plane_010_0 (pared posterior)']
for n in ['puertas_f07_inventario.json','PUERTAS_SUTHERLAND_F07.json']:save(n,catalog)
door_table='\n'.join('| '+d['id']+' | '+str([round(x,1) for x in d['center_cm']])+' | '+', '.join(p['mesh'].split('.')[-1] for p in d['parts'])+' | '+('Cabina modelada' if d['id']=='DOOR_F07_004' else 'Sin destino construido')+' | Cerrada: OK; hojas sin colisión: OK | REQUIERE SEPARACIÓN EN BLENDER |' for d in catalog['doors'])
for n in ['PUERTAS_SUTHERLAND_F07.md','PUERTAS_F07_CONCILIACION_4_DE_4.md']:
    with (OUT/n).open('a',encoding='utf-8') as f:f.write('\n## Resultado físico desde disco\n\nLas cuatro puertas bloquean cerradas. Tres barridos por acceso pasan al retirar exclusivamente la colisión de las hojas; después se restaura. Esto verifica el paso central muestreado, no los bolsillos completos ni toda la futura trayectoria de apertura.\n')
evidence=OUT/'Referencias_usuario';evidence.mkdir(exist_ok=True)
sources=[pathlib.Path('C:/Users/andro/Downloads/CODEX_F07_SUTHERLAND_PROMPT_V4_INTEGRAL_PUERTAS_IDENTIFICADAS.md'),pathlib.Path('C:/Users/andro/Downloads/README_REFERENCIAS_PUERTAS.md')]
sources+=list(pathlib.Path('C:/Users/andro/Downloads/Referencias_puertas').glob('*.png'))
source_manifest=[]
for src in sources:
    dst=evidence/src.name;shutil.copy2(src,dst);source_manifest.append({'source':str(src),'copy':str(dst),'sha256':digest(src)})
save('referencias_manifest.json',source_manifest)
md('00_entorno.md',f'''# Entorno F07

Fecha Madrid: {now.isoformat()}. Duración desde primer script: {duration} minutos; inspección documental previa adicional.

- Proyecto: `{ROOT / 'f07sutherland.uproject'}`.
- Motor comprobado: UE 5.8.2, CL 56702186. Asociación `.uproject`: 5.8. Sin conversión.
- Mapa: `/Game/maps/L_F07_Sutherland_Test`.
- Automatización: Python Editor Script Plugin, GeometryScripting y ProceduralMeshComponent habilitados por línea de comandos; APIs de la instalación local. `.uproject` y Config sin cambios.
- Inventario inicial: commandlet solo lectura. Física: editor completo inicializado con `-nullrhi`, no commandlet. Barridos de cápsula 35/90 cm con perfil Pawn, coherente con canal Pawn y bloqueo WorldStatic del Character real. No se ejecutó movimiento de Character ni Play humano.
- Pawn: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`; cápsula 70×180 cm; escalón máximo 45 cm.
- Al inicio no había Unreal abierto. Blender estaba abierto y no se intervino. Cada editor iniciado para la auditoría salió por su flujo normal.
- Fuente `.blend` indicada en el documento: NO EXISTE en esa ruta. No se modificaron fuentes Blender.
- Backup nuevo: `{backup}`. Se verificaron {len(manifest)} archivos SHA256 antes de guardar y nuevamente al cerrar el informe. Incluye Content, Config y .uproject; no cachés.
- Copias antiguas: preservadas. Fuente de recuperación exclusiva: `rollback_manifest.json`.
- Guardado: 90 .uasset y un .umap; ningún material, textura, Blueprint, Config ni .uproject difiere del backup. Un auxiliar oculto en el nivel; ningún asset nuevo.
- Lectura final desde disco y repetición idempotente completas. Sin errores fatales ni errores Python en las dos ejecuciones finales.
- Advertencia de logs conservada: 14 entradas `LogAutomationTest: Error: Condition failed` durante el arranque, antes del script, también presentes en la primera apertura de solo lectura. No se atribuyen a las colisiones; origen interno concreto no investigado. No se afirma que los logs carezcan de errores.
''')
measure=read('medidas_pasillos.json')
measure_table='\n'.join('| '+r['asset'].split('.')[-1]+' | '+r['side']+' | '+f"{r['minimum_measured_cross_section']['gap_cm']:.2f}"+' | 70.00 |' for r in measure)
pending='''# Pendientes F07

1. **Prioridad alta — pasos junto a consolas:** huecos reales de 59,9–61,0 cm frente a cápsula de 70 cm. Elegir un ajuste de distribución/modelado o revisar dimensiones del personaje. No se ha aplicado ninguna de esas opciones. Las bases y sillas permanecen sólidas. Hay rutas interiores alternativas comprobadas en x=±360 cm, y=130..650 cm.
2. **Puertas:** separar cada una de las ocho hojas de los assets compartidos entre lados opuestos. Se necesita localizar una fuente Blender válida o realizar una extracción en copia controlada. Mantener marcos fijos, pivotes y materiales. Falta validar bolsillos y recorrido completo de hojas. No hay Blueprint animado.
3. **Orientación humana:** revisar la descripción D02/D03: se enfrentan D01/D03 atrás y D02/D04 delante. Conservar los IDs y usar coordenadas.
4. **Play humano:** escaleras en ambos sentidos, enganches, salto, barandillas, esquinas, sillas completas, sillón, consola, pantalla y perímetro. Los barridos no sustituyen CharacterMovement.
5. **Panel gris de cabina Plane_027_0:** candidato adicional no confirmado como acceso. No contado como quinta puerta ni convertido en puerta automática.
6. **Acabados altos y mecanismos pequeños:** clasificados sin nueva colisión; revisar encuentros excepcionales al saltar y contactos finos en Play. No se certifica contacto físico de cada detalle decorativo.
7. **Tope de pantalla:** se añadió un bloqueo puntual dentro del marco porque la abertura no tenía superficie. Revisar visualmente su correspondencia con la pantalla prevista; no se añadió geometría visible.
'''
md('05_pendientes.md',pending)
report=f'''# Informe final F07 — Sutherland

**CONFIGURACIÓN PARCIALMENTE COMPLETADA — VER PENDIENTES.**

Trabajo guardado y recargado correctamente en el proyecto solicitado. Paredes, suelos, cabina y cuatro puertas cuentan con colisiones comprobadas por muestras físicas. El paso entre sillas y consolas sigue limitado por geometría real: aproximadamente **60 cm disponibles frente a una cápsula de 70 cm**. No se han movido muebles ni cambiado el personaje.

## Ejecución y alcance

{now.strftime('%d/%m/%Y %H:%M')} Europe/Madrid. Aproximadamente {duration} minutos desde el primer script, más inspección documental inicial. Windows 11, i9-14900HX; UE 5.8.2 CL 56702186. Proyecto `{ROOT / 'f07sutherland.uproject'}`; mapa `/Game/maps/L_F07_Sutherland_Test`. APIs Python locales del editor completo, ejecutado sin renderizado para las pruebas físicas. El editor terminó y no quedó ningún proceso Unreal de esta ejecución abierto.

Se guardaron **90 mallas y el mapa**. Las 170 mallas conservan hashes idénticos de vértices, índices, normales, UV0 y asignaciones de material; los transforms originales también coinciden. No se cambiaron luces, cámaras, distribución, materiales, texturas, Pawn ni Blueprints. La comprobación de apariencia es estructural: no se realizó comparación de capturas renderizadas.

## Cobertura verificable

| Concepto | Resultado |
|---|---:|
| Actores iniciales / finales | 345 / 346 |
| Mallas Sutherland y componentes examinados | 170 / 170 |
| Mallas guardadas / archivos de malla intactos | 90 / 80 |
| Colisiones anteriores conservadas en configuración | 13 |
| De esas 13: archivos intactos / sillas regeneradas con igual configuración | 7 / 6 |
| Arquitectura, superficies y consolas con triángulos estáticos exactos | 37 |
| Assets con convexos por componente | 43: bases + 42 partes de sillas |
| Formas simples nuevas en assets | 66 convexos + 8 cajas = 74 |
| Auxiliares en nivel | 1 cubo oculto, para hueco de pantalla |
| Assets nuevos / auxiliares eliminados | 0 / 0 |
| Mallas conservadas sin escritura | 80; incluye acabados y mecanismos |
| Casos físicos desde disco | {total}: {passed} OK, {total-passed} FALLAN |

Los 12 fallos son recorridos longitudinales deseados junto a las consolas, a ambos lados y en ambos sentidos. **Siguen siendo fallos funcionales**, aunque su causa geométrica está medida. Ningún otro caso final falló. La repetición del plan mantuvo 346 actores y 74 formas, reutilizó el auxiliar y no guardó archivos: comprobación de idempotencia.

## Matriz por áreas

| Área | Examinada / modificada | Evidencia automática | Play humano |
|---|---|---|---|
| Suelos / tarima | Sí / suelos auxiliares; Circle_0 preservada | 80 trazas de apoyo en geometría real, OK | PENDIENTE |
| Seis sillas laterales | Sí / regeneración de 6 datos físicos + convexos en 42 partes | Muestras de colisión y regresión de seis asientos OK | PENDIENTE |
| Consola independiente | Sí / cuerpo previo preservado, piezas superiores completadas | Muestras por asset OK | PENDIENTE |
| Sillón del Capitán | Sí / sin escritura de sus cuatro assets probados | Regresión física por triángulo OK | PENDIENTE |
| Consolas laterales / Cylinder_002_0 | Sí / 18 convexos y perfil BlockAll | 18 bases bloquean; pasos estrechos FALLAN | PENDIENTE |
| Escaleras / descansillos | Sí / superficies exactas | Apoyo muestreado OK; no locomoción ni subida completa | PENDIENTE |
| Barandillas | Sí / conservadas | Muestra de bloqueo OK | PENDIENTE |
| Mamparos interiores | Sí / triángulos exactos bidireccionales | Muestras por asset OK | PENDIENTE |
| Paredes exteriores / perímetro | Sí / colisión exacta + tope de pantalla | 72 direcciones × entrada/salida = 144 trazas OK | PENDIENTE |
| Puertas / accesos | 4/4 / 8 cajas independientes por isla | 24 barridos: cerrado bloquea y hojas sin colisión liberan paso central | PENDIENTE |
| Resto de mobiliario / decoraciones | 170 assets clasificados | Cobertura principal configurada; mecanismos finos y elementos altos conservados | PENDIENTE |

No se interpreta un perímetro muestreado como una certificación exhaustiva de todas las uniones, alturas o trayectorias. Los ensayos no son pruebas de movimiento de Character en Play.

## Diagnóstico de Cylinder_002_0 y pasillos

El mapa inicial tenía `Cylinder_002_0` en **NoCollision**, pese a la restauración descrita en el documento. Al activarlo, las 18 piezas físicas bloquean. Se sustituyó su colisión triangular por **18 convexos**, uno por base; no se creó ningún hull que uniera ambos lados del puente.

Las seis mallas `Mesh_589_*` tenían marcada colisión compleja, pero las consultas iniciales no detectaban sus superficies. Regenerar los datos físicos con la misma configuración hizo que respondieran, y el resultado persiste al recargar desde disco. El mecanismo interno exacto de esa discrepancia no está demostrado; el antes/después sí consta en `chair_probe.json`. Por ello no basta con leer el flag de colisión.

Con sillas y bases efectivamente sólidas, los barridos longitudinales deseados fallan. Intersecciones de los triángulos visuales con planos Y, dentro de la parte cilíndrica de la cápsula, dan estos estrechamientos:

| Asiento | Lado del Capitán | Hueco medido cm | Diámetro cápsula cm |
|---|---|---:|---:|
{measure_table}

Son medidas de secciones concretas, no un ancho constante de todo el pasillo. Cada sección menor que el diámetro impide el paso de esa cápsula erguida a esa altura. La colisión de las bases no es una caja global sobredimensionada. **No se ha resuelto el conflicto alterando cuerpos sólidos.** El paso interior alternativo x=±360, y=130..650 cm superó cuatro barridos con cápsula real.

Alternativas para revisión humana: desplazar o remodelar de forma deliberada la relación silla/consola, o revisar dimensiones de la cápsula respecto a la escala del entorno. No se ha aplicado ninguna; reducir primitivas por debajo de la geometría escondería el problema.

## PUERTAS AUTOMÁTICAS — PREPARACIÓN F07

Frente +Y, izquierda +X, derecha -X, tomando al Capitán orientado a la pantalla. Ocho islas de hojas en cuatro accesos. Cada asset de hoja agrupa una isla de cada lado opuesto del puente; no permite animarlas individualmente por puerta.

| Puerta | Centro XYZ cm | Assets de hojas | Destino | Prueba actual / hueco | Estado |
|---|---|---|---|---|---|
{door_table}

Marcos fijos configurados: sí; hojas con colisión propia por isla: sí; hueco central libre de nuevas colisiones fijas al retirar hojas: comprobado en tres barridos por acceso. Apertura completa, bolsillos laterales y pivotes: **no comprobados**. Todas las hojas vuelven al estado cerrado y sólido antes de guardar. Las tres salidas sin destino permanecen bloqueadas y la cabina modelada se conserva.

Discrepancia de descripción: D01/D03 se enfrentan atrás, D02/D04 delante; D02/D03 son diagonales en el modelo. Se conservan los IDs humanos y se pide revisión de ese emparejamiento. `Plane_027_0`, panel gris al extremo exterior de la cabina, queda como candidato no confirmado; no se suma como quinta puerta.

Fase futura propuesta, sin implementar: separar hojas por puerta en una copia controlada, pivotes y ejes documentados; `BP_ST_AutomaticDoor` con marco fijo y dos hojas móviles, proximidad jugador/NPC, estados cerrada/abriendo/abierta/cerrando/bloqueada, sensor que inhiba cierre con vano ocupado y audio suministrado. La autoridad de permisos de CoreRPG debe quedar separada del movimiento local. La fuente Blender citada no existe en esa ruta y habrá que localizarla antes de separar.

## Tope puntual de pantalla

Los rayos detectaron ausencia real de geometría en el centro de la pantalla principal; no era una puerta. Se añadió `F07_COLL_PANTALLA_PRINCIPAL_FIJA`, invisible, sin sombra, usando un cubo de Engine existente. Centro `(0, 998.492, 194.381)` cm; dimensiones `(432.810, 19.672, 388.762)` cm, medidas del marco `Plane_015_0`. Está restringido a esa abertura y lejos de las cuatro puertas. No es un muro general alrededor del puente. Revisar su correspondencia con la pantalla prevista en Play.

## Pruebas, incidencias y logs

- `audit_ue.py` / `export_geometry_ue.py`: inventario y 16.614 triángulos LOD0 exportados por APIs UE. El commandlet no proporcionaba StaticMeshEditorSubsystem ni mundo físico útil; sus trazas no se cuentan como validación. Los recuentos se completaron desde AggregateGeom.
- `physical_probe_ue.py`: antes/después temporal de bases, sin guardar; `chair_probe_ue.py`: ausencia y regeneración de colisión de asiento, sin guardar.
- `apply_plan_ue.py`: candidatos sin guardar, aplicación verificada y guardado final. Se rechazaron candidatos con pruebas fallidas y generación excesiva de hulls por costuras. La solución final usa exclusivamente una copia transitoria de vértices coincidentes para generar convexos; no cambia fuentes visuales.
- `verify_saved_ue.py`: recarga independiente, **sin regenerar colisiones ni guardar**, {total} casos físicos; detalle en `04_verificacion_desde_disco.json` y `04_pruebas.json`.
- Repetición idempotente: sin formas ni actores duplicados; ver `03_candidato_sin_guardar.json`. Las trazas usan cápsula radio 35 / semialtura 90, perfil Pawn; el personaje real bloquea WorldStatic. Ningún cambio del Pawn.
- Logs: `audit_ue.log`, `geometry_ue.log`, `physical_probe_ue.log`, `chair_probe_ue.log`, `apply_plan_ue.log`, `verify_saved_ue.log`. Los JSON `candidate_*.json` conservan intentos y fallos, incluidos errores de disponibilidad de APIs corregidos. No hubo errores fatales ni excepciones Python en las dos ejecuciones finales.
- Hay 14 mensajes `LogAutomationTest: Error: Condition failed` durante el arranque previo al script, reproducidos también en `probe_editor.log` de la primera sesión de solo lectura. No se ocultan ni se atribuyen sin evidencia a las colisiones. Origen exacto no investigado; no impidieron guardar, recargar o ejecutar las consultas.

## Backup y recuperación

Backup: `{backup}`. Incluye {len(manifest)} archivos comprobados mediante SHA256. Copias antiguas preservadas. `rollback_manifest.json` identifica los **91 archivos de contenido** cambiados, con hashes anteriores y posteriores.

Con Unreal cerrado, ejecutar `Tools/F07_Collision_Automation/rollback.ps1` realiza solo una comprobación. `-Apply` restaura esos 91 archivos, comprobando previamente que no hayan cambiado desde esta entrega y que el backup conserve sus hashes. Si detecta modificaciones posteriores, se detiene antes de copiar. Restaurar el mapa también elimina el auxiliar y recupera los perfiles iniciales. No borra archivos ajenos ni informes.

## Checklist humano en Play

1. Abrir `Content/maps/L_F07_Sutherland_Test.umap`. Verificar caída inicial sobre suelo y acceso a tarima.
2. Recorrer rutas interiores a ambos lados. Intentar el paso estrecho entre sillas y consolas: se espera bloqueo en los estrechamientos medidos; acordar solución dimensional.
3. Intentar atravesar cada una de las 18 bases y los seis asientos; deben bloquear. Revisar respaldos, apoyos y enganches.
4. Rodear consola independiente y sillón del Capitán; tocar barandillas y subir/bajar escaleras en ambos sentidos.
5. Recorrer mamparos, esquinas y pantalla; no atravesar el perímetro. Revisar el tope de pantalla en particular.
6. Comprobar las cuatro puertas cerradas. En una copia de pruebas, retirar temporalmente solo sus colisiones y revisar el vano; **no salir por los tres destinos inexistentes y no guardar ese estado**.
7. Revisar acceso/interior de cabina en copia controlada, salto y elementos altos. Anotar actor o asset usando el plano y `02_matriz_colisiones.csv`.

Pendientes completos en `05_pendientes.md`. No se ha realizado Play humano ni se ha certificado la subida por CharacterMovement, la totalidad de los huecos o la animación futura de puertas.

**CONFIGURACIÓN PARCIALMENTE COMPLETADA — VER PENDIENTES.**
'''
md('INFORME_FINAL_F07_SUTHERLAND.md',report)
(TOOLS/'README.md').write_text('''# F07 Collision Automation

Proyecto local de pruebas Sutherland, UE 5.8.2. Alcance: colisiones; sin reimportar mallas ni modificar apariencia.

El informe principal y todas las evidencias están en `Saved/F07_Sutherland_Audit/Codex_Full_Bridge/`.

## Repetir comprobación desde disco

Con este proyecto cerrado en Unreal, desde PowerShell:

```powershell
& .\\Tools\\F07_Collision_Automation\\run_editor.ps1 -Script verify_saved_ue.py
```

El wrapper evita escritura concurrente y usa la instalación UE 5.8. Abre una sesión oculta, ejecuta el script y sale normalmente. `verify_saved_ue.py` no regenera ni guarda assets. Produce 375 casos: 363 correctos y 12 fallos geométricos conocidos de los pasillos estrechos.

`apply_plan_ue.py` es simulación sin guardar por defecto. Solo guarda cuando existe `commit_plan.json` con SHA256 exacto de `collision_plan.json`. La autorización técnica de esta ejecución ya fue consumida y se conserva como `commit_plan.executed.json`; no existe un checkpoint activo.

`build_plan.py`, `analyze_geometry.py` y `measure_routes.py` usan NumPy/Pillow del runtime de trabajo. No ejecutarlos como si fueran scripts de UE. `audit_ue.py`, `export_geometry_ue.py`, los probes y el aplicador requieren el módulo `unreal` del editor.

## Recuperación

`rollback.ps1` comprueba hashes sin escribir. `rollback.ps1 -Apply` restaura solo los archivos entregados, con Unreal cerrado y siempre que no haya cambios posteriores. Consultar el manifiesto y conservar el backup completo.

## Límites

Hay pasos de 59,9–61,0 cm frente a cápsula de 70 cm. No se han cambiado muebles ni personaje. Las hojas de puertas aún comparten assets entre lados opuestos y requieren separación para futura animación. No se ha validado Play humano.
''',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
