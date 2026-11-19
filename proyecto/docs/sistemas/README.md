# Sistemas S01–S19 — catálogo conceptual formalizado

**Fecha:** 19-11-2026 · **Ámbito:** exclusivamente SISTEMAS · **Estado:** revisión documental posterior a auditoría, sin implementación nueva.

Este directorio es la **entrada de referencia** para los 19 sistemas funcionales aprobados conceptualmente en las conversaciones de diseño del videojuego Star Trek RPG. Consolida la auditoría [AUDITORIA_SISTEMAS_S01_S19_2026-11-19](../auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md) (PR #172, fusionada), sin reescribir decisiones históricas, Lore, Planificación 1, Planificación 2, HOST, CoreRPG ni código UE5.

## Documentos

1. [Fichas S01–S10](FICHAS_S01_S10_FORMALIZADAS_2026-11-19.md) y [fichas S11–S19](FICHAS_S11_S19_FORMALIZADAS_2026-11-19.md): propósito, funciones, exclusiones, propietarios, consumidores, dependencias, criterio conceptual de aceptación y madurez.
2. [Gobierno transversal, matriz de autoridad y pendientes](MATRIZ_TRANSVERSAL_Y_PENDIENTES_S01_S19_2026-11-19.md): rutas de acciones, servicios compartidos, conflictos/duplicidades resueltos documentalmente y avisos a otras auditorías.
3. [S19 — Audio, música y ambientación dinámica](S19_AUDIO_MUSICA_AMBIENTACION_DINAMICA_2026-11-19.md): alcance ya aprobado por el autor, efectos prioritarios y música condicionada a calidad.
4. [Acta de formalización](ACTA_REVISION_S01_S19_2026-11-19.md): trazabilidad A01–A16, conservación de decisiones, estados reales y decisiones que siguen abiertas.

## Precedencia y alcance de la aprobación

- **Los 19 números S01–S19 permanecen invariantes**; no se aprueba S20.
- **Autoría creativa:** las aprobaciones conversacionales prevalecen dentro de su ámbito, y las decisiones explícitas posteriores DEC-0020–0024 prevalecen solo en lo que modifican. Este documento formaliza límites y referencias; no revoca decisiones creativas ni convierte recomendaciones técnicas de la auditoría en aprobaciones autorales.
- **Campaña vigente:** proyecto personal de un jugador, continuidad propia, protagonista único híbrido humano-vulcano descendiente de Khan (DEC-0022), Academia desde 2383, USS Enterprise NCC-1701-D Galaxy reconstruida mediante Proyecto Valhalla (DEC-0020; **Valhalla es el programa, no la clase/nave**). La Enterprise-D no se adquiere ni se manda automáticamente; depende de vacante, mérito y autoridad.
- **Sensores del refit:** supremacía sensorial con lecturas ordinarias completas/prácticamente inmediatas cuando el equipamiento está instalado, operativo y el fenómeno es observable (DEC-0021). Ni fallo aleatorio de escaneo ni capacidades automáticas por escribir un documento.
- **Reglas de producto:** aventura predominantemente tranquila, emergencias excepcionales, experiencia Star Trek en castellano, interfaz LCARS y 3D premium sin sacrificar calidad por cantidad. El juego no requiere cuentas/servidores/multijugador. Las voces TTS deben buscar coste adicional cero y bajo impacto CPU/GPU/VRAM; clonación de celebridades no obligatoria.
- **No cambiar los otros pilares aquí:** inconsistencias de F10/F11, P2, Lore y HOST quedan registradas para sus auditorías independientes.

## Jerarquía de autoridades (no intercambiables)

| Capa | Responsabilidad |
|---|---|
| **CoreRPG** | Estado verdadero del mundo, identidad persistente, tiempo canónico, acciones admitidas y persistencia general; jamás inferir hechos de un texto de IA ni una animación. |
| **Reglas y dominios Star Trek / Fxx** | Semántica de Flota, rangos, acceso, doctrina sensorial, misión, carrera, órdenes y restricciones específicas; sin segunda copia en HOST. |
| **HOST** | Sesiones, encaminamiento, composición de servicios, adaptación de mensajes, ejecución de integraciones y cola/seguridad de IA; no crea una autoridad de mundo paralela. |
| **Unreal Engine 5** | Escena 3D, input, LCARS, animaciones, sonido, efectos y control del jugador; presenta el resultado autorizado, no inventa permisos ni estado. |
| **LORE** | Identidad, continuidad, marco narrativo y canon autoral; no convierte una posibilidad futura en hecho de WorldState. |
| **IA central S01 mediante HOST** | Lenguaje, diálogo y análisis de datos permitidos, bajo demanda; nunca es autoridad para crear/validar por sí misma acciones, identidades, permisos o sensores. |

## Lectura correcta del estado

**Aprobado conceptualmente** no equivale a **diseño técnico validado**; **contrato documentado** no equivale a **implementación**, **código nativo parcial** no equivale a **integración UE5**, y **prueba reportada** no equivale a **aceptación E2E certificada**.

Las fichas indican expresamente **evidencia localizada y madurez máxima demostrada en su alcance**, no un porcentaje de sistema completado. A fecha de esta formalización **ningún S01–S19 queda certificado integralmente como experiencia CoreRPG + HOST + UE5 por esta revisión**. Existen componentes parciales y algunas pruebas ajenas a una certificación transversal del sistema; se conservan sin inflar su alcance.

La fuente que prevalece para cada avance técnico futuro es una evidencia identificable (artefacto/versionado, prueba realmente ejecutada, entorno, resultado, revisión), conforme a [CRITERIOS_DE_CIERRE](../roadmap/master/CRITERIOS_DE_CIERRE.md). No asumir que «Fxx completada» implica «Sxx completo».

## Fuentes principales

- [Decisiones autorales vigentes](../decisions/README.md), especialmente DEC-0020, DEC-0021, DEC-0022, DEC-0023 y DEC-0024.
- [Auditoría original S01–S19](../auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md).
- [S04 — protagonista v2](../../../sistemas/gameplay/character_creation/S04_PROTAGONISTA_IDENTIDAD_CARRERA_v2.md).
- [S11 — astrometría](../../../sistemas/gameplay/astrometrics/README.md).
- [S18 — accesos](../../../sistemas/gameplay/access_control/README.md).
- [IA-01 HOST](../../../sistemas/ai/HOST_AI_SERVICE_IA01.md) y [decisión OpenAI](../../../sistemas/ai/OPENAI_RUNTIME_DECISION_2026-11-15.md).
- [Biblioteca musical personal](../../ideas/IDEA-0002_biblioteca_musical_personal.md).
- [Criterios de cierre de proyecto](../roadmap/master/CRITERIOS_DE_CIERRE.md).

**No ejecutado por esta formalización:** código, CI, compilación, juego UE5, mediciones en MSI, cambio de contratos, migración de guardados o integración de IA.
