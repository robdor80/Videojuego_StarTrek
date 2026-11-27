# H07 — Auditoría independiente de reconciliación con H08 (27-11-2026)

> **Acta de seguimiento previa al cierre.** No es una certificación, ni un acta de aceptación visual. Se actualizará con SHAs de fusión y resultados concluyentes antes de presentarla como acta de cierre. Ninguna prueba no ejecutada puede pasar a PASS.

## Alcance y autoridad

La entrega H07 consume expedientes y ascensos **ya confirmados** por F11/CoreRPG mediante una proyección de lectura privada al HOST y un adaptador C v1 consumido por Unreal. El emisor institucional productivo **no existe todavía**: las operaciones de emisión siguen en `SERVICE_UNAVAILABLE`. Un candidato Academy no se convierte en oficial ni obtiene permiso F05/F11. CoreRPG mantiene la autoridad. La ABI H05 y Academy v2 y el pin CoreRPG `76a7b7b485616d8c4994f384a90f123bf333591d` se conservan en la entrega examinada.

## Evidencia histórica ya auditada (23-11-2026)

| PR | Entrega | SHA previamente probado | Evidencia |
| --- | --- | --- | --- |
| [#203](https://github.com/robdor80/Videojuego_StarTrek/pull/203) | H07-P01/P02/P04 | `94fbd7f593ec3d7d753b753a1200deef40a5f683` | Contratos y frontera estáticos, pruebas negativas P02, CTest nativo y producto |
| [#204](https://github.com/robdor80/Videojuego_StarTrek/pull/204) | H07-P03 lector nativo | `3eb8ca458f64785741fbb1167ae49422a7c67042` | 26/26 jobs en 7 workflows, CTest 314/314 por SO, 159/159 ASan/UBSan; auditoría independiente |
| [#205](https://github.com/robdor80/Videojuego_StarTrek/pull/205) | H07-P05 Unreal y corrección H06 | `462d2dbd0447fbe5efd70bf4f0e23e0f484442f6` | 7/7 jobs; 315/315 Linux/Windows, 160/160 sanitizers; manifiesto MSI con 29/29 ejecuciones Automation según Codex; auditoría independiente favorable con reserva visual |

La evidencia del MSI del 23/11 está asociada al **código de aquella fecha**, no automáticamente a la revisión de integración de noviembre 27. La prueba visual humana de la ventana H06 y de H07 seguía pendiente. En H06, el cliente de modo ventana calculado a 150 % es `2538×1472` dentro de la zona de trabajo, no un cliente literal 2560×1600. No se ha acreditado nueva pulsación física del ratón, foco, Escape, Alt+Intro o Alt+F4.

## Dependencia sobrevenida: H08 ya fusionada

Desde entonces [H08-P01 #207](https://github.com/robdor80/Videojuego_StarTrek/pull/207), [H08-P02 #208](https://github.com/robdor80/Videojuego_StarTrek/pull/208), [H08-P03 #209](https://github.com/robdor80/Videojuego_StarTrek/pull/209) y [H08-P04 #210](https://github.com/robdor80/Videojuego_StarTrek/pull/210) se fusionaron antes de H07. `main` estaba en `e2a3dbe46c6dd395932405abb2abaf0fe9a9b776` al iniciar esta auditoría. La PR #203 no era fusionable directamente por cambios concurrentes en fuentes HOST y CI.

Para evitar perder eventos, relojes, notificaciones H08 o consultas F11 H07, se han integrado **sin reescribir los pines históricos** en las mismas ramas apiladas, manteniendo `main` intacta hasta CI:

- #203: `b159019eeb40a39457dbb90e498f233788fef9ec`.
- #204: `07bd012422c22a137aff0af0adc0aadec8281342`.
- #205: `9ad935d0976978db6b8463f069834cf04e900018`.

Las verificaciones nuevas se solicitan mediante PR temporales [#221](https://github.com/robdor80/Videojuego_StarTrek/pull/221), [#222](https://github.com/robdor80/Videojuego_StarTrek/pull/222) y [#223](https://github.com/robdor80/Videojuego_StarTrek/pull/223), que **no deben fusionarse**. En la primera ronda combinada, CTest H07-P02 detectó una referencia de enlazado `gateway_test_after_clock(F04Session*)` introducida por H08 en el núcleo: se corrigió en los **fixtures H07 independientes**, sin cambiar el reloj ni la autoridad del producto. Ese primer resultado fue **FAIL**, no PASS. Nuevas ejecuciones CI están solicitadas para los SHAs corregidos y deben verificarse antes de fusionar.

## Estado de cierre (pendiente de completar)

| Puerta | Estado previo a fusión |
| --- | --- |
| Auditoría original #203–#205 | FAVORABLE dentro de sus SHAs originales |
| Reconciliación H07+H08 | PREPARADA en ramas, pendiente de CI concluyente |
| Fusiones en `main` | NO REALIZADAS en esta revisión preliminar |
| Producto F11 emisor | BLOQUEADO / `SERVICE_UNAVAILABLE` |
| Aceptación visual/controles MSI actual | **NO EJECUTADA** por indisponibilidad física del usuario |
| Certificación integral H07 | **NO CERTIFICADA** |

**Regla de cierre:** comprobar CI verde en la composición, fusionar #203 → #204 → #205 después de corregir sus bases, actualizar SHAs y resultados reales de fusión y concluir expresamente un alcance técnico; dejar H07 pendiente de aceptación humana/Unreal final donde no exista evidencia del SHA fusionado. No transformar el presente informe preliminar en certificación por redacción.
