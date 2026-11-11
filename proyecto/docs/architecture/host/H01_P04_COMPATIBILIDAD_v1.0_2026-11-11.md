# H01-P04 — Compatibilidad Core, versiones y no duplicación v1.0

Fecha 2026-11-11. Estado: DISEÑO, sin CMake/CTest nuevo ejecutado. Fuentes: CMakeLists y cabeceras reales de F02/F03/F04/F05/F11.

## Pines CoreRPG comprobados

| Corte | Archivo/entrada | SHA Core | Uso |
|---|---|---|---|
| F02 | desarrollo/integration/f02/CMakeLists.txt | 4f282863737bcd8f5add401202a9e1064c133672 | ABI e hilo, laboratorio |
| F03 | desarrollo/integration/f03/core-revision.txt | 9c53a33787de13d91eb2abe4da07033ee0fa1dc1 | Conocimiento/tiempo |
| F04 estable | desarrollo/integration/f04/core-revision.txt | c147d81ed069da2e09149613ab02cbc3ebe95a4a | F04 sin historia extendida |
| F04 history | desarrollo/integration/f04/core-history-revision.txt | 89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98 | Historial alternativo |
| F05/F11 | desarrollo/integration/f05/core-revision.txt | 76a7b7b485616d8c4994f384a90f123bf333591d | **Candidato HOST H05** |

No cambiar, unificar ni actualizar los pins históricos. Elegir candidato específico y probarlo con manifiesto exacto al llegar H05, pues F11 seguirá evolucionando.

## Grafo real de build

- F05/CMakeLists.txt activa F05_ENABLE_ORDERS y monta F04 como subdirectorio; F04 usa una única F04Session.
- F04/CMakeLists.txt fuerza F04_ENABLE_HISTORY al habilitar F05, y usa pin F05. F11_ENABLE_PROMOTIONS solo es válido con F05 activo. El configure exige HEAD Core igual al SHA esperado y Core sin cambios rastreados.
- F11/CMakeLists.txt añade F05; crea TrekF11TrialHost SHARED solo para pruebas con F11_NATIVE_TEST_HOST. Este ejecutable de ensayo NO debe ser dependencia del HOST producto.
- f11_host/CMakeLists.txt crea TrekF11HostReader STATIC y enlaza con TrekF04Bridge de producto sin issuer de ensayo.
- F05.ai_provider define lenguaje opcional y no presupone servicios online.

H05 seleccionará UNA biblioteca TrekF04Bridge, UNA CoreRPG y UNA sesión; ni un F02Session ni un F03Session paralelo. Reutilizar contratos, no clonar fuentes. Inspeccionar símbolos exportados, librerías, defines y SHA antes de proclamar producto.

## Persistencia: distinguir dos vías

La API f04_save/f04_load es monolítica. Tras migración a historial Core, f04_bridge.h exige directorio de generaciones y f04_history_open/consolidate/publish; operaciones de guardar historia completa por vía monolítica pueden dar F04_SAVE. f04_history_export_active produce diagnóstico parcial, NO un guardado completo para f04_load. H04 elegirá adaptador por versión de esquema y verificará publicación, crash/recovery y roundtrip entre procesos; no inventar core_save_atomic.

## Protocolo para adoptar una versión nueva

1. Registrar SHA Star Trek/Core, flags, compiler, ABI, save schema y dependencias.
2. Proponer nuevo manifiesto de compatibilidad; no sobrescribir pins históricos.
3. Compilar en laboratorios/host/<fase>/<tarea>/; no usar laboratorios como dependencia final.
4. Ejecutar CTest Core/F04/F05/F11 aplicables y nuevos ensayos HOST de hilos, scope, revisión, idempotencia, persistencia, negativos y legado.
5. Verificar que el producto no enlaza TrekF11TrialHost ni define F11_NATIVE_TEST_HOST.
6. Publicar resultados exactos PASS/FAIL/SKIP y commit probado; marcar UE5_JUGABLE solo con .uproject principal real y NullRHI/D3D12 efectivos.
7. Migrar con backup verificable; aceptar/fusionar nuevo corte solo bajo autorización del usuario.

La identidad narrativa Enterprise NCC-1701-D no transforma automáticamente F04_VALHALLA_FLAGSHIP ni modifica el catálogo de F04.

## Dependencias de integración

H02: sesión/owner/hilo. H03: binding jugador-personaje. H04: IO, procedencia, historia y recuperación. H05: build F04/F05 y primer ciclo nativo. H06: .uproject y ejecución real. H07: lectura F11 y pasarela **no emisora** cuando F11 publique su API productiva.
