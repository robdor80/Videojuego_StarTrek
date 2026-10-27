# F03-P01 — Cronología, semillas, identidad y materialización

**Fecha de auditoría:** 2026-10-11. **Estado:** ESPECIFICACIÓN DOCUMENTAL PREPARADA / INTEGRACIÓN CORE BLOQUEADA. **Rama:** `docs/f03-world-knowledge-persistence`. **Producto:** Star Trek RPG 3D en PC; el ejemplo de Sensores v0.0.1 es prueba interna, no lanzamiento.

## 1. Fuente y autoridad

Se reutilizan, sin duplicar ni trasladar:
- `sistemas/universe/chronology/README.md`, `sistemas/universe/chronology/temporal_anchors/temporal_anchors.json`, `sistemas/universe/chronology/era_profiles/*/era_profile.json`;
- `proyecto/docs/decisions/campaign_continuity.md`, `proyecto/docs/decisions/universal_stardate_system.md`;
- `sistemas/universe/generation/procedural_generation_rules.json`, `generated_system_contract.json`, `persistent_entity_identity_contract.json`, `persistent_population_materialization_rules.json`, `observable_entity_model.json`, `civilization_latent_observed_materialized_pipeline_v0.1.json`;
- `sistemas/gameplay/persistence/persistent_state_roundtrip_contract.json`, `desarrollo/validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`.
- Traspaso documental F02: `proyecto/docs/roadmap/master/fases/F02/PLAN_INTEGRACION_PRIMER_CORTE.md`, paquete INT-02. **Actualización 13-10-2026: PR #3 ya fusionada en `main`; integración técnica Core/UE5 permanece pendiente.**

**Propiedad:** CoreRPG crea/valida IDs, reloj, hechos y mutaciones autoritativas cuando existan sus interfaces. Star Trek proporciona semillas de escenario, reservas canónicas, restricciones de época, perfiles de generación y referencias. UE5 materializa representaciones visuales desechables; sensores consultan, nunca generan la realidad.

## 2. Cronología y origen de una campaña

- El tiempo exacto de campaña (ejemplo del fixture `2372-03-14T10:42:11`) es el reloj autoritativo. La fecha estelar es **derivada**, tasa fija 1000 unidades/año; jamás origen de orden, TTL o causalidad.
- El perfil de era de inicio y su fecha fijan qué historia **canónica ya ocurrió**; el futuro posterior al inicio no se impone a la partida. Las anclas de 2259, 2265, 2364, 2369, 2371, etc. son referencias, **no un calendario futuro obligatorio**.
- Antes de crear una entidad: resolver continuidad/canon, fecha y lugar; reservar identificadores únicos canónicos; comprobar origen, validez temporal, tecnología y ámbito. Una fecha aproximada no debe materializarse como precisión fingida.
- `campaign_seed` es semilla de campaña, no semilla anónima para relanzar identidades; su combinación con dominio, contexto canónico y versión de generador debe definirse y versionarse **en Core** (sin prometer aquí algoritmo hash ni ABI).
- El fixture v0.0.1 usa `era_id=tng_ds9_voyager`, `campaign_date=2372-03-14`, `campaign_seed=fixture_sensor_v0_0_1`. **No presupone la presencia ni la fecha de servicio de la Clase Valhalla**, ya aprobada como clase nueva inspirada en Galaxy.

## 3. Identidad estable — propuesta de intercambio, NO API Core

| Concepto | Existencia / fuente | Invariante exigida |
|---|---|---|
| `campaign_id` / `campaign_seed` | Identidad de partida y proveniencia persistida | No se sustituye una semilla al recargar |
| `generator_id` / `generator_version` / origen | Contratos de generación existentes | Subdominios aislados; upgrades requieren migración explícita |
| `entity_id` | `persistent_entity_identity_contract.json` | Una identidad materializada no cambia tras observar, viajar o cargar |
| `character_id`, `vessel_entity_id`, `visual_identity_id` | Anclas específicas Trek / visuales | Una mejora visual, reparación o ascenso no crea otra persona/nave |
| `slot_id` de población | `persistent_population_materialization_rules.json` | C→B consume/referencia una plaza real; promoción irreversible |
| `materialization_timestamp_or_campaign_date` | Ancla inmutable del contrato de identidad | Nunca se desplaza retroactivamente por descubrimiento posterior |
| `history_ref` / eventos | Contrato de persistencia | Tras LOD, carga, refit, muerte o destrucción conserva prefijo histórico |

No equiparar `contact_id` de Sensores (relativo al observador) con `entity_id` interno. Un nombre de nave, nombre de civilización o señal tampoco es clave primaria de identidad.

## 4. Ciclo de vida y condiciones

| Estado | Existencia en mundo | Puede estar en UE5 | Operación legal | Operación prohibida |
|---|---|---|---|---|
| Contexto latente C | Sector/población ya determinada y reservada | No necesita Actor | Resolver detalle determinista por demanda | Inventar nueva plaza por interacción |
| Individuo o entidad materializada B/A | ID estable, origen, historia | Opcional | Guardar/proyectar/actualizar por evento autorizado | Regenerar identidad o devolver B→C |
| Observación parcial | Misma verdad, mayor conocimiento de observador | Consola visible si procede | Emitir proyección filtrada con incertidumbre | Cambiar verdad o revelar campo oculto |
| Descarga 3D / LOD inferior | Continúa su existencia y estado | Actor destruido | Avance causal fuera de escena | Destruir entidad, borrar agenda o historia |
| Recarga 3D / partida | Se recuperan ID y estado originales | Actor nuevo apunta al mismo ID | Resolver presentación desde identidad guardada | Tirar otra semilla o duplicar NPC |
| Inactivo, muerto, retirado o destruido | Identidad/historial siguen persistidos | No requiere Actor | Registrar transición autoritativa | Reutilizar ID para otro individuo |

**Regla antirretroactividad:** la primera observación no provoca generación de hechos físicos sobre los que observa. Puede solicitar completar detalles predeterminados o materializables desde la identidad/semilla previa, siempre preservando la coherencia con hechos ya observados. La llegada de una lanzadera se registra como cambio causal de ubicación y ocupación, nunca como decoración de hangar.

## 5. Puntos aún no homologados

1. CoreRPG `main@dcfcb83c9853e005b5450bd39e0ba693cb91e257` sigue sin 4.5 fusionada a fecha de auditoría; `feat/generic-world-state@2a3da891` no es una API de producción.
2. Falta acordar con Core cómo resolver dominios de semilla/versiones, claves de unicidad, reservas, atomicidad y migración de entidad.
3. Falta verificar con Host UE5 la vinculación `EntityId↔Actor` en descarga/recarga y enumeración de actores sin duplicados.
4. **DEC-0001 ya resuelta:** Galaxy/Enterprise-D como referencia creativa de la nueva Clase Valhalla. **No condiciona** el prototipo de Sensores ni acredita integración Core.

## 6. Casos P01 de aceptación futura

`F03-T01`: misma semilla/versión/contexto produce mismo conjunto materializado; `F03-T02`: repetir observación no crea entidad; `F03-T03`: C→B preserva cupo y jamás revierte; `F03-T04`: Actor unload/reload conserva entity_id, visual_identity y history_ref; `F03-T05`: reserva canónica impide sobrescribir la fecha. **Evidencia runtime: NO_EJECUTADO.**

La suite de referencia P05 comprueba consistencia de un escenario estático limitado; **no valida generador ni repositorio Core**. Al integrar Core se deberá convertir cada caso en prueba de ejecución con versión, SHA, resultado y fichero de log.
