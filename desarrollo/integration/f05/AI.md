# F05-P04 — lenguaje y propuestas opcionales

La inteligencia operativa es el controlador **determinista P03**. Funciona sin
modelos generativos, proveedor, API o red. P04 interpreta lenguaje, prepara
explicaciones y propone el único candidato ejecutable del flujo: `F04_SCAN`, sin
parámetros. No decide nuevas tareas ni implementa autonomía general.

Base comprobada: Star Trek main `f1ab2f33cccdd861077e59069addb8a12ff573d7`;
Core main `76a7b7b485616d8c4994f384a90f123bf333591d`. No hay cambios Core.
Se contrastaron P04/P03, INITIATIVE, DELEGATION, el contrato de computadora y
ai_routing_policy, F03/Visibility/ContextBuilder y las interfaces Core de acciones,
conocimiento, CampaignPersistence e HistoryPersistence. El contrato antiguo
CommandPlan incluye ejemplos futuros: navegación, combate y reparaciones **no**
se convierten en operaciones P04.

## Frontera y secuencia

```text
Host autenticado → P03 (siempre disponible, ninguna espera de red)
        ↓ petición opcional de lenguaje
f05_ai_begin → Visibility::project → ContextBuilder(subject=necesidad)
        ↓ contexto mínimo por actor
Provider.start / poll (sin Session ni WorldState)
        ↓ JSON no confiable
f05_ai_finish → esquema cerrado + bindings + revisión/reloj + plan P03 actual
        ↓ propuesta/clarificación/insuficiente/rechazada/obsoleta/fallback/aprobación
Host solicita explícitamente f05_ai_apply si corresponde
        ↓ mismo plan determinista P03, una transición máxima
P01/P02 → ActionEngine → resultado Core auténtico
```

`f05_plan` extrae el cálculo previo de P03 como función sin efectos, compartida
por validación y evaluación. No cambia su política. `finish` jamás ordena,
recibe, ejecuta, aprueba, aprende hechos ni consume RNG. `apply` vuelve a P03;
una interpretación de escaneo no selecciona otro ejecutor, estación, plazo,
permiso o mandato. La decisión efectiva puede ser proponer, esperar al jugador,
informar, escalar o no actuar. Un estado P04 `APPLIED` significa *tramitado*, nunca
*escaneo exitoso*. Se consulta el resultado P01/Core para afirmar un efecto.

Capitán NPC y jefaturas conservan sus atribuciones. XO sin atribución propone;
un operador sin orden no adquiere mando. P02 conserva aprobación explícita y
revalidación de mandatos. Identidad jugador fijada por P03: ni un capitán jugador
ni un operador jugador son aceptados o sustituidos por un texto generado.
Las delegaciones revocadas y los cambios de mundo invalidan respuestas pendientes;
P01/P02 revalidan de nuevo antes del efecto.

## Contexto y contrato

[f05_ai.h](include/f05_ai.h) es ABI C aditiva sobre la sesión/hilo F04 existentes.
El actor se autentica con `F04Ref`; el proveedor recibe solamente IDs persistentes
mínimos en `F05AiContext`, nunca scopes, sesión, save o diagnósticos privilegiados.
La identidad se fija en Host. La función permitida es asesorar sobre una obligación
de servicio comunicada; `allowed_operation=F04_SCAN` describe un candidato de
catálogo y **no** una concesión de autoridad.

Se reutiliza la proyección P03 sin grants, filtrada al sujeto, 32 hechos como
máximo y necesidad completa de siete hechos. Solo exporta identidad solicitante,
referencia de petición/proyección, revisión, ticks/plazo, necesidad conocida,
servicio, estación y operador comunicados. No existe exportación de campaña,
memorias ajenas ni órdenes globales. Un ID oculto y uno inexistente producen el
mismo contexto incompleto, con referencias operativas cero. El Host debe entregar
solo lenguaje originado legítimamente por ese actor; no adjuntar datos secretos
al campo de texto. Sin conocimiento suficiente, Job no llama al proveedor.

[proposal-v1.schema.json](proposal-v1.schema.json) y el parser C++ definen v1:
actor/request/projection/revision/issued_at/expires, intención, cero o un candidato,
parámetros vacíos, aclaración/datos insuficientes, explicación y trace efímero.
El parser rechaza claves extra/duplicadas, versiones, tipos y enums incorrectos,
campos omitidos, flags contradictorios, JSON múltiple, operaciones ajenas y
parámetros arbitrarios. Límites: 8192 bytes, profundidad 8, explicación 512 bytes,
trace 64 caracteres técnicos, IDs enteros de 48 bits. Se compara cada binding
contra el registro Host, sin confiar en IDs o revisiones del proveedor.

Texto, explicación e identificador del proveedor son **contenido no confiable**.
No se interpretan instrucciones dentro de ellos. `message(view)` ofrece plantillas
controladas sin afirmar resultados. Un consumidor puede presentar una explicación
solo como consejo externo identificado y bajo la visibilidad del solicitante;
no debe mostrarla como hecho/resultado ni compartirla con otro NPC. No se guardan
prompts, conversaciones, modelos, credenciales, endpoints ni prosa en Core/logs.
El trace técnico durable es el ID Host de petición y su vínculo con decisión/orden.

## Proveedores y rutas

[f05_ai_provider.h](include/f05_ai_provider.h) proporciona una interfaz de transporte
C++ utilizable: `start(Input)`, `poll(request)` y `cancel(request)`. No dispone de
capacidad de juego. Una implementación debe encolar y consultar sin bloquear,
con workers o servicio externo; jamás llamar a Core desde ese worker. El Host
conserva la propiedad de sesión y proveedor durante el trabajo.

`route_for` selecciona `DETERMINISTIC` para rutina o ausencia de proveedor,
`COMPUTER_FAST` para lenguaje breve y `COMPUTER_REASONING` para análisis complejo.
Los nombres configurables `Config.fast_model/reasoning_model` no son reglas de
juego. El routing se alinea con ai_routing_policy existente. El Host conoce la
necesidad real; no se deja al modelo decidir complejidad, permisos o rutas.
No hay escalado remoto ni reintentos facturables implícitos.

`Job` coordina begin/poll/finish y deadline monotónico de transporte (1..60000 ms),
separado del reloj Core. Devuelve inmediatamente ante proveedor pendiente; no
avanza tiempo ni invoca iniciativa. `SimulatedProvider` controla respuestas,
errores, excepciones y demoras en número de polls sin dormir ni usar Internet.
El adaptador simulado atraviesa la misma validación que cualquier transporte.

No se encontró una configuración runtime comercial compatible que pudiera
reutilizarse. Se entrega la interfaz, configuración externa y simulador; **no**
se entrega un cliente HTTP de producción ni se ha probado una conexión comercial.
La implementación futura de transporte debe mapear red, HTTP y cuota a los códigos
públicos y mantener credenciales fuera de contexto, respuestas, saves y logs.
No se han utilizado claves ni realizado llamadas de pago.

## Fallback y recuperación

Proveedor ausente, red, HTTP, cuota, timeout o vacío producen fallback sin acciones.
JSON inválido/restricciones se rechazan; actor/contexto equivocados no se aceptan.
Nada de ello invoca acciones nuevas. El Host continúa llamando a P03 normalmente,
independientemente del estado de Job. Las pruebas `offline`, `pending`, `timeout`,
`quota`, `network`, `http`, `empty` y `deterministic` completan el escaneo P03 real
sin ninguna ayuda generativa. No es necesario crear un Job para usar P03.

Cada petición vive en Core y retiene key/payload Host, actor, necesidad conocida,
revisión, ticks, ruta, categoría/error, intención aceptada y decisión P03 causal.
La primera resolución terminal prevalece: una respuesta duplicada no sustituye
el resultado. `apply` repetido recupera su decisión, incluso tras cargar en otro
proceso. La transacción por copia incluye todo P03/P01 y el vínculo P04.
Se reutilizan CampaignPersistence e HistoryPersistence; no hay archivo lateral.
Retención conserva tombstones y referencias del registro. La carga valida forma,
bindings históricos, categorías y causalidad antes de sustituir estado vivo.

Una solicitud de red pendiente queda retirada después de una carga, pues el
scope efímero ya no coincide. Se registra `STALE/RECOVERED` cuando el Host la
cierra; no se reenvía automáticamente. Una propuesta ya validada puede recuperarse
y tramitarse solo si revisión/plazo siguen vigentes y P03 la autoriza. Una decisión
ya tramitada siempre reproduce su registro sin segundo efecto. Una restauración
manual de un guardado anterior equivale a volver a ese estado de campaña; la
publicación durable y el bloqueo por publicación incierta son los de F04/Core.

Política conservadora: cualquier cambio de revisión, incluso otra petición P04,
invalida el snapshot previo. Esto descarta respuestas fuera de orden; no hay merge
inteligente de contextos. Plazo máximo de petición: 300 ticks Core. Máximo 512
registros por campaña; alcanzar el límite bloquea nuevas peticiones opcionales,
**no** P03. Se conservan los presupuestos P01/P02/P03. Es integración de Host nativo
de confianza, no autenticación multiusuario, scheduler general o memoria social.

## Reproducir y auditar

Compilar con [README](README.md) y ejecutar `ctest -R '^f05.p04_'`, o toda la
selección F04/F05. Las regresiones F02/F03 conservan sus pins. Core completo se
compila aparte con JSON y BUILD_TESTING. El workflow F05 ejecuta Linux/Windows,
las seis campañas congeladas con el pin histórico original F04 y gobierno documental. No se han cambiado oráculos:
solo se actualizan dos huellas de puente, conservando las anteriores y su motivo.

La tabla de cobertura y evidencia ejecutada está en
[F05-P04_IMPLEMENTACION](../../../proyecto/docs/roadmap/master/fases/F05/F05-P04_IMPLEMENTACION.md).
Las tres automatizaciones Unreal nuevas y las nueve anteriores se mantienen
pendientes en el [registro MSI](../../../proyecto/docs/roadmap/master/fases/F05/REGISTRO_VALIDACIONES_MSI.md).
F05 abierta, F06 bloqueada, P05 no iniciada; entrega para auditoría independiente.

El exportador de evidencia acepta rutas de resultados ejecutados, sin fabricar PASS:

```sh
python desarrollo/integration/f05/collect_ai_evidence.py \
  --native "$NATIVE_JUNIT" --core "$CORE_JUNIT" --f02 "$F02_JUNIT" --f03 "$F03_JUNIT" \
  --historical "$HISTORY_JUNIT" --history-runs "$HISTORY_RUNS" \
  --run-logs "$RUN_LOGS" --temp-root "$TEMP_OUTPUT_ROOT" --output "$NEW_EVIDENCE_DIRECTORY"
```

`RUN_LOGS` conserva configure-final.log, build-verified.log, native-tests-final.log,
core-tests.log, f02-tests.log, f03-tests.log, historical-final-tests.log y toolchain.txt.
El intento inicial de pin, si existe, se exporta aparte sin contarlo como PASS.
