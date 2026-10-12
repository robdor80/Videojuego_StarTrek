# PLAN MAESTRO — Videojuego Star Trek RPG 3D

**Versión organizativa:** 1.0 / 11-10-2026; **reconciliación post-merge:** 13-10-2026. **Objetivo:** dirección secuencial del producto, sin sustituir los sistemas técnicos ni sus roadmaps. **F00 y F01 cerradas a su nivel documental**; fase principal activa: **F02 EN_CURSO**, con puerta de integración Core/Host pendiente. [Acta de reconciliación](ACTA_RECONCILIACION_F00_F06_2026-10-13.md).

## Principios de producto conservados

- RPG 3D para PC/MSI con universo persistente, NPC que actúan sin el jugador y Academia de cuatro años antes del servicio activo; la web academiaflota sigue siendo complemento educativo.
- Carrera gradual y **opcional**; alférez nuevo ≠ capitán; quedarse en cualquier destino, cambiar de nave o aspirar al mando de una nave de **Clase Valhalla** debe tener consecuencias reales.
- **DEC-0001 resuelta:** Galaxy/Enterprise-D como inspiración de la **nueva Clase Valhalla** (no un refit ni la Enterprise-D renombrada); exterior reconocible pero modernizado. Sovereign y Odyssey se conservan como otras Damas potencialmente NPC; no confundir nave final con **puente piloto** de la v0.0.1. **No hay año de servicio Valhalla fijado.**
- Generar realidad antes de observarla. La IA remota propone y dialoga sin modificar World State por sí sola. La vida NPC persiste fuera de escena sin actores 3D cargados.
- Una fuente por responsabilidad; no crear un Core RPG paralelo en Star Trek; no duplicar temarios de la web en código de juego.

- **v0.0.x son prototipos internos de validación, no lanzamientos ni contenido necesariamente integrado en el juego 1.0**. v0.0.1 se limita a la guardia de Sensores; futuras pruebas parciales de Academia son posibles. La numeración de ensayos es independiente de las fases del plan; véase `docs/decisions/prototype_validation_and_release_policy.md`.

## Índice oficial de fases

| Fase | Tema | Estado global | Entrega objetivo |
|---|---|---|---|
| [F00](fases/F00/README.md) | Auditoría, inventario y gobierno | CERRADA | DOCUMENTACION_AUDITADA |
| [F01](fases/F01/README.md) | Visión y canon del producto | **CERRADA en diseño** (PR #2, acta F01) | DISENO_VALIDADO |
| [F02](fases/F02/README.md) | Arquitectura e integración | **EN_CURSO** (inventario/QA documental completados; Core/Host pendiente) | CONTRATO_VALIDADO |
| [F03](fases/F03/README.md) | Mundo autoritativo y persistencia | **EN_REVISION** (referencia probada; Core bloqueado) | CORE_INTEGRADO |
| [F04](fases/F04/README.md) | Naves, dotación y autoridad | **EN_REVISION** (referencia probada; validación de integración pendiente) | REFERENCIA_PROBADA |
| [F05](fases/F05/README.md) | Órdenes, delegación e iniciativa NPC | **EN_REVISION** (referencia probada; Core pendiente) | CORE_INTEGRADO |
| [F06](fases/F06/README.md) | Sensores funcionales | **EN_REVISION** (referencia probada; PDF/UE5/Core pendientes) | REFERENCIA_PROBADA |
| [F07](fases/F07/README.md) | Pipeline 3D y puente piloto | PLANIFICADA | UE5_JUGABLE |
| [F08](fases/F08/README.md) | Primera guardia jugable v0.0.1 | PLANIFICADA | ACEPTACION_SUPERADA |
| [F09](fases/F09/README.md) | Resto de consolas | PLANIFICADA | UE5_JUGABLE |
| [F10](fases/F10/README.md) | Academia jugable | PLANIFICADA | UE5_JUGABLE |
| [F11](fases/F11/README.md) | Carrera y flota jugable | PLANIFICADA | UE5_JUGABLE |
| [F12](fases/F12/README.md) | Vida a bordo y relaciones | PLANIFICADA | CORE_INTEGRADO |
| [F13](fases/F13/README.md) | Universo dinámico | PLANIFICADA | CORE_INTEGRADO |
| [F14](fases/F14/README.md) | Recursos audiovisuales y NAP | PLANIFICADA | UE5_JUGABLE |
| [F15](fases/F15/README.md) | QA, beta y distribución | PLANIFICADA | ACEPTACION_SUPERADA |

Cada fase contiene cinco pasos `Fnn-P01`…`Fnn-P05`; **80 pasos** en total. Los de **F00 y F01 están cerrados únicamente a su madurez documental**. Los entregables de F02–F06 ya están incorporados (PR #3–#7) y sus avances no vuelven a calificarse como no iniciados; las puertas **Core/Host/UE5** y la inspección del PDF de Sensores continúan donde corresponde. Un paso cerrado a nivel referencia **no** equivale a su integración ejecutable.

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

**Fotografía del control 13-10-2026:** las PR #2–#7 están fusionadas en `main`; sus pruebas y entregables de referencia son reales, pero **M1–M3 siguen sujetos a las evidencias definidas**, y no se certifica aún un corte Core↔UE5. Véase el [registro post-merge](ACTA_RECONCILIACION_F00_F06_2026-10-13.md).

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
- Una única fase principal activa en el estado global (**F02**). F03–F06 constan **EN_REVISION** por haberse trabajado preparatoriamente, sin convertirse en una segunda fase principal activa. F07/F08 continúan formalmente planificadas/pausadas hasta autorización y evidencias de integración, aunque los activos de Blender/UE5 puedan seguir preparándose de forma independiente.
- Para modificaciones que cambian la continuidad del juego, el alcance jugable o la arquitectura del Core, respetar las decisiones creativas expresamente aprobadas por el autor. **La cronología de pantalla puede alterarse para este juego personal**, con anotación GAME_ADDITION, sin habilitar por defecto tecnologías futuras en todas las eras.
- **Acta vigente de la nueva Clase Valhalla:** [ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md](fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md). Blindaje ablativo y torpedos transfásicos aprobados como diseño; Blender/UE5 y Core pendientes de implementar y validar.
