# LORE-02 A — Acta de suficiencia documental y propuesta de cierre

**Fecha:** 2026-10-21.  
**Bloque:** LORE-02 A — Tecnología de naves y estaciones.  
**Estado propuesto:** `NEEDS_REVIEW` — **investigación/documentación del alcance actual terminada, pendiente de revisión y fusión por el autor**.  
**No implica:** implementación de motor warp, combate, clínicas, colisiones, UI ni adaptador CoreRPG/UE5.

## 1. Resultado de la investigación

La fase dispone de dos capas **complementarias**, sin destruir el primer corte:

| Recurso | Cobertura | Función |
|---|---|---|
| [Catálogo de primera iteración](../../../mundo/lore/technology/ship_station_catalogue_v0.1.json) | 14 sistemas Starfleet | Contexto inicial, periodos registrados, fallos, dependencias y consumidores con proveniencia por ficha |
| [Atlas de resolución A-G01–08](../../../mundo/lore/technology/lore02_a_system_atlas_v0.2.json) | **45 sistemas/funciones adicionales** | Operación, dependencias, estados observables, fallos y extrapolaciones prohibidas por sistema |
| [Operadores e instalaciones](../../../mundo/lore/technology/lore02_a_operator_facility_profiles_v0.2.json) | **9 operadores**, **14 familias de estación** | Especificaciones limitadas por actor, clase, tarea y arquitectura de instalación |
| [Casos de primera iteración](../../../mundo/lore/technology/ship_station_cases_v0.1.json) | 14 | Disponibilidad por época, transportadores, observaciones y DLC |
| [Casos adversariales ampliados](../../../mundo/lore/technology/lore02_a_adversarial_cases_v0.2.json) | **36** | Secciones separadas, energía, deflectores, comunicaciones, vida, facciones, Defiant y estaciones |
| [Dossier de investigación](lore_02_a_eight_gaps_dossier_v0.2.md) | 8 áreas | Razonamiento, límites, fuentes y casos que invalidarían inferencias |
| [Perfil VAL-TEC 01–16](../../../mundo/lore/technology/valhalla_tech_profile_v0.1.md) | 16 decisiones | Tecnología de clase aprobada y procedencia expresa/delegada |
| [Addendum creativo Valhalla/Defiant](../../../mundo/lore/technology/valhalla_creative_addendum_2026-10-21.md) | 1 acta posterior | Prioridad de la continuidad propia, armas, camuflaje, hangares, espacios jugables |
| [Registro de fuentes](../../../mundo/sources/source_registry/source_registry.json) | 438 entradas acumuladas | ID persistente, URL/obra, tipo de evidencia y limitaciones; 17 entradas técnicas ampliadas |
| Validadores Python y CI | 2 validadores y 2 suites de LORE-02 A + regresiones LORE-01 | Evitar referencias rotas, poderes ficticios, contradicciones de estado y regresiones documentales |

**Total analizado en catálogos A: 59 sistemas/funciones cualitativas, 50 casos negativos.** No se confunden cantidades de fichas con cantidades de tecnologías diferentes probadas en pantalla; algunos registros son subfunciones de sistemas mayores. No es una enciclopedia infinita.

## 2. Cierre por laguna

### A-G01 — Impulso, maniobra y separación
**Cobertura cerrada para diseño:** impulso, propulsores de actitud, navegación segura, separación de secciones y prohibición de usar warp en el platillo separado. Dependencias entre timón, energía, ambiente y autorización.  
**Evidencia:** `MA_IMPULSE_ENGINE_RESEARCH`, `MA_GALAXY_CLASS`, `ST_OFFICIAL_BRIDGE_CREW_ENGINEERING` (este último es **material sobre videojuego**, no canon técnico para cifras).  
**Prueba crítica:** A2-SAUCER_WARP_ORDER; A2-DOCKING_FAILED_THRUSTERS.  
**Se difiere correctamente:** cinemática física y parámetros numéricos por clase, a propulsión/UE5. No bloquea la descripción de qué debe suceder cuando el sistema falla.

### A-G02 — Reactor, EPS, reservas, contención y refrigeración
**Cobertura cerrada para diseño:** reactor materia-antimateria, fusión auxiliar, EPS, reservas, contención, refrigeración, sobrecarga y fallos comunes de red.  
**Evidencia:** `MA_WARP_CORE_RESEARCH`, `MA_EPS_RESEARCH`, `MA_PLASMA_CONDUIT_RESEARCH`.  
**Prueba crítica:** A2-WARP_CORE_LOSS, A2-EPS_CASCADE, A2-POWER_RESERVE_EXHAUSTION.  
**Se difiere:** curvas de consumo, volúmenes, MW, autonomía y diseños de tuberías concretas, hasta que existan dimensiones y balance.

### A-G03 — Deflector de navegación frente a escudos, tractor y ablativo
**Cobertura cerrada para diseño:** funciones separadas y casos de degradación independiente; deflector reconfigurado bajo control científico; haz tractor condicionado; ablativo con integridad propia.  
**Evidencia:** `MA_NAV_DEFLECTOR_RESEARCH`, `MA_DEFLECTOR_SHIELD`, `MA_TRACTOR_BEAM_RESEARCH`, `ST_OFFICIAL_ENDGAME_JANEWAY`.  
**Prueba crítica:** A2-NAV_DEFLECTOR_DOWN y A2-SHIELDS_OFF_DEFLECTOR_OK (fallos en ambos sentidos).  
**Se difiere:** geometría y potencia del conjunto de emisores, a clases y modelos UE5.

### A-G04 — Comunicaciones subespaciales
**Cobertura cerrada para diseño:** transmisores/receptores, relés, cifrado, autenticación, balizas, intercom, pérdidas, retrasos y **conocimiento parcial**.  
**Evidencia primaria de recapitulación oficial:** `ST_OFFICIAL_SUBSPACE_RHAPSODY_RECAP`, además de `MA_SUBSPACE_COMMUNICATION`. El episodio sobre comunicaciones experimentales muestra que el sistema de relés puede causar demoras de semanas; **no se aplica esa cifra como regla universal**.  
**Prueba crítica:** A2-RELAY_LATENCY, A2-DECRYPTED_NOT_AUTHORIZED, A2-DEFIANT_LINK_LOST.  
**Se difiere:** propagación numérica del mensaje por ruta y civilización a un sistema de comunicaciones simulado.

### A-G05 — Soporte vital y habitabilidad
**Cobertura cerrada para diseño:** atmósfera por cubierta, gravedad artificial independiente, aislamiento de sectores, agua y residuos, cuarentena y variantes de especies.  
**Evidencia:** `MA_LIFE_SUPPORT_RESEARCH`, `MA_ARTIFICIAL_GRAVITY_RESEARCH`, `MA_ENGINEER`.  
**Prueba crítica:** A2-SINGLE_DECK_BREACH, A2-LOCAL_GRAVITY_DOWN, A2-MULTI_SPECIES_ENV.  
**Se difiere:** cifras ambientales específicas, biología clínica interespecie y procedimientos médicos a LORE-02 C o a balances del simulador.

### A-G06 — Tecnología de otras civilizaciones
**Cobertura cerrada para diseño:** perfiles limitados de klingon, romulanos, cardassianos, Dominio, Breen, Borg, operadores vulcanos y civiles ferengi, además de Starfleet; clases y excepciones no extrapolables.  
**Evidencia oficial:** `ST_OFFICIAL_KLINGON_D7_FEATURE`, `ST_OFFICIAL_ROMULAN_VALDORE`, `ST_OFFICIAL_BREEN_DOMINION_WAR`, `ST_OFFICIAL_BREEN_EXPLAINER`, `ST_OFFICIAL_BORG_101`.  
**Prueba crítica:** A2-CARDASSIAN_WRONG_HULL, A2-BREEN_WEAPON_COUNTERED, A2-BORG_NOT_OMNISCIENT.  
**Se difiere:** inventario completo de todas las clases/facciones del universo, que evoluciona progresivamente con el generador y no es un bloqueo de LORE-02 A.

### A-G07 — Valhalla y excepciones
**Cobertura cerrada a nivel autoral:** 16 decisiones VAL-TEC y addendum creativo posterior.  
- **Clase nueva Valhalla** (inspiración Galaxy), USS Enterprise NCC-1701-G **de trabajo**; tamaño/dotación similares a Galaxy.
- Continuidad **propia**, sin año obligatorio ni bloqueo de convivencia de naves de diferentes series.
- Rendimiento warp mínimo objetivo Voyager/Intrepid; armamento objetivo Sovereign/Odyssey o mejor; fuente energética con núcleo principal y fusión de apoyo.
- **Tres niveles de escudo muy potentes y blindaje ablativo desplegable extraordinariamente resistente**, pero con daño, consumo y reparación.
- **Nave auxiliar clase Defiant**, dotación pequeña, armamento y blindaje altos para su tamaño y **camuflaje romulano excelente expresamente aprobado**, no infalible.
- **Un gran hangar en anillo/platillo y dos hangares pequeños en sección de batalla**, con escenas independientes y accesos simulados.
- Interiores **jugables**: dos puentes, reuniones, despacho, bar, transportadores, Enfermería, Ingeniería y cubierta circular de camarotes.
- Yate del capitán descartado; independencia de secciones y persistencia del vehículo.
**Evidencia:** instrucciones del autor `AUTHOR_DECISION/GAME_ADDITION`, IDEA-0003/0005/0010; `ST_OFFICIAL_ENDGAME_JANEWAY` solo como inspiración.  
**Prueba crítica:** A2-VALHALLA_ERA_OWN, A2-DEFIANT_CLOAK_BROKEN, A2-DEFIANT_UNDOCKED_ELEVATOR.  
**Se difiere:** dimensiones reales, número de tubos y torpedos, factores warp, diseños 3D y garantías cuantitativas. No imponer canon estricto como barrera creativa.

### A-G08 — Instalaciones y tecnología industrial/civil
**Cobertura cerrada para diseño:** 14 familias **exactamente correspondientes** a `sistemas/universe/generation/procedural_station_design_grammar_v0.1.json`, infraestructura específica, atraques y capacidades finitas.  
**Evidencia:** `ST_OFFICIAL_STARBASES_FEDERATION`, con DS9/antigua Terok Nor como ejemplo de cambio de misión tras transformación, **no** como modelo idéntico de todas las estaciones.  
**Prueba crítica:** A2-SHIPYARD_NO_PARTS, A2-DOCK_INCOMPATIBLE, A2-RELAY_NOT_HOSPITAL, A2-STATION_NONEXISTENT.  
**Se difiere:** módulos físicos exactos, rutas de tráfico, reservas monetarias y población efectiva de cada estación, sujetos al sistema generador/persistencia.

## 3. Conflictos detectados y resueltos

| Conflicto potencial | Resolución explícita |
|---|---|
| Valhalla tratada como «Galaxy Refit» | **Clase Valhalla nueva**, Galaxy solo inspiración visual; datos históricos conservados como referencia |
| Exigencia de año canónico / prohibición de coexistencia | **Continuidad propia del videojuego**; no calendario rígido por canon televisivo |
| «Defiant inspirada» pero no clase | Decisión posterior: **clase Defiant**; buque individual aún sin nombre/matrícula final |
| Camuflaje de Defiant «quizá» | **Aprobado** por el autor; seguir simulando fallos/contramedidas |
| Yate del capitán heredado | IDEA-0004 **descartada**, IDEA-0010 prevalece |
| Hangares indefinidos | Gran hangar anillo/platillo + 2 pequeños sección de batalla; geometría final pendiente |
| Conocimiento remoto perfecto de mandos/IA | Observaciones por actor con tiempo/permiso; CoreRPG es autoridad |
| Triple escudo implica energía infinita | Capas condicionadas a fuentes/circuitos y daño |
| Escudo táctico y deflector son idénticos | Reglas separadas incluso ante fallos |
| Conocer Borg/Delta desbloquea DLC | Documentación ≠ spawn/portal/desbloqueo |
| Toda estación ofrece todo servicio | Capacidades por módulos, operador, inventario y causalidad |
| Toda clase de una civilización comparte equipamiento | Diferencias por época/clase/refit/individuo obligatorias |

## 4. Autoridad y compatibilidad con lo ya construido

LORE-02 A no duplica ni sustituye:
- Matriz de época `sistemas/gameplay/ship_operations/era_technology_matrix.json` (sirve de referencia a periodos históricos, no bloquea el canon propio decidido).
- Reglas de potencia `sistemas/gameplay/ship_operations/power_allocation_model.json`, de propulsión, transportadores, sensores y permisos.
- Catálogo de naves no federadas `mundo/lore/starships/classes/non_starfleet_core_starship_classes.json`.
- Gramática y pipeline de instalaciones bajo `sistemas/universe/generation/`.
- Contratos autoritativos de CoreRPG sobre estado, visibilidad, acciones y persistencia.
- Plan de ambientes UE5, escenas modulares, interiores y activos originales.

La IA conversacional propone, interpreta y redacta; **no ejecuta por sí misma reparaciones, transporte, combate, descubrimientos, curaciones ni construcciones**. Solo un futuro adaptador de juego a CoreRPG/Host podrá resolver esas transiciones.

## 5. Qué queda abierto y por qué NO bloquea el cierre documental

**No quedan las ocho lagunas de investigación general sin respuesta.** Sí existen detalles específicos de ingeniería/realización que requieren etapas posteriores:

- Prestaciones numéricas de cada clase y balance real (velocidad warp, consumos, tiempos, magnitudes, dotación).
- Diseño definitivo y capacidad de plazas de los hangares e integración 3D de puertas, placas, barquillas y generadores.
- Dotación, nombre/matrícula final de la nave auxiliar, ubicación exacta del anclaje y funcionamiento visual UE5.
- Traducción de fichas a **contenido ejecutable Star Trek** adaptado a CoreRPG y pruebas en MSI.
- Ampliación de clases/estaciones a medida que el juego cree nuevos operadores o misiones.
- Protocolos especializados de Medicina/Ciencia personal, previstos en LORE-02 B/C/D, que no deben falsamente declararse terminados con A.

No se requiere producir una cifra inventada para declarar suficiente la investigación **cualitativa**. Si la auditoría encuentra contradicción bloqueante se reabre A antes de fusión.

## 6. Puertas de aceptación

1. Validaciones v0.1 y v0.2 correctas, incluyendo regresiones LORE-01 C/D/E y tests negativos.
2. 14 + 45 sistemas con identidad y límites; 9 operadores; 14 familias de instalaciones; 50 casos.
3. Registro de fuentes completo, sin IDs huérfanos, y distinción `OFFICIAL_REFERENCE` / `RELIABLE_SECONDARY` / `GAME_ADDITION`.
4. LORE-01 A–E íntegra y DLC Delta **sin activar**.
5. Revisión humana y autorización de fusión de PR #31; solo entonces marcar A `COMPLETE` y comenzar B en `main`.

**Conclusión:** se recomienda llevar **LORE-02 A a `NEEDS_REVIEW`**, nunca directamente a `COMPLETE` antes del visto bueno del autor y la fusión en `main`. El objetivo de autoría/investigación del alcance actual queda cubierto; todo lo que requiere ejecución o datos de una nave individual permanece correctamente clasificado como futura integración.
