# DEC-0024 — Sistema 18: Identidad, autenticación y control de accesos

**Fecha:** 18-11-2026. **Decisión autoral expresa:** crear un sistema independiente y asignarle número libre. **Número S18 reservado y ámbito aprobado.** **Diseño técnico detallado propuesto para implementación posterior**, todavía sin certificación CoreRPG, HOST ni UE5.

## Decisión y separación de responsabilidades

Después de los 17 sistemas de diseño ya enumerados, se añade **Sistema 18 — Identidad, autenticación y control de accesos**, transversal al videojuego Star Trek RPG. No sustituye los anteriores ni renumera la fase F12 del plan maestro.

Este sistema existe para garantizar que el pulsador de un camarote sepa **quién lo pulsa** (jugador o NPC), reconozca si es propietario, residente, visitante autorizado o personal que actúa legítimamente por una incidencia, y devuelva una decisión verificable de **abrir / llamar / denegar / requerir verificación adicional**.

No es un sistema de decoración ni un Blueprint específico del camarote del protagonista; es un servicio reutilizable en **cualquier nave, Academia, estación o instalación** cuya seguridad y topología real lo permita.

**Frontera con S12:** S12 recibe proximidad, pulsación, estados/animación de hoja, turbolift y navegación interior. **S18 resuelve identidad, permisos, invitados, revocaciones y excepciones documentadas**. La apertura concreta depende también de energía, averías, presión, bloqueo físico y estado de la puerta. S18 no anima geometría ni transporta personajes.

## Base existente que debe reutilizarse

- Personaje CoreRPG con ID estable y separado de rango, puesto, servicio, afiliación, residencia, biología y avatar: `sistemas/gameplay/characters/character_runtime_model.json`.
- Seguridad base de la computadora y separación identidad/autorización: `sistemas/gameplay/ship_operations/ship_computer/access_control_rules.json`.
- Peticiones al ordenador y rutas deterministas antes que IA: `computer_request_contract.json` y `ai_routing_policy.json`.
- Grafo y espacios/estados de interior: `interior_location_model.json` y `interior_navigation_graph_v0.1.schema.json`.
- Administración de camarotes, destinos, cambios de guardia, roles, parejas, huéspedes y emergencias desde sus fuentes Core/F11/F12 y sistema de instalaciones. **No crear una segunda base de datos de personajes o de mandos.**

El sistema de puertas automáticas de la USS Sutherland ensayado con Quinn se considera una **referencia a auditar y reutilizar en S12**, no evidencia aquí de que S18 esté implementado. El informe F07 del 23-10-2026 menciona 50/50 pruebas comunicadas de puertas y 44/44 de circulación, pero faltan logs/artefactos locales para validar el componente concreto.

## Contratos de comportamiento

1. **Pulsador privado:** evento de interacción asociado por el runtime al **actor auténtico** (jugador/NPC) y convertido por la fuente de identidad en un `character_id` verificado, no tomado de una cadena que el cliente o la IA pueda inventar. S18 consulta la autorización actual para esa puerta. Si es propietario/residente autorizado, abrir; si es invitado autorizado, abrir en sus límites; de lo contrario, **timbre/solicitud al ocupante**, no acceso automático. Respuesta de negación sin revelar información personal.
2. **Puerta pública automática:** S12 puede abrir por proximidad según política de puerta, siempre que no esté restringida y los estados físicos lo permitan. Una zona restringida debe consultar S18 aun si su detector identifica un actor válido.
3. **Identidad de ficción coherente:** sesión Core autenticada y objeto interactuante como señal autoritativa; comunicador de la Flota, terminal o biometría narrativa como señales complementarias según seguridad. La voz o mera proximidad **no prueban por sí solas** que alguien sea quien afirma ser; distintivos pueden perderse o ser sustraídos. No recolectar datos biométricos reales del usuario.
4. **Políticas dinámicas:** asignación vigente de camarote/espacio, corresidentes, visitantes autorizados con caducidad y zona, turnos, departamentos, habilitación especial, rangos y puestos por separado, acceso de mantenimiento, invitados y escoltas, revocación inmediata verificable.
5. **Privacidad:** un camarote es privado. «Soy capitán» no abre automáticamente todos los camarotes; visita y privilegios solo con base legítima. Un visitante no obtiene autorización por estar físicamente al lado de alguien autorizado ni por conocer el nombre del residente.
6. **Salida y emergencias:** el mecanismo de evacuación y seguridad de vida se modela **diferente** de la entrada. No retener personas en una zona segura por exigir huella o credencial rutinaria; despresurización, cuarentena y confinamiento pueden introducir restricciones explícitas verificadas. Aperturas de excepción a cargo de oficiales competentes o servicios automáticos autorizados, con caso/incidencia y auditoría.
7. **Estado físico:** que S18 autorice no garantiza apertura: S12/ingeniería pueden devolver `BLOCKED_PHYSICAL` por falta de energía, bloqueo mecánico, compartimentación o puerta destruida; las denegaciones físicas no significan automáticamente que el actor carezca de permiso.
8. **Persistencia y trazabilidad:** permisos y caducidades sobreviven a guardado/carga, traslados, ascensos y reasignaciones. Cada solicitud sensible tiene ID, causa, decisión, revisión de política y traza de autorización sin registrar indiscriminadamente todas las visitas privadas.
9. **Sin IA en la cerradura:** motor determinista y local; el servicio central de IA, cuando exista, puede interpretar «autoriza a Geordi una visita hoy», pero **no concede permisos** ni atribuye identidad por el texto generado.

## Escenarios representativos

- Protagonista llega y pulsa su camarote → si está realmente asignado, se abre.
- Otro miembro de la tripulación pulsa → la puerta **llama**, no se abre por ser oficial de la Flota.
- Segundo residente o invitado con permiso temporal válido → abre mientras el permiso siga vigente.
- Cambia el camarote por un ascenso/destino → antigua puerta deja de reconocer residencia; la nueva utiliza la misma identidad persistente.
- Un NPC pretende pasar por una credencial prestada → la verificación adicional puede detectar inconsistencia según política y evidencias del juego.
- Incendio y rescate médico → aplicación de autorización excepcional o evacuación conforme a la normativa del barco, con evento trazable; no conceder acceso universal por un mensaje de IA.

## Implementación, alcance y cierre

S18 deberá convertirse en política y evaluador compartido, no en un microservicio externo ni nueva fuente de verdad. Contratos propuestos:
- `sistemas/gameplay/access_control/S18_IDENTIDAD_CONTROL_ACCESOS_DISENO_v1.md`
- `s18_access_decision_contract_v0.1.json`
- `s18_door_and_room_policy_v0.1.json`
- `s18_identity_assertion_contract_v0.1.json`
- `s18_acceptance_cases_v0.1.json`
- `s18_status_v0.1.json`

**Estado:** número y ámbito aprobados, diseño de detalle registrado **como propuesta técnica**, pruebas de contrato sí; **sin autorización para declararlo implementado ni cambiar Core/UE5**. Se implementará y probará en fases con Codex, auditando previamente el subsistema de puertas Sutherland y las autoridades actuales. La PR de S12 (separada) no se fusiona ni convierte en aprobada por esta decisión.
