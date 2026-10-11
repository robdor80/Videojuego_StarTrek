# F05-P02 — Ciclos de aceptación, rechazo y delegación
Fecha: 2026-10-11 · Nivel: diseño de referencia verificable; Core pendiente.

## Estados operativos
Una **orden** puede pasar de `issued` a `clarification_required`, `accepted`, `queued`, `executing`; los terminales son `completed`, `failed`, `refused`, `cancelled`. `expired` y `superseded` se tratarán como **razones/eventos**, no nuevos valores persistidos de `starship_order_contract.json` hasta aprobar migración. `task` tiene su propio estado `issued/acknowledged/clarification_required/in_progress/completed/failed/refused/cancelled/superseded`. No forzar un estado único para todo.

| Paso | Condición | Efecto |
| --- | --- | --- |
| Emisión `issued` | Intención estructurada; actor y ámbito identificables | Intento de validación, sin ejecutar |
| `clarification_required` | Ambigüedad/material insuficiente | Solicitar precisión sin inventar campos ni ocupar recursos irreversibles |
| `accepted` | Autoridad válida, destinatario competente, contexto suficiente | Aceptación y posibilidad de tarea; no presupone resultado |
| `queued` | Trabajo válido aplazado, plazo, capacidad disponible prospectivamente | Reserva solo si el motor la valida; sin suponer ocupación instantánea |
| `executing` | Guardia, nombramiento, aptitud, delegación, recursos y revision **revalidados** | Crear intento idempotente y operar por motor autoritativo |
| `completed` | Resultado comprobado | Registrar evidencia, liberar reservas, feedback contextual |
| `failed` | Falló un intento, recurso o condición de entorno | Registrar resultado real, posible nueva tarea, nunca éxito ficticio |
| `refused` | Ilegalidad, imposibilidad, falta de autoridad o desacato deliberado | Diferenciar `reason_code` y consecuencias; no mutación solicitada |
| `cancelled` | Revocación/caducidad anterior a efecto o sustitución | Registrar causa, liberar pendientes; historial intacto |

**Desobediencia:** `refused` con `reason_code=deliberate_noncompliance` y evento de disciplina/relación, nunca una omisión invisible. **Orden indebida:** `refused` con motivo `legal_constraint` o revisión contextual; Primera Directriz no es un bloqueo duro universal.

## Delegación, revisión, caducidad
Se conserva el contrato `gameplay/chain_of_command/command_decision_delegation_state_v0.1.json`: `draft → active → suspended/revoked/expired` (sin reactivación implícita); `manual`, `proposal_requires_approval` y `delegated_autonomous` son modos distintos. Deben vincularse `delegation_id`, autoridad de origen, receptor, dominio, ship_id, límites/acciones permitidas, rango de vigencia, origen y revisión. `active` solo tiene poder **dentro** de sus límites y si el delegante sigue habilitado. `proposal_requires_approval` jamás ejecuta cambios de política sin aprobación efectiva; `manual` tampoco. Revocar el mandato **no borra** decisiones válidas ya aplicadas: bloquea futuros intentos y crea tareas de compensación si procede. La subdelegación no amplía ámbitos ni duración.

La revocación debe **invalidar nuevas autorizaciones de ejecución**, incluso si la tarea se recibió antes; las acciones ya confirmadas requieren su propia orden correctora. Caducidad por tiempo o fin de guardia opera igual. No convertir suceso extraordinario (médico, ascenso, relevo) en cesión universal de autoridad.

## Competencia y carreras de ejecución
- Evaluar autoridad en `issued`, al aceptar y **al ejecutar**; ante conflicto versión/revisión devolver `stale_context` sin efectos y volver a planificar.
- Identidad lógica estable; logs de auditoría distinguen resultado de tarea, orden, acción y evento.
- `idempotency_key` por solicitud/intent, scope de campaña: mismo identificador + mismo payload devuelve mismo resultado; payload incompatible → rechazo `idempotency_conflict`.
- Si se revoca después de un efecto confirmado, no retroceder ese efecto por borrar la orden.
- Reportes y decisiones se proyectan por conocimiento y cargo; la IA no puede acceder a notas privadas ajenas ni a objetivos aún no detectados.

## Dos casos mínimos
**Alférez Sensores:** capitán NPC ordena barrido de contacto *conocido* → alférez acepta → consola comprueba guardia, cualificación, recursos y contacto → intento y resultado → informe; ante objetivo ambiguo se pregunta, no se inventa.

**Capitán jugador:** XO propone rotación → modo `proposal_requires_approval` → sin aprobación no cambia ningún turno → capitán acepta/modifica/delega dentro del ámbito → se revalida → se ejecuta; caducidad/revocación corta trabajos futuros, sin deshacer historial legítimo.

**Sin evidencia Core de 4.10+** no afirmar exclusión concurrente, persistencia ni evento real emitido por motor; serán tests E2E futuros.
