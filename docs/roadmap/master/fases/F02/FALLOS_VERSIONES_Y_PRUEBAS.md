# F02-P04 — Fallos, versionado, migraciones y validación

**Estado:** propuesta de política técnica; los escenarios descritos son **casos de prueba pendientes**, no tests ya ejecutados.

## Política de fallos

| Situación | Comportamiento seguro exigido | Regla |
|---|---|---|
| IA remota lenta, caída o no válida | Mantener funcionalidad determinista de consola/órdenes desde menús; informar de incapacidad de interpretación o diálogo; permitir reintento explícito | Nunca mutar estado por respuesta de IA |
| Salida IA malformada o «alucinada» | Rechazar candidato, ofrecer corrección o procedimiento manual | Todo candidato pasa por verificador de semántica, permisos y contexto actual |
| Petición tardía tras cambio de estado | Revalidar momento de aplicación; rechazar o pedir confirmación si cambian precondiciones | Sin ejecutar contra revisión obsoleta |
| Timeout de una acción | Estado **desconocido** hasta consultar resultado/ID correlacionable; no suponer ni éxito ni fallo | Evitar repetir operaciones con efectos si no hay deduplicación demostrada |
| Core runtime no disponible / error de ABI | Bloquear acciones persistentes y entrar en error recuperable o detener sesión con seguridad | No sustituirlo con un WorldState de Star Trek |
| Datos de sensor insuficientes/daño/interferencia | Mostrar lectura parcial, incertidumbre o error real | No inventar señal ni contacto positivo |
| Pérdida de conexión Companion (futuro) | Conservar partida y controles completos en PC | Companion opcional, sin autoridad autónoma |
| Cambios de modelo 3D/cubierta descargada | Mantener entidades/agenda, sustituir sólo representación | Identidad lógica != Actor |
| Guardado incompatible/corrupto | Validar formato/versión antes de cargar; abortar carga de forma atómica; preservar original | Nunca cargar estado parcial como si fuera correcto |
| Consulta que filtraría secretos | Rechazo o proyección reducida antes de entregar al Host o IA | Ocultar en pantalla NO es controlar conocimiento |

**Sobre reintentos:** no declarar operaciones idempotentes por defecto. Usar correlación/revisión y deduplicación **solo cuando Core publique un contrato que lo soporte**. No elegir segundos máximos, número de reintentos ni SLO sin medidas de MSI/red.

## Ejes de versionado separados

1. Commit/versionado de biblioteca **CoreRPG** (fijar SHA compilado y compatibilidad de ABI).
2. Versión **Content Contract** (Core actual: `0.1.0`).
3. Versión de **Content Pack** propio de Star Trek, cuando exista.
4. Versión de **savegame** (todavía no existe; no equiparar con Content Contract).
5. Versión de **protocolo Host↔Core / migraciones** cuando haya adaptador estable.
6. Versión independiente de assets, Consola de Sensores, UE5 y web Academia.

Toda prueba integradora registra los seis ejes **aplicables**, hashes de entrada y plataforma. Cambios de contrato requieren inventario de consumidores, política hacia atrás o migrador con pruebas; no forzar semver a un guardado inexistente.

## Matriz mínima de pruebas futuras

| ID | Caso | Prueba válida cuando… | Estado |
|---|---|---|---|
| F02-T01 | Identidad: Actor creado→destruido→recreado conserva EntityId | proyecto UE5 real conectado a Core probado | NO_EJECUTADO |
| F02-T02 | Cargar Content Pack compatible, rechazar referencia rota | Core JSON y pack de prueba con schemas reales | NO_EJECUTADO |
| F02-T03 | Rechazo de orden sin permiso | motor de acciones/autoridad disponible | BLOQUEADO_CORE |
| F02-T04 | Barrido observador-relativo no filtra datos | conocimiento/proyección vinculados a Core | BLOQUEADO_CORE |
| F02-T05 | Guardar/cargar conserva estado, IDs, orden y eventos | Core persistence integrada | BLOQUEADO_CORE |
| F02-T06 | IA caída, consola deterministicamente usable | Host con menú/manual y fallo simulado | NO_EJECUTADO |
| F02-T07 | Respuesta IA tardía nunca ejecuta permiso revocado | revalidación Core de acciones | BLOQUEADO_CORE |
| F02-T08 | UE5 Windows compila/enlaza la misma versión Core fijada | proyecto y toolchain reales | NO_EJECUTADO |
| F02-T09 | CI Core/main y rama 4.5 consultada | acciones GitHub reales | **CONSULTADA 2026-10-11** |

**Evidencia sólo de T09:** [Core/main CI 10-10-2026](https://github.com/robdor80/CoreRPG/actions/runs/38046482745) y [Core/4.5 CI 08-10-2026](https://github.com/robdor80/CoreRPG/actions/runs/37812440972) muestran `completed/success`; esto **no** acredita T01–T08.

## Regla de migración

- Antes de modificar contrato: fijar baseline y usos en Star Trek/Nimroel, abrir propuesta con responsables, diseñar semántica de compatibilidad.
- Migrador futuro probado con versiones origen/destino reales, backup, prueba de reversión o rechazo atómico, idempotencia solo si demostrada.
- No crear ahora un esquema savegame inventado ni afirmar tests E2E o UE5 sin ejecutarlos.
