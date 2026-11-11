# F11-P03 — Evaluaciones, ascensos y preparación garantizada de oportunidades (v1)

**Fecha:** 11-11-2026. **Madurez:** diseño + contrato + motor de referencia puro en Python; **NO** motor de ascensos real en CoreRPG ni escenas UE5.  
**Dependencias:** F03 persistencia, F04 plazas y dotación, F05 autoridad/órdenes, F10 Academia; F11-P01 jerarquía, P02 plazas y ofertas, P04 sucesiones de NPC, P05 integración efectiva.

## 1. Decisión autoral que gobierna P03

El personaje puede aspirar voluntariamente a una carrera **gradual, pero orientada a alcanzar la capitanía de la USS Enterprise NCC-1701-D modernizada**. **No** se aceptan esperas indefinidas, ascensos por XP, promociones automáticas cada cierto número de meses, «matar al primer oficial» ni traslados improvisados para hacer sitio al protagonista.

**Condición de progreso:** mientras el personaje permanezca activo, elija continuar su carrera, cumpla las exigencias profesionales razonables y el reloj ficticio avance, el juego **debe generar oportunidades suficientes** para ascender. Si una plaza necesaria está ocupada, el juego prepara con antelación una sucesión profesional **verosímil** para el NPC; solo tras su relevo efectivo podrá ofrecerse esa plaza. La promoción del grado **puede** hacerse sin cambio inmediato de puesto o nave; el acceso a jefatura, primer oficial o capitán requiere un nombramiento independiente.

El destino **final de carrera** no es el final del juego: se debe disfrutar durante tiempo significativo el mando de la Enterprise-D.

### Qué se garantiza y qué no

- **Garantizable por el planificador P03 de referencia:** al recibir hechos válidos y constatar que el personaje está preparado, siempre produce o mantiene una propuesta identificable de siguiente oportunidad dentro de un horizonte ficticio configurable. No depende de RNG ni de que la nave de destino ya tenga una vacante. Si el plazo se cumple sin resolverla, devuelve estado de **escalado urgente** para que P04/Host preparen alternativas.
- **Por garantizar realmente en P04/P05:** generación causal de oportunidades de NPC, emisión de ofertas auténticas, ascensos efectivos autorizados, ausencia de bloqueo indefinido y consistencia tras guardar/cargar. No sería honesto afirmar que esto ya ocurre dentro de la partida.
- **Nunca garantizado en contra de la voluntad del jugador:** si rechaza, pospone o decide no ascender. Una sanción o falta de capacitación tampoco se salta: el director debe ofrecer vías de formación, revisión y recuperación, no trucar el expediente.
- **La necesidad de servicio de Flota no puede servir de excusa permanente** para detener un avance razonable, pero sí condiciona las vías narrativas que el sistema prepara.

## 2. Progresión y ritmo ficticio

`alférez → teniente júnior → teniente → teniente comandante → comandante → capitán`.

El progreso **no emplea XP global ni barras de nivel**. Se evalúan hechos del juego: guardias, misiones, mando de equipos, entrenamiento, liderazgo, cualificaciones, observaciones de superiores, felicitaciones, errores, disciplina, responsabilidad y antigüedad.

Los parámetros del contrato `f11_p03_progression_policy_v0.1.json` se expresan en **meses ficticios de servicio** y son **exclusivamente ilustrativos para probar el algoritmo**. Por ejemplo, el simulador usa 12/12/18/24/24 meses mínimos por tramo y un horizonte de preparación de nueve meses desde que se registra la aptitud. **No son los plazos definitivos aprobados del videojuego.** Podrán ajustarse y equilibrarse con temporadas, saltos temporales y disfrute de cada cargo; no se comparan con horas reales de uso.

La evaluación profesional puede adelantarse o demorarse por méritos y acontecimientos, sin crear un «reloj de ascenso por decreto». El reloj ficticio no causa el ascenso: activa revisiones y deberes del director.

## 3. Estados y circuito de decisión

1. **NOT_DUE:** el personaje todavía está viviendo su etapa profesional mínima ilustrativa.
2. **REVIEW_PREPARATION_REQUIRED:** corresponde una evaluación del superior y faltan evidencias formalizadas; se programa revisión sin inventar un dictamen.
3. **TRAINING_PREPARATION_REQUIRED:** faltan competencias o una evaluación pide mejora; se propone mentoría, formación y nueva valoración. Una medalla no sustituye cualificaciones.
4. **DISCIPLINE_RESOLUTION_REQUIRED:** una sanción activa exige resolución/revisión de autoridad; no se promociona por la puerta de atrás.
5. **FITNESS_SUPPORT_REQUIRED:** el estado médico impide ciertos destinos; requiere apoyo y reevaluación profesional, **no** una sanción.
6. **PAUSED_BY_PLAYER:** el jugador ha optado por no continuar o ha aplazado oportunidades; no forzar el avance.
7. **READY_ANCHOR_RECORD_REQUIRED:** está preparado, pero falta registrar de forma duradera cuándo comenzó la preparación; el sistema debe registrar ese hecho en Core antes de producir planes con plazo.
8. **PLAN_PREPARED:** propuesta causal para la siguiente evaluación/oferta profesional; el rango sigue igual.
9. **PLAN_ALREADY_ACTIVE:** ya existía una propuesta del mismo tramo y personaje; **no duplicar oportunidades** cada vez que se abre el expediente.
10. **PLAN_URGENT:** venció o se alcanzó el horizonte ficticio; P04 debe replanificar/escalar, no seguir esperando pasivamente. No otorga el rango.
11. **CAPTAIN_POSITION_HANDOFF:** ya tiene grado de capitán; P04 debe preparar la **oportunidad de mandar la Enterprise-D**, que es un puesto y destino, no otro grado.

Una propuesta puede decidir la clase de oportunidad: revisión rutinaria de Flota; liderazgo o jefatura; selección para capitán de otra nave; posterior sucesión del mando de la Enterprise-D. La composición concreta de viajes, contactos, candidatos NPC y vacantes corresponde a P04.

## 4. Por qué el «anclaje de aptitud» es esencial

Ejemplo ilustrativo:

- Mes ficticio 36: el oficial cumple condiciones y se registra `ready_since_month=36`.
- Horizonte configurado de 9 meses ficticios: fecha objetivo = mes 45.
- Mes 39: el planificador mantiene la **misma** oportunidad sin duplicarla.
- Mes 45: si todavía no hay vía de progreso preparada o ha quedado atascada, aparece **PLAN_URGENT**.
- Mes 60: el director **no** reinicia el plazo ni borra la obligación. Continúa exigiendo solución.

La identidad del plan deriva de `character_id + rank_event_id + rango_siguiente + objetivo_profesional`, y **no** de la fecha de consulta, el generador aleatorio o la revisión del mundo. Un ascenso efectivo, registrado por Core, genera otro evento de rango, lo que abre un episodio profesional distinto. Una «recomendación de ascenso» nunca altera ese evento.

**Precisión:** P03 garantiza que la propuesta y la alarma no desaparezcan; la resolución en un plazo aceptable solo quedará acreditada cuando P04 y P05 demuestren que las sucesiones y órdenes realmente avanzan.

## 5. Evaluaciones y autoridad

Reutilizar `evaluations/evaluation_cycle.json` (competencia, procedimiento, iniciativa, liderazgo, equipo, criterio, fiabilidad, conducta, adaptabilidad) y `mission_performance_evidence.json`. Los méritos son evidencias, no multiplicadores de XP.

La evaluación requiere:

- Identidad del personaje y **evento vigente del rango actual**.
- Un superior competente y **firma/autoridad verificada por Core/Host**.
- Referencias a hechos originales verificables en el expediente.
- Momento y revisión válidos; el análisis no puede basarse en un informe inventado por IA.
- Resultado profesional: `satisfactory`, `exceptional`, `development_needed` o `adverse`.

**Una evaluación firmada no es un ascenso.** La propuesta pasa a selección y orden formal cuando corresponda. El expediente histórico `service_record_model.json` ya dispone de eventos `promotion`, `disciplinary_action`, `commendation`, `qualification_awarded` y otros: P03 debe usarlos, no crear otro historial paralelo.

**Recomendaciones humanas y afinidad:** pueden influir en expedientes motivados, nunca crear cualificaciones, borrar sanciones ni imponer nombramientos.

## 6. Interfaz entre P03 y P04

Para cada oportunidad, P03 devuelve en referencia:

`plan_id, character_id (en el contexto), rank_event_id, next_rank, opportunity_kind, ready_since_month, deadline_month, urgency, proposed_events`.

P04 recibirá los planes autorizados desde Core y planificará hechos futuros *con independencia de la presencia 3D del NPC*. Ejemplos:

- **Teniente → teniente comandante:** posible nueva jefatura, sustitución de responsable por traslado, ampliación justificada de personal o itinerario de liderazgo.
- **Teniente comandante → comandante:** ascenso, permanencia como jefe de departamento, experiencia de coordinación/guardias y preparación para competir más adelante por XO.
- **Comandante → capitán:** propuesta de mando en otra nave, con plaza y nombramiento auténticos; el jugador decide aceptar.
- **Capitán → comandante de Enterprise-D:** carrera del capitán NPC que asciende a almirante y recomienda al jugador; selección de Flota y traslado legítimo.

P03 **NO** selecciona qué NPC tiene que irse, ni expulsa a nadie, ni genera una plaza libre por el simple deseo del jugador. Ese trabajo específico y garantizado de **sucesión causal de personajes** se diseña en P04. No deben aparecer muertes o sanciones injustificadas para favorecer al protagonista.

## 7. Propiedades negativas y pruebas

El evaluador `desarrollo/tools/validation/f11_p03_progression_reference.py` es deliberadamente **puro e independiente**. Solo produce respuestas de referencia; no conecta con CoreRPG, no firma órdenes y no registra ascensos.

Pruebas representativas:

- Ninguna cantidad de XP altera un resultado.
- Un evento de mérito sin evaluación válida no basta.
- Una evaluación sin autoridad, de otro personaje, de un grado anterior o de un tiempo imposible se rechaza.
- Una sanción activa exige trámite; un estado médico se gestiona como apoyo.
- Las cualificaciones de mando se exigen antes de preparar la vía correspondiente.
- Una renuncia voluntaria suspende el avance sin cancelar la carrera.
- Dos consultas del mismo expediente no crean dos planes.
- Revisión del mundo y paso de los meses no reescriben el identificador del plan.
- Cumplido el horizonte, siempre se exige escalado; no desaparece la obligación.
- Simulación de cinco rangos con **órdenes de ascenso ficticias externas**: el motor propone una oportunidad en cada etapa, pero **él no cambia ningún rango**.
- Ser capitán de grado **no significa** ser capitán de la Enterprise-D.

**La prueba de propiedad más importante**: para un expediente que sigue siendo apto y no renuncia, si avanzan los meses ficticios, el estado pasa de propuesta normal a propuesta urgente, **nunca a silencio o espera indefinida**. Esto prueba el comportamiento del planificador de referencia, no la promesa completa de ascensos jugables.

## 8. Validaciones que deben hacerse en F11-P04/P05

- P04 debe proveer al planificador una política de sucesiones **con restricciones de NPC**: idoneidad real, ofertas alternativas, consentimiento de los involucrados cuando corresponda, tiempo de preaviso, nuevos destinos y relevo formal.
- Replanificación tras fracaso, desistimiento de un NPC o cambio de misión, manteniendo obligación activa y evitando secuencias inventadas.
- P05 debe demostrar en CoreRPG que las propuestas generan eventos auténticos idempotentes, sobrevivientes a guardado/carga, que no duplican plazas y que no aplican rangos antes de orden.
- Probar campañas completas y caminos alternativos con interrupciones, denegaciones, NPC que rechazan una oferta, bajas, cambios de nave y reconciliación temporal.
- El equipo/usuario deberá decidir el **ritmo final**: años ficticios en cada puesto, relación con temporadas y cuánto tiempo vivir como capitán de la Enterprise-D.

No marcar F11 `UE5_JUGABLE` ni alterar `ESTADO_GLOBAL.json` por tener documentos y Python. Los resultados CI solo permiten reclamar **REFERENCIA_PROBADA** cuando se verifiquen.
