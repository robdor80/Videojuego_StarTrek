# LORE-02 C — Medicina, xenobiología y razonamiento clínico

**Corte de investigación:** 21-10-2026 · **Estado:** NEEDS_REVIEW hasta aprobación humana · **Modo:** documentos y datos de autoría, no motor médico ejecutable.  
**Base GitHub auditada:** Videojuego_StarTrek/main 2306becaf7f9 (PR #33 fusionada); CoreRPG/main 4f282863737b (4.13 integrada).  
**Responsabilidades:** Star Trek proporciona biología contextual y reglas médicas especializadas; CoreRPG conserva estado, acciones, conocimiento y persistencia; Host autoriza, UE5 presenta. Ninguna lectura, texto de IA ni catálogo modifica la realidad.

## 1. Material ya existente: NO duplicar

- Medicina: lore/medicine/medical_capability_contract.json, gameplay/medical/medical_state_model.json y species_medical_hooks.json. Los estados clínicos reales, observables, diagnósticos conocidos, pronóstico y aptitud son distintos.
- LORE-01: lore/species/evidence/*.json y monographs/*.md. La evidencia cultural/biológica no equivale a valor clínico medido de cada individuo.
- LORE-02 A: atlas tecnológico de 59 sistemas, instalaciones y matriz de época; energía, sensores y transporte son capacidades de módulos reales, no poderes médicos implícitos.
- LORE-02 B: 73 equipos, de los que **9 pertenecen a la familia medical**. El tricorder médico, scanner de mano, hipospray, cartucho identificado, botiquín, regenerador dérmico, monitor portátil, camilla y kit de cuarentena NO autorizan actos por su mera existencia.
- Autoridad y privacidad: lore/federation/starfleet/regulations/medical_authority.json, gameplay/records_and_logs/access_and_privacy_rules.json y F04/LIMITES_MEDICOS_NORMATIVOS_P04.md. El médico jefe puede relevar por aptitud, no asumir el mando.
- Personal y experiencia: gameplay/characters/, gameplay/logistics/, gameplay/inventory/ y Academia rama médica (MED-201, MED-202, MED-203, MED-101, MED-102). Competencia del alumno ≠ actuación acreditada.
- CoreRPG 4.9 conocimiento/visibilidad, 4.10 acciones/simulación, 4.11 inspector, 4.12 contexto IA autorizado, 4.13 Content Pack real de Nimroel. Ninguno proporciona todavía un algoritmo clínico Star Trek.

## 2. Corpus e índices

| Archivo | Alcance | Limitación |
| --- | --- | --- |
| lore02_c_species_clinical_atlas_v0.1.json | 25 referencias de especies existentes + 1 perfil multiespecie de modificación Borg | Sin constantes vitales ni dosis universales |
| lore02_c_conditions_v0.1.json | 38 condiciones/estados/situaciones, con señales, diferenciales, ámbito y procedencia | 17 grupos documentales y de diseño no constituyen prevalencia ni curva médica |
| lore02_c_procedures_v0.1.json | 26 protocolos de diseño vinculados a material existente y requisitos | No son recetas reales ni procedimientos implementados |
| lore02_c_medical_agents_v0.1.json | 13 medicamentos y tecnologías presentes en referencias Star Trek | Datos cualitativos: sin dosis, eficacia, compatibilidad universal ni disponibilidad automática |
| lore02_c_facilities_staff_v0.1.json | 9 instalaciones + 12 roles | No crean camas, especialistas ni telemedicina |
| lore02_c_civilization_medical_profiles_v0.1.json | 13 perfiles interculturales de sanidad: Federación, vulcanos, klingon, bajoranos, cardassianos, romulanos, Trill, betazoides, vidiiianos, Dominio, cambiantes, andorianos y ferengi | Ningún perfil acredita superioridad o competencia automática de una facción |
| gameplay/medical/lore02_c_diagnostic_workflow_v0.1.json | 11 tipos de pasos con límites epistémicos, consentimiento y autoridad | El Host y Core deberán implementar transiciones posteriormente |
| lore02_c_clinical_decision_matrix_v0.1.json | 38 enlaces observación → diagnóstico diferencial → respuesta y ocho vínculos terapéuticos condicionados | Propuestas documentales; no prescripciones, ni stock, ni simulación clínica |
| lore02_c_adversarial_scenarios_v0.1.json | 62 casos con respuesta requerida/prohibida | Son pruebas documentales; no son partidas ejecutadas |

Todos son **editoriales**, con estado de revisión y sin edición directa de los contratos fundamentales. Los arquetipos GAME_ADDITION (accidente, hipoxia, contaminación genérica, crisis de recursos) no se venden como nombres de enfermedades canónicas.

## 3. Fisiología y diversidad

La evidencia de pantalla es de casos concretos y no siempre permite deducir fisiología estadística de toda una especie.

- **Humanos:** referencia de comparación, nunca norma clínica universal.
- **Vulcanos:** pon farr (TOS: Amok Time); síndrome Bendii en el caso Sarek (TNG); interacción mental con consentimiento. Requerir historia individual, no atribuir un ciclo exacto a un paciente recién conocido.
- **Klingon:** TNG Ethics relata la lesión de Worf, redundancias anatómicas específicas y cirugía experimental de alto riesgo. No extrapolar eficacia ni supervivencia segura por órganos duplicados.
- **Trill:** huésped, simbionte, unión y continuidad de recuerdos; ver TNG The Host / DS9 Invasive Procedures y la historia Dax. El simbionte es una entidad biológica relevante, pero no todo Trill está unido. Consentimiento de huésped y riesgos del simbionte requieren tratamiento distinto.
- **Betazoides:** síndrome Zanthi en casos señalados; proyección afectiva no es telemetría de patógenos ni diagnóstico mental infalible.
- **Vidiians:** el fago documentado explica cuadros degradantes e injertos de órganos. Rechazar discriminación automática, simplificaciones de consentimiento y supuesto de enfermedad en todos los individuos.
- **Bajoranos:** Kalla-Nohra ligado a exposición histórica, no a genes bajoranos.
- **Ocampa, Jem'Hadar, metamorfos, romulanos, cardassianos, andorianos, tellaritas y otros:** heredar evidencia de LORE-01, pero marcar lo clínico no demostrado. Cultura, uniforme y apariencia no equivalen a metabolización, inmunidad o signos vitales.
- **Borg:** colectivo de especies y modificaciones, **no especie de origen único**. Implantes, nanoprobes y dependencia de soporte deben constar por paciente; ejemplo excepcional de reanimación de Neelix con nanoprobes no funda un procedimiento universal.

**Política de vacíos:** constantes fisiológicas, valores normales, compatibilidades farmacológicas, prevalencia, latencias, dosis y tiempos permanecen nulos cuando no estén sustentados. Si más adelante el juego crea parámetros de balance, se etiquetarán GAME_ADDITION y se someterán a prueba.

## 4. Enfermedades y sus trampas de diseño

**Cuadros trazables a material oficial:** pon farr; Bendii; Zanthi; fago vidiiano; plaga de Teplan; macrovirus; metremia; Kalla-Nohra; complicaciones huésped-simbionte Trill; lesión medular del caso Worf; seguimiento postasimilación; efectos de intervenciones extraordinarias.

**Diferencias que importan:**
- En DS9 The Quickening, la intervención destinada a curar acelera las muertes, pero se logra prevención en descendencia. Es un precedente excelente de hipótesis razonable **equivocada**, iatrogenia y seguimiento, no una receta para cualquier enfermedad. Fuentes L02C_ST_QUICKENING y L02C_ST_BASHIR.
- En VOY Macrocosm, una operación de asistencia y los transportadores llevan a una brecha de cuarentena; sensores y biofiltros deben funcionar según estado real, no por la mera etiqueta de tecnología. Fuentes L02C_ST_MACRO y L02C_ST_QUICKENING.
- TNG Ethics enfrenta autonomía del paciente, terapias nuevas, criterio de médico jefe y eficacia incierta. El éxito observado fue contingente y no desbloquea cirugía equivalente en cualquier nave. Fuentes L02C_ST_MED_ETHICS y L02C_ST_ETHICS_DETAILS.
- En VOY Lifesigns, avatar holográfico sano y cuerpo enfermo divergen; representación gráfica jamás equivale a estado orgánico del paciente. Fuente L02C_ST_VID_LIFE.
- En VOY Latent Image, el profesional holográfico carece de omnipotencia y sufre conflicto por una elección de recursos limitados; la arquitectura IA debe conservar responsabilidad y incertidumbre. Fuente L02C_ST_MENTAL_EMH.

**Nunca:** toda afección universal en todas las especies; nanoescáner omnisciente; exposición = contagio probado; cirugía experimental sin riesgo; regenerador dérmico capaz de reconstruir cualquier órgano; fármaco sin compatibilidad ni autorización; curación con tiempo fijo de escena.

### Casos ampliados de diagnóstico diferencial (TNG / DS9 / Voyager)

- **Jem'Hadar y ketracel-white:** la privación del compuesto diseñado por el Dominio puede producir deterioro progresivo y pérdida funcional, pero existen casos genéticos documentados de individuos que generan la enzima faltante sin aporte externo. Para un personaje determinado, obtener su historial, análisis y suministro; evitar automatismos basados en su pertenencia al Dominio (fuente L02C_MA_KETRACEL_WHITE; DS9 *Hippocratic Oath* y *Rocks and Shoals*).
- **Bolianos y vulcanos:** una transfusión con sangre de origen vulcano puede ser peligrosa para un receptor boliano según VOY *Prototype*. La compatibilidad depende de la pareja concreta, no de que ambas especies sean humanoides (L02C_MA_BOLIAN_BLOOD).
- **Enfermedad de Orkett:** VOY *State of Flux* contiene un relato clínico atribuido por Seska a una enfermedad bajorana y supuesto trasplante de médula; los resultados del EMH lo contradicen. Diferenciar dato testimonial, marcadores medidos y causa real en NPC (L02C_MA_ORKETT).
- **Virus morfogénico:** DS9 muestra un patógeno fabricado por Sección 31 contra Fundadores. La transmisión entre individuos metamorfos y la cura extraordinaria forman parte de un contexto político/ético concreto. No asumir transmisión interhumanoide universal (L02C_MA_MORPHOGENIC).
- **Protomorfosis de Barclay:** TNG *Genesis* relata una intervención con linfocitos sintéticos que deriva en contagio iatrogénico. Distinguir condición primaria, error terapéutico, exposición del resto de la tripulación y medidas de investigación (L02C_MA_BARCLAY).
- **Síndrome irumódico:** TNG *All Good Things…* plantea futuro alternativo y predisposición neurológica, no futuro determinista en nuestra campaña. Una anomalía no equivale a enfermedad presente, y nuestras decisiones de continuidad no se supeditan a cronologías hipotéticas (L02C_MA_IRUMODIC).

Estos seis cuadros aportan una nueva comprobación adversarial cada uno. Procedencia **RELIABLE_SECONDARY** (reconstrucción del episodio por fuente especialista) y no instrucciones clínicas ejecutables. La causa oculta siempre se decide mediante el estado de CoreRPG.

## 5. Diagnóstico jugable: investigación, no respuesta escrita

1. Instanciar paciente real en Core con estado oculto; el Host solo recibe proyección autorizada.
2. Identificar identidad, origen biológico conocido, historia autorizada, exposición, síntomas y signos presentes.
3. Seleccionar exploración o tricorder real: comprobar calibración, energía, alcance, consumible, ambiente y formación.
4. Generar **resultado observable** con calidad, incertidumbre, instante y fuente; negativos y falsos positivos son posibles, pero los coeficientes son futuros datos de diseño, nunca valores ficticiamente canónicos.
5. Médico usa conocimientos y acceso específicos para mantener **varias hipótesis**. Registrar probabilidad cualitativa o evidencia; no inventar certeza matemática.
6. Solicitar pruebas de confirmación, especialista o segunda opinión. Error, falta de equipamiento y conocimiento desactualizado son vías de juego legítimas.
7. Proponer diagnóstico provisional o confirmado si se cumplen criterios de conocimiento, evidencia y autoridad; un diagnóstico conocido no transforma la causa real.
8. Prescribir tratamiento solo con indicación, consentimiento/excepción estrecha, especie, riesgos, profesional y recursos.
9. Host propone acción tipada, CoreRPG valida invariantes, consume recursos y simula evolución. UE5 muestra hechos autorizados, nunca decide la consecuencia.
10. Reevaluar, registrar evolución temporal, rehabilitación, aislamiento y aptitud. Recaídas, secuelas y revisión de órdenes forman parte del arco longitudinal.

Las explicaciones de NPC pueden ser creativas en tono, pero su diagnóstico debe poder rastrearse hasta datos visibles y competencia existente. El contexto de IA jamás incluye verdades privadas por el hecho de existir en un JSON de autoría.

## 6. Procedimientos, equipos y límites

- Tricorder médico y scanner manual: aportan mediciones, no etiología omnisciente.
- Hipospray + cartucho: requieren identificación del contenido, inventario de carga, prescripción y compatibilidad; no hay dosis canónica genérica.
- Regenerador dérmico: aplicación acotada por indicación, tejido, formación, estado del dispositivo; no curación universal.
- Camilla y botiquín: traslado y primeros cuidados; no crean un médico titulado.
- Monitor portátil: seguimiento con actualización temporal y calidad de medida.
- Kit de cuarentena: barrera contextual, mantenimiento, capacidad y descontaminación; no infalibilidad.
- Cirugía avanzada, trasplantes, asistencia a simbiontes y manipulación Borg requieren profesional, instalaciones y autorización específicos; se diseñan como **evaluaciones/derivaciones**, no actos disponibles desde el inventario de bolsillo.

Los procedimientos registrados en el catálogo son **pasos jugables diseñados**. Ninguno prescribe práctica clínica real, ni afirma curación/dosis/cronómetros. No convertir consecuencias de episodios individuales en rendimiento reproducible.

### Agentes médicos y tecnologías específicas

El catálogo adicional documenta **cordrazina, tricordrazina, hironalin, inaprovalina, lectrazina, tri-ox, felicium, arithrazina, regenerador dérmico, estimulador osteogénico, replicador genetrónico, terapia extraordinaria mediante nanoprobes Borg y ketracel-white como recurso bioquímico específico de Jem'Hadar**. Se incorporan dieciocho fuentes secundarias especializadas al registro, que totaliza 487 referencias en su corte de 21-10-2026. El origen de la evidencia no se convierte en una autorización para prescribir.

- **Medicamentos:** las referencias documentan indicaciones narrativas, efectos y contraejemplos; un nombre en el catálogo no certifica que una dosis o uso concretos sea seguro para cada especie, ni que el almacén de una nave contenga el fármaco. Por ejemplo, el caso **lectrazina** exige comprobar biología específica.
- **Felicium:** el caso de TNG *Symbiosis* muestra que una enfermedad histórica, una dependencia farmacológica y el aprovechamiento social no deben confundirse.
- **Regeneración / cirugía:** regenerador dérmico no equivale a replicador genetrónico. La tecnología del caso Worf fue **experimental** y su mera documentación no la hace disponible en Valhalla u otras enfermerías.
- **Nanoprobes:** el caso extraordinario de Neelix no demuestra un tratamiento de reanimación repetible ni autoriza manipular nanoprobes sin permisos, especialistas y evaluación paciente-específica.

El catálogo se separa del catálogo de procedimientos: **un agente es una referencia médica**, mientras un **procedimiento es una propuesta de interacción**. La futura simulación deberá vincular ambos con protocolos compatibles, efectos causalmente simulables y datos creados y versionados como GAME_ADDITION cuando no exista evidencia. El validador bloquea agentes sin procedencia, dosis o eficacia inventadas, disponibilidad automática, declaración de UE5 operativo y ampliación falsa de autoridad de fuentes.

## 7. Instalaciones, turnos y emergencias

La capacidad asistencial de una nave o estación se calcula con la intersección de módulos instalados, energía, reservas, camas, personal en ese turno, cualificación, seguridad ambiental, aislamiento, evacuación y aprovisionamiento. La instalación escrita en un plano no está disponible si se ha perdido su soporte.

**Situación ejemplo — Emergencia Valhalla:** impacto deja sin energía una sección, llegan cinco pacientes de procedencias distintas, dos aislamientos potenciales y un único médico de guardia. Ingeniería debe restablecer soporte; el responsable médico organiza triaje cualitativo, pide camillas y turnos de refuerzo, determina cuál puede trasladarse, y documenta incertidumbres. El capitán puede reasignar recursos lícitamente; no diagnostica por rango. La resolución es consecuencial y persistente, no un vídeo guionizado.

**Situación ejemplo — Exploración:** la lanzadera vuelve de un planeta con síntomas heterogéneos. Primero evaluar seguridad, cadena de muestras, posible exposición y origen biológico. La enfermedad puede ser no contagiosa; la cuarentena provisional no prueba culpabilidad ni justifica exclusión social.

**Situación ejemplo — Campaña longitudinal:** una oficial sigue incapacitada parcialmente tras el turno de batalla. El parte operativo sólo indica límites de aptitud y fecha de revisión; su tratamiento, privacidad, relación con compañeros y posible vuelta al servicio se desarrollan durante varios turnos.

## 8. Ética, IA, mando y otras civilizaciones

- Confidencialidad con mínimo privilegio; autenticación ≠ autorización; ni capitán ni oficial de seguridad acceden automáticamente a la historia privada.
- Consentimiento informado si existe capacidad; la excepción por emergencia debe ser estrecha, motivada, trazable, temporal y revisable. No usar orden militar como sustituto de voluntad capaz.
- Médico jefe releva exclusivamente por aptitud; la sucesión de mando normal se mantiene. No se proporciona acceso general al motivo clínico al resto de cadena.
- El consentimiento para muestras, investigación, intervención genética o trasplante debe tratarse separadamente del tratamiento rutinario y de la misión.
- Nunca deducir peligrosidad, contagio, competencia o medicina mejor/peor a partir de pertenencia klingon, romulana, cardassiana, borg, vidiiana o cualquier otra. Variantes de tratamientos quedan por operador, instalación, época, recursos y persona.
- Los pacientes tienen vida privada y posibles secuelas emocionales; no patologizar desacuerdo, trauma o diversidad cultural sin valoración.
- Población civil, prisioneros y poblaciones desconocidas requieren especial cautela frente a experimentación, muestras no consentidas y prejuicios.

### 8.1. Perfiles interculturales sin extrapolaciones

Se registran 13 perfiles por operador, institución o comunidad. Cada perfil enlaza especies o autoridad ya presente en LORE-01 y en contratos de mando, resume ejemplos concretos y explicita lo **no inferible**. No se equipara acceso a fármacos con una civilización determinada, ni se presupone que un médico klingon, romulano, cardassiano, vidiiiano, vulcano o ferengi actúe con una competencia o conducta fija.

La matriz de decisiones asociada enlaza los **38 cuadros** con observaciones, diagnósticos diferenciales, procedimientos condicionados y, solo cuando la referencia lo justifica, **ocho relaciones propuestas** con agentes y tecnologías. Distingue vínculos episódicos, opciones que exigirán validación del paciente, experimentos aislados y referencias históricas expresamente no prescriptivas. La matriz no decide efectos de CoreRPG.

## 9. Frontera técnica y referencias cruzadas

**CoreRPG:** WorldState guarda condiciones, recursos y evolución; Knowledge / Visibility distingue quién sabe qué; ActionEngine / Simulation resuelve solicitudes válidas y tiempo; Persistence almacena episodios; ContextBuilder sólo construye contexto autorizado. No existe todavía una implementación médica de estas reglas.

**Host Star Trek:** consume catálogos al transformarlos en Content Pack y reglas, valida profesión, consentimiento, observabilidad, compatibilidad individual y coste. La futura integración debe preservar IDs, versiones de evidencia y audit trail. **No** se pide ampliar Core genérico ahora.

**UE5:** animaciones del tricorder, biocamas, consolas, zonas de aislamiento, guardias y diálogo son presentación; nunca hacen mutaciones clínicas. El estado de cámara, PBR, ni la escena descargada de enfermería constituyen evidencia de gameplay.

**Academia:** prácticas graduadas de entrevista, diferencial, supervisión, emergencias múltiples, bioética y especialidades se conectan con MED-201/202/203/101/102. Una nota teórica no acredita una intervención sin práctica o permiso.

**LORE-02 D:** investigación general, agentes desconocidos y métodos experimentales más profundos pertenecen a Ciencia; C define frontera clínica y bioseguridad básica.

**LORE-02 E:** revisión cruzada de jerarquías de fuentes, IDs, era, operador, matriz tecnológica, validadores y precedencia de decisiones históricas. La transformación a pack importable y UE5 será fase distinta tras cerrar todos los LORE.

## 10. Evidencia y límites de validación

- Fuente primaria registrada cuando exista: TOS Amok Time, VOY Phage y otras entradas audiovisuales registradas previamente en source_registry; una fuente oficial de comentario NO se hace pasar por fotograma primario.
- Fuentes oficiales añadidas: investigación de TNG Ethics; análisis del fago vidiiano; Trill y Dax; Bashir y Teplan; Bendii/Zanthi; Voyager Macrocosm/Lifesigns/Mortal Coil/Latent Image; metremia y Kalla-Nohra. En cada afirmación, seguir source_ids y respetar su alcance.
- Hay vacíos pendientes de documentación: cifras por especie, protocolos farmacológicos aplicables por era, competencias médicas exactas por cultura, compatibilidad individual de simbiontes, instalaciones de todas las clases y simulación clínica efectiva.
- Los validadores solo comprueban coherencia referencial, seguridad del diseño y prohibiciones de afirmaciones falsas. **No acreditan seguridad médica real, tratamiento, playtesting, UE5 ni pruebas de causalidad**.
- Estado editorial final de esta PR: NEEDS_REVIEW. Tras la fusión autorizada, actualizar índice CONTENT_STATUS a COMPLETE mediante cambio administrativo posterior, sin alterar el carácter documental de los datasets.

## 11. Fuentes que ejemplifican la distinción de evidencia

- TOS Amok Time: TOS_AMOK_TIME (SCREEN_CANON).
- VOY Phage: VOY_PHAGE (SCREEN_CANON).
- TNG Ethics: L02C_ST_MED_ETHICS, L02C_ST_ETHICS_DETAILS (OFFICIAL_REFERENCE).
- VOY Macrocosm y DS9 The Quickening: L02C_ST_MACRO, L02C_ST_QUICKENING, L02C_ST_BASHIR (OFFICIAL_REFERENCE).
- Trill/Dax: L02C_ST_TRILL, L02C_ST_DAX (OFFICIAL_REFERENCE).
- Vidiian: L02C_ST_VIDIIAN, L02C_ST_VID_LIFE (OFFICIAL_REFERENCE).
- Neuro/empatía: L02C_ST_BENDII, L02C_ST_EMPATHY (OFFICIAL_REFERENCE).
- Caso Borg y secuelas: L02C_ST_BORG (OFFICIAL_REFERENCE).
- Medio de exposición: L02C_ST_JETREL (OFFICIAL_REFERENCE).
- Los límites de privacidad, triaje, acceso y reglas Host son GAME_ADDITION derivados de diseño propio; nunca citar fuente oficial como autorización normativa exacta de una mecánica nueva.
