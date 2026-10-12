# F03-P03 — Tiempo causal, eventos y vida fuera de escena

**Fecha:** 2026-10-11. **Estado:** CONTRATO PREPARATORIO, no simulación Core integrada. **Dependencias runtime:** Core 4.5, 4.8 y 4.10 aún no verificadas en `main`.

## Regla fundamental

La nave, tripulación, estación, colonia y civilizaciones continúan existiendo mientras ningún Actor 3D las representa. LOD ajusta el coste y la granularidad, no detiene el mundo ni concede recursos, teletransportes o actividades imposibles. CoreRPG es dueño de reloj, ejecución, agenda genérica y aplicación de eventos; Star Trek aporta tiempos de viaje, protocolos de guardia, requisitos de puestos y causalidad específica. **No se implementa simulador paralelo en esta PR.**

Fuentes existentes: `universe/generation/ship_facility_offscreen_simulation_contract.json`, `universe/generation/persistent_population_materialization_rules.json`, `gameplay/ship_operations/operational_event_log/operational_event_contract.json`, `event_type_catalog.json`, `gameplay/careers/academy_path/life/academy_offscreen_life_contract_v0.1.json` y `docs/decisions/universal_stardate_system.md`. Trabajo F02 INT-04 (PR #3).

## Ciclo causal mínimo

1. Partir de snapshot autoritativo en timestamp exacto `t0`, no de la fecha estelar representada.
2. Disponer sucesos/compromisos/órdenes pendientes con identificador, `due_at` y sus condiciones, sin convertir una sugerencia remota en orden.
3. Establecer horizonte `t1` no anterior a `t0`; procesar por tiempo efectivo y desempate estable definido por el motor (evitar depender del orden de iteración del contenedor).
4. Comprobar previamente autoridad y recursos requeridos, ocupación/ubicación, duraciones, rutas y restricciones. Un tripulante no puede ocupar dos puestos incompatibles simultáneamente.
5. Resolver resultado autorizado una sola vez por `action_id` / clave de idempotencia acordada en Core; añadir hechos/eventos con `causal_refs` y estampar `occurred_at`.
6. Marcar trabajo finalizado, suspendido, caducado o pendiente por efecto **registrado**. Un fallo indeterminado exige consulta/reconciliación antes de reintentar.
7. Persistir cursor de simulación, órdenes/reintentos/eventos y estado materializado de manera atómica; volver a LOD alto desde el estado actual, sin reconstruir desde una escena previa.

## Invariantes y límites

| Ámbito | Invariante | Caso que debe rechazarse |
|---|---|---|
| Reloj | Timestamps monotónicos a nivel de cadena causal | Evento hijo antes del causante |
| Ocupación | Un mismo individuo no ocupa simultáneamente compromisos exclusivos | Estar de guardia en Sensores y en enfermería a la vez |
| Viaje | Posición sólo avanza en tiempo/ruta factible | Nave en otro sistema sin tiempo de tránsito |
| Recursos | Combustible/energía, reparación, mantenimiento y suministros tienen coste | Reparación instantánea de daño sin recursos |
| Simulación agregada | Hechos rutinarios pueden agruparse; hechos irreversibles quedan individualizados | Muerte, destrucción, abandono, refit o daños graves sin evento |
| NPC | Sigue teniendo agenda y memoria fuera de cámara | El NPC desaparece cuando UE5 elimina Actor |
| Instalaciones | Generación y construcción responden a demanda, logística y contexto político | Estación aparece porque el jugador la necesita |
| Idempotencia | Catch-up del mismo intervalo sin nuevos eventos no reejecuta acciones | Reiniciar duplica evento, carga o ascenso |
| Dependencias | No ejecutar una orden sin su autorización/contexto válido al instante de ejecución | Delegación ya revocada pero acción ejecutada |
| Observación | Avance offscreen no vuelve conocimiento universal | NPC ausente aprende un secreto por existir evento |

## Resolución de interrupciones

- **Desconexión UI/IA:** el tiempo de campaña se gobierna por política de sesión Core, no por tiempo de red. No inferir avance simplemente por reloj real sin una decisión/contrato.
- **LOD bajo durante misión:** las operaciones continúan de forma acotada; conservar objetivo, ETA factible y consecuencias persistentes.
- **Interrupción Save/Load:** restaurar cursor confirmado y reanudar con seguridad; no aplicar dos veces una orden cuyo resultado ya está confirmado.
- **Imposibilidad por conflicto de agenda:** registrar rechazo/espera, jamás desplazar NPC por comodidad de escena.
- **Fallo de recursos o permiso:** evento de error sin mutación indebida del estado; reevaluar condiciones cuando exista nueva orden.
- **Intervalo largo:** segmentar por cambios causalmente relevantes, con límites/criterios de agregación definidos en Core; no congelar crisis relevantes ni ejecutar simulaciones infinitas.

## Secuencia ilustrativa (no resultado simulado por Core)

| Instante campaña | Suceso | Dependencia |
|---|---|---|
| 2372-03-14T10:42:11 | Capitán NPC ordena barrido a alférez de Sensores | Orden/autoridad |
| 2372-03-14T10:42:14 | Alférez acepta orden | Orden anterior |
| 2372-03-14T10:42:18 | Inicia uso exclusivo de consola | Guardia vigente, consola operativa |
| 2372-03-14T10:42:29 | Sensores producen resultado estructurado | Observación contra verdad preexistente |
| 2372-03-14T10:42:41 | Se informa al capitán | Resultado previo |
| 2372-03-14T10:42:47 | Se transfiere subconjunto a Ciencia | Resultado + derecho a compartir |

Las horas y eventos proceden de `gameplay/ship_operations/operational_event_log/sensors_vertical_slice_example.json`; no son una ejecución del videojuego.

## QA pendiente de runtime

`F03-T12` simulación con Actor descargado; `F03-T13` agenda exclusiva imposible; `F03-T14` viaje imposible, recursos y plazo; `F03-T15` replay de catch-up sin ejecución doble; `F03-T16` eventos causalmente ordenados y visibles solo por canal legítimo. La suite P05 comprueba un **caso documental de cadena causal**, no un planificador real.
