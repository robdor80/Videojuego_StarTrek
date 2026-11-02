# F05-P02 — Implementación nativa para auditoría

Fecha: 2026-11-02. Alcance exclusivo: delegación, cadena de mando y revocación.
No cierra F05 ni comienza P03. No autoriza fusionar ninguna PR.

## Base verificada en GitHub

- Star Trek #81: abierta, Draft y sin fusionar; HEAD auditado y actual
  `854aa5720ec8681d6e5eccc7fe4ed80ac0c65d9b`.
- #78: abierta, Draft y sin fusionar; HEAD
  `34e2b1b5fc355d06a01a43cdbfb9e92425e1a2d6`.
- Rama P02: `codex/f05-p02-delegation`, creada desde el HEAD anterior de #81.
  La PR P02 se publica apilada contra `codex/f05-p01-orders`, exclusivamente
  con su incremento. Depende de #81; no debe fusionarse antes de auditar ambas.
- CoreRPG main verificado: `76a7b7b485616d8c4994f384a90f123bf333591d`.
  Se utiliza sin modificaciones. No hace falta PR adicional de CoreRPG.

## Funcionalidad y prueba de autoridad real

Ver [contrato técnico ejecutable](../../../../../../desarrollo/integration/f05/DELEGATION.md).
La nueva API usa el mismo `F04Session*`, reloj y `WorldState`. Amplía el tipo
Core `trek.f04:delegation`, ya existente en F04; no crea un sistema de permisos
lateral. `commander`, nombramientos, credenciales, servicio, relevo, disponibilidad,
puestos y `scan_station` son las comprobaciones reales de F04.
Los cambios pasan por `ActionEngine` y se guardan en los archivos/generaciones Core.

Se implementan borrador, activación explícita, suspensión, reactivación explícita,
revocación terminal, caducidad efectiva, inventario recuperable y eventos causales.
Los límites fijan dominio Sensores, permiso de emitir F04_SCAN, ejecutor, estación,
nave e intervalo. Ambos nombramientos de origen y credenciales de mando limitan
la duración. No se concede autoridad de política, profesional o mando universal.

Las órdenes P01 fijan su delegación y la revalidan al emitir, recibir y ejecutar.
La ejecución pendiente tras revocación registra fallo y `performed=0`; las
acciones ya confirmadas conservan eventos y resultados. Manual/propuesta requieren
aprobación persistente del delegante efectivo. Subdelegación rechazada explícitamente.
No hay IA, iniciativa NPC, contactos F06 ni nuevas operaciones ficticias.

Los tests nativos comparan la tirada real y los streams con F04 directo,
inspeccionan la entidad delegation en un archivo Core y ejecutan el mismo flujo
sobre una dotación F04 con nombramientos y puestos reales. Verifican guardado,
restauración y futuro exacto entre procesos, tanto monolítico como histórico.

## Contraste documental y decisiones de alcance

Se han leído `CICLOS_REVOCACION_P02.md`, `CONTRATOS_P01_P02.json`,
`MODELO_ORDENES_P01.md`, integración F04/P01 y contratos chain_of_command.
Las referencias de octubre describen Core como pendiente y contemplan ámbitos
que todavía no tienen operación ejecutable. El estado real actual prevalece:
F04 sí ofrece entidades delegación, pero su API estable solo admite F04_POLICY;
P01 solo ejecuta F04_SCAN. P02 añade exclusivamente el permiso acotado de emitir
esa operación. No finge delegación funcional de rutas, mantenimiento, rotaciones,
alertas o política de primer contacto. Se mantienen intactos los contratos JSON
originales como referencias, sin convertirlos en una ABI Core inventada.

Se conserva la semántica P01 de una ejecución máxima: pérdida de autoridad tras
aceptación produce `failed` con motivo y sin efecto. No se añade un nuevo estado
persistente `expired` a las órdenes; el estado expired existe en la delegación.
No hay compensación automática ni eliminación retroactiva de efectos.

## Validación y evidencia

Corte local corregido, con XML permanentes en [evidence/F05-P02](evidence/F05-P02):

| Suite Linux | Resultado |
| --- | --- |
| P02 específico | 20/20 |
| P01 compatible | 20/20 |
| F04/P01/P02 combinada | 301/301 (261 F04 + 20 P01 + 20 P02) |
| CoreRPG completo, incluido JSON | 483/483 |
| F02 con su pin original | 15/15 |
| F03 con su pin original | 25/25 |
| F04 original con su pin | 270/270 |

Las suites se solapan; no sumar sus recuentos como pruebas independientes.
Los baselines de capacidad de F04 son diagnósticos y no certifican campañas
completas. La aceptación de seis campañas históricas es un workflow separado,
con sus mismos oráculos congelados. XML, hashes de fuentes, traza real y la
reproducción del defecto corregido quedan publicados. La descripción final de
la PR enlaza las conclusiones de CI y el HEAD exacto verificado, sin atribuir
validación UE/MSI a los tests nativos. Los tests documentales F05, cross-phase
y gobierno también pasan; no se presentan como efectos autoritativos Core.

Durante desarrollo se corrigieron errores de compilación de las nuevas fixtures
y una consulta del test con el excapitán que había perdido acceso al resultado.
La consulta se realiza ahora con el destinatario autorizado; se conserva la
restricción de acceso efectiva. Se reprodujo además un defecto P02: cancelar una guardia SCHEMA4 acorta
`appointment.END`, pero el validador comparaba retrospectivamente el plazo
histórico del mandato con ese final acortado, bloqueando F04 con F04_INTERNAL.
Se corrige conservando el intervalo histórico del mandato; el límite se comprueba
al crear y la autoridad efectiva siempre revalida el nombramiento actual. La
prueba `f05.p02_roster_relief` demuestra cancelación F04, rechazo previo al efecto
y recuperación exacta del historial. Las ejecuciones finales deben pasar completas.

## Límites y deuda local

- Host nativo confiable, un hilo propietario; no se autentican actores remotos.
- Límites de 256 mandatos, 4096 eventos y 512 órdenes por campaña, sin borrado
  de tombstones. Recuperación inversa con builds F04/P01 antiguos no soportada.
- Caducidad y pérdida de autoridad cortan efectos inmediatamente al revalidar;
  el evento administrativo expired requiere petición explícita. F04 registra
  sus propias causas de incapacidad, relevo o baja. No existe scheduler nuevo.
- Las seis campañas históricas de regresión conservan su Core original; los
  tests P02 de persistencia histórica usan el Core fijado por P01.
- [Validaciones MSI P02 pendientes](VALIDACIONES_PENDIENTES_MSI_P02.md), además
  de las seis pendientes P01. UE 5.8.2, MSVC local y RHI no ejecutados en Cloud.

Laboratorio temporal: `Videojuego_StarTrek/laboratorios/f05/p02/`, excluido de Git.
Contiene checkouts Core, herramientas aisladas, builds, campañas y logs. Puede
eliminarse entero una vez conservadas las evidencias: el producto no depende de él.
No se ha eliminado ningún laboratorio, recurso ni archivo anterior.
Solo se modifica el harness Unreal aislado de F05; ningún recurso 3D, Blender,
interior, nave, material PBR, respaldo ni proyecto artístico del propietario.
