# Sistema 18 — Especificación funcional y arquitectura de control de accesos

**18-11-2026 · Versión 1.0 de propuesta técnica.** Numeración y propósito aprobados por el autor. **Implementación pendiente.**

## 1. El problema

En una Galaxy con cientos de camarotes, cada puerta tiene propietario, posibles convivientes, invitados, servicio de limpieza, privacidad y estados de seguridad. Una puerta **no puede averiguar quién ha pulsado mirando la malla o la proximidad**. El evento de interacción debe vincularse a una persona identificada por CoreRPG y su derecho actual a entrar.

Ejemplo: el protagonista pulsa su puerta → la puerta ve la acción originada en su avatar controlado y la convierte en la identidad persistente del héroe; comprueba la asignación real; autoriza apertura. Si un NPC pulsa, se consulta la identidad **de ese NPC**, no se usa siempre el jugador como sujeto; y si carece de permiso, funciona el timbre.

## 2. Reutilización y fronteras

- **CoreRPG:** identidad `character_id`, rol/rango/puesto, residencia, permisos legítimos, tiempo y eventos de guardado; referencias de verdad autorizada.
- **Sistema 18:** reglas Star Trek de autenticación, acceso y excepciones, evaluación determinista de solicitud y recibo; sin una base duplicada de personajes.
- **HOST:** entrada confiable del evento y consulta a Core; traslado de respuesta a los consumidores y a la computadora. No reemplazar política domain-specific en Core.
- **Sistema 12 / Unreal:** `OnInteract`, `OnBeginOverlap` para puertas con sensor automático, animación de hojas, pulsador, timbre, colisiones, estado eléctrico y de seguridad, turboascensores y rutas. **S12 jamás debe permitir la apertura restringida solo por recibir una señal de trigger.**
- **Seguridad, Medicina e Ingeniería:** normas específicas de acceso/seguridad, incidentes, cuarentena, emergencia, reparación y anulación; S18 consulta esas decisiones. No se inventa autoridad por hablar con la IA.
- **Ordenador central:** usuario puede pedir autorizaciones por voz/LCARS; lenguaje natural produce una **intención propuesta**; la identidad y el permiso de conceder el acceso se verifican en S18/Core.

Contratos preexistentes que se mantienen: `character_runtime_model.json`, `ship_computer/access_control_rules.json`, `ship_computer/computer_request_contract.json`, `ship_computer/ai_routing_policy.json`, `interior_location_model.json`, `interior_navigation_graph_v0.1.schema.json`.

## 3. Tres familias funcionales de puerta (clasificación propuesta)

| Familia | Activación por jugador/NPC | Respuesta |
|---|---|---|
| **Paso ordinario** | Detector de proximidad y seguridad básica; mecanismo equivalente al prototipo Sutherland | Se abre automáticamente si físicamente transitable y política libre; se cierra al despejarse, sin atrapar personajes |
| **Camarote o despacho privado** | Pulsador exterior / timbre; mando interior de salida | Identidad y permisos: residente/invitado → abre; desconocido → timbre sin apertura |
| **Zona restringida** | Pulsador/panel, aproximación o petición de acceso según configuración | Autenticación reforzada según riesgo, autorización/escorta/guardia; denegar o pedir verificación adicional |

La puerta **no debe inferir identidad** solo porque el avatar visible lleve uniforme, comunicador, insignia o diga un nombre. Un comunicador autenticado puede ser prueba adicional; no resuelve por sí solo un riesgo de suplantación.

## 4. Autenticación: ¿de dónde sale el actor?

1. Interacción física producida por avatar UE5 → controlador/AIController y entidad de gameplay, validado por sesión y Core → referencia confiable a `character_id`. **No aceptar el ID que un texto de cliente indique sin validación.**
2. Acción de NPC fuera de la escena → acto autorizado desde Core/agenda/operación de NPC, con autor real y presencia temporal plausible.
3. PADD, terminal o comunicador → sesión y dispositivo autenticados; una orden de voz es texto de intención, no prueba concluyente de identidad. Para permisos altos exigir señales adicionales según política.
4. Huella/biometría diegética o desafío de seguridad opcional → se simula con estado y evidencias ficticias del mundo. **El videojuego no tiene por qué procesar huellas, rostros o voz biométrica reales del usuario**.
5. Si un actor no puede validarse (personaje ausente, identidad inválida, dispositivo robado, sesión caducada), **no abrir por defecto**; contestar con denegación o verificación/llamada según la puerta.

Autenticación y autorización **son cosas distintas**: saber quién eres no significa que puedas entrar.

## 5. Política de acceso dinámica

La política se consulta por `resource_id` (normalmente `location_id` o puerta vinculada) y `operation=ENTER` / `GRANT` / `REVOKE` / `EXIT` / `REQUEST_VISIT`.

Reglas propuestas:
- Propietario/residente confirmado en la asignación oficial vigente → entrada.
- Corresidente confirmado → entrada equivalente al residente según habitación.
- Invitado con permiso explícito, ámbito, hora y revocación válidos → entrada limitada.
- Servicio de mantenimiento/limpieza o visita médica autorizada **por tarea concreta** → acceso según necesidad, no llave maestra universal.
- Guardia o capitán **no es omnipotente** para irrumpir en todas las habitaciones por el rango.
- Quien no está autorizado en una habitación privada → timbre, intercomunicador o negativa; no revelar si la persona está dentro sin permiso.
- Residentes pueden invitar/revocar a terceros mediante acción confirmada y permisos de propiedad/tenencia vigentes.
- Cambio de camarote, destino, expulsión o traslado revoca los permisos derivados de la asignación antigua y habilita los de la nueva **por eventos autorizados**, no por texto conversacional.
- Quienes estén físicamente dentro conservan una **ruta de salida segura** en condiciones normales. Confinamiento, aislamiento y despresurización requieren una política excepcional explícita y compatible con supervivencia.
- El estado energético/mecánico, emergencia, presión o sabotaje puede impedir la **apertura física** aunque la autorización sea concedida; devolver razón física sin fingir denegación de identidad.

## 6. Emergencias y excepciones

Solicitudes de forzado legítimo se evalúan con: identificador de incidente, autoridad/servicio, objetivo, acción requerida, duración y razón. **Ningún 'override' es válido por el simple hecho de llamarse emergency**. Las normas sanitarias, rescate, seguridad, cuarentena, sellado y evacuación vienen de sus dueños Core/domains.

**La seguridad de salida es distinta de entrar.** No implementar una puerta privada que encierre a su residente por falta de pulsera o comunicador; tampoco abrir automáticamente un compartimento despresurizado peligroso. Reglas de emergencia deterministas, auditables, sin decisiones arbitrarias de LLM.

## 7. Rendimiento, privacidad y persistencia

La interacción de pulsador debe sentirse **inmediata**, incluso con IA deshabilitada. No hacer una solicitud HTTP por cada puerta: consulta local/Core o HOST ya iniciado con revisión de permisos; cachés de autorización solo si saben invalidarse en cambio de residencia, incidente, revocación, turno o expiración. Un fallo de red de IA no afecta la cerradura.

Registro de seguridad con `request_id`, `actor_id` verificado, `resource_id`, `operation`, decisión, política/revisión, tiempo y referencia de evento/incidente si procede. **No construir un historial universal de visitas privadas accesible para cualquier oficial**. Registros por política de privacidad y autorización de seguridad.

Guardado/carga preserva asignaciones y permisos/expiraciones con su origen; no guarda autorizaciones que se puedan recalcular como verdad paralela. Evitar eventos duplicados por doble pulsación y estados inconsistentes al salir/entrar de una escena.

## 8. Pruebas necesarias para ejecución

- Jugador abre su camarote; NPC de otra asignación pulsa → no abre y llama.
- Corresidente y visitante temporal entran, luego caduca/revoca permiso.
- Cambio de camarote hace válido el nuevo y revoca el antiguo.
- Uniforme, nombre pronunciado o comunicador no verificado no concede acceso.
- Puerta de pasillo se abre sola por proximidad sin usar un LLM; no aplasta al que cruza.
- Cámara de seguridad/PADD con acceso clasificado requiere autorización independiente.
- Ingeniero autorizado por tarea puede entrar cuando corresponda; un capitán no abre cualquier habitación por defecto.
- Emergencia legítima frente a una falsa; salida de seguridad frente a compartimentación peligrosa.
- Puerta físicamente averiada devuelve bloqueo físico, no 'usuario no autorizado'.
- Carga de partida y dos pulsaciones no producen permisos o eventos fantasma.
- Rendimiento en MSI/UE5 y NPC reales; reutilización del precedente Sutherland tras inspección del artefacto.

## 9. Responsables y estado

**S18-I01** auditoría de fuentes y sistema de puertas Sutherland; **S18-I02** contrato Core y evaluación; **S18-I03** interacciones con S12/UE5; **S18-I04** invitaciones/permisos y privacidad; **S18-I05** emergencias y funciones de ordenador; **S18-I06** regresión, save/load, NPC, MSI y certificación. ChatGPT diseña/audita; Codex implementa C++/HOST/UE5 después. No declararlo completado por elaborar este diseño.
