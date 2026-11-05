# VOY-02 — Resumen ejecutivo
**VOY-02 · cierre de evaluación técnica · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · UE 5.8.2 instalado, sin ejecutar.**

[Índice](README.md) · [Pruebas y límites](08_PRUEBAS_Y_LIMITACIONES.md) · [Galería](GALERIA.html)

La evaluación técnica se entrega cerrada con resultados positivos y negativos explícitos. Los recursos permiten plantear **un puente detallado, una red pequeña de pasillos, cabina y un camarote**, con adaptación importante. El prototipo no acredita todavía un puente enteramente transitable ni sistemas funcionales terminados. La prioridad siguiente es resolver circulación y puestos, antes del acabado artístico o la integración.

## Recuperación y conservación
Se leyeron íntegramente el prompt adjunto y los tres documentos de continuidad. El laboratorio real es `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY02_Laboratorio`. La comprobación previa confirmó 207/207 archivos iguales al inventario de parada, 115/115 entradas originales intactas, 106/106 copias concordantes y 59 archivos JSON/NPZ/PNG legibles. Las 33 capturas existían. No había procesos de laboratorio pendientes. Las rutas de fuentes y el entorno Blender/Unreal están accesibles; el nuevo chat trabaja sobre el mismo laboratorio. No se repitió `00_preparar.py`, ni se sustituyó el baseline.

La inspección reveló una incidencia que el traspaso dejaba abierta: **el `.blend` había perdido la base de importación del OBJ (+90° X)** al clonar sus objetos. Las superficies ensayadas numéricamente eran correctas, pero su representación guardada no lo era. Se repararon 630 datablocks compartidos exclusivamente en el laboratorio, con respaldo SHA-256 verificable. El contraste final de G abarca 645 componentes —630 OBJ, seis módulos, seis adaptadores y tres volúmenes de mobiliario— frente al NPZ. Error máximo 11.444 µm, tolerancia explícita 20 µm para aritmética float32. Hay ocho escenas útiles y 49 imágenes empaquetadas. La comprobación no guarda cambios.

## Resultados que condicionan el proyecto

| Área | Grado / confianza | Resultado |
| --- | --- | --- |
| Puente detallado como base de trabajo | C | Recuperable; escala y restauración local, circulación integral sin demostrar. |
| Escala global 1,10 | B / confianza media | Hipótesis arquitectónica provisional; no canon ni escala definitiva de todos los muebles. |
| Uniones de pasillos seleccionadas | B / C | Cápsulas y soporte pasan; perfiles discrepan, no hay uniones A. |
| Conexión posterior y red | C | Dos rutas geométricas parciales, adaptadores de diagnóstico y puertas abiertas estáticas. |
| Acceso desde centro/navegación | E | No aparece conexión en la búsqueda refinada; requiere estudio de escalones y obstáculos. |
| Mesh4 como base espacial de camarote | C | Habitable como maqueta; no dormitorio artístico/funcional final. |
| Puertas como mecanismos | C / funcionamiento E | Contactos investigados; bolsillos, barrido continuo y lógica no certificados. |
| Sillas y postura | C / ocupación E | Grupos corregidos y proxies; sin rig ni sentarse/levantarse validados. |
| 57 superficies planas independientes | A solo separabilidad | No acredita materiales emisivos, alcance, UI ni interacción. |
| PBR, iluminación y rendimiento UE | C / rendimiento E | Canales y presupuestos estudiados; sin perfil real. |
| Accesibilidad física continua | E | Giros locales no resuelven cambios de nivel ni rutas continuas. |

Las siete pruebas modulares mantienen sus resultados de cápsula y soporte para H=1,60/1,75/1,90 m y r=0,35 m. Las dos rutas del conjunto desde la pasarela posterior suman 948 y 1110 poses **por altura y por recorrido**, respectivamente. Tras corregir el adaptador se repitieron esas seis pruebas y su soporte. No son CharacterMovement ni NavMesh.

La rejilla nueva de 10 cm no conecta centro/navegación con la pasarela posterior, tanto para H=1,60 como 1,90 m. No se interpreta como prueba de imposibilidad absoluta. La alternativa nueva que la rejilla propone para la pasarela roza un soporte al refinar el margen; no reemplaza el recorrido previo que sí pasó.

Las puertas laterales cruzan superficies de cerramiento en fracciones intermedias. La posterior mantiene contactos de borde/tangencia, sin bolsillo probado. Se ensayaron desplazamientos normales y elevaciones pequeños: ninguno dejó todas sus poses libres de contactos. Además, el adaptador original cruzaba las hojas posteriores abiertas; se retranquearon **0,14 m** sus paredes/techo, manteniendo el suelo. La revisión elimina esos cruces transversales en la pose abierta, sin certificar el mecanismo.

## Qué se entrega y qué se conserva
Nueve informes, índice, galería, 33 capturas revisadas, cuatro láminas analíticas, hojas de contacto, tablas CSV/JSON, scripts y logs; ZIP local en `PAQUETE/VOY02_ENTREGA.zip`. El `.blend` y los NPZ geométricos permanecen fuera del ZIP; sus rutas figuran en el índice. El archivo principal es `ESCENAS/VOY02_Laboratorio.blend`.

Se preservan resultados antiguos, incluido el estado anterior a la corrección del OBJ, las capturas originales y los datos anteriores al retranqueo. Las revisiones y descartes se explican en el informe 08. No se modificaron modelos originales, Sutherland, parámetros del personaje o proyectos UE. No hubo instalación, integración, publicación, commit, fusión ni cambios en main.

## Siguiente decisión
Conservar 1,10 como referencia experimental mientras se resuelven escalones/accesos y se ajustan los puestos localmente. A continuación, prototipar una puerta completa con alojamiento físico, una estación sentada y una conexión terminada. Las decisiones artísticas corresponden al usuario; la hoja de ruta separa tareas Blender, pruebas UE futuras y sistemas del videojuego. El cierre de este laboratorio no inicia esas fases.
