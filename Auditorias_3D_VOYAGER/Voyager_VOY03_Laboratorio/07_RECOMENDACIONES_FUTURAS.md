# VOY-03 — Recomendaciones futuras

**VOY-03 · 21/10/2026 · MSI Raider · Blender 5.2.2 LTS · escala de puente 1,10 provisional · Unreal sin ejecutar.**

[Índice](README.md) · [Galería](GALERIA.html) · [Método](08_METODOLOGIA_Y_LIMITACIONES.md)

## Decisión recomendada

Conservar la arquitectura de los escalones. La opción A satisface la circulación geométrica del alcance con cero cambios de malla o posición. No hay fundamento en estos ensayos para rehacer el suelo completo, ampliar el puente, reducir la cápsula, eliminar barandillas o sustituir definitivamente la escalera por una rampa.

Mantener 1,10 como escala experimental documentada. Antes de decidir una escala final, contrastar el personaje, el uso de los puestos y las colisiones en una fase posterior autorizada. No utilizar el aprobado geométrico para dar por resuelta la ergonomía sentada de navegación o mando.

## Orden útil para una fase siguiente, sin iniciarla

1. Revisar conjuntamente las láminas y las escenas. Aceptar o ajustar los criterios de personaje, fidelidad y locomoción.
2. Preparar colisiones por función de pieza en una copia independiente, conservando los apoyos medidos y las narices. Revisar normales y no borrar coincidencias sin determinar su función.
3. Cuando se autorice un laboratorio UE, importar una muestra y repetir con CharacterMovement y colisión reales todas las rutas, subida y bajada. Dar prioridad a las aproximaciones oblicuas y al atajo negativo de esquina, que debe seguir rechazado.
4. Verificar acceso al asiento y postura sentada por separado, después puertas completas con alojamiento y ocupación. Esas tareas no se convirtieron en parte de VOY-03.
5. Solo después decidir restauración visual, interacciones/NPC y optimización basadas en pruebas de motor.

## Riesgos y asuntos secundarios anotados

Las huellas son compuestas y algunas caras apuntan hacia abajo. El detalle de rejilla y marco difiere 5,85 mm; el margen de colisión de la cápsula es milimétrico. Una colisión simplificada puede producir una regresión aunque parezca igual en pantalla. Las polilíneas verificadas no están suavizadas para animación ni circulación de múltiples agentes.

Persisten asuntos heredados fuera del alcance: ergonomía completa de puestos, carreras y bolsillos de puertas, uso real del camarote, materiales/PBR, parámetros de rendimiento e integración RPG. VOY-03 no los declara corregidos. Las puertas abiertas de la red son solo condiciones estáticas de estos ensayos.

La circulación ambulante medida no proporciona acceso sin escalones. La misión no evaluó silla de ruedas, cuerpo con equipamiento voluminoso, combate, evacuación ni cumplimiento normativo. Cualquier nuevo cuerpo o cambio de radio exige un experimento identificado, no sustituir esta referencia.

## Criterio para avanzar

**Sí hay base geométrica suficiente para planificar VOY-04**: seis rutas objetivo y conexiones completas resueltas sin alterar la identidad visual. Esto no es autorización ni ejecución de VOY-04. La misión se detiene al entregar el laboratorio y su ZIP; no hay integración Unreal, commit, PR, publicación ni inicio de la siguiente fase.
