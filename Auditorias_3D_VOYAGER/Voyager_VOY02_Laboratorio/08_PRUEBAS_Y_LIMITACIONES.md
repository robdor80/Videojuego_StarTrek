# VOY-02 — Pruebas, trazabilidad y limitaciones
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

## Qué significa el cierre
Se cierra una evaluación técnica, con análisis y ensayos documentados y paquete local. **No se declara aprobada una Voyager final.** E significa no demostrado, aunque se haya ejecutado una búsqueda o evaluación cuyo resultado sea negativo. El laboratorio reduce incertidumbre y conserva tanto éxitos como defectos.

Clasificación: A verificado/compatible en el alcance expresamente probado; B ajustes menores; C adaptación importante; D reconstrucción recomendada; E no demostrado. La ausencia de grado D global no implica que todos los detalles merezcan conservarse: la decisión de reconstrucción local depende del siguiente prototipo. Los 57 A de pantallas solo acreditan separabilidad plana.

## Registro de pruebas y autoridad
| Evidencia | Ejecución | Resultado y límites |
| --- | --- | --- |
| Integridad de recuperación 13 | Rehash nuevo, antes de modificaciones | 207 archivos, 115 entradas originales y 106 copias coinciden; 59 JSON/NPZ/PNG legibles |
| Sondeos/importación 01–06 | Recuperados del trabajo previo | Geometría, correspondencias, vanos completos y factores; no reimportados |
| Ensamblajes 07 | Recuperados, sin cambio de geometría | Siete casos ×tres H pasan rutas centrales y soporte; B/C de perfiles |
| Tránsitos 08 | Históricos de VOY-02 | Ruta pasarela verificada; centro/navegación no acreditados |
| Prototipo 09 | Recuperado y repetido en 24 tras R1 | Dos recorridos ×tres H y soporte; inicio pasarela, no centro |
| Funcional 10 | Histórico de VOY-02 | Carreras y grupos provisionales; resultados no transferidos a grupos revisados |
| Escenas 11, corrección 14c y presentación 20 | Guardado y revisión nuevos | Base OBJ reparada, agrupación semántica y cuello de referencias; ocho escenas, 49 imágenes |
| Contraste 14 | Lectura del `.blend` final sin guardar | 645/645 componentes de G coinciden a tolerancia 20 µm; máximo 11.444 µm |
| Ergonomía 15 y 18 | Nuevas mediciones | Superficies de asiento, suelos/alturas, aproximaciones y miembros hipotéticos; sin rig humano aprobado |
| Carreras 16 | Nuevas 21 fracciones +seis variantes de cinco poses/puerta | Cruces laterales; posterior con contactos; ningún pequeño offset resuelve todos |
| Acceso 17 | Nueva rejilla 10 cm, H=1,60/1,90 | Centro/navegación desconectados bajo hipótesis; ruta nueva pasarela falla refinado marginal |
| Materiales 19 | Recalculo desde metadatos VOY-01 | 49 imágenes, 102 materiales, escenarios 2K/4K; ninguna memoria UE medida |
| Accesibilidad 21 | Nuevos cilindros/soporte y rayos de cama | Cuatro giros locales libres, uno junto a cama bloqueado; no accesibilidad continua |
| Encuentros 22 y revisión 24 | Nuevos SAT por los seis adaptadores | AD_PUENTE cruzaba hojas estáticas; R1 retranquea paredes/techo y se vuelve a contrastar |
| Capturas 12 y galería 23 | Regeneración tras cambios pertinentes | 33 PNG, bounds proyectados, aislamiento B y detalles; atlas y láminas |

No se suman recargas, revisiones o renders como casos nuevos. Los datos por prueba permiten reconstruir qué se ejecutó, sobre qué superficies y en qué versión. `pruebas_rutas.csv`, `contactos_puertas.csv`, `incidencias.csv`, `clasificacion_final.csv` y `DATOS/estado_final.json` son entradas de revisión, no sustitutos de los JSON completos.

## Incidencias resueltas y resultados sustituidos
1. **Base OBJ omitida en 11:** comparación inicial mostraba diferencias de metros. Se confirmó la matriz +90° X del cache y se horneó solo en datablocks copiados. Se conserva `TRASPASO/VOY02_Laboratorio_ANTES_CORRECCION_OBJ.blend`, SHA-256 igual al fichero original inventariado. `correccion_base_obj.json` registra las 630 mallas. Se corrigió también el generador 11 para que no reintroduzca la pérdida de base.
2. **Orden de vértices:** el primer comparador ordenaba flotantes casi iguales lexicográficamente. Ese diagnóstico mezclaba cambios de orden con distancias geométricas. Se sustituyó por KDTree de centroides y seis permutaciones; el JSON preliminar y logs permanecen. No se movió geometría para resolver ese defecto del comparador.
3. **Residuo float32:** una tolerancia preliminar de 10 µm dejaba ACCESO_TURBO a ~11,44 µm. Se documentó una tolerancia final de 20 µm por transformación/cancelación de coordenadas nativas lejanas, manteniendo el residual publicado y el log estricto. No se cambiaron baselines.
4. **Cámaras y vecinos:** encuadre ortográfico por proyección sobre ejes de cámara y aspecto, margen 12%; aislamiento temporal del caso; plantas largas en formato vertical. Se conservan capturas/script previos en ZIP de TRASPASO. Los cortes BMesh y cámaras de captura nunca se guardan sobre el maestro.
5. **Agrupaciones y asientos:** navegación incluía consola/plataforma, mando omitía cojines. Se revisó la semántica y la escena E. El JSON `ergonomia_preliminar_shell_no_asiento.json` se conserva como resultado sustituido: su medida de carcasa no es una altura de cojín. No se ocultan los fallos de scripts previos ni se usan como resultados válidos.
6. **AD_PUENTE:** se detectaron cruces con las hojas estáticas abiertas. Se preservan JSON/NPZ/SAT previos en `TRASPASO/ANTES_RETRANQUEO_*`; R1 cambia solo paredes/techo nuevos. Se repiten rutas G, SAT de encuentros, contraste y capturas C/G afectados. Sigue C y necesita acabado de junta; no se certifica carrera.

Los logs de fallos de 01 y 15 se mantienen. 01_sondeo_max.log y 15_ergonomia_cojines_reales.log acreditan las ejecuciones que los sustituyen. `13_verificar_reanudacion.py` es una auditoría inicial con aserción contra la parada y **no debe repetirse al cerrar**, porque detectaría los cambios de laboratorio autorizados. La verificación final compara originales/copias contra su baseline y lista los cambios derivados por separado.

## Límites geométricos y humanos
Las cápsulas usan distancia exacta segmento–triángulo sobre candidatos espaciales. El recorrido es discreto (≤25 mm), con margen declarado; no solver continuo de cuerpos o escalones. Las superficies por debajo de pie+2 mm se excluyen del obstáculo y el soporte se verifica aparte. Cinco u ocho rayos no cubren un disco continuo. La rejilla no prueba imposibilidad absoluta y un nodo libre no prueba una conexión.

SAT cuenta superficies triangulares y contactos; no resuelve contención en volúmenes sólidos ni cavidades mecánicas. Una hoja dentro de una pared cerrada podría no cruzar superficie en el extremo abierto. Los controles de topología no certifican un bolsillo. La profundidad publicada es testigo de cruce de planos, no distancia mínima de salida del sólido.

Los proxies sentados son hipótesis paramétricas publicadas: no cubren percentiles, ropa, articulaciones, ocupante animado o confort. Los centros de pantalla no representan toda su área de botones ni una tarea manual. No se afirma campo visual, legibilidad dinámica o acceso universal. Los criterios externos son referencias de diseño con enlaces, no certificados de NASA/OSHA/CTE.

Los NPZ originales contienen superficies con sus defectos; no se limpiaron para pasar pruebas. La correspondencia numérica con esas superficies y la legibilidad de ficheros no convierten el activo en producción. El tamaño del `.blend` comprimido no es memoria GPU ni presupuesto de FPS.

## Preservación y alcance
Fuentes registradas, recursos originales, Sutherland, proyectos UE y parámetros del personaje permanecen intactos. Ningún proyecto Unreal se abrió. No hay cambios Git/publicaciones/fusiones ni instalaciones. La biblioteca original indicada por el usuario fue consultada para comprobar acceso; el trabajo se ejecutó en las copias existentes del laboratorio.

ZIP compartible: informes, tablas JSON/CSV, capturas, láminas, scripts, logs y documentos de continuidad. Fuera quedan modelos y texturas originales, `.blend`, NPZ de geometría y respaldos voluminosos; se enumeran rutas exactas en README. El paquete conserva baseline y resúmenes de integridad, sin duplicar los grandes recursos. `PAQUETE/COMPROBACION_ZIP.json` y el SHA-256 final permiten verificarlo. Las limitaciones de licencias de VOY-01 no se interpretan como prohibición de este ZIP local solicitado; no se publica en ningún servicio.
