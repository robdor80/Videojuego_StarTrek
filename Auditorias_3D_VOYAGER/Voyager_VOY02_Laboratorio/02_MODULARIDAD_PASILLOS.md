# VOY-02 — Modularidad y pasillos
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

## Catálogo y significado de las interfaces
Se conservan 83 mallas nativas, no 317 módulos: la cifra mayor del GLB corresponde a divisiones por material. `clasificacion_modulos.csv/json` cubre cada malla con padre fuente, familia descriptiva, triángulos, envolvente, puertos candidatos y grado. Los nombres ayudan a clasificar, pero no certifican función, habitación completa o transitabilidad.

Familias: rectos corto/medio/largo, curva 90°, T/cuatro vías, tramos con puertas; accesos residenciales, marcos y nichos; cabina/accesos turbolift; conductos Jefferies; mantenimiento y conexiones verticales; envolventes y sala/sanitario. Jefferies, de ~0,914 m de altura exterior en las piezas revisadas, no es un pasillo de pie. La cabina no es un ascensor funcional y Mesh57 es acceso residencial, no un camarote suministrado.

Hay 332 sondeos cardinales en `interfaces.csv`; incluye los rechazados. Un puerto candidato exige anchura ≥0,65 m a las alturas examinadas, suelo compatible y centro sin bloqueo. Los segmentos se extraen 2 mm hacia dentro; se conservan ancla, normal, nivel, techo y anchuras a 0,4/1/1,7/2,2 m. La orientación normal y el ancla definen el ensamblaje; ni bbox ni pivote de catálogo se aceptan como socket final. El catálogo completo tiene grado E para usos aún no ensayados; los recursos seleccionados tienen C global por preparación pendiente. El grado B/C de cada unión se registra aparte.

## Siete ensamblajes ejecutados

| Caso | Grado por unión | Δ ancho mm | Hausdorff aproximado mm | Poses por H | Soporte del recorrido |
| --- | --- | --- | --- | --- | --- |
| B01_CORTO_LARGO | B | 0.0 | 82.4 | 130 | sí |
| B02_DOS_RECTOS_CURVA | C / C | 365.8 / 365.8 | 95.4 / 41.3 | 356 | sí |
| B03_RECTA_T | C / C | 365.8 / 365.8 | 95.4 / 82.4 | 267 | sí |
| B04_CUATRO_VIAS | C / C | 365.8 / 365.8 | 38.5 / 38.5 | 266 | sí |
| B05_MODULO_PUERTAS | B | 219.5 | 82.4 | 120 | sí |
| B06_TURBOLIFT | B / C | 146.3 / 422.3 | 82.4 / 376.3 | 273 | sí |
| B07_RESIDENCIAL | B | 219.5 | 82.4 | 120 | sí |

En todos los casos, H=1,60/1,75/1,90 m y r=0,35 m pasan el recorrido central seleccionado, con muestras ≤25 mm y margen 12,5 mm. El soporte usa cinco rayos por pose, cada ≤50 mm, huella de radio 0,20 m y error vertical ≤10 mm. Los resultados y matrices existentes se recuperaron íntegros; no se repitieron por cambiar cámaras.

La diferencia de perfil es un Hausdorff aproximado sobre segmentos muestreados cada 10 mm. No mide un ajuste sólido continuo ni toda la moldura. Residuos de ancla ~0 no eliminan diferencias de hasta 0,422 m de ancho o ~0,376 m en sección de la garganta a cabina. Los rectos comparten sección humana aproximada; algunos encuentros necesitan remates, otros adaptadores completos.

En B06 se conserva el negativo de suelo a ±0,90 m en el extremo estrecho de acceso→cabina: faltan 8/12 sondas amplias. El centro y la huella seleccionada sí tienen soporte. Esto impide afirmar continuidad del extremo completo. Los módulos con hojas laterales cerradas no demuestran un tránsito lateral.

## Decisión de arquitectura modular
Se puede construir una red pequeña mediante anclas propias y adaptaciones. No se demuestra un kit de perfiles intercambiables perfecto. Ninguna unión obtiene A. Priorizar Mesh12/13/18 como familia recta; usar Mesh41/40/38 para desvíos reducidos; completar una única familia de molduras y materiales antes de extender la red. Los accesos de puertas fusionadas exigirán separación local o nuevas hojas de diagnóstico en la fase funcional.

Las matrices en `matrices_instancias.csv/json` aplican normalización y giro/traslación a la geometría fuente en mundo. No son matrices locales de importación nativa: en Blender se componen además con la matriz fuente guardada en VOY-01. No aplicar nuevamente el factor 0,01 ni 100 por costumbre. Hay 24 colocaciones: 18 en los siete casos y seis en G; el mosaico B añade desplazamientos de presentación recogidos en `escenas_manifest.json`.

## Evidencia visual y límites
Las 15 capturas B se revisaron con encuadre dependiente del aspecto. Cada caso oculta temporalmente a los vecinos; las fuentes guardadas permanecen completas. Los cortes Z=2,30 m son solo de captura. Los colores son diagnósticos, sin texturas o PBR validados. La galería muestra perfiles distintos, no una continuidad artística aprobada.

Evidencias: [galería](GALERIA.html), `ensamblajes_pruebas.json`, `compatibilidades.csv`, `interfaces.csv`, `clasificacion_modulos.csv`, `matrices_instancias.json`, `pruebas_rutas.csv`. Pruebas UE, colisión simple, luz, rendimiento y circulación de NPC: E. Reutilizar las interfaces medidas; posponer el resto de la biblioteca hasta necesitarla.
