# F05-P04 — continuación obligatoria en MSI

**PENDIENTE / NO EJECUTADA.** MSI apagado durante esta entrega Cloud.
La compilación de CI Windows no equivale a ejecución MSI, UBT/UHT o Unreal.
F05 continúa abierta y F06 bloqueada hasta todas las validaciones obligatorias.
P01/P02/P03 conservan íntegros sus pendientes en
[REGISTRO_VALIDACIONES_MSI.md](REGISTRO_VALIDACIONES_MSI.md).

Prerrequisitos: checkout de la rama P04 al SHA de entrega, Core limpio en
`76a7b7b485616d8c4994f384a90f123bf333591d`, MSVC/SDK compatibles y **UE 5.8.2**
real. Usar directorios nuevos de la tarea, sin reutilizar DLL ni laboratorios
previos. No abrir ni editar proyectos artísticos. No configurar servicios de pago.

Desde la raíz del repositorio, seleccionar rutas del operador:

```powershell
$CoreSource = '<checkout Core fijado>'
$Output = Join-Path (Get-Location) 'laboratorios/f05/p04/msi-run-01'
./desarrollo/integration/f05/run_f05.ps1 -Stage All -Suite All -CoreSource $CoreSource -BuildRoot $Output -EngineRoot '<UE 5.8.2>'

# Selección individual aditiva, tres tests P04:
./desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite P04 -CoreSource $CoreSource -BuildRoot $Output -EngineRoot '<UE 5.8.2>'
# Repetición con el RHI real del MSI:
./desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite All -RealRHI -CoreSource $CoreSource -BuildRoot $Output -EngineRoot '<UE 5.8.2>'
# Repetir All en otro directorio nuevo: msi-run-02.
```

El runner admite P01/P02/P03/P04/All, exige 3 tests por selección o **12** en All,
y conserva XML/JUnit nativo, logs y reporte Automation. Si falta algún test,
`notRun>0`, fallo o versión incorrecta, no hay PASS. Debe verificarse:

- [ ] MSVC/DLL: ABI y exports `f05_ai_begin/finish/view/apply`, SHA Core, dependencia de la DLL correcta y carga sin símbolos faltantes.
- [ ] UBT/UHT: compilar y cargar el módulo aislado con UE **5.8.2**, `ready=1`.
- [ ] `F05.P04.AIProposalValidation`: JSON corrupto rechazado sin orden; propuesta válida sin efecto; entrega explícita a P03 genera orden P01 pendiente, no ejecución supuesta.
- [ ] `F05.P04.StaleAuthorityAndFallback`: cambio médico de autoridad durante respuesta invalida contexto; timeout simulado deja P03 operativo y produce solo el resultado Core auténtico.
- [ ] `F05.P04.OffscreenRecoveryAndSafety`: destruir Actor/UWorld, tramitar fuera de escena, guardar/cargar y repetir respuesta/aceptación sin modificar el resultado ni duplicar efectos.
- [ ] Las **nueve automatizaciones anteriores** P01/P02/P03 completas, sin modificaciones ni omisiones.
- [ ] Las **12** juntas, y repetición integral en directorio nuevo/limpio.
- [ ] Carga y automatización con **RHI real**. NullRHI no acredita gráficos/interfaz jugable.
- [ ] Recuperación de partida con petición externa pendiente, propuesta validada y decisión ya aplicada; ejecutar además suite nativa P04 y sus pruebas entre procesos/history.
- [ ] Fallback reproducible sin proveedor, timeout/red/cuota/JSON malicioso usando el simulador nativo; ninguna conexión real es necesaria.

Registrar fecha UTC, equipo, Windows, UE/CL exactos, compilador/SDK, ambos SHAs,
comandos, recuentos por suite, `index.json`, XML/JUnit, logs y SHA256 de evidencia.
No guardar prompts, credenciales, respuestas brutas ni datos privados de campaña.
Publicar evidencia permanente en un commit posterior y actualizar el registro
solo para lo realmente ejecutado. No fusionar esta entrega ni iniciar P05/F06.
