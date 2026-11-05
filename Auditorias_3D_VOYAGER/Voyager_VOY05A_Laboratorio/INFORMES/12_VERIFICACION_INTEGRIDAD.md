# VOY-05A — Verificación de integridad y entrega

Los archivos originales se inventariaron y calcularon con SHA-256 antes de usar las copias. `VERIFICACION/originales_antes.json` y `referencias_antes.json` enumeran el alcance exacto: no es un hash global de todo el MSI, de CoreRPG ni de todos los proyectos Sutherland. La relectura final está en `VERIFICACION/integridad_final.json`, que distingue cambios de bytes y metadatos. Consultar su resultado, no inferir integridad a partir de este texto.

Las escenas de revisión conservan posiciones/hojas estáticas y materiales/UV fuente. Se comprueban por recarga de Blender contra las coordenadas mundiales, triángulos y nombres fuente; `VERIFICACION/escenas_readback.json` documenta resultados. Se empaquetan recursos de imagen disponibles; los ausentes se informan, sin sustituirlos por texturas nuevas. Las escenas distribuidas son las `*_Revision.blend`; las primeras escenas de importación quedan como pasos intermedios locales.

`VERIFICACION/validacion_local.json` comprueba IDs, CSV/JSON, existencia de cada captura, dimensiones de PNG, enlaces relativos de Markdown/HTML y estructura de informes. Los datos numéricos, scripts, manifiestos y referencias acompañan el paquete documental. No se incluyen cachés, bytecode ni dependencias Python descargadas en los ZIP documentales.

Cada ZIP se abre, comprueba CRC, nombres únicos y rutas relativas seguras, se extrae a verificación temporal dentro del laboratorio y se contrasta su SHA-256 por miembro. `VERIFICACION/paquetes_validacion.json` guarda la comprobación y `PAQUETE/VOY05A_Paquetes_SHA256.txt` sus hashes. Cada paquete debe permanecer por debajo de 100 MiB; si se divide la colección de imágenes, cada ZIP conserva rutas completas y es extraíble por sí mismo en la misma raíz.

La entrega remota tiene una verificación separada: `VOY05A_Drive_Verificacion.json` y `VOY05A_Drive_SHA256.txt`. Se exige metadata real de Drive, tamaño y SHA-256 remoto cuando esté disponible. Si solo existe MD5 se compara también con el archivo local; no se afirma descarga si no se hizo. Los dos manifiestos finales se suben después de los paquetes. Su propio hash no se incluye dentro de sí mismos, para evitar autorreferencia.

No se hicieron commits ni PR, no se abrió Unreal, no se añadieron animaciones o mecanismos, y no se guardó sobre los originales. Los cambios temporales son cámaras, visibilidad, líneas de contorno y cortes sobre mallas desechables. Las copias locales se conservan después de la publicación.
