# F04-P04 — Autoridad médica, órdenes externas, Primera Directriz y límites (11-10-2026)

**Fuentes:** `lore/federation/starfleet/regulations/medical_authority.json`, `medical_command_authority.md`, `prime_directive/prime_directive.json`, `gameplay/first_contact/prime_directive_operational_protocol_v0.1.json`, `gameplay/chain_of_command/captain_operational_decision_authority_contract_v0.1.json`, `gameplay/orders/starfleet_mission_tasking_order.json`.

## Precedencia por ámbito, no jerarquía plana de rango

| Restricción | Ejemplo | Resultado |
|---|---|---|
| Seguridad **no anulable** y física | Orden activar un arma inexistente / pasar un límite inviolable | Denegar ejecución; explicar incapacidad concreta |
| Cualificación/aptitud | Capitán no es médico; alférez no cualificado para cierto sistema | No elevar competencia por rango; posibilidad de reasignación lícita |
| Médico jefe en **aptitud para el servicio** | Médico certifica incapacidad del CO y documenta | Apartamiento **solo** de ese ámbito; activar sucesión normal, no transferir mando al médico |
| Orden válida de escalón superior | Cambio de objetivo de misión | Limita discreción; conflicto/desobediencia se tramita expresamente |
| Primera Directriz | Intervención cultural o primer contacto no autorizado | Advertir, exigir revisión/contexto, evaluar consecuencia: **no** es bloqueo duro universal (`not_a_hard_action_block: true`) |
| Decisión del capitán dentro de límites | Cuatro guardias con recursos suficientes | Ejecutar opción legal aunque no sea la recomendación del motor |
| Autonomía personal | Relaciones/consentimiento de un NPC | Mando nunca autoriza coacción o alteración de consentimiento |

## Puertas especializadas

- **Médico:** el profesional cualificado tiene juicio y registro (quién, a quién, instante, razón, estado de aptitud y revisión). Solo remueve del servicio; la cadena establece al mando legal siguiente. No aceptar que un operador sin autoridad médica expulse al capitán.
- **Primer contacto:** separar civilización observada, estado de capacidad, preparación cultural, autorización y misión; "posee warp" no da permiso automático de contacto. Debe existir evaluación de interferencia y respuesta a contaminación accidental. No inventar especies por un informe de sensores: F13/F03 gestionan persistencia.
- **Órdenes externas:** guardar validez, ámbito, jerarquía, vigencia y referencias; no permitir que una orden anulada conserve autorización. La oposición del jugador **puede** ser jugable con consecuencias, nunca un override silencioso de la ley.
- **Técnico:** guardas de acceso y bloqueo *overrideable* solo si el contrato del subsistema así lo define. Orden de sistema sin energía, personal o permiso → fallo seguro.
- **IA:** mostrar consejo e incertidumbre; cada aprobación mutadora exige revalidación en Core con estado contemporáneo.

## Alcance deliberado

F04 consolida matriz de autorización operativa Star Trek y la **prueba de referencia** de P05; no implementa el flujo completo de órdenes de F05, ni simula leyes complejas, ni acredita una decisión médica viva en Core/UE5. Cualquier conflicto canon importante nuevo se eleva al autor.
