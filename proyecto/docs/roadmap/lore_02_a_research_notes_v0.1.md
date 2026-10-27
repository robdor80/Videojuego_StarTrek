# LORE-02 A — Investigación y límites de tecnología de naves/estaciones (primer corte)

**Fecha:** 19-10-2026. **Estado:** `IN_PROGRESS`. **No** es cierre de LORE-02 A ni runtime.  
**Datos:** [14 fichas documentales](../../../mundo/lore/technology/ship_station_catalogue_v0.1.json) y [14 escenarios negativos](../../../mundo/lore/technology/ship_station_cases_v0.1.json).  
**Normas:** `mundo/sources/canon_policy.md`, `mundo/sources/provenance_policy.md`, `sistemas/gameplay/ship_operations/era_technology_matrix.json`.

## 1. Método de evidencia y coherencia

Se partió del estado real de `main`, incluyendo LORE-01 E fusionada en PR #30. La matriz tecnológica existente es la fuente de verdad **editorial** para estados de época; cada ficha remite a claves exactas de la matriz y reproduce sólo una disponibilidad derivada y comprobable. No se abre una matriz alternativa. Las 14 fichas no son las 14 únicas tecnologías de Star Trek: son un primer conjunto priorizado con ancla estructural existente.

Fuentes ya registradas: `MA_WARP_DRIVE`, `MA_DEFLECTOR_SHIELD`, `MA_LONG_RANGE_SENSOR_SCAN`, `MA_TRANSPORTER`, `MA_REPLICATOR`, `MA_FOOD_SYNTHESIZER`, `MA_HOLODECK`, `MA_BIONEURAL_GEL_PACK`, `MA_QUANTUM_TORPEDO`, `MA_TACTICAL_STATION`, `MA_ENGINEER`. Son fichas **RELIABLE_SECONDARY** de búsqueda/contraste; no equivalen a prueba técnica escena a escena. Los episodios registrados `TNG_ENCOUNTER_AT_FARPOINT`, `DS9_TAKE_ME_OUT_TO_THE_HOLOSUITE`, `VOY_THE_KILLING_GAME` y `VOY_CARETAKER` aportan anclas audiovisuales puntuales, tampoco una fórmula de rendimiento general. Las restricciones de jugabilidad descritas son principalmente **INFERRED**, no hechos de tecnología demostrados en todos los casos.

La documentación oficial del episodio SNW «A Space Adventure Hour» (<https://www.startrek.com/news/recap-304-space-adventure-hour>) describe pruebas holográficas durante Pike y una recomendación de no instalarlas como equipamiento de nave activo en ese momento. Es una referencia oficial **de investigación pendiente de incorporar formalmente al registro de fuentes y cotejar con el episodio**; no se modifica con ella la matriz de época ni se afirma que todos los buques de Pike careciesen de simulación.

## 2. Lectura por subsistema

### Propulsión y energía

**Warp:** distinguir capacidad histórica de la civilización, instalación efectiva de nave, estado del motor y maniobra admitida por la navegación. Sin modelo de clase y condiciones ambientales no puede extraerse un factor warp, velocidad, consumo o ETA constante. El contrato `sistemas/gameplay/propulsion/propulsion_capability_contract.json` ya gobierna las entradas para una resolución futura.

**Impulso, maniobra y redes energéticas:** están documentados de manera transversal, pero no cuentan todavía con perfiles completos y trazables por era en la matriz. La ausencia de claves de impulso para determinados perfiles tardíos NO demuestra ausencia de motores. La distribución, generación, almacenamiento, pérdidas y prioridades de red deberán estudiarse con referencias propias; no se crea un reactor universal de estaciones. `sistemas/gameplay/ship_operations/power_allocation_model.json` conserva las invariantes de asignación.

### Protección, sensores y señales

**Escudos:** su disponibilidad no implica capacidad defensiva instantánea idéntica en cualquier nave; pérdidas de potencia y daños del emisor cambian resultados. En transportadores se consultarán conflictos entre campos/escudos, sin decretar que toda configuración prohíba la transferencia en todos los casos.

**Sensores:** separar detección de clasificación, clasificación de identificación, e identificación de conocimiento público del objetivo. En `sistemas/gameplay/ship_operations/sensor_resolution/` y el manual de sensores ya existen modos, resultados, probabilidades de detección referenciales y restricciones. LORE-02 añade explicación y procedencia, no un segundo algoritmo de escaneo. La interferencia puede disminuir confianza y generar contradicciones; no debe causar «conocimiento mágico» de la IA.

**Comunicaciones subespaciales:** faltan fichas individuales y la matriz no aporta cobertura comparable. Los contratos ya reconocen comunicaciones/secretos, pero no justifican alcance o latencia fijos; esta investigación permanece pendiente.

### Transporte, fabricación y simulación

**Transportador:** un traslado requiere plataforma habilitada, bloqueo, energía, seguridad y autorización. No puede darse por realizado sin mutación aprobada por CoreRPG. Separar personal de transporte punto a punto; en épocas antiguas la falta de entrada para una variante equivale a investigación pendiente y no a demostración de imposibilidad absoluta.

**Sintetizadores de alimentos y replicadores:** no son equivalentes entre Kirk y TNG. En 2370s existen límites de recursos, patrones, autorización y equipamiento; no se deduce fabricación ilimitada ni que el software de la computadora pueda crear directamente un objeto de inventario.

**Holocubiertas:** empleadas para formación, ocio e investigación. Una simulación no altera por sí misma la localización galáctica ni da conciencia/condición de persona a todos los hologramas. La seguridad, fallos o derechos de un holograma requieren contexto y reglas adicionales. El hecho de que exista una demostración durante Pike no hace el equipo normal en toda la Flota.

### Computación, protección táctica y maniobras

**Computadoras isolineales y sistemas bioneurales:** una definición tecnológica no incluye biografía, visibilidad de expedientes ni permiso de ejecutar acciones; CoreRPG 4.9/4.12 protege la información mediante proyecciones autorizadas. Los sistemas bioneurales son específicos de determinadas plataformas, no el destino universal de toda nave de 2371.

**Fáseres, torpedos fotónicos, torpedos cuánticos:** distinguir disponibilidad de época, instalación y munición real. Los cuánticos llegan a equipos selectos en el periodo tardío, no a todos los buques por actualización automática. No se inventan daños/alcances/cadencias para rellenar los catálogos. El inventario y la resolución táctica pertenecen a contratos de gameplay futuros, no a estas fichas.

**Haz tractor:** disponibilidad en matriz no prueba que cualquier objetivo pueda ser remolcado, ni concede capacidad infinita. Se requieren condiciones de instalación, suministro, compatibilidad, fijación del objetivo y posibles efectos colaterales.

### Particularidad de las estaciones

Naves y estaciones comparten tecnologías, pero **no el mismo diseño físico ni redundancias**. La referencia de una tecnología para Starfleet no autoriza instalarla indiscriminadamente en centros sanitarios, puestos fronterizos, relés, astilleros o estaciones civiles. Falta investigar el ciclo de mantenimiento/reparaciones, personal y capacidad de estaciones; el resultado irá vinculado a los modelos de instalaciones existentes. No se asumirán cifras de tripulación, camas, reactores o comunicaciones.

## 3. Matriz de responsabilidades (no duplicación)

| Fuente de verdad | Qué aporta | Qué NO crea LORE-02 |
|---|---|---|
| `sistemas/gameplay/ship_operations/era_technology_matrix.json` | Estado editorial por época | Otra matriz independiente |
| `mundo/lore/starships/classes/` | Clasificación, diseños/capacidades de clases | Nuevas especificaciones de clase por intuición |
| `sistemas/gameplay/ship_operations/power_allocation_model.json` | Reglas energéticas | Watts ni reservas ficticias |
| `sistemas/gameplay/ship_operations/sensor_resolution/` | Resolución observacional y estructura de registros | Sensor de «verdad absoluta» |
| `sistemas/gameplay/transporters/transporter_operation_contract.json` | Flujo de transferencia condicionado | Duplicación y teletransporte por relato |
| `mundo/lore/technology/ship_station_catalogue_v0.1.json` | Investigación y explicación de capacidades con fuente | Estado vivo, instalación o autoridad |
| `CoreRPG` 4.13 | Catálogo genérico, estado, observación, acciones | Reglas Trek ya instaladas |
| UE5/Host | Presentación/consolas/permisos y puente de integración | Una segunda simulación autoritativa |

## 4. Ocho lagunas de investigación abiertas

**A-G01** completar impulso/maniobra por época; **A-G02** generación y distribución de energía; **A-G03** diferenciar deflector de navegación y escudos; **A-G04** comunicaciones y latencia; **A-G05** soporte vital, hábitat y estaciones; **A-G06** perfiles tecnológicos de otras civilizaciones; **A-G07** excepciones de diseño Valhalla y refits; **A-G08** escenarios de estación, industria y transporte civil.

Estas lagunas son incompatibles con declarar A `COMPLETE`, pero no con publicar un primer corte `IN_PROGRESS` que ya protege invariantes y deja el alcance verificable.

## 5. CoreRPG revisado y fronteras reales

`CoreRPG/main` = `4f282863737bcd8f5add401202a9e1064c133672`; PR #11 de 4.13 fusionada el 19-10-2026. Las fases 4.9–4.12 permiten conocimiento de observador, acciones estructurales y contexto autorizado. La 4.13 prueba la carga de contenido Nimroel concreto sin implementar automáticamente su semántica ni una vertical Star Trek. Por tanto **las fichas A no se entregan como Content Pack compatible**, no añaden definiciones a WorldState y no modifican `CoreRPG`.

## 6. Puerta de revisión del primer corte

Criterios comprobables desde herramientas: JSON legible, IDs únicos, referencias reales, procedencia cruzada, claves por época verificadas contra matriz, disponibilidades derivadas, estado no ejecutable, casos negativos de autoridad y Delta, regresión LORE-01 E. La CI de esta rama deberá ejecutarse; hasta entonces todo resultado de integración queda `PENDIENTE`.

**Cierre completo futuro de A:** las ocho lagunas deberán resolverse mediante evidencia y datos suficientes, o quedar justificadamente excluidas del alcance con referencias; se añadirá una revisión de tecnología no federada, instalaciones y contradicciones canónicas. Se necesita revisión humana de la PR antes del merge. Ningún cambio creativo sustancial ha sido aprobado automáticamente.
