# F06-P03 — Memoria de nave, Ciencia y registro operacional

## Contratos conservados
- gameplay/ship_operations/ship_memory/contact_dossier_model.json
- gameplay/ship_operations/interconsole/sensor_to_science_analysis_handoff.json
- gameplay/ship_operations/interconsole/interconsole_data_package_contract.json
- gameplay/ship_operations/operational_event_log/operational_event_contract.json
- gameplay/ship_operations/operational_event_log/event_type_catalog.json

## Dossier de contacto
run_reference_scan devuelve, para cada detección, contact_id, observation_id, source_system=sensors, hora, confianza, datos **realmente observados** y procedencia. Las propuestas known_facts_candidates no son hechos ya reconciliados: Core deberá cotejar evidencia, conservar contradicciones, decidir reidentificación y prevenir duplicados. **No se escriben dossiers persistentes**.

## Transferencia Sensores → Ciencia
science_handoff_candidate acepta exclusivamente IDs de observaciones ya presentes en el dossier suministrado. Rechaza observaciones ajenas, repetidas, contacto distinto y metadatos esenciales ausentes. Entrega paquete en estado queued con los datos, confianza y procedencia. No concede acceso universal ni interpreta científicamente. Ciencia responderá, si Core lo permite, con una **nueva** observación propia, sin reescribir el sensor original.

## Cadena de eventos
Cuando hay orden referenciada: ORDER_ACKNOWLEDGED → ACTION_STARTED → ACTION_EXECUTED → RESULT_CREATED → REPORT_MADE → ACTION_COMPLETED. El evento original ORDER_ISSUED corresponde a F05/Core. Sin orden previa hay secuencia de acción propia, siempre sujeta a autorización externa.

Todos los eventos generados son **candidatos**, tienen identidad reproducible, sujeto/actor, referencia causal y política de proyección pendiente. Jamás enviar DATA_SENT si el envío no ocurrió ni RESULT_SAVED si no hubo commit. El registro no concede conocimiento a todos los NPC por existir.

## Límite comprobable
No hay almacenamiento, transmisión, save/load, entrega real a Ciencia, reloj autoritativo ni eventos realmente añadidos al log. **effects_applied=0; authoritative=false**. Los futuros adaptadores deben verificar idempotencia del commit y proyección por destinatario.

**P03:** contrato conciliado y lógica referencial, no integración Core.
