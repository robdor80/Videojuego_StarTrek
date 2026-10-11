# F01-P04 — Propuesta de primer MVP y límites medibles (DEC-0002)

**Fecha:** 2026-10-11 · **Estado:** PROPUESTA_PENDIENTE_AUTOR · **No autoriza implementación anticipada de F07/F08.**

## Contexto: experiencia completa vs primer ejecutable

**Producto final:** RPG 3D que incluye Academia vivida durante cuatro años, servicio en la Flota, carrera opcional, universo persistente, NPC sociales y diferentes naves. **Primera entrega jugable:** corte vertical mínimo para comprobar que estas bases pueden funcionar; no se confunde con producto final.

## Alcance recomendado del prototipo v0.0.1 (sujeto a aprobación)

- Un **escenario de guardia en Sensores** dentro de una nave de Starfleet del periodo `tng_ds9_voyager`; para verificación de reglas reutilizar el fixture de **2372-03-14**, semilla `fixture_sensor_v0_0_1`.
- El jugador ocupa un puesto subordinado autorizado; otro oficial entrega una orden; el jugador ejecuta una operación de Sensores real, ve el resultado según permisos/conocimiento y transmite un informe.
- Hay una consola 3D interactiva en un puente importado lícitamente, no un menú con botones sin World State.
- El universo ya contiene objetos antes de la observación. Resultado reproducible con semilla fija. Acciones relevantes pasan por el Core, se registran con trazabilidad y la evaluación consume evidencias, nunca inventa resultados.
- Un pequeño conjunto **fijo y explícito** de NPC relevantes para la guardia, con IDs, rol, puesto y límites de conocimiento; los demás NPC y eventos se simulan conforme al alcance real del Core disponible.
- Guardar y recuperar como mínimo identidad, estado de observación, orden/registro y la continuidad de la guardia cuando las capacidades reales del Core lo permitan.

**No incluidos en v0.0.1:** cuatro años de Academia 3D, cadena completa de ascensos, todas las consolas, teletransporte, combate espacial completo, planeta explorado libremente, tres puentes jugables, centenas de tripulantes renderizados a la vez, IA libre escribiendo el World State.

**Importante:** excluir la Academia *del primer build* no la elimina del **juego**. El prototipo puede situar temporalmente a un jugador ya asignado para probar una guardia; en la experiencia completa la Academia sigue siendo el itinerario de entrada previsto.

## Flujo de aceptación propuesta

1. Se selecciona/carga escenario semilla fija y un operador con permiso.
2. Se valida la orden y la guardia; fallo de permiso no produce operación autorizada.
3. Se ejecuta un escaneo desde la consola, con entradas observables.
4. Se muestra información parcial, incertidumbre o ausencia de detección según sensores y mundo; sin revelar atributos ocultos.
5. Se envía informe y queda evento append-only con autor y hora; NPC sin acceso no conoce datos mágicamente.
6. Se guarda, recarga y comprueba igualdad de IDs, datos observados, registro y consecuencias.
7. Un fallo de proveedor IA o red no anula las reglas deterministas ni fabrica datos.
8. Se presenta con control e interacción reales en UE5 y hay evidencia registrada en el MSI.

## Presupuesto técnico: método y propuestas, NO cifras aprobadas

**Equipo de referencia para probar:** MSI Raider GE78 HX 14V: i9-14900HX, 32 GB RAM, RTX 4070 portátil 8 GB VRAM, Windows 11, panel 2560×1600.

| Área | Métrica observable | Estado |
|---|---|---|
| FPS / frame time | media, percentil 95, máximos picos; en 1920×1080 y resolución nativa | Umbral de aceptación pendiente |
| GPU / VRAM | memoria máxima y media; ausencia de agotamiento, fallos y degradación acumulada | Se medirá en F07/F08 |
| CPU / RAM | tiempo en hilo de juego y render, memoria residente y picos | Se medirá en F07/F08 |
| Carga | arranque a guardia interactiva, transición y carga/guardado | Sin presupuesto aprobado |
| NPC | número simultáneo de actores visibles, NPC simulados fuera de escena y tiempos de actualización | Presupuesto por diseñar F04/F07/F12 |
| Estabilidad | 30 min de sesión repetible, 0 bloqueantes, 0 pérdidas de estado en casos aprobados | Protocolo sugerido, pendiente |
| Determinismo | misma semilla/entrada produce mismo resultado sin red; negatividad por permisos y fugas | Requisito funcional ya derivado |
| Licencias/assets | fuente, permiso de uso, hash de origen, importación UE5 y materiales visibles | Puerta previa de F07/F14 |

No declarar «60 FPS garantizados» ni «jugable a resolución nativa» antes de medir. Como **referencia de discusión**, valorar perfiles 1080p fluido / nativo ajustado sin aceptar números por fe. Los umbrales se fijarán con el autor y después se medirán.

## Decisión de autor solicitada

Aprobar o modificar la **guardia de Sensores como primer build** en lugar de empezar por toda la Academia 3D, y dar prioridad a fluidez/estabilidad del MSI con objetivos numéricos que fijaremos tras benchmarking real.

## Fuentes y dependencias

`docs/roadmap/ship_console_vertical_slice_v0_0_1.md`; `validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json`; `gameplay/careers/academy_path/academy_gameplay_loop.md`; `docs/roadmap/master/fases/F07/README.md`; `docs/roadmap/master/fases/F08/README.md`; `docs/roadmap/master/CRITERIOS_DE_CIERRE.md`.

**Evidencia en F01:** propuesta documental inspeccionable; **NO_EJECUTADO:** benchmarking MSI, import UE5, Core o sesión jugable.
