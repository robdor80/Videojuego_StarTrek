# VOY-03 — Resumen ejecutivo

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

## Cierre: COMPLETADA

Los recorridos geométricos objetivo están validados sobre la geometría original **de trabajo de VOY-02**, sin reparación arquitectónica. Opción A recomendada. Se ha conservado la orientación de importación +90° X y la escala experimental 1,10. «Original de trabajo» incluye las puertas en su pose estática abierta y los adaptadores experimentales existentes de VOY-02; no significa OBJ sin preparar ni versión definitiva para producción.

Hay **39 casos finales positivos**: 13 trayectorias × alturas 1,60 / 1,75 / 1,90 m, radio constante 0,35 m. Incluyen las seis rutas exigidas, tres vuelos de escalera, los dos recorridos completos y dos regresiones. Se verificaron 48,090 poses y 48,051 intervalos barridos. Los recorridos inversos comparten el mismo volumen barrido y apoyo con criterio simétrico de subida/bajada; no se cuentan como otros 39 experimentos independientes.

## Respuestas a los diez criterios de cierre

1. **Causa de la desconexión:** el algoritmo anterior mantenía el pie de la cápsula sobre el suelo bajo su centro, sin resolver su paso por narices y contrahuellas. La selección de suelos por material omitía apoyos reales y admitía una consola. La rejilla y las diagonales añadían falsos bloqueos y un cruce real. No había prueba de imposibilidad física del puente.
2. **Geometría original transitable:** sí, en los recorridos y poses documentados. No se han movido, borrado ni reconstruido piezas. No se certifica cada punto de la planta.
3. **Superficies problemáticas:** las escaleras son compuestas; marcos, rejillas y remates no están todos en una sola malla. Hay normales invertidas, bordes abiertos y coincidencias que exigen colisiones futuras cuidadosas. Las escaleras laterales ofrecen tres ascensos de aproximadamente 15,20 cm y huellas de 24,3–24,5 cm, no un salto directo de 30–45 cm.
4. **Tres alturas y continuidad:** sí. Cápsula completa contra mallas, barridos de intervalos y apoyo continuo sobre triángulos reales. El peor cambio vertical entre muestras de la ruta centro–pasarela es aproximadamente 1,27 cm, conectado por un segmento probado; no hay teleportación.
5. **Solución que funciona:** opción A, interpretación física de apoyos y búsqueda con rechazo de aristas incorrectas. Se conservan candidatos fallidos, incluido un atajo de esquina con apoyo lateral inválido.
6. **Mejor conservación visual:** opción A; diferencia de arquitectura y transformaciones respecto a referencia = cero. B–E no se ejecutaron porque A cumplió los objetivos.
7. **Centro a turbolift y camarote:** sí, aproximadamente 31,54 m y 35,54 m, tres alturas, conexión y adaptadores existentes reutilizados. Puertas estáticamente abiertas; sus mecanismos siguen fuera del alcance.
8. **Regresiones de VOY-02:** los dos itinerarios de pasarela/red posterior a sus destinos vuelven a superar los ensayos geométricos para las tres alturas.
9. **Pendiente en Unreal:** colisiones importadas, CharacterMovement real, subir/bajar, giro con cuerpo/animación, contactos de narices, puertas dinámicas y NavMesh. No se ha abierto Unreal ni se declara validación en el motor.
10. **Paso a VOY-04:** la circulación geométrica del alcance está suficientemente resuelta para planificar la siguiente fase. La escala sigue provisional y la naturalidad de marcha requiere personaje y movimiento reales. VOY-04 no se ha iniciado y requiere autorización.

## Límites que acompañan al aprobado

Se acredita viabilidad geométrica de una cápsula ambulante, no simulación biomecánica, certificación normativa, accesibilidad en silla de ruedas ni funcionamiento de asientos. Las rutas de mando terminan cerca de los sillones y navegación en un acceso junto al asiento, no sentadas. Las trayectorias son polilíneas verificables, no animaciones terminadas ni caminos optimizados. La separación de unos 4 mm de las mallas es una tolerancia de contacto geométrico; la futura colisión debe contrastarse de nuevo.

El archivo Blender final contiene cuatro escenas y comparte las 645 piezas de referencia. Se reabrió y contrastó: máximo residual numérico 11.444 µm con tolerancia explícita de 20 µm; las huellas de vértices, caras y matrices coinciden exactamente con las copias de origen. La integridad protegida final se detalla en `DATOS/integridad_final.json`.

Entregables: nueve informes, escenas en `ESCENAS/VOY03_Circulacion.blend`, datos completos, scripts, registros, capturas originales y finales, láminas y ZIP verificado. Véase [README](README.md).
