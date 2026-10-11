# F02-P05 — Plan técnico del primer corte jugable

**Objetivo de producto confirmado en F01:** la **v0.0.1 será prueba interna** de una guardia en la **Consola de Sensores**, no lanzamiento comercial ni misión obligatoria del producto final. Una v0.0.2+ podrá ensayar Academia u otros sistemas de forma independiente. No insertar en esta fase la idea del replicador u otras funciones ajenas a Sensores.

**Dependencia autoral independiente:** la clase base de Imperator (Galaxy/Sovereign/Odyssey) sigue pendiente de decidir por el autor; no condiciona la auditoría de Core ni autoriza elegir una Dama. Un puente piloto técnico en F07 puede ser diferente.

## Secuencia mínima, sin atajos de autoridad

| Orden | Entregable | Responsable lógico | Fase y puerta |
|---|---|---|---|
| 1 | CoreRPG 4.5 integrado en `main` con invariantes, CI y API revisada | CoreRPG | Dependencia F02→F03; hoy NO integrada |
| 2 | Acordar modelo vivo mínimo, IDs, contenido y límites de edición | CoreRPG + Star Trek | F02/F03; sin inventar payload Trek en 0.1.0 |
| 3 | Reglas/acciones/eventos y persistencia del mínimo de guardia | CoreRPG + especificación Star Trek | F03–F06; interfaces sólo después de disponibilidad real |
| 4 | Resolver orden NPC→jugador→barrido→resultado→informe/bitácora con pruebas, secretos protegidos | Star Trek + CoreRPG | F04–F06; ejecución de referencia ≠ integración |
| 5 | Spike UE5 Windows: compilar Core, crear entidad, asociar actor, descargar y conservar ID | Host UE5 + CoreRPG | F07; puede explorarse antes sin certificar producción |
| 6 | UX de Sensors operable con ratón/teclado, sin IA ni Companion obligatorios | Star Trek/Host | F06–F08 |
| 7 | Encadenar una guardia completa, save/load, negativa por permisos, fallos IA, logs, evaluación | Integración global | F08 `ACEPTACION_SUPERADA` solo tras E2E real |

## Camino de un único escenario de aceptación

**Fixtures reutilizables, no misiones finales:** `validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json` y `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`. Contexto de prueba actual: época TNG/DS9/Voyager, fecha 2372-03-14, semilla `fixture_sensor_v0_0_1`. La elección de nave definitiva no altera esos invariantes.

Secuencia: estado ya materializado → capitán NPC ordena → alférez jugador abre consola → barrido estructurado → motor valida parámetros y recursos → motor devuelve observación parcial/total → transferencia/autorización → bitácora causal → informe y evaluación → guardar/cargar → continuar sin recrear verdad ni NPC.

## Validación cruzada requerida

| Contraparte | Validar antes de cierre F02 | Estado verificado hoy |
|---|---|---|
| CoreRPG | Dependencias reales 4.5 y contrato de adaptación, ownership, acciones previstas | `main` hasta 4.4; rama 4.5 parcial con CI; **pendiente validación formal** |
| Star Trek | Coherencia con Sensores, órdenes, visibilidad, dotación, F01 | Modelos de referencia localizados; **pendiente validación E2E** |
| Host UE5 | Compilación ABI, threading, mapa EntityId→Actor, controles PC | **NO_EJECUTADO** |
| academiaflota | La web sigue como apoyo educativo; evitar doble fuente de contenido | Sin cambios en F02 |
| NAP/Rob3D | Entrega 3D y licencias independientes de lógica | Sin importación nueva en F02 |
| Servicio IA | Caída/reintento seguro y separación propuesta/ejecución | Contrato normativo localizado; sin servicio E2E en F02 |

## No regresión, exclusiones y cierre

- No implementar un segundo Core, persistencia paralela, IA con autoridad ni nuevo mecanismo genérico de delegación.
- No modificar CoreRPG ni academiaflota en esta fase sin PR específico y revisión de su responsable.
- No cerrar F01 por inferencia; [PR F01](https://github.com/robdor80/Videojuego_StarTrek/pull/2) continúa abierta hasta DEC-0001.
- No afirmar que UE5/v0.0.1 es jugable porque exista un manual, fixture o script Python.
- **Puerta F02:** contratos contrastados con versiones reales, decisiones de frontera aceptadas por Core/Host, pruebas apropiadas y acta de evidencia. A falta de esto, el paso P05 permanece `EN_REVISION`/bloqueado y la fase no pasa a `CERRADA`.

## Referencias de seguimiento

- `AUDITORIA_CORE_RPG_2026-10-11.md`
- `MATRIZ_INTERCAMBIO_Y_PROPIEDAD.md`
- `ADAPTADORES_Y_FRONTERAS.md`
- `FALLOS_VERSIONES_Y_PRUEBAS.md`
- `docs/roadmap/master/CRITERIOS_DE_CIERRE.md`
