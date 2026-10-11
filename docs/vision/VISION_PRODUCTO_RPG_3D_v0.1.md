# Visión de producto — Star Trek RPG 3D (F01-P01)

**Versión:** 0.1 · **Fecha de auditoría:** 2026-10-11 · **Estado:** BASELINE_RECONCILIADA (principios heredados aprobados; NO equivale a aprobación de Dama/MVP) · **Madurez:** DISENO_VALIDADO del alcance ya fijado.

## Promesa al jugador

Vivir una trayectoria personal dentro de Star Trek: entrar en la Flota Estelar, formarse, adquirir experiencia, desarrollar relaciones, tomar decisiones operativas y habitar un universo que continúa funcionando cuando el jugador está en otro sitio. No es una secuencia obligatoria de episodios, ni un simulador de combate sin vida social, ni una carrera que culmine forzosamente en capitanear la Imperator.

## Reglas de producto vigentes (REUTILIZAR; no son propuestas nuevas)

1. **Plataforma de destino:** videojuego 3D para PC Windows, con el MSI Raider GE78 HX 14V como equipo de desarrollo/prueba (i9-14900HX, 32 GB, RTX 4070 portátil de 8 GB, 2560×1600). El hardware de prueba NO constituye un presupuesto de fotogramas medido; pendiente de F07/F08.
2. **Tres épocas jugables** `pike`, `kirk`, `tng_ds9_voyager`, con tecnología, uniformes y disponibilidad filtrados por fecha; no hay siete universos duplicados.
3. **Canon histórico hasta el inicio de la partida; futuro emergente** sin reproducir obligatoriamente la historia audiovisual posterior.
4. **Academia jugable:** ingreso, cuatro años × tres trimestres, vida de cadete, formación, especialización, graduación y destino como alférez. `academiaflota` publica estudio/formación; no es el mundo 3D.
5. **Ascensos por evidencia y oportunidades reales:** sin XP genérico, sin capitanía inmediata al graduarse. El jugador puede seguir en su puesto, aceptar/solicitar destinos, progresar en distintas especialidades o perseguir el mando de la Imperator; no hay «final obligatorio».
6. **Universo preexistente al conocimiento del jugador:** mundo autoritativo, simulación determinista/persistente, memoria limitada de NPC, y simulación fuera de escena desacoplada de cargar actores 3D.
7. **Relaciones y hábitos significativos**, sujetos a agendas, consentimiento/privacidad y consecuencias contextuales ya definidas; no adjudicar nuevos límites de contenido en F01 sin intervención de autor.
8. **Operaciones reales:** consolas funcionales con operaciones y permisos independientes del aspecto visual; primer corte vertical es Sensores, con orden, resolución, resultado, registro y posible evaluación.
9. **Lengua pública:** castellano de España (`es-ES`); IDs internos estables independientes de idioma.
10. **Fronteras:** Core RPG general = reglas/estado/persistencia autoritativos cuando existan; Star Trek = datos, políticas y reglas de universo; UE5 = escena/interacción/render 3D; IA remota = lenguaje/asistencia, no mutación de estado; NAP/Rob3D = producción de recursos, no motor de mundo.

## Vivencia prevista y ritmos (visión, no backlog ejecutado)

- **Cadete:** clases, compañeros con memoria, prácticas, decisiones, ocio, tareas y calificaciones con consecuencia.
- **Oficial de servicio:** turno, consolas, órdenes contextualizadas, subordinación real, incidentes y registros.
- **Trayectoria larga:** ascensos, cambios de destino, especialización, puestos con distinta autoridad, oportunidades de mando y relaciones que no se congelan.
- **Universo:** descubrir un lugar no equivale a crearlo; las consecuencias pueden alcanzar a otras naves y facciones fuera de cámara.

## Límites explícitos

- No prometer contenido de toda la galaxia en el primer ejecutable, ni puentes/espacios interiores de las tres Damas simultáneamente.
- No transformar aprobaciones documentales de 120 capas / 20 pasos en validación de juego UE5.
- No convertir «capitán» en una opción universal de anular cualquier ley física, autoridad, permisos o Primer Directriz; el control de decisiones de mando depende del puesto, delegación y reglas Trek.
- No construir Core RPG paralelo ni segunda versión del currículo de la web.
- No elegir clase base de Imperator por comodidad del prototipo, ni imponer un destino o final.
- Los perfiles temporales no autorizan por sí solos naves posteriores a la fecha de campaña.

## Fuente de verdad / trazabilidad

- `docs/decisions/playable_eras.md`; `docs/decisions/campaign_continuity.md`.
- `docs/decisions/player_facing_language.md`; `docs/decisions/personnel_model.md`; `docs/decisions/player_objectives.md`; `docs/decisions/character_growth_without_xp.md`.
- `docs/decisions/academy_playable_hub.md`; `gameplay/careers/academy_path/academy_career_v0_2.md`.
- `docs/decisions/authoritative_observable_universe.md`; `docs/roadmap/ship_console_vertical_slice_v0_0_1.md`.
- `gameplay/careers/starfleet_service/README.md`; `docs/roadmap/game_design_readiness_v0_2.md`.
- `docs/roadmap/master/PLAN_MAESTRO.md`; `docs/roadmap/master/DECISIONES_Y_RIESGOS.md`.

**Pendiente exclusivamente de autor:** `DEC-0001` (Dama/Imperator) y `DEC-0002` (límites del MVP). Véanse los expedientes en `docs/roadmap/master/fases/F01/`.
