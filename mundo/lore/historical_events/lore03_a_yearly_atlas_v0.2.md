# LORE-03 A — Atlas cronológico editorial, v0.2

**Ámbito jugable:** 2364–2383 como referencia histórica; **2383 año de ingreso aprobado** del cadete (día/mes pendiente). Los hitos de desarrollo de clase posteriores a 2383 son planes GAME_ADDITION, no sucesos de pantalla ni guiones forzados. **Estado:** preparado para revisión documental, nunca runtime. Se preservan Pike/Kirk como pasado histórico.

> **Decisión prevalente 2026-10-30:** [DEC-0013–0016](../../../proyecto/docs/decisions/odyssey_valhalla_program_2383_2387_quantum_slipstream.md). Odyssey operativa y puntera desde 2383; Valhalla objetivo 2387 después de siete años de construcción desde 2380. El motor de flujo cuántico es experimental en ciertos prototipos Odyssey y candidato posterior en Valhalla; los resultados no son predestinados. El hito de 2387 es un **objetivo de diseño futuro**, no una afirmación histórica anterior al día D.

## Uso: un único pasado hasta la fecha D

Los identificadores en la columna **LORE-01 D** apuntan a la definición original `mundo/lore/diplomacy/historical_events_v0.1.json`, con sus fuentes. Los identificadores en **03-A** son fichas nuevas en `lore03_a_chronology_index_v0.1.json`. Un acontecimiento sólo es pasado establecido si **precede de forma demostrable** la fecha D; si tiene el mismo año aproximado que D, su ocurrencia es **INDETERMINADA** hasta disponer de orden más preciso. Cuando ocurre *después* de D deja de ser obligatorio.

| Año aproximado | Referencias existentes LORE-01 D | Fichas añadidas 03-A | Lectura histórica |
|---:|---|---|---|
| 2364 | `federation_ferengi_first_contact`, `romulan_return`, `tng_alliance` | `enterprise_d_farpoint` | Farpoint, aparición de la Enterprise-D en su marco de TNG, relaciones y contactos tempranos. |
| 2365 | `borg_first_encounter` | — | Contacto de la Enterprise-D con los Borg; no implica conocimiento de la amenaza por toda la población. |
| 2366 | `borg_earth_offensive` | — | LORE-01 D sitúa aquí la ofensiva Borg; resolver solapamiento editorial con Wolf 359 (2367). |
| 2367 | — | `wolf_359_battle` | Wolf 359, pérdidas de la Flota y trauma de supervivientes; la memoria del evento dependerá del actor. |
| 2368 | — | `klingon_civil_war_crisis`, `romulan_unification_contacts` | Guerra civil klingon y contactos en Romulus, cada uno con su cadena política propia. |
| 2369 | `cardassian_withdrawal_bajor`, `ds9_joint_arrangement`, `post_cardassian_border_conflict` | `bajoran_wormhole_discovery` | Fin de ocupación de Bajor, gobierno provisional, DS9 y agujero de gusano; simultaneidad anual no significa fecha idéntica. |
| 2370 | `dominion_first_warning`, `federation_cardassian_border_settlement`, `maquis_emergence` | `bajoran_circle_coup_defeated` | Crisis del Círculo, reclamaciones Maquis, reajustes fronterizos; no confundir tratados con armonía alcanzada. |
| 2371 | `omarion_ambush`, `trill_commission_secret`, `tzenkethi_false_coup_report` (**alegación falsa**) | `defiant_ds9_entry`, `enterprise_d_veridian_loss`, `voyager_delta_displacement`, `voyager_maquis_starfleet_crew` | Primer despliegue Defiant en DS9, pérdida Enterprise-D, desplazamiento Voyager; lugares y trayectorias distintas. |
| 2372 | `changeling_infiltration_discovered`, `klingon_cardassian_invasion` | `leyton_star_fleet_coup_attempt` | Infiltración y crisis del intento de Leyton; nadie obtiene datos secretos por leer el atlas. |
| 2373 | `bajoran_dominion_nonaggression`, `bajoran_federation_membership_deferred`, `cardassian_dominion_accession`, `dominion_cardassian_war_bajor`, `dominion_war_begins`, `klingon_federation_reconciliation`, `maquis_pressure_war`, `orion_syndicate_infiltration`, `romulan_dominion_nonaggression`, `thal_dominion_nonaggression` | `sector_001_borg_invasion` | Escalada Dominio/Cardassia, inicio Guerra del Dominio y ataque Borg del Sector 001; no simultaneidad automática. |
| 2374 | `romulan_enters_war`, `section31_revealed` | `voyager_borg_8472_contact`, `ds9_operation_return`, `voyager_hirogen_crisis` | Campaña bélica con Operación Retorno; implicaciones Borg/8472 en recorrido de Voyager. |
| 2375 | `breen_enter_war`, `cardassian_fleet_switches`, `cardassian_resistance`, `damar_rebellion`, `derna_hospital_dispute`, `rom_becomes_nagus`, `treaty_of_bajor` | `defiant_chintoka_loss`, `sisko_joins_prophets` | Cierre canónico de la Guerra del Dominio, caída Defiant original y cambio de estatus de Sisko. |
| 2376 | — | `voyager_vaadwaur_encounter` | Historia de Voyager continúa en Delta, con episodio Vaadwaur; no licencia rutas al DLC. |
| 2377 | — | `voyager_unimatrix_zero` | Conflicto de Unimatrix Zero; conocimientos fragmentados y no accesibles a todo personaje. |
| 2378 | — | `voyager_talaxian_settlement`, `voyager_canonical_return` | Tramo final Voyager y regreso canónico, no retorno obligatorio de las partidas anteriores. |

| 2379 | — | `nemesis_shinzon_romulan_crisis`, `riker_titan_captaincy` | Shinzon, pérdida de Data y transición de Riker a capitán de Titan; **inicio propuesto** del programa Valhalla GAME_ADDITION. |
| 2380 | — | `cerritos_era_2380` | Era Cerritos; construcción prevista de Valhalla como adición del juego. |
| 2381 | — | `picard_promoted_admiral` | Picard asciende a almirante; la construcción e integración Valhalla continúan según propuesta. |
| 2382 | — | `protostar_delta_assignment` | Salida Protostar/Chakotay; Valhalla sigue en construcción/integración, sin comisión hasta el objetivo 2387. |
| 2383 | — | **GAME_ADDITION_ODYSSEY_2383** (no pantalla) | **Ingreso en Academia (año aprobado)**; Odyssey ya en servicio y punta de lanza de Flota. Valhalla continúa en desarrollo. Flujo cuántico en unidades Odyssey de pruebas, no estándar. |

## Hito posterior al inicio del juego (GAME_ADDITION; no historia canónica previa)

- **2387:** objetivo de puesta en servicio de la primera Valhalla; no es evento obligatorio en partidas iniciadas en 2383. La madurez del flujo cuántico y la posible instalación en la clase pueden requerir pruebas posteriores. La fecha exacta de botadura y de graduación están pendientes; pueden no coincidir.

## Antecedentes anteriores a 2364

- **2293 aproximado:** proceso de Khitomer referenciado por `khitomer_diplomacy`. Es contexto político Klingon–Federación y memoria institucional, no época seleccionable.
- **Bajor:** presencia militar, anexión y posterior ocupación deben distinguirse. Las referencias secundarias discrepan entre fechas de ~2319 y ~2328 para definir comienzo; *no* se fija en esta fase una fecha exacta de inicio. Retirada = 2369 aproximado, ya documentada en LORE-01 D.
- **Federación–Cardassia:** hostilidades y tensiones previas a acuerdos fronterizos de 2369–2370; no inventar día inicial de la guerra o tratados no fechados.
- **Naves veteranas:** Miranda, Oberth y Excelsior pueden operar en siglo XXIV cuando exista un casco/estado documentado; no convierten los años Kirk en periodo jugable.
- **Amenaza Borg:** contacto, conocimiento institucional y memoria no son sinónimos. La ofensiva 2366 de LORE-01 D y batalla 2367 de este índice forman un **punto de revisión cronológica**: no declarar dos invasiones independientes por diferencia de año aproximado.

## Temporalidad, información y eventos de pantalla

1. **Pantalla anterior a D:** bootstrap histórico sólo con procedencia y compatibilidad causal. **Pantalla posterior a D:** registro de investigación posible, **no** verdad futura garantizada.
2. Un `reference_year` no es una fecha exacta. **Comparación de año con mismo año = indeterminada**, nunca autoactivar el desenlace.
3. Una historia sobre viajes temporales, como *First Contact* o *Endgame*, puede existir como **registro histórico de ficción**, pero **se mantiene la prohibición de viajes temporales jugables** y de misiones basadas en reescribir el pasado.
4. Cambios creativos antes de D requieren aprobación expresa del autor y etiqueta `GAME_ADDITION`; la fuente `SCREEN_CANON` no se borra.
5. Separar guerra, ocupación, soberanía, control de una estación, armisticio y reconocimiento; los contratos de simulación estratégica son preexistentes y sólo se enlazan en LORE-03B.
6. No se deducen clases/tecnologías de un GLB, la existencia de un episodio, ni de un personaje histórico. Clase ≠ unidad concreta ≠ assignment.
7. **Sutherland**: su intervención en el contexto de guerra civil klingon de 2368 permite referencias históricas a una nave específica, no significa que el puente prototipo en UE5 reproduzca automáticamente su estado histórico.

## Academia, personajes y Valhalla en 2383–2387

El cadete entra en 2383 (año aprobado, día/mes abiertos) y completa cuatro cursos hasta graduarse aproximadamente en 2387. Odyssey ya opera como nave punta de lanza cuando comienza la Academia. Valhalla inicia el programa tras Némesis (2379), construcción/desarrollo desde 2380 y tiene **primera comisión objetivo en 2387**, tras **siete años**. Su incorporación como destino de alférez exige entrada en servicio efectiva y vacante real; no se presupone disponible antes de la graduación. Picard ya es almirante (2381), Riker capitán de Titan (2379), Janeway almirante, Geordi sin destino 2383 verificado. Ninguno está congelado en un puesto de las series. Rómulo no está destruido en 2383, sino en 2387 en el referente de pantalla; su destrucción no se impone como futuro del guardado.

## Riesgos de anacronismo en las naves

| Elemento | Estado editorial conservador |
|---|---|
| Enterprise-D | Participa en 2364+, pérdida Veridian III ~2371 si D es posterior y no hay GAME_ADDITION específica |
| Enterprise-E / Sovereign | StarTrek.com sitúa presencia de Enterprise-E alrededor de 2372 y combate Sector 001 en 2373; catálogo actual sólo afirma Sovereign en servicio **como muy tarde en 2373** (no fecha estricta de primera botadura). No colocarla en 2364 |
| Voyager / Intrepid | Viaje canónico 2371–2378; disponibilidad de Voyager y clase individual dependen de D, no de tener el modelo del puente |
| USS Defiant | Desplegada en 2371, pérdida del casco original en 2375; otra nave rebautizada no hereda mágicamente matrícula/daños |
| Odyssey / Enterprise-F | **Clase Odyssey operativa desde 2383** por GAME_ADDITION autoral y líder tecnológico al comenzar Academia; **no** inferir que Enterprise-F concreta está entonces en servicio ni copiar su historia futura de pantalla |
| Clase Valhalla | Programa después de Némesis (2379), construcción/desarrollo 2380–2387 y **primera comisión objetivo 2387 (GAME_ADDITION)**; destino de alférez sólo tras comisión real y vacante legítima |

## Revisión y reservas

La bibliografía de hechos son episodios/películas registradas y referencias oficiales añadidas al registro central en esta PR. El registro documental fue auditado estructuralmente; **no se ha visionado toda la filmografía ni resuelto hasta el día cada fecha**. La diferencia 2366/2367 de la ofensiva y la datación de algunas crisis diplomáticas permanecen documentadas para contrastes posteriores. Las fichas originales de LORE-01 D no se editan ni duplican.

**Contratos:** `mundo/lore/historical_events/historical_event_contract.json`, `mundo/lore/conflicts/conflict_definition_contract.json`, `sistemas/gameplay/conflict/conflict_war_index_v0.1.json`. Nadie debe interpretar este Markdown como evento emitible por IA o simulador.
