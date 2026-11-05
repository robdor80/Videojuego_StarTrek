# Verificar la entrega VOY-02

El ZIP contiene MANIFIESTO_ENTREGA.json con ruta, tamaño y SHA-256 de cada archivo de contenido. El propio manifiesto no se incluye a sí mismo en esa lista. La comprobación del ZIP vuelve a leer cada entrada y contrasta todos esos hashes, además de revisar el CRC.

PAQUETE/COMPROBACION_ZIP.json y PAQUETE/VOY02_ENTREGA.sha256.txt permanecen al lado del ZIP en el laboratorio local. Contienen el hash del ZIP completo y el resultado real de comprobación. No se incluyen dentro del ZIP para evitar una dependencia circular de su propio hash.

Los nueve informes, tablas, capturas y galería pueden leerse tras extraer la carpeta. Repetir ensayos de geometría requiere los archivos grandes locales listados en README, excluidos del paquete. Los originales y baselines no deben reconstruirse ni sobrescribirse para ejecutar una verificación.

Los JSON de TRASPASO y los logs anteriores son historia conservada. El estado de cierre está en DATOS/estado_final.json y los informes finales; un resultado anterior negativo o sustituido no debe confundirse con la versión final sin leer el informe 08.
