# Plan futuro propuesto — no ejecutado

## Viabilidad y alcance real

**Viable como recuperación de complejidad media/alta**, especialmente por disponer de OBJ separado y texturas sanas. La carga de ~272.000 triángulos no es por sí sola un bloqueo demostrado. El coste práctico dependerá de materiales, cantidad de componentes/secciones, transparencias/doble cara, sombras y colisiones; no se ofrecen FPS, draw calls reales ni memoria UE5 medida. Un solo objeto con 102 materiales tampoco equivale a una sola llamada de dibujo.

## Orden recomendado para una futura fase autorizada

1. **Copia trazable del OBJ con MTL y dependencias.** Separar sus 630 grupos en una escena nueva, clasificar por arquitectura, mobiliario, pantallas y mecanismos; preservar UV0/normales. Esta auditoría hizo esa separación solo en memoria para inspección y no entregó un máster restaurado.
2. **Escala y suelo primero.** Probar un maniquí/cápsula del proyecto y medir vanos completos, altura de asiento respecto a su plataforma, escalones y suelos. Contrastar escala OBJ/MAX sin normalizar a ciegas. Revisar coincidencias y normales por componente antes de cualquier limpieza global.
3. **Un recorrido piloto.** Acceso→una estación→retorno, con suelo y límites visibles. Mantener bloqueados destinos sin construir, siguiendo el criterio documentado en Sutherland. El kit modular puede aportar un tramo, pero necesita adaptador de cota/sección al puente.
4. **Organización de Static Meshes.** Mantener por separado suelos por nivel, tramos de muros/techo, carcasas de consolas y barandillas coherentes. Puertas/hojas, marcos, base/silla móvil y superficies de pantalla deben ser independientes. Agrupar remates pequeños estáticos por sector/material solo tras perfilar; no exportar cada tornillo como actor por defecto.
5. **Materiales.** Conservar imágenes BaseColor existentes y reconstruir respuesta PBR por familia. Emisión selectiva para LCARS y luminarias, sin convertir toda arquitectura a unlit. Revisar sRGB/color, mapas lineales y normales; añadir mapas nuevos solo cuando esa fase artística se autorice. Tratar cuero, metal y alfombra según referencias artísticas, no aplicar una rugosidad uniforme a todo.
6. **Colisión.** Primitivas/convexos específicos para suelos, escalones, mamparos con huecos, consolas y bases de sillas. Una caja que cubra un vano sería incorrecta. Las hojas móviles precisan barrido y retorno; probar cápsula completa, no solo rayos. La receta debe comprobarse con render y Chaos, como mostró la discrepancia de convexos en Sutherland.
7. **Interacción/NPC.** Primero una puerta y una consola; después agrupación de silla, postura y ocupación. Reutilizar conceptos de intención, permiso, espera y umbral del laboratorio Sutherland, con medidas propias. NavMesh o SmartLinks y permisos de puerta requieren implementación/pruebas, no están en el activo.
8. **Validación UE5 5.8.2 aislada.** Revisar importación/escala/materiales/normales/tangentes, espacios de paso, iluminación, frame time y memoria en MSI. Registrar versión exacta y opciones. Solo después ampliar al resto del puente e integrar; esta misión no abrió el proyecto ni hizo ese ensayo.

## Iluminación con Lumen

Recomendación teórica basada en [Lumen Technical Details, documentación UE 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine): separar paredes, suelos y techo en piezas razonables para cobertura de Surface Cache. Las mallas cóncavas que contienen una habitación y mobiliario completos no son una organización apropiada para esa cobertura. Comprobar superficies delgadas y caras posteriores; el material double-sided no demuestra un cerramiento volumétrico correcto. Para la ruta de software por campos de distancia, Epic recomienda paredes de al menos 10 cm para reducir fugas; no es una medida certificada de estas paredes ni una garantía universal. No se añadieron espesores.

El uso de Lumen no obliga a fabricar un UV de lightmap únicamente para iluminación dinámica. Si se opta por iluminación horneada, preparar canal independiente sin solapes. UV0 existente para LCARS debe preservarse. No se probó Surface Cache, hardware RT, campos de distancia ni exposición del proyecto.

## Facilidad de los trabajos

| Tipo | Trabajo previsto | Por qué |
|---|---|---|
| Ajustes limitados | Recuperar grupos OBJ, nombres/colecciones, pivotes, selección de pantallas | Fuente y superficies ya existen; el agrupado funcional requiere atención |
| Intervención artística | PBR, emisión, limpieza localizada de solapes/normales, UV afectadas, detalle de consola | Texturas existentes no equivalen a acabado final; defectos medidos |
| Reconstrucción/recuperación desde otra fuente | Suelo perdido en conversión MAX; mobiliario ausente del puente de colección; adaptador a pasillos | No compensa rehacer una conversión dañada cuando el OBJ conserva superficie |
| Evaluación todavía necesaria | Vanos completos, sentado/NPC, colisiones, rendimiento, fidelidad canónica | No se ejecutó el laboratorio dinámico ni comparación con planos canónicos |

No se instala software ni se usa MAX como bloqueo de toda la investigación: se conserva su estado E y se avanza con OBJ/GLB ya comprobados. Para colisiones exportadas, nombres y restricciones se consultarían en [FBX Static Mesh Pipeline de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine). El soporte general de GLB se describe en [glTF Support de Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/gltf-file-format-support-in-unreal-engine); soportar el formato no garantiza material idéntico ni colisión gameplay.

## Matriz de aprovechamiento

| Componente | Grado | Evidencia/condición |
|---|---|---|
| Imágenes embebidas del GLB detallado | A | 49/49 decodificadas; datos reutilizables, sin afirmar calidad final PBR |
| OBJ original + MTL vigente | B como fuente / C como puente final | 630 grupos recuperables, UV y mapas conservados; requiere saneado y preparación |
| Puente detallado exportado GLB | B como referencia / C para interacción | Una malla con 102 primitivas; materiales legibles; organización fusionada |
| Sillas y consolas OBJ separadas | B/C | Geometría real y piezas independientes; pivotes, agrupación, ergonomía y PBR pendientes |
| Carcasa del puente de colección | C | Muy simplificada y fusionada; sin mobiliario ni arte de estaciones |
| Sillas/LCARS ausentes de la colección | D: crear o tomar de otra fuente | No hay base suficiente en esta familia para esos elementos |
| Pasillos rectos/curvos y cruces | B | Secciones compatibles en muestras; falta ensamblaje, materiales y colisiones |
| Conductos Jefferies / mantenimiento | B | Existen módulos; dimensiones de conducto, no circulación humana de pie |
| MAX convertido: floorfront | D para esta conversión | Recuperación preferible desde OBJ |
| Resto de conversión MAX | C | Más separación que GLB, pero escala, suelo y materiales problemáticos |
| MAX binario original | E | Inventariado; no abierto en 3ds Max ni certificado |
| Transitabilidad, NPC, rendimiento UE5 | E | No se abrió Unreal; no hay prueba dinámica en esta misión |

La estimación no se convierte en un calendario de horas sin definir calidad visual, alcance de interactividad y plataforma objetivo. **Auditoría finalizada; toda actuación descrita aquí es una propuesta para otra fase.**

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
