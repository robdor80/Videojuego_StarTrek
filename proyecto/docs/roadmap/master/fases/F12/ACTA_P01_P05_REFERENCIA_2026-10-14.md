# F12 — Acta de preparación autónoma P01–P05 (referencia offline)

**Fecha:** 14-10-2026. **Rama:** `feat/f12-shipboard-social-reference-20261014`.  
**Base de partida:** `main@df71e38f7c5fe0261a6a86006008d15f1788303c` (F11 fusionada).  
**Madurez:** diseño y referencia comprobable, **no** `CORE_INTEGRADO`, `UE5_JUGABLE` ni aceptación final.  
**Fase principal:** F02 sigue EN_CURSO; F12 sigue PLANIFICADA globalmente, sin marcar P01–P05 como cerrados.

## 1. Fuentes auditadas que permanecen intactas

Se han revisado y NO se reemplazan:
- `sistemas/gameplay/characters/character_runtime_model.json`: identidad individual; rango ≠ puesto; historia persistente.
- `sistemas/gameplay/characters/activity_schedule_model.json`: disponibilidad, tránsito, descanso, obligaciones y no simultaneidad.
- `sistemas/gameplay/ship_operations/crew_manifest_model.json`, `sistemas/gameplay/duty_system/shipboard_watch_generation_contract_v0.1.json`: dotación, turnos y mando, sin fabricar sustitutos para plazas vacantes.
- `sistemas/gameplay/ship_operations/off_watch_obligation_model_v0.1.json` y `sistemas/gameplay/ship_operations/off_duty_activity_catalog_v0.1.json`: obligaciones reales, instalaciones y ocio condicionado a recursos.
- `sistemas/gameplay/characters/wellbeing/habit_state_model.json` y `sistemas/ai/memory/character_memory_contract.json`: fatiga, hábitos, memoria y atribución por personaje.
- `sistemas/gameplay/social/social_event_rules.json`, `social_simulation_lod.json`, `social_knowledge_propagation.json`, `relationship_graph_model.json`: cambios direccionales, información parcial, LOD A/B/C.
- `sistemas/gameplay/relationships/relationship_change_provenance_contract.json`: no crear lazos profundos por simple vecindad.
- `sistemas/gameplay/personality/persistent_personality_profile_contract_v0.1.json`: no regenerar personalidad durante el LOD.
- `sistemas/gameplay/social/adult_heterosexual_relationship_canon_v0.1.json`: restricciones autorales de las mecánicas románticas/sexuales para este proyecto, edad adulta y consentimiento; no restringen amistad ni cooperación.
- `proyecto/docs/roadmap/academy_life_social_simulation_plan_v0.1.md`: Academy Life 20/20 en referencia, no integración operativa con UE5 ni justificación de relaciones nuevas a bordo.

## 2. Entregables por paso

| Paso | Entrega en esta rama | Límite explícito |
|---|---|---|
| **F12-P01** | Tabla de reutilización anterior; instantánea de tripulantes individuales con ID estable, destino, localización, LOD, estado de turnos y edad equivalente | No genera NPC, salud, personalidad o biografías; Core es dueño del estado persistente |
| **F12-P02** | `screen_activity`: cribado de ocupación temporal, descanso/guardia, consentimiento de actividad conjunta, capacidad, facilidades de la nave y ubicación presente | No reserva, cancela ni prioriza turnos; no teletransporta al NPC; viajes y descansos biológicos necesitan Core |
| **F12-P03** | `screen_social_event` exige fuente causal y contacto; `project_event_for_npc` separa participante/testigo/desconocido; consentimiento romántico contextual y acciones explícitas del jugador | Fuente del fixture no autenticada. Nunca confirma amistad, atracción, hostilidad, secretos ni autorización por entrada de UI/IA |
| **F12-P04** | `render_lod_plan`: presupuesto de actores 3D con prioridad A/B/C, guardando población individual íntegra | Es lista de representación, no spawning, Unreal streaming, NPC mesh ni rendimiento medido |
| **F12-P05** | `replay_reference`: cronología determinista hasta 24 meses, eventos causales, traslado entre naves, relaciones direccionales y huella SHA-256; sin eventos no hay evolución social | No es un save/load de Core; las causas son testimonios offline sin verificación, no demuestra simulación autónoma mensual ni memoria en partida |

**Archivos nuevos:**
- `desarrollo/tools/validation/f12_shipboard_reference.py` — comprobador/ejecutor **sin mutaciones** del estado recibido.
- `desarrollo/validation/fixtures/f12/f12_shipboard_scenarios_v0.1.json` — 45 escenarios inventados y explícitamente **NO CANON**, con Miranda/Intrepid ficticias, tripulación ficticia y casos negativos.
- `desarrollo/tools/validation/test_f12_shipboard_reference.py` — batería independiente de regresión.
- `.github/workflows/f12-shipboard-reference.yml` — Python 3.12 y evidencia JSON; no inicia UE5.

## 3. Invariantes y barreras comprobables

1. Un `character_id` materializado sobrevive a cambios de nave y distintas prioridades LOD; degradar renderizado no borra vida anterior.
2. No se crean personajes solo por acercarse el jugador: población y lista de presencia son conceptos diferentes.
3. Ausencia o cambio de localización no permite ignorar la obligación, el tiempo de desplazamiento, la capacidad o los turnos.
4. Un espacio sin holocubierta no puede ofrecer actividad de holocubierta, aunque la IA la sugiera.
5. El jugador no obliga a nadie a aceptar encuentros sociales ni libera tiempo del NPC por iniciar conversación.
6. Encuentros en el mismo sitio no producen amistad automática; colaboración profesional no da intimidad ni atracción.
7. Evento romántico: adultos, pareja compatible con el canon bloqueado, acción específica si participa jugador y consentimiento contextual en compromisos/intimidad. La selección **no** crea deseo ni consentimiento.
8. Testigo solo conoce que ocurrió una interacción, no su contenido privado; no se expone el grafo global.
9. Después de un traslado, un encuentro entre naves necesita prueba explícita de contacto; historia previa y memoria no se reescriben.
10. Un evento inventado, duplicado o fuera del horizonte no es evidencia válida de evolución.
11. Toda salida calculada por la herramienta devuelve `OFFLINE_REFERENCE_ONLY_NO_MUTATION`; `REVIEW_REQUIRED` significa **pendiente**, nunca `APPROVED`.

## 4. Evidencias y comandos

El workflow ejecuta:
```bash
python -m py_compile desarrollo/tools/validation/f12_shipboard_reference.py desarrollo/tools/validation/test_f12_shipboard_reference.py
python -m json.tool desarrollo/validation/fixtures/f12/f12_shipboard_scenarios_v0.1.json >/dev/null
python desarrollo/tools/validation/f12_shipboard_reference.py --scenario desarrollo/validation/fixtures/f12/f12_shipboard_scenarios_v0.1.json --output desarrollo/validation/results/f12_shipboard_offline_report.json
python -m unittest discover -s desarrollo/tools/validation -p 'test_f12_*.py' -v
```

**Resultado:** a confirmar con la CI del HEAD/PR de esta rama; no declarar PASS hasta comprobar la ejecución.  
**Ensayo UE5/MSI:** `NO_EJECUTADO`. **Integración CoreRPG:** `NO_EJECUTADO`. **Meses simulados en mundo autoritativo:** `NO_EJECUTADO`. **Persistencia entre sesiones reales:** `NO_EJECUTADO`. **Rendimiento 300–1.000 NPC:** `NO_EJECUTADO`.

## 5. Propiedad e integración futura (bloqueos de cierre)

- **CoreRPG**: tiempo y planificación excluyente, economía de acciones, identidades, evento causal confirmado, relaciones y conocimiento direccionales, control de privacidad, persistencia/guardado y memoria. Auditar sus APIs existentes antes de crear adaptadores; los campos de esta referencia **no son una API oficial CoreRPG**.
- **Star Trek Host**: política de servicio, cuadrantes aprobados por capitán, recursos/capacidad de la nave, canon social cerrado y reglas sociales específicas de Flota. Debe validar la fuente y permisos, no aceptar `cause_event_ref` enviado por UI/IA como prueba.
- **UE5 MSI**: visualización bajo demanda de NPC presentes, colisiones, conversaciones, interacción con camarotes, instalaciones y estrés de memoria/CPU/GPU; nunca se asume spawn probado.
- **IA remota**: puede proponer frases o interpretar estados autorizados, jamás crear una cita, transferencia, consentimiento, secreto o memoria verificable a partir de texto.
- **Aceptación posterior**: pruebas E2E con guardias y descanso real, alarmas/relevos, trayectos dentro de nave, amistad NPC↔NPC nacida de eventos confirmados, revelaciones privadas y meses sin el jugador; save/load real y traslado que preserva vínculos; actores A/B/C visibles bajo demanda y medición en MSI.

## 6. Decisiones de autor

No se han tomado nuevas decisiones creativas. Se conserva el canon social ya aprobado, sin ampliarlo ni introducir mecánicas nuevas como hechos definitivos. Propuesta futura: decidir en sesión de diseño la granularidad de simulación mensual, límites de coste CPU y los plazos de caducidad de reservas sociales; no se fijan aquí como cánones.

**Criterio de revisión de esta PR:** fusionar únicamente la **preparación verificable de referencia** si GitHub Actions y la auditoría pasan; nunca declarar F12 finalizada, Core integrado ni NPC UE5 jugables por ello.
