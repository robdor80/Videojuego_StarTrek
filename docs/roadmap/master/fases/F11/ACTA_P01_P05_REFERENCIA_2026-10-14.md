# F11 — Acta de preparación verificable P01–P05

**Fecha:** 14 de octubre de 2026  
**Estado real:** REFERENCIA DE CARRERA IMPLEMENTADA, aún **no** UE5_JUGABLE / CORE_INTEGRADO.  
**Rama de entrega:** `feat/f11-career-fleet-reference-20261014`.  
**Fase principal del roadmap:** F02 EN_CURSO; F11 continúa PLANIFICADA globalmente.

## 1. Auditoría de fuentes conservadas

No se han modificado ni sustituido los contratos originales de:
- `gameplay/careers/academy_path/first_assignment_model.json` y `graduation_model.json`;
- `gameplay/careers/starfleet_service/career_progression_rules.json`;
- `gameplay/careers/assignments/assignment_transition.json`;
- `gameplay/careers/promotions/promotion_pipeline.json`;
- `gameplay/careers/service_record/career_state.json` y `service_record_model.json`;
- `gameplay/careers/evaluations/evaluation_cycle.json`;
- `gameplay/careers/post_academy/`, `transfers/` y `chain_of_command/`;
- `lore/starships/classes/core_starship_classes.json`;
- `docs/roadmap/master/fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md`.

Se ha comprobado su significado, diferenciando *elegibilidad*, *recomendación*, *vacante*, *orden de destino*, *mando provisional* y *nombramiento de capitán*. Las notas y datos nuevos se sitúan junto al material existente sin migraciones destructivas.

## 2. F11-P01 — Rutas profesionales y cronología

Contrato de referencia: `gameplay/careers/starfleet_service/f11_route_plan_v0.1.json`.

| Ruta | Clases con ficha verificable y posibles destinos | Candidatas aún no verificadas en catálogo / pipeline |
|---|---|---|
| Ciencia/Sensores | Oberth → Intrepid/Nebula | Nova |
| Táctica/Operativa | Miranda | Saber, Akira, Steamrunner |
| Exploración/Mando | Galaxy/Sovereign | Odyssey; **Valhalla** |

**Esto no es una asignación garantizada ni una escalera obligatoria.** Por ejemplo, un alférez podría entrar en una nave grande si su campaña y la plaza lo admiten; un científico puede cambiar de especialidad. Las prioridades conservan las tres rutas aprobadas (Ciencia: Oberth/Nova → Intrepid/Nebula; Táctica: Miranda/Saber → Akira/Steamrunner; Exploración/Mando: Galaxy/Sovereign → Odyssey/Valhalla). Son afinidades de carrera, no bloqueos: una plaza válida puede seguir siendo un destino cruzado.

La disponibilidad se deriva del *catálogo de clases* y de los perfiles de época, nunca del deseo del jugador. La fecha desconocida de entrada en servicio de la nueva **Clase Valhalla** permanece desconocida: no debe asignarse silenciosamente `2372` ni ninguna otra. Las clases ausentes de la ficha canónica verificable se excluyen de la selección ejecutable por defecto. El motor offline trata `confirmed_active_from_decade` de modo conservador: la década indicada acredita presencia en algún momento de ella, por lo que un año anterior a la década siguiente exige comprobación específica.

Perfiles jugables admitidos: Pike, Kirk y TNG/DS9/Voyager, con filtros temporales y sin universos duplicados. La flota viva, las vacantes y la continuidad de campaña siguen pendientes de consulta autoritativa.

## 3. F11-P02 — Alférez y autonomía progresiva

La graduación acreditada de Academia puede **proponer** la comisión como `ensign`. Ni aprobar cuarto curso, ni completar Kobayashi Maru, ni un registro externo de academiaflota equivalen por sí mismos a la comisión y destino autoritativos. El primer destino requiere:
1. Nave operativa existente, clase disponible en la época y vacante real.
2. Puesto compatible con rango, cualificaciones y necesidad de servicio.
3. Orden de incorporación identificada y emitida por autoridad válida.
4. Responsable/supervisor y cadena de mando, agenda y relevo de guardia.
5. Alta en expediente persistente, traslado de historial y continuidad social.

Durante el primer servicio predominan guardias supervisadas, orientación a sistemas de la clase, tutoría y adquisición real de cualificaciones. **Rango y cualificación no son lo mismo**. El sistema de referencia `tools/validation/f11_career_reference.py` revisa compatibilidad; no asigna al personaje, no rellena vacantes ni otorga permisos.

## 4. F11-P03 — Evaluaciones, expediente y decisiones

Se implementa cribado reproducible para: **permanecer**, **declinar promoción**, **solicitar ascenso**, **pedir traslado**, **cambiar de puesto**, **cambiar de especialidad**, **evaluación**, **mando temporal** y **mando permanente**.

El resultado `BLOCKED` expresa precondiciones no satisfechas; `CANDIDATE_FOR_AUTHORIZED_REVIEW` identifica una plaza revisable y `REVIEW_REQUIRED` identifica una petición potencialmente coherente **no aprobada**. `NO_CHANGE` conserva el derecho del jugador a continuar donde está. Los dictámenes incluyen `OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION` de forma explícita.

Una recomendación, evidencia operacional o nota de mentor no sustituye al expediente de Core. La IA redacta, no decide ni asigna puntuaciones de verdad. Las emociones/relaciones y el favoritismo no crean rango ni cualificación; un traslado exitoso ha de conservar el historial social y profesional sin resetear relaciones ni asegurar aceptación amistosa del resto de tripulantes. La reacción de NPC, la memoria, el prestigio y consecuencias personales **no están simulados todavía**.

El mando temporal exige cualificación y referencia a orden operativa cuyo origen debe **autenticarse en el Host**. La presencia de una cadena o booleano en JSON de entrada no acredita tal autenticación. Para mando permanente se exige revisión de rango de capitán, aptitud y vacante del puesto de capitán, sin despedir mágicamente al titular.

## 5. F11-P04 — Escalera técnica de naves y producción 3D

Se diferencian **presencia en el mundo**, **clase candidata a destinos** y **nave con interiores realmente jugables**. Son tres estados distintos.

| Prioridad técnica | Clases | Puerta de modelado y prueba |
|---|---|---|
| Piloto de flota | Oberth y Miranda | Auditoría de mallas/licencias → exterior, puente e interacciones → importación aislada en UE5 → colisiones, navegación, sensores y rendimiento MSI |
| Evolución científica | Intrepid | Revisar puente Voyager/pasillos modulares, UV/PBR, interiores transitables y misión adecuada, sin reutilizar escenas a ciegas |
| Evolución avanzada | Sovereign | Aprovechar originales y trabajos de hangar ya auditados, separar decisiones sobre activos de la disponibilidad en campaña |
| Tramo grande / referencias | Galaxy, Odyssey | Su presencia en el universo no garantiza un modelo jugable ni interiores listos; pendientes activos y validación UE5 |
| Horizonte opcional | **Nueva Clase Valhalla** | Solo tras especificación/cronología aprobadas y desarrollo propio inspirado en Galaxy; **no** reinterpretarla como refit o Enterprise-D renombrada |

La **USS Sutherland** sigue siendo el puente seleccionado para la prueba v0.0.1 de Sensores, **no** una clase nueva ni una imposición sobre el primer destino del jugador. El puente Kelvin continúa reservado para trabajos posteriores.

La asignación de naves también condiciona la narrativa: una Oberth científica no recibe automáticamente misiones de gran batalla de una nave de guerra. Queda para diseño específico de temporadas/capacidades de F13 y de la propuesta aprobada correspondiente; **no** se inventan capacidades ni misiones en esta fase.

## 6. F11-P05 — Continuidad y libertad de carrera

**Recorridos de referencia comprobables:**
- Alférez apto para Sensores en Oberth o Miranda, con plaza y época compatibles.
- Alférez rechazado por vacante ocupada, cualificación no acreditada o clase fuera de época.
- Trayecto con candidatura a ascenso, siempre sujeto a revisión y evidencias.
- Permanencia indefinida sin imponer traslado, candidatura a capitán ni final de partida.
- Traslado solicitado con o sin ascenso; no se cambia automáticamente el rango.
- Renuncia a un ascenso o cambio de especialidad con formación necesaria.
- Mando temporal subordinado a orden y aptitud profesional.
- Comandante no recibe puesto de capitán por estar en el puente; Capitán cualificado tampoco recibe una nave sin vacante.
- Valhalla y Odyssey no aparecen como ofertas aptas sin ficha verificable y disponibilidad temporal. El objetivo Valhalla sigue **opcional**, no recompensado automáticamente.

**Artefactos:** `validation/fixtures/f11/f11_career_scenarios_v0.1.json` contiene 40 escenarios con resultados esperados, y `tools/validation/test_f11_career_reference.py` añade 36 pruebas unitarias. El ejecutor de escenarios genera una huella SHA-256 estable y un informe **offline**; no es una firma confiable ni un guardado de partida. Workflow: `.github/workflows/f11-career-reference.yml`.

## 7. Puertas explícitas para continuación

1. **CoreRPG**: obtener de forma autenticada actor, eventos, cualificaciones, agenda, vacantes, autoridad, decisiones y guardado/carga; definir un adaptador Star Trek sin duplicar Core. El progreso del desarrollo Core 4.9/4.10 no es certificación de integración.
2. **Host/UE5**: ejecutar comisiones, órdenes, ascensos, cambios de destino y mando en escena; vínculos sociales, diálogos y consecución o rechazo real, con NPC persistentes.
3. **Canon técnico de clases**: fichas validadas para candidatas ausentes; fechar **Valhalla** únicamente tras decisión expresa del autor. La futura ampliación no debe permitir una era incongruente.
4. **MSI**: builds y casos E2E de carrera, guardado/carga real a través de cambios de nave, opción de permanecer, continuidad de tutoría y contexto de tripulación; evidencias y mediciones.
5. **Gobierno**: mantener F11 `PLANIFICADA` hasta acreditación de su puerta `UE5_JUGABLE`. La PR se entrega para revisión y fusión de **referencia** solamente. No modificar `ESTADO_GLOBAL.json` para fingir cierre.

**No realizado:** ninguna importación 3D, ejecución CoreRPG, autoridad firmada, acceso al MSI, simulación de relaciones, save/load de partida real ni demostración UE5. La CI prueba código Python y fixtures; no prueba videojuego.
