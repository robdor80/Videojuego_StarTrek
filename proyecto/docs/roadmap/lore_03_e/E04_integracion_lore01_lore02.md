# E04 — Cruce LORE-01, LORE-02 y fases F00–F15
## Reglas de autoridad de datos
| Propietario previo | Qué aporta a LORE-03 | Qué no se debe duplicar |
|---|---|---|
| LORE-01D | 40 hechos, diplomacia, tratados y referencias de facción | hechos, tratados, guerras declaradas |
| LORE-01A/B/C/E | sociedades, atlas y límites de conocimiento, cultura, contactos | gobiernos, estereotipos, cartografía |
| LORE-02A/B | matriz tecnológica, nave/clase/equipo y restricciones de época | capacidades asumidas por cinematografía o GLB |
| LORE-02C | medicina, procedimientos, evidencia clínica | diagnósticos o curaciones retroactivas obligatorias |
| LORE-02D | ciencia, fenómenos y legado profesional | descubrimientos/instalaciones sin investigación causal |
| LORE-02E | auditoría previa de integración y reservas | nuevo catálogo de compatibilidad redundante |
| F10/F11 | calendario Academia, cualificación y carrera | graduación, ascensos o destinos forzados |
| F12/F13 | servicio, LOD, mundo dinámico, identidad y consecuencias | segundo motor de simulación histórica |
| F00–F09, F14/F15 | reglas de estados, interfaces, validación y preparación | inferencia de funcionalidad real UE5/CoreRPG |

## Discrepancia transversal prioritaria
CONTENT_STATUS.md aún describe arriba un alcance histórico de tres eras. La decisión propietaria posterior en proyecto/docs/decisions/playable_eras.md y la sección LORE-03 de CONTENT_STATUS.md ordenan solo tng_ds9_voyager. Pike/Kirk conservados únicamente como fuentes históricas. Migración no destructiva de selectores, documentación genérica y consumidores futuros: deuda **pendiente**, no nueva decisión.

## Otra deuda constatada
Algunas notas de B y documentación de CI F07 registran una regresión de inventario de activos UE5 relacionada con estados de evidencia modificados. Es ajena a LORE-03; no se falsean expectativas antiguas para hacerla pasar. Validaciones de E se acotan a integridad histórica, no certifican inventario F07.

## Revisión directa del estado F00–F15
Se han leído los README de proyecto/docs/roadmap/master/fases/F00 a F15 en el main observado el 27-10-2026. Resultado por naturaleza de evidencia:

| Grupo | Estado documental declarado en su README | Consecuencia para LORE-03 |
|---|---|---|
| F00 | cierre organizativo | preservar trazabilidad del árbol y no redefinir repositorio |
| F01 | diseño cerrado pero acta anterior conserva tres eras | prima decisión posterior de 2026-10-23 de única era TNG |
| F02 | EN_CURSO y contrato Core/Host real no certificado | no deducir interoperabilidad de una PR documental |
| F03–F06 | EN_REVISION, pruebas de referencia; integración Core/UE5 pendiente | historia, autoridad, órdenes, conocimiento y sensores no se asumen ejecutables |
| F07 | EN_REVISION, evidencia UE5 local parcialmente pendiente de cotejo | material 3D no da por instanciadas naves ni situaciones históricas |
| F08 | planificada/pausada | no confundir vertical slice con producto terminado |
| F09 | planificada; 16 familias de consolas como diseño | ausencia de prueba de interconexión operativa |
| F10 | planificada; Academia de cuatro años para futura realización | no confundir diseño curricular con paso automático 2383–2387 en partida |
| F11 | planificada; carrera/flota para futura realización | Valhalla accesible como posibilidad, sin destino ni comisión exacta |
| F12 | planificada; vida a bordo, NPC y LOD | sin prueba real de identidad social persistente a escala |
| F13 | planificada; universo dinámico, bloques 4–10 pendientes | bloque 1–3 de simulación de referencia no ejecuta toda galaxia en CoreRPG |
| F14 | planificada; producción audiovisual/NAP | evidencias de recursos y licencias, no funcionalidad histórica |
| F15 | planificada; QA, beta y distribución | CI documental nunca equivale a certificación del juego |

Se respetan las etiquetas del propio repositorio: que los planes F08–F15 estén documentados no los convierte en funcionalidad verificada. Este es un **cotejo de controles README y contratos**; no una revisión de cada escena UE5 o de cada asset. La coexistencia de textos heredados no altera la regla de precedencia de decisiones autorales.
