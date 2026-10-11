# Dependencias y fronteras con Core RPG (auditoría F00)

**Fecha:** 11-10-2026. Referencia: informe de coordinación `Star_Trek_RPG_Coordinacion_CoreRPG_4_10_Iniciativa_Ordenes_Delegacion.md`, remitido por la conversación de Core RPG, y contratos ya presentes en Star Trek.

## Autoridad de los subsistemas

| Capa | Responsable | Se le permite | No se le permite |
|---|---|---|---|
| Core RPG | Motor universal compartido | World State, IDs/tiempo, validación base, acciones genéricas, eventos, persistencia, simulación, límites de conocimiento genéricos **cuando existan** | Rangos de la Flota, Primera Directriz, LCARS, mando Trek específico |
| Videojuego_StarTrek | Universo/reglas de juego | Procedimientos, puestos, cadena de mando, órdenes de nave, consola/acción Trek, normativas, datos y fixtures | Duplicar runtime autoritativo genérico o escribir directamente el estado desde texto de IA |
| UE5 | Juego 3D | Escenas, cámaras, actor cargado, interacción de consola, sonido, VFX e input | Ser fuente independiente de verdad persistente si la comparte Core |
| IA remota | Servicio propositivo/dialogante | Análisis, interpretación, respuesta narrativa con contexto visible al personaje | Ejecutar mutaciones directas, inventar permisos o hacer al NPC omnisciente |

## Dependencia por ventana de Core RPG

| Fase Core | Necesidad desde Star Trek | Estado de compromiso contrastado en informe | Fases del juego |
|---|---|---|---|
| **4.5 Generic World State** | Identidad, entidades/estado autoritativo y observación | Esperada según roadmap; F00 no verifica ejecutable desplegado | F02, F03, F06, F08 |
| **4.6 Rules** | Reglas/validación compartida extensible con normativa Star Trek | Diseñar sin asumir API final | F02–F06 |
| **4.7 Persistence** | Guardado/carga de hechos, órdenes, NPC, delegaciones y memoria | Requiere integración posterior comprobada | F03–F05, F08, F10–F13 |
| **4.9 Knowledge** | Visibilidad/percepción, información por actor y conocimiento derivado | Mantener límites actor-relativos | F03, F05, F06, F12–F13 |
| **4.10 Actions + Simulation** | Acciones estructuradas genéricas/validación/resultados/eventos; **evaluar** tareas/autoridad/delegación mínima reutilizable | **Luz verde arquitectónica, no promesa de UniversalCommandSystem ni cobertura completa** | F04–F06, F08–F09 |
| **4.12 Context Builder + AI** | Contexto autorizable para propuestas IA y revalidación a recepción | Integración progresiva cuando exista | F05, F09, F12–F13 |

**No se valida aquí el estado exacto de Core RPG actual:** F00 auditó `Videojuego_StarTrek` y el informe recibido, no el repositorio del Core. En **F02-P01** se deberá leer su `main` real y registrar SHA, versión, pruebas y contratos expuestos antes de implementar una adaptación.

## Necesidades funcionales hacia Core (NO APIs aprobadas)

1. Acción/resultado universal con actor, entidad objetivo, tiempo, precondiciones y mutaciones autorizadas.
2. Eventos persistentes causalmente enlazados; proyección de conocimiento sin filtrado de verdad oculta.
3. Agenda/tarea/ocupación consistente incluso fuera de escena; no dos actividades incompatibles simultáneas.
4. Autoridad contextual/delegación **como mecanismo común solo si se demuestra reutilizable**; la cadena específica es Star Trek.
5. Compromisos duraderos, revocación/caducidad y guardado/carga sin pérdida de historial.
6. Asesoramiento IA desacoplado de la ejecución, siempre revalidado al recibirse la respuesta.
7. Consulta de estado/diagnóstico de capacidad para fallar de forma segura y permitir UI/escena.

## Ejemplo guía y pruebas a llevar a F05/F08

Jugador **alférez de Sensores** en la USS Voyager: contacto existente → Sensor detecta solo lo observable → reporte válido al capitán NPC → capitán decide barrido sin pedir permiso al jugador → orden con autoridad y datos adecuados → jugador actúa desde consola → acción produce resultado, informe y eventos → se conserva tras carga/descarga; otros tripulantes siguen actuando fuera de foco.

Pruebas de aceptación adicionales: NPC→NPC; NPC→jugador; jugador como capitán→NPC; delegación/revocación; mando temporal; recursos insuficientes; desobediencia de orden válida; orden indebida con consecuencias; API remota caída/lenta; cambios de contexto entre propuesta y ejecución; privacidad/conocimiento.

## Prohibiciones de implementación prematura

- No declarar `UniversalCommandSystem` existente o aprobado.
- No crear contratos públicos definitivos en Star Trek que la arquitectura de Core no haya aceptado.
- No incluirlo retroactivamente en Core 4.5.
- No convertir una propuesta de IA en cambio directo de World State.
- No trasladar reglamentos de Starfleet a un motor supuestamente universal.
- No marcar `CORE_INTEGRADO` sin PR, SHA, versión y pruebas contra Core real.
