# F00 — Auditoría, organización y gobierno del proyecto

**Estado:** CERRADA (alcance organizativo). **Fecha:** 11-10-2026. **Siguiente fase principal:** F01 — Visión del producto y canon.

## Objetivo y exclusiones

Establecer una única estructura profesional de dirección para el RPG Star Trek 3D, aprovechando el repositorio actual y **sin** mover archivos técnicos, rediseñar el canon, escribir un segundo Core RPG, ejecutar módulos pendientes ni crear contenido UE5 nuevo.

## Cinco pasos y comprobaciones

- [x] **F00-P01 — Inventario y línea base.** Árbol completo `main@0800322d4321cc781f0d9603f9a900dcb2f2bc27`: 1.720 archivos y 794 directorios; JSON con ruta, SHA, tamaño y fase orientativa.
- [x] **F00-P02 — Reutilización y diagnóstico.** [MATRIZ_REUTILIZACION.md](../../MATRIZ_REUTILIZACION.md) enlaza los planes y sistemas; [AUDITORIA_F00.md](../../AUDITORIA_F00.md) separa lo observado de lo pendiente. Ninguno de los 1.720 archivos originales ha sido trasladado.
- [x] **F00-P03 — Estados y pruebas de cierre.** [CRITERIOS_DE_CIERRE.md](../../CRITERIOS_DE_CIERRE.md) fija estado vs nivel de madurez y evidencia requerida; [ESTADO_GLOBAL.json](../../ESTADO_GLOBAL.json) registra 16 fases y 80 pasos.
- [x] **F00-P04 — Dependencias y riesgos.** [Core RPG](../../DEPENDENCIAS_CORE_RPG.md), [externos](../../DEPENDENCIAS_EXTERNAS.md) y [decisiones/riesgos](../../DECISIONES_Y_RIESGOS.md), incluyendo restricciones y asuntos de autor pendientes.
- [x] **F00-P05 — Publicación y enlace.** [Plan maestro](../../PLAN_MAESTRO.md), fichas F00–F15, índice desde raíz/`proyecto/docs/roadmap`, buzón de ideas enlazado; commit mediante rama y PR validado antes del cierre en `main`.

## Qué se ha decidido en F00

1. **Carpetas técnicas originales intactas**; las fases viven bajo `proyecto/docs/roadmap/master/fases/` y apuntan a ellas.
2. 16 fases `F00`–`F15` y cinco pasos iniciales por fase; **estructura de gestión aprobada**; tareas futuras pueden subdividirse con control de versión.
3. Un plan maestro de nivel producto; subplanes antiguos conservados íntegros y con sus propias numeraciones.
4. El criterio `COMPLETE` anterior solo acredita su **alcance declarado**; estado de planificación y madurez técnica son independientes.
5. Una **fase principal** abierta de trabajo; entradas nuevas en `proyecto/ideas/`, con traza a fase/decisión/prueba.
6. Core RPG universal / Star Trek específico / UE5 visual / Academia web / NAP como herramientas diferenciadas.

## Evidencias de alcance y límites

- Inventario base: [JSON](../../INVENTARIO_BASELINE_2026-10-11.json).
- CI histórica comprobada: [Academy Life Closure run 38080058680 — success, 10-10-2026](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/38080058680); F00 **no ha ejecutado localmente las 482 pruebas definidas**.
- En el árbol auditado no se localizaron proyectos ni modelos de fuente `.uproject/.uasset/.umap/.blend/.fbx/.glb/.gltf`; esto no prueba ausencia en otros repositorios o en el PC.
- Dama base y alcance autoral del MVP están **pendientes** en [DECISIONES_Y_RIESGOS.md](../../DECISIONES_Y_RIESGOS.md); no se han elegido en F00.
- El informe de Core 4.10 expresa luz verde **arquitectónica y gradual**, no un motor universal de mando implementado.

## Puerta de entrada a F01

- Estudiar documentos ya aprobados de visión y épocas; no decidir por defecto la Dama.
- Presentar al autor solo decisiones realmente creativas (alcance mínimo UE5, Dama, prioridades), conservando otras ya fijadas.
- No abrir la implementación de otras fases hasta verificar la relación con Core RPG y el primer corte jugable.

**Cierre F00 = cierre de organización.** No implica implementar F01–F15, ni que toda la documentación original esté revalidada individualmente.
