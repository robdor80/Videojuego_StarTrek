# USS Sutherland — comparación PBR

28/10/2026. Investigación de solo lectura con Blender 5.2.2 LTS. Destino: `juego/Clase Miranda/puente/blender/Miranda_Puente_Sutherland_Ergonomia_04.blend`.

## Fuente recomendada

**`Referencia_Visual02.blend`**, en:

`C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\TABULA RASA COPIA SEGURIDAD\01_TEXTURAS_PBR_SUTHERLAND\DERIVADOS_EXISTENTES\Blender_Integracion_Final\Referencia_Visual02.blend`

**Modificación: 23/10/2026, 18:28:05, Europe/Madrid (UTC+02).** Es la copia recuperada de la referencia Blender de VISUAL_02: conserva los mismos grafos de los 37 materiales usados de `Sutherland_PBR_Lab_v01.blend`, pero tiene **27/27 imágenes utilizadas empaquetadas**, sin bibliotecas Blender enlazadas. Es la fuente principal más completa y portable encontrada; esto no equivale a una aprobación artística por renderizado.

Se consultaron primero los índices e informes de TABULA RASA y la documentación ya localizada de VISUAL_02. Se acotaron ocho rutas candidatas —cinco contenidos distintos tras comparar hashes— y se abrieron en detalle **solo estas tres fuentes**, además del destino:

| Fuente | Modificación | Resultado |
|---|---|---|
| `assets/ships/starfleet/bridges/USS Suntherland/Sutherland_PBR_Lab_v01.blend` | 22/10/2026 20:09:19 UTC+02 | Mismas recetas; 22/27 imágenes empaquetadas y cinco rutas externas rotas, recuperables en la biblioteca conservada. |
| `Referencia_Visual02.blend`, ruta anterior | 23/10/2026 18:28:05 UTC+02 | **Recomendada:** 37 materiales usados, 27 imágenes empaquetadas y dependencias completas. |
| `Sutherland_Definitivo_Recuperado.blend`, misma carpeta que la recomendada | 25/10/2026 21:19:09 UTC+01 | 30 materiales usados, 19/19 imágenes empaquetadas; añade `PBR_Paneles_Prueba_Gris`. Fuente complementaria válida, aunque carezca de sillas laterales. |

La última no se elige automáticamente por ser más reciente: aporta la variante gris, mientras que VISUAL_02 conserva íntegra la biblioteca usada del laboratorio. La carpeta antigua `Documents/StarTrek_3D/Sutherland_PBR_Lab` ya no está en su ubicación original.

## Qué se puede trasladar

«Sí» significa recuperar el material y su asignación, conservando toda la geometría del destino. No significa sustituir mallas.

| Elemento | Material antiguo | Material actual | ¿Transferible? |
|---|---|---|---|
| Paredes y paneles | `PBR_Mamparos_Composite_Oscuro`, `PBR_Paneles_Composite_Claro/Hueso` | `grey`, `cream`, `ceiling` | **Sí, por caras.** Coinciden topología y UV en ejemplos como `Plane_0`, `Plane.005_0`, `Plane.009_0` y `ceiling_0`. |
| Suelo y plataforma | `PBR_Moqueta_Puente`, `PBR_Moqueta_Capitan`, `PBR_Puente_Plataforma_Titanio` | `floor`, `grey` | **Sí.** `Circle_0` conserva topología/UV, pero antes repartía dos moquetas y ahora usa un solo `floor`: recuperar los índices por cara. |
| Consolas | `PBR_Paneles_Composite_Claro`, materiales LCARS y `Luz_Azul_Suave_Consola` | `grey`, `BLUE`, `lcardtype`, `turbolcar` | **Adaptación.** Ocho piezas centrales actuales agrupan pares antiguos; `Editable Mesh_Mat.003_0` tiene UV distintas. Preservar la nueva iluminación azul. |
| Metales y techo | `PBR_Puente_Barandillas_AceroCepillado`, `PBR_Techo_Faldones_Gunmetal`, `PBR_Techo_Acero_Cepillado_Claro` | `grey`, `ceiling` | **Sí, por caras.** `Plane.028_0` y `Plane.020_0` conservan topología y UV. El techo tenía varios acabados, no uno único. |
| Luces | `PBR_Luz_Sutherland_Fria`, `Luz_Azul_Suave_Consola` | `light`, `light.001`, `BLUE` | **Sí para el grafo; adaptación de selección** para las superficies azules nuevas. Conservar la mezcla Light Path/Transparent/Emission. |
| Puertas | `PBR_Puertas_Burdeos_ConTexto` | `door` | **Sí.** Las cuatro mallas fuente `Plane.001_0/017_0/018_0/019_0` conservan topología y UV. Solo material, sin alterar dimensiones. |
| Variante gris posterior | `PBR_Paneles_Prueba_Gris` | `grey` o `cream` según objeto | **Adaptación opcional**, desde el archivo final recuperado. Requiere decidir qué caras deben adoptar ese acabado. |

## Recetas propias y procedencia de las imágenes

Los acabados personalizados están en los **nodos, tintes, mezclas, parámetros y asignaciones**. Ejemplos comprobados: panel claro metallic=0/roughness=0,8; moquetas con Mapping UV 6×6 y roughness=0,9; barandilla metálica metallic=1/roughness=0,35; emisión azul RGB lineal ≈(0,2705; 0,4125; 1), fuerza 1,2.

`Plastic010`, `Fabric023`, `Metal011/027/059A`, etc., son imágenes de las colecciones descargadas conservadas, no texturas propias por llevar un material `PBR_`. Los atlas/diagramas `Image_*` y LCARS son recursos heredados del puente: **no se ha identificado aquí un diagrama raster adicional de autoría propia confirmada**. No se amplió la búsqueda para inventar esa atribución.

Las recetas se conservan dentro del `.blend`. En la referencia recomendada, también están incrustadas todas sus imágenes utilizadas. `Marcos_Ascensor_Negro` y `Luz_Azul_Suave_Consola` no requieren imágenes; otros grafos sin imágenes incluyen `light`, `Plane.037_0` y `space`. No tienen grupos de nodos externos enlazados.

Varios materiales usan color de textura con metallic/roughness constantes: **no están conectados automáticamente todos los canales Normal/Displacement disponibles en la biblioteca**. No se proponen mapas ni sustitutos nuevos.

## Dependencias y precauciones para una transferencia futura

- En `PBR_Lab_v01` faltan en sus rutas guardadas dos colores del techo (`Metal027_…_Color.jpg`, `Metal011_…_Color.jpg.001`) y tres mapas Leather023 de sillas. Se localizaron archivos reales correspondientes en `TABULA RASA COPIA SEGURIDAD/01_TEXTURAS_PBR_SUTHERLAND/ORIGINALES_DESCARGADOS/Sutherland_PBR_Lab/textures/fabric23/` y en el `PBRSource` conservado. **No se repararon rutas.** La fuente recomendada ya los tiene empaquetados y evita esta dependencia.
- No reemplazar globalmente `grey`, `cream` o `BLUE`: un nombre actual puede reunir superficies que antes tenían acabados diferentes. Por ejemplo, `Plane.008_0` y `Editable Mesh_Mat.003_0` ahora usan `BLUE`, donde la fuente asignaba composite; copiar por nombre borraría esa intención actual.
- Para paredes, suelo, techo y metales compatibles, conviene un **script de correspondencias objeto + topología + caras/materiales**, añadiendo únicamente los materiales. Para las consolas agrupadas, resolver primero la correspondencia de mitades/islas y la excepción UV de `.003_0`; no copiar UV ni geometría antigua a ciegas.
- Las UV iguales permiten conservar el mapa actual; aun así, los cambios dimensionales pueden variar la densidad aparente del patrón. Los grafos Light Path deben mantenerse completos en Blender. No se ha comprobado su aspecto mediante render, por el alcance autorizado.
- Las sillas quedan totalmente fuera de una eventual selección de transferencia. Su ausencia en una fuente no la invalida como biblioteca de materiales.

**Conclusión:** hay material suficiente y con dependencias completas para autorizar posteriormente una transferencia controlada desde `Referencia_Visual02.blend`, con la variante gris del archivo final como opción. No conviene una asignación masiva por nombre ni trasladar geometría antigua.

No se aplicó ningún material, se guardó ningún `.blend`, se renderizó ni se abrió Unreal. Los ocho candidatos y `Ergonomia_04` conservaron sus SHA-256. Evidencia técnica acotada: `datos/pbr_comparacion_resumen.json`; script de inspección: `scripts/comparar_pbr_solo_lectura.py`. Sin commit, push ni PR. **Trabajo detenido tras este análisis.**
