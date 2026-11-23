# R1 — Revisión independiente documental de F05-P05B y puerta de cierre

**Fecha:** 19-11-2026  
**Fase:** F05 — órdenes, delegación e iniciativa NPC  
**Repositorio:** robdor80/Videojuego_StarTrek  
**Informe de origen:** proyecto/docs/auditorias/AUDITORIA_PLANIFICACION_1_F00_F15_2026-11-19.md (PR #174)  
**Dictamen:** **CUMPLE LA PUERTA AUTOMATIZADA HISTÓRICA EN EL ALCANCE DE LABORATORIO, PERO NO SE EMITE ACTA FINAL DE CIERRE F05**. Requiere verificación final del paquete de evidencias y aceptación expresa del responsable sobre la incidencia Unreal y el alcance. El estado oficial **permanece EN_CURSO**, sin atribuir UE5_JUGABLE.

## 1. Alcance y método de esta revisión

Inspección remota de **metadatos GitHub de la PR #89**, comparación de commits, informe P05B, resultados estructurados, aceptación original, inventario SHA256, cuatro JSON de pruebas Unreal y fragmentos originales de logs del control de motor. No hay reejecución de C++, CoreRPG, UBT, MSI, UE5 ni partida en esta revisión. Las cifras PASS provienen de los resultados originales versionados. La inspección sintáctica del manifiesto (117 referencias únicas con campos SHA256 válidos) **no equivale** a recomputar los 117 hashes sobre todos los bytes ni verificar la integridad de los artefactos no publicados.

La PR **#89 fue fusionada** (merge commit **f6d52e95ebe9631ab19f83450b87fa1d08576a76**). Su HEAD final fue **b54a50fb784e010e9a06466794cf4161262cfe19**. El código ensayado corresponde a **027bb1d680da1f3317dac00d23ef06e0640c14ba**, CoreRPG separado **76a7b7b485616d8c4994f384a90f123bf333591d**. Comparación GitHub del SHA ensayado con el HEAD final: un commit adicional que modifica únicamente archivos de documentación y agrega evidencias, **sin cambios en fuentes de ejecución F05 probadas**. No confundir SHA del commit documental con el SHA de la compilación.

## 2. Evidencias comprobadas por lectura

| Comprobación | Resultado contenido en evidencia original | Alcance de esta revisión |
|---|---|---|
| PR #89 | **FUSIONADA**, no Draft | Metadatos GitHub contrastados; informes de 05-11 que aún dicen Draft son históricos |
| Ejecución MSI | **2/2** repeticiones oficiales PASS_AUTOMATED | Resumen, aceptación, fechas y argumentos; no reejecutado |
| CoreRPG | **483 descubiertos: 482 PASS + 1 SKIP POSIX autorizado**, 0 FAIL por pasada | El único skip es ContentPackLoaderFilesystemTest.ReportsUnreadableManifestWhenPlatformEnforcesIt |
| Enlaces simbólicos | **3/3 PASS** por pasada, bajo elevación temporal | No equivale a eliminar requisitos de seguridad Windows |
| F04/F05 nativos | **395/395 PASS** por pasada, incluida suite integral P05A y carga entre procesos | Pruebas nativas documentadas, no experiencia jugador |
| DLL | Cada pasada creó DLL con **62 exports**; checksum de staged coincide con DLL compilada | DLL no publicada; hashes referenciados en resultados |
| Unreal UBT | **Succeeded** en dos repeticiones | Unreal Engine **5.8.2** / CL 56702186; laboratorio F05OrdersLab |
| Unreal automatización | Por pasada, **12/12 Success NullRHI + 12/12 Success D3D12 hardware**, 0 FAILED/NOT_RUN | Cuatro informes JSON originales cotejados; no prueba interfaz, escena ni juego completo |
| RHI real | NVIDIA GeForce **RTX 4070 Laptop GPU**, adaptador D3D12 0, SM5 | D3D12 efectivo descrito en logs y manifiesto |
| Controles sin F05 | NullRHI y Hardware terminan con salida **0**, no cargan módulo F05; ambos emiten **14 Condition failed** de arranque | Incidencia está en arranque de instalación Unreal, no en automatizaciones F05 |
| Manifiesto | **117 rutas únicas**, campos de bytes/hashes SHA256 con formato válido | **Pendiente** recomputar hashes individuales; no dar por verificada integridad criptográfica completa |
| Certificación final | acceptance.json: **final_certification=PENDIENTE_ACTA** y **hardware_rhi_acceptance=PENDIENTE_REVISION_LOGS** | Hay verificación técnica positiva, no consta aceptación firmada |

Fuentes primarias: [PR #89](https://github.com/robdor80/Videojuego_StarTrek/pull/89), [informe P05B](F05-P05B_CERTIFICACION_INTEGRAL_MSI_20261105.md), [summary](evidence/F05-P05B/20261105-MSI-INTEGRAL/summary.json), [acceptance](evidence/F05-P05B/20261105-MSI-INTEGRAL/acceptance.json), [SHA256SUMS](evidence/F05-P05B/20261105-MSI-INTEGRAL/SHA256SUMS.json), [control NullRHI](evidence/F05-P05B/20261105-MSI-INTEGRAL/engine-only/control-v2/NullRHI-engine.log) y [control D3D12](evidence/F05-P05B/20261105-MSI-INTEGRAL/engine-only/control-v2/Hardware-engine.log).

## 3. Incidencia UE — tratamiento obligatorio y límites

Los cuatro arranques de automatización y los dos controles del motor registran **14 líneas LogAutomationTest: Error: Condition failed por arranque**, antes de la inicialización del motor. Los controles sin módulos de proyecto ni cola de automatización F05 reproducen la misma incidencia con ambos RHI; la atribución razonable es el **arranque de la instalación UE, independiente de F05**, no una aserción del módulo. **No se sabe qué llamada o test interno emite la condición.** El macro CHECK señalado en LowLevelTestAdapter.h línea 130 es solo una pista. No se recogió stacktrace/PDB de la instalación; **no concluir inocuidad ni arranque limpio**.

La aceptación de **CORE_INTEGRADO en el laboratorio F05** puede plantearse con **excepción de motor explícita y acotada**, siempre que el propietario acepte el riesgo para ese corte y que los logs íntegros demuestren que no contamina los resultados ni provoca bloqueo/mutación. Si se exige identificar la aserción o demostrar su inocuidad antes del cierre, la fase debe quedar abierta hasta esa prueba adicional. En ambos casos esta incidencia permanece visible para F07/F08/F15, que deberán volver a medirla en su producto real; no se hereda automáticamente una exención para la partida UE5.

Advertencias adicionales registradas sin ocultar: C4805 y C4838 en pruebas C++, aviso de Content inexistente del harness, uso de r.MotionVectorSimulation en render thread, avisos de toolchain/compatibilidad del editor. No presentan FAIL en las suites pero continúan como deudas de mantenimiento según alcance.

## 4. Puertas exactas que faltan para ACTA_CIERRE_F05

1. **Integridad y procedencia.** Recomputar/verificar cuando sea viable los 117 hashes del manifiesto contra los ficheros versionados, o declarar con precisión el subconjunto no verificable. Revisar el inventario y las dos actas de ensayo, sus SHAs, Core pin y sus cuatro informes Unreal; los informes originales están presentes. No repetir toda la suite MSI sin motivo técnico concreto.
2. **Aceptación técnica del responsable.** Resolver en acta la marca hardware_rhi_acceptance=PENDIENTE_REVISION_LOGS (aceptación tras leer logs, sin alterar evidencia original). Determinar si los errores de arranque son una **excepción admisible solo para CORE_INTEGRADO F05** o un bloqueante que requiere stacktrace/control de versión UE. No modificar ni suprimir logs.
3. **Alcance de cierre firmado.** Decidir explícitamente que P01–P04 quedan certificados hasta **CORE_INTEGRADO** para las funciones demostradas; P05 se cierra para la integración técnica completa a ese alcance (más allá de su cierre antiguo de suite de referencia). Emitir acta fechada, responsable, SHAs, resultado y excepciones. No declarar UE5_JUGABLE, no proclamar partida operativa ni convertir la PR fusionada en acta por sí sola.
4. **Sincronización del gobierno.** Solo tras (1)–(3): pasar F05 a CERRADA, marcar los cinco pasos CERRADA en el alcance del acta, actualizar madurez alcanzada/por pasos, cierre con evidencias y PLAN_MAESTRO/README y ejecutar de nuevo CI de gobierno. Mantener deudas F04 y F05 de integración UE5 para F08/F15.
5. **Desbloqueo parcial F06.** Al cerrar F05, levantar solo la dependencia de su **componente de órdenes ya validado**. F06 P01 manual, fuente espacial Core/HOST, Ciencia, PR #91→#96→#97 Draft y consola UE5 siguen pendientes; **no declarar F06 desbloqueada al completo ni fusionar borradores automáticamente**.

## 5. Borrador de decisión de cierre — NO FIRMADA

**Propuesta para el responsable del videojuego, no vigente:** aceptar F05 con estado CERRADA exclusivamente en el alcance **CORE_INTEGRADO del laboratorio F05-P05B**, con dos repeticiones automatizadas MSI, registro abierto de la incidencia global Unreal no atribuida a F05, sin proclamación de UE5 jugable. **Alternativa:** mantener F05 EN_CURSO hasta identificar la aserción si el responsable considera inaceptable el riesgo de motor en el siguiente corte. Es una decisión de tratamiento de excepción técnica, no una nueva decisión creativa ni permiso automático para fusionar.

**Estado a 19-11-2026:** **NO FIRMADA / F05 EN_CURSO / F06 parcialmente preparable pero sin aceptación de integración F05**. La reconciliación R0 vive en PR independiente #176, que también requiere CI/revisión y no debe confundirse con este expediente R1.

## 6. Trabajo posterior

R2: evaluar #91→#96→#97 por orden, orígenes espaciales reales y persistencia; R3: Sutherland, #95, asiento y consola UE5; R4: primera guardia F08 E2E en MSI. El motor de producción y su rendimiento deben validarse independientemente. Mantener referencias y resultados de 05-11 originales, sin reescribirlos para simular aceptación retroactiva.
