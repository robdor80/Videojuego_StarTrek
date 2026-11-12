# A01 — Inventario, contradicciones y precedencia

| Fuente preexistente | Evidencia / significado | Tratamiento vigente |
|---|---|---|
| F01 DEC-0001, PR #2 | «Nueva clase Valhalla inspirada en Galaxy» | **HISTÓRICA para la nave protagonista**; no sobrescribir el expediente |
| LORE-03 PR #38 | Primer planteamiento Academia 2383 y Valhalla 2383 | Cronología de servicio 2383 superada por DEC-0015 |
| DEC-0013–0016, PR #69 | Odyssey operativa 2383, Academia 2383, programa 2379/2380–2387 y flujo cuántico experimental | **MANTENER FECHAS**, reinterpretando «construcción de clase» como reconstrucción individual Enterprise-D |
| Tecnología `valhalla_tech_decisions_v0.1.json` | Identificador `NEW_VALHALLA_CLASS_GALAXY_INSPIRED_NOT_GALAXY_REFIT` | Legado, **no** identidad nueva; no reemplazar silenciosamente la cadena porque puede haber consumidores |
| `core_starship_classes.json` | `class_id=valhalla` histórico y `class_id=galaxy` | Preservar ambos IDs; la **Enterprise-D** usa `galaxy`, no `valhalla` |
| `core_canonical_ships.json` | Nave `uss_enterprise_ncc_1701_d`, `NCC-1701-D`, clase `galaxy` | Fuente de identidad de nave; NO duplicar el registro de buque |
| F04 PR #74 | 1.800 personas Flota + 400 civiles, plantilla anterior | Dato heredado, **NO transferir automáticamente** al refit individual |
| F06 PR #91 | Perfil de Sensores Enterprise-D modernizada, distinto de una clase Valhalla | Compatible en intención, integración y aceptación jugable pendientes; PR Draft |
| F11 PR #98/#101 | Enterprise-D como destino y capitanía aspiracionales | **Vigente** y compatible con DEC-0020; no concede vacantes ficticias |
| Estilo Galaxy Refit A2 | Interiores de lujo y LCARS azul/cian | Dirección artística vigente, **no** demuestra capacidades o colliders |
| *Generations* / *Picard* | 2371 Veridian; reconstrucción exhibida en 2401 | Separar **canon en pantalla** de **objetivo alternativo 2387** |

## Hallazgos

- **H05A-01 / RESUELTO EN IDENTIDAD:** nueva clase Valhalla no es la nave aspiracional; el buque es Enterprise-D individual de clase Galaxy.
- **H05A-02 / RESUELTO EN CRONOLOGÍA DOCUMENTAL:** 2379–2387 se conserva como programa de reconstrucción y objetivo de alistamiento, no como hechos de pantalla.
- **H05A-03 / RESERVA DE RUNTIME:** clase `valhalla`, plantilla F04 y tecnologías antiguas permanecen hasta migración de consumidores en sus fases; este bloque no certifica esa migración.
- **H05A-04 / RESERVA CANÓNICA:** los ~20 años de reconstrucción mencionados en *Picard* no son una fecha exacta de comienzo. Un objetivo 2387 diverge deliberadamente del relato de 2401.
- **H05A-05 / RESERVA JUGABLE:** no se garantiza en una partida real que en 2387 la nave esté lista, exista vacante o se haya instalado la propulsión cuántica.

## Orden de autoridad

**DEC-0020 (identidad, propósito y reinterpretación)** > DEC-0013–0019 en aspectos que cambie expresamente > actas de diseño anteriores.  
Las decisiones previas **no modificadas** retienen su fuerza y procedencia. El estado de ejecución pertenece a CoreRPG/Host, y ninguna entrada de lore cambia automáticamente un guardado.

No se han identificado otros cambios autorales aprobados en esta revisión que justifiquen borrar contenido antiguo.
