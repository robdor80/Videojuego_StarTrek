# F05-P01 — Sistema de órdenes nativo para auditoría

Fecha: 2026-11-02. Alcance exclusivo **P01**. Entrega en Draft; no autorización
de fusión ni de P02. La fase F05 completa **no se declara CORE_INTEGRADO**.

## Comprobación inicial

- Star Trek `main`: `142f852e5a1abfa373413002be928fd4f437b3bc` (PR #76).
- CoreRPG `main`: `76a7b7b485616d8c4994f384a90f123bf333591d` (PR #13).
- Consultadas ramas remotas de ambos repositorios, PR abiertas y búsqueda
  histórica F05. No había implementación P01 previa que reanudar/duplicar.
  Las PR Valhalla #79/#80 y restantes trabajos ajenos quedan intactos.
- Revisada [PR #78](https://github.com/robdor80/Videojuego_StarTrek/pull/78):
  abierta, Draft, sin fusionar, HEAD `34e2b1b5fc355d06a01a43cdbfb9e92425e1a2d6`.
  Su apertura administrativa de F05 sigue pendiente. Esta rama parte de main
  y no cambia sus seis archivos de gobierno, README F05 incluido, evitando
  mezclar cierres administrativos. El estado antiguo de esos índices en main
  debe leerse junto a #78; esta entrega no los da por fusionados.
- Leídos los ocho documentos/contratos F05, integración F03/F04, contratos
  de órdenes, autoridad, Actions 4.10, CampaignPersistence y HistoryPersistence
  reales. Se preservan los diseños históricos y suites de referencia.

## Implementación

[Código, contrato y reproducción](../../../../../../desarrollo/integration/f05/README.md).
`TrekF04Bridge` añade las funciones P01 mediante opción explícita de compilación;
F04 sin la opción mantiene sus pins y API. CoreRPG no requiere cambios.

| Concepto | Registro autoritativo | Creación/efecto |
| --- | --- | --- |
| Petición | `f05_request` | Intención tipada, payload e idempotency key |
| Orden | `f05_order` | Emisor, destinatario, puesto, nombramiento, estado |
| Tarea | `f05_task` | Solo al recibir y aceptar; responsabilidad del destinatario |
| Acción | `f05_attempt` | Un intento desde una orden aceptada |
| Resultado | `f05_result` | Validación fallida o salida verdadera de ActionEngine |
| Evento | `f05_event` | Hecho causal con actor, tick, referencias y anterior |

Todos los IDs los emite el único WorldState de la sesión F04. Se reutilizan
identidades, cadena de mando, cualificación, guardias, presencia, reloj,
RNG e historial. El ciclo implementado es `issued → accepted → executing →
completed/failed`, con `refused` antes de aceptar y `cancelled` antes del efecto.
Estados de aclaración/colas y ampliaciones de referencia no se atribuyen a P01.

En el escenario mínimo, el capitán ordena `F04_SCAN` al operador Sensores ya
asignado, de guardia y en su consola. El destinatario recibe explícitamente.
Al ejecutar se revalida también la autoridad del origen. `perform(F04_SCAN)`
llama al **ActionEngine real** sobre el mismo WorldState y RandomStreams.
Se persiste el resultado de `StreamRollAction{0xF0401,1,100}` con sus revisiones
y consecuencia. **No equivale a detección de un contacto**: F04 no proporciona
ese subsistema. Otras operaciones se rechazan con `F05_UNSUPPORTED`.

## Evidencia de integración

La prueba `f05.scenario` comprueba que emisión y aceptación no consumen RNG,
que los seis objetos tienen IDs distintos y que la cadena causal conserva
los actores. Compara la salida P01 con dos caminos independientes:

1. `f04_execute(F04_SCAN)` sobre el mismo checkpoint previo.
2. Restauración con `CampaignPersistence` y llamada directa a
   `ActionEngine::process(StreamRollAction)` de CoreRPG.

El stream y el valor deben coincidir. Los tests entre procesos comparan bytes
completos del futuro, incluyendo identidades, revisiones, RNG e historial
relacional. También hay escenario sobre organización real Miranda de 130
personas y migración/publicación/consolidación/recuperación del historial Core.

## Pruebas y publicación

La evidencia final de Cloud y Actions se consolida en
`evidence/F05-P01/RESULTADOS.json` y su informe de validación. No atribuir a
esta entrega las antiguas 48 propuestas de referencia como acciones reales.
El workflow nuevo prueba Linux y Windows nativos; los workflows F04 existentes
mantienen sus campañas de 365/730 días y pins anteriores.

La ampliación de `f04_bridge.cpp` y su CMake exige actualizar sus dos huellas
en el manifiesto de compatibilidad de las referencias F04. Se conservan allí
las huellas anteriores y el commit del cambio. **No se cambian los seis
oráculos, sus acceptance.json ni sus archivos de procedencia históricos.**
Su reutilización queda condicionada a que las seis campañas reales actuales
coincidan de nuevo con todos sus bloques y futuro final. Se corrige además la
selección de extensión `.exe` en dos drivers de pruebas para Linux y se declara
el directorio temporal requerido por la suite de referencias históricas.

## Deuda y continuación

El contrato nativo es para un Host autenticado y un único hilo. No hay UI
jugable ni autenticación de red. Las consultas son diagnóstico acotado, no
proyecciones de conocimiento NPC. El máximo de 512 órdenes retiene tombstones
y sus dependencias en memoria; requiere ampliación antes de campañas con más
órdenes. No existe scheduler de órdenes: la caducidad se aplica al volver a
recibir/ejecutar. Guardar/publicar sigue siendo una operación explícita del Host.

El harness Unreal está preparado pero requiere el MSI; véase
[VALIDACIONES_PENDIENTES_MSI.md](VALIDACIONES_PENDIENTES_MSI.md).
No se han modificado recursos artísticos, escenas, USS Valhalla, laboratorio
Sutherland ni copias de seguridad. P02, P03, P04 y cierre P05 no se desarrollan.

Tras publicación se detiene el trabajo para auditoría técnica de ChatGPT.
**No fusionar ninguna PR.**
