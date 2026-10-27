# LORE-03 A — Casos de corte de campaña D

**2383** es el año preferente propuesto; día/mes no decidido. Los casos anteriores siguen siendo comparaciones documentales, no campañas adicionales. Los casos siguientes son ejemplos de pruebas, no selecciones aprobadas del videojuego.

| Ejemplo de D (solo año) | Pasado que puede darse por anterior | En el mismo año | Qué no debe ocurrir |
|---|---|---|---|
| 2364 | Khitomer y antecedentes documentados | Farpoint/Ferengi/romulanos: `UNRESOLVED_SAME_YEAR` | Implantar automáticamente toda TNG |
| 2366 | Farpoint y encuentro con Borg de 2365 | Ofensiva Borg de 2366: `UNRESOLVED_SAME_YEAR` | Forzar Wolf 359 de 2367 |
| 2368 | Wolf 359 de 2367 si fuente cronológica aplicable | Crisis civil klingon y reunificación: `UNRESOLVED_SAME_YEAR` | Dar por terminada la crisis sin orden |
| 2369 | Hechos anteriores a 2369 | Retirada de Bajor/DS9/agujero de gusano: `UNRESOLVED_SAME_YEAR` | Colocar agujero y mando DS9 antes de existir |
| 2371 | Eventos anteriores a 2371 | Voyager, Enterprise-D y Defiant: `UNRESOLVED_SAME_YEAR` | Hundir Enterprise-D o transportar Voyager por calendario |
| 2373 | Anclas anteriores a 2373 | Dominio/Borg Sector 001: `UNRESOLVED_SAME_YEAR` | Ejecutar inicio de guerra ni batalla |
| 2375 | Operación Retorno 2374 | Tratado Bajor, caída Defiant, estatus Sisko: `UNRESOLVED_SAME_YEAR` | Dar por terminada guerra al comienzo de ese año |
| 2378 | Anclas anteriores a 2378 | Voyager regresa: `UNRESOLVED_SAME_YEAR` | Forzar final de Voyager o cierre partida |
| **2383, preferido** | Némesis 2379, Picard almirante 2381, Riker/Titan, Protostar 2382 | Programa Valhalla propuesto para su primer servicio: fecha exacta pendiente | Aplicar destrucción de Rómulo 2387 o dar por acabada Academia antes de 2387 |

La comparación provisional está documentada en el validador como función *puramente editorial* `classify_by_year`: si el evento es anterior devuelve `ESTABLISHED_BEFORE_D`; si es posterior devuelve `NOT_YET_AT_D`; en el mismo año `UNRESOLVED_SAME_YEAR`. **No genera datos de partida ni muta CoreRPG**. Cuando una fecha intradiegética exacta esté certificada, se podrá sustituir esta comparación sin atribuir precisión retroactiva a todas las fuentes.

Un evento de la línea televisiva posterior a D podría surgir o no por la simulación causal, y el guardado conserva únicamente lo realmente ocurrido.
