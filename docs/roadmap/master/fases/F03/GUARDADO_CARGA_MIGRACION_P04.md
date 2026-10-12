# F03-P04 — Guardado, carga, migración y continuidad de órdenes

**Fecha:** 2026-10-11. **Estado:** DISEÑO OPERATIVO PREPARADO, `CORE_INTEGRADO` NO. **Responsable técnico:** CoreRPG Persistence (4.7+), con serialización específica Trek mediante acuerdos de interfaz todavía no publicados.

Fuente normativa reutilizada: `gameplay/persistence/persistent_state_roundtrip_contract.json`; fuente complementaria: `universe/generation/persistent_entity_identity_contract.json`, `gameplay/ship_operations/operational_event_log/operational_event_contract.json`, `ai/memory/character_memory_lifecycle_contract.json` y `docs/roadmap/master/fases/F02/PLAN_INTEGRACION_PRIMER_CORTE.md` (PR #3 INT-05).

## Snapshot lógico mínimo que debe conservar la infraestructura

No se fija un formato de archivo ni se inventa API; se enumeran dominios a persistir:

| Dominio | Contenido obligatorio cuando exista | Motivo |
|---|---|---|
| Identificación | ID partida, época/continuidad, fecha de inicio, semilla y versiones de contratos | Evitar que una migración abra otra campaña |
| Reloj | timestamp exacto, cursor de procesamiento y zona/referencia de simulación coherente | No repetir intervalos fuera de escena |
| Entidades | `entity_id`, tipo, estado, origen, semilla/versión, materialización, `history_ref`, estado operativo | Evitar re-generación y duplicación |
| Población | plantilla, `slot_id`, asignaciones, individuos promocionados C→B y bajas | Mantener cupos y continuidad de NPC |
| Historia | secuencia de eventos append-only y dependencias causales, correcciones sin reescribir pasado | Auditoría, disciplina, investigación y progresión |
| Conocimiento | por observador, nave y consola; contactos relativos, fuente, fecha, confianza, permisos | Un reload no restaura conocimiento omnisciente |
| Memoria | recuerdos por actor, fuentes, vigencia, incertidumbre y privacidad | La memoria no es un clon del world state |
| Operaciones | orden emitida, autorizaciones, delegaciones vigentes, acción iniciada, resultado, acuse, reintentos y claves de idempotencia | No ejecutar 2 veces ni perder órdenes pendientes |
| Vínculos | asignación, relación, localización, hangar/docking, propiedad, capacidad y estado | Una lanzadera no aparece en dos hangares |
| Presentación | referencias opcionales `visual_identity_id` / recursos re-creables | UE5 actor/mesh no reemplazan entidad |

La colección anterior es una **checklist de datos**, no `savegame.schema.json` definitivo. El motor y los dominios propietarios establecerán versión y mecanismos reales. Mantener referencia estable aunque un asset visual deje de estar disponible.

## Protocolo de seguridad previsto (negociación con Core)

1. Validar versiones/esquemas y procedencia antes de aplicar cambios; no cargar datos arbitrarios en estado vivo.
2. Leer snapshot y eventos/órdenes pendientes en staging de forma transaccional; verificar integridad, IDs, referencias, contador de población, cursor, permisos y causalidad.
3. Si hay migración: especificar `from_version`, `to_version`, transformación y prueba de reversibilidad/rechazo; nunca cambiar semilla/ID por regeneración silenciosa.
4. Sólo cuando se valida el conjunto, efectuar sustitución atómica del estado de sesión; fallo ⇒ conservar partida actual intacta, informar de error y preservar fichero original.
5. Tras cargar: revalidar órdenes y delegaciones según tiempo actual; reconciliar `IN_FLIGHT` con log y claves de idempotencia antes de intentar reejecución. Con resultado desconocido, **no repetir a ciegas**.
6. Recrear Actor 3D sólo desde `EntityId` y estado restaurado; LOD y assets no deben escribir nueva verdad ni generar individuos sustitutos.
7. Reanudar cursor de catch-up confirmado; si el usuario abre partida duplicada en otra sesión, Core debe definir protección de escritura/versión concurrente, no resolverlo en UI.

## Tabla de compatibilidad orientativa, no política Core aprobada

| Situación | Política segura |
|---|---|
| Misma versión soportada | Validar, restaurar y comparar prefijo histórico + identidad |
| Versión antigua con migrador probado | Copia inmutable de origen + migración versionada + validación completa |
| Versión antigua sin migrador | Rechazar explícitamente, sin sobrescribir |
| Versión futura no soportada | Rechazar explícitamente, sin downgrade silencioso |
| Corrupción o referencia huérfana crítica | Rechazar snapshot completo, no borrar entidades sueltas |
| Guardado interrumpido | Recuperar último checkpoint validado; no aceptar escritura parcial |
| Acción remota con timeout y estado ambiguo | Consultar resultado por clave antes de reintentar |
| LOD/recarga visual | Reconstruir sólo vista 3D desde identidad persistida; jamás resembrar |

## Pruebas de aceptación futuras

- `F03-T17` guardado→carga preserva identidad, historial, conocimiento, órdenes y cursor.
- `F03-T18` crash o snapshot truncado ⇒ rechazo **sin** modificar la partida actual.
- `F03-T19` versión futura/antigua desconocida ⇒ rechazo explícito.
- `F03-T20` migración versionada conserva relación `entity_id/slot_id/visual_identity_id`.
- `F03-T21` reintento de orden en vuelo ⇒ no duplica efecto ni evento; estado ambiguo bloquea ejecución ciega.
- `F03-T22` recarga visual no cambia NPC ni posición de nave/lanzadera.

El validador P05 usa **snapshot sintético inerte** para detectar alteraciones, duplicados y corrupción estructural; no serializa ni deserializa World State Core. Para declarar `CORE_INTEGRADO` deberán verificarse todas estas transiciones sobre Core real en CI/Windows con SHA y versión exactos.

## Bloqueos de validación externa

CoreRPG `main@dcfcb83c` y la rama 4.5 separada aún no proporcionan Persistence 4.7 ni Knowledge 4.9 / Actions 4.10 confirmados. No se modifica Core ni se publica serializador paralelo bajo `Videojuego_StarTrek`. F02 PR #3 y F01 PR #2 estaban abiertas **en el corte de auditoría del 11-10-2026**; **ambas quedaron fusionadas el 13-10-2026**. Esto no modifica el estado de Core ni convalida la persistencia. Por lo que no se altera unilateralmente `ESTADO_GLOBAL.json`.
