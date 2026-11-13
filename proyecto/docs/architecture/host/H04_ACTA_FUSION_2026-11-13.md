# H04 — Acta de fusión y continuidad del HOST

**Fecha:** 13 de noviembre de 2026.  
**Repositorio:** `robdor80/Videojuego_StarTrek`.

## Resultado comprobado

| Apartado | Estado |
|---|---|
| H04-P01/P02/P03/P04 | IMPLEMENTADO |
| Pruebas de H04 dentro de su alcance | PROBADO |
| Incidencia H04-AUD-01 (registro inicial interrumpido) | CORREGIDA y PROBADA |
| PR #135 | FUSIONADA en `main` |
| Certificación integral del HOST y del juego | NO CERTIFICADA; H13 pendiente |

- [PR #135 — H04 guardado, recuperación y procedencia](https://github.com/robdor80/Videojuego_StarTrek/pull/135): **fusionada**, merge commit `7b88a61abf2c3e2878ade8178238c0f068911607`.
- Código y pruebas de la corrección H04-AUD-01: `a191d239503cb72ebe7a19384581330da3d018dd`.
- Commit de entrega documental de H04: `8dc665025153bf4b18b6c12436642768f0f8c249`.
- [CI H04 del código corregido](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43453368894): cinco jobs success. Linux/GCC y Windows/MSVC: 210/210 cada uno. ASan/UBSan: 55/55. Productos Release con pruebas OFF: Linux y Windows PASS.
- [Seis campañas históricas F04](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43433024139): PASS con las fuentes y oráculos históricos conservados.
- El informe técnico original [H04_ACTA_2026-11-13.md](H04_ACTA_2026-11-13.md), [H04_PRUEBAS_2026-11-13.md](H04_PRUEBAS_2026-11-13.md) y [H04_AUD_01_CORRECCION_2026-11-13.md](H04_AUD_01_CORRECCION_2026-11-13.md) son **instantáneas anteriores a la fusión**: sus rótulos «NO FUSIONADA» describen el momento de su redacción. Esta acta posterior documenta el cierre real, sin reescribir las evidencias originales.

## F11: incidencia de alcance resuelta por separado

- [PR #136 — Guard histórico F11 A02-02](https://github.com/robdor80/Videojuego_StarTrek/pull/136): **fusionada** previamente; merge commit `cb0c017f0b36c993833c9c4993b8a44132ec697f`.
- El verificador histórico de allowlist de la certificación A02-02 no se ha modificado ni relajado. Su workflow se limita a repetición manual sobre el commit histórico certificado; no se aplica como guard general a todas las fases posteriores.
- Se mantienen las CI funcionales independientes de F11/F04/F05/HOST. El FAIL anterior del guard temporal sobre H04 **no** fue presentado como una regresión nativa de ascensos.
- La repetición manual del workflow archivado tras #136: NOT_RUN (no se declara PASS sin ejecución).

## Límites y decisiones de producto

- Se excluyen expresamente los **ensayos físicos de corte de alimentación** del portátil MSI; el usuario utiliza el equipo enchufado y cuenta con batería. Se mantienen las pruebas ya realizadas de interrupción de procesos. No se prometen garantías de hardware no verificadas.
- H04 conserva datos estructurados CoreRPG; no almacena modelos 3D, texturas, audio ni vídeo. Los formatos y validadores de Core se mantienen.
- La retención de generaciones anteriores y el volumen real de guardados permanecen por medir; **512 MiB por historial es un límite máximo de seguridad**, no una estimación de consumo normal.
- Tras H05-P04 se medirá tamaño real de campañas y repetición de objetos históricos. La eventual **deduplicación/reutilización por contenido** y la política de retención corresponden a H12-P04, con adelanto solo si las mediciones descubren un consumo desproporcionado. No se optimiza a ciegas ni se borra ninguna generación sin una solución validada.
- La PR #110 de F11 permanece en Draft; el emisor institucional sigue pendiente del proyecto principal Star Trek RPG. H05 construirá el HOST nativo mínimo; H07 conectará la infraestructura con F11 cuando la API institucional de producto esté aprobada. HOST no reimplementa las reglas de F11.
- El proyecto principal Unreal y la integración funcional UE permanecen sujetos a H06 y a verificación real de `.uproject`.

## Siguiente paso

**H05 — Pasarela CoreRPG y primer ciclo funcional nativo.**

No se afirma que H05, H06, H07 ni H13 estén implementadas o certificadas. Este documento es un registro de fusión y continuidad, no una certificación nueva ni una alteración de pruebas históricas.
