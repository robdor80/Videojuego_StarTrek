# S18 — Hoja de ruta de identidad y accesos

**Sistema numerado 18, aprobado en propósito el 18-11-2026. Diseño detallado propuesto, ejecución pendiente.**

## Enfoque de trabajo

No añadir una segunda fuente de identidad, ni un servidor independiente por puerta, ni un modelo IA por solicitud. Las identidades de `PERSON` y sus asignaciones ya las gobiernan CoreRPG y la cadena de mando. S18 comparte esas fuentes y devuelve una decisión.

| Fase | Responsable | Entrega verificable |
|---|---|---|
| **S18-I01 — Inventario y recuperación de Sutherland** | ChatGPT + Codex al recuperar el MSI | Encontrar componentes UE5/Blueprints reales, prueba de Quinn, detección NPC y estado de las 50/50 y 44/44 pruebas reportadas; no inventar ruta ni nombres de assets |
| **S18-I02 — Motor de política y autenticación** | Codex (CoreRPG/HOST) | Resolver actor verificable, pertenencia a habitación y política; permitir/denegar/timbre/verificación adicional; no depender de OpenAI |
| **S18-I03 — Puertas S12** | Codex + revisión ChatGPT | Automáticas por proximidad vs pulsadores de camarote; un componente de autorización para todas las puertas sin per-door hardcode |
| **S18-I04 — Residentes, invitados y revocaciones** | Codex + pruebas | Permisos temporales, residentes, cambio de camarote, personal de servicio legítimo, privacidad y persistencia |
| **S18-I05 — Excepciones, ordenador y seguridad** | Codex + ChatGPT contratos | Emergencia genuina, rescate, evacuación, incidencias, voz como intención no como credencial, control por LCARS/PADD |
| **S18-I06 — Certificación MSI** | Codex + ChatGPT/autor | NPC/jugador, save/load, puertas distintas, spoofing, caducidad, alertas, latencia y colisiones en UE5 |

## Mínimo viable sugerido

Usar **dos puertas** y tres personajes (jugador residente, NPC invitado sin permiso, NPC residente) como vertical slice: una puerta pública automática y una puerta privada con pulsador. Confirmar que la pública abre con detección y la privada decide correctamente para cada NPC/jugador, que el timbre aparece y la salida funciona. Después introducir permiso temporal, revocación y dos cubiertas.

**No mezclarse con S12:** ese sistema construye su geolocalización, guía de NPC y turboascensores a la **parada real más cercana**. S18 solo aporta identidad y autorización a puertas y zonas. Los ascensores no necesitan reconocimiento biométrico del jugador para interpretar «a mi camarote», pero los pisos/paradas o zonas restringidas respetarán la autorización que corresponda.

## Criterio de cierre

Pruebas de contrato verificadas, integración Core/HOST real, puertas Sutherland/Valhalla físicas en UE5, identidad NPC y jugador sin suplantación, permisos temporales/revocación, excepciones de emergencia, guardado y mediciones en MSI. **Diseño o pruebas documentales nunca equivalen a código UE5 implementado.**
