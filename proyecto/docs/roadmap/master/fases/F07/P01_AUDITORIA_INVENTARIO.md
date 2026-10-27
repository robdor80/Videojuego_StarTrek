# F07-P01 — Auditoría de modelos, catálogo y derechos

**13-10-2026 · EN_REVISION.** No se ha tenido acceso al disco del MSI desde este trabajo.

## Auditoría preexistente
Ver F02/AUDITORIA_GLB_USS_SUTHERLAND_2026-10-12.md. Original star_trek_sutherland_bridge.glb, 13.429.416 bytes, SHA-256 **53ac9b52fe9fb4b19c5488d7265f6f7471383ae89071204fd3fc62232ca3889b**, 170 mallas, 343 nodos, 19.501 triángulos, 25 materiales KHR_materials_unlit, 17 imágenes, sin rig/animaciones. No equivale a UE5 jugable.

Metadatos internos declaran Andrew Perdzock y CC-BY-4.0: https://sketchfab.com/3d-models/star-trek-sutherland-bridge-7dcbb60473164f36a0a4f39df11b34c1 . **Pendiente comprobación independiente de licencia, condiciones de atribución y derechos de Star Trek.** Archivo de Rob3D con sufijo Validado sin comparación hash; no asumir identidad.

## Ingesta del MSI
Cuando el autor disponga del equipo, desde una copia del repositorio usar Python 3.10+:

    python desarrollo/tools/assets/f07_inventory.py --root "D:\Modelos3D" --output "C:\Temp\f07_catalogo.json"

Opcional: --hash-files para SHA-256 completos; puede tardar con bibliotecas grandes. La herramienta **solo lee** los archivos fuente, no sigue enlaces ni modifica/renombra contenidos; produce JSON de **rutas relativas** fuera de la carpeta fuente. No publicar el catálogo sin revisar procedencia y metadatos privados.

Campos: ID estable basado en ruta, original, nombre amigable (alias), ruta relativa, extensión, bytes, categoría sugerida (bridge/ship/station/npc/prop/texture/archive/unknown), hash opcional, procedencia/licencia y validación UE5 pendientes. La clasificación por nombres NO sustituye inspección geométrica.

## Regla de renombrado
**Preservar siempre originales de Rob3D.** Trabajar con alias amigables y manifest de equivalencias, sin borrar automáticamente números/sufijos; estos pueden contener metadatos útiles. Si en el futuro se renombra un derivado, conservar hash original y referencias.

## Pendientes de ejecución
Listado local de muchos modelos (autor, sin fecha límite), revisión por lotes; hashes original y export Rob3D; permisos de uso/atribución antes de distribuir; pruebas UE5/Blender. Catálogo de decisiones ya conocidas: assets/otros/escenas/bridges/f07_registry.json.

## Auditor estructural local adicional (nueva herramienta F07)

El analizador `desarrollo/tools/assets/f07_gltf_audit.py` comprueba, sin modificar, integridad del contenedor GLB 2.0, vistas de buffers, accesores, UV por primitiva, materiales, extensiones unlit, imágenes, triángulos y SHA-256. No es un importador UE5, ni afirma escala transformada mundial ni derechos. En el MSI puede auditar el original Sutherland verificando previamente el SHA indicado en F02:

    python desarrollo/tools/assets/f07_gltf_audit.py --input "C:\\ruta\\star_trek_sutherland_bridge.glb" --expect-sha256 53ac9b52fe9fb4b19c5488d7265f6f7471383ae89071204fd3fc62232ca3889b --output "C:\\Temp\\sutherland_audit.json"

Esto se ejecutará solo cuando se disponga del GLB local; no consta ejecutado en el MSI.

## Reconciliación posterior — 23-10-2026

El párrafo inicial y los pendientes anteriores describen **el estado histórico de 13-10-2026**. Después hubo pruebas locales UE5 del Sutherland, por lo que ya no debe interpretarse que nunca se trabajó con el original/derivados en el MSI.

**Siguen pendientes de incorporarse a este expediente:** inventario completo del disco, ruta exacta del derivado importado, comparación SHA/GLB y procedencia de variantes. No asumir que el hash original anterior corresponde automáticamente al archivo realmente usado en UE5.

Véase [reconciliación F07 del 23-10-2026](RECONCILIACION_EVIDENCIAS_MSI_2026-10-23.md). Esta actualización **no implica** haber accedido al MSI desde GitHub ni haber cerrado la revisión de procedencia.
