# USS Sutherland — transferencia PBR 01

28/10/2026. Blender 5.2.2 LTS. **Entregado:** `../blender/Miranda_Puente_Sutherland_PBR_01.blend` (34.039.949 bytes).

## Fuente y procedimiento

Fuente única de materiales: `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\TABULA RASA COPIA SEGURIDAD\01_TEXTURAS_PBR_SUTHERLAND\DERIVADOS_EXISTENTES\Blender_Integracion_Final\Referencia_Visual02.blend`. Destino original: `C:\Users\andro\Documents\GitHub\Videojuego_StarTrek\juego\Clase Miranda\puente\blender\Miranda_Puente_Sutherland_Ergonomia_04.blend`. Ambos conservan sus SHA-256. No se sobrescribió ningún original, no se abrió UE5 ni se realizó commit, push o PR. No se cargó ni aplicó la variante `PBR_Paneles_Prueba_Gris`.

Antes de transferir se comprobó el Ergonomia_04 guardado: silla del capitán al 85 % de las dimensiones de Ergonomia_03; cilindro al 85 % en X/Y con altura conservada; tres paneles LCARS 30 cm más bajos; dos soportes inferiores separados y con sus caras superiores ajustadas a las consolas; franja azul presente y conectada a su atlas/emisión. Se utilizó únicamente el registro dimensional anterior para contrastar estas medidas; no se modificaron.

Se añadieron **14 materiales completos**, sin importar objetos ni mallas, y se asignaron **5.435 caras de 33 objetos**. La correspondencia directa exige orden de polígonos, topología y UV actuales coincidentes. Para las consolas agrupadas se verificó cada lado por signo X, índices de vértices normalizados y UV por esquina. Los índices de material anteriores no se sustituyeron globalmente: se añadieron ranuras y se reasignaron solo las caras verificadas.

## Materiales y superficies

| Material recuperado | Caras | Objetos actuales |
|---|---:|---|
| `Luz_Azul_Suave_Consola` | 34 | `Editable Mesh_Mat.004_0` |
| `Marcos_Ascensor_Negro` | 130 | `Circle.001_0`, `Plane.003_0`, `Plane.004_0`, `Plane.013_0`, `Plane.016_0` |
| `PBR_Capitan_Titanio` | 841 | `Plane.012_0`, `Plane.020_0`, `Plane.044_0` |
| `PBR_Luz_Sutherland_Fria` | 80 | `Plane.046_0` |
| `PBR_Mamparos_Composite_Oscuro` | 534 | `Circle.002_0`, `Cube.000_0`, `Cube.001_0`, `Plane.014_0`, `Plane.020_0`, `ceiling_0` |
| `PBR_Moqueta_Capitan` | 24 | `Circle_0` |
| `PBR_Moqueta_Puente` | 12 | `Circle_0` |
| `PBR_Paneles_Composite_Claro` | 2599 | `Circle.002_0`, `Cylinder.002_0`, `Editable Mesh_Mat.005_0`, `Editable Mesh_Mat.006_0`, `Plane.004_0`, `Plane.005_0`, `Plane.007_0`, `Plane.010_0`, `Plane.011_0`, `Plane.013_0`, `Plane.015_0`, `Plane.016_0`, `Plane.020_0`, `Plane.022_0`, `Plane_0` |
| `PBR_Paneles_Composite_Hueso` | 521 | `Circle.002_0`, `Plane.005_0`, `Plane.009_0`, `Plane.011_0`, `Plane.015_0`, `Plane_0` |
| `PBR_Puente_Barandillas_AceroCepillado` | 208 | `Plane.028_0` |
| `PBR_Puente_Plataforma_Titanio` | 56 | `Circle.001_0`, `Plane.002_0`, `Plane.003_0` |
| `PBR_Puertas_Burdeos_ConTexto` | 96 | `Plane.001_0`, `Plane.017_0`, `Plane.018_0`, `Plane.019_0` |
| `PBR_Techo_Acero_Cepillado_Claro` | 104 | `Plane.020_0` |
| `PBR_Techo_Faldones_Gunmetal` | 196 | `Plane.020_0` |

`Circle_0` recupera exactamente 24 caras de moqueta del capitán y 12 de moqueta del puente. `Plane.020_0` conserva la distribución original de cinco acabados; no se unificó el techo. `PBR_Capitan_Titanio` se aplicó únicamente a estructuras del techo (`Plane.012_0`, `Plane.020_0`, `Plane.044_0`), nunca a la silla ni a su cilindro. Las cuatro mallas de puertas mantienen sus dimensiones y geometría (alturas entre 303,08 y 304,50 cm).

## Conservación y excepciones

- **Siete sillas intactas:** se protegieron las 96 piezas de las seis sillas laterales y las cinco piezas de la silla del capitán, incluidos soporte/cilindro. No cambió ninguna geometría, transformación, ranura, asignación ni grafo de sus materiales.
- **LCARS:** 2.198 caras conservan sus materiales y UV; también se conservan sus imágenes y grafos originales.
- **Azul:** `Editable Mesh_Mat.004_0` recibe `Luz_Azul_Suave_Consola` en las 34 caras con correspondencia exacta de la fuente: 18 a un lado y 16 al otro. Otras dos caras del segundo lado conservan `BLUE`, como en la fuente. Ambas franjas mantienen emisión. No se simplificó ningún grafo Light Path/Transparent/Emission.
- **Piezas inferiores:** `Editable Mesh_Mat.003_0` y `.003_0.001` conservan íntegramente sus materiales actuales porque no hay correspondencia de topología + UV verificada. No se copiaron las UV antiguas.
- **BLUE protegido:** no se aplicaron acabados opacos antiguos sobre `Editable Mesh_Mat.007_0`, `.010_0`, `.011_0`, `Plane.008_0`, `Plane.023_0` o `Plane.025_0`. Se preservaron sus caras azules actuales, además de las dos citadas en `.004_0` y las piezas inferiores.
- Los materiales básicos sin sustitución PBR compatible se conservaron, incluidos los materiales de sillas, LCARS, rótulos y otras superficies heredadas. No se trasladaron cueros de las sillas antiguas. No hay dependencias pendientes: **26/26 imágenes utilizadas empaquetadas**, con tamaño válido; ninguna biblioteca Blender enlazada.

## Validación ejecutada

Se guardó el archivo nuevo y se reabrió en un proceso independiente de Blender. Pasaron todas las comprobaciones de `datos/pbr01_verificacion.json`: **346 objetos y 171 mallas**, identidad de vértices, aristas, conectividad y orden de caras/esquinas, todas las capas UV, atributos de normales personalizadas y aristas duras, transformaciones, dimensiones, jerarquías y configuración de modificadores/restricciones. Coinciden los materiales protegidos y todos los grafos/imágenes originales. Las únicas caras reasignadas son las del manifiesto; los 14 grafos añadidos coinciden con los de la fuente, incluidas conexiones y parámetros.

Comprobación visual ligera **ejecutada en la interfaz de Blender**, modo Material Preview, vistas exterior, superior e interior oblicua: se muestran las dos moquetas, puertas burdeos, atlas LCARS, las siete sillas y ambas consolas con franjas azul claro. No se observaron texturas magenta en esas vistas. No se guardaron los cambios de navegación/previsualización. **Esta revisión no constituye aprobación estética definitiva**, ni prueba de iluminación indirecta por render ni validación en UE5.

Manifiesto compacto: `datos/pbr01_manifest.json`; incluye fuente/destino, hashes, exclusiones y correspondencias por intervalos de caras (índices desde cero). Evidencia inicial: `datos/pbr01_preflight.json`. Scripts: `scripts/transferir_pbr01.py`, `scripts/verificar_pbr01.py` y auxiliar `scripts/pbr01_integrity.py`. El script de transferencia rechaza sobrescribir una salida existente.

**Limitación pendiente:** aprobación visual del usuario y, si se desea en otra intervención, revisión artística de las superficies conservadas por precaución. Trabajo finalizado en Blender; sin continuación automática.
