# Proyecto MENU — Menú principal Star Trek Legends

- [Plan maestro MENU v1.0](PLAN_MAESTRO_MENU_v1.0_2026-11-27.md): 9 fases y 90 subfases, dependencias, responsables y criterios.
- [MENU-00 — Auditoría inicial](MENU_00_AUDITORIA_2026-11-27.md): evidencia y reutilización HOST/UE, límites pendientes.
- [MENU-01 — Arquitectura funcional](MENU_01_ARQUITECTURA_FUNCIONAL_2026-11-27.md): P01–P07 especificadas, P08 matriz de aceptación preparada; no certificación funcional.
- [MENU-01 — Grafo y pruebas](MENU_01_NAVIGATION.json): 15 pantallas, 49 aristas condicionales, 40 casos (NOT_RUN). Validación estructural por lectura del blob publicado: JSON válido, IDs/aristas únicos, 15/15 pantallas alcanzables, referencias y cambios de pantalla coherentes, EXIT terminal y guardas explícitas en entrada GAME. Sin errores en estas comprobaciones. No equivale a pruebas UE/HOST.
- [MENU-02 — Contrato de configuración](MENU_02_CONFIGURACION_2026-11-27.md): P01–P11 diseño; P12 especificación de pruebas, ejecución pendiente.
- [MENU-02 — Catálogo y pruebas](MENU_02_SETTINGS.json): 48 opciones semánticas, 66 casos NOT_RUN, 11 áreas. Relectura GitHub: JSON parseable, IDs únicos, secciones/rangos válidos, P01–P12 presentes, casos no ejecutados. No constituye validación UE.
- [MENU-03 — Gestión de partidas](MENU_03_GESTION_PARTIDAS_2026-11-27.md): P01–P10 diseño, P11 matriz de aceptación; integración MENU-06-P06 y certificación MENU-08-P09 pendientes.
- [MENU-03 — Matriz de aceptación](MENU_03_SAVE_ACCEPTANCE.json): 75 casos NOT_RUN, 11 subfases. Relectura GitHub: JSON válido, IDs únicos, referencias de subfase y encabezados coherentes. Sin ejecución de runtime. Continuar universal, autoguardado, metadatos y correlación durable requieren capacidades adicionales; no se declaran implementadas.
- [MENU-04 — Sistemas complementarios](MENU_04_SISTEMAS_COMPLEMENTARIOS_2026-11-27.md): P01–P11 diseño contractual, catálogo, permisos, progresión y límites de integración. Implementación MENU-06-P08, medios MENU-07 y certificación MENU-08 pendientes.
- [MENU-04 — Matriz de aceptación](MENU_04_EXTRAS_ACCEPTANCE.json): 71 casos NOT_RUN, 11 sistemas/subfases; relectura GitHub: JSON válido, IDs únicos, referencias, encabezados, cobertura y campos obligatorios correctos. Sin ejecución UE. Pendiente inventario de lore/medios, adaptadores de dominio y aprobación de políticas de desbloqueo/visibilidad.
- Siguiente diseño: MENU-05, sujeto a revisión/fusión ordenada de MENU-00 a MENU-04. Estética, UX final, políticas de pausa/autoguardado/retención y valores efectivos pendientes de aprobación/pruebas.

Documentación contractual aquí; recursos UI en `audiovisual/ui/menus/`; implementación futura en el proyecto Unreal existente. No crear un proyecto UE paralelo. Aplican AGENTS.md y el gobierno HOST.
