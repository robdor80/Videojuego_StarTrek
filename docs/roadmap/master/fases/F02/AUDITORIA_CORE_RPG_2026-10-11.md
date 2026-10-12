# F02-P01 — Auditoría del CoreRPG REAL

**Corte:** 2026-10-11. **Método:** lectura de repositorio, ramas, fuentes C++/CMake, contratos y GitHub Actions. **No se ha compilado CoreRPG localmente.**

## Referencias comprobadas

| Repositorio/ref | SHA exacto | Uso |
|---|---|---|
| [CoreRPG `main`](https://github.com/robdor80/CoreRPG/tree/dcfcb83c9853e005b5450bd39e0ba693cb91e257) | `dcfcb83c9853e005b5450bd39e0ba693cb91e257` | **Única API de producción integrada comprobada** |
| [CoreRPG `feat/generic-world-state`](https://github.com/robdor80/CoreRPG/tree/2a3da891d8c56e9868c7bd67dbeb6041509df2ce) | `2a3da891d8c56e9868c7bd67dbeb6041509df2ce` | 4.5 en desarrollo, **NO integrada en main** |
| [CoreRPG CI de main](https://github.com/robdor80/CoreRPG/actions/runs/38046482745) | main `dcfcb83`, 2026-10-10 | GitHub Actions `completed/success`; no sustituye build UE5 |
| [CoreRPG CI de rama 4.5](https://github.com/robdor80/CoreRPG/actions/runs/37812440972) | rama `2a3da89`, 2026-10-08 | GitHub Actions `completed/success`; no acredita merge |
| [Star Trek main](https://github.com/robdor80/Videojuego_StarTrek/tree/164be98ab02d81ac9580160e555e75a10e6d489f) | `164be98ab02d81ac9580160e555e75a10e6d489f` | Base al crear rama F02 |
| [F01, PR #2](https://github.com/robdor80/Videojuego_StarTrek/pull/2) | rama `docs/f01-vision-canon-scope`, foto del 11-10-2026 | **Estado entonces:** abierta y Dama pendiente. **Actualización 13-10-2026:** fusionada, Dama Galaxy → nueva Clase Valhalla aprobada |

## Capacidades comprobadas en CoreRPG/main

| Capacidad | Evidencia en código/documento | Resultado |
|---|---|---|
| Identidad entidad viva | `include/corerpg/entity_id.hpp`: `EntityId` entero sin signo 64-bit, cero inválido | **DISPONIBLE**, identidad scoped a un WorldState, no universal |
| Estado mundo mínimo | `include/corerpg/world_state.hpp`: `create_entity()`, `contains()`, `entity_count()`, `revision()` | **DISPONIBLE**, no almacena ficha de nave/NPC |
| Determinismo | `include/corerpg/random.hpp`, `roll_action.hpp` | **DISPONIBLE** vertical `RollAction` no mutante, **no** framework de acciones |
| Definiciones | `DefinitionId`, `PackId`, `ResourceKind` y `ContentCatalog::create` | **DISPONIBLE** catálogo de referencias/validación |
| Content JSON | `CoreRPGContentJson` opcional, `schemas/content/0.1.0/` | **DISPONIBLE** sólo manifest/definiciones básicas, sin payload Trek |
| Reglas genéricas aplicables | Roadmap 4.6 | **NO DISPONIBLE en main** |
| Eventos y motor de acciones general | Roadmap 4.10 | **NO DISPONIBLE en main** |
| Persistencia campaña/save-load | Roadmap 4.7 | **NO DISPONIBLE en main** |
| Tiempo, actividad fuera de escena, NPC | Roadmap 4.8/4.10 | **NO DISPONIBLE en main** |
| Visibilidad/Knowledge/Context Builder | Roadmap 4.9/4.12 | **NO DISPONIBLE en main** |
| Adaptador UE5 / puente `DefinitionId → EntityId` | Roadmap 4.14 y README | **NO DISPONIBLE en main** |

En la **rama 4.5**, `world_state.hpp` añade, entre otras cosas, `next_entity_id`, `container_of`, `place_entity` y `remove_containment`, con estados explícitos para errores de contención. Esa interfaz es **evidencia de desarrollo**, no contrato aprobado de main, ni proporciona simulación de tripulación.

## Condiciones técnicas verificadas

- C++20 y CMake 3.25+, biblioteca principal `CoreRPG`, biblioteca opcional `CoreRPGContentJson`. Documentación: [README de Core](https://github.com/robdor80/CoreRPG/blob/dcfcb83c9853e005b5450bd39e0ba693cb91e257/README.md).
- Core es agnóstico de UE5, Nimroel y Star Trek; sus Content Packs no ejecutan scripts; la autoridad de las mutaciones reside en el Core.
- El **Content Contract 0.1.0** no admite todavía fichas completas de especies, naves o miembros de dotación; no se debe hacer pasar `ResourceDefinition` por esquema Trek.
- **No se ha ejecutado** CMake, CTest, compilación Windows en el MSI, UE5 ni un E2E Core↔Star Trek en esta auditoría. Únicamente se ha **consultado** CI remota existente y leído código.

## Riesgo y decisión operativa

**R-CORE-01 — ALTO:** adaptar Star Trek a métodos de 4.5 mientras no estén en main causaría acoplamiento inestable. **Mitigación:** fichar contratos existentes, describir necesidades y verificar el SHA después de cada merge; no fijar ABI, versión o llamadas de un Core futuro.

**Conclusión P01:** auditoría de capacidad/estado actual completada con evidencias remotas. Esto **no cierra F02** y no certifica integración funcional. Fuentes de coordinación: `docs/roadmap/master/DEPENDENCIAS_CORE_RPG.md` y `docs/roadmap/master/CRITERIOS_DE_CIERRE.md`.
