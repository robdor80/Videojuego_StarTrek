# Sistema 11 — Astrometría 360°

**Estado: DISEÑO APROBADO / NO IMPLEMENTADO (18-11-2026).**

[Decisión DEC-0023](../../../proyecto/docs/decisions/s11_astrometria_360_2026-11-18.md) · [Diseño completo](S11_ASTROMETRIA_360_DISENO_v1.md)

La Enterprise-D modernizada dispondrá de un **laboratorio de Astrometría 360°** con mapa volumétrico interactivo, cuatro escalas, ciencia, rutas, filtros, información autorizada y controles físicos, LCARS y voz.

## Documentación

- Diseño: S11_ASTROMETRIA_360_DISENO_v1.md
- Datos y mapa: s11_projection_contract_v0.1.json
- Interacciones: s11_interaction_contract_v0.1.json
- Sala Valhalla: s11_enterprise_d_scene_profile_v0.1.json
- Pruebas de aceptación: s11_acceptance_cases_v0.1.json
- Estado técnico real: s11_status_v0.1.json
- Plan de implementación: proyecto/docs/roadmap/S11_ASTROMETRIA_360_PLAN_2026-11-18.md

## Límites

CoreRPG es la verdad; Sensores detectan; Ciencia interpreta; Navegación calcula y ejecuta; HOST coordina; UE5 presenta. **Astrometría no crea una base de datos galáctica nueva ni ejecuta comandos de vuelo.**

Las fichas ordinarias son rápidas y completas cuando la información es legítimamente observable/conocida, según DEC-0021. No se revela información oculta de regiones lejanas ni futuro de WorldState. No hay dependencia de IA externa para zoom, selección o lectura básica.

**Este repositorio contiene por ahora únicamente el diseño del Sistema 11. Los materiales UE5 y su integración ejecutable son tareas futuras.**
