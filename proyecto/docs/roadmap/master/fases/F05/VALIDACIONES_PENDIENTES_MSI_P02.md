# F05-P02 — Validaciones pendientes del MSI

**Todas pendientes.** Cloud no dispone de MSI, MSVC local ni Unreal Engine 5.8.2.
La CI Windows, aun pasando, no sustituye estas comprobaciones del propietario.
No comenzar F06 hasta superar todas las pruebas obligatorias acumuladas F05.
Este archivo no declara F05 finalizada ni autoriza P03/P04/P05.

## Deuda P01 conservada

1. Compilación MSVC y carga de DLL en el MSI.
2. Compilación y carga con Unreal Engine 5.8.2.
3. `F05.P01.LifecycleAndRecovery`.
4. `F05.P01.Negatives`.
5. `F05.P01.WorldAndActorIndependence`.
6. Repetición de las pruebas UE5 en un entorno limpio.

Se mantiene también [el registro P01](VALIDACIONES_PENDIENTES_MSI.md).
Ninguna de estas seis validaciones se marca superada por desarrollar P02.

## P02 adicional

- Compilar ABI aditiva con MSVC y cargar DLL comprobando exportaciones P02.
- Compilar el harness aislado con UBT/UHT de **UE 5.8.2**, cargar el módulo y
  ejecutar `F05.P02.DelegationRevocationRecovery`: mandato real, orden aceptada,
  revocación, rechazo antes del efecto, recuperación exacta y repetición inocua.
- `F05.P02.ModesAndLimits`: propuesta sin efectos, prohibición de autoaprobación,
  aprobación del capitán, ejecución Core y rechazo explícito de subdelegación.
- `F05.P02.ExpiryAndChainOfCommand`: caducidad y revocación del nombramiento de
  origen; la sucesión F04 no rescata una orden fijada a autoridad revocada.
- Ejecutar de nuevo los tres tests P01 junto con los tres P02.
- Repetir compilación/carga y los seis tests en un directorio limpio nuevo;
  conservar versiones, logs y JSON de Automation, sin reutilizar DLL anteriores.
- Validar carga del módulo con el RHI real del MSI. El harness automatizado usa
  `NullRHI` y no acredita comportamiento gráfico ni una consola jugable.

No se modifica ningún proyecto artístico existente. El harness definitivo es
solo una plantilla de código y `.uproject` aislado, sin contenido artístico.

## Comandos reproducibles PowerShell

Partir de la rama P02 publicada y un checkout Core separado en
`76a7b7b485616d8c4994f384a90f123bf333591d`. `$Salida` debe ser un directorio
nuevo dentro del laboratorio P02 autorizado por el propietario; el script
rechaza destinos ajenos o preexistentes no identificados. No borrar archivos
para conseguir un entorno limpio: elegir otro directorio de salida.

```powershell
# Desde la raíz del repositorio. Definir $CoreSource y $Salida explícitamente.
pwsh -File desarrollo/integration/f05/run_f05.ps1 -Stage Native -CoreSource $CoreSource -BuildRoot $Salida
pwsh -File desarrollo/integration/f05/run_f05.ps1 -Stage Stage -CoreSource $CoreSource -BuildRoot $Salida
pwsh -File desarrollo/integration/f05/run_f05.ps1 -Stage Unreal -CoreSource $CoreSource -BuildRoot $Salida -EngineRoot 'C:/Program Files/Epic Games/UE_5.8'
pwsh -File desarrollo/integration/f05/run_f05.ps1 -Stage TestUnreal -Suite All -CoreSource $CoreSource -BuildRoot $Salida -EngineRoot 'C:/Program Files/Epic Games/UE_5.8'
# Suite P01 o P02 ejecuta exactamente sus tres tests; All exige los seis.
```

El script verifica la versión exacta de Unreal y el SHA Core. Conservar logs,
XML nativo y `index.json` de Automation; no basta el código de salida del Editor.
Las fuentes y la recuperación nativa sí se prueban en Cloud; UBT/UHT, DLL local,
Automation, RHI y repetición limpia solo se acreditarán después de ejecutarse.
