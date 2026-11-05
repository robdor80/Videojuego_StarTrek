# VOY-05A — Método y reproducción

Entorno observado: Windows 11, Blender 5.2.2 LTS instalado en `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`; Python de análisis con NumPy/Pillow y SciPy. `requirements.txt` identifica las dependencias; la copia instalada de SciPy en HERRAMIENTAS solo pertenece al laboratorio. No modifica Blender ni proyectos del usuario.

En una copia nueva del laboratorio: ejecutar `00_preparar.py` para copiar entradas originales disponibles y generar baseline; `01_inspeccionar_blender.py` con los siete nombres de recurso para exportar matrices/triángulos; el modo `catalogo` produce caras opuestas y cortes. Las vistas ISO/TOP de la primera pasada se conservan; `09_capturas_inventario.py` y las elevaciones del script 04 suministran la evidencia final por registro. No repetir el preparador sobre una entrega cuyo baseline se quiera preservar.

Orden de análisis: 03 conectividad→06 rayos/superficies→07 bordes de colección y puente→08 inventario→10 contraste/grupos→09 capturas→11 láminas→12 informes→14 recarga de escenas→15 validación/paquetes. El inventario tiene selección semántica explícita de caras frontales, verificada con elevaciones; no es un detector automático de puertas genérico. Las caras se identifican por índices de triángulo fuente y hashes, no por color/material.

Se sueldan coordenadas solo para análisis a 10 µm. Se extraen componentes de borde y se filtran secciones verticales de ancho ≥0,50 m y alto ≥0,65 m, error de plano <0,07 m; la revisión visual excluye placas exteriores, ranuras y ventanas inclinadas. Los 18 extremos de ejes verticales y el registro con tapa se incorporan explícitamente. Se conservan todos los rechazos. Las tres E no se fuerzan a una función.

`widths_by_height` conserva intersecciones reales de segmentos a distintas cotas. La envolvente de borde no garantiza la anchura libre mínima en cada profundidad. Los rayos del puente omiten hojas estáticas para sondear el hueco; no se desplazan piezas. No se ejecuta apertura/cierre ni se crean keyframes en A. Los datos de barrido anteriores permanecen bajo REFERENCIAS con su atribución histórica.

Los renders usan Workbench, geometría y colores originales de diagnóstico. CAT_*_CUT se obtiene de bisección de una malla desechable. Las líneas amarillas siguen segmentos de borde real; el texto añadido explica ID y medida. Las vistas del puente usan recorte frontal para evitar que otra arquitectura tape el acceso. No se usa ImageGen ni evidencia ficticia.

La comparación de formatos usa vecino de vértice más cercano en ambos sentidos, sin muestreo. Un máximo distinto de cero no implica automáticamente agujero o superficie distinta: puede haber teselación diferente. Tampoco una nube equivalente demuestra UV/topología/materiales iguales. Se separa esta prueba de la verificación exacta de las escenas guardadas.

Las escenas de revisión incluyen geometría completa e inventario como texto Blender; no tienen dependencias geométricas enlazadas a los originales. Los paquetes de fuentes opcionales preservan los recursos usados para reproducir las variantes. Los ZIP no incluyen el `.max` original; su conversión Blender y el registro SHA permanecen disponibles.
