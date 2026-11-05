# VOY-04 — Hoja de ruta y aceptación

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Decisiones que permite tomar VOY-04

Conservar la arquitectura y la consola es una alternativa viable para seguir investigando el piloto. El problema no exige escalar el personaje o mover todo el puente. La silla necesita altura adaptable y una solución mecánica de acceso. Puede conservar la mayor parte del conjunto superior original.

La aceptación propuesta es **COMPLETADA CON RESERVAS** del laboratorio documental y cinemático. No es aprobación del activo de producción. Las reservas tienen testigos y medidas; no se retocaron fuera de Blender para parecer resueltas.

## Trabajo pendiente priorizado

1. Ajustar apoyo dorsal y profundidad útil: aún quedan 58–76 mm. Probar acercar/reconstruir localmente el soporte o añadir apoyo coherente, comprobando otra vez todas las poses y capas.
2. Revisar cabeza y lectura en 1,90 m (mirada descendente estimada 48,2°), con un rig que tenga ojos/cuello y la tarea visual real. Evitar mover la consola sin evidencia adicional.
3. Diseñar casquillo, anclajes, topes, guía y carro con una relación mecánica creíble. El prototipo ocupa un volumen comprobado, pero no transmite cargas ni certifica contacto/desgaste.
4. Sustituir la traslación lateral por marcha articulada con apoyos alternados, giro cuando proceda, equilibrio y contacto. Repetir con ropa y rig real. Conectar la aproximación a los recorridos del puente.
5. Ejecutar comprobación continua o suficientemente conservadora de movimientos, incluidos contactos y sólidos cerrados reconstruidos donde sea necesario. Los 601 estados por altura no eliminan toda incertidumbre entre muestras.
6. Evaluar las cuatro sillas restantes con sus propias posturas/espacios; mantener grado E hasta esa prueba.
7. Solo en una fase autorizada posterior: importación y verificación en Unreal, colisiones, retarget, reservas/ocupación, persistencia de NPC e interfaces.

## Revisión humana sugerida

Abrir `VOY04_Laboratorio.blend`, elegir `04_PROTO_1.75`, revisar los marcadores 1/31/61/91/121/151/211/241/301 y después las otras tallas. Comparar con `03_ORIGINAL_1.xx`. La escena 01 conserva toda la referencia y 02 muestra los pivotes. Abrir `VOY04_Fallos_y_Comparativa.blend` para los fallos rechazados. Revisar las capturas E y la lámina antes/después sin confundir sus cortes visuales con modificaciones de arquitectura.

La aceptación del informe puede conservar esas reservas; una aceptación de ergonomía definitiva requiere resolverlas. No se inicia VOY-05 ni integración Unreal al terminar este trabajo.
