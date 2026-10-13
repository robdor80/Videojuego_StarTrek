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
