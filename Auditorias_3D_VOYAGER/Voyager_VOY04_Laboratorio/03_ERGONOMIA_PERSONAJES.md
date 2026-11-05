# VOY-04 — Ergonomía con personajes articulados

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Referencias humanas

La búsqueda por nombres de recursos humanos/rigs en los assets locales del proyecto y la inspección de la escena VOY-03 no localizaron un personaje reutilizable adecuado. Se documenta el alcance en `busqueda_rigs_locales.txt`; un resultado vacío no demuestra ausencia de cualquier recurso en todo el disco. No se abrieron proyectos Unreal para buscar sus maniquíes. Se construyeron tres rigs sencillos de laboratorio de **18 huesos** y cápsulas rígidas articuladas, con pesos 1:1 mediante Armature modifier.

Las alturas nominales son 1,60 / 1,75 / 1,90 m. Se usa cadera de pie a 0,53H, cabeza a +0,407H con radio 0,063H: el máximo vertical nominal es H. Fémur/tibia: 0,245H cada uno; húmero 0,186H; antebrazo 0,146H; hombro +0,288H sobre cadera. Radios muslo/pantorrilla: 0,043H/0,029H; pelvis semiancho 0,055H. Pies con radio 0,027H y eje 0,105H. Son proporciones razonables de un proxy documentado, **no percentiles antropométricos ni certificación normativa**. El JSON `proporciones_maniqui.json` recoge todos los parámetros.

La IK analítica mantiene longitudes y resuelve codos y rodillas. Los huesos son independientes y rígidos, sin piel, dedos, masa, ropa o deformación del cojín. No se escala un maniquí durante una prueba para hacerle pasar. Las cápsulas analíticas envuelven las superficies poligonales renderizadas.

## Postura original y adaptación

La pose original con muslos horizontales y cadera retrasada conserva interferencias de pantorrilla con el borde del asiento; adelantar el cuerpo puede invadir Object_129. Los pies quedan aproximadamente 16,4–23,8 cm por encima del plano bajo el pedestal en ese ensayo. No se acepta esa pose como éxito. Los archivos `original_1.xx.json` incluyen los triángulos testigo.

| Altura humana | Descenso del asiento | Asiento sobre suelo de pies | Retirada | Distancia tronco–respaldo | Mirada descendente al centro |
| --- | --- | --- | --- | --- | --- |
| 1.60 m | 21.54 cm | 39.12 cm | 40 cm | 7.59 cm | 30.6° |
| 1.75 m | 17.83 cm | 42.82 cm | 40 cm | 6.72 cm | 40.4° |
| 1.90 m | 14.13 cm | 46.53 cm | 40 cm | 5.84 cm | 48.2° |

Las posturas adaptadas ponen los pies a Z=0,023326 m sobre Mesh_1728, con seis rayos de apoyo por talla en la pose de trabajo de la animación reabierta. La cadera queda sobre el cojín; muslos horizontales, rodillas aproximadamente a 90° y piernas separadas según el ancho de pelvis. Los contactos por debajo de 2 mm se tratan como tolerancia del proxy, sin afirmar compresión física. No se excluyen globalmente la silla o la consola del chequeo.

| Talla | Holgura mínima pierna–carcasa de consola | Alcance hombro–mano | Flexión interior de codo | Visibilidad |
| --- | --- | --- | --- | --- |
| 1.60 m | 17.71 cm | 43.6–43.6 cm | 90.8–90.9° | Centros Plane_94/95 visibles |
| 1.75 m | 12.65 cm | 45.4–45.5 cm | 85.2–85.4° | Centros Plane_94/95 visibles |
| 1.90 m | 7.65 cm | 48.7–48.8 cm | 84.8–85.1° | Centros Plane_94/95 visibles |

Las holguras de la tabla se calculan contra Object_129/126/127, no son separación a todo el entorno ni profundidad volumétrica. Las manos terminan con su envolvente a 2 mm de cada pantalla; no se simulan dedos o presión. El arco de manos evita el canto que atravesaba la primera trayectoria directa. No se acredita alcanzar cualquier botón de las texturas.

## Reservas ergonómicas

El tronco mantiene 5,8–7,6 cm hasta el respaldo incluso tras adelantarlo. Es una postura posible sin apoyo dorsal completo, con comodidad prolongada pendiente. La mirada descendente estimada es de 30,6 / 40,4 / 48,2°: la talla alta necesita una revisión específica de cabeza, ojos y lectura, sin inferir un límite normativo. Solo se verificaron rayos a los centros, no campo visual completo u oclusión por manos.

No hay reposabrazos en este piloto. La cadera no rota anatómicamente y no se demuestra equilibrio durante sentarse. La aproximación lateral usa traslación guiada y un paso de elevación sobre la guía; no hay ciclo de marcha con apoyos alternados, fuerzas o transferencia de peso. El maniquí empieza orientado hacia la consola; otros giros y conexión exacta con las rutas VOY-03 quedan por contrastar. El resultado permite estudiar adaptación local, no aceptar ergonomía definitiva.

![Sección real adaptada](CAPTURAS/E_ADAPTADO_SECCION_1.75.png)
![Tallas](CAPTURAS/D03_COMPARACION_TRES_ALTURAS.png)
