# LORE-03 A — Auditoría de arranque y matriz de migración (v0.1)

**Fecha:** 2026-10-23. **Base:** `main@867077e4a0108f5ae71485ba668c0419ee29aa2f`. **Estado histórico del documento:** auditoría de arranque, superada por expediente final `lore_03_a_completion_audit_v0.2.md`. Conservar como registro de inicio.

## Resultado de inspección

- `proyecto/docs/decisions/playable_eras.md` afirmaba tres épocas jugables; decisión posterior del 23-10 lo sustituye. La nota en archivos históricos F01 es una **rectificación temporal trazable**, no borrado.
- Los archivos `pike/era_profile.json` y `kirk/era_profile.json` permanecen disponibles y pasan a `playable: false`. El de `tng_ds9_voyager` sigue activo con ventana referencial `2364–2378`.
- `sistemas/gameplay/careers/academy_path/academy_era_profiles.json`, `sistemas/gameplay/ship_operations/era_technology_matrix.json`, `mundo/lore/starships/classes/core_starship_classes.json` y los `temporal_anchors.json` conservan IDs Pike/Kirk como **patrimonio histórico**. **Pendiente** separar sus consumidores UI/bootstrapping de los usos históricos. No reescribir contratos aprobados silenciosamente.
- `mundo/lore/diplomacy/historical_events_v0.1.json` contiene **40** entradas diplomáticas y bélicas fechadas con `YEAR_APPROXIMATE`. `tzenkethi_false_coup_report` es una **noticia falsa**, NO un golpe ocurrido.
- `mundo/lore/historical_events/historical_event_contract.json` y `mundo/lore/conflicts/conflict_definition_contract.json` son contratos fundacionales; sus datos de lore no equivalen a ejecución del motor.
- `sistemas/gameplay/conflict/conflict_war_index_v0.1.json` reúne la autoridad de conflicto de gameplay y sus contratos, con simulador determinista de referencia; NO se crea un índice paralelo de guerra.
- Registro central de fuentes: **501** en la instantánea auditada. El nuevo índice sólo referencia `source_id` ya existentes. Es revisión documental, no visionado íntegro de los episodios.

## Corte conceptual A: catálogo por referencia

`mundo/lore/historical_events/lore03_a_chronology_index_v0.1.json` señala los 40 IDs originales en LORE-01 D, sin replicar los hechos ni sus proveniencias. Añade cuatro anclas que **faltaban como fichas propias** en esa colección:

1. **Batalla de Wolf 359**, 2367 **aproximado**; no confundir con el inicio de la ofensiva Borg 2366 ya descrita en LORE-01 D.
2. **Descubrimiento del agujero de gusano bajorano**, 2369 **aproximado**; diferenciar del control político sobre DS9 y del mito/religión personal de cada actor.
3. **Desplazamiento de Voyager al Delta**, 2371 **aproximado**; separación causal y espacial, no desbloqueo automático del DLC Delta.
4. **Regreso canónico de Voyager**, 2378 **aproximado**, dato sólo histórico si `D` es posterior; nunca final obligado de una partida que comience antes.

Las fechas en estas fichas son de **año narrativo aproximado**, no fecha de estreno, stardate exacta ni día fijo. Los títulos de episodios están en el registro central; antes del cierre A se contrastarán escenas/fechas de cada registro crítico, registrando incertidumbres cuando corresponda.

## Impacto sobre naves y temporalidad

| Clase/identidad | Evidencia actual | Criterio para LORE-03 |
|---|---|---|
| Miranda, Oberth, Excelsior | Ya aparecen como clases operativas de largo recorrido | Se conservan como barcos veteranos cuando exista constancia de actividad en `D` |
| Galaxy / Enterprise-D | Disponibilidad TNG en catálogo | La pérdida u otros episodios posteriores a `D` no son obligatorios |
| Intrepid / Voyager | Catálogo y aventura de Voyager | No inferir que cada Intrepid acabará en Delta |
| Sovereign / Enterprise-E | Catálogo indica actividad tardía `<=2373` | No inferir presencia 2364 ni extrapolar capacidades a otra clase |
| Odyssey / Enterprise-F | No consta como disponible en catálogo principal auditado | Investigar y pedir autorización si se quiere en una fecha incompatible |
| Clase Valhalla | Diseño creativo independiente inspirado en Galaxy | **Fecha de alta no decidida**. Tecnología excepcional aprobada ≠ disponibilidad automática |

## Dudas y deuda de comprobación para cerrar A

- Separar `año de episodio` de `año intradiegético`; completar diferencias entre Wolf 359 y ofensiva 2366.
- Documentar guerra Federación–Cardassia anterior a DS9 sin atribuir día de inicio/fin no confirmado.
- Precisar comienzo de ocupación bajorana y referencias históricas desde 23º siglo **sin convertir esos periodos en campañas seleccionables**.
- Contrastar desapariciones/retornos, pérdidas de tripulaciones y grandes cambios de mando a partir de fuentes de pantalla.
- Investigar la frontera 2378 para hechos canónicos futuros, sin convertir el final del marco documental en fin de cada campaña.
- Resolver los identificadores de personajes/naves sólo cuando exista referencia inequívoca; no crear falsas instancias.
- Auditar los mensajes antiguos de tres eras en UI/Academia sin modificar lógica de ejecución en esta fase.

## Validación y límites

Primer corte con validador/CI de **integridad referencial, época única, futuro no obligatorio, sin runtime y reservas de naves**. **No implica que los 40 sucesos diplomáticos hayan sido auditados audiovisualmente uno a uno**. Tampoco certifica adaptación a UE5/CoreRPG.

**Próximos pasos dentro de A:** expansión del dossier cronológico 2364–2378 y antecedentes, contraste episodio por episodio, casos de fecha `D` y revisión previa a `NEEDS_REVIEW`. B no empieza todavía.
