# Sistema 18 — Identidad, autenticación y control de accesos

**S18**, creado por decisión del autor el **18-11-2026**, es un sistema funcional y transversal de Star Trek RPG: identifica a quienes actúan y decide si pueden acceder a una estancia o instalación.

**DEC-0024:** [Decisión del sistema 18](../../../proyecto/docs/decisions/s18_identidad_autenticacion_control_accesos_2026-11-18.md)

## Responsabilidades

- Identificar al actor real de una pulsación o solicitud mediante identidad persistente Core.
- Autenticar las credenciales exigidas según el nivel de riesgo.
- Evaluar políticas de acceso para camarotes, despachos, laboratorios, armería y zonas sensibles.
- Administrar permisos delegados y temporales, residentes, invitados, caducidades y revocaciones verificadas.
- Distinguir entrada restringida, timbre, salida segura y excepciones de emergencia.
- Registrar decisiones sensibles con trazabilidad y privacidad.

**No** anima la puerta, controla la proximidad, crea el mapa de la nave ni mueve al jugador: eso corresponde al Sistema 12 (interiores y desplazamiento) y los servicios físicos de la nave. **No crea nuevas identidades**, rangos, plazas, residencias ni autorizaciones de capitán: consulta los sistemas propietarios.

## Documentación

- [Diseño funcional S18](S18_IDENTIDAD_CONTROL_ACCESOS_DISENO_v1.md)
- [Contrato de identidad y evidencias](s18_identity_assertion_contract_v0.1.json)
- [Contrato de políticas de puerta y habitación](s18_door_and_room_policy_v0.1.json)
- [Contrato de decisión](s18_access_decision_contract_v0.1.json)
- [Escenarios de prueba](s18_acceptance_cases_v0.1.json)
- [Estado real](s18_status_v0.1.json)
- [Plan de implementación](../../../proyecto/docs/roadmap/S18_IDENTIDAD_ACCESOS_PLAN_2026-11-18.md)

**Diseño documental preparado; aún no hay runtime de autenticación/puertas S18 en UE5/HOST/Core.** Las pruebas documentales no certifican puertas funcionales.
