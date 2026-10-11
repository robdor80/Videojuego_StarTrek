# F04-P02 — Guardias, agendas, aptitud y exclusividad temporal (11-10-2026)

**Fuentes:** `gameplay/duty_system/shipboard_watch_generation_contract_v0.1.json` (`116c0257`); `duty_assignment_model.json` (`3642349c`); `duty_watch_state.json` (`67b19e1c`); `watch_handoff_model.json` (`ec5cdb69`); `gameplay/characters/activity_schedule_model.json` (`ab999713`); `gameplay/ship_operations/off_watch_obligation_model_v0.1.json`.

## Resolución autoritativa (contrato de juego; interfaz Core pendiente)

- Los intervalos son **[inicio, fin)**, en un reloj único de campaña; zonas/horarios de a bordo se muestran por separado. Dos intervalos adyacentes no colisionan; dos tareas que solapan requieren compatibilidad declarada, no deducida de que el jugador esté lejos.
- Reserva de puesto solo por persona asignada + válida en el instante + servicio activo + habilitación médica/técnica. Guardia programada no fuerza teleportación ni presencia; la llegada, desplazamiento y relevo consumen tiempo.
- Distinguir **puesto permanente**, **tarea temporal**, **rol de oficial de guardia**, **actividad extralaboral**, **disponibilidad localizada** y **ubicación física**. Pueden coexistir solo si son compatibles; **estar localizado no equivale a ocupar la consola**.
- Guardias de Flota: Alpha/Beta/Gamma (3×8 h), o también Delta (4×6 h) como patrón configurable **por nave**. Nunca imponer horarios/terminología de Flota a naves alienígenas.
- La disponibilidad viene del estado real: enfermedad, sanción/suspensión, destino, baja, descanso protegido, órdenes, formación, trayecto y alerta. Una cualificación histórica no equivale a habilitación en vigor.
- Ausencia/avería/vacante: resolver sustitución de personas reales cualificadas y disponibles. Si falla, informar `unfilled_watch_slot` y consecuencias de disponibilidad, sin inventar tripulantes ni duplicar NPC.
- En alerta, una retirada de descanso exige una **preempción explícita** con causa, prioridad, evento y deuda de fatiga; no borrar compromisos anteriores silenciosamente.
- Relevo de guardia: transferir misión, contactos **conocidos**, limitaciones, comunicaciones, peligros y trabajos pendientes. No incluir verdad oculta del universo.

## Matriz temporal

| Caso | Resolución |
|---|---|
| Sensores 08:00–12:00 / descanso 11:30–13:00 | Rechazar solapamiento no preemptado |
| Sensores 08:00–12:00 / ingeniería 12:00–16:00 | Horarios compatibles; comprobar desplazamiento antes de confirmar |
| Guardia 08:00–12:00 + localizado 09:00–10:00 | Potencialmente compatible **solo** si localidad/política lo permite; no ocupa 2 consolas |
| Guardia y licencia médica activa | `unable_to_report`; plaza sin cubrir hasta relevo |
| Alerta roja y descanso protegido | Solo interrumpir con evento explícito y deuda fisiológica |
| Saliente conoce contacto, entrante no | Informe tras relevo, no filtración retrospectiva |
| Guardado/carga durante guardia | Misma asignación, persona y tareas pendientes, sin nueva tirada |

**Propiedad:** Core resuelve intervalos y persistencia; Star Trek aporta cualificación/turnos/roles; UE5 representa presencia, no la inventa; IA aconseja sin reasignar. **No aprobada API Core**. Pruebas de referencia P05 ejecutan la exclusividad; continuidad real queda F03/Core.
