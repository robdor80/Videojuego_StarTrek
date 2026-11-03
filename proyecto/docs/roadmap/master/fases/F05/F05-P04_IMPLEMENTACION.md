# F05-P04 — integración opcional de lenguaje, contexto y propuestas

Entrega para auditoría independiente, 2026-11-03. **F05 abierta; F06 bloqueada.**
P05 no iniciada. No se ha fusionado ninguna rama en esta tarea.

Repositorio: `robdor80/Videojuego_StarTrek`; rama `codex/f05-p04-ai-integration`.
Base main real comprobada: `f1ab2f33cccdd861077e59069addb8a12ff573d7`.
Core main real: `76a7b7b485616d8c4994f384a90f123bf333591d`, fijado en P04,
sin cambios ni PR Core. P01–P03 se reutilizan desde main, no se reconstruyen.
La PR Draft y sus Actions identifican el SHA final; el manifiesto de evidencia
identifica el commit de fuentes y las huellas exactas de archivos comprobados.

## Arquitectura y comportamiento entregados

El controlador operativo **P03 es autónomo y determinista**, sin modelo, API ni
conexión a Internet. P04 no es el cerebro de los NPC ni gobierna sus tareas.
La capa optativa interpreta lenguaje/propuestas; Host autentica, filtra y valida;
Core conserva el estado, las acciones y sus resultados. La misma sesión F04
contiene identidad, reloj, revisiones, conocimiento, historial y persistencia.

El [contrato ejecutable AI.md](../../../../../../desarrollo/integration/f05/AI.md)
describe ABI, transporte no bloqueante, contexto privado, esquema JSON v1, errores,
plazos, aprobación y recuperación. El Host puede usar P03 directamente durante
una petición IA pendiente. Un modelo solo sugiere `F04_SCAN` sin parámetros,
referido a una obligación real comunicada. La entrega explícita a P03 vuelve a
calcular autoridad, delegación, guardia, salud, disponibilidad, ubicación y
consentimiento, conservando los límites P01/P02/P03.

Capitán NPC puede ordenar bajo su autoridad; XO propone sin mando universal;
operador solo continúa la orden real; capitán jugador exige su decisión efectiva;
jugador subordinado nunca acepta ni ejecuta mediante texto generado.
`finish` no emite órdenes ni consume RNG. `APPLIED` no confirma éxito: el único
efecto sigue siendo `StreamRollAction{0xF0401,1,100}` ejecutado por P01/Core.
No se implementan navegación, combate, reparación, contactos/sensores F06,
recursos, gestión de personal, personalidad o memoria social general.

`Visibility::project` y `ContextBuilder` suministran solo los siete hechos de
obligación comunicados a ese actor. No se exportan memorias ajenas ni campaña.
Un modelo que adivine un ID oculto no lo convierte en conocimiento. La prosa del
modelo es inerte y efímera; los mensajes de estado/fallback son plantillas.
El registro durable conserva bindings Host, categoría, intención aceptada y
vínculo causal P03/P01, sin conversaciones, secretos ni trace remoto bruto.

## Cobertura nativa P04

Cada caso usa campañas Core reales; el transporte simulado es controlable, sin
servicio comercial. Las pruebas rechazan efectos no autorizados comprobando RNG,
órdenes/tareas/resultados y conocimiento, además de categorías de respuesta.

| Requisito del encargo | Casos CTest `f05.p04_…` |
|---|---|
| 1. Interpretación válida | `valid`, `provider_valid` |
| 2. Ambigüedad/aclaración | `ambiguous` |
| 3. Información insuficiente | `insufficient`, `hidden` |
| 4. Memorias privadas por NPC | `privacy`, `scope` |
| 5. Hecho oculto no revelado/aprendido | `hidden`, `privacy`, `injection` y regresión F03 |
| 6. Proveedor caído | `offline`, `network`, `provider_exception` |
| 7. Timeout/cuota | `timeout`, `quota` |
| 8. Respuesta corrupta | `malformed`, `provider_malformed`, `empty` |
| 9. Prompt injection en datos/respuestas | `injection`, `parameters`, `provider_valid` |
| 10. Autoridad inexistente | `authority`, `parameters`, `binding` |
| 11. Revocación durante respuesta | `revoked` |
| 12. Revisión antes de tramitar | `stale`, `accept_stale` |
| 13. Respuesta tardía/desordenada | `late`, `out_of_order`, `pending` |
| 14. Duplicados y carga | `duplicate`, `recovery`, `process_save/load` |
| 15. Capitán jugador sin aprobación | `approval` |
| 16. Subordinado jugador sin aceptar | `player` |
| 17. Autonomía sin red/IA | `offline`, `pending`, `deterministic`, `routing` y regresión P03 |
| 18. Orden P01 real | `valid` |
| 19. Delegaciones P02 | `delegation`, `approval`, `revoked` |
| 20. Persistencia sin doble efecto | `history`, `duplicate`, `process_save/load`, `corrupt` |

`advice` verifica propuesta de consejo sin acción, `http` el error HTTP y `scope`
el propietario de sesión/hilo. Se distinguen datos aceptados y efectos Core;
una explicación maliciosa no enseña secretos, concede permisos o certifica éxito.

## Validación y evidencia

La evidencia de ejecución definitiva se publica en `evidence/F05-P04/`, con JUnit,
logs, resumen, huellas de fuentes y SHA256 de entregables. No son fixtures PASS
sintéticos. `collect_ai_evidence.py` rechaza tests fallidos/omitidos o campañas
sin aceptación y equivalencia real con los seis oráculos originales.

Estado de verificación al preparar la entrega: Core **483/483**, F02 **15/15**,
F03 **25/25** y primera regresión F04/F05 **361/361** ya ejecutadas. La ejecución
final ampliada de **365** y las **seis campañas históricas** están en curso;
esta sección se actualiza con su resultado real antes del informe final.

Se conservan los pins originales de F02/F03 y F04 histórico
(`89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`). El primer intento de ejecutar campañas
con el Core actual se detuvo por incompatibilidad de pin antes de simularlas;
se corrigió usando el checkout histórico sin cambiar expectativas. Los seis
oráculos permanecen byte a byte: solo se amplían las huellas del puente F04,
conservando las previas y la justificación de compatibilidad.

El workflow F05 ampliado ejecuta compilación y regresiones Linux/Windows y seis
campañas históricas en Linux. Cada run corresponde a un SHA GitHub concreto;
los resultados finales y sus enlaces se anotan en la PR y el informe de entrega.
No confundir CI Windows con validación del MSI o con ejecución de Unreal.

## Simulado y pendiente

La interfaz de proveedor y el adaptador simulado están implementados. La
configuración de modelos es externa, sin endpoints inventados ni claves.
**No hay conexión comercial probada, cliente HTTP de producción ni llamadas
facturables.** Timeout/red/HTTP/cuota son fallos simulados que atraviesan el mismo
validador. No se afirma generación remota real. Las capacidades demostradas son
las del contexto, propuestas, validación, handoff determinista y fallback.

Limitaciones: una obligación P03/un candidato `F04_SCAN`, revisión conservadora
que invalida ante cualquier cambio, 512 peticiones durables por campaña, Host
nativo confiable, sin scheduler universal ni servidor multiusuario. El registro
P04 no amplía los canales de conocimiento P03 ni crea resultados de sensores.
La persistencia durable usa la publicación explícita Core y sus fallos existentes.

Se preparan las tres automatizaciones P04, manteniendo las nueve fuentes/tests
Unreal anteriores. **Ninguna prueba Unreal ha sido ejecutada en Cloud.**
[VALIDACIONES_PENDIENTES_MSI_P04](VALIDACIONES_PENDIENTES_MSI_P04.md) detalla MSVC,
DLL, UBT/UHT UE 5.8.2, carga, 12 tests, repetición limpia, recuperación, RHI real
y proveedor simulado. El [registro central](REGISTRO_VALIDACIONES_MSI.md) conserva
todos los pendientes P01/P02/P03 y añade los nuevos sin acreditarlos.

## Protección y límites de publicación

Solo código de integración, contratos, tests, harness aislado, CI, documentación
y evidencia P04. No se modifican Clase Valhalla/Enterprise-G, Sutherland, Blender,
modelos, interiores, PBR, proyectos artísticos, copias ni laboratorios anteriores.
Temporales de esta tarea bajo `laboratorios/f05/p04/`, excluidos de Git. La carpeta
completa es prescindible: ninguna fuente de producto depende de sus resultados.
Las evidencias permanentes se publican en el directorio documental autorizado.
No se inicia P05/F06, no se declara F05 CORE_INTEGRADO/cerrada y no se fusiona PR.
