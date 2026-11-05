# VOY-04 — Metodología, reproducibilidad y límites

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Fuentes y aislamiento

Se identificaron y leyeron VOY-02/03 en sus rutas reales y el informe F07-CHAIR-01. Se copió `VOY03_Circulacion.blend` a `REFERENCIAS`, sin guardar sobre el origen. `baseline.json` registró SHA-256, tamaños y mtimes antes de crear experimentos. La relectura final conserva 3634 archivos; `integridad_final.json` detalla el alcance y todos los hashes.

Todas las escrituras de artefactos del laboratorio se dirigen a `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY04_Laboratorio`. Los proyectos Unreal no se abrieron; no hubo escrituras ni comandos remotos de GitHub. La carpeta de trabajo Git solo mostraba `.codex-remote-attachments/` sin seguimiento; no se hizo commit. No se afirma un hash de CoreRPG/Valhalla o de todo el equipo, cuyos proyectos no se abrieron ni editaron.

La referencia contiene 645 piezas, incluidas 630 del OBJ y contexto heredado. Cada escena de trabajo copia sus objetos y **datos de malla**, compensando padres al conservar matrices mundiales. No se modifican mallas compartidas de VOY-03. 1184 copias contrastadas: UV/asignaciones iguales y mallas con un único usuario. El error máximo esperado de vértices fue 2.14 µm, por redondeo de coma flotante. Los 49 recursos de imagen se mantienen empaquetados.

## Cálculo geométrico

Se exportan vértices, triángulos e identidad de objeto del Blender real, transformados a metros del marco puente. Se miden superficies mediante rayos, extremos locales y ajuste SVD de planos. La geometría de cada silla se mide en Voyager; los números de Sutherland no intervienen en sus cotas o carreras. La escala arquitectónica 1,10 sigue siendo una hipótesis heredada, no una unidad original certificada.

La distancia segmento–triángulo se calcula con proyección, aristas y cruce del plano. Al restar el radio se obtiene la separación de cada cápsula corporal. Las superficies se consideran a doble cara. Se usa umbral de penetración principal de 2 mm; eso no significa que los pequeños contactos negativos sean físicamente aceptables. No se excluyen globalmente el asiento, las piernas o la consola. Los volúmenes contiguos del maniquí se solapan intencionadamente para formar articulaciones: no se interpreta su unión como autocolisión física.

La silla usa BVH para candidatos y SAT de 17 ejes para contactos de triángulos, con tolerancia de separación de 1 µm y test transversal de 10 µm. Contacto, coplanaridad y cruce transversal no son automáticamente volumen penetrado. El contacto carro–guía se conserva por separado como interfaz propuesta. Los contactos originales entre piezas se registran, no se borran.

La topología diagnóstica suelda puntos a 10 µm en memoria y cuenta bordes abiertos/no manifold; **no repara** el recurso. Una cápsula completamente contenida en un sólido cerrado exigiría además pertenencia volumétrica. Muchas piezas originales son abiertas/no manifold (Object_129 incluido), por lo que no se certifica un interior sólido ni ausencia universal de penetración por un resultado de superficies. Los recorridos parten de un estado exterior conocido y se inspeccionan visualmente; la certificación física queda pendiente.

## Muestreo, rig y límites

301 frames y 300 puntos medios por talla, más 81 posiciones de silla por talla, no son un barrido continuo. No se han probado todos los caminos, todas las tallas intermedias, todos los puntos LCARS o giros desde cualquier rumbo. La vuelta simétrica no duplica la independencia del ensayo. Se verifican ejes del rig reabierto con máximo error 1.30 µm; la cápsula analítica es una envolvente conservadora del polígono renderizado.

No hay fuerzas, equilibrio, peso, fricción, masas, presión sobre cojines, biomecánica, ropa, dedos o animación final de marcha. Los huesos rígidos conservan sus longitudes; la altura corporal no cambia de forma arbitraria. La traslación guiada no sustituye una prueba de locomoción. Los rayos de mirada solo acreditan dos centros de pantalla, no lectura o visibilidad completa.

Las capturas son renders de Blender. Las secciones E/D recortan copias **solo para visualización** y las comparativas aíslan el entorno. Las colisiones y la escena principal usan la consola completa. Las láminas solo reordenan y rotulan renders existentes; GIF/WebP reúnen los PNG sin alterar posiciones. No se generó ninguna evidencia con IA ni se ocultaron los ensayos fallidos de los datos.

## Reproducción

Conservar esta entrega. Para repetir, usar otra carpeta/copia, nunca ejecutar el aislamiento encima de un laboratorio protegido. Blender instalado: `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`. Su Python con NumPy: `5.2\python\bin\python.exe`. El script 16 usa Python local con Pillow únicamente para ensamblar renders y verificar archivos.

Orden de reconstrucción final: 00 (nueva baseline y copias), 01 (Blender: extracción/renders), 02–04 (medidas y búsqueda), 06 (búsqueda de retiradas), 07 (trayectoria final), 08 (Blender/escenas/renders), 09 (Blender/SAT/topología), 10 (Blender/recarga), 11 y 14 (métricas), 12–13 (Blender/anclajes/evidencias), 15 (Blender/contactos internos), 16 (láminas/integridad), 18a (Blender/imágenes empaquetadas), 20 (píxeles y animación), 17 (informes), 18 (paquete). Repetir 10 tras añadir anclajes, como en la entrega. El script 19 regenera solo la exportación visual si se necesita; 08 ya incluye la corrección de escena activa.

07b/07c/07d documentan correcciones históricas y no son necesarios en una reconstrucción limpia con la función final de 06. Los JSON A1/A3 suministrados son entradas de reproducción de fallos para 12; conservan todas las poses rechazadas. No renombrar un ensayo nuevo como esos históricos. 00 y los archivadores históricos tienen guardas contra sobrescritura. El paquete contiene geometría numérica y scripts; los .blend de referencia/final quedan en el MSI y sus rutas están en README y manifiestos.
