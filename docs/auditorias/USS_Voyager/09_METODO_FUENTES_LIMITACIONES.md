# Método, pruebas, fuentes y límites

## Herramientas verificadas

- Windows/PowerShell para listados, copias e invocación; Python **3.10.11** y biblioteca estándar para hashes, cabeceras/BIN/JSON, OBJ, MTL y ZIP; Pillow **12.2.0** para decodificar imágenes y componer láminas de sus píxeles existentes.
- **Blender 5.2.2 LTS**, build d13f752e3b9c, instalado en `BLENDER_INSTALADO`. Background, factory-startup, disable-autoexec. BLEND abierto con `use_scripts=False, load_ui=False`. No se controló ni cerró una sesión Blender del usuario.
- Importador glTF integrado y OBJ integrado (split objects/groups, validate meshes). Workbench con color de material para geometría; Cycles CPU a 64 muestras sin denoise para shaders/texturas originales del GLB detallado.
- No se instaló ninguna dependencia. No se ejecutó Unreal ni se abrieron `.uproject`, mapas o assets del motor. Solo se leyeron informes locales y listados de carpetas relacionadas. No se ejecutaron scripts anteriores del proyecto.

## Procedimiento

Inventario acotado de biblioteca y rutas derivadas de metadatos. Modelos pequeños (4–38 MB) inspeccionados antes de cargar. Copias de los BLEND/GLB bajo `TEMP/`; OBJ original leído en una sesión vacía temporal, sin guardado ni exportación. Cálculo de matrices, bbox, usuarios, materiales/nodos, UV, áreas y conectividad. Accesores de ambos GLB decodificados directamente y comparados con recuentos Blender. Validación de índices y decodificación de imágenes; no se llama «validación Khronos completa» a este inspector propio.

Soldaduras de diagnóstico sobre bmesh desechables y cortes sobre mallas temporales en memoria. Los originales no se guardaron; las capturas no son modelos restaurados. No se utilizó ImageGen ni imagen sintética de IA. Las láminas son montajes de capturas o texturas reales. Workbench no muestra imágenes: se acompaña de renders Cycles reales y del contacto de imágenes embebidas para evitar confusión.

La primera preparación Workbench falló porque el GLB no tenía World; se creó uno temporal y se repitió correctamente. No se necesitó cancelar pruebas por memoria o inestabilidad. El render interior cerrado es oscuro porque las lámparas exteriores no resuelven la ausencia de emisión: se conserva como diagnóstico y se añade una vista con una luz interior temporal de inspección. La iluminación de capturas no es la iluminación original ni una propuesta artística final.

## Fuentes documentales leídas

- `auditoria_voyager.md` (fuente local: `RECUPERACION_VOYAGER/informes/auditoria_voyager.md`)
- `auditoria_voyager.json` (fuente local: `RECUPERACION_VOYAGER/informes/auditoria_voyager.json`)
- `VoyagerB_Informe_reparacion.txt` (fuente local: `FUENTE_OBJ/VoyagerB_Informe_reparacion.txt`)
- `INFORME_FINAL_F07_P03F.md` (fuente local: `LABORATORIOS_3D/F07_P03FG_DoorLab/Reports/INFORME_FINAL_F07_P03F.md`)
- `INFORME_FINAL_F07_P03G.md` (fuente local: `LABORATORIOS_3D/F07_P03FG_DoorLab/Reports/INFORME_FINAL_F07_P03G.md`)
- `INFORME_FINAL_F07_CHAIR_01.md` (fuente local: `LABORATORIOS_3D/F07_Chair_AutoLab/Reports/INFORME_FINAL_F07_CHAIR_01.md`)
- `INFORME_FINAL_F07_COLL_01.md` (fuente local: `LABORATORIOS_3D/F07_COLL_01_Lab/Reports/INFORME_FINAL_F07_COLL_01.md`)
- [AUDITORIA_GLB_USS_SUTHERLAND_2026-10-12.md](../../roadmap/master/fases/F02/AUDITORIA_GLB_USS_SUTHERLAND_2026-10-12.md)
- [P02_PIPELINE_PBR_BLINDAJE.md](../../roadmap/master/fases/F07/P02_PIPELINE_PBR_BLINDAJE.md)
- [P04_PLAN_PRUEBA_UE5.md](../../roadmap/master/fases/F07/P04_PLAN_PRUEBA_UE5.md)

Los informes de Sutherland más recientes documentan laboratorios ejecutados; las especificaciones del repositorio de fechas anteriores aún decían «pendiente». Se distingue la fecha/fuente: no se desechan los informes posteriores ni se afirma haber repetido sus ensayos. El informe Voyager del 09/10 se usó como guía; los recuentos/modelos de esta entrega proceden de nueva inspección. En particular se corrige su resumen de Mesh1497 con 14 caras verificadas ahora.

## Referencias técnicas primarias consultadas el 21/10/2026

- [Especificación glTF 2.0: unidades, atributos, materiales y GLB](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html).
- [Epic: Lumen Technical Details, documentación 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine).
- [Epic: FBX Static Mesh Pipeline](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine).
- [Epic: glTF Support](https://dev.epicgames.com/documentation/en-us/unreal-engine/gltf-file-format-support-in-unreal-engine).

## Alcance de la evidencia

**Verificado:** cantidades y estructura enumeradas, píxeles decodificados, rutas originales resueltas, áreas/cotas y muestras BVH, recuperación temporal de 630 grupos OBJ, defectos de suelo citados y diferencias de escala de piezas contrastadas.

**Estimado/inferido:** conveniencia de base principal, grado A–E, coste artístico relativo, potencial modular, tamaño humano probable y riesgos teóricos UE5. No se certifica fidelidad canónica con planos/fotogramas externos.

**No evaluado:** MAX binario en 3ds Max (no se abrió ni instaló lector), render mental ray/Poser original, equivalencia cara por cara MAX↔OBJ, todos los empalmes modulares, atlas UV/estiramiento exhaustivos, intersecciones arbitrarias, cápsula/NPC/ergonomía, recorrido físico UE5, Lumen, rendimiento, empaquetado e integración.

Las cotas de objeto incluyen a veces vértices sueltos; `deep_*.json` separa bbox de superficie efectivamente referenciada y área. Los umbrales de área son pruebas numéricas, no una medida universal de defecto visible. Normal opuesta a winding no identifica automáticamente «cara invertida» respecto al interior del puente. Coincidencia triangular cuantizada no clasifica intención de capas. Los rayos no tienen radio y no sustituyen colisiones de cápsula.

## Reproducción y preservación

Scripts conservados exclusivamente en el MSI, dentro de `SCRIPTS/` de la auditoría local: `inventory.py`, `blender_inspect.py`, `raw_gltf.py`, `deep_geometry.py`, `material_audit.py`, `render_diagnostics.py`, `render_textured.py`, `create_reports.py`. Las rutas fuente están declaradas en ellos. No ejecutar sobre otra ubicación sin revisar las rutas de salida; se escriben exclusivamente en esta carpeta de auditoría. Los logs guardan importaciones/avisos.

[DATOS/inventario_archivos.json](DATOS/inventario_archivos.json) publica metadatos Voyager con SHA-256, bytes y mtime_ns; la línea base local completa incluye 230 entradas y esta edición conserva 221, excluyendo las de modelos Sutherland; [DATOS/integridad_final.json](DATOS/integridad_final.json) registra la relectura final. El manifiesto documental tiene hashes de referencia, no un snapshot anterior a toda lectura. No se afirma haber rehasheado todos los proyectos/archivos del ordenador. Durante la auditoría inicial no se realizaron operaciones Git ni cambios de código. La publicación documental posterior utiliza una rama y PR Draft independientes, con autorización expresa; no incluye implementación ni merge.

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
