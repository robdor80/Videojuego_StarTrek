# Sistemas S01–S19 — catálogo conceptual formalizado; S20 incorporado después

**Fecha:** 19-11-2026 · **Ámbito:** exclusivamente SISTEMAS · **Estado:** revisión documental posterior a auditoría, sin implementación nueva.

Este directorio es la **entrada de referencia** para los 19 sistemas funcionales aprobados conceptualmente en las conversaciones de diseño del videojuego Star Trek RPG. Consolida la auditoría [AUDITORIA_SISTEMAS_S01_S19_2026-11-19](../auditorias/AUDITORIA_SISTEMAS_S01_S19_2026-11-19.md) (PR #172, fusionada), sin reescribir decisiones históricas, Lore, Planificación 1, Planificación 2, HOST, CoreRPG ni código UE5.

## Documentos

1. [Fichas S01–S10](FICHAS_S01_S10_FORMALIZADAS_2026-11-19.md) y [fichas S11–S19](FICHAS_S11_S19_FORMALIZADAS_2026-11-19.md): propósito, funciones, exclusiones, propietarios, consumidores, dependencias, criterio conceptual de aceptación y madurez.
2. [Gobierno transversal, matriz de autoridad y pendientes](MATRIZ_TRANSVERSAL_Y_PENDIENTES_S01_S19_2026-11-19.md): rutas de acciones, servicios compartidos, conflictos/duplicidades resueltos documentalmente y avisos a otras auditorías.
3. [S19 — Audio, música y ambientación dinámica](S19_AUDIO_MUSICA_AMBIENTACION_DINAMICA_2026-11-19.md): alcance ya aprobado por el autor, efectos prioritarios y música condicionada a calidad.
4. [S20 — Sistema de Voz de NPC y gestión dinámica de recursos](S20_SISTEMA_VOZ_NPC_Y_GESTION_DINAMICA_RECURSOS_2026-11-20.md): **nueva aprobación conceptual del 20-11-2026**, posterior a la revisión original. TTS CPU/GPU, presupuesto VRAM, streaming seguro y pruebas futuras; no implementación.
5. [Acta de formalización](ACTA_REVISION_S01_S19_2026-11-19.md): trazabilidad A01–A16, conservación de decisiones, estados reales y decisiones que siguen abiertas.

## Precedencia y alcance de la aprobación

- **Los 19 números S01–S19 permanecen invariantes**. En la formalización **del 19-11-2026** no se aprobaba S20. La **aprobación autoral posterior del 20-11-2026** incorpora ahora **S20 — Sistema de Voz de NPC y gestión dinámica de recursos** sin modificar los diecinueve anteriores. Véase la ficha independiente S20.
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

## Registro de madurez de los 19 sistemas — corte 19-11-2026

| Sistema | Idea aprobada | Evidencia técnica disponible | Estado integral que **NO** se atribuye |
|---|---|---|---|
| S01 — IA central | Sí | Servicio HOST IA-01 en C++ parcial documentado | No IA común conectada a todos los consumidores E2E |
| S02 — Interacción/LCARS | Sí | Diseños y contratos de ordenador/consolas | No interacción unificada UE5 certificada |
| S03 — Universo Vivo | Sí | P2 B01–B10 documentados/referencias | No simulación galáctica ejecutable certificada |
| S04 — Personaje/carrera | Sí, DEC-0022 | S04 v2 diseño; anterior F10/H06 parcial | No migración del protagonista fijo implementada/certificada |
| S05 — NPC/tripulación | Sí | Contratos y trabajo F04/F05 parcial | No autonomía total UE5 certificada |
| S06 — Relaciones | Sí | Contratos sociales/memoria | No relaciones jugables E2E certificadas |
| S07 — Misiones | Sí | Contratos narrativos/planes | No director narrativo E2E certificado |
| S08 — Navegación | Sí | Contratos y referencias de operaciones | No vuelo UE5 completo certificado |
| S09 — Combate espacial | Sí | Contratos de táctica/daños | No combate completo UE5 certificado |
| S10 — Sensores | Sí, DEC-0021 | F06/contratos/prototipos acotados | No perfil refit integrado y certificado |
| S11 — Astrometría | Sí, DEC-0023 | Diseño y contratos S11 | No holograma/sala UE5 runtime |
| S12 — Interiores | Sí | Concepto, geometría y propuestas en rama separada | No recorrido/puertas/turbolift E2E certificado |
| S13 — Planetas | Sí | Concepto y referencias de expedición | No zonas 3D de superficie certificadas |
| S14 — Holocubierta | Sí | Diseño de experiencias | No programa inmersivo UE5 certificado |
| S15 — Objetos | Sí | Contratos de tipos/instancias | No ciclo de manipulación/custodia UE5 certificado |
| S16 — Vida a bordo | Sí | Contratos de estado y ocio | No vida cotidiana jugable integral certificada |
| S17 — Minijuegos | Sí | Concepto y motores candidatos estudiados | No ajedrez/damas/póquer/mus integrados |
| S18 — Identidad/accesos | Sí, DEC-0024 | Diseño y contratos S18 | No evaluador compartido/puertas UE5 runtime |
| S19 — Audio/música | Sí | Ficha S19 + biblioteca IDEA-0002 | No gestor central de audio runtime certificado |

La madurez de cada **componente** se acredita con su fuente original; esta tabla no rebaja resultados ya probados en ámbitos acotados ni los extrapola al sistema entero.

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


## Ampliación posterior — S20 (20-11-2026)

Por instrucción expresa posterior del autor se incorpora [**S20 — Sistema de Voz de NPC y gestión dinámica de recursos**](S20_SISTEMA_VOZ_NPC_Y_GESTION_DINAMICA_RECURSOS_2026-11-20.md) como sistema **conceptualmente aprobado**, sin implementación ni proveedor TTS elegido. Su cometido específico es investigar y finalmente coordinar el presupuesto de GPU/VRAM/CPU para síntesis dinámica de voces NPC en UE5.8.2 (RTX 4070 8 GB), incluyendo evaluación de Piper, Kokoro, modelos alternativos y descargado/precarga *seguros* de recursos gráficos no visibles, **siempre tras perfilar el juego y sin prometer liberar memoria fija**.

La revisión S01–S19, su matriz, fichas y acta **permanecen como fotografía válida de 19-11-2026**. La ampliación no cambia sus estados históricos ni atribuye rendimiento/certificación a S20. **S01/HOST** continúan gobernando el acceso a IA y el texto; **S19/UE5** gobiernan la mezcla y reproducción; **S20** gobierna la **política específica de coste/síntesis de voz** y solicita medidas de gestión gráfica que **solo UE5 puede ejecutar**. La reconciliación de contratos se reserva a la implementación futura.
