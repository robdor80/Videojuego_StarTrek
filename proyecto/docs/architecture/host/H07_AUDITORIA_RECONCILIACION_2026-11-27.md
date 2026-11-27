# HOST H07 — Acta de integración y cierre técnico (27-11-2026)

**Estado: IMPLEMENTADO, PROBADO en CI y FUSIONADO en `main`; CERTIFICACIÓN PRESENCIAL PENDIENTE.** La certificación integral de la fase **no** se declara. El presente documento registra exactamente lo que se ha verificado y lo que aún requiere el MSI.

## Alcance cerrado técnicamente

- **H07-P01:** auditoría de frontera UE/HOST/F11 y contratos.
- **H07-P02:** admisión de identidad, procedencia y validación negativa de órdenes institucionales no habilitadas.
- **H07-P03:** lectura del propio expediente profesional y promociones ya confirmadas por F11/CoreRPG, con invalidación tras SAVE/RESTORE/CLOSE.
- **H07-P04:** matriz de conformidad y comprobaciones de no mutación.
- **H07-P05:** integración de la consulta autorizada en Unreal 5.8.4, proyección Slate de solo lectura y pruebas automatizadas.

El HOST **no** emite ascensos, rangos, comisiones ni hechos institucionales. El emisor F11 de producto continúa en `SERVICE_UNAVAILABLE` y está fuera del alcance de H07. La autoridad de estado y cronología permanece en CoreRPG; la identidad local y el hilo propietario no se eluden. ABI H05/Academy y pin CoreRPG `76a7b7b485616d8c4994f384a90f123bf333591d` preservados en las comprobaciones de las entregas.

## Fusiones verificadas

| Orden | PR | Contenido | HEAD H07 validado en CI | Commit de fusión en `main` |
| --- | --- | --- | --- | --- |
| 1 | [#203](https://github.com/robdor80/Videojuego_StarTrek/pull/203) | P01/P02/P04 | `b159019eeb40a39457dbb90e498f233788fef9ec` | `5b3f242639278fbe7b184488a1ba018f3636f4a4` |
| 2 | [#204](https://github.com/robdor80/Videojuego_StarTrek/pull/204) | P03 | `07bd012422c22a137aff0af0adc0aadec8281342` | `b33a474494ca011b17e8eba6c799fc99a2f745fa` |
| 3 | [#205](https://github.com/robdor80/Videojuego_StarTrek/pull/205) | P05 y corrección H06 ventana | `9ad935d0976978db6b8463f069834cf04e900018` | `5125d8ace7df655f8a44452d001ab745b37c42fc` |

Las tres PR aparecen en GitHub como **merged**. El orden preserva la dependencia P02 → P03 → P05 y mantiene H08 ya fusionada.

## Auditoría y resultados contrastados

1. La rama H07 se reconcilió con los cambios previamente fusionados de H08-P01…P04 (PR #207–#210), conservando distribución de eventos F05, notificaciones, reloj Core, respuestas correlacionadas, comprobaciones de identidad, guardado y recuperación.
2. En la primera integración se detectó un **FAIL** por falta de símbolo `gateway_test_after_clock(F04Session*)` en fixtures nativas independientes; se corrigió solo el adaptador de prueba H07. No se reescribieron reglas del reloj, autoridad institucional, API histórica ni pines Core.
3. **PR #203 integrada:** 5/5 jobs de `HOST native H02-H06` completados correctamente en el SHA conciliado, más contratos H01/H07.
4. **PR #204 integrada:** 7/7 workflows de Actions completados correctamente en el SHA `07bd0124…`, con 5/5 jobs del workflow HOST nativo y 10/10 de integración F05.
5. **PR #205 integrada:** 7/7 workflows de integración (PR temporal #223) completados correctamente en el SHA `9ad935d0…`, más 3/3 workflows específicos de la PR #205; 5/5 jobs del workflow HOST nativo y 10/10 de integración F05. Incluye F04, F11 y pruebas de producto.
6. Evidencia histórica del MSI para el SHA original `462d2dbd…`: informe Codex de 29/29 ejecuciones automatizadas de Unreal y paquete Win64, documentado en `H07_P05_EVIDENCIAS_MSI_2026-11-23.json`. Esta evidencia **no se atribuye** automáticamente al HEAD fusionado.
7. Tras las fusiones, las nuevas ejecuciones de Actions de `main` comenzaron automáticamente: contratos estáticos H07 PASS; las regresiones HOST de los commits de fusión #204/#205 **estaban en curso cuando se redactó esta acta**. Consultar su estado definitivo en Actions; no se registran como superadas aquí.

## Corrección asociada de H06

La PR #205 contiene también la corrección de la geometría de ventana Windows a 150 % DPI. La dimensión física anterior incorrecta era 3840×2400; el cliente ajustado documentado es **2538×1472** dentro del área disponible. Mantiene el modo ventana, sin forzar pantalla completa. **Código FUSIONADO, aceptación visual en MSI PENDIENTE.** No reemplaza retroactivamente el certificado limitado M1 de H06.

## Pendientes explícitos

- **NO EJECUTADO presencialmente:** en el MSI, menú a 1920×1080, modo ventana solicitado a 2560×1600 y pantalla completa, centrado, ratón, teclado, foco, Escape y Alt+Intro.
- **NO EJECUTADO presencialmente:** vista H07 de expediente propio con los estados permitidos y denegados, y verificación tras guardar, restaurar y cerrar. Usar únicamente guardados de laboratorio; no considerar fixture una comisión real del jugador.
- **NO CERTIFICADO:** emisor productivo F11 de ascensos ni autoridad institucional de escritura, expresamente fuera del alcance implementado.
- **NO CERTIFICADO aún:** aceptación visual de H07/H06 ni integración manual final contra el HEAD fusionado `5125d8ac…`.

### Dictamen

**H07 queda integrada y cerrada a nivel de implementación técnica de lectura y denegación, con pruebas CI históricas y conciliadas favorables y fusiones verificadas.** Su **certificación final se mantiene abierta** hasta superar la validación del MSI y registrar evidencia de esa ejecución. No existe autorización para presentar como PASS una prueba física no realizada.

La documentación de este cierre no amplía las competencias institucionales del HOST ni altera CoreRPG.
