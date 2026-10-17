# LORE-01 A — Informe de entrega y auditoría

**Fecha:** 2026-10-17 · **Época:** TNG/DS9/VOY, 2364–2378 como marco de investigación, NO fecha fija de campaña.  
**Estado:** CONTENIDO DESARROLLADO Y VALIDADO DOCUMENTALMENTE; **PENDIENTE REVISIÓN DE PR, FUSIÓN Y VERIFICACIÓN EN main**.  
**Rama:** `lore/01-tng-species-cultures`.

## Decisión del autor
El juego principal recibe solo la ampliación boliano, benzita, el-auriano, breen y pakled. Kazon, ocampano, talaxiano, vidiano e hirogen se documentan para un **futuro DLC independiente del cuadrante Delta**. Portal transwarp Borg: idea aprobada para estudiar más adelante; modelo 3D disponible al autor, ninguna ruta ni mecánica desarrollada.

Excepciones **expresas y justificadas**: diáspora el-auriana y presencia Borg en el juego principal. No convertir el DLC en requisito para encuentros Borg canónicos de TNG.

## Inventario y ubicación
- 15 perfiles de especie heredados, **sin sustituir ni migrar**; los documentos `founding_species_profiles.json`, `major_species_profiles.json` y `dominion_borg_profiles.json` siguen siendo resúmenes, sin duplicación.
- 1 fichero de asimilación Borg (estado de personaje, conserva especie de origen).
- 5 perfiles nuevos de especie principal + 5 perfiles culturales contextuales nuevos.
- 5 perfiles nuevos reservados al DLC Delta + 5 perfiles culturales contextuales nuevos.
- 12 documentos culturales existentes conservados y enlazados.
- Lenguas: 5 existentes, 3 añadidas con fuentes (breen, kazon, talaxiano). Otras lenguas siguen como desconocidas/no catalogadas; **no se deduce el idioma desde la especie**.
- Registro de fuentes incrementado de 294 a 333 entradas (39 fuentes de pantalla, oficiales y secundarias añadidas sin borrar el legado).
- Control de disponibilidad autoral único `universe/generation/lore01_tng_content_availability_v0.1.json`; no toca `CoreRPG` ni `UE5`.

## Pruebas y compatibilidad
- Nuevo validador de rutas de especies/culturas, 25 IDs únicos, fuentes registradas, referencias lingüísticas y política de DLC; tests de no fuga de especies Delta, diáspora el-auriana, Borg en principal y portal no implementado.
- GitHub Actions `LORE-01 — TNG species & cultures (documental)`: **primera ejecución falló** por suponer que los tres perfiles culturales legados Andorian/Aenar/Human compartían un único formato; adaptado el validador sin modificar las fichas y **segunda ejecución completada correctamente**, acción ID `39025989665`. Ejecutar nuevamente en la PR y tras nuevas modificaciones.
- Compatibilidad **de autoría/diseño**: usa IDs `species_id`, referencias culturales, `language_id`, `provenance`, fechas de evidencia no transformadas en barreras de existencia y estados de pertenencia separados, coherentes con `gameplay/species/species_runtime_model.json`, `gameplay/species/species_biology_contract.json`, `gameplay/species/culture_socialization_contract.json` y generación `universe/generation/procedural_population_rules.json`.
- Compatibilidad **runtime no probada ni afirmada**. Ningún generador existente ha sido modificado para aplicar el gate DLC: es un contrato de contenido para la integración futura. La fecha de observación del episodio no es la fecha de nacimiento de una cultura ni autorización para forzar historia.

## Incertidumbres y limitaciones conservadas (no bloquean el alcance documental definido)
- Algunas fichas antiguas se apoyan en referencias `ENT_*` registradas históricamente como SCREEN_CANON aunque *Enterprise* queda fuera del corpus televisivo seleccionado. Este legado queda señalizado para auditoría posterior, **sin reescribir la política ni eliminar datos preaprobados**.
- La ficha histórica betazoide sigue apoyada en una fuente secundaria de biología; requiere futuros contrastes de afirmaciones finas con TNG cuando haya una necesidad concreta de gameplay.
- Vida media, fisiología íntima/reproductiva, idioma no demostrado, motivaciones y densidad de población de muchas especies permanecen `unknown` o `null`.
- Cultura nombrada no se adjunta automáticamente a un NPC. No se han definido rutas, puestos fronterizos, mapas, leyes, tecnologías ni eventos futuros: corresponden a B/C/D/LORE-02/03/04.
- Los perfiles son *authoring baselines*, no una simulación galáctica acabada ni certificación de conocimientos de la computadora de una nave.

## Aceptación para cierre formal
1. Revisar diferencias de la PR; confirmar cinco especies de juego principal y cinco solo DLC.
2. Confirmar CI verde tras el último commit.
3. Fusionar PR a `main` únicamente por decisión del propietario.
4. Verificar commit de fusión, contenido y validación de `main`.
5. Actualizar estado definitivo en `CONTENT_STATUS.md`, autorizar borrado de la rama y solicitar autorización expresa del propietario **antes de iniciar el apartado B**.

## Sincronización posterior con main (IDEA-0011)

Durante el trabajo apareció en `main` la idea autorizada `ideas/IDEA-0011_dlc_cuadrante_delta_portal_transwarp.md`. El contrato de disponibilidad ahora la referencia explícitamente. Incluye reserva documental de regreso por el mismo portal (opción C), interrupciones solo por hechos causales y prohibición categórica de entrada de Borg al cuadrante Alfa a través **de este portal**; no elimina Borg del canon TNG ni convierte el diseño en mecánica ejecutable. Tests de regresión lo verifican. El desarrollo técnico de la IDEA-0011 queda fuera de LORE-01.
