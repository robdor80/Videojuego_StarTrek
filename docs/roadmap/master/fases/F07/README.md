# F07 — Pipeline 3D, Rob3D y puente piloto

**Estado de la fase global:** PLANIFICADA (reconocimiento de trabajo previo no equivale a cierre de fase).
**Nivel objetivo:** PROTOTIPO_UE5_PROBADO.

## Objetivo

Cadena reproducible de importación/modelado y una escena interactiva usable en UE5.

## Pasos y entregables

- [ ] **F07-P01** — Auditar fuentes 3D externas, Rob3D, Blender, formatos, materiales, licencias y versiones sin tocar originales.
- [ ] **F07-P02** — Fijar procesos de mallas, escala, ejes, UV/PBR, texturas, colisiones, pivotes y optimización.
- [ ] **F07-P03** — Seleccionar puente piloto para corte vertical sin confundirlo con la decisión final de la Dama.
- [ ] **F07-P04** — Preparar movimiento, interacción, cámaras y modos de consola en puente 3D.
- [ ] **F07-P05** — Verificar empaquetado reproducible, uso de RAM/VRAM y rendimiento en el equipo objetivo.

## Material del repositorio que se aprovecha sin moverlo

- `assets/ships/`
- `assets/scenes/`
- `art_direction/visual_bibles/`
- `presentation/`
- `ui/bridge/`
- `ui/lcars/`

**Tratamiento:** auditar vigencia de archivos y subcontratos antes de afirmar que cada paso está cerrado; conservar rutas originales y referenciarlas en la [matriz de reutilización](../../MATRIZ_REUTILIZACION.md).

## Dependencias y límites

F01 para canon de nave final; F06 para operativa; pipeline puede prototiparse antes de integración Core.

## Puerta de cierre

Escena 3D jugable de prueba con elementos inspeccionados y licencias verificadas; no contar imágenes/blueprints como modelos UE5. Registrar pruebas realmente ejecutadas, commit/PR, incidencias y decisiones de autor. Sin evidencias, no marcar `CERRADA`.

Véanse [criterios de cierre](../../CRITERIOS_DE_CIERRE.md), [plan maestro](../../PLAN_MAESTRO.md) y [estado global](../../ESTADO_GLOBAL.json).
