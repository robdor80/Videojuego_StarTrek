# LORE-02 — Plan maestro de Tecnología, Ciencia y Medicina

**Fecha de inicio:** 2026-10-19  
**Repositorios inspeccionados:** `Videojuego_StarTrek/main` = `3479faefb9aa56980265c5b03aeab3ba3ddd083f` (LORE-01 E fusionada, PR #30); `CoreRPG/main` = `4f282863737bcd8f5add401202a9e1064c133672` (4.13 fusionada por PR #11).  
**Estado vigente (22-10-2026):** `COMPLETE` **documental** tras las PR #31, #33, #34, #35 y #36, y 11 workflows postfusión en verde. Este documento conserva los objetivos originales de investigación/autoría; **no** significa runtime, Content Pack Trek instalado ni integración UE5/Host.

## 1. Justificación y ajuste de alcance

El roadmap `docs/roadmap/gameplay_lore_readiness.md` prioriza precisamente tecnología/equipos y medicina/ciencia para generadores procedurales, formación, consolas, misiones y consultas a la computadora. Se mantiene la división A–E propuesta porque refleja dominios separados y permite puertas de revisión.

La documentación previa **ya contiene contratos**, no catálogos investigados exhaustivos:
- `lore/technology/technology_definition_contract.json`, `gameplay/technology/technology_capability_contract.json`, `gameplay/ship_operations/era_technology_matrix.json`.
- `gameplay/propulsion/propulsion_capability_contract.json`, `gameplay/ship_operations/power_allocation_model.json`, `gameplay/transporters/transporter_operation_contract.json`, `gameplay/ship_operations/consoles/sensors/`, `gameplay/ship_operations/sensor_resolution/`.
- `lore/equipment/`, `lore/medicine/medical_capability_contract.json`, `gameplay/medical/medical_state_model.json`, `gameplay/medical/species_medical_hooks.json`, `lore/science/scientific_domain_contract.json`, `gameplay/science/sensor_analysis_model.json`.
- Academias, manual de sensores, perfiles de especie y arte existente son **consumidores/fuentes de contexto**, no réplicas que haya que reescribir.

Los documentos maestros F00–F15 y `ESTADO_GLOBAL.json` describen **madurez/implementación** con históricos explícitos; LORE-02 no actualiza a mano un estado `CORE_INTEGRADO`. La PR narrativa ST-NAR-00 #24 permanece ajena.

## 2. Orden ejecutivo y entregables

| Bloque | Entrega verificable | No implica |
|---|---|---|
| **02-A** Tecnología de naves y estaciones | Catálogo cualitativo con sistemas, variantes y dependencias; anclas por era/matriz; contexto civilizatorio y de clase; fallos; firmas, autorizaciones y pruebas | Simular motores, inventar MW/alcance o modificar modelos de nave |
| **02-B** Equipamiento personal y especializado | Fichas de dispositivos, perfiles de uso por puesto, disponibilidad/permiso, desgaste y riesgos; relación con A y Academia | Equipamiento 3D, inventario ejecutable o balance de armas inventado |
| **02-C** Medicina y xenobiología | Catálogo clínico prudente, observación→hipótesis→diagnóstico, diversidad biológica revisada, recursos/privacidad/criterios de actuación; referencias A/B/LORE-01 | Diagnóstico garantizado, protocolo médico real ni sustitución de estado clínico Core |
| **02-D** Ciencia, investigación y fenómenos | Fenómenos, procedimientos de toma de datos y análisis con incertidumbre, trazabilidad observacional y competencias por puesto | Omnisciencia de sensores, anomalías guionizadas o poderes arbitrarios |
| **02-E** Auditoría cruzada | Índices A–D, integridad referencial, matriz de contradicciones, escenarios y lagunas; prueba de regresión LORE-01 | Cierre automático de LORE-02 o integración de los contenidos en UE5/Core |

Cada bloque deberá contar con rama/PR propia o, si se documentan subincrementos por tamaño, una PR por bloque claramente delimitado y con validación independiente. Nunca fusionar ni borrar ramas sin permiso.

## 3. Orden de fuente y procedencia

Se aplican `sources/canon_policy.md` y `sources/provenance_policy.md`: pantallas retenidas → referencia oficial → material licenciado → secundarias. `INFERRED` y `GAME_ADDITION` se distinguen de `SCREEN_CANON`. Cada afirmación operativa debe anotar fuente o declarar que es hipótesis/criterio del videojuego, su nivel de confianza y cómo invalidarla.

No inferir datos de rendimiento, fechas exactas, dosis médicas, rangos, reglas universales, límites mágicos, patrones clínicos ni disponibilidad de una tecnología por mero conocimiento de su existencia. Ausencia en una matriz o un catálogo significa **dato no registrado**, no necesariamente `unavailable`. Fuentes secundarias documentan candidatos y requieren contraste con pantalla para cerrar afirmaciones fuertes.

## 4. Epocas, disponibilidad y excepciones

Anclas de `gameplay/ship_operations/era_technology_matrix.json`: `pike_2259_2264`, `kirk_tos_2265_2269`, `kirk_films_2278_2293`, `tng_2364_2370` y `late_24c_2371_2378`. No rellenar huecos entre periodos ni suponer que la lista es exhaustiva. Separar:
1. conocimiento/historia accesible al consultante;
2. techo tecnológico por era y operador;
3. equipamiento instalado y refits de clase/nave/estación;
4. estado real (potencia, integridad, personal, suministros) y autorización;
5. observación y conocimiento **del actor**, distintos de verdad del mundo.

Una excepción real exige evidencia registrada y localización/actor/fecha adecuados. La tecnología excepcional del diseño creativo (por ejemplo futuras prestaciones de la clase Valhalla) no se introduce como dotación universal ni en una fecha no aprobada.

## 5. Frontera CoreRPG / Star Trek / IA / UE5

Se verificó `CoreRPG/main` 4.13 integrada. Core ofrece content pack JSON 0.1.0, catálogo tipado, estado de mundo/población, persistencia, Knowledge/Visibility, ActionEngine/Simulation y ContextBuilder para una vista autorizada. **No** interpreta automáticamente fichas Trek ni implementa reglas específicas de medicina, energía, torpedos, warp, inventario, órdenes de mando, tareas complejas o integración UE5. La 4.13 de Nimroel prueba un pack particular, no habilita un adaptador Star Trek.

- **LORE-02**: evidencia, limitaciones, taxonomías y datos de autoría, no estado mutante.
- **Star Trek gameplay**: contratos y reglas específicas cuando se aprueben y se integren.
- **CoreRPG**: identidad, verdad/estado, acciones y conocimiento con autoridad exclusiva.
- **UE5/Host**: representación, autorizaciones específicas, interacción y presentación.
- **IA**: contextualización o propuestas, nunca confirmación de mediciones/cura/reparación por texto; propuesta revalidada por Host y Core.

No modificar `CoreRPG` para resolver lagunas narrativas ni fingir que un JSON de LORE-02 cumple el manifest/schema Content Pack.

## 6. Regresiones y puertas de cierre

- Referencias a fuentes y rutas existentes; IDs únicos y estables; sin mezcla arbitraria de identificadores de definición con IDs de instancias.
- Disponibilidad por era referenciada desde **una sola matriz** siempre que exista; sin copiar su estado como segunda verdad.
- Catálogos explican limitación/fallo, procedencia, consumidor y grado de incertidumbre.
- Escenarios negativos: sistema no instalado, equipo sin potencia, personal no autorizado, interferencia, conocimiento insuficiente, trasvase de época, fallo parcial, peligro clínico, encuentro reservado Delta.
- LORE-01 A–E preservada, sin activar especies `kazon`, `ocampan`, `talaxian`, `vidiian`, `hirogen` ni el portal de IDEA-0011.
- Comprobaciones locales + GitHub Actions antes de recomendar revisión; ausencia de CI verde equivale a **pendiente**.
- Sólo el usuario autoriza merge. Sólo después de fusionar todos los bloques, auditoría E y comprobación en `main` marcar LORE-02 `COMPLETE`.

## 7. Riesgos conocidos y decisiones pendientes

1. Hay contratos de fundación pero poca investigación dedicada en `lore/technology`, `lore/equipment`, `lore/medicine` y `lore/science`. Completar sustancia sin duplicar datos operativos.
2. Las cinco anclas de matriz no describen todas las plataformas, especies ni años. No extrapolar a clases o civilizaciones sin evidencia.
3. La investigación médica interespecie exige diferenciación entre hechos vistos, inferencias y restricciones sin convertir fisiología en estereotipo.
4. El contenido Borg/Delta puede estudiarse como antecedente histórico sin habilitar encuentros, tránsito ni generación.
5. El avance Core 4.13 permite planificar futuras pruebas de adaptación, no declarar que existe compatibilidad de datos o ejecución UE5.
6. Las decisiones creativas que cambien la cronología o capacidades de la Valhalla, el alcance Delta o la experiencia jugable se elevan al usuario.

**Criterio de suficiencia:** un bloque documental puede cerrarse con incertidumbres explícitas y bien registradas; no necesita catálogo infinito. Lo que no puede cerrar es una contradicción bloqueante, una procedencia inventada ni una prestación no fundamentada.
