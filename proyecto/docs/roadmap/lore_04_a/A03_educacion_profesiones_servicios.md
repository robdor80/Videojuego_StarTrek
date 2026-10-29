# LORE-04A / A03 — Educación civil, profesiones y servicios cotidianos

**Estado:** CANDIDATE_COMPLETE_DOCUMENTARY; autor y PR Draft pendientes. **Alcance:** época TNG/DS9/Voyager, continuidad abierta y jurisdicciones variables. **Fuentes:** `lore04a_evidence_ledger_v0.1.json` (LA-E03, E04, E06, E09, E13), LORE-01, LORE-02 y contratos existentes.

## A03.1 Regla de causalidad del empleo y los servicios

Una ocupación es una relación entre **persona** y **función autorizada**, dentro de **entidad/instalación/institución existente**, en **jurisdicción y época compatibles**, con **capacidad, horario y recursos**. La función puede ser vocacional, comunitaria, asignada, remunerada, familiar o mixta dependiendo de la cultura y el contexto: no fijar salario, pago, beneficio ni régimen de propiedad por defecto.

Secuencia documental de validación (sin implementar nuevo runtime):
1. Resolver entidad poblacional, establecimiento y función **ya existentes** en WorldState.
2. Comprobar operador, competencia organizativa, legalidad, tecnología y habilidades necesarias.
3. Comprobar disponibilidad individual, desplazamiento, turno y servicio efectivo.
4. Consultar capacidad, recursos y límites de acceso, incluidos parámetros de accesibilidad.
5. Exponer al observador exclusivamente el resultado observable y su conocimiento autorizado.
6. Mutaciones/eventos reales —nombramiento, consumo, reparación, traslado, fallo, sanción— solo mediante CoreRPG.

Contratos propietarios: `sistemas/universe/generation/persistent_population_materialization_rules.json`, `settlement_infrastructure_contract.json`, `sistemas/gameplay/logistics/resource_inventory_state.json`; no duplicar `Academy Life`.

## A03.2 Educación y socialización

| Contexto | Hecho/evidencia | Regla documental, NO legislación inventada |
|---|---|---|
| DS9, escuela de Keiko | LA-E03: escuela y controversia religiosa en *In the Hands of the Prophets* | Institución civil, comunidad, autoridad educativa, enseñanza y diferencia de creencias requieren identidad distinta; una persona religiosa no representa por defecto al gobierno |
| Entornos familiares | LA-E01 y LA-E04: convivencia y transmisión de tradiciones familiares | No derivar currículo, tutoría legal ni aprendizaje obligatorio de la composición doméstica |
| Academia de Flota | `academy_life_final_closure_v1.0.md`: 20/20 paquetes documentales | Es educación de servicio de una organización específica; nunca sustituir todo sistema educativo civil de la Federación |
| Colonias generadas | `settlement_infrastructure_contract.json` incluye dominio `education` | Colegio o centro solo si la población, ubicación, tecnología, operadores y capacidad justifican su existencia; puede carecer de algunos servicios |
| Sociedades no federales | Perfiles culturales de LORE-01 y gramática de gobierno | No convertir especies en currículos: centros religiosos, públicos, familiares o privados son **posibilidades a evidenciar**, no modelos universales |

**Desconocido:** edades y duración exactas de escolarización por cada planeta, financiación, convalidaciones de estudios y autorización parental. A03 no las define.

## A03.3 Familias ocupacionales y dependencias

| Familia de actividad | Condición para aparición | Necesidad visible | Evitar |
|---|---|---|---|
| Sanidad y cuidados | población, clínica/sanador, competencias, insumos y acceso | atención, turnos, recursos agotados, derivación | atención instantánea ilimitada |
| Enseñanza e investigación civil | alumnado, tutores, centro, curriculum/contexto autorizado | clases, cierres, investigación, efectos sociales | academia de Flota para cualquier niño |
| Agricultura, alimentación, restauración | tierra/recursos/instalación/operador y demanda | abastecimiento, cocina, cultivo, ocio | concluir que replicador elimina oficios |
| Construcción, reparación, mantenimiento | infraestructura, fallo/necesidad y habilidades | técnicos en ruta, cierre temporal, recambios | reparar con assets inventados |
| Administración, justicia y mediación | órgano competente y jurisdicción aplicable | trámites, disputas, reclamaciones | oficiales de Flota asumiendo juez civil |
| Comercio, transporte y servicios | operador, ruta, inventario, intercambio y ley | entregas, desplazamientos, horario de local | comerciantes materializados porque jugador quiere vender |
| Arte, comunicación, deporte, hostelería | participantes, recursos, lugar y horarios | evento, espectadores, interacción social | cualquier personaje disponible 24/7 |

Los ejemplos no atribuyen a una cultura específica los porcentajes de trabajadores; tampoco asignan a una persona la profesión que «corresponde» a su especie.

## A03.4 Servicios públicos, mixtos y privados

**No imponer** privatización ni gratuidad universal. El `service_ref` debe apuntar al servicio existente; `institution_ref` identifica responsabilidad; `access_rule_ref` solo si está normativamente establecido; `availability_state` y `resource_state` provienen del WorldState. La denominación pública, privada, mutual, religiosa o comunitaria precisa contexto jurídico real. Si no hay evidencia, el modelo es `UNKNOWN`, no «público federado por defecto».

- Un local puede abrir sin que el propietario esté presente si hay empleados autorizados; la IA no finge que un empleado ausente atendió.
- Las reservas de capacidad, emergencias y cambios de turno requieren eventos causales; las colas y aforos no son cosméticos.
- La asistencia médica se enlaza con LORE-02C y no permite diagnósticos narrativos creados por IA.
- La movilidad de alumnos/pacientes/personal usa rutas reales, no teletransporte gratuito por conveniencia.
- En territorios con posguerra o escasez, los servicios pueden estar degradados con causa e historia, sin asignar miseria a todos sus ciudadanos.

## A03.5 Casos de comprobación

**CIV-A03-01 — Escuela y comunidad (escenario GAME_ADDITION de prueba):** existir centro, docente, alumnado y conflicto de interpretación acreditado por actores distintos; educación y competencia religiosa no se mezclan; una protesta no genera automáticamente ley. Referencia de investigación LA-E03.

**CIV-A03-02 — Clínica con interrupción:** la persona solicita una consulta, pero el centro carece de energía o personal; respuesta válida: espera, rechazo o derivación basada en rutas existentes. Prohibido inventar médico, equipo o teletransporte.

**CIV-A03-03 — Reparación doméstica:** técnico civil acepta una reparación solo si hay solicitud, disponibilidad, desplazamiento, piezas y acceso legal. Un acuerdo no repara el objeto antes de la resolución autoritativa.

**CIV-A03-04 — Exresidente de zona de conflicto:** el oficio actual de un civil cardassiano no se determina por la antigua autoridad ocupante ni por culpa colectiva; *Duet*, LA-E09, es una alerta contra generalizaciones, no una plantilla para cualquier biografía.

## A03.6 Cierre y reservas

Listo como **dossier de diseño y contexto**, no como sistema educativo o laboral implementado. Pendientes de otra fase: economía y remuneración (04B), transportes y centros (04C), competencias legales (04D). No hay decisión de autor para edades escolares universales, sueldo, código profesional, servicios gratuitos o régimen jurídico nuevo.
