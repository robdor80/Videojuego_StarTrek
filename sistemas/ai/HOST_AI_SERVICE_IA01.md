# HOST IA-01 — servicio común OpenAI

Documento permanente de implementación, trabajo 1 de 3. No implementa consumidores F10,
NPC, computadora, PERSON, menús Unreal ni cambios en Nimroel.

## Arquitectura y autoridad

`desarrollo/integration/host/include/trek/host/ai/service.h` proporciona la API C++20
interna de `TrekHost`. Una instancia compartida de `Service`, propiedad de la composición
HOST, atiende todos los consumidores futuros. No crear una instancia por NPC ni por petición.
Un único trabajador procesa una cola acotada sin bloquear al remitente. No hay proceso
auxiliar, servidor, base de datos, cuenta de jugador, suscripción ni segundo Core.

`Transport` permite sustituir HTTPS por un simulador. El transporte real usa WinHTTP
en Windows x64 (biblioteca del sistema) y libcurl >= 7.85 mediante pkg-config en Linux.
El analizador y validador JSON Schema reutiliza jsoncons ya presente en la composición.
El servicio no incluye cabeceras ni enlaza APIs Core; la prueba aislada solo enlaza
jsoncons, threading y transporte. Devuelve candidatos sin capacidad de modificar partida,
calificaciones, permisos, rangos o hechos. F11 conserva toda su autoridad.

## Configuración

`host_service_config_v1.json` es configuración de implementación separada del contrato
histórico `openai_runtime_v0.1.json`. El futuro bootstrap HOST debe leer este documento
(o la copia editable instalada), con límite de 16384 bytes, llamar a `load_config` (o `parse_config` para un documento ya cargado) y crear
la instancia compartida. Errores bloquean la configuración; no se ignoran campos desconocidos.
No se necesita recompilar para cambiar modelos, rutas, esfuerzo, tokens, límites o tiempo.
La configuración es una instantánea inmutable durante la vida de la instancia. Para recargar,
cancelar y destruir la anterior fuera de Game Thread antes de crear otra.

Luna es habitual. Solo `REASONING_LANGUAGE` selecciona Sol por defecto; el consumidor
seleccionará esa ruta si existe necesidad justificada. Cualquier ruta puede configurarse
explícitamente como `reasoning`. `COMPUTER_ANALYSIS` usa Luna inicialmente. No hay escalada,
reintento ni fallback automático, ni otros proveedores. Cada envío aceptado consume como
máximo un intento de transporte. `max_calls` cuenta intentos por instancia y ejecución,
no dinero; no garantiza un presupuesto monetario. La cola llena rechaza sin consumir API.

HTTPS tiene endpoint fijo `https://api.openai.com/v1/responses`, verificación de certificado
y hostname, sin redirecciones. Solicitudes con `store:false`, instrucciones internas separadas
del mensaje `user`, sin herramientas. El propietario del consumidor debe ensamblar únicamente
contexto autorizado, tratar textos del jugador como datos y validar resultados antes de
cualquier acción. La separación de roles reduce el riesgo de inyección, no garantiza obediencia
del modelo ni sustituye puertas deterministas de autoridad.

Esquemas opcionales usan `text.format.type=json_schema`, `strict:true` y objetos con todas
las propiedades requeridas y `additionalProperties:false`. Solo referencias locales; no
resolución de esquemas por red. El HOST valida también el JSON devuelto contra ese esquema.
Se rechazan contenido HTTP incorrecto, salida vacía/múltiple, herramientas, rechazo, JSON
malformado e incompletitud. Razonamiento del proveedor no se publica como texto.

Plazo desde `submit`, incluyendo espera en cola. Cancelación antes de red evita el intento;
con red iniciada aborta IO pero no promete cancelar una facturación ya aceptada por OpenAI.
El simulador debe respetar plazo y cancelación. WinHTTP vigila el plazo cada 10 ms; curl
usa timeout total y callback de progreso (cancelación durante IO puede tardar alrededor de
un segundo según fase/resolución DNS del sistema). Nunca esperar un futuro en Game Thread.
`shutdown` solo solicita cancelación; el destructor hace join y debe ejecutarse en el
trabajador de cierre HOST. No se ejecutan callbacks sobre objetos Unreal.

## Credencial compartida y asistente futuro

Identidad estable de Credential Manager: **`PersonalRPG/OpenAI/APIKey/v1`**,
`CRED_TYPE_GENERIC`, `CRED_PERSIST_LOCAL_MACHINE`. El nombre no pertenece a un juego.
Permite a cualquier videojuego del mismo propietario y usuario Windows reutilizar la misma
clave. No accede a otros usuarios, perfiles ni secretos de aplicaciones desconocidas.
No exige cambiar la cuenta OpenAI. Nimroel no se modifica en esta entrega: hoy conserva
`OPENAI_API_KEY`; una adaptación posterior podrá usar exactamente esa identidad.

`credential_status` informa solo presencia de clave compartida y de entorno y estado del
almacén. `register_key` registra o sustituye la entrada conocida. `import_environment_key`
es una operación **explícita** del futuro asistente, nunca una escritura automática.
`CredentialStore::read` es exclusivo de módulos HOST de confianza: no se expone a Blueprint.
No hay logs de solicitudes, cabeceras, texto, claves ni mensajes remotos; `diagnostic` devuelve
únicamente códigos fijos. Errores nunca contienen salida parcial del proveedor.

Resolución: entrada compartida Windows primero; `OPENAI_API_KEY` si no existe entrada o el
almacén no está soportado (Linux). Un error de almacenamiento/entrada inválida no se oculta
con otra clave. Una clave caducada requiere sustituir la entrada o corregir explícitamente
la configuración; un 401 no borra ni sobrescribe credenciales. Presencia no equivale a validez
remota: solo una llamada efectiva puede comprobarla. Linux usa entorno sin persistencia propia.

**Decisión de producto obligatoria para los futuros menús:** mostrar siempre el asistente
en el primer arranque de cada videojuego, incluso si hay credencial compartida. Mostrar:
«Se ha encontrado una configuración de OpenAI en este equipo. ¿Quieres utilizarla también
en este videojuego?». Permitir aceptarla, introducir otra o importar una de entorno.
Guardar la finalización del asistente en preferencias locales de cada juego, separadas de
modelos y secretos, cuando se implementen los menús. No pedir de nuevo en cada partida;
reabrir ante configuración ausente/inválida. IA necesaria bloqueada si no está disponible,
sin inventar aprobaciones ni resultados. No hay modo alternativo sin IA ni autorización por
llamada normal. Esta entrega implementa las operaciones, no el asistente ni su persistencia.

Android podrá implementar `CredentialStore` con almacenamiento privado y Android Keystore,
y adaptar `Transport`/bootstrap manteniendo solicitudes y resultados. Primera instalación
puede ocurrir allí sin MSI/Windows. Windows y Android no sincronizan claves automáticamente.
No hay transferencia por Internet ni servidor propuesto. Compilación Android no realizada.

## Uso desde un futuro consumidor HOST

```cpp
using namespace trek::host::ai;
// Bootstrap HOST: cargar un documento de configuración acotado desde disco.
Config config;
if (load_config(config_path, config) != Error::OK) { /* bloquear configuración */ }
// Instancia única compartida, fuera de UWorld; no crear por petición.
Service ai(config);
Request request;
request.route = "FAST_LANGUAGE";
request.instructions = "Clasifica el texto autorizado según el esquema indicado.";
request.input = authorized_context_and_player_text;
request.json_schema = trusted_strict_schema_json;
auto pending = ai.submit(std::move(request));
// Poll desde el futuro adaptador, sin get bloqueante:
if (pending.result.wait_for(std::chrono::milliseconds(0)) == std::future_status::ready) {
    auto candidate = pending.result.get();
    // Comprobar error, generación/contexto vigente y reglas del dominio antes de usar.
}
// pending.cancel() ante LOAD/cambio de contexto/cierre.
```

La interfaz es interna del HOST con toolchain común. No pasar STL por la ABI binaria de
Unreal: el adaptador futuro debe copiar valores/pollear a través de una extensión C acotada
del adaptador ya existente. Esta entrega no cambia la ABI C 1 ni integra formularios. El
servicio no conoce generaciones: el futuro consumidor debe descartar resultados obsoletos.

## Precedencia contractual

La decisión autoral `OPENAI_RUNTIME_DECISION_2026-11-15.md` y su contrato autorizan OpenAI
por encima de la restricción local antigua F10. El encargo IA-01 posterior divide la entrega:
solo servicio común en trabajo 1; adaptador y motor biográfico en trabajo 2. No reescribe
contratos cerrados, huellas F10 ni puertos históricos porque aún no activa ese consumidor.
La armonización de política y huellas previa al uso productivo F10 sigue siendo obligatoria
en el trabajo 2. El antiguo Gemini de Holodeck y los controles de fallback de issue Nimroel
#29 son históricos/de otro proyecto: no activan proveedores ni restricciones de gasto ajenas
a la autorización OpenAI de este encargo.

## Errores, pruebas y humo explícito

`diagnostic(Error)` distingue falta de clave, autenticación, almacenamiento, modelo, HTTP,
conexión, cuota, rate limit, timeout, cancelación, incompletitud, JSON, rechazo y límites.
`retryable` orienta sobre reintento manual; 401/cuota/configuración requieren corrección.
No se preserva cuerpo remoto de error, texto privado ni credencial en diagnósticos.

`host_ai_tests` usa transporte simulado y no consume API. En Windows, si la entrada compartida
no existe, registra una clave ficticia, la sustituye, la recupera desde un segundo proceso y
elimina exclusivamente la entrada ficticia creada. Si ya existe, la conserva y omite las
escrituras. Linux verifica el estado no soportado. La CI HOST incorpora esta prueba en Linux,
Windows y ASan/UBSan, además de las regresiones existentes.

`host_ai_smoke` está excluido del build normal y de CTest. Compilar explícitamente ese target
y ejecutarlo con `--live-openai` y `OPENAI_API_KEY` disponible. Realiza **una sola** solicitud
mínima Luna/128 tokens, JSON estricto, sin contexto del universo; imprime solo código/HTTP.
Sin clave termina sin llamar. No ejecutarlo para diagnosticar repetidamente errores de cuota.
Ver el informe IA-01 para resultados realmente obtenidos y estado de CI/OpenAI.
