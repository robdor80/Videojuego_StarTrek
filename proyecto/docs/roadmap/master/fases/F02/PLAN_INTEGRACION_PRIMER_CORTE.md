# F02-P05 — Plan de integración y traspaso operativo a F03

**Fecha:** 11-10-2026. **P05: PLAN DE EJECUCIÓN COMPLETADO, VALIDACIÓN EXTERNA PENDIENTE.** La planificación está aprobada para trabajo preparatorio por la luz verde del autor; **no** hay aprobación técnica de APIs por los responsables Core/Host, ni runtime validado. F02 sigue **EN_REVISION/BLOQUEADA_CORE** a su madurez objetivo `CONTRATO_VALIDADO`. Este documento conserva la foto técnica del 11-10-2026; la PR #3 sigue pendiente de fusión en la revisión del 13-10-2026.

**Propósito:** convertir P01–P04 en trabajo verificable, sin crear un segundo Core, sin inventar llamadas C++ y sin marcar como jugable un conjunto de JSON/diagramas.

## 1. Línea base contrastada antes de escribir

| Dependencia | Estado remoto comprobado | Consecuencia |
|---|---|---|
| CoreRPG `main` | `dcfcb83c9853e005b5450bd39e0ba693cb91e257` | `WorldState` todavía mínimo; NO Actions, Knowledge ni Persistence de partida |
| Core 4.5 `feat/generic-world-state` | `2a3da891d8c56e9868c7bd67dbeb6041509df2ce`, **no en main** | Permite preparar interfaces/contratos en papel; no se pueden certificar integraciones |
| Star Trek `main` | `5d95b13fb7fef962c64f9b770bc45d8fc3fa35cd` | Se han añadido ideas desde creación de F02; no sustituir `main` ni sus cambios |
| F01 (foto 11-10-2026) | [PR #2](https://github.com/robdor80/Videojuego_StarTrek/pull/2) **estaba abierta en borrador**, con DEC-0001 pendiente | **Superado 13-10-2026:** PR #2 fusionada; Galaxy → nueva Clase Valhalla aprobada |
| F02 (foto 11-10-2026) | [PR #3](https://github.com/robdor80/Videojuego_StarTrek/pull/3) estaba en borrador; **13-10-2026: Ready for review** | P01–P04 auditoría, contratos y QA estática; P05 diseño/handoff; runtime sin validar |
| QA documental | [F02 Actions run 38149428834](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38149428834) `completed/success` | Valida documentación en checkout real; **NO** compilación/integración de Core o UE5 |

**Decisión de alcance ya tomada:** `v0.0.1` es una **prueba interna de una guardia en Sensores** como alférez que recibe órdenes de un capitán NPC. No es lanzamiento final ni obliga a elegir ya la clase definitiva. `v0.0.2+` podrá ensayar Academia u otros módulos posteriormente.

## 2. Plan operativo ordenado y propietarios

El registro [HOJA_RUTA_EJECUCION_P05.json](HOJA_RUTA_EJECUCION_P05.json) es la fuente trazable de **11 paquetes de trabajo (INT-00 a INT-10)**, responsables, predecesores, adaptadores, fases Core requeridas, pruebas y puerta de salida. **No es una API/contrato runtime.**

| Paquete | Cuándo | Responsable propuesto | Entrega de aceptación | Situación |
|---|---|---|---|---|
| **INT-00** | F02-P05 | Star Trek + coordinación | Documentos P01–P05 y referencias; **DEC-0001 ya resuelta en F01** sin modificar el alcance de Sensores | Documentado |
| **INT-01** | Core 4.5 | Equipo CoreRPG | Merge de `WorldState` extendido en `main` + ABI/API verificadas + CI | **BLOQUEO CRÍTICO** |
| **INT-02** | F03-P01 | CoreRPG + Trek | Semilla/identidad/cronología/materialización persistente antes de ser observada | Diseño disponible; runtime bloqueado |
| **INT-03** | F03-P02 | CoreRPG + Trek Sensores | Verdad del mundo separada de observaciones y datos vedados | Diseño disponible; requiere Core 4.9 |
| **INT-04** | F03-P03 | CoreRPG + Trek | Turnos, reloj y actividad fuera de escena, con eventos causales | Diseño disponible; requiere Core 4.8/4.10 |
| **INT-05** | F03-P04 | CoreRPG | Guardado/carga y migración/denegación segura, sin regeneración | Requiere Core 4.7+ y datos vivos |
| **INT-06** | F03-P05 | CoreRPG + Trek | Determinismo/identidad/observación/continuidad probados sobre runtime | Requiere INT-02…INT-05 |
| **INT-07** | F04/F05 | CoreRPG + Trek | Dotación, guardias, permisos, capitán NPC→alférez, orden→resultado | Requiere Actions 4.10 |
| **INT-08** | F06 | CoreRPG + Trek | Sensores deterministas, sin contactos fabricados ni filtraciones | Requiere Knowledge 4.9 y Actions |
| **INT-09** | F07 | Host Windows UE5 + CoreRPG | Spike C++/ABI: entidad↔Actor, unload/reload, controles PC | Puede anticiparse tras INT-01 |
| **INT-10** | F08 | Integración de los tres responsables | Guardia de Sensores v0.0.1 jugable con save/load, eventos, evaluación y QA | Requiere INT-05…INT-09 |

**Paralelización segura:** INT-09 (spike visual de identidad) puede empezar en cuanto Core 4.5 esté disponible, **sin** esperar a acabar F03–F06, pero no certifica un juego persistente. La especificación/fixtures de F03-P01 y F03-P02 pueden auditarse ya, aunque el runtime siga bloqueado. F01-DEC-0001 **no bloquea** la auditoría lógica ni el spike con puente de prueba.

## 3. Condición mínima de una prueba interna de Sensores

**Fixture oficial sin cambio:** `desarrollo/validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`.

| Parámetro | Valor fijo del fixture |
|---|---|
| Época | `tng_ds9_voyager` |
| Fecha de campaña | `2372-03-14` |
| Semilla | `fixture_sensor_v0_0_1` |
| Punto de partida | Sistema ya materializado; no se crean entidades por escaneo |
| Jugador | Alférez destinado a Sensores, no capitán automático |
| Mando | Capitán NPC legítimo ordena y supervisa |
| Controles | Teclado/ratón desde MSI; no requiere Gemini, internet ni Companion |
| Bucle | Orden → consola → barrido → resultado por observador → informe → bitácora → valoración → guardar/cargar |

**Ocho adaptadores obligatorios para un corte integrado:** `ADP-01` (identidad), `03` (tiempo), `04` (órdenes), `05` (sensores), `06` (eventos), `07` (conocimiento), `08` (persistencia), `09` (UE5). `ADP-02` (contenido) permite ampliar, pero el primer spike puede usar fixture acotado; `ADP-10` (IA) y `ADP-11` (interconsolas ampliadas) no son necesarios para demostrar los controles iniciales. Ni Academia completa ni la Dama elegida son requisito del spike técnico.

### Trece pruebas imprescindibles

El registro JSON enlaza **13/13 invariantes del fixture** con un paquete responsable, **sin marcar ningún test E2E como ejecutado**:

| ID del fixture | Responsable de prueba inicial | Se comprobará |
|---|---|---|
| `deterministic_world`, `reality_precedes_scan`, `persistent_identity`, `era_validity` | INT-02 | Generación estable por semilla, validez temporal, realidad previa y misma identidad |
| `hidden_information_gate`, `anti_leakage`, `observer_relative_contacts`, `knowledge_visibility` | INT-03 | Información revelada adecuada al observador y límites de conocimiento |
| `detection_not_truth_creation`, `system_state_matters`, `ai_boundary` | INT-08 | Barridos alteran observación, dependen de la nave; IA no inventa datos |
| `event_chain` | INT-07 | Orden, acción, resultado e informe relacionados causalmente |
| `save_load_roundtrip` | INT-05 | Continuidad de identidad, historia y observaciones tras recargar |

Los casos no positivos también son obligatorios: guardia sin anomalías, orden rechazada por falta de autoridad, pérdida de señal sin hipótesis ficticia, revelación bloqueada de secretos, fallo de IA, respuesta tardía, timeout desconocido, partida corrupta y desaparición de un Actor sin borrar su NPC.

## 4. Punto de entrada concreto a F03

**F03-P01, primer trabajo seguro que se puede iniciar inmediatamente en otra conversación:**

1. Leer **las fuentes existentes** en `sistemas/universe/generation/`, `sistemas/universe/chronology/`, `sistemas/gameplay/persistence/`, `proyecto/docs/decisions/universal_stardate_system.md`, y las 24 fuentes P02. Evitar mover o replicar documentos.
2. Clasificar cronología, `campaign_seed`, `generator_version`, `EntityId`, `character_id`, `ship_id`, materialización y procedencia (canon frente a procedural), sin inventar un serializador.
3. Elaborar matriz de transiciones *latente → materializado → observado → descargado visualmente → cargado de nuevo*, con propiedad y no regresión por fase.
4. Revisar Core `main` antes de cualquier interfaz: si 4.5 sigue fuera, documentar propuesta y **bloquear únicamente las pruebas runtime dependientes**, no el trabajo de diseño.
5. Abrir PR específica de **F03** para este trabajo; no mezclar cambios F03 en PR #3. No proclamar F03 cerrada, no alterar `ESTADO_GLOBAL.json` hasta F01/F02 coherentes y revisadas.

**Entregable esperado F03-P01:** `CONTRATO_DE_IDENTIDAD_Y_MATERIALIZACION` basado en archivos existentes, matriz de identidad/semillas/fechas y casos de prueba de continuidad, clasificados como `DISENO_VALIDADO` o `EN_REVISION` hasta acuerdo Core. Nunca crear un motor de estado paralelo.

## 5. Puerta de verificación y decisión GO/NO-GO

| Ámbito | Evidencia precisa requerida | Resultado 11-10-2026 |
|---|---|---|
| **P05 documentación** | 11 trabajos trazados, 13 invariantes, prioridades, owners, links y dependencias comprobables | **PREPARADO PARA REVISIÓN** |
| **P05 coordinación con Core** | 4.5 real en `main`; negociación Q01–Q08 del [handoff P03](SOLICITUD_COORDINACION_CORE_P03.md); firmas/CI y aceptación | **NO-GO: PENDIENTE** |
| **P05 coordinación con Host** | Respuestas H01–H04, toolchain/ABI UE5/Windows y prueba mínima de EntityId↔Actor | **NO-GO: PENDIENTE** |
| **F02 completa al nivel objetivo** | Contratos Core+Host contrastados, evidencia del estado, PR revisada y sincronización con F01 | **NO CERRAR TODAVÍA** |
| **F03 documentación preparatoria** | Usar el índice de fuentes existente y abrir su propia PR de fase | **GO** |
| **F03 integración runtime** | Reglas y API Core publicadas y pruebas de la fase | **NO-GO HASTA DEPENDENCIAS** |
| **F08 v0.0.1 jugable** | Build en MSI + 13/13 escenarios y todos los bloqueos cerrados | **NO-GO: NO EJECUTADO** |

**No se necesita decisión autoral adicional para continuar F03-P01 documental**: F01 **ya resolvió** la elección Galaxy → Clase Valhalla. Esta elección es independiente del primer puente de Sensores, y **no** acredita integración Core/UE5.

## 6. Gestión de cambios, seguridad y trazabilidad

- Ni `CoreRPG`, `academiaflota`, NAP ni UE5 han recibido cambios desde esta PR F02.
- Core sigue siendo la **única fuente autoritativa** de realidad; no crear `WorldState`, `RulesEngine`, `PersistenceCore` ni motor de órdenes alternativo en el repo Star Trek.
- UI/IA sólo reciben proyección autorizada; el texto de respuesta no aplica mutaciones, y un timeout no confirma fallo/éxito de la acción.
- Cada futura prueba registra SHA Core, SHA Trek/Host, contexto del fixture, plataforma y logs. `PASS` de validación JSON no equivale a `CORE_INTEGRADO` ni `UE5_JUGABLE`.
- Las líneas base de P02/03/04 no deben actualizarse automáticamente para ocultar cambios; toda incompatibilidad obliga a reauditar.
- Se mantiene `ESTADO_GLOBAL.json` sin tocar desde esta rama. **Actualización 13-10-2026:** F01/DEC-0001 ya aprobada e incorporada en `main` por PR #2; PR #3 pasó a revisión. F02 mantiene pendientes sus puertas de validación Core/Host y no se declara cerrada.

## Referencias

[P01 — auditoría real](AUDITORIA_CORE_RPG_2026-10-11.md) · [P02 — matriz y fuentes](MATRIZ_INTERCAMBIO_Y_PROPIEDAD.md) · [P03 — adaptadores](ADAPTADORES_Y_FRONTERAS.md) · [P04 — fallos y pruebas](FALLOS_VERSIONES_Y_PRUEBAS.md) · [Plan de trabajo P05 en JSON](HOJA_RUTA_EJECUCION_P05.json) · [Criterios globales](../../CRITERIOS_DE_CIERRE.md) · [F03](../F03/README.md).
