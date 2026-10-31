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
