# F11-P05-A02-03 — Integración nativa incremental: lector Host

**Estado:** primer incremento C++ de consumo de hechos confirmados, no emisor de Personal de Flota.

El contrato/acta de A02-03 existe en la PR anterior (#108). Esta rama añade una
biblioteca **C++20 compilable** que traduce desde la API de producto
`f11_personnel` / `f11_promotion` hacia proyecciones nativas de carrera
y evento de promoción para el Host. Solo lee el `WorldState` de una
`F04Session`; no genera un rango, evaluación, orden, comisión, credencial,
autorización, notificación ni acuse y no incorpora un estado lateral.

## Fronteras

- El código Host llama estas funciones **solo después de autenticar el sujeto
  y autorizar su visibilidad**. Las referencias numéricas y las estructuras
  C por sí mismas no autentican al jugador, ni esto es una API Blueprint.
- La implementación no enlaza ni compila `f11_trial_host.inc` y se prueba
  contra **`TrekF04Bridge` de producto**. En los ensayos se reutilizan
  guardados producidos por el proceso CTest `f11.process_save`, que se inicia
  con el escenario autorizado de ensayo previo; **no se usa ese emisor en
  este ejecutable**.
- El API F11 de producto existente devuelve errores por identidad/scope,
  sujeto incorrecto y falta de comisión. La proyección limpia la salida
  cuando deniega y verifica identidad/evento/visibilidad.
- No se modifica ni el emisor histórico, ni F04, F05, CoreRPG, los oráculos,
  los pins ni el guard congelado A02-02. Esta subbiblioteca está separada para
  que A02-02 continúe siendo un certificado del árbol anterior, no un gate
  artificial para nuevas implementaciones.

## Pruebas

`run_native.py` exige **17 pruebas CTest distintas**, sin SKIP:
13 pruebas F11 preexistentes y cuatro nuevas de lectura nativa
(`f11.host_before`, `f11.host_after`, `f11.host_access`,
`f11.host_legacy`). Se comprueba el compilador MSVC en Windows, el pin
Core `76a7b7b485616d8c4994f384a90f123bf333591d`, los guardados
antes/después de un ascenso, el acceso denegado por sujeto distinto,
`F04_SCOPE`, legados y la ausencia de cualquier cambio de bytes
causado por la lectura.

GitHub Actions utiliza `laboratorios/f11/p05-a02-03/ci/`, ignorado y
eliminable, para compilar y conservar evidencias temporales. **Ningún
artefacto de laboratorio es dependencia de producción.**

## Bloqueos que todavía impiden llamar esto «Host institucional integrado»

1. El Host del producto UE debe determinar quién representa al jugador y
   autenticar el origen de guardados antes de consultar el expediente.
2. Falta servicio institucional **privado** para crear hechos de graduación,
   comisión, concesión, evaluación y orden real, distinto del fixture; no
   se permite exponer al cliente un emisor con bandera verificada.
3. `f11_schema.inc` aún reconoce la raíz de ensayo `CAUSE=110501`. Un
   marcador no es una credencial: el nuevo origen institucional necesita
   diseño, migración controlada y pruebas negativas antes de admitirlo.
4. No hay canal UE5 de producto, comprobación NullRHI/D3D12 en MSI,
   presentación diegética, `presented_at` o autoridad inter-nave.

**No fusionar como integración institucional completa.** Esta PR puede
aceptarse únicamente como incremento nativo de proyección de solo lectura,
tras validar CI y revisión. La F11 global sigue PLANIFICADA.
