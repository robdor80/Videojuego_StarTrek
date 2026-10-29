# LORE-04A / A06 — Rutinas civiles, LOD, vida fuera de pantalla y persistencia

**Estado:** CANDIDATE_COMPLETE_DOCUMENTARY; no implementación de scheduler, motor social, inventario ni WorldState. **Autoridad:** CoreRPG exclusivamente. **Propietarios de contratos:** población persistente, social LOD, memoria, agendas y movimientos preexistentes.

## A06.1 Jerarquía de resolución de realidad (sin nuevo sistema)

El presente documento es una tabla de aplicación de:
- `sistemas/universe/generation/persistent_population_materialization_rules.json`: población latente A/B/C, identidad irreversible y pertenencia a estructura real.
- `sistemas/gameplay/social/social_simulation_lod.json`: LOD social A/B/C, profundidad independiente de existencia.
- `sistemas/gameplay/social/social_event_rules.json`: posibles transiciones sociales condicionadas.
- `sistemas/gameplay/social/social_knowledge_propagation.json`: conocimiento por observador y canal.
- `sistemas/universe/generation/population_movement_contract.json`: movimiento de residencia, viajeros y visitantes.
- `sistemas/gameplay/careers/academy_path/life/academy_offscreen_life_contract_v0.1.json`: ejemplo de criterios de catch-up ya cerrados en Academia; **no** lo expandimos a motor civil sin autorización y dependencia CoreRPG.

**Peligro de nomenclatura:** A/B/C de *población* y A/B/C de *LOD social* se refieren a conceptos **diferentes**. Un NPC persistente B puede recibir detalle social A por relevancia, sin regresar nunca a población anónima C. Ningún cambio de detalle borra identidad, causalidad o recuerdos previamente confirmados.

## A06.2 Modelo de consulta documental

| Pregunta | Fuente previa | Prohibición |
|---|---|---|
| ¿Existe la persona? | población y `character_id` materializado / plaza latente | inventar vecino por demanda |
| ¿Dónde reside / trabaja? | hogar y puesto/operador en WorldState | ubicación por conveniencia del guionista |
| ¿Puede prestar servicio? | horario, ruta, disponibilidad, calificación, estado de local | presencia simultánea en dos lugares |
| ¿Con quién mantiene vínculos? | grafo direccional y parentesco | amistad por raza o convivencia automática |
| ¿Qué ha ocurrido fuera de cámara? | evolución / eventos persistentes de CoreRPG, si existen | hecho creado retrospectivamente por la IA |
| ¿Qué sabe cada participante? | conocimiento/canales/privacidad | revelar secretos sin fuente |
| ¿Qué ve el jugador? | observación filtrada + capacidades del cliente | convertir texto o visualización en autoridad |

## A06.3 Ejemplo de jornada (hipotético, no calendario canon)

Un hogar de dos residentes en una colonia con instalación sanitaria ya materializada:
- **Tramo inicial**: quien está de servicio utiliza la ruta disponible al centro; el familiar que está libre permanece en vivienda si no existe plan distinto.
- **Tramo intermedio**: servicio sujeto a demanda, colegas y suministros; no puede atender a otro centro remoto a la vez.
- **Tramo posterior**: puede producirse invitación social respaldada por disponibilidad de los participantes, lugar y consentimiento relevante; un diálogo no crea por sí solo amistad.
- **Interrupción**: avería real de energía cambia la posibilidad del turno y puede generar solicitud de mantenimiento; no garantiza reparación. Si falta el evento causal, el servicio permanece como estaba.
- **Fuera de cámara**: el tiempo puede avanzar usando las reglas implementadas por CoreRPG y conservar consecuencias. Si aún no hay integración, el ejemplo sigue siendo especificación conceptual.

No se fijan horas 08:00–17:00, duraciones laborales ni «fines de semana» universales; la localización y escala temporal pertenecen al modelo del mundo.

## A06.4 Determinismo, ahorro de recursos y eventos

Una población agregada puede cubrir un barrio de tamaño grande sin asignar 100.000 psicologías completas. Si un residente pasa a personaje individual, debe surgir de un puesto/población ya existente y conservar un ID estable. La materialización **no** crea otro residente; cambiar nivel de detalle **no** causa traslado ni envejecimiento adicional. Una vez confirmado un suceso relevante (lesión, nacimiento, muerte, pérdida de trabajo, disputa contractual, cambio de domicilio), no se puede reemplazar por un resultado diferente al cargar partida.

Los resultados de simulación fuera de cámara deben ser causales, ordenados y deterministas con semillas/IDs aprobados. Los hechos mayores requieren eventos explícitos, no acumulación de puntos por inactividad. Las propuestas de IA quedan sujetas a validación; su ausencia no implica que un NPC deje de existir.

## A06.5 Escenarios negativos de aislamiento temporal

1. **Salto de partida**: dos jornadas renderizadas no deben generar dos personas con el mismo puesto si solo hay una plaza.
2. **Viaje mientras trabaja**: un civil no puede estar «de guardia» en estación y simultáneamente en superficie sin desplazamiento autorizado.
3. **Cerrar sesión en plena conversación**: al reabrir, la relación y el tiempo real guardado no se rerollean por distinta semilla de diálogo.
4. **LOD bajo**: no desaparecen la deuda histórica, un accidente documentado ni los familiares.
5. **Rumor**: llegar a oídos de un NPC requiere canal y cronología plausibles; el rumor conserva duda y no modifica la verdad.
6. **Cambio político tras inicio**: una ley/autoridad nueva solo puede afectar actividades posteriores si se produjo un evento válido; no se impone el canon futuro externo.
7. **Academia y sociedad**: la vida en Academia usa sus 20 paquetes cerrados; en otros territorios se reutilizan **patrones**, no registros/copias del campus.

## A06.6 Fronteras de desarrollo

A06 **no** define ticks, fórmula de productividad, estructura de colas, subsistema de ahorro, planificación avanzada, contratos ni motor temporal. Lo que sigue pendiente es integración CoreRPG y evidencia ejecutable; su falta no equivale a hueco de lore ni permite afirmar que una ciudad viva esté operativa. Ver A08.
