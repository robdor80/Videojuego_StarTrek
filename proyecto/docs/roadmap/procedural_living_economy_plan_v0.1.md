# Planificación 2 · Bloque 4 — Economía viva interplanetaria e interestelar v0.1

**Estado:** CANDIDATO EN AUDITORÍA (no equivalente a runtime CoreRPG). **Fecha:** 2026-11-12.
**Secuencia:** Bloques 1, 2 y 3 COMPLETE; Bloque 4 es el único bloque activo; Bloques 5–10 no iniciados.

## Objetivo y autoridad

Permitir producción, uso, escasez, comercio y transporte **causales** entre ubicaciones preexistentes. Las consecuencias se conservan aunque el jugador no observe el sistema.

```text
existencia y estados persistentes de nodos + recursos + operadores + instalaciones + rutas
→ demanda/orden/contrato autorizado
→ producción o consumo comprobado / reserva y despacho material
→ tránsito de vehículo con origen, destino y plazo
→ entrega o retención por frontera/avería/bloqueo
→ saldos/stock/consecuencias y trazabilidad
→ observación y conocimiento sujeto a acceso
```

La autoridad del WorldState, reloj, eventos genéricos, transacciones, persistencia, acciones y LOD pertenece exclusivamente a **CoreRPG**. Este bloque define reglas Star Trek, un simulador determinista de referencia y pruebas; no crea un backend paralelo ni altera F11/HOST/UE5.

## Paquetes

| Código | Entrega | Estado objetivo |
|---|---|---|
| LE001 | Límites CoreRPG, autoría, versión y referencias | CANDIDATE |
| LE002 | Nodos de stock, titularidad, jurisdicción e identidades | CANDIDATE |
| LE003 | Demanda, reservas, consumo y escasez explícitas | CANDIDATE |
| LE004 | Producción material, trabajo, capacidad e insumos | CANDIDATE |
| LE005 | Replicación: energía, insumos, patrón, permiso | CANDIDATE |
| LE006 | Sociedades postescasez sin convertirlas en regla universal | CANDIDATE |
| LE007 | Operadores comerciales y acuerdos verificables | CANDIDATE |
| LE008 | Modelos de compensación sin moneda ni tasa universal inventadas | CANDIDATE |
| LE009 | Rutas, naves, plazas y transporte con causalidad temporal | CANDIDATE |
| LE010 | Fronteras, legalidad, bloqueos y demoras | CANDIDATE |
| LE011 | Flujos, pérdidas y conciliación de existencias | CANDIDATE |
| LE012 | Presión económica y resiliencia sin crear guerras/crisis | CANDIDATE |
| LE013 | Estado persistente, idempotencia, orden temporal y LOD | CANDIDATE |
| LE014 | Separación entre verdad, conocimiento e IA | CANDIDATE |
| LE015 | Simulador de referencia, fixtures y pruebas positivas/negativas | CANDIDATE |
| LE016 | Auditoría transversal, índice y cierre administrativo | CANDIDATE |

## Fuentes y reutilización

- Plan de bloques: `proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`.
- LORE-04B01–B06 y `lore04b_cases_v0.1.json`: límites culturales, Tierra/Federación, Ferengi, Bajor, Cardassia y fronteras.
- `sistemas/gameplay/economy/replicator_post_scarcity_contract.json`.
- `sistemas/gameplay/economy/civilian_trade_operator_contract.json`.
- `sistemas/universe/generation/procedural_civilization_economy_resource_trade_grammar_v0.1.json`.
- `sistemas/universe/generation/civilization_economy_governance_history_contract.json`.
- `sistemas/universe/generation/colonization_offscreen_simulation_contract_v0.1.json`.
- `desarrollo/validation/consistency/movement_logistics_economy_diplomacy_invariants_v0.1.json`.
- Bloque 3: control efectivo/bloqueo no equivale a soberanía; economía consume los cambios **ya resueltos** por sus responsables.

Los contratos existentes siguen siendo la fuente: LE no sustituye ni copia sus campos canónicos. Los esquemas nuevos especifican un **adaptador de prueba**, no una migración obligatoria de CoreRPG.

## Reglas normativas

1. Solo los hechos existentes en el WorldState pueden producir stock, actores, rutas y capacidad. El jugador no provoca una oferta «por aparecer».
2. Producción consume físicamente insumos y energía, exige tecnología, instalación operativa, mano de obra/capacidad disponible y autoridad. Una fórmula declarada no equivale a fabricación instantánea.
3. Replicación exige patrón autorizado, soporte material y energía; ni replicadores, ni postescasez, ni riqueza generan libremente componentes estratégicos.
4. Consumo, comercio y despacho no permiten inventario negativo; cuantías no finitas ni negativas se rechazan.
5. Un movimiento espacial necesita origen, destino, operador/vehículo, ruta existente, capacidad suficiente, acceso fronterizo y tiempo; no teletransporta mercancías.
6. Despacho retira stock de origen y lo deja **en tránsito**. Entrega valida llegada y acceso actual; bloqueo posterga sin crear ni destruir bienes.
7. Destrucción/merma necesita un evento causal explícito y evidencia, sin desaparición automática al cambiar LOD.
8. Un intercambio requiere aceptación y autorización, titularidad, existencia y forma de contraprestación determinada o renuncia explícita. `UNKNOWN` nunca equivale a «gratis».
9. No existe tipo de cambio ni salario universal; latinio (incluidas denominaciones ferengi), trueque, donación, servicios, asignación y monedas locales permanecen **modelos distintos**.
10. El régimen económico lo determinan jurisdicción, política y contexto temporal, no la especie biológica ni una etiqueta general «Federación».
11. La presión de abastecimiento puede generar **candidatos** para diplomacia, colonización, guerras o crisis; no ejecuta ni reemplaza los bloques propietarios.
12. La misma secuencia de eventos produce idéntico resultado en LOD alto y bajo; no reroll de materialización.
13. Un `event_id` repetido con contenido idéntico es idempotente; reutilizarlo con otro contenido se rechaza.
14. Evento fallido no cambia ni parcial ni silenciosamente el estado.
15. Tiempos, hechos, cantidades y nombres desconocidos siguen `UNKNOWN`; nunca se sustituyen por valores plausibles inventados.
16. Las conversaciones de IA, rumores y pronósticos no alteran stock, demanda real, condiciones ni resultados; solo proponen acciones y expresan conocimiento autorizado.
17. La llegada del jugador, un guion y una misión futura no son variables económicas.
18. Un bloqueo declarado por la autoridad de conflicto puede afectar rutas. Este bloque no declara guerras, redefine soberanía ni crea tratados.

## Adaptador de referencia

El esquema `sistemas/universe/generation/living_economy_reference_contract_v0.1.json` define un subconjunto autocontenido:

- `stores`: inventario entero por artículo, `owner_ref`, `location_ref`.
- `facilities`: producción autorizada y replicadores con `power_units`, `feedstock`, `patterns`, `operational`.
- `routes`: origen/destino, `open`, `legal_access`, capacidad y tiempo mínimo.
- `vessels`: identidad preexistente, capacidad y disponibilidad.
- `shipments`: manifestaciones persistentes, nunca duplicadas.
- `wallets`: saldos por unidad de cuenta explícita; ausencia de wallet no equivale a crédito.
- `event_log`: eventos causales aceptados y resúmenes; el `event_id` conserva su huella.

Tipos de evento de prueba: `produce`, `replicate`, `consume`, `dispatch`, `deliver`, `trade`, `set_route_access`, `loss`. Se procesan **acciones explícitas**, jamás un motor periódico de precios/salarios o el scheduler galáctico del futuro Bloque 10.

El CLI de referencia nunca escribe en el repositorio: consume un JSON y emite un estado candidato en stdout. No debe utilizarse como runtime jugable.

## Matriz de escenarios exigida

- Producción con insumos, energía y capacidad reales; rechazo por insuficiencia.
- Réplica permitida; rechazo por patrón, energía, feedstock o pieza no soportada.
- Consumo sin saldos negativos y evento de pérdida causal trazable.
- Despacho legítimo; stock permanece en tránsito hasta tiempo de entrega.
- Bloqueo de ruta antes del despacho; cierre de frontera **después** del despacho aplaza entrega.
- Viaje sin nave, ruta, jurisdicción o capacidad es rechazado.
- Comercio con contraprestación real; negociación `UNKNOWN` rechazada; transferencia no duplicada.
- Idempotencia, rollback, orden temporal, conservación para mercancía no transformada y continuidad LOD.
- Situación ferengi de latinio sin fijar equivalencia global.
- Hospital de colonia con replicador sin energía: cero fabricación.
- Rumor de escasez, aparición del jugador y salida de LOD: cero cambio de World Truth.

## Cierre, riesgos y criterio de verdad

Cerrar el **diseño de referencia Star Trek** solo si contratos, fixtures, CLI y pruebas locales/CI funcionan, índices son consistentes y la PR está fusionada. No afirmar economía viva en UE5/Host ni en CoreRPG hasta disponer de integración/runtime específico y pruebas de persistencia de campaña real.

**Pendencias ajenas a este bloque:** integración CoreRPG real; generación de historia previa (B5); invención científica (B6); fenómenos (B7); crisis (B8); misiones (B9); scheduler galáctico (B10). Esas dependencias no impiden completar el alcance **de referencia** de B4.
