# PLAN MAESTRO — Videojuego Star Trek RPG 3D

**Versión organizativa:** 1.0 / 11-10-2026. **Objetivo:** dirección secuencial del producto, sin sustituir los sistemas técnicos ni sus roadmaps. **Fase F00: cerrada (organización)**. Próxima fase global: **F01**.

## Principios de producto conservados

- RPG 3D para PC/MSI con universo persistente, NPC que actúan sin el jugador y Academia de cuatro años antes del servicio activo; la web academiaflota sigue siendo complemento educativo.
- Carrera gradual y **opcional**; alférez nuevo ≠ capitán; quedarse en cualquier destino, cambiar de nave o aspirar a la Imperator debe tener consecuencias reales.
- Tres clases candidatas para la futura Dama base (Galaxy, Sovereign, Odyssey) **todavía sin selección aprobada**; no confundir clase Imperator final con el puente piloto del vertical slice.
- Generar realidad antes de observarla. La IA remota propone y dialoga sin modificar World State por sí sola. La vida NPC persiste fuera de escena sin actores 3D cargados.
- Una fuente por responsabilidad; no crear un Core RPG paralelo en Star Trek; no duplicar temarios de la web en código de juego.

## Índice oficial de fases

| Fase | Tema | Estado global | Entrega objetivo |
|---|---|---|---|
| [F00](fases/F00/README.md) | Auditoría, inventario y gobierno | CERRADA | DOCUMENTACION_AUDITADA |
| [F01](fases/F01/README.md) | Visión y canon del producto | PLANIFICADA | DISENO_VALIDADO |
| [F02](fases/F02/README.md) | Arquitectura e integración | PLANIFICADA | CONTRATO_VALIDADO |
| [F03](fases/F03/README.md) | Mundo autoritativo y persistencia | PLANIFICADA | CORE_INTEGRADO |
| [F04](fases/F04/README.md) | Naves, dotación y autoridad | PLANIFICADA | REFERENCIA_PROBADA |
| [F05](fases/F05/README.md) | Órdenes, delegación e iniciativa NPC | PLANIFICADA | CORE_INTEGRADO |
| [F06](fases/F06/README.md) | Sensores funcionales | PLANIFICADA | REFERENCIA_PROBADA |
| [F07](fases/F07/README.md) | Pipeline 3D y puente piloto | PLANIFICADA | UE5_JUGABLE |
| [F08](fases/F08/README.md) | Primera guardia jugable v0.0.1 | PLANIFICADA | ACEPTACION_SUPERADA |
| [F09](fases/F09/README.md) | Resto de consolas | PLANIFICADA | UE5_JUGABLE |
| [F10](fases/F10/README.md) | Academia jugable | PLANIFICADA | UE5_JUGABLE |
| [F11](fases/F11/README.md) | Carrera y flota jugable | PLANIFICADA | UE5_JUGABLE |
| [F12](fases/F12/README.md) | Vida a bordo y relaciones | PLANIFICADA | CORE_INTEGRADO |
| [F13](fases/F13/README.md) | Universo dinámico | PLANIFICADA | CORE_INTEGRADO |
| [F14](fases/F14/README.md) | Recursos audiovisuales y NAP | PLANIFICADA | UE5_JUGABLE |
| [F15](fases/F15/README.md) | QA, beta y distribución | PLANIFICADA | ACEPTACION_SUPERADA |

Cada fase contiene cinco pasos `Fnn-P01`…`Fnn-P05`; **80 pasos** en total. Los de F00 ya son de organización y los restantes son trabajo **pendiente de consolidar/ejecutar hasta prueba**. Un paso puede aprovechar entregables muy avanzados sin volver a redactarlos.

## Flujo principal y dependencias

```text
F00 (auditado/cerrado)
  ↓
F01 visión y decisiones de alcance
  ↓
F02 arquitectura y contratos
  ↓
F03 mundo, persistencia → F04 dotación/autoridad → F05 órdenes/NPC
  ↓                                      ↓
F06 Sensores funcionales ←───────────────┘
  ↓
F07 puente 3D y pipeline (preparación paralela permitida)
  ↓
F08 v0.0.1 JUGABLE  ← bloqueo explícito de Core si procede
  ↓
F09 consolas → F10 Academia jugable → F11 carrera/flota
  ↓
F12 vida a bordo / F13 universo dinámico / F14 producción audiovisual
  ↓
F15 beta/distribución (QA siempre transversal)
```

Este diagrama es el **camino crítico orientativo**, no una prohibición de diseñar/probar componentes independientes antes de otra fase. Dentro de F13 rige además el orden 1→10 del plan dinámico existente; bloques 1–3 constan cerrados **a nivel de referencia**, 4 siguiente pendiente.

## Hitos de aceptación

| Hito | Resultado | No se acepta como sustituto |
|---|---|---|
| M0 — F00 | Plan y línea base comprobados en GitHub | Una lista informal de ideas |
| M1 — F01/F02 | Producto definido y contratos contrastados con Core | APIs imaginadas o elecciones tácitas de canon |
| M2 — F03/F06 | Universo/Sensores reproducibles y reglas auditadas | Solo README o fixtures sin ejecutar |
| M3 — F07/F08 | **Primer guardia de Sensores interactiva en UE5** | Capturas, PDFs o validación de JSON |
| M4 — F09–F11 | Operaciones, Academia y carrera reales | Cursos web por sí solos |
| M5 — F12–F15 | Universo persistente y beta comprobada | Cantidad de documentos sin jugabilidad |

## Gestión de cambios

- F00 manda el control global; cada fase mantiene sus enlaces a **ubicaciones existentes**. Prohibido trasladar cientos de rutas para adaptarse al plan.
- Idea `IDEA-xxxx` → decisión `DEC-xxxx` cuando haga falta → fase/paso `Fnn-Pnn` → evidencia/prueba → cierre.
- Todo `COMPLETE` previo se registra con **alcance declarado** (lore, contrato, simulador, CI o UE5), no como prueba de implementación general.
- Una única fase principal activa; no iniciar otra por casualidad. Trabajo transversal compatible, en rama, con verificación y sin adelantarse a decisiones autorales.
- Para modificaciones que cambian el canon principal, el alcance jugable o la arquitectura del Core, solicitar decisión del autor o coordinador antes de fijarlas.
