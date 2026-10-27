# F02-P04 — Fallos, compatibilidad, migraciones y pruebas de contratos

**Estado 11-10-2026:** **POLÍTICA DOCUMENTADA Y VALIDADOR ESTÁTICO CREADO; integración externa PENDIENTE.** No es una API de CoreRPG, ni un formato savegame, ni una implementación de recovery. F02 continúa en revisión. **F01/DEC-0001 y elección de Imperator no se alteran.**

## Alcance, fuentes y evidencia

- [Registro P04 verificable](REGISTRO_FALLOS_COMPATIBILIDAD_P04.json): **13 situaciones de fallo**, **6 ejes de versión**, **10 condiciones de compatibilidad**, **16 pruebas** y preflight exigido para migraciones.
- [Validador estático](../../../../../../desarrollo/tools/validation/validate_f02_contracts.py) y [sus nueve tests aislados](../../../../../../desarrollo/tools/validation/test_validate_f02_contracts.py), sin librerías externas.
- [Workflow GitHub Actions F02](https://github.com/robdor80/Videojuego_StarTrek/blob/docs/f02-core-integration-contracts/.github/workflows/f02-contracts.yml): ejecuta chequeo de procedencia y tests sin atribuirse pruebas Core/UE5.
- [Inventario P02](INVENTARIO_INTERCAMBIO_P02.json): 24 fuentes JSON/73 selectores con SHA blob; [mapa P03](MAPA_ADAPTADORES_P03.json): 12 fronteras/11 gaps.
- CoreRPG línea base real: `main@dcfcb83c9853e005b5450bd39e0ba693cb91e257`, 4.5 rama `2a3da891d8c56e9868c7bd67dbeb6041509df2ce`. `main` carece de acciones generales, Knowledge y Persistence.
- La referencia `sistemas/gameplay/persistence/persistent_state_roundtrip_contract.json` exige identidad, historia y procedencia; **no** define el formato físico o una implementación existente de save/load.

La matriz P04 añade verificaciones estáticas sin modificar ni duplicar `desarrollo/tools/validation/validate_internal_references.py`, el simulador de Sensores o el motor Core.

## 1. Prioridades de gestión de errores

Para **acciones que cambian hechos**, la autoridad es Core. Para **presentación**, UE5 puede degradarse sin cambiar Core. Para **IA o red**, un error no genera hechos nuevos. Un mensaje no entregado al Host no significa que Core no lo haya confirmado.

| Código | Fallo | Política de protección y experiencia del jugador |
|---|---|---|
| F02-E01 | IA inaccesible o timeout | Interfaz manual de Sensores operativa; explicar fallo del lenguaje natural, no bloquear guardia |
| F02-E02 | IA devuelve intención inválida o hechos no observados | Rechazar candidato y texto no autorizado; permitir corregir orden |
| F02-E03 | Petición llega tarde tras cambio de estado/autoridad | Revalidar contexto *en el compromiso efectivo*, rechazar o aclarar |
| F02-E04 | Timeout tras enviar orden cuyo resultado se desconoce | Estado de resultado **desconocido**, reconciliación antes de un eventual reintento |
| F02-E05 | Core no disponible o build incompatible | Bloquear acciones persistentes; no crear segundo WorldState de emergencia |
| F02-E06 | Sensores dañados/interferencia/firma débil | Lectura parcial o ninguna; jamás crear contacto para rellenar pantalla |
| F02-E07 | Contacto perdido | Conservar último dato/historial; no inferir explosión, camuflaje o warp |
| F02-E08 | Actor UE5 descargado por escena/LOD | Recrear representación cuando proceda; mantener NPC lógico/guardia en Core |
| F02-E09 | Guardado corrupto/incompatible | Rechazo completo; preservar guardado anterior, identidad y sesión vigente |
| F02-E10 | Riesgo de fuga de datos ocultos a UI/IA | **Fail-closed antes de construir la respuesta**; registrar diagnóstico adecuado |
| F02-E11 | Companion opcional desconectado | Juego Windows continúa sin pérdida de control; reautorizar si reconecta |
| F02-E12 | Versión Core/Host/Content Pack cambiada | Comparar contrato y batería de pruebas; sin compatibilidad presumida |
| F02-E13 | Falta reloj de campaña coherente o causalidad | Rechazar evento autoritativo hasta poder ordenar/verificar; fecha estelar no es reloj |

### Estados de petición vs. resultado (regla conceptual, NO enum API)

Distinguir **entrada recibida**, **orden aceptada**, **tarea en cola/en progreso**, **efecto confirmado en Core**, **rechazo validado** y **resultado desconocido para Host**. Un aviso local tipo *«Enviando solicitud»* no puede presentarse como *«Barrido completado»*.

El contrato Trek `sistemas/gameplay/orders/starship_order_contract.json` ya tiene estados `accepted`, `clarification_required`, `queued`, `executing`, `completed`, `failed`, `refused`, `cancelled`. No añadir en este paso un `UnknownAction` ficticio a Core; **desconocido** designa la incertidumbre de diagnóstico del Host tras pérdida de respuesta, no un hecho asumido del mundo.

Para reconciliar un timeout futuro, se necesitarán mecanismos de correlación y consulta del resultado que acuerde Core 4.10. **No** adoptar ahora política implícita de reintentos, deduplicación, intervalos o idempotencia.

## 2. Compatibilidad: seis ejes independientes

| Eje del registro | Qué se fija o inspecciona | Situación comprobada |
|---|---|---|
| `CORE_RPG_BUILD` | Commit/build de Core; firma pública y ABI para Host | SHA `dcfcb83` sólo línea base; **no** UE5 validado |
| `CORE_CONTENT_CONTRACT` | Versión de manifests y definiciones JSON | Core `0.1.0` existe; **sin** payload Trek |
| `TREK_CONTENT_PACK` | Versión propia del pack y dependencias futuras | **No existe pack de producción definido** |
| `SAVEGAME_FORMAT` | Formato físico versionado, metadatos y migraciones | **No existe** |
| `HOST_CORE_ADAPTER` | ABI/herramientas/build y versión contrato Core↔Host | **No existe** |
| `PRESENTATION_ASSETS` | UE5, sensores, mallas, texturas, web/Companion | Versiones independientes de autoridad de mundo |

Los identificadores anteriores son **etiquetas para auditoría**, no nuevos campos obligatorios de Core. No meter `schema_version` del modelo Trek dentro de `content_contract_version` ni equiparar versión de asset con versión de guardado. El cambio visual puede admitir degradación o reconstrucción; un cambio de estructura de entidad o savegame **requiere revisión/migración**.

### Matriz de decisiones antes de cargar/ejecutar

| Situación | Decisión conservadora |
|---|---|
| Core mismo SHA conocido | Habilita contraste de compatibilidad, **no** certifica ABI UE5 |
| Core SHA diferente | Revisar API, contratos y suite; no asumir compatibilidad por número mayor |
| Content Contract desconocido | Rechazar carga de pack no soportado |
| Content Pack Trek cambia | Verificar referencias/semántica/dependencias |
| Savegame de formato desconocido | Rechazar y conservar original; no «intentar parsear» con adivinaciones |
| Savegame truncado, corrupto o referencialmente inconsistente | No mutar el mundo vivo ni sobrescribir archivo previo |
| ABI adaptador/Host no probada | No declarar integración compilada/jugable |
| Cambio de malla/textura | Revalidar asset/presentación sin regenerar entidad |
| Cambio de IA | Tratar salida como candidato no confiable igualmente |
| Migración no definida o sin cobertura | Mantener el guardado sin alterar y rechazar hasta acuerdo |

El registro JSON contiene las **10 decisiones `COMP-01…COMP-10`** para su verificación cruzada.

## 3. Migraciones: política sin inventar serializer

La **secuencia obligatoria conceptual** para un futuro migrador Core 4.7:

1. Conservar los bytes originales (y copia/backup según almacenamiento disponible); nunca guardar encima antes de verificar.
2. Inspeccionar cabecera/manifiesto y versiones **sin** modificar el WorldState activo.
3. Determinar si existe una ruta de migración explícitamente aprobada de origen a destino; en caso contrario, rechazar de forma segura.
4. Validar integridad, referencias, identidad y datos mínimos antes de transformar.
5. Construir estado candidato en un espacio aislado; convertir mediante un migrador versionado e idempotente sólo si esta propiedad ha sido demostrada.
6. Validar salida: mismos `EntityId` donde corresponda, historia/identidad visual, semillas, relaciones, conocimientos, dotación, guardias, causalidad.
7. Publicar el nuevo guardado **atómicamente sólo tras superar todas las condiciones**, dejando trazabilidad de versión y origen.
8. Si cualquier fase falla, preservar los bytes originales y la partida activa sin efectos parciales.

**Límites:** no sustituir entidades ausentes por NPC generados, no borrar eventos difíciles, no utilizar la fecha estelar redondeada como origen de tiempo, no volver a sortear identidades ni guardar un duplicado de WorldState en el Host.

Un guardado que no puede migrarse debe quedar recuperable por una versión compatible futura. No se decide aquí si el contenedor será JSON, binario, SQLite, snapshots, deltas o combinación: **eso corresponde al Core y a su mecanismo publicado**.

## 4. Matriz de 16 pruebas, con evidencia por nivel

| Prueba | Alcance | Estado 11-10-2026 |
|---|---|---|
| **F02-T01** | Identidad al crear/descargar/recrear Actor UE5 | BLOQUEADO Core+UE5 |
| **F02-T02** | Content Pack compatible y rechazo referencia rota | Prueba Core independiente **no ejecutada** |
| **F02-T03** | Orden sin permisos, rechazo sin efecto | BLOQUEADO Actions 4.10 |
| **F02-T04** | Resultado Sensores observador-relativo sin fugas | BLOQUEADO Knowledge 4.9 + Actions |
| **F02-T05** | Save/load conserva estado, historia y tiempo | BLOQUEADO Persistence 4.7 |
| **F02-T06** | IA caída, control manual Sensores sigue | NO EJECUTADO en Host |
| **F02-T07** | IA tardía y permisos revocados: cero efectos | BLOQUEADO Actions + Host |
| **F02-T08** | Compilación y enlace C++ Core con UE5 | NO EJECUTADO; necesita MSI/UE5 |
| **F02-T09** | Examinar CI existente Core main/rama 4.5 | **Solo observación remota previa**; no demuestra integración |
| **F02-T10** | Integridad de fuentes P02, refs P03 y registro P04 | **SUPERADA en CI con checkout real de la rama**: 24 fuentes, 73 selectores, 12 adaptadores, 19 rutas, 11 gaps |
| **F02-T11** | Validador rechaza errores introducidos deliberadamente | **9/9 unit tests OK**, repetidos también en GitHub Actions con checkout real |
| **F02-T12** | Política de campos vedados de Sensores | Comprobación **estática** del contrato, NO anti-leak runtime |
| **F02-T13** | Drift en SHA de fuente P02 | **Prueba sintética OK y comparación 24/24 SHA OK en CI**; detección preventiva, no migración |
| **F02-T14** | Seis ejes y dependencias pruebas/adaptadores | **Integridad referencial superada en CI**; compatibilidad runtime no probada |
| **F02-T15** | Timeout de orden y reconciliación sin doble efecto | BLOQUEADO Actions 4.10 |
| **F02-T16** | Rechazo atómico de partida corrupta/incompatible | BLOQUEADO Persistence 4.7 |

**Importante:** ninguno de T10–T14 con comprobación estática equivale a T01, T03, T04, T05 o T08 ejecutadas. El `sensor_result_contract.json` prohíbe campos de verdad, pero sólo una prueba sobre salida real demuestra que el Host no filtra.

### Evidencia de pruebas ejecutadas en P04

- Entorno de comprobación aislada: **Python 3.13.5 / Linux**.
- Comando ejecutado sobre una copia local del validador y su fixture construido expresamente: `python -m unittest discover -s . -p 'test_validate_f02_contracts.py' -v`. **Resultado: 9 pruebas, 9 OK** (valid fixture, fuente alterada, selector ausente, gap perdido, test ref inválida, restricción anti-fuga ausente, archivo borrado, ID repetido y normalización CRLF Windows).
- **Prueba real sobre checkout de GitHub Actions:** [workflow F02, run 38149311936](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38149311936), completado con conclusión **success**. Los logs muestran: `p02_sources=24`, `p02_selectors=73`, `p03_adapters=12`, `p03_source_paths=19`, `p03_gaps=11`, `p04_failures=13`, `p04_axes=6`, `p04_tests=16`; mensaje `PASS: documentary registries and provenance match` y `Ran 9 tests ... OK`. **El checkout local del asistente no fue posible por DNS**, pero el runner GitHub sí clonó y validó el repositorio real.
- Verificación independiente adicional: vía conector GitHub se contrastaron **24/24 SHA de blobs fuente P02** y **19/19 rutas de P03**; el workflow verifica también coherencia de los tres registros y campos vetados de Sensores. Las restricciones anti-filtración siguen siendo **estáticas**, no test de proyección real.
- Evidencia CI independiente sólo para F02-T09: [CoreRPG/main, run 38046482745](https://github.com/robdor80/CoreRPG/actions/runs/38046482745) y [CoreRPG/4.5, run 37812440972](https://github.com/robdor80/CoreRPG/actions/runs/37812440972), previos a cualquier integración Star Trek/UE5.

### Comandos para repetir la comprobación en cualquier checkout de la rama

```bash
python desarrollo/tools/validation/validate_f02_contracts.py
python -m unittest discover -s desarrollo/tools/validation -p 'test_validate_f02_contracts.py' -v
python desarrollo/tools/validation/validate_internal_references.py
```

El primer comando comprueba **fuentes P02 y hashes Git blob**, campos, el mapa de adaptadores, cobertura de gaps, IDs y refs P04, además de las restricciones textuales del contrato Sensores; sale con código 1 ante inconsistencia. En checkout Windows con archivos de texto CRLF, el verificador tolera normalización CRLF→LF para cotejar el blob Git de texto. Si cambia intencionadamente un contrato base, fallará hasta **re-auditar P02**; esa señal es deliberada.

La segunda orden ejecuta pruebas **aisladas** del propio verificador y no necesita Core ni red. La tercera reutiliza el validador existente del proyecto; sigue siendo independiente de P04.

## 5. Puertas de aprobación y próximos pasos

**Aceptación de diseño P04:** política de 13 fallos, seis ejes, diez reglas de compatibilidad y 16 pruebas trazadas; validador de fuentes y nueve tests **ejecutados satisfactoriamente en GitHub Actions sobre checkout real**. Esto **no** supone aceptación de ABI, serializer ni política de errores de Core.

**Para `CONTRATO_VALIDADO`:** CoreRPG debe acordar y publicar interfaces de control de transacciones, estados/errores, consulta tras timeout, tiempo, autorizaciones, proyección, persistencia y migración. Versiones/SHAs reales, CI y aprobación de consumidor Trek obligatorios.

**Para `CORE_INTEGRADO` y `UE5_JUGABLE`:** ejecutar los tests sobre el sistema real y el MSI, incluir fallos inducidos con datos reales y guardar evidencia del build. Hasta entonces, F02-P04 se anota **`DISEÑO_DOCUMENTAL_COMPLETO; EN_REVISION/BLOQUEADA_CORE`**, sin modificar `ESTADO_GLOBAL.json` ni cerrar F02/F01.

Relacionado: [arquitectura P03](ADAPTADORES_Y_FRONTERAS.md), [handoff Core](SOLICITUD_COORDINACION_CORE_P03.md), [plan P05](PLAN_INTEGRACION_PRIMER_CORTE.md), [criterios de cierre](../../CRITERIOS_DE_CIERRE.md).
