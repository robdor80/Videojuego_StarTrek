# Comparación y selección de base

No hay una única línea de versiones por tamaño. Son dos familias de autoría/procedencia distinta y varios derivados de la familia detallada.

| Variante | Integridad/organización | Arte/UV | Selección |
|---|---|---|---|
| Colección .blend nativo | 83 mallas / 189 objetos; módulos con materiales, puente simple de 8 mallas | Sin imágenes; UV0 general con tiling/degeneraciones | Base del kit de pasillos, no del puente protagonista |
| Colección GLB | 317 mallas divididas por material; 67.563 triángulos crudos | 8 materiales constantes, 0 imágenes | Referencia portable del kit; no es una versión texturizada |
| ZIP colección | Un único BLEND, hash igual al extraído | Exactamente la misma fuente | Respaldo, no nueva versión |
| OBJ + MTL vigente | 630 grupos recuperables; 271.705 triángulos tras validar; suelo frontal íntegro en comparación | 102 materiales, 49 imágenes activas; UV0 en todos los grupos | BASE PRINCIPAL de recuperación propuesta |
| BLEND de trabajo OBJ | 1 objeto fusionado, 271.705 triángulos | 49 imágenes externas con rutas originales correctas | Referencia editable limitada por fusión; conserva arte |
| GLB de trabajo OBJ | 1 nodo / 1 malla / 102 primitivas | 49 imágenes embebidas sanas; albedo sin PBR completo | Referencia visual autocontenida y respaldo de arte |
| BLEND MAX de trabajo | 631 mallas MAX + 1 OBJ heredado; escalas diferentes, suelo dañado, dos piezas alejadas | 90 materiales MAX usados sin imagen; 41 mallas MAX sin UV | Fuente secundaria; no elegirla por número de objetos |
| MAX 2011 original | Inventariado / 19.895.548 bytes; no abierto con 3ds Max | MC6 y texturas asociados disponibles | Conservar para futura comprobación; E en equivalencia completa |

## Evidencia decisiva

- La prueba temporal de separación OBJ **ya se ejecutó**: 630 objetos, sin guardarlos como modelo derivado. Por tanto no es una promesa basada solo en el nombre del archivo.
- `floorfront_1` del OBJ tiene 613 caras triangulares y **32,829204 m²**. En MAX convertido `floorfront` conserva **0,000133254 m²** con 593 vértices sueltos. La mayor dimensión de su bounding box no representa un suelo mejor.
- La separación del OBJ no conserva pivotes originales: todos quedan en cero. Aun así conserva mejor equilibrio de superficies, UV, texturas y editabilidad que iniciar desde el GLB fusionado o la conversión MAX defectuosa.
- El archivo MAX de trabajo del Escritorio y el de Recovery tienen hash idéntico: no son dos recuperaciones distintas.
- El GLB detallado tiene la misma envolvente y triangulación que el BLEND fusionado, con más vértices por atributos. No se ejecutó equivalencia completa de normales/UV cara por cara; coincidencia de conteos no es prueba suficiente de identidad completa.
- El OBJ y el MAX convertido no se pueden mezclar por coordenadas: la pieza de techo contrastada muestra escala relativa ~1,5081 y desplazamientos. No se ha decidido cuál es la escala canónica de rodaje.

## Recomendación concreta

Conservar juntos **OBJ original, MTL vigente, MTL anterior, 102 imágenes del Escritorio, GLB texturizado y MAX/MC6/BLEND originales**. Para una futura copia de trabajo empezar con la importación separada del OBJ, manteniendo el GLB como patrón de aspecto. Conservar el nativo BLEND de la colección para módulos, con su ZIP idéntico como respaldo. No se copiaron materiales entre familias ni se eligió el modelo de más bytes/polígonos.

Comparación visual: `CAPTURAS/comparativa_puentes.png`, vistas completas y cortes por versión en el índice. Las vistas de corte eliminan solo caras altas en sesiones temporales; no deben usarse para inferir ausencia de techo en el archivo original.

> Edición pública documental: las rutas personales se sustituyen por alias de origen. Las capturas citadas por nombre se conservan solo en el MSI; no están incluidas en el repositorio. Los ocho análisis mantienen su alcance técnico. Véase [publicación y límites](README.md#publicacion-y-limites).
