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

## 3. Auditoría independiente y evidencia verificable
- **Diff auditado:** PR #46 contra `main@32f4a018bc75b37ff0a4e10fb466ffac6963c381`: únicamente documentación LORE-03D, validador/test nuevos, workflow y nota de plan maestro. `CONTENT_STATUS.md` se ha restaurado al original para mantener la invariante pre-merge de LORE-03A. Ningún contrato propietario ni fichero de LORE-03A/B/C modificado.
- **CI previa verificada:** workflow LORE-03D [run 40504585803](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40504585803), `SUCCESS`, incluye compilación, validador y 45 pruebas D y regresiones LORE-03A/B/C y LORE-01D/02E. Workflow LORE-03A [run 40504585702](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40504585702), `SUCCESS`. Ambas sobre commit `e4b24c77af2d97829a35ceb4261edf4d1bf21a4f`.
- **Incidencia encontrada y resuelta:** el validador previo de LORE-03A exige que la fila D siga `TODO` hasta autorización/fusión; marcar anticipadamente `NEEDS_REVIEW` en `CONTENT_STATUS.md` provocó fallo verificable [run 40504418752](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40504418752). Se restauró íntegramente el archivo sin alterar el validador A. La PR y el índice de D reflejan `NEEDS_REVIEW_DOCUMENTARY` hasta aprobación.
- **Puerta final:** toda revisión de este acta genera un nuevo HEAD y requiere comprobar también las nuevas ejecuciones de CI; la evidencia anterior no se atribuye falsamente a un SHA diferente.
- **Limitación de alcance:** estas son pruebas de integridad referencial/puertas documentales; **no** hay prueba de simulación, persistencia, migración, Host, UE5 o IA reales, ni revisión audiovisual exhaustiva. El cierre sigue `NEEDS_REVIEW`, no `COMPLETE`.

## 4. Decisiones de autor realmente pendientes
1. **Día/mes exactos del inicio de 2383** y criterios para resolver hechos del mismo año cuando sean relevantes.
2. **Fechas de botadura/entrada en servicio y matrícula** de la primera Valhalla (los objetivos 2379–2383 no las fijan).
3. **Decisiones narrativas excepcionales pre-2383**, si se pidieran: cada `GAME_ADDITION` individual requiere aprobación. No se propone ninguna aquí.

No se requiere que el autor decida el destino de Rómulo, de los NPC o de las campañas futuras: dejarlos abiertos **es la decisión aprobada**. LORE-03E — auditoría global A–D — sigue pendiente como fase independiente.

## 5. Puerta de cierre
Documentación `NEEDS_REVIEW_DOCUMENTARY` → CI y auditoría técnica → revisión del autor → autorización **expresa** para fusionar → PR de cierre administrativo con SHA reales y estado `COMPLETE`. **Nunca** autofusión, auto-merge ni eliminación de rama.
