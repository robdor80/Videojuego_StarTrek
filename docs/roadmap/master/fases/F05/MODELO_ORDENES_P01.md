# F05-P01 — Semántica y propiedad del ciclo de órdenes
Fecha: 2026-10-11 · Alcance: contrato Star Trek de referencia, **no ABI de Core**.

## Seis objetos diferentes
| Objeto | Identidad | Autor | Consecuencia |
| --- | --- | --- | --- |
| **Solicitud** (request) | request_id | Actor humano/NPC/UI o IA como propuesta etiquetada | Expresa intención; no concede autoridad ni muta nada |
| **Orden** (order) | order_id | Emisor con identidad y cargo/autoridad vigente | Instrucción propuesta o validada, con destinatario, alcance y plazo |
| **Compromiso/tarea** (task) | task_id | Destinatario acepta o asignación válida según reglas | Trabajo duradero con agenda, prioridades, avance y obligación de informar |
| **Acción** (action_attempt) | attempt_id | Ejecutor realmente autorizado | Intenta una transición verificable en el estado actual |
| **Resultado** (result) | result_id | Resolvedor autoritativo | Describe efectos reales, ninguno/parte/todos, recursos y error |
| **Evento** (event) | event_id | Registro autoritativo append-only | Constancia causal visible solo mediante proyección de conocimiento |

Un mismo request puede proponer varias órdenes; una orden puede crear varias tareas; una tarea puede exigir varios intentos; un intento produce un único resultado terminal e identifica cero o más eventos. No son sinónimos ni comparten IDs. **Una respuesta verbal «Sí, capitán» no acredita ejecución**.

## Envelope de intercambio de referencia (no API publicada)
Campos mínimos propuestos: `id`, `kind`, `schema_version`, `world_id`, `issued_at`, `actor_id`, `ship_id`, `causal_refs[]`, `expected_revision`, `idempotency_key` y `visibility_scope`. Orden añade `issuer_appointment_ref`, `authority_domain`, `recipient_id`, `station_id`, `action_id`, `parameters`, `constraints`, `deadline_at` y `standing_order_ref` opcionales según tipo. Tarea añade responsable, carga de trabajo, ventana, prioridad, condición de cierre e informe. Intento contiene executor efectivo y snapshot/revisión usados para revalidación. Resultado distingue autorización, aplicación real y efecto parcial.

Se preservan, sin migración retroactiva, `gameplay/orders/starship_order_contract.json` (v0.2) y `gameplay/orders/subordinate_task_order.json`; las denominaciones `accepted`, `clarification_required`, `queued`, `executing`, `completed`, `failed`, `refused`, `cancelled` continúan válidas para órdenes. `expired` y `superseded` son extensiones **propuestas** para un contrato futuro, no valores implantados silenciosamente.

## Fronteras de ownership
- **Star Trek** determina nombramientos, cadena de mando, doctrina, puestos/estaciones, procedimientos, limitaciones médicas y Primera Directriz contextual.
- **Core RPG (cuando implemente 4.6/4.7/4.9/4.10)** autentica identidad lógica, valida transiciones y recursos, persiste el estado autoritativo y el historial causal.
- **UE5** presenta diálogo, consola y animación; no marca una acción como realizada porque se reprodujo una frase.
- **IA** puede proponer una estructura que pasará esquema, conocimiento, autoridad, capacidades y estado contemporáneo. Nunca escribe World State ni crea autorizaciones.

## Invariantes auditables
1. Una orden no equivale a acción; ninguna aceptación modifica por sí misma escudos, ruta, armamento ni recursos.
2. Emisor, destinatario, ejecutor y autor del evento pueden ser diferentes; `issuer_authority_context` no se copia como permiso al ejecutor.
3. Cada ejecución consulta permisos **vigentes** y revisión contemporánea, incluso si el emisor tenía permiso al emitir.
4. Prohibidos IDs reutilizados para nuevos objetos, doble efecto por retransmisión y reescritura de eventos históricos.
5. Reporte/sensor solo comunica información observada; ni el capitán NPC ni el jugador adquieren verdad universal por pertenecer al puente.
6. Las acciones no ejecutables/ilegales fallan con razón explícita; las lícitas pero subóptimas se pueden ejecutar y dejar consecuencias.
7. Guarda/carga debe conservar orden pendiente, delegaciones, intentos ya resueltos, idempotency_key, causalidad y revisiones; caso E2E aún sin ejecutar.

## Trazabilidad de fuentes existentes
`gameplay/orders/starship_order_pipeline.md`, `gameplay/orders/starship_order_contract.json`, `gameplay/orders/subordinate_task_order.json`, `gameplay/ship_operations/operational_event_log/operational_event_contract.json`, `gameplay/chain_of_command/command_decision_delegation_state_v0.1.json`, `ai/command_interpretation/starship_command_contract.md`.

**Puerta:** diseño y propuesta de intercambio documentados. `CONTRATO_VALIDADO` con Core no alcanzado: CoreRPG/main dcfcb83 (4.4), sin Actions 4.10.
