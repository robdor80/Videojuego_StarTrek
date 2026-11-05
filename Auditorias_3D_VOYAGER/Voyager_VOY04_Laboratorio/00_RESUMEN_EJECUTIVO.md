# VOY-04 — Resumen ejecutivo

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Cierre: COMPLETADA CON RESERVAS

El laboratorio demuestra un recorrido cinemático **muestreado** de entrada, sentado, trabajo, levantado, salida y retorno de la silla para 1,60 / 1,75 / 1,90 m, en una copia adaptada del puesto delantero de navegación. No acredita que el conjunto original ya sea ergonómico o móvil, ni una simulación biomecánica. La arquitectura y la consola se conservan. Quedan problemas concretos de respaldo, mirada, marcha y mecánica del soporte.

Se inventariaron cinco asientos y 92 piezas de silla: navegación 8, laterales 31 + 31, mando 11 + 11. La base común de mando Mesh_2093 pertenece al contexto fijo. El OBJ aporta 630 objetos; la referencia de VOY-03 reúne 645 piezas con su contexto/adaptadores. Operaciones no se identifica como una sexta silla.

### Respuestas a los doce criterios de cierre

1. **Asientos reales:** dos sillones de mando y tres sillas de estación. Por posición y comparación contextual: capitán a babor, primer oficial a estribor, CONN delante, ciencia e ingeniería en los laterales bajos. Operaciones y Táctica son puestos posteriores de pie. La asignación al modelo es una inferencia de su proa hacia −Y; los nombres históricos IZQ/DER son de coordenadas, no navales. [Referencia contextual primaria](https://roddenberry.x.io/2371-uss-voyager-ncc-74656/).
2. **Piloto:** navegación, con ocho piezas separadas, sin reposabrazos, pedestal y dos superficies LCARS principales independientes. Permite investigar un problema real de piernas sin reconstruir la consola.
3. **Geometría móvil:** sí, con jerarquía, pivotes corregidos y mallas independientes. El OBJ no contiene una guía funcional acreditada. El prototipo incorpora carro/guía nuevos y reconstruye localmente la longitud del casquillo inferior; no se presenta como mecanismo original descubierto.
4. **Aproximación:** geométricamente positiva en la traslación lateral cercana ensayada, con silla retirada y elevación del pie sobre la guía. El maniquí empieza ya alineado. No es marcha terminada ni prueba de giros desde cualquier rumbo.
5. **Sentado:** positivo en la copia con altura ajustada y pies en suelo. La pose original conserva fallos de borde/rodilla y pies elevados. La espalda queda sin apoyo suficiente incluso tras avanzar el respaldo 18 cm.
6. **Trabajo:** ambas manos alcanzan puntos interiores de Plane_94/95, con envolvente de contacto a 2 mm de la superficie; sus centros son visibles desde los ojos estimados. El ángulo descendente llega a 48,2° en 1,90 m. No se valida comodidad prolongada, lectura completa, dedos o uso de toda la consola.
7. **Levantado y salida:** recorrido inverso muestreado positivo; silla vuelve a su referencia horizontal. El asiento queda en la regulación de altura de cada usuario. No se afirma marcha física o estabilidad del cuerpo.
8. **Tres alturas:** no se cambió la talla para hacerlas pasar. Se modificó la altura del asiento, manteniendo constantes las longitudes de cada maniquí.
9. **Modificaciones:** descenso 14,13–21,54 cm, avance de respaldo 18 cm, casquillo inferior ajustado, guía fija y carro nuevos, retirada común 40 cm y trayectorias específicas de pies/manos. El ajuste de respaldo aún es insuficiente. No se movió ni recortó la consola en el prototipo guardado.
10. **Otros asientos:** comparten metodología, pero siguen E por ergonomía completa pendiente. Navegación original recibe C por intervención importante. Ningún asiento se promueve a A.
11. **Unreal:** faltan colisiones, retarget y animación real, validación física/marcha, ocupación/reservas/NPC, persistencia y la futura interfaz. Se entregan anclajes y cámaras sin implementar sistemas.
12. **Aceptación técnica:** preparada para revisión y aceptación **con reservas** del laboratorio; no para aprobar ergonomía definitiva, mecanismo de producción o integración jugable.

| Altura humana | Descenso del asiento | Asiento sobre suelo de pies | Retirada | Distancia tronco–respaldo | Mirada descendente al centro |
| --- | --- | --- | --- | --- | --- |
| 1.60 m | 21.54 cm | 39.12 cm | 40 cm | 7.59 cm | 30.6° |
| 1.75 m | 17.83 cm | 42.82 cm | 40 cm | 6.72 cm | 40.4° |
| 1.90 m | 14.13 cm | 46.53 cm | 40 cm | 5.84 cm | 48.2° |

## Evidencia y conservación

Se contrastaron 301 poses + 300 subfotogramas por altura: **1803 posiciones** de la animación guardada. No hubo penetraciones principales por encima del umbral de 2 mm del proxy. El error máximo de ejes de rig fue 1.30 µm. La silla adaptada pasó 81 posiciones por altura, cada 5 mm, sin contactos externos; se distingue su interfaz carro–guía. Estos resultados no son un barrido continuo certificado.

Las 1184 copias de malla verificadas conservan UV, asignaciones de material y datos independientes; error de vértices esperado máximo 2.14 µm. La escena de referencia está intacta. Los fallos A1 (pie/guía) y A3 (manos/canto) están conservados en datos, renders y otro Blender.

La relectura SHA-256 de **3634 archivos protegidos** no detectó cambios, bajas o altas dentro de los árboles registrados. No se abrió Unreal ni se realizaron escrituras en GitHub. La comprobación no pretende ser un inventario de todo el disco.

![Antes/después real](CAPTURAS/LAMINA_ANTES_DESPUES.png)

Escena principal: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY04_Laboratorio\ESCENAS\VOY04_Laboratorio.blend`. Escenas de fallo: `%USERPROFILE%\Documents\Auditorias_3D\Voyager_VOY04_Laboratorio\ESCENAS\VOY04_Fallos_y_Comparativa.blend`. [Secuencia animada](ANIMACIONES/VOY04_Ciclo_175.gif). [Paquete documental](PAQUETE/VOY04_Entrega.zip). VOY-04 termina aquí; VOY-05 no se inicia.
