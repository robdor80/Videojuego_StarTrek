# F00 — Auditoría estructural del repositorio (línea base)

**Fecha:** 11-10-2026. **Ámbito:** `robdor80/Videojuego_StarTrek`. **Base verificada:** `main@0800322d4321cc781f0d9603f9a900dcb2f2bc27`. La F00 añade una estructura de control **sin mover ni modificar contratos/activos técnicos**.

## Evidencia de estructura Git

Consulta de árbol Git recursivo de `main` (`truncated=false`): **1.720 archivos (blobs), 794 directorios (trees)**, incluyendo los 2 archivos ya creados en `ideas/` antes de F00. En la raíz: **22 directorios** contando `ideas/`, y **4 archivos**. Antes de `ideas/` había 1.718 archivos.

| Área | Archivos | Lectura |
|---|---:|---|
| `gameplay/` | 839 | Contratos, currículos, carrera, simulación y sistemas de nave |
| `lore/` | 238 | Referencias y lore utilizable |
| `validation/` | 148 | Fixtures, invariantes y referencias de aceptación |
| `universe/` | 87 | Cronología/generación |
| `assets/` | 83 | Predominio de planos, referencias e imágenes de puentes |
| `tools/` | 66 | Generadores Python, scripts de prueba y validación |
| `docs/` | 53 | Roadmaps, decisiones, documentación |
| `art_direction/` | 48 | Biblias visuales y contratos NAP |
| `ai/` | 33 | Comportamiento, memoria, diálogo y contextos |
| `narrative/` | 21 | Misiones y eventos causales |
| `presentation/` | 19 | Estados visuales, cámaras, POV, escenas |
| `ui/` | 18 | Diseño de HUD y consolas |
| `audio/` | 15 | Sobre todo estructura de carpetas |
| Otros y raíz | 52 | `content,localization,manifests,nap,research,schemas,sources,ideas,.github` y cuatro archivos raíz |

**Comprobaciones añadidas:** 438 rutas `README.md`; **293 miden 150 bytes o menos**, por lo que una parte de la estructura es potencialmente marcador de posición. Es un **indicador para revisión, no una afirmación de que los 293 carecen de contenido**. Hay **60 archivos Python**, pero la consulta de rutas no contiene extensiones `.uproject`, `.uasset`, `.umap`, `.blend`, `.fbx`, `.glb` o `.gltf` (en este repositorio y corte). Los modelos analizados externamente con Blender/Rob3D no deben darse por incorporados.

**Límite del método:** se han revisado en profundidad índices, roadmaps y contratos representativos, y se ha enumerado cada ruta, SHA y tamaño. **No** se ha inspeccionado manualmente el contenido de cada uno de los 1.720 archivos ni ejecutado toda la batería local. La clasificación automática por ruta queda señalada como heurística en el JSON de inventario.

## Verificación de entregables anteriores

- `CONTENT_STATUS.md` diferencia explícitamente `COMPLETE` según el alcance documental. Hay que conservar esa precisión.
- `docs/roadmap/game_design_readiness_v0_2.md`: ocho pilares con base establecida y profundización pendiente.
- `docs/roadmap/procedural_layers_master_plan_v0.1.md`: 001–118 cerradas en diseño/contratos, 119 parcial y 120 bloqueada por runtime.
- `docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md`: bloques 1–3 cerrados a nivel de referencia; 4 es el siguiente pendiente.
- `docs/roadmap/academy_life_final_closure_v1.0.md`: 20/20 pasos en referencia; **482 pruebas definidas** en su manifest. Existe workflow `academy-life-closure.yml`.
- **CI observada:** GitHub Actions [Academy Life Closure, run 38080058680](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38080058680), desencadenada por commit `fc5976ae8b3f6ceb78b0fdd49ea51a37c5693a58` el 10-10-2026, estado `completed/success`. Se acredita ese run, **no se ha reejecutado la suite local durante F00**. Existieron runs fallidos anteriores corregidos después.
- `docs/roadmap/shipboard_life_and_procedural_starship_generation_plan_v0.1.md`: 15/15 paquetes `COMPLETE` a nivel de reglas/generadores de referencia.
- `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`: base de Sensores, log, fixture; integración UE5/Core pendiente.
- `gameplay/chain_of_command/`, `gameplay/orders/`: autoridad por puesto y contexto, órdenes estructuradas y delegación. Auditoría Core del 11-10-2026 solo acepta necesidad e integración posible a partir de **4.10+**: no inventar contrato universal ya entregado.

## Hallazgos que justifican F00

1. **Planes maestros solapados:** existe plan global documental, roadmap de 8 pilares, 120 capas, 10 bloques, 20 pasos de vida académica y 15 paquetes de nave, pero no gobernaban la entrega completa UE5/Core/Academia.
2. **Estados confundibles:** `COMPLETE` de contratos, scripts, CI y juego 3D no son equivalentes. Introducir dos dimensiones (estado y madurez/objetivo).
3. **Estructura vs desarrollo:** cientos de README cortos; contar directorios no mide ejecución.
4. **Falta de vínculo único:** idea → decisión → fase/paso → archivo existente → prueba → cierre.
5. **Separación de repositorios:** Star Trek contiene reglas; Core RPG desarrolla motor; UE5 se implementará en su entorno; NAP gestiona producción y archivos; academiaflota publica material web.
6. **Cambios recientes de producto aún por reconciliar:** carrera gradual, tres rutas, Galaxy/Sovereign/Odyssey y futura Imperator, puente piloto, herramientas 3D y límite hardware.
7. **Raíz poco orientativa:** `README.md` original de solo 23 bytes y `docs/roadmap/README.md` presentaba el roadmap de 8 pilares como principal. Se añade índice profesional sin tocar reglas.

## Decisión de arquitectura organizativa

**Conservar** el repositorio técnico entero. Crear `docs/roadmap/master/` como autoridad de **planificación y progreso general**; 16 fases F00–F15 con cinco pasos cada una. Mantener los roadmaps anteriores como subplanes con sus IDs intactos y matriz de reutilización. `ideas/` sigue siendo la entrada sin alterar agenda. El inventario JSON incorpora las 1.720 rutas originales (SHA, tamaño, fase primaria inferida), facilitando comparación futura.

**Nada de implementar por ocurrencia:** cada idea se captura, compara con archivos existentes, se decide y se programa en el lugar correcto. La fase activa y los criterios de cierre gobiernan las prioridades.

## Resultado operativo de F00

- `F00-P01` — inventario de rutas Git / distribución / límites del muestreo: **CERRADO**.
- `F00-P02` — matriz de reutilización y reconciliación de roadmaps: **CERRADO a nivel de áreas/sistemas**, no certificación individual de los 1.720 contenidos.
- `F00-P03` — doble estado y criterios de evidencia: **CERRADO**.
- `F00-P04` — dependencias y registro de riesgos/decisiones: **CERRADO**.
- `F00-P05` — estructura de dirección F00–F15 e índices publicados/validados: **CERRADO** tras merge verificado.

**No incluido en F00:** creación de lógica de juego, elección de la Dama, validación binaria de los assets, ejecución completa de suites, inspección íntegra de cada archivo o integración UE5. Eso se programará en fases y pruebas concretas.

**Estado siguiente:** F01 — decidir visión, hitos y cuestiones autorales antes de comprometer producción. El universo dinámico conserva Bloque 4 como su **próxima unidad interna pendiente**, no se mezcla con la prioridad global F01.
