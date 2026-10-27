# C08 — Auditoría transversal y criterios de aceptación
**Estado antes de fusión:** NEEDS_REVIEW_DOCUMENTARY. No afirmar cierre COMPLETE, merge, eliminación de rama o integración CoreRPG.

## Artefactos verificables
- C01–C08: ocho documentos autónomos en esta carpeta; preservan ST-ORG-01.
- `mundo/lore/historical_events/lore03c_memory_casebook_v0.1.json`: casos **hipotéticos** anclados en hechos preexistentes; no NPC canónicos nuevos.
- `mundo/lore/historical_events/lore03c_institutional_patterns_v0.1.json`: patrones institucionales condicionales, sin memoriales/archivos creados.
- `desarrollo/tools/validation/validate_lore03_c.py` y `test_lore03_c.py`: comprobar límites históricos, fechas, creencias, edades, acceso, duplicación, dependencia de contratos y pruebas de mutación.
- `.github/workflows/lore03-c-memory.yml`: gate documental C y regresiones de 03A/B, 01D y 02E.

## Condiciones innegociables
1. C no crea hechos nuevos, personas reales de la ficción, guerra/tecnología ejecutable ni sus estados.
2. Falsa noticia del golpe tzenkethi sigue siendo falsa.
3. Diferencia fecha de la ofensiva Borg (2366) y Wolf 359 (2367 aproximado) no produce segunda invasión.
4. Fecha D: año 2383 propuesto; día/mes sin fijar; Rómulo vivo; 2387 no forma parte de pasado ni futuro impuesto.
5. Un caso de biografía debe rechazar nacimiento posterior al acontecimiento, participación sin evidencia, conocimiento clasificado sin acceso y recuerdos imposibles.
6. Dos participantes pueden recordar distinto; compartir guerra no presupone conocerse.
7. Reconocimiento de «Sensores Rise» permanece ejemplo, nunca instalación o invención efectivas.
8. La memoria y los hechos no se resetean por LOD/guardado.
9. Scripts de validación no implementan estados de CoreRPG ni hacen mutaciones.
10. Validación verde significa integridad **editorial y de ejemplos**, no corrección escena a escena del canon ni interoperabilidad runtime.

## Reservas y deuda posterior
- Ejemplos de servicio histórico son ficticios y se deben convertir a procedencia de individuos concretos **antes** de activar NPC; historia solo por año exige cautela ante el orden día/mes.
- Sigue pendiente el trabajo transversal de reparar menciones obsoletas de épocas jugables en documentación general; no tocar contratos de otras fases sin trazabilidad.
- Contratos de `sistemas/ai/lore_context` y `sistemas/narrative/historical_intersections` reservados: C los referencia, no añade una segunda autoridad de memoria ni pone runtime en marcha.
- La compatibilidad con repositorio CoreRPG no se certifica por esta fase; esa auditoría requiere cotejo específico posterior.
- LORE-03D/E, activación de misión Omega, misiones y transición de datos a live WorldState permanecen fuera del alcance.

## Procedimiento de cierre administrativo posterior
Con PR revisada, CI verde y autorización expresa del autor: fusionar, verificar HEAD, actualizar estado de C con PR/SHA reales en otro cambio administrativo si el validador de A lo necesita, y eliminar rama solo con permiso. Nunca registrar pruebas futuras como ya ejecutadas.
