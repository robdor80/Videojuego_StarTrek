# D08 — Auditoría integral, pruebas negativas y cierre **pendiente de revisión**

## 1. Alcance auditado
Se ha comprobado documentalmente la existencia de la estructura ST-ORG-01, el cierre fusionado de LORE-03A/B/C y los contratos propietarios enumerados en D01. El paquete de D no modifica expedientes anteriores ni crea contenido importable: D01–D08, índice, casos de referencia, validador y pruebas `unittest` se mantienen bajo carpetas existentes. La autoridad sobre WorldState sigue exclusivamente en CoreRPG.

## 2. Matriz de escenarios/amenazas (criterio verificable)
| ID | Prueba | Resultado esperado |
|---|---|---|
| T01 | Reescribir un antecedente anterior a D | **REJECT** |
| T02 | Programar destrucción de Rómulo en 2387 por canon | **REJECT** |
| T03 | Rómulo ya destruido al iniciar 2383 | **REJECT** |
| T04 | Mismo año 2383, orden intranual desconocido | **UNRESOLVED**, no asumido anterior |
| T05 | Suceso autónomo sin causa/procedimiento | **REJECT** |
| T06 | IA establece tratado o cambia WorldState | **REJECT** |
| T07 | NPC conoce hecho futuro o clasificado sin acceso | **REJECT** |
| T08 | Dos guardados con eventos distintos se mezclan | **REJECT** |
| T09 | Save/load modifica prefijo o duplica evento | **REJECT** |
| T10 | Cambio LOD/descarga regenera actor o nave | **REJECT** |
| T11 | Fallecimiento implica trauma universal o identidad borrada | **REJECT** |
| T12 | Ascenso por mero paso del tiempo | **REJECT** |
| T13 | Diferencia por decisiones y causas posterior a D | **ALLOW**, bajo CoreRPG |
| T14 | Retorno de una noticia por comunicación posterior al hecho | **ALLOW** si accesible |
| T15 | Academia no congela eventos civiles a distancia | **ALLOW** si autorizados |
| T16 | Rumor tzenkethi clasificado como golpe real | **REJECT** |
| T17 | Al graduarse en 2387 destino Valhalla garantizado | **REJECT** |
| T18 | Aplicación de sensores Rise sin ciencia/verificación/instalación | **REJECT** |

La colección `D_escenarios_documentales_v0.1.json` aporta casos positivos/negativos que ejercitan estas puertas **como validación editorial**, no como pruebas reales de un motor CoreRPG.

## 3. Revisión independiente prevista/real
- Releer cada D0X por consistencia causal, fecha y autoridad, sin sustituir el control de CI.
- Ejecutar `validate_lore03_d.py`, `test_lore03_d.py` y regresiones A/B/C, LORE-01D y 02E en CI. Registrar resultados reales antes de declarar **verde**.
- Revisar `compare main...rama` para verificar exclusión absoluta de LORE-03A/B/C, sistemas propietarios y todo ejecutable UE5.
- Clasificar incidencias: errores documentales bloqueantes; migraciones runtime explícitamente **no probadas**; decisiones de autor reservadas.
- Estado de esta PR: **NEEDS_REVIEW**, no `COMPLETE`. Esta acta no certifica ejecución de simulación, guardado/carga de CoreRPG, UE5, pantalla o IA.

## 4. Decisiones de autor realmente pendientes
1. **Día/mes exactos del inicio de 2383** y criterios para resolver hechos del mismo año cuando sean relevantes.
2. **Fechas de botadura/entrada en servicio y matrícula** de la primera Valhalla (los objetivos 2379–2383 no las fijan).
3. **Decisiones narrativas excepcionales pre-2383**, si se pidieran: cada `GAME_ADDITION` individual requiere aprobación. No se propone ninguna aquí.

No se requiere que el autor decida el destino de Rómulo, de los NPC o de las campañas futuras: dejarlos abiertos **es la decisión aprobada**. LORE-03E — auditoría global A–D — sigue pendiente como fase independiente.

## 5. Puerta de cierre
Documentación `NEEDS_REVIEW_DOCUMENTARY` → CI y auditoría técnica → revisión del autor → autorización **expresa** para fusionar → PR de cierre administrativo con SHA reales y estado `COMPLETE`. **Nunca** autofusión, auto-merge ni eliminación de rama.
