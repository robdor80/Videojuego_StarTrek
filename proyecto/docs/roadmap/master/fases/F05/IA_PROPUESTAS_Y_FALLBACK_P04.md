# F05-P04 — IA remota: propuesta, contexto, caducidad y fallback
Fecha: 2026-10-11 · Contrato de integración **propuesto**, no endpoint Core vigente.

## Frontera irreversible
**LLM = diálogo/intención/explicación/propuesta. Host/Star Trek = reglas de dominio. Core = validación/efecto.** Ningún modelo ni proveedor escribe entidades, cambia rangos, inventa conocimiento, crea órdenes válidas o confirma resultados por texto. El proveedor no recibe secretos de mundo, fichas ajenas ni capturas del estado autoritativo completo.

## Envelope mínimo de propuesta (interno, no API pública)
`proposal_id, originating_actor_id, request_id, observer_projection_ref, context_revision, issued_at, action_candidates[], needs_clarification, explanation, provider_trace_id`. La propuesta referencia un **contexto ya filtrado** y no incluye credenciales ni verdad oculta. La respuesta del proveedor es **datos no confiables**: schema/enum/IDs válidos, escape de instrucciones incrustadas y respeto de dominios. La descripción narrativa jamás se usa como fuente de hechos nuevos.

## Validación posterior obligatoria
1. Respuesta asociada a petición activa y a actor correcto; respuesta tardía/desordenada fuera de ventana → `stale_context` y descarte seguro.
2. Revalidar proyección y revisión; si ha cambiado el mundo, se reconstruye el contexto autorizado; no reutilizar permisos expirados.
3. Revalidar emisor, cargo, fin de guardia, reglas médicas, delegación/standing order, objetivo, recursos y disponibilidad.
4. Ante ambigüedad pedir aclaración o usar procedimiento determinista **ya autorizado**. No rellenar parámetros críticos por azar.
5. Solo motor autoritativo puede aceptar intención como acción, producir resultado y confirmar éxito al jugador.

## Degradación por fallos
| Incidencia | Conducta segura |
| --- | --- |
| Sin red, timeout, cuota o 5xx | `deterministic_fallback`: catálogo de intenciones conocidas, plantillas de reporte y decisiones rutinarias aprobadas; diálogo menos natural |
| Modelo devuelve JSON corrupto/hallucinado | Rechazar propuesta, pedir aclaración o fallback; no ejecutar interpretación parcial insegura |
| Respuesta tras revocación/traspaso/fin de guardia | Descartar `stale_context`, dejar evento técnico sin efecto |
| Falta conocimiento observable del contacto | `insufficient_knowledge`: solicitar barrido/reporte, no revelar contacto oculto |
| Orden peligrosa o recurso escaso | Evaluación reglas actual; negativa/ruta de revisión, sin convertir «optimización IA» en prohibición nueva |
| Orden lícita pero subóptima del capitán | Permitir, registrar consejo y consecuencias; la IA no toma el mando |
| La IA no está disponible durante una simulación offscreen | El tick operativo determinista continúa con datos y agenda válidos; ninguna transición espera a la red |

Se usan rutas existentes `DETERMINISTIC`, `COMPUTER_FAST`, `COMPUTER_REASONING` en `sistemas/gameplay/ship_operations/ship_computer/ai_routing_policy.json`; **no** codificar nombres Gemini/OpenAI como reglas del juego ni obligar a red para funciones básicas.

## Privacidad y observabilidad
Auditoría restringida: ID de solicitud/propuesta, actor, versión de esquema, ID/context_revision, categoría de respuesta, resultado de validación, tiempos y eventos causales. El texto libre/prompt bruto solo con retención mínima y permisos explícitos; nunca logs globales accesibles por todos los NPC. `visibility_projection_rules.json` manda sobre la presentación. No presentar «El capitán ha ordenado» si el sistema solo creó una sugerencia LLM.

## Testabilidad
Matriz P05 incluye proveedor caído, propuesta sin permiso, contexto obsoleto y desconocimiento de un objetivo; deben **no causar mutación**. Contrato/Core API para 4.12 pendiente; integración UE5 y proveedor real NO_EJECUTADA. Fuentes: `sistemas/ai/command_interpretation/starship_command_contract.md`, `sistemas/gameplay/ship_operations/ship_computer/ai_routing_policy.json`, `sistemas/ai/npc_behavior/character_decision_guardrails.md` y `proyecto/docs/roadmap/master/DEPENDENCIAS_CORE_RPG.md`.
