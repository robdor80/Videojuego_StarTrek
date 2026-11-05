# Voyager VOY-03 — Laboratorio reproducible

**Estado: COMPLETADA · circulación geométrica · opción A sin modificar arquitectura.**

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

- [Resumen y diez respuestas](00_RESUMEN_EJECUTIVO.md)
- [Causas del bloqueo](01_DIAGNOSTICO_CIRCULACION.md)
- [Perfiles y cotas](02_ESCALONES_Y_DESNIVELES.md)
- [Pruebas por altura](03_PRUEBAS_CAPSULAS.md)
- [Comparación de alternativas](04_SOLUCIONES_EXPERIMENTALES.md)
- [Red completa y regresiones](05_RECORRIDOS_COMPLETOS.md)
- [Información para pruebas futuras](06_PREPARACION_UE5.md)
- [Próximas decisiones](07_RECOMENDACIONES_FUTURAS.md)
- [Método y límites](08_METODOLOGIA_Y_LIMITACIONES.md)

## Abrir las escenas

Archivo final: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY03_Laboratorio\ESCENAS\VOY03_Circulacion.blend`. Incluido en el ZIP bajo ESCENAS.

1. `01_REFERENCIA_ORIGINAL`: conjunto físico de referencia VOY-02, puertas abiertas y adaptadores existentes.
2. `02_DIAGNOSTICO`: mismas piezas, perfiles y cápsulas de referencia; ayudas sin colisión.
3. `03_EXPERIMENTO_A_SIN_CAMBIOS`: rutas validadas del puente, arquitectura intacta.
4. `04_RECORRIDOS_COMPLETOS`: centro a turbolift y camarote sobre el ensamblaje existente.

Los 645 objetos físicos se comparten entre escenas para evitar duplicación. No editar su malla en una escena esperando que las demás sean independientes; crear otra copia explícita para una futura modificación. En diagnóstico se muestra por defecto la cápsula de 1,90 m; las de 1,60 y 1,75 están ocultas para evitar superposición y pueden activarse en el Outliner. Referencia original completa de ocho escenas: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY03_Laboratorio\REFERENCIAS\VOY02\VOY02_Laboratorio.blend` (fuera del ZIP para evitar duplicarla; SHA en baseline). Fuente anterior intacta: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio\ESCENAS\VOY02_Laboratorio.blend`.

## Datos y evidencia

Empezar por [GALERIA.html](GALERIA.html), las láminas y `DATOS/resultados_rutas.csv`. `barridos_resultados.json` conserva todas las poses y fallos finales; `apoyo_continuo.json` acredita soporte entre muestras. NPZ y scripts reproducen las pruebas. `contraste_VOY03.json` verifica el archivo guardado. `baseline_protegido.json` / `integridad_final.json` comparan fuentes antes/después. Los JSON A0/A1/A2 y la carpeta REVISION_A1_NO_VALIDADA son resultados descartados conservados, no aprobados.

Reproducción y orden de scripts en [metodología](08_METODOLOGIA_Y_LIMITACIONES.md). Los scripts 00 y los archivos de cierre son operaciones de auditoría/paquete; no borrar el baseline ni reemplazar las evidencias originales de una repetición.

ZIP: `PAQUETE/VOY03_Entrega.zip`. Incluye informes, datos, NPZ, scripts, registros, capturas, láminas y Blender final. Excluye únicamente la referencia Blender duplicada, cachés Python y el propio directorio PAQUETE. `MANIFIESTO_SHA256.json` dentro del ZIP permite comprobar cada entrada; verificación externa en `PAQUETE/verificacion_zip.json`.

No se abrió Unreal ni se inició VOY-04. No hay commits, PR ni publicaciones. Mantener separadas viabilidad geométrica, estimación para Unreal y validación real en Unreal pendiente.
