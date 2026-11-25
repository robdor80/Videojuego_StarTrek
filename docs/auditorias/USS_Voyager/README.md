# Auditoría 3D — USS Voyager

Fecha de diagnóstico: **21/10/2026**, Europe/Madrid. Estado: **AUDITORÍA_DOCUMENTADA / RECUPERACIÓN_NO_INICIADA / UE5_NO_PROBADO**. Publicación exclusivamente documental para revisión en una PR Draft, sin integración ni merge.

## Conclusiones principales

- Hay dos familias distintas: colección modular con un puente esquemático y un puente detallado OBJ/MAX.
- El OBJ original permite recuperar **630 objetos separados, 271.705 triángulos y UV0 en los 630**. Se propone como base junto a su MTL vigente y dependencias; el GLB texturizado sirve como patrón de aspecto.
- La colección tiene ocho materiales constantes y **ninguna imagen**. El puente GLB detallado incluye **49 imágenes embebidas decodificables**, aunque carece de mapas PBR completos y emisión.
- La conversión MAX presenta suelos deteriorados, enlaces de material incompletos y diferencias de escala. La separación por objetos no la convierte en la mejor fuente.
- Los pasillos tienen potencial modular; no se demostró ensamblaje completo, transitabilidad con cápsula, ergonomía ni funcionamiento en Unreal.

## Informes completos

1. [Resumen ejecutivo](01_RESUMEN_EJECUTIVO.md)
2. [Inventario de modelos y dependencias](02_INVENTARIO.md)
3. [Geometría, escala y defectos](03_GEOMETRIA.md)
4. [Materiales, texturas y UV](04_MATERIALES_TEXTURAS.md)
5. [Puertas, sillas, consolas, circulación y NPC](05_INTERACTIVIDAD.md)
6. [Pasillos y módulos adicionales](06_MODULOS_ADICIONALES.md)
7. [Comparación y base recomendada](07_COMPARATIVA_VERSIONES.md)
8. [Plan futuro para Blender y Unreal 5.8.2](08_PLAN_FUTURO.md)
9. [Método, fuentes y limitaciones](09_METODO_FUENTES_LIMITACIONES.md)

## Inventarios y evidencia numérica

- [Índice de datos](DATOS/README.md): inventario con hashes, componentes, hallazgos, grados A–E, mapas/UV y medidas de pasillos.
- [Hallazgos con gravedad, prueba, consecuencia y recomendación](DATOS/hallazgos.csv).
- [Resumen de variantes](DATOS/resumen_modelos.json) y [matriz de aprovechamiento](DATOS/aprovechamiento.csv).
- [Catálogo de las 55 capturas locales](CAPTURAS/README.md). **Imágenes publicadas: 0; imágenes conservadas en el MSI: 55.**

## Publicacion y limites

Se publica la documentación completa y una selección de diagnósticos textuales. No se incluyen modelos 3D, texturas originales, píxeles de capturas, miniaturas, scripts con rutas de máquina, logs, copias temporales, credenciales ni datos de otros proyectos. No se han reducido las pruebas ni los informes originales para preparar esta edición.

La colección declara internamente CC-BY-4.0 y autor scrimshawsean, pero la consulta pública a Sketchfab devolvió 403 y no permitió confirmar el permiso de publicación de las capturas. No se ha verificado una licencia aplicable a la familia detallada OBJ/MAX. Por instrucción del usuario, se retienen **todas las capturas solo en local**, incluidas las láminas que muestran imágenes originales. Esta retención es una limitación de publicación, no una cancelación de la auditoría ni una afirmación de que las imágenes estén prohibidas. No hay imágenes publicadas a las que aplicar optimización de tamaño.

La edición pública omite coordenadas de triángulos duplicados y descriptores glTF crudos que no son necesarios para leer el diagnóstico. Conserva los conteos, áreas, envolventes, referencias de material, resultados de prueba y umbrales. Las copias completas, scripts reproducibles y logs siguen en la carpeta local `Voyager_Puente_2026-10-21`. Las fuentes de los laboratorios Sutherland se citan como evidencia previa; sus pruebas no se han repetido ni se transfieren automáticamente a Voyager.

## Alias de origen

Los alias identifican fuentes locales; **no son carpetas ni enlaces de descarga de este repositorio**. Las rutas exactas permanecen en el inventario privado del MSI.

| Alias | Significado |
|---|---|
| `BIBLIOTECA_3D` | Biblioteca histórica de modelos Star Trek, colección de pasillos |
| `FUENTE_OBJ` | OBJ del puente detallado, MTL y dependencias |
| `FUENTE_MAX` | MAX/MC6 y BLEND de conversión, con imágenes asociadas |
| `RECUPERACION_VOYAGER` | Documentación local previa de recuperación |
| `AUDITORIA_LOCAL` | Informes, datos completos, scripts y capturas de esta auditoría |
| `LABORATORIOS_3D` | Informes locales previos de laboratorios Sutherland |
| `CATALOGO_HISTORICO` | Metadatos de la biblioteca que permitieron localizar fuentes |
| `REPOSITORIO` | Rutas relativas del repositorio de diseño Star Trek |

## Qué queda por comprobar

Licencias para publicar imágenes; equivalencia completa MAX↔OBJ; limpieza localizada de superficies/normales/UV; calibración humana y vanos completos; ensamblaje de módulos; postura sentada y NPC; colisiones y recorrido real; Lumen, rendimiento e importación UE5 5.8.2. El MAX binario no se abrió con 3ds Max. No se inicia restauración con esta publicación.

## Integridad y trazabilidad

La auditoría inicial releyó **230/230 entradas sin cambios de SHA-256, tamaño y mtime_ns**; no fue un snapshot de todo el ordenador. El inventario público omite las entradas de modelos Sutherland ajenos, conservando las de Voyager. Los ocho informes, el anexo metodológico y las 55 capturas locales permanecen en el MSI; esta edición adapta navegación y privacidad.
