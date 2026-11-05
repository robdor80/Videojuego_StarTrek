# VOY-02 — Materiales y rendimiento
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

## Estado real de los materiales
La base VOY-01 aporta 49 imágenes de color utilizables, 102 materiales y UV0 en los 630 objetos OBJ. La colección modular blanca tiene geometría, sin texturas artísticas recuperadas. VOY-02 no ha reconstruido PBR, pintado materiales definitivos, modificado imágenes, remapeado UV, reducido resolución ni optimizado activos de producción. Workbench muestra colores de diagnóstico; sus renders no prueban acabado, iluminación o emisión.

La consolidación de los metadatos glTF identifica **101 OPAQUE y un BLEND (`Window`, alfa ~0,2), 102 doubleSided**. El estado glTF es una exportación de referencia, no una configuración recomendada para todos los materiales UE. `materiales_canales.csv` conserva por material los canales presentes y factores. No se presupone que una imagen de color proporcione normal, ORM o una emisión selectiva útil. Debe distinguirse color, máscara de emisión LCARS, normal y mapas lineales, sin derivar automáticamente PBR convincente de los albedos.

## Presupuesto de imágenes calculado

| Hipótesis, 49 imágenes | RGBA8 nivel base MiB | RGBA8 + mips ideales MiB |
| --- | --- | --- |
| Original | 1881.728 | 2508.971 |
| Lado máximo 4096 | 1363.941 | 1818.588 |
| Lado máximo 2048 | 407.707 | 543.609 |

Se usa width×height×4 bytes y factor ideal 4/3 de mipmaps. Los límites se simulan manteniendo relación de aspecto y redondeando píxeles, sin ampliar imágenes pequeñas. No se aplica padding potencia de dos, compresión GPU, residencia, streaming, formatos de canal o costes de mipmaps reales. **No es VRAM medida**. Los ficheros comprimidos pequeños pueden decodificar imágenes grandes; ejemplos: scn6.4 7536×5056, scn6.7/scn2.3 6546×5056 y scn4.1 10933×2917.

2K reduce mucho el presupuesto teórico, pero puede destruir legibilidad de LCARS en primer plano. 4K conserva mayor detalle a coste teórico superior. La selección debe ser por uso y densidad de texel, con comparación visual de lecturas cercanas/lejos; no un recorte global ya aprobado. `texturas_presupuesto.csv` permite revisar cada imagen y ambos escenarios. No se han cargado ni reescalado los píxeles para este cálculo.

![Presupuesto teórico](LAMINAS/L04_texturas_hipotesis.png)

## Geometría, slots y riesgos localizados
Leather2 agrupa 68.392 de 271.705 triángulos del puente (~25,2%). Algunos apoyabrazos tienen ~1500 triángulos. Antes de reducir todo, revisar esas concentraciones, repetición, slots, dobles caras y superficies transparentes. `materiales_triangulos.csv` contiene la distribución completa. El número de objetos o materiales no equivale al número real de draw calls de una escena UE.

VOY-01 registra en su GLB derivado 578 triángulos de área <1e−10, 11.919 de UV con área cero y 5368 duplicados locales a cuantización 1e−6. Se atribuyen a aquella validación y conversión concreta, no a un ensayo nuevo de producción. Repararlos exige preservar UV/sombreado y comprobar falsos bloqueos; no se ha limpiado silenciosamente el recurso. El contraste actual demuestra correspondencia de laboratorio con sus superficies ensayadas, no una topología de producción perfecta.

## Plan para Lumen y pruebas UE futuras
La documentación oficial de Lumen recomienda interiores con paredes, suelos y techos separados y revisar cobertura de Surface Cache; una habitación completa con muebles fusionada en una malla no es una preparación suficiente. En Voyager conviene separar por arquitectura y función conservando UV/materiales, revisar los modelos modulares de una sola malla y comprobar caras reversas, espesores y cobertura. Es una recomendación, no un resultado de Unreal ejecutado. [Epic: detalles técnicos de Lumen](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine).

Evitar tratar pequeñas superficies LCARS muy brillantes como única fuente de luz; contrastar emisión artística con luminarias controladas y revisar ruido/reflejos. No aumentar todos los materiales a doubleSided por defecto ni eliminar transparencia sin revisar su intención. [Epic: GI y reflejos de Lumen](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine).

Preparar una escena UE de laboratorio separada solo cuando se autorice esa fase: resolución interna/salida y escalabilidad fijas; comparar calidad de GI/reflejos, iluminación, Surface Cache, geometría y coste GPU/CPU; medir residencia de texturas y streaming con cámaras de uso real. Los objetivos de rendimiento de Epic para sus plataformas son presupuestos de referencia, no FPS prometidos para la RTX 4070 Laptop del MSI. [Epic: guía de rendimiento](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-performance-guide-for-unreal-engine). El streamer selecciona mips según punto de vista y memoria disponible; medir ese estado antes de fijar presupuesto. [Epic: texture streaming](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-streaming-overview-for-unreal-engine).

Grado C de preparación PBR/optimización; E de rendimiento real, Lumen y memoria UE. No se ha abierto un proyecto Unreal ni alterado su configuración. Evidencias locales: `materiales_rendimiento_revision.json`, los tres CSV de materiales/texturas y referencias VOY-01.
