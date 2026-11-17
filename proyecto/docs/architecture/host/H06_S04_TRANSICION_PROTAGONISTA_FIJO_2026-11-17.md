# HOST H06 / F10 — Cambio autoral de producto a protagonista fijo (DEC-0022)

**Fecha:** 17-11-2026. **Estado:** DISEÑO REGISTRADO, HOST/CODEX POR ADAPTAR.

El 15-11-2026, IA-03A/PR #166 implementó una ruta C++ para escoger entre humano, vulcano e híbrido, y el formulario v0.3 admitía edad/origen/biografía libre. Esas herramientas **fueron válidas históricamente**, pero la decisión posterior del autor cambia la UX y el dominio del **jugador inicial**:

- **Un único protagonista canónico** (varón, `human_vulcan_hybrid`, padre descendiente de Khan, madre vulcana, 45 años en 2383), con habilidades/experiencia real ya definida y nombre/cosmética variables.
- **Sin selección de especie, sexo, edad ni historia** en la nueva partida. El código de IA-03A sigue admitiendo tres especies **hasta migración efectiva**; no disfrazar documentación de ejecución.
- No alterar la política general NPC, la biología de otras especies, contratos LOCKED, CoreRPG, F11 ni la seguridad de fuente/recibo/identidad. Publicar/adaptar versión nueva, fixture autoral confiable y pruebas específicas antes de reemplazar la selección de tres especies.
- F10 sigue **dueño** de las restricciones biográficas y admisión; HOST solo coordina; CoreRPG conserva únicos estados autorizados. La IA no añade genética, títulos, rangos, plazas, permisos ni hechos no registrados.
- **Cinemática 2D** con Janeway y Picard, sin Sisko en 2383. Repetición/salto no crea actos de admisión nuevos, relaciones ni ascensos.
- Aprobación/denegación justa de la candidatura se integra con el sistema académico: no saltar el mecanismo institucional ni obligar a repetir evaluaciones ya reconocidas como aprobadas antes de entrar en la Academia.

**Lecturas imprescindibles antes de Codex:** `proyecto/docs/decisions/s04_protagonista_unico_khan_intro_academia_2026-11-17.md`, `sistemas/gameplay/character_creation/S04_PROTAGONISTA_IDENTIDAD_CARRERA_v2.md`, `sistemas/gameplay/character_creation/S04_MIGRACION_F10_HOST_v2.md`, `sistemas/gameplay/character_creation/s04_fixed_protagonist_contract_v2.json`.

Esta nota **no certifica IA-03B/IA-03C ni la integración runtime**; solo previene que HOST vuelva a construir un editor completo del protagonista por seguir planes antiguos.
