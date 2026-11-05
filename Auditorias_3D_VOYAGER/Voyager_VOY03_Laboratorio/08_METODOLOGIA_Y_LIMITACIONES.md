# VOY-03 — Metodología, trazabilidad y límites

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

## Entradas, aislamiento y conservación

Laboratorio anterior: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio`. Laboratorio nuevo: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY03_Laboratorio`. Se leen copias de datos geométricos y la referencia Blender, nunca se guarda sobre VOY-02. La toma inicial SHA-256 incluye **2762 archivos protegidos**: VOY-01, todo VOY-02 y los 115 originales registrados por la fase anterior. También se registran hashes de las 27 copias iniciales de referencia y, por separado, diez capturas de continuidad copiadas para revisión. Las 33 capturas originales siguen intactas en VOY-02. `baseline_protegido.json` es inmutable; la comprobación final genera otro archivo, no reemplaza el estado inicial.

No se realizaron operaciones sobre Sutherland, proyectos Unreal, CoreRPG ni otros proyectos. No se ejecutó Git, se crearon commits/PR, se accedió a GitHub ni se hicieron publicaciones. No se instaló software. La prueba de hashes cubre los conjuntos registrados; no se presenta como un hash global de todos los discos del MSI.

## Procedimiento reproducible

`01_topografia.py` reconstruye coordenadas físicas desde la importación OBJ numérica de VOY-02, aplica solo la escala de referencia y las poses abiertas completas de las puertas. `walkgeom.py` clasifica apoyos por función explícita y conserva el resto como obstáculos. El BVH busca superficies horizontales por ambos lados; si falla en una arista coincidente, se intersectan esos mismos triángulos en doble precisión.

`04_busqueda_original.py` propone una rejilla de 10 cm. `06_replanificar_aristas.py` vuelve a comprobar nodos con apoyo vertical, usa cambios de suelo ≤18 cm y rechaza enlaces cuyo refinamiento a 1 cm colisione o pierda apoyo. No se presenta la mera resolución del grafo como un aprobado físico. `07_barridos_y_recorridos.py` comprueba cada tamaño de cápsula contra mallas completas y los intervalos de traslación. `09_apoyo_intervalos.py` exige apoyo continuo por convexidad sobre triángulos reales; su certificado final incluye componente vertical ≥0,50 y cota de separación ≤8 mm. `14_datos_y_exportacion.py` exige ambos resultados antes de producir tablas finales.

`10_mediciones.py` mide perfiles y secciones transversales, conserva límites y anomalías de topología. `11_comparacion_algoritmos.py` reproduce el control negativo del pie fijo sobre las primeras candidatas. `12_laboratorio_blender.py` crea cuatro escenas compartiendo los 645 componentes físicos; las viejas 24 piezas de maniquí se identifican como auxiliares y no se incorporan a la arquitectura. `16_contraste_guardado.py` reabre el archivo final, contrasta todos los componentes contra los triángulos del prototipo y comprueba sus huellas geométricas y matrices.

El contraste admite 20 µm por cancelación de precisión simple en módulos con coordenadas nativas alejadas del origen; máximo observado **11.444 µm**. No se cambió una pieza para borrar ese residual. Se comprueba además igualdad exacta de vértices/caras/matrices con las copias de origen y que el archivo no cambió durante la verificación.

## Errores y resultados negativos conservados

Los scripts y resultados intermedios registran inventario incompleto, arista diagonal bloqueada, tolerancia de triángulo errónea, fallo BVH y candidato con apoyo lateral. Los informes finales distinguen esos diagnósticos del resultado definitivo. Las primeras capturas B se conservan en `CAPTURAS/REVISION_A1_NO_VALIDADA`; algunas estaban recortadas u ocluidas y sus rutas no tenían certificado de apoyo. No son evidencia de aprobación. Las nuevas plantas usan límites de cámara medidos, y los detalles de cápsula se reencuadraron. El montaje QA inicial también se conserva.

El primer lanzamiento de depuración tuvo una ruta mal escrita y no ejecutó el script; se corrigió la ruta. El registro `05_perfiles_y_bloqueos.log` conserva un error de sintaxis de la primera versión, corregido antes de medir. Un código de salida cero de Blender no se usa como criterio único: se revisan los JSON, el número de casos, las métricas, imágenes y el contraste guardado.

## Qué significa el resultado

Se demuestra existencia de una trayectoria continua de cápsula con apoyo geométrico y sin intersecciones dentro de las tolerancias declaradas. No se demuestra comportamiento dinámico de un controlador, equilibrio biomecánico, contacto de la planta del pie, animación, confort, velocidad, inercia ni accesibilidad universal. El algoritmo de envolvente inferior permite que la cápsula redondeada suba progresivamente por las narices, sin suponer un salto de nivel. La ruta final mantiene apoyos intermedios y rechaza el atajo que perdía soporte vertical.

La reversibilidad usa identidad del volumen barrido y una hipótesis simétrica de subida/bajada de 18 cm. No es una segunda simulación física. Los obstáculos son caras trianguladas por ambos lados; el futuro motor puede interpretar normales y colisiones de otra manera. La clasificación COMPLETADA se refiere al alcance **geométrico** de VOY-03, no a un puente jugable terminado.

## Reproducción

Usar Blender 5.2.2 LTS en segundo plano con `--background --python RUTA_SCRIPT`. Los scripts resuelven R desde su carpeta SCRIPTS. No volver a ejecutar `00_copias_y_baseline.py` sobre este laboratorio: se detiene si ya existe el baseline. Para una repetición íntegra usar una copia nueva del laboratorio y conservar primero los resultados entregados. No ejecutar los antiguos scripts VOY-02 desde su carpeta.

Orden funcional: 01 → 04 → 05 → 06 → 07 → 09 → 10 → 11 → 14; después 12 → 16 → 15 → 17 → 18 → 19 → 20 → 21. `15_laminas.py` y `17_informes.py` usan Python del sistema con Pillow para las láminas; los demás cálculos geométricos usan NumPy y mathutils de Blender. 18 se ejecuta con Blender; 19–21 con Python del sistema. No precisan instalar paquetes. `02_planta_soportes.py` y 03 son diagnósticos iniciales y no sustituyen las salidas finales. 08 y 13 son reproducciones de errores conservados; sus salidas no deciden el estado final.

Se incluyen NPZ de entrada suficientes para repetir el cálculo sin el blend fuente. La referencia Blender completa queda en REFERENCIAS/VOY02 dentro del laboratorio local, documentada por ruta/hash; la escena final se incluye en el ZIP. Los datos de baseline conservan rutas absolutas del MSI para auditoría local.
