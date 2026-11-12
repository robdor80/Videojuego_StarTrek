# Planificación 2 — Bloque 10: Evolución galáctica en segundo plano y simulación offscreen

**Fecha:** 12/11/2026. **Objetivo:** cerrar los 10 bloques de Planificación 2 con madurez **REFERENCE_COMPLETE**, nunca anunciar un HOST/CoreRPG/UE5 galáctico ya operativo. **Ámbito:** coordinación del reloj y propuestas de tareas externas B01–B09, equidad, presupuestos, persistencia contractual y resultados conocidos, con demostración reproducible offline.

## Experiencia que queremos

Mientras el personaje pasa cuatro años en la Academia, sirve en una Oberth, está en un camarote de la Enterprise-D o duerme, las civilizaciones no esperan al jugador: nacen y desaparecen colonias, cambian rutas y acuerdos, progresan investigaciones y se atienden crisis *cuando sus sistemas propietarios acepten esos hechos*. Las naves NPC pueden completar trabajos sin nuestra presencia. La noticia llegará según los canales y retardos efectivos; el jugador puede ignorar un suceso, llegar tarde o descubrir décadas después sus huellas.

Eso **no** significa simular cada tripulante y cada comercio en 3D, ni hacer que un NPC distante avance su misión cuando la cámara mira en otra dirección. Las decisiones de alto nivel se registran en un mundo lógico persistente; la representación visual/LOD cambia el detalle de presentación, **jamás la verdad histórica**.

## Propiedad técnica y límites

- **CoreRPG** es el único dueño del reloj autoritativo, WorldState, transacciones, registros aceptados, reanudación y commits. La política de reloj —incluido un posible universo acelerado en juego— se fija fuera de este simulador. Nunca convertir automáticamente horas reales transcurridas con el juego cerrado en años ficticios.
- **B01–B09** siguen siendo dueños de sus reglas: política y población; expansión; conflictos; economía; historia; investigación; anomalías; crisis; expedientes de misiones. B10 no recalcula B04 ni acepta por sí mismo una misión B09.
- **F11/HOST**: orden de mando, sesión, autenticación, permisos, parada/reanudación y arbitraje de comandos.
- **UE5**: streaming del mapa, escenarios y actores visibles. LOD/posición del jugador sólo filtran vistas, no cambian el orden del trabajo.
- **Narrativa**: las temporadas pueden consultar hechos y generar oportunidades autorizadas, pero nunca fabricar hechos globales para sostener su capítulo.
- **Conocimiento/PADD**: rango no equivale a omnisciencia; sólo entregas acreditadas y clasificación autorizada dan visibilidad. Se respetan Primera Directriz, jurisdicción, secretos y noticias demoradas.
- **Entrega presente**: Python de referencia offline + JSON/contratos, fixture ficticio y CI. No hay daemon, motor nativo, servidor 24/7 ni runtime guardado/ejecutado en CoreRPG.

## Veinte paquetes GS001–GS020

| Paquete | Criterio |
|---|---|
| GS001 | Únicamente reloj virtual autorizado, sin reloj real ni render |
| GS002 | Identidad de campaña y revisión de WorldState obligatoria |
| GS003 | Cola determinista para intenciones externas aceptadas |
| GS004 | Reanudación/catch-up en lotes limitados |
| GS005 | Presupuesto positivo de propuestas por tick |
| GS006 | Cupo por dominio B01–B09 para evitar monopolio |
| GS007 | Envejecimiento de prioridad y orden estable |
| GS008 | Backpressure con retención de trabajo pendiente |
| GS009 | Identificadores de despacho persistentes y sin duplicados |
| GS010 | Nunca inventar intenciones ni hechos fuera de B01–B09 |
| GS011 | Titularidad de los nueve dominios y dependencias intacta |
| GS012 | B09 exige necesidad real aceptada; riesgo B08 insuficiente |
| GS013 | Simulación NPC sin jugador ni Enterprise-D como eje |
| GS014 | LOD y distancia exclusivamente presentación |
| GS015 | Acuses de CoreRPG externos, sin aplicar sus efectos |
| GS016 | Contrato de save/replay, journal encadenado SHA-256 |
| GS017 | Vistas según noticias recibidas y confidencialidad |
| GS018 | Rechazos atómicos, conflictos, timestamps y revisiones |
| GS019 | Caso sintético, adversariales, regresión dinámica/F13/Academia y CI |
| GS020 | Acta, manifiesto, fronteras runtime y cierre de Planificación 2 |

## Flujo causal de referencia

1. **Entrada**: snapshot de campaña y revisión; intenciones ya aceptadas por sus dueños y respaldadas por hechos previos, B09 con necesidad real; autorizaciones de rango de ticks procedentes del reloj central. El string «accepted» de una prueba local no acredita ninguna firma.
2. **Elegibilidad**: un trabajo sólo entra en cola desde su tick debido; la identidad no depende de distancia de jugador, apertura del mapa, número de FPS o si su región está cargada.
3. **Arbitraje**: presupuesto máximo por tick, cuotas por dominio y antigüedad creciente; desempate estable por tick de vencimiento e ID; si no hay presupuesto, el trabajo permanece en cola sin ser eliminado.
4. **Despacho**: emisión de propuesta PROPOSAL_ONLY con fuente, dominio, campaña, clasificación e identificador estable. No cambia población, inventario, resultados, guerra, recursos, naves, misiones ni canon.
5. **Resultado**: sólo un recibo de aceptación/rechazo ya aceptado por el escritor CoreRPG permite anotarlo como confirmado; el verdadero efecto deberá ejecutarse transaccionalmente en el sistema propietario.
6. **Memoria/reanudación**: se conserva la cola, despachos, recibos, reloj, revisión y hash encadenado de acciones. Un lote de catch-up se rechaza cuando excede el límite. El consumidor real deberá garantizar persistencia atómica y deduplicación también en fallos/reintentos.
7. **Información**: cada observador recibe únicamente despachos para los que existe entrega acreditada anterior o igual al corte de la vista y clasificación suficiente. El retraso de llegada no reescribe el resultado.
8. **Cierre**: reproducibilidad y pruebas integrales; *REFERENCE_COMPLETE* no equivale a un universo nativo jugable.

## Escenario

Fixture **SYNTHETIC_NONCANONICAL** «demo-2383»: seis intenciones de dominios B02, B04, B05, B06, B08 y B09, aprobadas exclusivamente dentro del caso ficticio. El presupuesto limitado exige repartir trabajo en ticks; una agencia NPC ya dispone de una necesidad B09 aceptada y recibe su propuesta sin jugador. Se verifica el acuse externo simulado de B04. El capitán conoce el expediente B09 únicamente al llegar un mensaje retrasado; una persona no autorizada no ve nada. Tres permisos de reloj virtual cubren ocho ticks por lotes, sin saltos temporales automáticos.

## Archivos

- Contrato: sistemas/universe/generation/background_galactic_evolution_reference_contract_v0.1.json
- Simulador: desarrollo/tools/generation/simulate_background_galactic_evolution.py
- Pruebas: desarrollo/tools/generation/test_simulate_background_galactic_evolution.py
- Fixture: desarrollo/validation/fixtures/background_galactic_evolution/verified_npc_offscreen_catchup_v0.1.json
- Workflow: .github/workflows/p2-b10-background-galactic-evolution.yml
- Manifiesto y acta: procedural_background_galactic_evolution_status_v0.1.json y P2_B10_ACTA_CIERRE_REFERENCIA_20261112.md.

## Puerta de aceptación y futuro de F13

Cierre de referencia exige: paquete íntegro GS001–GS020, JSON válido, simulador y pruebas adversariales, regresiones B01–B10 + F13 + Academia, última CI de PR verde, auditoría del diff/factores de autoridad y fusión segura. Actualizar explícitamente la frontera de diez bloques, sin alterar las capas 119/120 y sin promover F13 global.

**Siguiente trabajo después de cerrar Planificación 2:** integración nativa y por hitos en CoreRPG/HOST/UE5 (reloj persistido, snapshots atómicos, consumidores reales, órdenes F11, ejecución de dominios, sensor/PADD, benchmarks). No duplicar en Star Trek servicios genéricos que pertenecen a CoreRPG. Respetar AGENTS.md; nada de laboratorios temporales versionados.
