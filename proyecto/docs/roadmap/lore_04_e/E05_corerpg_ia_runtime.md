# LORE-04E05 — CoreRPG, WorldState, IA, persistencia y observación

**Estado:** AUDITORÍA DOCUMENTAL EN PR DRAFT — sin merge, sin certificación runtime ni decisiones creativas añadidas.

## 1. Verificación independiente disponible

Se ha leído GitHub `robdor80/CoreRPG/main@4f282863737bcd8f5add401202a9e1064c133672`. El último commit visible en la verificación es `Merge pull request #11 ... 4.13: validar Content Pack real de Nimroel y continuidad estructural`. Ello demuestra una base avanzada, **pero no** ejecución de la integración de este contenido Star Trek LORE-04 con CoreRPG y Unreal Engine. No se ha abierto ni compilado un runtime Star Trek ni conectado a una escena UE5.

## 2. Fronteras irrevocables

**CoreRPG**: IDs, WorldState, reloj y ejecución genérica, validación de acciones, historia, conocimiento, persistencia, simulación y transiciones. **Star Trek**: lore, sociedades y perfiles específicos, instituciones y reglas de dominio, pruebas de contratos y contexto. **UE5/NAP**: visual, representación, assets. **IA**: interpretación, diálogo, propuesta autorizada, jamás modificación del estado. La división de autoridad se mantiene aunque el NPC hable como gobernador, médico o comerciante.

## 3. LOD y tiempo

Las poblaciones agregadas y los individuos persistentes no se rerollean, y el detalle reducido no modifica existencia ni permite actuar en dos lugares simultáneos. No se inventan eventos pasados al entrar en una región. Las simulaciones fuera de cámara requieren evento/capacidad real de CoreRPG, sin pretender que las fichas de este repositorio constituyen un scheduler.

## 4. Reserva técnica

La revisión de integración deberá confirmar aplicación del Content Pack Star Trek, WorldState con actos de comercio, ley vigente, servicios y tránsito, reproducibilidad guardado/carga y observadores diferentes. Hasta entonces el estado es `BLOCKED_RUNTIME_FOR_GAMEPLAY` y `DOCUMENTARY_CANDIDATE` para esta fase.

**Control:** CoreRPG es dueño del WorldState; fuentes de verdad LORE-01/02/03 y F00–F15 no se duplican. El dictamen final depende de CI, revisión de autor y fusiones posteriores expresas.
