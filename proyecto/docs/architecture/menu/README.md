# Proyecto MENU — Menú principal Star Trek Legends

- [Plan maestro MENU v1.0](PLAN_MAESTRO_MENU_v1.0_2026-11-27.md): 9 fases y 90 subfases, dependencias, responsables y criterios.
- [MENU-00 — Auditoría inicial](MENU_00_AUDITORIA_2026-11-27.md): evidencia y reutilización HOST/UE, límites pendientes.
- [MENU-01 — Arquitectura funcional](MENU_01_ARQUITECTURA_FUNCIONAL_2026-11-27.md): P01–P07 especificadas, P08 matriz de aceptación preparada; no certificación funcional.
- [MENU-01 — Grafo y pruebas](MENU_01_NAVIGATION.json): 15 pantallas, 49 aristas condicionales, 40 casos (NOT_RUN). Validación estructural por lectura del blob publicado: JSON válido, IDs/aristas únicos, 15/15 pantallas alcanzables, referencias y cambios de pantalla coherentes, EXIT terminal y guardas explícitas en entrada GAME. Sin errores en estas comprobaciones. No equivale a pruebas UE/HOST.
- Siguiente diseño: MENU-02, sujeto a revisión/fusión de MENU-00 y MENU-01. Estética, UX final y política de pausa pendientes de decisión del propietario.

Documentación contractual aquí; recursos UI en `audiovisual/ui/menus/`; implementación futura en el proyecto Unreal existente. No crear un proyecto UE paralelo. Aplican AGENTS.md y el gobierno HOST.
