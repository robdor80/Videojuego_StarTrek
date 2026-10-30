# USS Sutherland — seis sillas operativas

Intervención local del 29 de octubre de 2026, con Blender 5.2.2 LTS. Resultado guardado y vuelto a abrir para una comprobación independiente.

## Entrega

- [Archivo Blender de resultado](../blender/Miranda_Puente_Sutherland_PBR_Manual_01_Seis_Sillas_01.blend).
- [Script de reproducción](scripts/seis_sillas_replicar.py), con [funciones comunes](scripts/seis_sillas_comun.py) y la utilidad existente [pbr01_integrity.py](scripts/pbr01_integrity.py).
- [Manifiesto: correspondencia exacta de objetos y matrices](datos/seis_sillas_manifest.json).
- [Validación tras reabrir el resultado](datos/seis_sillas_verificacion.json): `ok: true`, sin errores.
- [Inventario previo](datos/seis_sillas_inspeccion.json) y [firmas completas anteriores](datos/seis_sillas_antes.json).

Original conservado: `Miranda_Puente_Sutherland_PBR_Manual_01.blend`, 65.805.452 bytes. Su SHA-256 antes y después coincide; el valor completo consta en el manifiesto y la validación. No se ha exportado a Unreal, ni realizado commits, PR, publicaciones o cambios remotos.

## Silla maestra y alcance

La maestra es el puesto lateral de **X positivo, Y = −5,51422 m**, con origen de referencia **(4,6803799; −5,5142207; aproximadamente 0) m**. El objeto de referencia es `Mesh.589_0.002` (asiento). Está organizada en `SS_Sillas_Operativas_Seis_01 / P01_Maestra_Xpos_Y-5.51422`.

El conjunto contiene **16 objetos de malla**: 14 piezas originales de silla, el cilindro adaptado y la plataforma instalada. La descripción de las piezas se basa en su geometría; los nombres importados no son semánticos.

| Objetos maestros | Identificación geométrica |
| --- | --- |
| `Mesh.589_0.002` | Tapicería del asiento |
| `Mesh.591_0.002` | Respaldo tapizado |
| `Mesh.588_0.002`, `Mesh.600_0.002` | Reposabrazos tapizados |
| `Mesh.598_0.002`, `Mesh.601_0.002` | Soportes inclinados de los reposabrazos |
| `Mesh.592_0.002`, `Mesh.596_0.002` | Travesaños de la estructura |
| `Mesh.590_0.002`, `Mesh.593_0.002`, `Mesh.597_0.002`, `Mesh.599_0.002` | Remates/articulaciones de la estructura |
| `Mesh.594_0.002` | Tramo interior del soporte central |
| `Mesh.602_0.002` | Montaje bajo el asiento |
| `Cilindro` | Pie cilíndrico adaptado: Ø 0,132 m, altura 0,494 m |
| `Floor_aiWireframe1_0` | Plataforma instalada: 0,750 × 0,500 × 0,030 m; incluye las ranuras/guías modeladas |

No se identificaron controles como objetos independientes adicionales en este conjunto. Toda la geometría y las asignaciones de materiales de las 14 piezas, incluidos posibles detalles integrados, se conservaron sin reinterpretarlas.

Se conservaron los 14 nodos vacíos de las piezas y el nodo `Floor` de la plataforma. Cada copia incluye esos nodos, las 16 mallas y un nuevo vacío de agrupación. No se copiaron cámaras, luces, consolas ni ancestros comunes del puente. Las copias usan los mismos bloques de geometría y materiales que la maestra, manteniendo UV, normales, atributos y relaciones internas; no se fusionaron objetos ni se aplicaron transformaciones a las mallas.

## Puestos replicados

Las coordenadas son los orígenes de referencia de cada puesto, en metros de mundo. La orientación se obtuvo de las matrices de cada silla existente, comprobando escala y signo del determinante. Los valores de giro son relativos a la maestra, alrededor de Z mundial.

| Puesto / colección nueva | Referencia original | X (m) | Y (m) | Giro relativo | Pie y plataforma |
| --- | --- | ---: | ---: | ---: | --- |
| P01 — maestra | `Mesh.589_0.002` | 4,68038 | −5,51422 | 0° | Sí |
| `P02_Xpos_Y-3.72934` | `Mesh.589_0.001` | 4,68038 | −3,72934 | 0° | Sí |
| `P03_Xpos_Y-1.73943` | `Mesh.589_0` | 4,68038 | −1,73943 | 0° | Sí |
| `P04_Xneg_Y-1.80778` | `Mesh.589_0.003` | −4,69025 | −1,80778 | ≈180° | Sí |
| `P05_Xneg_Y-3.59266` | `Mesh.589_0.004` | −4,69026 | −3,59266 | ≈180° | Sí |
| `P06_Xneg_Y-5.58256` | `Mesh.589_0.005` | −4,69026 | −5,58256 | ≈180° | Sí |

Se mantuvieron las pequeñas diferencias entre las posiciones existentes. No se impuso una distribución simétrica ni una orientación común a los seis puestos. Los giros del lado X negativo son −179,999986° en las matrices calculadas. Los orígenes Z originales son inferiores a una micra, consecuencia de la transformación de importación, y se respetaron.

## Ajuste de apoyo e incidencias resueltas

1. **Pie manual bajo el suelo.** El cilindro original alcanzaba Z = −0,01367469 m. En el archivo de resultado se trasladó únicamente `Cilindro` **+0,03923373 m en Z**, sin alterar su altura, escala, malla, material ni la altura del asiento. Su base quedó en Z ≈ 0,02555904 m, sobre la superficie real de la plataforma medida por rayo en el eje del pie. Este mismo ajuste está en los seis conjuntos. La matriz anterior y la nueva constan en el manifiesto; es reversible. El cilindro conserva el solape de montaje con el soporte interior de la silla.
2. **Raíles importados sin colocar.** Los dos objetos `FloorRail01_aiWireframe1_0` y `FloorRail02_aiWireframe1_0` estaban alrededor del origen mundial, no junto a la plataforma instalada. Tras la instrucción expresa del usuario se eliminaron del resultado, junto con sus mallas exclusivas y los vacíos exclusivos `FloorRail01` y `FloorRail02`. Se conservaron los materiales compartidos y el resto de la jerarquía importada. El archivo original no se modificó. La plataforma de cada silla conserva sus propias guías/ranuras modeladas; no hay otros dos raíles externos añadidos a cada conjunto.

## Conservación y recuperación de las sillas anteriores

Las otras cinco sillas originales permanecen completas: **80 mallas y sus 80 vacíos**, sin eliminar su pie antiguo, modificar su geometría o cambiar sus transformaciones base. Se trasladaron únicamente de colección. Están en **`SS_Originales_5_Recuperables`**, con una subcolección `Original_P02…` a `Original_P06…` por puesto, desactivadas mediante la colección superior tanto en viewport como en render.

Para recuperar las cinco: desactivar en viewport y render las colecciones nuevas P02–P06 y activar en ambos modos `SS_Originales_5_Recuperables`. Para recuperar solo una, ocultar primero las otras cuatro subcolecciones originales, activar la colección superior y ocultar la réplica del puesto correspondiente. La maestra P01 puede seguir visible. Al habilitar las originales, Blender vuelve a evaluar su jerarquía; la validación ha comprobado sus matrices después de hacerlo temporalmente, sin guardar cambios de visibilidad.

## Validación

- Archivo reabierto en un proceso independiente de Blender. Resultado: **513 objetos**, frente a 357 al inicio: +160 objetos nuevos, −4 objetos de los raíles autorizados.
- Los seis conjuntos tienen **16 mallas** cada uno y dimensiones de envolvente en mundo de aproximadamente **0,946759 × 1,075996 × 1,511494 m**. La comparación de las dimensiones de cada pieza con la maestra pasa con tolerancia de 0,00002 m; las pequeñas diferencias de envolvente entre lados son inferiores a una micra.
- Correspondencia de matrices verificada contra la transformación rígida de cada puesto, con tolerancia de 0,00002 por elemento. Jerarquías de las réplicas comprobadas. No hay escalados de las sillas para adaptarlas a los puestos.
- Geometría, UV, normales, atributos y asignaciones de materiales de **todas las mallas conservadas** coinciden con las firmas previas. Las únicas mallas eliminadas son las de los dos raíles autorizados.
- Todos los grafos de materiales y todas las imágenes conservan sus firmas previas. Las rutas de imágenes no cambian, no hay imágenes externas de archivo faltantes y el resultado se guarda junto al original para mantener las referencias relativas.
- Los objetos ajenos a las sillas y a los dos raíles eliminados conservan sus propiedades auditadas: matrices, geometría, materiales, jerarquías, modificadores y visibilidad. Las colecciones originales solo pierden los objetos reorganizados o eliminados expresamente. Se conservan cámara, mundo, motor de render y unidades de escena.
- Rayos al suelo bajo las cuatro esquinas de cada plataforma y el eje de cada pie: apoyo a nivel de suelo, con desviación numérica máxima inferior a **0,0000001 m**. No hay penetración significativa. Los contactos coplanares con el suelo se registran por separado con tolerancia de 0,00002 m.
- Distancia vertical entre la base del cilindro y la superficie de la plataforma en su eje: **0 a 0,00000003 m** en los seis puestos.
- Comprobación BVH de superficies evaluadas contra las mallas visibles del escenario: **sin intersecciones detectadas**, salvo los contactos de apoyo con el suelo dentro de la tolerancia. Revisión visual de ambos lados del puente, sin cruces evidentes con las consolas. Los solapes internos de montaje entre componentes de silla se excluyen de esa comprobación.

La comprobación de superficies no sustituye las futuras pruebas de ergonomía, ocupación corporal o colisiones de juego. Estas siguen pendientes con Quinn en UE5, tal como estaba previsto. No queda ninguna colocación insegura pendiente en Blender; la valoración visual del ajuste del cilindro y de las guías de la plataforma puede hacerse sobre las vistas adjuntas.

## Vistas y reproducción

- [Lado X positivo, geometría](capturas/seis_sillas/Seis_Sillas_01_lateral_Xpos.png).
- [Lado X negativo, geometría](capturas/seis_sillas/Seis_Sillas_01_lateral_Xneg.png).
- [Conjunto maestro aislado](capturas/seis_sillas/Seis_Sillas_01_maestra.png).
- [Lado X positivo, materiales PBR](capturas/seis_sillas/Seis_Sillas_01_PBR_Xpos.png).
- [Lado X negativo, materiales PBR](capturas/seis_sillas/Seis_Sillas_01_PBR_Xneg.png).

Las vistas se generan con `seis_sillas_vistas.py`; sus cámaras, iluminación de presentación y ajustes de render son temporales y no se guardan en el `.blend` entregado.

El script de reproducción abre el original y se niega a sobrescribir un resultado existente. Para repetir en otra ubicación, mantener la misma estructura de carpetas y las dependencias de scripts indicadas, o ajustar las constantes `ROOT`, `ORIGINAL` y `OUTPUT` de `seis_sillas_comun.py`. Ejemplo PowerShell desde este repositorio:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --disable-autoexec `
  'juego\Clase Miranda\puente\blender\Miranda_Puente_Sutherland_PBR_Manual_01.blend' `
  --python 'juego\Clase Miranda\puente\analisis_dimensional\scripts\seis_sillas_replicar.py'
```

La validación independiente usa el archivo de resultado con `--python` apuntando a `seis_sillas_verificar.py`. No guarda el archivo. El original, el manifiesto y las firmas previas deben estar disponibles.
