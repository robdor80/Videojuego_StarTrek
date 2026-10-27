# B08 — Auditoría preparatoria y criterios de cierre

## Dictamen actual

**DOCUMENTACIÓN PREPARATORIA: PRODUCIDA — NO FUSIONADA, NO VALIDADA EN CI DEL REPO.**

El material se mantiene aislado de GitHub mientras ST-ORG-01 no conste terminado. No llamar LORE-03B `COMPLETE` hasta integrar, ejecutar pruebas reales, revisar y fusionar con autorización. La comprobación local que acompaña este ZIP valida referencias contra una **instantánea parcial verificada** del repositorio, no suplanta la ejecución sobre `main` actualizado.

## Puertas de aceptación futuras

- [ ] ST-ORG-01 terminado y verificado por autor y/o evidencias verificables.
- [ ] Rutas reconciliadas con organización definitiva; no eliminar ni sobrescribir archivos previos.
- [ ] Fuentes/IDs validados contra registro central actualizado, especialmente campos `source_refs`.
- [ ] Fecha D y orden de eventos del mismo año tratados sin falsear precisión.
- [ ] Un solo conflicto `dominion_war`, sin duplicación por eventos o resistencia cardassiana.
- [ ] Revisión editorial de fronteras, pactos, colectivos y facciones no estatales.
- [ ] Tzenkethi falso golpe preservado como falsedad; guerra previa referida como hecho distinto.
- [ ] Romulus no destruido en 2383; Shinzon 2379 no sustituido por supernova futura.
- [ ] No alteración de esquema/mecánicas de CoreRPG/UE5 y cero efectos en WorldState.
- [ ] Ejecutar validador local sobre rutas reales tras ST-ORG-01, pruebas positivas/negativas y regresiones LORE-01D/LORE-02E/LORE-03A.
- [ ] Incidencia preexistente F07 arreglada o declarada como reserva de regresión ajena, con logs y aprobación; no falsear `NO_EJECUTADO`.
- [ ] PR única LORE-03B con CI verde, revisión humana, autorización explícita de fusión.

## Hallazgos y reservas

**B-AUD-01:** `lore/conflicts/README.md` seguía reservado; `lore/conflicts/` contenía solamente contrato, sin dosieres, al auditar `main@a5f76737`.

**B-AUD-02:** existe índice estratégico `conflict_war_index_v0.1.json`; manifest declara 18/18 paquetes y simulador/pruebas de referencia. Ello NO equivale a implementación CoreRPG.

**B-AUD-03:** las 5 definiciones diplomáticas de conflictos y 7 tratados existentes no son expedientes completos; este paquete añade historia y contexto.

**B-AUD-04:** discrepancia editorial en ofensiva Borg 2366 versus Wolf 359 2367; inicio de ocupación Bajor ~2319/~2328; dos eventos Dominion solapados: conservar reservas y no corregir LORE-03A.

**B-AUD-05:** la última ejecución de workflow LORE-02 E falló en regresión F07, porque la prueba exige 9 `NO_EJECUTADO`, mientras 4 registros UE5 ya se marcaron «reportado pendiente de cotejo». No significa que LORE-02 documental fallara.

**B-AUD-06:** descripciones de algunos resultados incluyen inferencia editorial; revisión de escenas/anclas críticas pendiente antes de aceptación final.

## No acciones

No se ha creado rama ni PR, modificado `main`, importado un Content Pack ni ejecutado nada en UE5/CoreRPG. Este entregable es externo al repo, autocontenido y de preparación.