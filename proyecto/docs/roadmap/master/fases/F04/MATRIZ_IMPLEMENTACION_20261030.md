# F04 P01–P05 — matriz del corte operativo

| Etapa | Implementado realmente | Evidencia ejecutable |
| --- | --- | --- |
| P01 | Clase del catálogo, nave, población individualizada, categorías, plazas persistentes, destino departamental, habilitaciones y vacantes sin generación compensatoria | identity, class, vacancy, manifest, qualification, assignment, authorized_posts |
| P02 | [inicio,fin), adyacencia, exclusividad, descanso/franco, localizado separado de consola, enfermedad/licencia/suspensión, relevo, ventanas Alpha/Beta/Gamma/Delta, cambio autorizado de patrón, agenda fuera de escena | overlap, adjacent, rest, oncall, absence, relief, coverage, policy, rotation, recall |
| P03 | Nombramientos temporales, cuatro roles, sucesión por destino cualificado, delegación acotada, origen persistente, revocación, caducidad, permisos al ejecutar y motivos | roles, watch, appointment, succession, delegation, revoke, expiry, origin_reappointment, stale |
| P04 | Incapacidad documentada sin mando médico, límites técnicos y físicos no anulables, mandato externo limitado, revisión contextual persistente, IA sin autorización | medical, technical, safety, superior, order_expiry, context_review, ai, credential_expiry, pending_credential |
| P05 | Escenario unido, tareas pendientes, destrucción/nueva sesión, carga entre procesos, archivos deterministas, validación semántica de grafo, UWorld y Actors reales, regresiones F02/F03 | integrated, process_save/process_load, roundtrip, determinism, bounded, corrupt, schema; F04.Core.* |

Core reutilizado sin cambios: WorldState, EntityId/RelationKind, población,
ContentCatalog, ActionEngine, RandomStreams, Timeline y CampaignPersistence.
Knowledge/Visibility y el adaptador F03 se mantienen íntegros y se regresan;
F04 no implementa un relevo de conocimiento del universo ni entrega verdad
oculta a una IA. Las consultas F04 son proyecciones de manifiesto autorizado.

Componentes nuevos Trek: ABI f04_bridge, esquema relacional validado, reglas
de disponibilidad/guardias/mando, catálogo compilado desde JSON existente,
52 pruebas nativas, subsistema de representación y cinco pruebas Unreal,
runner aislado y workflow CI. No hay componente nuevo Core ni dependencia
de una PR Core sin fusionar.

P05 cubre los 16 pasos solicitados en el test integrado: nave/personas/plazas;
guardia; operación cualificada del alférez; gestión departamental; oficial de
guardia; decisión con revisión del capitán; ausencia y vacante; relevo existente;
delegación revocada; acción imposible denegada; avance sin Actors; archivo;
destrucción; nueva sesión; restauración de identidad, autoridad, agenda y tarea;
reanudación con el mismo resultado. La cobertura 3×8/4×6 y los negativos
adicionales se comprueban en casos separados del mismo adaptador real.

## Pendientes expresos

Los límites detallados en `desarrollo/integration/f04/README.md` son parte de
la entrega: este es un laboratorio vertical, no el sistema completo de vida
a bordo. Especialmente: política de descanso biológico y fatiga acumulada,
optimización real de una semana de 120 personas, itinerarios y duración de
relevo 10–20/15–30 minutos, transferencia de informes conocidos, edición de
destinos/cualificaciones, configuración personalizada de rotaciones, nuevos
sistemas técnicos y normas contextuales completas. F05 conserva órdenes e
iniciativa NPC. No se acredita UE5_JUGABLE ni se altera canon de Valhalla/Miranda.

El validador general de referencias tiene 564 incidencias preexistentes,
reproducidas en un worktree limpio de la base; se conservan ambas salidas.
Su saneamiento global excede este corte y no se oculta como prueba superada.
El validador de gobierno y los contratos específicos F02/F03/F04 sí se ejecutan
por separado. F04 sigue EN_CURSO y pendiente de auditoría independiente.
