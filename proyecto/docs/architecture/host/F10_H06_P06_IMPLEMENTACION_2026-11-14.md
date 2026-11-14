# F10 / H06-P06 · Implementación del corte nativo

**Fecha** 14-11-2026. **Alcance implementado** Prueba de factibilidad nativa sobre el pin CoreRPG, con compilación de pruebas aislada e integración en CI. **Alta productiva** BLOCKED en la doble validación F10.

| Archivo | Función |
|---|---|
| [academy_core_feasibility.cpp](../../../../desarrollo/integration/host/tests/academy_core_feasibility.cpp) | Conecta directamente con la biblioteca del pin. Construye un campus de ensayo con catálogo propio y ejercita población, PERSON, hecho de creación, almacenamiento de biografía, recuperación y fallos. |
| [academy_core_feasibility.py](../../../../desarrollo/integration/host/tests/academy_core_feasibility.py) | Ejecuta escritura, recuperación y rechazo de archivo manipulado en procesos distintos, con directorio de salida único. |
| [CMakeLists.txt](../../../../desarrollo/integration/host/CMakeLists.txt) y [CI HOST](../../../../.github/workflows/host-h02-native.yml) | Registran y ejecutan `host.academy.core_feasibility` en Windows, Linux y Linux ASan/UBSan. El ejecutable solo se construye con `TREK_HOST_TESTS=ON`. |
| [inspect_product.py](../../../../desarrollo/integration/host/tests/inspect_product.py) | Comprueba la ausencia del binario experimental en Release de producto. |

La prueba usa entradas estructurales deterministas. El texto de ensayo carece de una aprobación biográfica y el proceso solo publica en su archivo Core de prueba. La cohorte del ensayo sirve para comprobar el balance poblacional; su cifra no se propone para una campaña.

## Secuencia pendiente de producto

| Tramo | Estado y salida necesaria |
|---|---|
| F10-A · borrador | BLOCKED. Mantener la biografía en el flujo conceptual de borrador hasta disponer de reglas objetivas ejecutables y revisión semántica verificable, ambas bajo F10. El proyecto aún carece de un editor de borrador de Academia expuesto por HOST. |
| F10-B · candidato | BLOCKED. Con una revisión válida, registrar PERSON, identidad genérica, intención idempotente, revisión y hecho de candidatura en un solo Core, con rollback. Una confirmación separada de admisión requerirá pruebas de acceso válidas y plaza real. |
| HOST-C · vínculo | BLOCKED por el recibo F10. El vínculo de jugador Academy debe ser único y durable en el mismo estado. Debe denegarse `SUBMIT_SCAN` en la pasarela antes de F05 y sin mutación para un candidato sin competencia naval. |
| HOST-D · ranura | BLOCKED por el alta y el vínculo. Introducir un sobre explícito y elegir el lector por versión/escenario/catálogo, verificando procedencia y coherencia completa antes del swap. El restablecimiento H04 de una sesión naval conserva su vía actual. |
| HOST-E · Unreal | NOT_RUN por la cadena previa. La ABI de nave conserva la prueba C11 `OPEN academy`. La operación Academy y su proyección de GameInstance requieren un alta, vínculo y restore nativos probados. |
| Continuidad F11 | BLOCKED para CB-24. La identidad genérica existe como concepto desde candidatura; la profesional requiere comisión F11. El acuerdo sobre un vínculo duradero y su migración queda a cargo de F10 y F11. |

El pin, F04/F05/F11, las operaciones de HOST y las fuentes de Unreal conservan su código. La PR se mantiene Draft para auditoría de [#148](https://github.com/robdor80/Videojuego_StarTrek/issues/148) y seguimiento de [#144](https://github.com/robdor80/Videojuego_StarTrek/issues/144). F10 sigue abierto y H06/M1 parciales. H13 mantiene su certificación pendiente.
