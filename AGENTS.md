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
- **Limpieza obligatoria al finalizar cada tarea (autorización permanente del propietario):** Codex debe eliminar los artefactos temporales y laboratorios prescindibles que él mismo haya creado para esa tarea, una vez concluidas las pruebas, registradas las evidencias necesarias y verificada la ausencia de dependencias. No requiere una autorización adicional para esa limpieza acotada.
- **No eliminar laboratorios ni archivos preexistentes, de otras tareas, del usuario o de procedencia incierta sin autorización expresa.** La limpieza obligatoria no autoriza un borrado retroactivo general ni de recursos originales.

## 3. Protección de originales y excepciones

- Nunca sobrescribir modelos originales, archivos Blender base, texturas PBR, proyectos UE ni copias de seguridad para hacer una prueba. Utilizar copias aisladas.
- Las copias de seguridad deliberadas en HDD están permitidas; **no son lugares de desarrollo ni de ejecución de auditorías**.
- Si una instrucción pide generar evidencia documental definitiva dentro de un directorio del juego, aclarar su carácter permanente antes de publicarla. Los datos brutos temporales siguen en `laboratorios/`.
- Ante una duda sobre ubicación, dependencias o borrado, **detener esa operación y consultar** en lugar de inventar otra carpeta.

## 4. Limpieza obligatoria y criterio de finalización

- Antes de generar artefactos, identificar el directorio propio de la tarea y distinguirlo de cualquier contenido preexistente. Evitar duplicados y reutilizar únicamente salidas regenerables cuando sea seguro.
- Al concluir cada tarea, subfase o validación, registrar los comandos, resultados, versiones y evidencias mínimas necesarias en el informe o ubicación autorizada. Conservar solo los resultados definitivos aprobados; no guardar compilaciones, cachés, binarios, copias, renders de diagnóstico, logs masivos ni otros artefactos regenerables por rutina.
- Comprobar que los resultados aprobados funcionan sin el laboratorio y que ninguna revisión, prueba pendiente o proceso activo depende de los elementos a eliminar. Limpiar los artefactos propios prescindibles y, cuando quede vacío o sea completamente desechable, eliminar el subdirectorio completo de la tarea.
- Antes de borrar, comprobar rutas absolutas y su pertenencia al directorio autorizado de la tarea; no seguir enlaces simbólicos ni junctions hacia otros directorios. Prohibido usar borrados globales como `git clean -fdx` o eliminar indiscriminadamente `laboratorios/`. Preservar `laboratorios/README.md`, originales, recursos creativos, copias de seguridad y archivos de terceros.
- Si queda pendiente una aceptación visual, auditoría o reproducción no sustituible, conservar únicamente lo imprescindible, identificando ruta, tamaño, motivo y condición de eliminación; limpiar al resolverse si se trata de artefactos propios autorizados. Ante dudas, conservar y consultar.
- Medir, cuando el entorno lo permita, el tamaño antes y después de limpiar. El informe final debe indicar rutas limpiadas, espacio liberado, elementos retenidos y motivo, o la limitación que impidió medir o limpiar.
- **No dar por finalizada una tarea sin ejecutar esta limpieza o documentar explícitamente el impedimento justificado.** Si Codex no tiene acceso al equipo donde se generaron los archivos, indicar qué queda pendiente y proporcionar una instrucción de limpieza acotada y segura; no afirmar que se ha liberado espacio sin verificarlo.

Consulta también `laboratorios/README.md`.
