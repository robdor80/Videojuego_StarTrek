# STAR TREK — PLAN MAESTRO DE DESARROLLO PROCEDURAL POR CAPAS v0.1

**Estado:** ACTIVO  
**Método:** desarrollo secuencial por capas con validación obligatoria  
**Inspiración metodológica:** construcción progresiva usada en Nimroel/Treskal, adaptada a un universo Star Trek de escala galáctica  
**Regla:** una capa no se considera cerrada porque exista un archivo; debe cumplir su criterio de salida y no romper capas anteriores.

---

## 1. Principio de trabajo

El universo no se construirá mediante sistemas aislados ni mediante generación oportunista.

Cada capa debe responder:

1. qué realidad autoritativa añade;
2. de qué capas depende;
3. qué datos/contratos produce;
4. qué puede cambiar con el tiempo y qué debe persistir;
5. qué reglas deterministas aplica;
6. qué sabe o no sabe cada actor sobre esa realidad;
7. qué implicaciones tiene para IA, gameplay, visuales y NAP;
8. qué invariantes permiten demostrar que funciona.

**Regla rectora:** generar primero la realidad; observarla después.

---

## 2. Estados

- `TODO` — no desarrollada.
- `AUDITED` — dominio auditado y alcance conocido.
- `IN_PROGRESS` — contratos o datos en desarrollo.
- `PARTIAL` — existe base útil pero no cumple aún definición de terminado.
- `COMPLETE` — cumple contrato, persistencia, validación y dependencias.
- `BLOCKED_AUTHOR` — necesita una decisión real de autor.

Una capa marcada `COMPLETE` solo vuelve a abrirse mediante una migración explícita.

---

# FASE 0 — AUTORIDAD, ARQUITECTURA Y GOBERNANZA

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 001 | Jerarquía de autoridad de datos | COMPLETE | — | Canon, campaña, procedural y World State tienen precedencia inequívoca |
| 002 | Separación CoreRPG / Star Trek | COMPLETE | 001 | Cada contrato sabe si es genérico o Trek-específico |
| 003 | Identificadores estables y namespaces | COMPLETE | 001 | Todas las entidades persistentes pueden referenciarse sin usar nombres visibles |
| 004 | Semillas deterministas por subsistema | COMPLETE | 003 | Añadir subsistemas no rerolleará resultados existentes |
| 005 | Versionado y migraciones | COMPLETE | 003-004 | Cambios de reglas tienen estrategia de migración explícita |
| 006 | Canon temporal y reservas | COMPLETE | 001 | Generadores no pisan hechos/entidades reservados por fecha |
| 007 | Proveniencia y confianza de fuentes | COMPLETE | 001 | Todo dato sensible a canon puede rastrear fuente y nivel de autoridad |
| 008 | Definición de terminado y validación transversal | COMPLETE | 001-007 | Toda futura capa usa la misma plantilla de cierre |

# FASE 1 — EXISTENCIA, IDENTIDAD Y PERSISTENCIA

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 009 | Contrato universal de entidad persistente | COMPLETE | 003-005 | ID + procedencia + historial + estado actual quedan separados |
| 010 | Identidad persistente de personajes | COMPLETE | 009 | Un individuo jamás se rerollea tras materialización |
| 011 | Identidad visual persistente | COMPLETE | 009-010 | Cambiar edad/ropa/estado no crea otra persona |
| 012 | Identidad persistente de naves | COMPLETE | 009 | Refit, reparación y cambio de capitán preservan nave |
| 013 | Identidad persistente de instalaciones | COMPLETE | 009 | Daño/reconstrucción compatible preserva continuidad |
| 014 | Identidad de objetos únicos | COMPLETE | 009 | Propiedad, daño o traslado no rerollean objeto |
| 015 | Población A/B/C | COMPLETE | 009-010 | C→B irreversible conserva contabilidad poblacional |
| 016 | Materialización desde slots reales | COMPLETE | 015 | NPC nace de necesidad/posición/hogar real, no de petición del jugador |
| 017 | Persistencia fuera de cámara / LOD | COMPLETE | 009-016 | Descargar simulación no altera identidad ni hechos |
| 018 | Guardado/carga y round-trip de identidad | COMPLETE | 009-017 | Serializar y restaurar preserva exactamente identidad e historia |

# FASE 2 — PERSONA, MEMORIA, CONOCIMIENTO Y RELACIONES

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 019 | Definición base de personaje | COMPLETE | 010 | Identidad inicial separada de estado vivo |
| 020 | Personalidad estable vs estado emocional | COMPLETE | 019 | Personalidad no deriva automáticamente de especie/rango |
| 021 | Valores, objetivos, miedos y límites | COMPLETE | 020 | Motivaciones persistentes tienen causas y privacidad |
| 022 | Toma de decisiones | COMPLETE | 020-021 | Decisiones consumen estado, no inventan hechos |
| 023 | Modelo de conocimiento | COMPLETE | 019 | Saber requiere canal válido de adquisición |
| 024 | Memoria actor-específica | COMPLETE | 023 | Memoria ≠ World Truth; admite saliencia e incertidumbre |
| 025 | Olvido, resumen y reinterpretación | COMPLETE | 024 | Perder detalle no fabrica ni borra consecuencias |
| 026 | Grafo social multidimensional | COMPLETE | 019 | Relaciones son direccionales y no un único score |
| 027 | Procedencia de relaciones | COMPLETE | 026 | Amistad/confianza/hostilidad requieren historia plausible |
| 028 | Romance, afecto, intimidad y consentimiento | COMPLETE | 026-027 | Estados separados, recíprocos cuando corresponda y nunca forzados |
| 029 | Parentesco y redes familiares | COMPLETE | 019,031-036 | Familia separada de amistad, hogar, tutela y afecto |
| 030 | Reputación, rumor y propagación social | COMPLETE | 023-027 | Información pública emerge por observación/transmisión |

# FASE 3 — BIOLOGÍA, ESPECIES, CULTURAS Y CICLO VITAL

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 031 | Esquema universal de especie | COMPLETE | 002 | Biología tiene contrato común sin definir personalidad |
| 032 | Morfología y anatomía | COMPLETE | 031 | Rasgos físicos canon y variación individual diferenciados |
| 033 | Fisiología y necesidades | COMPLETE | 031 | Sueño, alimentación, ambiente y tolerancias son resolubles |
| 034 | Longevidad, madurez y envejecimiento | COMPLETE | 031-033 | Edad cronológica se traduce correctamente por especie |
| 035 | Reproducción y desarrollo | COMPLETE | 031-034 | Reglas dependen de biología/canon y nunca de supuestos humanos |
| 036 | Sexo, género y variación biológica | COMPLETE | 031-035 | Datos permiten especies no humanas sin forzar binarios universales |
| 037 | Medicina específica por especie | COMPLETE | 031-036 | Diagnóstico/tratamiento respeta fisiología y conocimiento disponible |
| 038 | Capacidades sensoriales y cognitivas | COMPLETE | 031 | Telepatía/empatía/sentidos no equivalen a omnisciencia |
| 039 | Cultura como dimensión independiente | COMPLETE | 031 | Cultura no está bloqueada por especie |
| 040 | Socialización, origen y culturas mixtas | COMPLETE | 039 | Individuos pueden pertenecer a múltiples contextos culturales |
| 041 | Lenguas y comunicación | COMPLETE | 039 | Lengua conocida, competencia y traducción universal quedan separadas |
| 042 | Ciclo vital completo y muerte | COMPLETE | 019,029,031-041 | Nacimiento/creación→vida→envejecimiento→muerte→legado es persistente |

# FASE 4 — ORGANIZACIONES, SERVICIO Y CARRERA

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 043 | Modelo universal de organización | COMPLETE | 002,009 | Federación, imperios, gobiernos, civiles y organizaciones caben sin hacks |
| 044 | Afiliación, ciudadanía y lealtad | COMPLETE | 043 | Dimensiones separadas y temporalmente mutables |
| 045 | Starfleet: divisiones y departamentos | COMPLETE | 043 | División, departamento y función tienen semántica clara |
| 046 | Rangos y antigüedad | COMPLETE | 045 | Rango no equivale a puesto |
| 047 | Puestos y posiciones | COMPLETE | 045-046 | Puesto define función y requisitos, no personalidad |
| 048 | Cadena de mando y sucesión | COMPLETE | 046-047 | Autoridad efectiva puede resolverse en cualquier momento |
| 049 | Turnos, guardias y relevos | COMPLETE | 047-048 | Cobertura temporal y handoff son consistentes |
| 050 | Cualificaciones y competencias | COMPLETE | 019,047 | Puestos exigen evidencia/cualificación real |
| 051 | Carrera, evaluaciones, ascensos y traslados | COMPLETE | 046-050 | Trayectoria emerge de servicio e historial |
| 052 | Academia → graduación → primera asignación | COMPLETE | 045-051 | Formación enlaza sin discontinuidad con personaje y carrera reales |

# FASE 5 — NAVES, TRIPULACIONES E INSTALACIONES

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 053 | Clase de nave vs nave individual | PARTIAL | 012 | Diseño/clase no se confunde con instancia |
| 054 | Era/configuración/refit de clase | PARTIAL | 006,053 | Capacidades dependen de configuración fechada |
| 055 | Misión y función operacional de nave | PARTIAL | 043,053 | Una nave existe por operador, función y contexto |
| 056 | Sistemas de nave como capacidades | PARTIAL | 054-055 | Sistemas disponibles son fecha/configuración dependientes |
| 057 | Topología e interiores funcionales | PARTIAL | 053-056 | Espacios existen por función y conectividad |
| 058 | Necesidades de dotación | TODO | 045-057 | Departamentos/puestos nacen de sistemas y misión |
| 059 | Generación de tripulación por slots | PARTIAL | 015-016,058 | Complemento conserva contabilidad y cualificaciones |
| 060 | Cuadrantes/turnos de tripulación | PARTIAL | 049,059 | Cada guardia mantiene cobertura viable |
| 061 | Vida a bordo y espacios privados/sociales | TODO | 026-030,057-060 | Rutinas personales y de servicio coexisten |
| 062 | Daño, reparación y mantenimiento | PARTIAL | 012,056 | Estado técnico cambia sin reemplazar identidad |
| 063 | Instalaciones, estaciones y starbases | PARTIAL | 013,043 | Función→servicios→staff→tráfico→estado |
| 064 | Astilleros, atraque, reabastecimiento y refit | PARTIAL | 054,062-063 | Servicios requieren capacidad, cola, recursos y tiempo |

# FASE 6 — ASTROGRAFÍA, PLANETAS Y CIVILIZACIONES

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 065 | Coordenadas, sectores y anclas espaciales | PARTIAL | 006 | Toda localización tiene identidad espacial consistente |
| 066 | Sistemas estelares | PARTIAL | 065 | Estrella/cuerpos/orbitas se generan antes de ser observados |
| 067 | Planetas y lunas físicos | PARTIAL | 066 | Masa, gravedad, atmósfera, órbita y superficie son coherentes |
| 068 | Clima y estado ambiental | PARTIAL | 067 | Tiempo actual evoluciona sobre clima persistente |
| 069 | Biomas y ecosistemas | TODO | 067-068 | Distribución ecológica responde a condiciones físicas |
| 070 | Habitabilidad y biosfera | TODO | 067-069 | Vida no aparece sin causalidad ambiental |
| 071 | Civilización y nivel tecnológico | PARTIAL | 067-070 | Sociedad deriva de mundo/historia, no de etiqueta decorativa |
| 072 | Regiones y asentamientos | TODO | 071 | Población e infraestructura se distribuyen espacialmente |
| 073 | Infraestructura y servicios | TODO | 071-072 | Energía, transporte, salud, administración, etc. tienen soporte real |
| 074 | Economía y recursos planetarios | TODO | 071-073 | Producción/escasez/comercio reflejan tecnología y política |
| 075 | Política, leyes e instituciones | TODO | 043,071-074 | Autoridad e instituciones tienen jurisdicción y estado |
| 076 | Historia local y conflictos persistentes | TODO | 071-075 | El presente tiene causas históricas trazables |

# FASE 7 — MOVIMIENTO, LOGÍSTICA, ECONOMÍA Y DIPLOMACIA

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 077 | Rutas y costes de navegación | PARTIAL | 065-066,056 | Trayectos consumen distancia/tiempo/riesgo válidos |
| 078 | Tráfico espacial causal | PARTIAL | 055,063-077 | Cada nave en tráfico tiene origen, destino y razón |
| 079 | Pasajeros, migración y visitantes | TODO | 015,072,078 | Movimientos alteran población sin duplicarla |
| 080 | Recursos, inventarios y abastecimiento | PARTIAL | 064,074,078 | Stock cambia por causas reales |
| 081 | Replicadores y economía post-escasez contextual | TODO | 056,074,080 | Replicación no elimina energía, acceso, rareza ni logística especial |
| 082 | Comercio y operadores civiles | TODO | 043,074,078-081 | Actividad comercial tiene actores/rutas/demanda |
| 083 | Fronteras, jurisdicción y diplomacia | PARTIAL | 043-044,065,075 | Espacio político afecta acceso y conducta |
| 084 | Crisis, bloqueos, guerras y alteración de redes | TODO | 076-083 | Eventos estratégicos repercuten en tráfico, suministro y población |

# FASE 8 — TECNOLOGÍA TREK Y CASOS EXCEPCIONALES

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 085 | Matriz tecnológica por era/civilización | TODO | 006,071 | Disponibilidad tecnológica se resuelve por fecha y actor |
| 086 | Warp, impulso y propulsión | PARTIAL | 056,077,085 | Rendimiento y disponibilidad coherentes |
| 087 | Sensores y firmas detectables | PARTIAL | 056,085 | Sensores observan realidad preexistente |
| 088 | Comunicaciones subespaciales | TODO | 023,065,085 | Información tiene latencia/alcance/interferencia cuando proceda |
| 089 | Transportadores | TODO | 033,056,085 | Movimiento y riesgos respetan restricciones de época/contexto |
| 090 | Replicación, holocubierta y computación | TODO | 056,081,085 | Capacidades no se convierten en magia sin límites |
| 091 | Seres y estados excepcionales | TODO | 031-042,085 | Androides, hologramas, simbiontes, Changelings, Borg, etc. usan extensiones explícitas |
| 092 | Anomalías temporales/subespaciales | TODO | 006,066,085 | Excepciones no destruyen causalidad ni persistencia sin evento explícito |

# FASE 9 — SISTEMA VISUAL Y NAP

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 093 | Contrato Trek ↔ NAP | PARTIAL | 009-018 | Todo asset productivo puede rastrear entidad, reglas y procedencia |
| 094 | Esquema de contexto visual resuelto | TODO | 093 | Prompt/asset recibe composición completa de autoridades |
| 095 | Biblia Visual Global Star Trek | TODO | 093-094 | Lenguaje visual común sin borrar diferencias de era/cultura |
| 096 | Biblia de retrato/personaje | TODO | 011,031-041,095 | Identidad base separada de estado visual temporal |
| 097 | Perfiles visuales de especies | TODO | 031-038,096 | Morfología canon + variación individual controlada |
| 098 | Perfiles de cultura/afiliación/organización | TODO | 039-045,095 | Uniformidad institucional sin convertir cultura en estereotipo |
| 099 | Uniformes, divisiones, rango y variantes de era | TODO | 006,045-052,098 | Vestuario deriva de fecha/organización/función |
| 100 | Naves exteriores e identidad de clase/instancia | TODO | 012,053-056,095 | Clase reconocible; nave individual persistente |
| 101 | Interiores, consolas e instalaciones | TODO | 057,063,095 | Operatividad primero; skin visual después según era |
| 102 | Planetas, entornos, equipo y props | TODO | 067-075,085,095 | Assets visuales consumen World State y función real |

# FASE 10 — SIMULACIÓN VIVA, IA Y CONSECUENCIAS

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 103 | Agenda y actividad diaria | PARTIAL | 019-030,049 | Presencia deriva de deberes, necesidades y rutina |
| 104 | Necesidades, bienestar y fatiga | PARTIAL | 033,103 | Estado físico/cognitivo altera rendimiento sin redefinir identidad |
| 105 | Simulación social off-screen | PARTIAL | 026-030,103 | Relaciones solo cambian con contacto/causa plausible |
| 106 | Simulación profesional off-screen | TODO | 049-052,103 | Trabajo, carrera y evaluaciones avanzan causalmente |
| 107 | Simulación de naves/instalaciones off-screen | TODO | 053-064,078 | Operaciones cambian estado sin necesitar al jugador |
| 108 | Simulación planetaria off-screen | TODO | 067-084 | Población/economía/política evolucionan a LOD apropiado |
| 109 | Sistema universal de eventos y consecuencias | TODO | 009-108 | Eventos mutan estado con historial trazable |
| 110 | Muerte, destrucción, duelo y continuidad | TODO | 042,109 | Pérdidas persisten social, profesional y materialmente |
| 111 | IA como capa de expresión/decisión limitada | PARTIAL | 022-030,109 | IA no escribe World Truth por su cuenta |
| 112 | Misiones emergentes desde World State | PARTIAL | 078-111 | Misión descubre/explota problemas existentes en vez de crearlos retroactivamente |

# FASE 11 — VALIDACIÓN, VERTICAL SLICE Y PREPARACIÓN DE RUNTIME

| Capa | Sistema | Estado inicial | Dependencia | Criterio de cierre |
|---|---|---|---|---|
| 113 | Invariantes de identidad/persistencia | PARTIAL | 009-018 | Tests cubren años, LOD, save/load y migraciones |
| 114 | Invariantes de población/social | PARTIAL | 015-030 | No duplicación, omnisciencia ni relaciones sin procedencia |
| 115 | Invariantes biología/cultura | TODO | 031-042 | Especie no fuerza personalidad/cultura y casos especiales son válidos |
| 116 | Invariantes organización/tripulación | PARTIAL | 043-064 | Puesto/rango/cualificación/turno/complemento coherentes |
| 117 | Invariantes mundo/logística | PARTIAL | 065-084 | Geografía, tráfico, inventario y política conservan causalidad |
| 118 | Invariantes tecnología/canon/era | PARTIAL | 006,085-092 | Nada existe antes de tiempo ni fuera de capacidades válidas |
| 119 | Fixture vertical v0.0.1 — Sensores | PARTIAL | 087 + dependencias | Una consola detecta/analiza mundo generado previamente |
| 120 | Readiness CoreRPG + UE5 | TODO | 001-119 | Contratos estables, fixtures reproducibles, migraciones y límites definidos |

---

## 3. Orden operativo

El desarrollo avanza por dependencia, no solo por número.

Se permite trabajar varias capas consecutivas de una misma dependencia en un bloque, pero:

- no se saltan huecos estructurales por comodidad;
- no se marca COMPLETE una capa que depende de otra todavía indefinida;
- no se duplica en Star Trek lo que deba convertirse en CoreRPG;
- no se migra de Nimroel una regla ambientacional disfrazándola de genérica;
- cada bloque cerrado actualiza validación y este plan.

---

## 4. Regla de integración visual

La representación visual nunca decide la realidad.

Cadena obligatoria:

`World/Entity State → resolved visual context → Visual Bibles/profiles → prompt/asset request → NAP → production asset`

Para una entidad persistente:

`entity_id + visual_identity_id + history + current_state → current visual representation`

Nunca:

`current scene → regenerate a convenient identity`

---

## 5. Puertas de decisión de autor

El trabajo se detiene únicamente cuando una capa exige una decisión que cambie el diseño creativo global, por ejemplo:

- límites definitivos de eras jugables;
- divergencia importante respecto al canon;
- filosofía de representación de una especie no resuelta por canon;
- reglas creativas sensibles de reproducción/familia/relaciones;
- límites de contenido o muerte;
- cambios fundamentales en la fantasía de juego.

Decisiones técnicas, estructura de datos, validaciones, migraciones, organización documental y separación Core/Trek se resuelven autónomamente.

---

## 6. Próximo bloque

Secuencia inmediata:

**001–008 → consolidar gobernanza**  
**009–018 → cerrar identidad/persistencia**  
**019–030 → persona/conocimiento/memoria/relaciones**

Tras esas capas, especies y ciclo vital pueden desarrollarse sin crear contradicciones posteriores.
