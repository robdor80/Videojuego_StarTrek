# Planificación 2 · Bloque 7 — Fenómenos, anomalías y arqueología procedural

**Fecha:** 12/11/2026. **Alcance:** contrato Trek, generador/simulador de referencia Python determinista, fixture sintético, pruebas adversariales y CI. **Nivel de cierre objetivo:** `REFERENCE_COMPLETE`; **no** CoreRPG, HOST, sensores físicos UE5 ni planificación galáctica en producción.

## Propósito

El universo preexiste a sus observadores. En sectores, lunas y planetas puede haber estructuras antiguas, campos de radiación, perturbaciones espaciales o restos de civilizaciones incluso cuando jamás llegue la Enterprise-D, una nave NPC o el jugador. Una lectura permite adquirir conocimiento parcial, no instanciar realidad; un yacimiento conserva su historia y custodia hasta que hechos autorizados la modifiquen. Un problema científicamente interesante no implica una misión o desastre. Los capitanes reciben informes y toman decisiones de riesgo/ética; la profundidad de investigación es opcional y también puede correr a cargo de equipos NPC.

## Auditoría y no duplicación

Se reutilizan expresamente:

- `proyecto/docs/decisions/authoritative_observable_universe.md`: verdad anterior a observación, conocimiento individual, persistencia e IA sin autoridad.
- `sistemas/universe/generation/anomaly_temporal_state_contract.json`: familias, causación, temporalidad y no reescribir historia.
- `sistemas/universe/generation/detectable_signature_model.json`, `observable_entity_model.json`: entidad/señal vs sensor/observador.
- `mundo/lore/science/lore02_d_phenomena_atlas_v0.1.json` y `lore02_d_research_cases_v0.1.json`: tipologías editoriales, propiedades **NO** universales ni homologadas para runtime.
- `proyecto/docs/decisions/lore_02_d_author_decisions_v0.1.md`: no viajes temporales jugables, agujeros de gusano excepcionalmente raros y anclados, Omega reservado a misión especial de autor.
- `proyecto/docs/roadmap/procedural_science_technology_discovery_plan_v0.1.md`: B06 trabaja hipótesis, ciencia y tecnología; B07 aporta sujetos y procedencia, no inventa innovaciones.
- B01–B05: identidad/semillas, civilizaciones históricas, custodias, fronteras, economía e historia aceptada. F06 valida lecturas; F11/Host autoridad; CoreRPG posesión y eventos; UE5/NAP representación.

Los directorios de anomalías y exploración existentes están reservados, no constituyen simulador ya operativo. No se trasladan ni sobrescriben datos históricos, Blender, PBR, original de la Enterprise-D ni archivos UE.

## Paquetes aprobados

| ID | Responsabilidad y decisión | Aceptación de referencia |
|---|---|---|
| PA001 | Verdadero propietario CoreRPG; Python no escribe el runtime | Sin doble escritor ni mutaciones externas |
| PA002 | Fecha, corte de campaña, canon y regiones reservadas | Un ancla canónica no se rerollea |
| PA003 | Slots permanentes, ID por campaña y azar controlado | Replay/orden/LOD no alteran resultados |
| PA004 | Localización astrográfica existente y causa previa | Sin entidad nacida de proximidad |
| PA005 | Campos estelares, objetos y fenómenos astronómicos | Familias y condiciones explícitas |
| PA006 | Perturbación espacial/subespacial, gravedad y radiación | Sin peligro inherente obligatorio |
| PA007 | Temporal/dimensional/agujeros de gusano/Omega | Fuera del generador ordinario |
| PA008 | Señal física distinta de medición instrumental | Fact de sensor aceptado, instrumento y autor |
| PA009 | Fases físicas y degradación en el tiempo | Sólo transición con causa aceptada |
| PA010 | Ruinas, pecios, asentamientos antiguos, estratigrafía | Origen cultural real, sin poblaciones inventadas |
| PA011 | Hallazgos con artefacto/estrato/procedencia | Sin datación infalible ni tecnología gratuita |
| PA012 | Custodia, preservación, derechos, Primera Directriz | Excavación sin permiso rechazada |
| PA013 | Contradicciones, interpretaciones limitadas y dudas | Dos actores e instrumentos independientes |
| PA014 | Investigadores NPC, transmisión, permisos y PADD | Conocimiento sin telepatía ni filtraciones |
| PA015 | Referencias para historia/ciencia/consecuencias | Ninguna guerra, crisis, misión ni obra automáticas |
| PA016 | Replay, separación de partidas, migraciones | Hash, idempotencia y errores atómicos |
| PA017 | Fixture doble y tests adversariales | Positive/negative tests + regresiones |
| PA018 | Evidencia CI, documentación, frontera con B08 | Cierre referencia, runtime sigue pendiente |

## Reglas de generación física

1. El contexto `campaign_id`, la semilla galáctica, el **slot estable** y el perfil de generador definen un resultado reproducible. `rarity_bps` es una probabilidad de laboratorio (0–10000), no un porcentaje oficial de fenómenos Trek; no existen rerolls por escanear, descargar/reabrir el nivel o cambiar nave/cámara.
2. Un slot se vincula a una localización previamente existente. Debe poseer un hecho causal `formation` o `archaeological_origin` aceptado, fechado **antes de la materialización**. Puede haberse formado después del corte de campaña por una causa mundial aceptada; en un yacimiento antiguo se debe acreditar además su propio contexto histórico. Si el slot queda vacío por rareza, la decisión también se registra. En runtime sólo CoreRPG podrá aceptar o materializar el resultado.
3. Las familias ordinarias referenciadas son `astronomical`, `spatial`, `subspace`, `gravimetric`, `radiation`, `ruin`, `derelict` y `artifact_field`. Un fenómeno natural puede ser inofensivo, latente, intermitente, erróneamente interpretado o peligroso **según su caso**, no por tipología universal.
4. Anomalías temporales, dimensionales, agujeros de gusano transitables y excepciones Omega **no** se crean al azar por este adaptador; requieren contratos excepcionales y anclas/autoría validadas. No se crean rutas ni se hace viaje temporal jugable.
5. Formación antigua y materialización técnica son conceptos distintos: el fixture puede reconocer hoy una entidad física formada siglos atrás sin que haya sido creada por un descubrimiento. En producción el inventario universal existe antes del primer escaneo.
6. Una entidad materializada nunca pierde identidad por LOD, cámara, recarga o upgrade de reglas. Migraciones explícitas; ninguna actualización puede alterar un pasado ya aceptado.

## Arqueología, conservación y hallazgos

Una ruina tiene referencia espacial, una línea cultural/histórica **proveniente de hechos aceptados** y un custodio del sitio, si existe. Debe haber una cadena de procedencia desde el estrato arqueológico hasta el objeto registrado. La detección de cerámica, tecnologías desconocidas o restos biológicos **no** demuestra automáticamente edad, civilización, tecnología utilizables ni causa de extinción.

El equipo necesita permiso válido de custodia o autoridad aplicable, plan de preservación y evidencia aceptada para registrar una excavación. Esta referencia **no modifica el inventario físico**, ni inventa propiedad sobre bienes, ni legitima intervenir una sociedad prewarp. Donde la Primera Directriz, la propiedad o la soberanía sean inciertas, se propone esperar una decisión autorizada en vez de resolverla por la propia IA. Caben especies/culturas extinguidas, registros contradictorios, falsificaciones y contextos indeterminados; las identificaciones culturales nunca dependen sólo de especie.

## Vida del fenómeno y experiencia jugable

- `dormant → active → quiescent/spent`: cambios de fenómeno y actividad aceptados en ticks.
- `stable_ruin → eroding_ruin → lost_ruin`: erosión progresiva, expolio o degradación causal; B07 registra sólo el estado de su propio objeto.
- Las señales observables son **hechos físicos**; una lectura F06 determina si el observador recibe traza, parcial, corroboración, contradicción o nada. Ninguna lectura crea la anomalía.
- Un oficial científico puede mantener hipótesis rivales, iniciar nuevas exploraciones y reconocer incertidumbre. El contrato de laboratorio exige dos lecturas positivas de observadores **e instrumentos** independientes para una interpretación apoyada, nunca certeza universal.
- Un capitán puede pedir análisis, ordenar aislamiento, solicitar salvaguardas arqueológicas, contactar a autoridades o marcharse. Ninguna elección dispara automáticamente B08 (crisis), B09 (misión) ni un avance B06.
- La experiencia se distribuye según permisos, registro de observación y mensajes entregados a tiempo. El PADD externo, NPC y el ordenador de la nave **consumen una proyección**, no acceso indiscriminado al `ground_truth`.
- Los objetos de B07 pueden alimentar **candidatos** de registro B05, investigación B06, crisis B08 y misiones B09, pero la transformación real y sus controles permanecen en sus respectivos propietarios.

## Caso sintético verificable

El fixture aporta una perturbación subespacial en un sector y un yacimiento lunar protegido. Ambos existen por hechos anteriores al inicio. Los jugadores no son necesarios: un generador de referencia materializa sus identidades; dos observadores y dos instrumentos obtienen lecturas aceptadas; hay hipótesis apoyadas pero no certeza; una causa física activa la perturbación; una arqueóloga excava con custodia y conservación y registra un artefacto de estrato conocido; los hallazgos llegan a otro NPC sólo tras una comunicación. Ningún contenedor, moneda, nave, clasificación tecnológica, misión ni planeta se altera.

**Límites explícitos de la prueba:** los hechos `accepted` del fixture son **declaraciones sintéticas**, no evidencias de firma/CoreRPG. El adaptador no fabrica observaciones, no resuelve orbitales, radiación real ni contención de naves; no dispone de scheduler B10, sensor en UE5, orden HOST/F11, guardado Core, inventarios B04 ni simulación galáctica real.

## Entregables y puerta de aceptación

- Contrato: `sistemas/universe/generation/phenomena_anomalies_archaeology_reference_contract_v0.1.json`.
- Simulador offline: `desarrollo/tools/generation/simulate_phenomena_archaeology.py`.
- Fixture: `desarrollo/validation/fixtures/phenomena_archaeology/phenomena_archaeology_exploration_v0.1.json`.
- Tests adversariales: `desarrollo/tools/generation/test_simulate_phenomena_archaeology.py`.
- GitHub Actions: `.github/workflows/p2-b07-phenomena-archaeology.yml`.
- Manifiesto: `proyecto/docs/roadmap/procedural_phenomena_archaeology_status_v0.1.json`.
- Acta: `proyecto/docs/roadmap/P2_B07_ACTA_CIERRE_REFERENCIA_20261112.md`.

Sólo tras CI **verde en último commit y fusión** se declara `REFERENCE_COMPLETE`; no se confundirá con F13 terminada. El siguiente bloque será **8 — Crisis sistémicas**, que podrá reaccionar a estados de fenómenos aceptados, **pero no reimplementar** su origen, sensores o arqueología.
