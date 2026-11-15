# H06 / IA-01 — Informe de implementación

**Entrega permanente, 15/11/2026. Trabajo 1 de 3.** Responsable: Codex.
Rama: `codex/h06-ia01-central-ai`. [PR Draft #164](https://github.com/robdor80/Videojuego_StarTrek/pull/164), sin fusionar.

## Revisión y alcance

Base actualizada: `2c976b0a4a699882c545286c40aef930cce515e2`, fusión de PR #163 confirmada.
HEAD de código auditado: `1e49c6ae4d6f3fd757a129c7d7973d15fd35ec88`.
El commit que incorpora este informe solo añade documentación. El HEAD de entrega se obtiene
en la [rama de la PR](https://github.com/robdor80/Videojuego_StarTrek/tree/codex/h06-ia01-central-ai)
y en su historial; el SHA definitivo se registra también en la descripción de la PR.
CoreRPG conserva `76a7b7b485616d8c4994f384a90f123bf333591d`, checkout limpio, sin modificaciones.

Se leyeron `AGENTS.md`, las reglas de experimentación, README/orquestación IA, decisión y contrato
OpenAI del 15/11, CMake HOST, puertos e implementación biográfica F10, contratos de creación,
frontera semántica, factoría de candidatos, confianza H01, integración H06 y frontera F11.
No había cliente OpenAI existente en el HOST que hubiera que duplicar.

El encargo IA-01 posterior limita esta entrega al servicio común. Aunque el documento previo
pedía también adaptador F10, aquí no se implementa. La autorización OpenAI del 15/11 prevalece
sobre la restricción histórica de transporte local. No se cambian contratos cerrados ni sus
huellas: armonizar la política y digests F10 antes de activar su consumidor corresponde al
trabajo 2. Se conserva la doble puerta de biografía y la autoridad F11.

## Arquitectura implementada

Código en `desarrollo/integration/host/src/ai/` y API interna en
`desarrollo/integration/host/include/trek/host/ai/service.h`, integrado en `TrekHost` existente.

- `Service`: un trabajador y cola acotada, futuros, cancelación por operación, plazo desde envío,
  cierre, límite de intentos y respuestas de error sin resultados inventados. No reintenta automáticamente.
- `Transport`: HTTPS real y puerto simulado. WinHTTP asíncrono en Windows; libcurl en Linux.
  Contexto/buffer WinHTTP se conservan hasta el último callback de cierre; ningún hilo cierra
  una petición síncrona concurrente. Se siguen las reglas de vida de Microsoft WinHTTP.
- Responses API: endpoint fijo HTTPS, certificados y hostname verificados, sin redirecciones,
  `store:false`, sin herramientas, roles separados para instrucciones y datos.
- Structured Outputs: `text.format=json_schema`, `strict:true`, esquemas con referencias locales,
  comprobación técnica del sobre y validación local del resultado con jsoncons existente.
- Errores controlados: configuración/clave/almacén/modelo/HTTP/conexión/cuota/tasa/timeout/
  cancelación/incompletitud/JSON/rechazo/límites. Diagnóstico de códigos fijos, sin claves,
  mensajes de proveedor, cabeceras ni textos del jugador en logs.

La suite IA aislada no enlaza Core ni puentes. No recibe WorldState, sesiones Core, setters,
permisos ni recibos autoritativos. La IA solo produce candidatos. No crea PERSON, no cambia
biografías, no admite cadetes ni concede rangos. No añade persistencia, servidor o multiusuario.

## Referencia Nimroel

Consulta exclusivamente de lectura de los seis archivos solicitados y de
[issue #29](https://github.com/robdor80/Videojuego_Nimroel/issues/29).
Se reutilizan conceptualmente Responses API, `OPENAI_API_KEY`, modelos por clase,
`store:false`, límites de bytes/tokens/plazo, separación de errores seguros, rechazo de
respuestas incompletas/múltiples y pruebas con transporte sustituido sin consumo.

Referencias inspeccionadas en `main` de Nimroel (SHA de blob):

| Archivo | SHA |
|---|---|
| `Tools/NIM04/provider_proxy.py` | `e51d37c866fc0ea6c88ae8f30efef01124308b88` |
| `Tools/NIM04/test_openai_adapter.py` | `9dd7ea8052e144ce6203bdee93e1a018100bd65b` |
| `Tools/NIM04/test_provider_proxy.py` | `0ad39d49a42721be518e64f3855a9e0c3abadb50` |
| `Docs/IA/POLITICA_MODELOS_NIMROEL_2026-10-17.md` | `477e3f107e3e6ea405b5880412346860ef221457` |
| `Docs/IA/catalogo_modelos_nimroel_2026-10-17.json` | `c23bb2d39fea1fde1e8b9e775a2a634d754e11d0` |
| `Docs/NIM-04_PROVEEDORES_Y_PRUEBAS_17-10.md` | `738dd4fc40d87110b3a8dedd6b2ed6b9bbbaa5f2` |

No se copia el servidor Python, fallback multiproveedor, autenticación del laboratorio ni
infraestructura Android histórica. La issue advierte correctamente que un contador de llamadas
no garantiza dinero: `max_calls` aquí solo cuenta intentos por instancia/ejecución.
No se modifica ni se escribe ningún archivo, issue o PR en Nimroel.

## Configuración, credenciales y modelos

`load_config` carga un archivo JSON acotado y `parse_config` valida un documento ya cargado,
sin alterar la configuración anterior si falla. La configuración editable de ejemplo es
`sistemas/ai/host_service_config_v1.json`. Identificadores, esfuerzo, rutas, tokens, tamaños,
plazo, pendientes e intentos se cambian sin recompilar. Instancia inmutable; recargar requiere
cerrar la anterior fuera de Game Thread y crear la nueva en la composición HOST.

Luna (`gpt-6-luna`) habitual. Sol (`gpt-6.1-sol`) para `REASONING_LANGUAGE` o configuración
explícita. Las cinco rutas existentes están disponibles. `COMPUTER_ANALYSIS` comienza con Luna;
el consumidor futuro debe justificar la selección de razonamiento. Ningún otro proveedor activo.

Windows Credential Manager: `PersonalRPG/OpenAI/APIKey/v1`, credencial genérica persistente
para el mismo usuario local. Operaciones: detectar presencia sin revelar clave, registrar,
sustituir, recuperar internamente e importar explícitamente `OPENAI_API_KEY`. Misma cuenta y
misma clave para los juegos que adopten la identidad; no se exige credencial por juego.
Entrada compartida primero, entorno si no existe/no hay almacén soportado. No se ocultan
fallos del almacén ni una clave compartida inválida con un fallback silencioso.

El futuro asistente se muestra siempre en la primera ejecución de cada juego, ofrece reutilizar
la entrada compartida con el texto aprobado y permite introducir/importar otra clave. Vuelve
ante configuración ausente/inválida. La preferencia de finalización será propia de cada juego;
no se implementan ahora menús ni nueva persistencia. Uso de OpenAI aprobado sin confirmación
por llamada normal. Si IA requerida falla, el consumidor bloquea esa función y conserva datos.

Windows no depende de nuevas DLL de terceros para HTTP/credenciales: WinHTTP y Advapi32 son
del sistema. Linux requiere libcurl >= 7.85 y pkg-config y usa clave de entorno sin almacén propio.
Android podrá implementar `CredentialStore` con almacenamiento privado/Keystore y adaptar el
transporte conservando la interfaz. Primer arranque Android independiente de Windows/MSI;
ninguna sincronización ni servidor. Adaptación Android y Nimroel fuera de esta entrega.

## Ejemplo para un futuro consumidor

```cpp
using namespace trek::host::ai;
Config config;
if (load_config(config_path, config) != Error::OK) return; // Bloquear hasta corregir.
Service service(config); // Una instancia HOST compartida, no una por NPC.
Request request{"FAST_LANGUAGE", trusted_instructions, authorized_input, strict_schema};
auto operation = service.submit(std::move(request));
// Sondear sin bloquear; el futuro adaptador lleva los valores al Game Thread.
if (operation.result.wait_for(std::chrono::milliseconds(0)) == std::future_status::ready) {
    auto candidate = operation.result.get();
    // Comprobar error, vigencia del contexto y aceptación autoritativa del dominio.
}
// operation.cancel() en LOAD/cierre/cambio de contexto.
```

Esta es API C++ interna del HOST, con toolchain común. La ABI C 1 existente no cambia ni se
pasa STL a Unreal. El adaptador futuro extenderá la fachada C acotada; F10 deberá enlazar su
borrador/contexto/política exactos y verificar resultados antes de cualquier efecto.
Detalles de ciclo de vida y ejemplo ampliado: [contrato del servicio](../../../../sistemas/ai/HOST_AI_SERVICE_IA01.md).

## Pruebas y resultados

| Comprobación | Resultado |
|---|---|
| Compilación nativa Linux GCC 14.2, C++20, Release | PASS |
| Suite IA offline, revisión final | PASS |
| Regresiones seleccionadas HOST/F04/F05, incluidas F10 y ABI | 263/263 PASS |
| Contratos H01 | 11/11 PASS |
| Producto Release con tests OFF, carga de bibliotecas e inspección de exports/dependencias | PASS |
| ABI C 1 desde producto tests OFF | PASS |
| Suite IA sin dependencias ni símbolos Core/F04/F05/F11 | PASS |
| Compilación y pruebas Windows, almacén real y segundo proceso | PASS (MSVC x64) |
| ASan/UBSan y regresión F11 aislada | PASS (109 casos HOST sanitizados; F11 17/17 por plataforma) |
| Humo OpenAI real | **PENDIENTE / NOT_RUN** |

La suite IA cubre carga válida/inválida/de tamaño excesivo, rutas Luna/Sol y configuración,
separación de instrucciones/datos, `store:false`, ausencia de clave en payload/diagnósticos,
JSON Schema estricto y validación local, múltiples salidas, herramientas, rechazo, incompletitud,
HTTP 400/401/403/404/429/500/503, cuota, red, límites, timeout/cancelación/cierre/cola,
concurrencia, clave ausente/inválida, importación de entorno y almacén no soportado Linux.
En Windows una entrada ficticia recién creada se sustituye y recupera desde otro proceso,
comprobando reutilización por el mismo usuario; una entrada personal previa nunca se sobrescribe.

El humo se compiló y ejecutó con opt-in `--live-openai`; terminó `MISSING_KEY (no call)`.
No existe clave disponible en este entorno. **No hubo llamada autenticada, gasto medido ni
prueba de acceso remoto a Luna/Sol.** El ejecutable limita el humo a una solicitud Luna de
128 tokens con JSON estricto, se compila explícitamente y está excluido de CTest/CI automática.

## Evidencia CI

Revisión de código `1e49c6ae4d6f3fd757a129c7d7973d15fd35ec88`:
[HOST native H02-H06 — ejecución 84](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43718500008).
**5/5 trabajos correctos:** nativo Linux (264/264), nativo Windows (264/264),
ASan/UBSan (109/109), producto Linux tests OFF y producto Windows x64 tests OFF.
Ambas suites nativas completaron además H01 (11/11) y F11 aislado (17/17).

[Artefacto Windows con LastTest.log y evidencia del almacén compartido](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43718500008/artifacts/14164080328).
La suite Windows pasó con su prueba de almacén del sistema. Esta prueba escribe, sustituye,
recupera desde otro proceso y elimina exclusivamente una entrada ficticia cuando no existe
entrada previa; si existe, la preserva y omite las escrituras. La salida detallada queda en
`LastTest.log` del artefacto para auditoría.
SHA-256 del ZIP de evidencia: `631fbd68bedabc535c1f2c4c1557908885f79ea3382111cf3fc780937bf06fba`.
Los artefactos de esa ejecución incluyen logs, JUnit, compiladores y revisión Core.
Este informe se incorpora después sin cambiar el código probado.

La primera ejecución detectó una colisión de nombre de prueba con la macro `concurrency` de
MSVC; se corrigió sin cambiar el servicio. La revisión del transporte Windows también cambió
la cancelación a WinHTTP asíncrono conforme a su contrato oficial de cierre. Las ejecuciones
anteriores no sustituyen la evidencia de la revisión final enlazada arriba.

## Limitaciones y cierre del alcance

- No se ha probado una llamada OpenAI real ni la conectividad/cancelación WinHTTP con un
  proveedor remoto. La evidencia Windows separa compilación, almacén real y simulación de red.
- La cancelación después de enviar no garantiza evitar facturación. El cierre conserva el
  contexto nativo hasta recibir su último callback. curl puede demorar la cancelación según
  fase DNS/IO; nunca se debe esperar en Game Thread.
- La separación de roles no garantiza obediencia de un LLM: toda salida sigue siendo no
  autoritativa. El consumidor filtra contexto y descarta resultados obsoletos.
- `max_calls` no es presupuesto monetario. No hay retry/fallback automático ni contador de dinero ficticio.
- La fachada Unreal, asistente, política/digests y motor biográfico F10, PERSON, NPC, Android y
  adaptación de Nimroel continúan fuera del trabajo 1. No se certifica M1 ni el juego completo.

No hay dependencias del producto respecto a resultados temporales. La ubicación local de
experimentación y su carácter eliminable se comunican en la entrega; no se incorpora material
experimental a Git. PR Draft preparada para auditoría de ChatGPT, sin fusión.
