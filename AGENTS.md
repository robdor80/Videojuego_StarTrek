# Reglas de trabajo para Codex — Videojuego Star Trek

Estas reglas se aplican a todas las tareas de Codex en este repositorio, además de las instrucciones particulares de cada tarea.

## 1. Pruebas, auditorías y experimentos: ubicación obligatoria

- Raíz única de trabajo del proyecto: `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek`.
- **Todo resultado temporal de pruebas, auditorías, mediciones, benchmarks, renders de diagnóstico, simulaciones, compilaciones experimentales, registros y scripts desechables** debe guardarse dentro de `laboratorios/<area>/<tarea>/`. Organizar por fase, sistema o clase de nave; usar un subdirectorio identificable por tarea si hace falta.
- Utilizar la carpeta `laboratorios/` existente. **No crear laboratorios permanentes ni nuevos proyectos o árboles paralelos** fuera del repositorio, incluidos `Documentos/ChatGPT/`, Escritorio, otras carpetas de Documentos u otros repositorios.
- Si una herramienta obliga a usar cachés o rutas temporales del sistema, no tratarlas como lugar de entrega ni dejar allí artefactos del proyecto. Avisar si no es posible redirigir o limpiar su salida de forma segura.
- `.gitignore` excluye `/laboratorios/**`, salvo `/laboratorios/README.md`. **No forzar su inclusión en Git, ni hacer commits o push de su contenido.**

## 2. Laboratorios aislados y eliminables

- Cada laboratorio debe funcionar como unidad **autocontenida y prescindible**. El código, los datos y los proyectos definitivos no podrán depender de scripts, rutas, binarios o archivos almacenados allí.
- No insertar referencias permanentes a `laboratorios/` ni a sus rutas absolutas en archivos definitivos, configuraciones, proyectos de Unreal, CMake, pruebas CI o documentación contractual.
- Si una prueba produce algo que deba conservarse, **trasladar solo el resultado aprobado** a la ubicación definitiva apropiada (por ejemplo, `juego/`, `sistemas/` o `desarrollo/`), con autorización cuando suponga ampliar el alcance. Verificar que funciona sin el laboratorio. No considerar permanente una salida por el mero hecho de haber sido generada.
- Al finalizar, indicar la ruta del laboratorio, qué se obtuvo y si existen dependencias pendientes. Una vez integrado o descartado, debe poder eliminarse **la carpeta completa** sin afectar al juego, al repositorio ni a otros experimentos.
- **No eliminar laboratorios ni archivos anteriores sin autorización expresa del usuario.** Esta norma no autoriza limpieza retroactiva, traslado o borrado de material existente.

## 3. Protección de originales y excepciones

- Nunca sobrescribir modelos originales, archivos Blender base, texturas PBR, proyectos UE ni copias de seguridad para hacer una prueba. Utilizar copias aisladas.
- Las copias de seguridad deliberadas en HDD están permitidas; **no son lugares de desarrollo ni de ejecución de auditorías**.
- Si una instrucción pide generar evidencia documental definitiva dentro de un directorio del juego, aclarar su carácter permanente antes de publicarla. Los datos brutos temporales siguen en `laboratorios/`.
- Ante una duda sobre ubicación, dependencias o borrado, **detener esa operación y consultar** en lugar de inventar otra carpeta.

Consulta también `laboratorios/README.md`.


## 4. Retención de resultados, espacio y cierre verificable

- En todas las pruebas de rendimiento, **extraer y conservar antes del cierre** métricas en CSV/JSON y resumen MD en una ruta definitiva versionable fuera de `laboratorios/`, indicando unidad, versiones, condiciones, variante, limitaciones y procedencia. Una exportación agregada de `.utrace` NO conserva la cronología ni todos sus canales; no borrar la captura hasta una decisión específica sobre esa pérdida.
- Antes de declarar cerrada una fase, consignar en el informe: ruta de laboratorio, tamaño y contenido, resultados trasladados, inventario de dependencias, si la carpeta es eliminable de extremo a extremo, y qué hace falta para autorizar su borrado. No acumular decenas de GB sin informar.
- Los intermedios de compilación (cabeceras `.pch`, objetos `.obj` SOLO cuando son de compilación, cachés, `Intermediate/`, `CMakeFiles/`) son regenerables, pero su eliminación exige no interferir con tareas ni procesos activos. No confundir objetos `.obj` de geometría 3D con los de compilación.
- Nunca eliminar por extensión, ni en bloque sin inspección, `.utrace`, `.blend`, `.blend1`, `.fbx`, `.glb`, `.uasset`, `.umap`, scripts no integrados, texturas originales o datos no versionados.

## 5. Exclusiones de limpieza durante HOST H06 (13/11/2026)

- **PROTECCIÓN ABSOLUTA: `laboratorios/host/h06/`** y su contenido, durante la ejecución de H06 (PR #142). Prohibido mover, modificar o borrar, también de forma indirecta mediante glob, enlaces o limpieza por patrón.
- **EXCLUIR `laboratorios/host/` completo**, otras tareas HOST activas, `laboratorios/f05/`, `laboratorios/F04/` y `C:\F04`, hasta revisar las dependencias y la actividad de Codex, CMake/CTest/UBT/Visual Studio.
- **No limpiar `laboratorios/valhalla/` ni `laboratorios/Enterprise_G/` mientras G0 de H06 esté pendiente**, porque H06 los inventarió como posibles proyectos Unreal reutilizables. Las métricas `.utrace` y los modelos 3D también quedan protegidos por separado.
- Una limpieza independiente debe comprobar primero que no atraviesa junctions/symlinks y que no afecta a recursos compartidos o procesos activos. Si aparece incertidumbre, aplazar **solo ese objetivo**, no el resto de la auditoría.
- Al cerrar H06, confirmar que los entregables, pruebas y resultados definitivos quedaron en GitHub, comprobar que ningún archivo del juego depende del laboratorio H06 y registrar la posibilidad real de eliminarlo. **No se borra H06 automáticamente al cerrar**.
