# Análisis pausado a petición del usuario

El usuario solicitó detener el trabajo para apagar el ordenador. No continuar automáticamente.

## Alcance vigente
Solo análisis dimensional y ergonómico de las seis sillas correderas. No modificar Blender, recursos/configuración/código Unreal, posiciones, materiales ni mecanismos. No ejecutar operaciones Git.

Referencia: archivo Blender Hueco_Cerrado_01. La X amarilla indica acceso/retraída y la X roja trabajo/adelantada. Plataforma fija durante el recorrido; estudiar silla+pie móviles. El traslado global de plataforma+silla hacia la consola es una alternativa que debe medirse, no está ejecutado.

## Guardado
- mediciones_blender.json: 171 mallas visibles, seis estaciones con sus 16 piezas, coordenadas, envolventes y asignaciones.
- geometria_fuente_cm.npz: vértices y triángulos evaluados en centímetros, sin guardar la escena.
- integridad_ue_antes.json: hashes de 1823 archivos no regenerables del proyecto.
- quinn_ue_lectura.json y logs: intentos de lectura/exportación incompletos; no asumir éxito ni usar como validación de esqueleto.
- ESTADO_PAUSADO.json: estado y hashes de la fuente.
- Scripts nuevos en ../scripts/correderas01_*.py.

## Hallazgos preliminares, aún sin conclusión de diseño
Plataformas de aproximadamente 75 × 50 × 3 cm, pie de Ø13,2 cm centrado. Asiento lateral entre aproximadamente 70,6 y 77,5 cm de altura. La consola lateral debe identificarse en Plane.008_0/Cylinder.002_0/Plane.040_0 y sus pantallas. No confundir las consolas centrales Editable Mesh_Mat.* con las laterales.

El código y las pruebas guardadas confirman cápsula de Quinn de radio 35 cm y semialtura 90 cm. La silla del capitán usa transitoriamente radio 25 / semialtura 35 al sentarse. Las pruebas históricas incluyen huesos de una pose sentada del capitán, que no demuestra ergonomía lateral. STSlidingChair ya barre las 15 piezas, pero el ocupante sigue siendo bloqueante y no tiene sincronización integrada.

## Al retomar
Leer el encargo adjunto de esta conversación y ESTADO_PAUSADO.json. Verificar la fuente y los archivos ya generados antes de ejecutar scripts; no sobrescribir exportaciones existentes. Completar primero la lectura de proporciones de Quinn. El intento UE final terminó con error nativo durante exportación; inspeccionar el log antes de repetir. No hay posiciones ni recorridos óptimos aprobados, ni informe final. La investigación web inicial usó documentación oficial de Epic; completar referencias técnicas antes de entregar la arquitectura.

## Aviso para la reanudación
El hash del Blender actual difiere del registrado al medir. Los scripts de esta intervención no guardan archivos Blender. La diferencia no se investigó porque el usuario pidió detener el análisis; al retomar, comprobar el estado actual antes de reutilizar mediciones o proponer posiciones. No asumir que la fuente sigue siendo idéntica.
No se encontraron procesos Blender/Python/UnrealEditor-Cmd de los scripts correderas01 activos al detener el trabajo.
