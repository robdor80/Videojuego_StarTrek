# R3/R4/R6/R7 — Correcciones de integración y criterios de aceptación
**19-11-2026 · Planificación 1 · Corrección de diseño y gobierno, sin desarrollar fases**

Este documento **no abre** F07/F08/F09/F12/F13/F14/F15 ni acredita un test de juego. Se redacta para evitar que, al retomarlas, se construyan componentes paralelos o se confundan prototipos con aceptación real.

## A. Única cadena de autoridad por operación

| Eslabón | Pregunta que debe responder | Propietario |
|---|---|---|
| 1. Intención de jugador/NPC | ¿Qué acción pide y desde qué consola/puesto? | UX Unreal / NPC, sin mutación |
| 2. Principal | ¿Quién la solicita, cómo se autentica y en qué sesión/partida? | HOST |
| 3. Reglas de Star Trek | ¿Puede hacerlo con su rango, destino, contexto y capacidad de nave? | F04/F05/F06/F09/F10/F11/F13 según dominio |
| 4. Realidad y causalidad | ¿Qué hechos existen, en qué revisión y tiempo, qué cambia y qué recibo se emite? | CoreRPG / componentes de dominio autorizados |
| 5. Observabilidad | ¿Qué puede conocer este observador sin omnisciencia ni información de otra partida? | Core Knowledge + filtros de dominio; HOST proyecta sin ampliar |
| 6. Representación | ¿Qué estado confirmado aparece en LCARS, voz, HUD y NPC? | UE5 / interfaz, sin segunda verdad |
| 7. Continuidad | ¿Qué queda en journal/save, cómo se reanuda en otro proceso y qué ocurre fuera de escena? | CoreRPG + consumidores de proyección |
| 8. Degradación | ¿Qué sucede si IA/TTS/red/arte falla? | HOST para servicios, reglas deterministas nunca dependen de ellos |

**Regla:** ningún comando procedente de HTML, voz o LLM puede mutar WorldState o asignar rangos por un acceso lateral. Los sistemas S01–S19 son contratos de necesidades; **no un segundo motor**. Planificación 2 B01–B10 aporta referencias; F13 no las ejecuta automáticamente.

## B. F07/F08 — separar laboratorio, escena y campaña

- **F07:** piloto técnico vigente **USS Sutherland** con fixture de 2372; conservarlo para diagnóstico y regresiones. #95 es UI LCARS HTML/JS Draft, no interfaz de Unreal certificada. El asiento F07-SEAT-01 sigue no aprobado. Exigir glTF/GLB fuente y derivado con procedencia/hashes, materiales PBR, escala, colisión, puntos de interacción, mapa UE5, build MSI, prueba visual y perfilado.
- **F08:** escenario de **guardia v0.0.1** por ejecutar, no una fase completada por tener plantilla ni arnés. El [proyecto Unreal principal](../../../../juego/UE5/StarTrekRPG/README.md) ya existe como **diagnóstico HOST**, no como puente completo; nunca afirmar que falta todo `.uproject` ni que el diagnóstico es juego integrado.
- **Campaña futura:** 2383–2387 protagonista fijo y Enterprise-D en reconstrucción con sucesos emergentes; no copiar el fixture 2372 ni declarar 2387 como hecho garantizado del WorldState.

**Operación mínima E2E para una futura aceptación F08**: orden verdadera de capitán NPC → recibo, actor y puesto válidos → barrido sobre verdad espacial → contacto según conocimiento observable → transferencia científica confirmada → respuesta/decisión persistida en Core → consola UE5 refleja ese hecho → SAVE → cerrar proceso → LOAD → mismo resultado sin repetición. Fallback IA/TTS sin bloqueo.

**Negativas obligatorias:** principal anónimo, orden caducada, contacto perdido, información clasificada, retry doble, partida ajena o guardado manipulado, IA caída, fallo de TTS, enlace HOST interrumpido, cambio de turno en curso y carga desde proceso nuevo. El arnés Python solo comprueba consistencia de metadatos y nunca otorga `UE5_JUGABLE`.

## C. F09/F12/F13/F14 — deuda futura acotada

| Fase | Corrección de dirección de esta auditoría | No equivale a |
|---|---|---|
| **F09** | Consolas son consumidores de acciones confirmadas, con rol/permiso y transferencia interconsola verificables. Seleccionar mínimo para guardia antes de catalogar todas las estaciones. | Consolas jugables por disponer de fichas |
| **F12** | Agendas, ausencias, turnos, sustituciones, relaciones y memoria social se conectan al mismo tiempo/identidades F04/F11; se prueba un NPC sin duplicarlo en transición. | Vida NPC integrada por test Python |
| **F13** | P2 B01–B10 = **REFERENCE_COMPLETE**, con causalidad, scheduler, límites offscreen y LOD pendientes de implementación en Core/HOST. No abrir ni repetir la auditoría de P2. | Simulador galáctico runtime |
| **F14** | Activo clasificado **READY / PLACEHOLDER / BLOCKED** con ID, licencia/procedencia interna, versión, SHA de origen y derivado, escala/UV/PBR/LOD, colisión, animación, import UE5, VRAM y escena de prueba; solo READY con evidencia puede figurar en una aceptación. | Material listo para jugar por existir GLB, biblioteca NAP o mockup |

No bloquear el corte piloto por contenido ornamental, toda la galaxia, NPC legendarios sin modelo o totalidad de S01–S19. Todo aplazamiento requiere dueño y motivo; no quitar la necesidad del backlog ni confundir omisión autorizada con éxito técnico.

## D. Presupuesto MSI y aceptación sin métricas inventadas

**Equipo objetivo existente:** MSI i9-14900HX, RTX 4070 Laptop **8 GB VRAM**, 32 GB RAM, Unreal 5.8.2. Ninguna prueba NullRHI, C++ nativa o LCARS web acredita FPS del juego. Para cada futuro gate real registrar hardware, driver, calidad gráfica, pantalla/resolución, versión UE, SHA commit/build/asset, sesión, escena, modo RHI y capturas/logs originales.

Medir explícitamente **frametime/FPS medio/1% low, pico VRAM, RAM, CPU, latencia de IA, tiempo de guardado/carga, crecimiento tras sesión larga**, además de NPC/LOD, cambio de cubierta y pérdida de red. Umbrales numéricos **pendientes de presupuesto y medición**: no escribir «60 FPS PASS» ni «8 GB disponibles» como tolerancia garantizada sin propuesta y aceptación. La lógica Core debe avanzar aun si IA/TTS no responde; TTS local no puede apropiarse silenciosamente de VRAM que comprometa la escena.

## E. F15 — exclusivamente instalación privada y recuperable

El objetivo **no** es publicación, distribución ni pruebas con terceros. El gate de P05 exige versión, SHA256 de artefacto local, ejecución MSI, E2E, migración, rollback, **restauración desde copia**, cero bloqueantes y evidencia. Los canales autorizados en la herramienta corregida son `private_local` y `private_candidate` (nombres de API `release_gate` mantenidos por compatibilidad). La plantilla `NO_EJECUTADO` permanece denegada; un resultado `REVIEW_REQUIRED` requiere acta humana y nunca constituye automáticamente F15 CERRADA.

## F. Checklist de evidencia cuando se reabra el desarrollo

Cada operación futura llevará un ID estable y: fase/dueño, fecha, actor y principal, sesión/ship_id, versión/revisión Core, comando y precondiciones, permisos, recibos, observaciones permitidas, journal, savedata y replay, captura UE5 con versión/asset SHA, casos positivos/negativos, telemetría, fallbacks, resultado y firma de aceptación del responsable. Una PR fusionada o CI verde sin esto puede probar un **corte técnico**, nunca una partida jugable completa.

**Resultado de esta remediación:** quedan fijadas fronteras, pruebas y criterios de rechazo; no se ha ejecutado F07–F15, no se ha enviado trabajo a HOST/Lore/P2, no se ha cambiado el diseño creativo y no se ha autorizado una nueva fase de producción.
