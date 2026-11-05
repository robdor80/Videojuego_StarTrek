# VOY-04 — Comparativa y reutilización de procedimientos

22/10/2026 · Blender 5.2.2 LTS · escala arquitectónica 1,10 provisional · Unreal sin abrir.

[Índice](README.md) · [Galería](GALERIA.html) · [Límites](09_METODOLOGIA_LIMITACIONES.md)

## Criterio de clasificación

A exige geometría y ergonomía verificadas para el alcance completo. B admite ajustes menores ya identificados con evidencia suficiente. C necesita intervención importante. D recomienda reconstrucción. E indica evaluación insuficiente. Inventariar y medir no basta para asignar A/B a la ergonomía de una silla.

| Puesto | Familia/piezas | Altura original sobre referencia | Grado global | Motivo |
| --- | --- | --- | --- | --- |
| NAVEGACION | pedestal_8 / 8 | 0.630 m | C | Intervencion local: altura, apoyo, respaldo y mecanismo nuevo; prototipo muestreado positivo, ergonomia completa pendiente |
| LATERAL_DER | ruedas_31 / 31 | 0.599 m | E | Inventario y dimensiones, sin prueba articulada completa de entrada/trabajo/salida; no promover a A |
| LATERAL_IZQ | ruedas_31 / 31 | 0.599 m | E | Inventario y dimensiones, sin prueba articulada completa de entrada/trabajo/salida; no promover a A |
| MANDO_IZQ | mando_11 / 11 | 0.492 m | E | Inventario y dimensiones, sin prueba articulada completa de entrada/trabajo/salida; no promover a A |
| MANDO_DER | mando_11 / 11 | 0.492 m | E | Inventario y dimensiones, sin prueba articulada completa de entrada/trabajo/salida; no promover a A |

Navegación es C en su estado original: bajar 14–22 cm, modificar casquillo y crear guía/carro supera un ajuste menor. El prototipo adaptado pasa las muestras geométricas pero mantiene reservas de respaldo, mirada y marcha. No se presenta como A ni se recomienda reconstruir toda la silla o consola.

Las dos laterales tienen 31 piezas y familia visual común de asiento/respaldo, soporte y base de cinco radios con ruedas. Pueden reutilizar la organización, identificación de capas y maniquíes. Deben estudiar de nuevo rodadura/giro, apoyo de ruedas, alturas, orientación, proximidad lateral de consolas y recorrido. Su altura de casi 60 cm requiere atención; no se ha demostrado que el descenso del piloto o su carrera funcione allí.

Los dos sillones de mando comparten estructura visual y base común Mesh_2093, con 11 piezas de carcasa, cojines y reposabrazos por silla. La altura sobre suelo de pies ronda 49 cm, pero reposabrazos, acceso entre muebles y base compartida pueden exigir otra solución. No se inventa un reposabrazos abatible ni un asiento giratorio por tener objetos separados. Las plataformas no deben viajar con la silla sin estudio propio.

## Componentes reutilizables

Son reutilizables el medidor de geometría/UV, el cambio compensado de pivotes, los controles abstractos de traslación/altura/respaldo, el maniquí proporcional, la IK, los ensayos de distancia cápsula–triángulo, SAT, exportación JSON/CSV y contraste después de recarga. Los controles no deben implicar que todas las sillas necesitan los mismos grados de libertad.

Se reutiliza de Sutherland el aislamiento, separación base/grupo móvil, controles locales, conservación de UV, poses intermedias, retorno y recarga. Sus seis sillas tenían otra estructura y una carrera de 30 cm documentada; no acreditaban sentado. Voyager obtiene sus 40 cm de su propia serie. No se copió geometría, dimensión ni Blueprint de Sutherland.
