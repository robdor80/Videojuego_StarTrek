# F03 — informe de ejecución para auditoría independiente

**30-10-2026, Europe/Madrid. Implementación P01–P05 ejecutada en el MSI.**
El corte vertical alcanza evidencia `CORE_INTEGRADO` en ramas aisladas. F03 sigue
abierta: depende de [CoreRPG Draft #12](https://github.com/robdor80/CoreRPG/pull/12),
todavía sin fusionar. No se declara integración final en `main`, cierre oficial ni
`UE5_JUGABLE`. No se modifica `ESTADO_GLOBAL.json` ni la historia aprobada de F02.

Entrega publicada: [Star Trek Draft #62](https://github.com/robdor80/Videojuego_StarTrek/pull/62)
y [CoreRPG Draft #12](https://github.com/robdor80/CoreRPG/pull/12), ambas abiertas,
sin fusionar. La aprobación independiente todavía no se ha solicitado como cierre.

## Referencias y arquitectura entregada

Star Trek parte de `9b33f32caab21ce0eb1ecb74cd38739b45d2f035`, cierre F02
verificado antes de crear rama. Rama:
`codex/f03-mundo-autoritativo-persistencia-20261030`.
CoreRPG parte de `4f282863737bcd8f5add401202a9e1064c133672`; rama
`codex/f03-authoritative-timeline-20261030`; dependencia final exacta
**`9c53a33787de13d91eb2abe4da07033ee0fa1dc1`**, fijada también por CMake.

[Auditoría previa y matriz de reutilización](AUDITORIA_TECNICA_2026-10-30.md).
[Código e instrucciones reproducibles](../../../../../../desarrollo/integration/f03/README.md).

Core sigue siendo la única autoridad. Se reutilizan WorldState/EntityId,
ContentCatalog, Population, RandomStreams, ActionEngine, Visibility, Knowledge,
ContextBuilder y Persistence. Se añaden en Core `Timeline` y `CampaignPersistence`,
sin código Trek ni dependencia Unreal. El nuevo archivo versionado contiene el
SAVE Core original y la agenda en un único bloque validado. Los formatos v1–v3 y
las interfaces anteriores permanecen compatibles; no se introduce migrador implícito.

Trek aporta un fixture sintético y catálogo estructural, ruta de prueba, canales
autorizados y C ABI 1. Unreal tiene subsistema de GameInstance y Actors efímeros
por identidad/UWorld. El overlay F03 se aplica exclusivamente en el laboratorio
externo, conservando el laboratorio y fuentes F02 originales.

## Resultado por paso

| Paso | Implementación real | Evidencia de aceptación |
|---|---|---|
| P01 | Ocho identidades Core; bootstrap reproducible; dos individuos promovidos de tres plazas; refs scoped; materialización/desmaterialización; dos niveles visuales; Actors independientes en dos UWorld | `f03.identity`, `determinism`, `scope`, `roundtrip`; `F03.Core.IdentityLodWorlds`; regresión F02 de dos UWorld |
| P02 | Dos observadores con conocimiento distinto; nave oculta; percepción por colocalización explícita; informe con solo existencia; consultas sin mutación; vistas y ContextBuilder filtrados; permiso revocable | `f03.observers`, `hidden`, `acquire`, `report`, `denied`, `readonly`, `tampered`; `F03.Core.Knowledge`, `Recovery` |
| P03 | Reloj entero, orden `(due,id)`, agenda persistente; ruta fuera de escena; padre causal; terminales no reejecutables; presupuesto/reanudación; fecha exacta y estelar derivada | `f03.offscreen`, `order`, `bounded`, `duplicate`, `backwards`, `calendar`; `F03.Core.Offscreen`; pruebas Timeline de rechazo causal y prefijo confirmado |
| P04 | Mundo, IDs, definiciones, cupos, conocimiento, RNG, reloj y agenda en archivo Core; restauración candidata; cierre de sesión y reconstrucción; guardado/lector en procesos distintos | `f03.roundtrip`, `rng`, `corrupt`, `incompatible`, `process_save`, `process_load`; `F03.Core.Recovery`, `SafeFailure`; inyección de cada fallo de asignación en carga Core |
| P05 | Suite completa Core, nativo C ABI, UE5 real, validadores documentales; CI; inventario protector; revisión de diff y manifiestos de fuentes | [Resultados compactos](evidencias_20261030/results.json), [trazabilidad ejecutada](evidencias_20261030/native-tests.xml), [Core](evidencias_20261030/core-tests.xml), [UE](evidencias_20261030/unreal-tests.json) |

La identidad no depende de Actors ni LOD. La ruta de la segunda nave funciona sin
Actor: salida t=10, llegada t=20, tirada t=21 y regreso t=40. Al materializar se
lee la ubicación Core ya resultante. Cambiar la representación deja el archivo
de campaña idéntico byte por byte. Cargar con éxito invalida todos los bindings;
cargar un archivo inválido conserva tanto realidad como representaciones válidas.

La observación legítima requiere ambas naves en el sector de destino. El Core
recuerda existencia, definición y contención para la segunda nave; el informe a
la primera solo transmite existencia. No hay clasificación oculta en la vista
del receptor. Los contactos son relativos al observador; nunca se exporta el
objeto WorldState mediante las consultas de presentación. Handles, estadísticas,
marker_state y saves son diagnósticos privilegiados, no canales públicos de UI/IA.

El reloj exacto usa un segundo por tick desde `2372-03-14T10:42:00`, época fija
del fixture Trek 0.1.0. La representación gregoriana y el desplazamiento estelar
de 1000 unidades por año se derivan al consultar. No se usa fecha estelar como
reloj, ni se inventa un ancla estelar absoluta. Se verifica el cruce de día y la
recuperación de la fecha; valores fuera del rango del adaptador se rechazan.

## Validación ejecutada

| Batería local final | Superadas | Fallidas | Omitidas |
|---|---:|---:|---:|
| CoreRPG completo Release, ContentJson activado | 447 | 0 | 4 |
| Core F03 Debug, subset adicional de reloj/archivo/memoria | 15 | 0 | 0 |
| F03 nativo C ABI, incluyendo escritor/lector en procesos distintos | 25 | 0 | 0 |
| F02 nativo original, dependencia Core original | 15 | 0 | 0 |
| UE5.8.2 combinado: seis F02 + seis F03 | 12 | 0 | 0 |
| Validador documental F03 | 26 | 0 | 0 |
| Validador documental F02 | 9 | 0 | 0 |

No sumar el subset Debug a las 447 como funcionalidades distintas. Los seis UE
F02 también se ejecutaron previamente en su proyecto aislado; no se duplican en
la tabla. Los cuatro skips Core son comprobaciones de permisos de archivo o
symlinks que Windows no permite ejercer en esta configuración; no son éxitos.
Los validadores de fixture F03 y contratos/plan F02 devolvieron éxito por separado.

UE final: **12 éxitos, cero éxitos con avisos, cero fallos y cero no ejecutados**.
Compilación real Editor Win64, carga de las dos DLL, Actors y UWorld reales.
Las pruebas se ejecutaron con `-NullRHI`: verifican representación y ciclo Actor,
no calidad gráfica, rendimiento ni jugabilidad. No se afirma demostración gráfica
DX11 nueva ni se reutiliza la captura histórica F02 como evidencia nueva.

Entorno verificado: UE 5.8.2 CL 56702186, Windows 11 25H2, MSVC 19.51.36256 /
toolset 14.51.36231, Visual Studio/MSBuild 18.9.1, SDK 10.0.26100.0, CMake 4.4.3,
Python 3.10.11, Git 2.52.0. UBT advierte que este compilador es más reciente que
el preferido y muestra deprecaciones del motor; compilación/enlace correctos.

## Fallos reales encontrados y corregidos

1. **Orquestación de build inicial:** se editó CMake mientras una compilación
   paralela seguía activa; regeneraciones concurrentes fallaron en archivos de
   CMake/FetchContent. Se dejó terminar, se reconfiguró y repitió secuencialmente.
   Una consulta CTest previa al registro devolvió «No tests were found»: no se
   contabiliza como éxito. Todas las ejecuciones finales exigen `--no-tests=error`.
2. **Memoria en MSVC Debug:** inyectar asignación fallida durante una carga
   terminaba el proceso por el constructor move `noexcept` de vector con checked
   iterators. Se sustituyó por construcción que propaga fallos y `swap` sin
   asignación. La inyección exhaustiva y el prefijo parcialmente confirmado
   pasan en Release y Debug. Los registros anteriores se conservan.
3. **Orden de limpieza UE de los fixtures:** el primer pase pasó 12 tests con
   avisos al destruir un Actor tras perder el contexto UWorld. Se añadió retirada
   explícita por mundo antes de destruirlo. El resultado final no tiene avisos de tests.
4. **Caché del SHA en UBT:** tras cambiar Core, Build.cs había conservado una
   definición del SHA anterior. El adaptador denegó abrir F03: cinco tests fallaron,
   F02 permaneció correcto. Se genera ahora una cabecera versionada en staging,
   rastreada por el compilador. La repetición completa con el SHA final pasa 12/12.
5. **Alcance de carga endurecido en auditoría interna:** el Host ahora comprueba
   ruta exacta, observers y campos permitidos, población y catálogo. `f03.tampered`
   construye archivos con CRC válido y estado Core estructuralmente válido, pero
   actor de ruta o clasificación del receptor no autorizados: el Host los rechaza
   sin modificar la sesión vigente.

Los fallos negativos esperados incluyen corrupción de cada byte, todas las
truncaciones, versión futura, horizonte anterior, actor/observador ajeno, revisión
caducada, scope antiguo, hilo incorrecto, canal inventado y permiso revocado.
Un test que verifica ese rechazo es un éxito del contrato, no un fallo ocultado.

## Reproducción y evidencias

Los comandos ejecutados y parámetros están en los logs fechados; instrucciones
completas en el README del laboratorio. Ubicaciones usadas:

- Worktree Trek: carpeta `f03-integration` junto a la planificación original.
- Worktree Core: `C:/F03/CoreRPG`; build Core: `C:/F03/core-build`.
- Host F03: `C:/F03/native`; laboratorio UE extendido: `C:/F03/ue`.
- Regresión F02: `C:/F03/f02-regression`, con Core original sin cambios.
- Logs originales: `C:/F03/evidence/logs` y logs fechados de los runners.
- Colección: ver [índice externo con tamaños, SHA-256 y estado de publicación](EVIDENCIAS_EXTERNAS_2026-10-30.json).

`collect_evidence.py` valida los recuentos reales antes de reunirlos, preserva
resultados fallidos, genera manifiestos de fuentes y empaqueta exclusivamente
logs, saves de prueba y binarios propios. La publicación redacta perfil de usuario,
nombre de equipo y cabeceras de autorización; los logs originales permanecen locales.
No se suben binarios UE, Intermediate, PDB gigantes ni arte a GitHub.

## Protección y límites para la auditoría

CI remota comprobada en `e85c11f1e730bdbb1ae13123025bfa59aa9bc4f1`:
[integración nativa F03](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41041233210),
[referencia documental](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41041233221)
y [gobierno de roadmap](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41041233315),
los tres `completed/success`. Core en `9c53a337`:
[CI 41040471499](https://github.com/robdor80/CoreRPG/actions/runs/41040471499),
seis jobs `completed/success`: Windows/Linux, Core-only y sanitizers ASan/UBSan,
incluida integración con paquete externo de pruebas. UE se valida localmente,
no en GitHub-hosted. [Lectura verificable de CI](evidencias_20261030/ci-verification.json).
Los commits posteriores a ese corte añaden únicamente metadatos/documentación.

Inventario real previo/posterior del checkout artístico: **19.691/19.691 archivos**,
cero nuevos, ausentes o cambios de tamaño/mtime. Es una comprobación de metadatos,
no una auditoría criptográfica de todo el arte. La referencia histórica F02 era
19.030; no se presupuso que el inventario actual tuviera el mismo tamaño.
El original Star Trek conserva HEAD `7ee52d5` y sus archivos sin seguimiento.
El original Core conserva HEAD `4f282863` y está limpio. No se ejecutó reset hard,
clean, movimiento/borrado de recursos ni modificación de respaldos o .gitignore.
El diff final se limita al laboratorio F03, su workflow y documentación/evidencias F03.

Este corte no implementa los contratos completos de sensores, memoria psicológica,
viaje, logística, agenda profesional, migraciones generales o estado arbitrario de
naves. La contención en sectores es suficiente para la actividad sintética, sin
afirmar que resuelve vuelo real o consumo de combustible. El fixture inerte del
11-10 se preserva y sus pruebas estáticas siguen siendo estáticas.

La agenda retiene hasta 4096 acciones y revalida estructura al ejecutar. La
autorización es previa, del Host; no hay cancelación ni permiso revocable persistido
por orden. Un permiso Host revocado impide avances externos nuevos, pero no borra
recuerdos ni reescribe acciones ya autorizadas. No hay concurrencia de escritores
ni garantía frente a pérdida eléctrica en mitad de IO. CRC detecta corrupción,
no autentica archivos editados maliciosamente. No se promete migración de saves
F02 al archivo nuevo: se requiere un futuro migrador explícito si se necesitara.

**Siguiente puerta:** auditoría independiente de ChatGPT y resolución de la
dependencia Core antes de cualquier declaración de integración en `main`.
Ambas PR permanecen Draft y sin fusionar; el cierre oficial sigue reservado a dirección.
