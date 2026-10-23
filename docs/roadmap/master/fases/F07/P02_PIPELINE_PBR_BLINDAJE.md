# F07-P02 — Cadena Blender/Rob3D/UE5, UV y PBR

**13-10-2026 · CERRADA SOLO COMO ESPECIFICACIÓN.** Ni Blender ni UE5 se han ejecutado aquí.

1. **Original inmutable:** conservar máster con SHA-256; exportar derivados con versión y trazabilidad. No sobrescribir mallas ni texturas recibidas.
2. **Escala y ejes:** verificar origen, pivote, bounding box, normals/winding, tangentes y unidades con una cápsula de 1,70 m. Unreal usa centímetros; al pasar de glTF/Blender a UE comprobar rotación real, no transformar a ciegas.
3. **UV:** UV0 para mapas de superficie (albedo/normal/ORM), UV adicional si se requiere lightmap; comprobar seam, estiramientos, tiling y densidad de texel.
4. **Material:** albedo BaseColor sRGB; Normal sRGB OFF; mapas AO, Roughness y Metallic **lineales**; empaquetado ORM estándar de proyecto R=AO G=Roughness B=Metallic; revisar canales en material UE5.
5. **Iluminación:** la arquitectura de Sutherland viene enteramente unlit. Convertir **selectivamente** paredes, piso, techo, pilares, asientos y carcasas a Default Lit/PBR manteniendo originales. Conservar LCARS emisivos; reemplazar visualmente una pantalla con superficie dinámica de consola, sin confundir imagen estática con interacción.
6. **Colisiones:** crear primitivas simples diferenciadas para suelo/paredes/platformas/barandillas/sillas; no fusionar puertas, asientos o consolas animables. Optimizar por medición real de draw calls, FPS, VRAM; LODs/instancing por grupos cuando proceda.

## Placas de blindaje ablativo — Clase Valhalla
Preparar placa individual con ID, pivote, sección del casco, espesor geométrico cuando despliegue, UV0 y mapas PBR; rugosidad pintada y microdesgaste en Material Instances, juntas coherentes. Un normal map no crea relieve de colisión. En módulos desplegables comprobar trayectorias, z-fighting, interferencia con torpedos/ventanas/hangares y LOD. Estados **propuestos visualmente**: RETRAIDO / DESPLEGANDO / DESPLEGADO / RETRAYENDO; no definir en F07 reglas de daño, tiempo de activación ni API Core no verificada.

## Puerta local pendiente
Una placa de blindaje de prueba + una sección interior Sutherland, con capturas bajo luces variadas, normales/roughness/metallic correctos, dimensiones y consumo medidos. La aprobación del tratamiento artístico no equivale a modelado ni a blindaje funcional.

## Implementación de referencia verificable (13-10-2026)

En `tools/assets/f07_pbr_plate.py` se ha creado un generador **independiente de Blender** que produce un GLB glTF 2.0 determinista, sin dependencias Python externas. Su placa de **laboratorio** contiene geometría real, normales, UV0, texturas PNG incrustadas para BaseColor, normal y ORM, y dos materiales **PBR lit**. No representa la geometría definitiva de Valhalla, ni despliegue, ni efecto de daño.

En `tools/assets/f07_gltf_audit.py` hay un inspector GLB de **solo lectura**, con validación de cabecera, segmentos BIN/JSON, accesores, UV y referencias de texturas. Detecta material `KHR_materials_unlit`, emite SHA-256 y registra explícitamente que **UE5 no está probado**.

### Ejecutar en cualquier Python 3.10+ sin Blender

```powershell
python tools/assets/f07_pbr_plate.py --output "C:\Temp\F07_Plate_Demo.glb" --manifest "C:\Temp\F07_Plate_Demo.manifest.json"
python tools/assets/f07_gltf_audit.py --input "C:\Temp\F07_Plate_Demo.glb" --require-pbr --output "C:\Temp\F07_Plate_Demo.audit.json"
python tools/validation/test_f07_pbr_pipeline.py -v
```

Nunca sobreescribir los originales; el generador **rechaza sobrescrituras por defecto**. `--force` solo debe usarse con salidas generadas deliberadamente, jamás con un asset descargado. Guardar derivados fuera de las carpetas maestras.

**Evidencia técnica limitada:** el test automatizado ejercita el generador, detección de unlit, integridad GLB y UV, reproducibilidad, protección contra sobrescritura y prohibición de confundir los metadatos con prueba de UE5. La CI correspondiente es `.github/workflows/f07-pbr-reference.yml`. Registrar en el PR y acciones el resultado real; su aprobación permite decir **REFERENCIA_PROBADA del ejemplo procedural**, no que los materiales del Sutherland o Valhalla estén ya modificados.

### Primer paso posterior en MSI

Abrir `F07_Plate_Demo.glb` en Blender y Unreal, comprobar ejes/unidades, aspecto real de rugosidad/metalness, normals y maps ORM; reemplazar por modelo canónico solo tras decisión de arte. La conversión lit de la arquitectura Sutherland y la importación real siguen P02/P04 pendientes de ejecución local.

## Reconciliación posterior — trabajo artístico local (23-10-2026)

El encabezado «Ni Blender ni UE5 se han ejecutado aquí» se refiere al **alcance de la especificación de 13-10-2026**, no al historial completo posterior del proyecto. Desde entonces se ha comunicado trabajo de texturizado PBR de Sutherland **en una copia artística de Blender** (suelo, techo, puertas, iluminación y algunos elementos de mobiliario). Estos archivos locales todavía no están cotejados ni exportados como prueba oficial desde este repositorio.

Por tanto, mantener dos carriles sin mezclarlos:
- **Referencia P02 versionada:** generador PBR, auditor GLB y test/CI; sigue cerrada a nivel REFERENCIA_PROBADA.
- **Proyecto artístico del Sutherland:** ejecución local Blender **reportada**; comprobar ruta/copia, materiales, textura y visualización real en UE5 antes de aprobar la conversión.

El blindaje de Valhalla **no** se considera desplegable por disponer del ejemplo de placa procedural; sigue siendo una tarea de modelado/integración específica separada. Ver [acta de evidencia F07](RECONCILIACION_EVIDENCIAS_MSI_2026-10-23.md).
