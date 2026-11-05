# VOY-02 — Conexión puente–pasillos y acceso central
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

## Configuración comprobada
Se usa el acceso posterior, a factor de puente 1,10. La traslación exacta es `[-1.3102440953254701, -7.020256090164185, -0.7835251118119737]` m, para llevar su umbral al origen. La biblioteca modular mantiene su escala numérica 1. Las tres parejas completas de hojas están desplazadas a apertura estática, nunca ocultadas para superar cápsulas. Los giros y colocaciones precisos están en `prototipo_conjunto.json` y `matrices_instancias.json`.

La red contiene Mesh13 (recto principal), Mesh38 (cruce), Mesh37 (acceso turbo), Mesh17 (cabina), Mesh18 (ramal camarote) y Mesh4 (envolvente). Hay seis adaptadores nuevos, independientes y naranjas:

| Adaptador | Longitud m | Anchura libre inicio→fin m | Altura libre inicio→fin m |
| --- | --- | --- | --- |
| AD_PUENTE | 1.40 | 0.820 → 3.181 | 1.950 → 2.816 |
| AD_CRUCE | 0.60 | 3.181 → 2.961 | 2.816 → 2.816 |
| AD_RAMAL_TURBO | 0.60 | 2.961 → 3.181 | 2.816 → 2.816 |
| AD_GARGANTA_TURBO | 0.65 | 1.571 → 1.149 | 2.100 → 2.100 |
| AD_RAMAL_CAMAROTE | 0.60 | 2.961 → 3.181 | 2.816 → 2.816 |
| AD_CAMAROTE | 1.40 | 3.181 → 1.080 | 2.816 → 2.100 |

Suelo/techo de diagnóstico de 60 mm y paredes de 80 mm; no son restauración final ni especificación constructiva de la nave. Los verdes son tres obstáculos de mobiliario de referencia.

## Revisión de encuentros y corrección R1
Se revisaron los seis adaptadores contra todos los triángulos próximos del prototipo mediante BVH/SAT. Se conservan contactos de borde, coplanares y cruces transversales por separado en `encuentros_adaptadores.json`. En la primera revisión, AD_PUENTE intersectaba hojas completas ya abiertas, en particular Mesh_1979/1987 y sus remates; el suelo seguía siendo transitable por el centro, pero no era un encuentro correcto.

R1 conserva el suelo desde Y=0 y retranquea paredes/techo hasta **Y=+0,14 m**. Las hojas llegan aproximadamente hasta Y=+0,02338 m y el marco fijo hasta ~+0,135 m. No se cambia ni una hoja ni el puente fuente. La revisión elimina los cruces transversales de AD_PUENTE con las hojas en esa pose, conservando el diagnóstico anterior en `TRASPASO/ANTES_RETRANQUEO_*`. Queda una junta constructiva nominal de unos 5 mm y acabados por resolver. El adaptador sigue siendo C; no se declara recinto estanco ni bolsillo funcional. No se desactivaron colisiones o superficies para aparentar paso.

## Recorridos positivos
Después de R1 se repitieron únicamente las rutas afectadas del conjunto:

| Ruta: inicio real en pasarela posterior | Poses por H | H m | Colisión muestreada | Soporte cinco rayos |
| --- | --- | --- | --- | --- |
| PUENTE_AL_TURBOLIFT | 948 | 1,60 / 1,75 / 1,90 | libre | correcto |
| PUENTE_AL_CAMAROTE | 1110 | 1,60 / 1,75 / 1,90 | libre | correcto |

Muestras ≤25 mm, r=0,35 m, margen 12,5 mm. El soporte se comprueba cada 50 mm. Se ensayan triángulos del puente, módulos, adaptadores y tres muebles. Los archivos JSON incluyen todos los puntos, radios, alturas y límites; un mínimo `null` sin candidatos no es una holgura infinita.

## Acceso desde el centro: resultado negativo conservado
El ensayo nuevo utiliza rejilla de 0,10 m reales, con inicios/destinos fijos y ajustes máximos de 0,20 m. Los ajustes encontrados son solo 30 mm desde el centro, 40 mm desde navegación, 50 mm desde pasarela y ~16 mm en la salida. H=1,60 y 1,90 m, r=0,35 m: no se encuentra ruta centro→posterior ni navegación→posterior. Se obtienen 5770 y 5767 nodos libres, respectivamente, repartidos en componentes.

La separación mínima entre componentes de centro y posterior es ~0,838 m en 3D; el diagnóstico recto cruza Mesh_1755, Mesh_1859, Mesh_1892, Mesh_1915, Object_119 y remates. Desde navegación, la separación entre componentes es ~0,926 m y el diagnóstico encuentra Mesh_1739/Mesh_1861, entre otros obstáculos. Estos son lugares de investigación, no puentes virtuales que el personaje pueda saltar. Los cambios de altura observados y la capacidad de subir peldaños requieren un solver apropiado.

La rejilla permite optimistamente diferencias de nivel ≤0,31 m entre vecinos, pero no simula un escalón. Su ruta nueva pasarela→posterior falla un margen refinado junto a `hallwaysupports_3` (~10,50 mm frente a 12,50 mm exigidos). Se conserva ese fallo; no invalida ni sustituye la ruta anterior distinta de pasarela que sí pasó y se utilizó en el conjunto. Una búsqueda finita negativa tampoco demuestra inexistencia absoluta de ruta geométrica o de una solución con cambios locales.

**Grado E para acceso jugable desde el centro y circulación integral. C para el prototipo conectado parcial.** El siguiente paso técnico es caracterizar/subir los cambios de nivel y despejar rutas mediante intervenciones visibles y justificadas, sin reducir cápsula ni esconder arquitectura.

## Contraste de escena guardada
El contraste final cubre los 645 componentes de G, con triángulos en mundo, correspondencia de centroides y permutaciones de vértices; para las tres cajas nuevas se admite distinta diagonal coplanar mediante distancia bidireccional de superficie. Tolerancia de 20 µm, error máximo ~11,44 µm por cancelación float32 en módulo nativo lejano. El diagnóstico más estricto de 10 µm se conserva. El umbral de 20 µm es 625 veces menor que el margen de cápsula, se declara expresamente y no altera ningún baseline.

![Acceso central](LAMINAS/L01_acceso_central.png)
Evidencias: `acceso_central_revision.json`, `contraste_blend.json`, `encuentros_adaptadores.json`, `retranqueo_adaptador.json`, logs 14/17/22/24 y capturas C/G. La escena no prueba CharacterMovement, NavMesh, ascensor, concurrencia ni NPC.
