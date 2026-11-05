# USS Enterprise-G · Clase Valhalla
## Distribución de salas por cubiertas

**Fecha:** 2 de noviembre de 2026  
**Estado:** Distribución conceptual de referencia, pendiente de ajuste dimensional en Blender  
**Ámbito:** Interiores jugables del proyecto *USS Enterprise-G*

---

## 1. Principio de diseño

La nave tendrá **dos grandes cubiertas circulares jugables** y **una tercera cubierta superior pequeña**, dedicada exclusivamente al puente principal y a la sala de observación.

La distribución se organiza para facilitar la jugabilidad y el trabajo de construcción, **sin exigir correspondencia geométrica exacta entre cada sala y su ubicación ficticia en el casco exterior**. No se crearán más cubiertas circulares completas para justificar salas altas o espacios especiales.

El **puente de batalla** se colocará donde resulte práctico dentro del escenario de la cubierta inferior, pero **solo estará disponible narrativamente cuando se desacople el platillo**.

## 2. Cubierta 01 — Puente de mando (pequeña, superior)

| N.º | Instalación | Posición conceptual | Observaciones |
|---:|---|---|---|
| 01 | **Puente principal + sala de observación/reuniones** | Parte superior; sala de observación detrás del puente | Conexión mediante turboascensor o acceso compacto con la cubierta 02. Se considera una instalación conjunta. |

**Carácter:** mando principal. No se prevén otras salas grandes en esta cubierta.

## 3. Cubierta 02 — Vida, ciencia y operaciones (circular superior)

| N.º | Instalación | Posición conceptual | Observaciones |
|---:|---|---|---|
| 02 | **Sala táctica de combate** | Proa, sector interior | Próxima a las comunicaciones con el puente principal. |
| 03 | **Sala de astrofísica / cartografía espacial** | Proa, estribor | Reserva de volumen para su gran altura; estudiar el encaje vertical. |
| 04 | **Enfermería** | Proa, babor | Se adaptará la enfermería amplia de la Enterprise-A. |
| 05 | **Sala de transportación** | Babor, próxima a enfermería | Facilita traslados y emergencias. |
| 06 | **Camarotes** | Perímetro exterior | Aprovechar ventanas; módulos amplios de poca profundidad cuando convenga. |
| 07 | **Bar** | Perímetro exterior, estribor | Priorizar vistas al espacio. |
| 08 | **Comedor / sala de esparcimiento** | Sector central de popa | Espacio social compartido. |
| 09 | **Plataforma superior del hangar** | Popa | Relación visual y funcional con el hangar principal inferior; se puede resolver como escenario de doble altura. |

**Carácter:** espacios habitables y de servicio, ciencia y operaciones cotidianas.  
**Total:** 8 instalaciones principales.

## 4. Cubierta 03 — Ingeniería y grandes instalaciones (circular inferior)

| N.º | Instalación | Posición conceptual | Observaciones |
|---:|---|---|---|
| 10 | **Sala del reactor WARP** | Núcleo técnico central o sector interior conveniente | Reactor de varios niveles de acceso. No obliga a modelar cubiertas circulares adicionales. |
| 11 | **Sala de ingeniería** | Junto al reactor WARP | Comunicación funcional y cercana con el reactor. |
| 12 | **Sala de la supercomputadora** | Sector amplio de estribor | Gran volumen; verificar interferencias con la cubierta superior. |
| 13 | **Hangar principal** | Popa | Se coordina con la plataforma superior de hangar en cubierta 02. |
| 14 | **Sala holográfica** | Sector de babor | Recinto cerrado, adaptable a las misiones. |
| 15 | **Puente de batalla** | Sector interior reservado, posición flexible | **Acceso narrativo únicamente durante la separación de la nave**. No necesita coincidir con una posición física realista del cuerpo de la nave. |

**Carácter:** propulsión, sistemas técnicos y grandes volúmenes.  
**Total:** 6 instalaciones principales.

## 5. Resumen

| Cubierta | Tipo | Instalaciones |
|---|---|---:|
| **01** | Superior pequeña — mando | 1 |
| **02** | Circular superior — vida, ciencia y operaciones | 8 |
| **03** | Circular inferior — ingeniería y grandes instalaciones | 6 |
| **TOTAL** | **Tres espacios de cubierta: dos grandes y uno pequeño** | **15** |

> El número 15 cuenta el **puente principal y su sala de observación** como un conjunto, según la lista original. El hangar principal y su plataforma superior se cuentan como dos instalaciones relacionadas.

## 6. Circulación y mantenimiento

- **Cubiertas 02 y 03:** corredor principal de distribución en anillo, complementado con pasillos radiales hacia las salas.
- **Conexión entre cubiertas:** turboascensores y, donde tenga sentido, accesos verticales mediante escalera de mano.
- **Red técnica secundaria:** corredores de mantenimiento ocultos y conductos Jefferies; no es necesario que cubran todos los metros del perímetro.
- **Zonas todavía sin construir:** cerrar o bloquear físicamente las salidas para que el personaje no acceda a vacíos.
- **Biblioteca modular:** consultar `CATALOGO_BIBLIOTECA_MODULAR_VALHALLA.md`, situado en `PROYECTO VALHALLA/Cubiertas Enterprise G/`.

## 7. Volúmenes especiales y criterios de implementación

1. **Reactor WARP:** permitir varios niveles de acceso mediante tramos técnicos parciales o espacios interiores adecuados, sin crear nuevas cubiertas circulares enteras.
2. **Supercomputadora:** reservar altura y superficie suficientes; no superponer habitaciones donde atraviesen su techo o su volumen.
3. **Cartografía espacial:** requiere comprobar su altura antes de fijar una sala encima o debajo.
4. **Hangar:** coordinar hangar principal y plataforma superior; el hueco entre ambos debe quedar libre si se adopta doble altura.
5. **Puente de batalla:** emplazamiento físico al servicio de la producción; su aparición y accesibilidad dependerán del estado de desacoplamiento en el juego.
6. **Escenarios y transiciones:** se permiten soluciones de carga o transiciones discretas para evitar hacer inabarcable el desarrollo. No exigir continuidad arquitectónica absoluta si perjudica la viabilidad.

## 8. Pendientes antes de construir los anillos de corredores

- Medir o verificar la ocupación real de las salas principales en Blender.
- Determinar diámetro y alturas prácticas de las cubiertas circulares.
- Reservar huecos y sectores compartidos por salas altas.
- Definir conexiones radiales, turboascensores y accesos Jefferies por sector.
- Probar compatibilidad y dimensiones reales de los módulos de la biblioteca Voyager-Valhalla.
- Tras estos pasos, convertir esta distribución conceptual en dos planos de planta, uno por cubierta circular, y un esquema pequeño del puente.

---

**Regla del proyecto:** priorizar una Enterprise-G explorable y divertida, construible con los recursos disponibles. La coherencia del universo de *Star Trek* guía la ambientación, pero no debe forzar una reproducción física completa del casco de la nave.
