# Voyager — VOY-02

Evaluación técnica cerrada el 21/10/2026. Hay adaptación pendiente antes de producción; el acceso desde el centro del puente no está demostrado.

## Nueve informes

- [RESUMEN EJECUTIVO ](00_RESUMEN_EJECUTIVO.md)
- [ESCALAS ERGONOMIA ](01_ESCALAS_ERGONOMIA.md)
- [MODULARIDAD PASILLOS ](02_MODULARIDAD_PASILLOS.md)
- [CONEXION PUENTE PASILLOS ](03_CONEXION_PUENTE_PASILLOS.md)
- [CAMAROTE JUGADOR ](04_CAMAROTE_JUGADOR.md)
- [PUERTAS SILLAS CONSOLAS ](05_PUERTAS_SILLAS_CONSOLAS.md)
- [MATERIALES RENDIMIENTO ](06_MATERIALES_RENDIMIENTO.md)
- [HOJA DE RUTA RECOMENDADA ](07_HOJA_DE_RUTA_RECOMENDADA.md)
- [PRUEBAS Y LIMITACIONES ](08_PRUEBAS_Y_LIMITACIONES.md)

## Revisión visual

[Galería de las 33 capturas](GALERIA.html). [Acceso central](LAMINAS/L01_acceso_central.png), [carreras](LAMINAS/L02_carreras_contactos.png), [asientos](LAMINAS/L03_asientos_medidos.png), [presupuesto de texturas](LAMINAS/L04_texturas_hipotesis.png). Las cuatro hojas CONTACTO muestran todas las vistas con leyendas.

## Estado y paquete

[Clasificación final](DATOS/clasificacion_final.csv), [incidencias](DATOS/incidencias.csv), [pruebas de rutas](DATOS/pruebas_rutas.csv), [estado final](DATOS/estado_final.json), [cambios frente a parada](DATOS/cambios_desde_parada.json), [matrices](DATOS/matrices_instancias.json). ZIP local: `PAQUETE/VOY02_ENTREGA.zip`; su checksum y comprobación se guardan fuera del propio ZIP en `PAQUETE/COMPROBACION_ZIP.json`. [Cómo verificar](VERIFICACION_ENTREGA.md).

## Archivos grandes locales, fuera del ZIP

- `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\ESCENAS\VOY02_Laboratorio.blend`
- `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\DATOS\obj_geometria.npz`
- `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\DATOS\modulos_geometria.npz`
- `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\DATOS\max_geometria.npz`
- `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\DATOS\prototipo_geometria.npz`
- `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\TRASPASO\VOY02_Laboratorio_ANTES_CORRECCION_OBJ.blend`
- `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\TRASPASO\CAPTURAS_Y_SCRIPT_ANTES_CORRECCION.zip`
- `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\TRASPASO\ANTES_RETRANQUEO_prototipo_geometria.npz`

Las copias de fuentes existentes están en FUENTES/OBJ, FUENTES/COLECCION y FUENTES/MAX; las rutas originales se conservan en DATOS/entradas_antes.json y TRASPASO/VOYAGER_HANDOFF.md. No se han movido ni recreado.

## Continuidad

Comenzar por los informes 00, 01, 03 y 08. El generador 00_preparar no debe repetirse. Los scripts 13, 14c, 20 y 24 tienen un propósito/estado específico y guardas contra repetición; no ejecutarlos en lote. Los scripts 11 y 09 reconstruyen/sobrescriben productos y no se utilizan para leer o verificar el cierre. El contraste 14 es de solo lectura; el cierre no inicia UE ni restauración artística. Ver la hoja de ruta para el siguiente encargo.

El ZIP es autocontenido para lectura y revisión de resultados. Repetir las pruebas geométricas requiere los NPZ y archivos Blender locales excluidos, en las rutas anteriores.
