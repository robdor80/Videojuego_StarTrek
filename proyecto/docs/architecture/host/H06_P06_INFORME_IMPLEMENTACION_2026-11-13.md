# H06-P06 · Informe de implementación

**Fecha** 13-11-2026. **Entrega parcial** en la [PR #147 Draft](https://github.com/robdor80/Videojuego_StarTrek/pull/147), rama `codex/host-h06-p06-20261113`, desde `9619e2baadc7bf4e19c4e6cd9025e81da209a794` (PR #146 fusionada). **Revisión de código sometida a pruebas** `dceb892d00d4992cdb417f423938a8ce8fce1675`. El SHA final de la entrega, que incorpora los informes, figura en la [ficha de la PR](https://github.com/robdor80/Videojuego_StarTrek/pull/147) y en su [lista de commits](https://github.com/robdor80/Videojuego_StarTrek/pull/147/commits).

## Cambio realizado

Se añadió `host.abi.unsupported_academy_open` al consumidor C11 existente de TrekHost, bajo `TREK_HOST_TESTS=ON`. El test usa la ABI pública, un cliente sin raíz de guardado y el puente real. Envía `OPEN` con `class_id=academy` y parámetros de población por lo demás válidos. Comprueba el rechazo `INVALID_ARGUMENT`, finalización de ticket con generación y payload vacíos, estado final `CLOSED`, ausencia de principal y servicio institucional `SERVICE_UNAVAILABLE`. Un segundo cliente puede abrir y cerrar el escenario Miranda permitido y queda `PRINCIPAL_UNBOUND`. Esta última comprobación demuestra que el intento fallido liberó la reserva de campaña. El test observa la publicación de sesión y la reserva desde C11. Para comprobar el estado interno de una transacción de Academia se necesita el factory de F10. [Prueba C11](../../../../desarrollo/integration/host/tests/host_abi_tests.c), [Registro CTest](../../../../desarrollo/integration/host/CMakeLists.txt).

El nombre `academy` se usa como entrada de clase no admitida por la ABI v1 de esta revisión. Si F10 entrega una ruta de producto, su prueba positiva debe usar el contrato aprobado de alta y comprobar el WorldState. El modo `OFF` excluye esta prueba y el registro CTest por el mismo guard que la suite anterior. Las suites históricas conservan sus oráculos y entradas. El diff de código afecta solo al ejecutable de pruebas y su registro bajo `desarrollo/integration/host/`. [Composición CI](../../../../.github/workflows/host-h02-native.yml).

## Límite del corte de producto

| Tramo | Estado | Condición para implementarlo |
|---|---|---|
| P06-A · Alta candidata y posterior admisión | BLOCKED | Factory F10 de campaña Academia, perfil validado, catálogo y política de plaza/cohorte. |
| P06-B · Vínculo H03 | BLOCKED | Resultado interno de alta comprobable en la campaña y vínculo persistente separado de la iniciativa F05. |
| P06-C · H04 y Unreal | BLOCKED | Recuperación versionada con el catálogo de Academia y comprobación de su vínculo; después ABI de intención/vista y prueba MSI. |

La prueba nueva cubre el rechazo de una entrada por la composición actual. No se implementó un adaptador de Academia porque no hay una fuente autoritativa o una vista de candidato que pueda consumir. La puerta de elegibilidad F05 de la campaña de nave permanece en su dominio. El [informe de factibilidad](H06_P06_INFORME_FACTIBILIDAD_2026-11-13.md) detalla los dos diseños y la decisión pendiente sobre continuidad F10/F11. La [matriz de resultados](H06_P06_RESULTADOS_2026-11-13.md) acota la evidencia de las regresiones de H03/H04/H05 y de la frontera C. HU-08 y M1 siguen pendientes. Seguimiento en [#144](https://github.com/robdor80/Videojuego_StarTrek/issues/144).

## Entorno, disco y conservación

Se creó una rama con checkout disperso dentro de la carpeta ignorada propia `laboratorios/host/h06-p06-20261113` del repositorio principal. Usa los objetos Git compartidos y el checkout CoreRPG local existente, que se verificó limpio en el pin. No se hicieron builds locales nativos o UE. Se reutilizó el workflow HOST de GitHub Actions para Windows, Linux, sanitizers y Release OFF. El checkout y las evidencias locales ocupaban aproximadamente 10,6 MB de contenido al redactar el informe. Incluyen fuentes dispersas de Git, logs Python y artefactos de CI. Todo se puede obtener de las fuentes o regenerar con los comandos de la matriz. El directorio propio está registrado como worktree Git en `w` y debe tratarse como tal al retirarlo en la limpieza autorizada. No se realizó ningún borrado, movimiento o modificación de laboratorios históricos o compartidos.
