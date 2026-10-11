# Dirección del proyecto — Star Trek RPG 3D

**Plan maestro global de control.** Actualizado: 11-10-2026. Este directorio está **por encima de los roadmaps especializados**, no los reemplaza.

## Por dónde empezar

1. [PLAN_MAESTRO.md](PLAN_MAESTRO.md) — secuencia F00–F15, hitos y pasos.
2. [ESTADO_GLOBAL.json](ESTADO_GLOBAL.json) — estado de cada fase y nivel objetivo, legible por máquinas.
3. [AUDITORIA_F00.md](AUDITORIA_F00.md) — evidencias del repositorio y conclusión de la F00.
4. [MATRIZ_REUTILIZACION.md](MATRIZ_REUTILIZACION.md) — ubicación original → fases/pasos donde se aprovecha.
5. [INVENTARIO_BASELINE_2026-10-11.json](INVENTARIO_BASELINE_2026-10-11.json) — instantánea de los 1.720 archivos preexistentes.
6. [DEPENDENCIAS_CORE_RPG.md](DEPENDENCIAS_CORE_RPG.md) y [DEPENDENCIAS_EXTERNAS.md](DEPENDENCIAS_EXTERNAS.md) — límites de integración.
7. [CRITERIOS_DE_CIERRE.md](CRITERIOS_DE_CIERRE.md) — qué significa terminar de verdad.
8. [DECISIONES_Y_RIESGOS.md](DECISIONES_Y_RIESGOS.md) — decisiones de autor y riesgos.
9. [fases/F00/README.md](fases/F00/README.md) — acta de cierre F00 y puertas pendientes para F01.

Las demás fases están en `fases/F01/` a `fases/F15/`, todas con cinco pasos iniciales. Las ideas nuevas se registran en [`ideas/BUZON.md`](../../../ideas/BUZON.md) y **no se implementan fuera de fase**.

## Jerarquía de autoridad documental

- **Este plan maestro** gobierna prioridad, alcance, fase activa, puertas de cierre y trazabilidad del desarrollo global.
- **`CONTENT_STATUS.md`** conserva el avance editorial/lore y el alcance declarado de cada contrato. Un `COMPLETE` documental no implica `UE5_JUGABLE`.
- **Roadmaps especializados existentes** (8 pilares, 120 capas, 10 bloques, 20 pasos de vida académica, Sensores, vida a bordo) conservan su propio orden, ID, entregables y evidencias: no se renumeran.
- **`gameplay/`, `lore/`, `universe/`, `ai/`, `assets/`, etc.** son los originales técnicos y la fuente de reglas. **No se mueven a las carpetas por fase**.
- **Core RPG** controla estado/acción/persistencia genéricos cuando estén implementados. **Star Trek** reglas y contenido Trek. **UE5** presentación/experiencia 3D. Ninguna fase autoriza un motor paralelo.

## Cómo trabajar en cada paso

1. Consultar `ESTADO_GLOBAL.json`, ficha de fase y sus dependencias.
2. Buscar existencia previa en `MATRIZ_REUTILIZACION.md` e inventario, más búsqueda real de contratos/archivos relacionados.
3. Clasificar: **REUTILIZAR / COMPLETAR / CORREGIR / NUEVO / DECISION_AUTOR / BLOQUEADO_EXTERNO**.
4. Definir alcance, diseño, contrato, pruebas y enlaces; trabajar en rama y PR siempre que se pueda.
5. Ejecutar las validaciones relevantes y guardar evidencia (comando, resultado, commit, enlace).
6. Actualizar fichas y estado **solo al alcanzar el nivel objetivo**. No cambiar `CONTENT_STATUS.md` si no ha cambiado su alcance editorial.

**Regla antifallos:** una idea nueva no altera la fase activa. Se registra, se evalúa al planificar y se incorpora con ID y dependencias; si cambia una decisión de autor, hay que obtener aprobación expresa.
