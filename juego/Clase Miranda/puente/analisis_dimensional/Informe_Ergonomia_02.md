# MIRANDA-01 — Puertas: Ergonomía 02

Resultado guardado en `../blender/Miranda_Puente_Sutherland_Ergonomia_02.blend`. Fuente: `Miranda_Puente_Sutherland_Ergonomia_01.blend`. Blender 5.2.2 LTS. Fecha: 27/10/2026.

## Antes / después

Todas las medidas están en centímetros y coordenadas globales. Altura libre = suelo local hasta la cara inferior del dintel en el centro del paso, con las hojas cerradas excluidas del sondeo. Las hojas permanecen cerradas; no se ha creado animación.

| Puerta / ubicación mundial | Suelo Z | Paso antes → después | Hoja derecha antes → después | Hoja izquierda antes → después | Ancho útil antes → después |
|---|---:|---:|---:|---:|---:|
| D1_referencia_turbo: X=-565,86, Y=-827,38 | 0,00 | 300,14 → 300,14 | 303,08 → 303,08 | 303,08 → 303,08 | 143,75 → 143,75 |
| D2_opuesta_Yneg: X=565,86, Y=-827,38 | 0,00 | 388,53 → 300,00 | 391,48 → 302,95 | 391,48 → 302,95 | 143,75 → 143,75 |
| D3_Xpos_Ypos: X=634,92, Y=87,21 | 60,00 | 386,94 → 300,00 | 391,48 → 303,49 | 391,48 → 304,50 | 163,64 → 163,64 |
| D4_Xneg_Ypos: X=-634,92, Y=87,21 | 60,00 | 386,94 → 300,00 | 391,48 → 303,49 | 391,48 → 304,50 | 163,64 → 163,64 |

La altura de hoja incluye la parte que ya quedaba por debajo del suelo; por eso supera la altura libre. Las tres puertas nuevas terminan a 300,588 cm sobre su suelo y solapan aproximadamente 0,588 cm bajo el revestimiento. Los extremos inferiores no se han desplazado.

## Objetos y diferencias

- **D1, referencia del turbo (X negativo, Y negativo):** partes X negativas de `Plane.018_0`, `Plane.019_0` y `Plane.004_0`, íntegramente conservadas. Materiales `door` en hojas; ranuras `cream` y `captainschair` en el marco, con sus asignaciones originales. El marco interior `Plane.039_0` conserva el dintel alto anterior: no se ha modificado la cabina ni la puerta de referencia.
- **D2, opuesta (X positivo, Y negativo):** se modifican solo las partes X positivas de `Plane.018_0`, `Plane.019_0` y `Plane.004_0`. Hueco inclinado unos 10° en planta. Paredes adyacentes `Plane.011_0` y `Plane.022_0`, sin cambios. No tiene habitación construida detrás.
- **D3 y D4 (Y positivo):** hojas de las partes X positiva/negativa de `Plane.001_0` y `Plane.017_0`; marco `Plane.013_0`. Materiales `door` y `grey`. Suelo elevado a Z=60 cm, hueco más ancho, perfil y espesor propios conservados. Paredes adyacentes `Plane.009_0`, `Plane.010_0`, `Plane.014_0` y techo `ceiling_0`, sin cambios. No se han creado habitaciones.

Solo cambian seis objetos de malla compartidos. Se bajan los vértices superiores de las hojas y todo el contorno superior de los tres huecos; los vértices de coronación y los inferiores permanecen fijos. Los paños frontales existentes se alargan hacia abajo con su propia conectividad. No se añaden caras, objetos, materiales ni interiores; no se aplica escala global.

## Verificaciones

- Copia reabierta y verificada: 345 objetos; 339 objetos completos sin cambios y seis mallas con cambios limitados a los vértices registrados.
- Referencia D1 sin cambios en sus vértices, UV o asignaciones. Los originales Base, Analisis y Ergonomia_01 conservan sus SHA-256.
- Transformaciones, jerarquías, conectividad, índices de materiales, UV y referencias de imágenes conservados. Consistencia de los materiales verificada al reabrir.
- Anchuras, extremos inferiores y coronaciones conservados dentro de la precisión numérica de Blender; variaciones de anchura inferiores a 0,001 cm.
- Consolas y silla del capitán: conservación íntegra respecto a Ergonomia_01, comprobada junto con todos los objetos no relacionados.
- 2.911 rayos por puerta sobre el revestimiento superior sin huecos detectados. Coincidencias de vértices comprobadas; sin nuevas aperturas de costuras, triángulos degenerados o caras invertidas.

## Advertencias y límite de la validación

- La referencia tiene paso central **300,135 cm** sobre el suelo del puente y se deja intacta. El suelo de la cabina está aproximadamente 0,10 cm más alto; desde ese lado su paso es unos 300,035 cm.
- Los **300 cm corresponden al centro del dintel**. Se conservan los biseles de cada marco: sus arranques junto a las jambas quedan a 287,23 cm en D2 y 285,46 cm en D3/D4. La referencia conserva 287,36 cm. No existe un rectángulo de 300 cm de alto que abarque toda la anchura entre jambas.
- Las UV no se han reproyectado: las superficies acortadas o extendidas pueden mostrar compresión o estiramiento de textura, como consecuencia de conservar sus coordenadas originales.
- El muestreo del revestimiento cubre el 95% central de la anchura, desde 3 cm sobre el nuevo dintel hasta 1 cm bajo la coronación. No certifica estanqueidad volumétrica, animaciones o colisiones del motor.
- Validación visual final pendiente del usuario en Blender. No se han modificado Unreal, Valhalla ni otros modelos. Sin commit, push, PR o inclusión forzada de archivos .blend en Git.

## Evidencias y reproducción

- `datos/ergonomia02_inspeccion.json`: inventario original, geometría mundial, UV, materiales y hashes.
- `datos/ergonomia02_resultados.json`: medidas antes/después, vértices editados, pruebas de cobertura y hashes de la copia.
- `datos/ergonomia02_verificacion_final.json`: comprobaciones tras reabrir el archivo.
- `scripts/ergonomia02_inspeccion.py`, `scripts/ergonomia02_aplicar_verificar.py`, `scripts/ergonomia02_verificacion_final.py`: scripts conservados dentro de analisis_dimensional. El script de edición se niega a sobrescribir un Ergonomia_02 existente.

Trabajo geométrico finalizado. No quedan bloqueos detectados para las operaciones realizadas; se mantienen las limitaciones indicadas.
