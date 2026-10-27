# IDEA-0005 — Blindaje ablativo y torpedos transfásicos en Clase Valhalla

**Estado:** APROBADA CONCEPTUALMENTE por el autor; pendiente de viabilidad, diseño técnico, implementación y pruebas.  
**Fecha de registro:** 2026-10-13  
**Proyecto:** Videojuego Star Trek 3D — continuidad alternativa personal.  
**Nave destinataria:** nueva **Clase Valhalla**, inspirada en Galaxy (no un refit Galaxy).

## Propuesta aprobada
La nueva Clase Valhalla dispondrá de:
1. **Blindaje ablativo desplegable**, reconocible al exterior y distinto de los escudos, con funcionamiento y daños propios a definir.
2. **Torpedos transfásicos** (*transphasic torpedoes*), munición avanzada diferente de los fotónicos y cuánticos; **no** denominarlos «transwarp».
3. Compatibilidad de diseño con **separación funcional del platillo y combate independiente** de platillo y sección motriz. La distribución final de placas, armas y recursos en cada sección queda por determinar.

**Inspiración narrativa:** el capítulo doble «Endgame» de *Star Trek: Voyager*, donde una Janeway futura lleva tecnologías avanzadas a la Voyager. El autor aprueba expresamente modificar la **cronología televisiva** de su videojuego personal cuando resulte apropiado, incluso adelantando sucesos; **no se fija ninguna nueva fecha histórica ni el año de entrada en servicio de Valhalla**.

## Tratamiento del canon y disponibilidad
- Esta capacidad pertenece al **canon propio / GAME_ADDITION** del videojuego.
- No modificar silenciosamente otros perfiles jugables Pike/Kirk, ni introducir automáticamente estas tecnologías en todas las naves o en 2372.
- Cuando se defina la fecha de servicio de Valhalla, documentar coherencia de disponibilidad por época/partida. Las fechas originales de televisión pueden alterarse por decisión del autor, sin necesidad de justificar cambios ante el canon oficial.
- No convertir la aprobación conceptual en afirmación de código, mallas o gameplay ya implementados.

## Investigación Blender y UE5 pendiente
**Blindaje:** evaluar placas/mallas desplegables, segmentos, materiales, animaciones, colisiones y VFX; recubrimiento coherente de platillo, sección motriz y sus juntas; comportamiento durante separación/reacoplamiento; compatibilidad con hangares, emisores, deflector, barquillas y accesos; presupuesto de GPU/LOD/perfiles **Fluidez** y **Calidad**. Ninguna solución gráfica está cerrada.

**Torpedos:** definir puntos de lanzamiento, secuencia y trayectoria, VFX de salida/tránsito/impacto, iluminación, audio, colisiones, destrucción y comportamiento del armamento cuando la nave esté dividida. No se aprueban números arbitrarios de daño, munición o cadencia.

## Responsabilidades previstas
- **Star Trek específico:** configuración de armas y defensas, autorizaciones, doctrina, balance de juego y disponibilidad temporal.
- **Core RPG genérico:** identidad, estado autoritativo, acciones, recursos, daños, eventos y persistencia cuando existan contratos genéricos reales; no codificar allí nombres y reglas exclusivos de Star Trek.
- **Host Unreal Engine 5:** presentación 3D, animaciones y efectos; no autoritativo para el resultado de combate.
- **Blender/Rob3D/NAP:** preparación, auditoría, escalas, mallas y trazabilidad de activos con licencias apropiadas.

## Dependencias y exclusiones
- Depende del diseño exterior de Valhalla, separado funcional del platillo y posterior integración de combate/defensas. La primera **v0.0.1 de Sensores** no queda bloqueada por ello.
- Se asignarán fases/pasos y pruebas reales tras resolver geometría y contratos; no iniciar F07/F08 o implementar el armamento por el simple registro.
- No hay todavía prueba UE5 de blindaje desplegable, lanzadores ni impactos.

## Trazabilidad
- Acta de decisiones creativas: `proyecto/docs/roadmap/master/fases/F01/ACTA_DECISIONES_CLASE_VALHALLA_2026-10-13.md` (en rama F01 PR #2 hasta fusión).
- Gobierno: DEC-0001 (Valhalla), DEC-0011 (continuidad propia) y DEC-0012 (estas tecnologías), en `proyecto/docs/roadmap/master/DECISIONES_Y_RIESGOS.md` de la PR #2.
- Ideas relacionadas: [hangares independientes IDEA-0003](IDEA-0003_hangares_independientes_atraque_simulado.md).
