# VOY-05A — Referencias Sutherland

Se leyeron copias de informes disponibles de F07_P03FG_DoorLab, incluidos los baselines de P02/P03B/P03C/P03D/P03E y los informes finales P03F/P03G. No se modificó ningún archivo Sutherland ni se abrió Unreal. Los hashes de estos documentos se conservan en `VERIFICACION/referencias_antes.json`. El informe de sillas leído por VOY-04 es contexto ergonómico, no fuente de dimensiones de puerta.

La última entrega Sutherland se describe como **preparada para revisión humana, sin integración en producción**. Registra cuatro puertas/ocho hojas y un único BP parametrizado. D04 tiene cabina construida; D01–D03 permanecen bloqueadas por falta de destino. Esas pruebas no aprueban automáticamente Voyager ni Valhalla.

Procedimientos aprovechables: identificar caras originales de las hojas y preservar UV/normales; usar raíz de puerta con X normal, Y deslizamiento y Z altura; agrupar toda la hoja y conservar las bases/mamparos fijos; fabricar alojamientos huecos sólidos y retornos que oculten la hoja en vistas oblicuas; mantener referencias originales sin duplicados activos; comprobar lectura de assets importados frente a Blender guardado.

Problemas documentados y lecciones: D02/D04 necesitaron pequeñas elevaciones propias para holgura con sus suelos; D03 necesitó carcasa posterior menos profunda para evitar techo/paneles; D04 detectó discrepancia Chaos frente a SAT y se recocinó un convexo exacto en assets nuevos, sin encoger hojas. Una jamba siguió bloqueando un carril lateral y no se recortó para falsear el paso. El fallo de NavMesh provenía de un volumen temporal recolocado al origen por el fixture; se comprobó la posición real después de construirlo.

No se trasladan los recorridos ≈86,8 cm, vano ≈164 cm, ranuras, márgenes, elevaciones o tiempos de Sutherland: pertenecen a sus hojas y contexto. El puente Voyager examinado tiene aproximadamente la mitad de ese ancho a escala fuente. Reutilizar el procedimiento y el contrato de ejes resulta razonable; reutilizar dimensiones sin medición no.

Pruebas futuras a tomar como referencia en C/D: poses intermedias y barrido completo ida/vuelta; geometría real antes de interpretar cajas; comprobar contactos intencionales por separado; ocultación física en varias vistas; paso y soporte en cabina real; bloqueo mientras no exista destino. VOY-05A no ejecuta esos ensayos ni crea Blueprints. La organización desacoplada de sillas informa el criterio de componente fijo/móvil, sin importar su desplazamiento de 30 cm.
