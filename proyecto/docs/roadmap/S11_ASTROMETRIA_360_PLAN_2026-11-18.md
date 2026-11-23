# S11 — Plan de implementación incremental de Astrometría 360°

**Fecha:** 18-11-2026. **Autor:** aprobación explícita de diseño. **Estado:** fase de diseño concluida; runtime pendiente. DEC-0023.

## Meta

Una sala holográfica 360° **real, interactiva y espectacular** que utilice información de CoreRPG, cartas estelares, sensores, ciencia y navegación. No crear una galaxia paralela ni animar billones de estrellas. El prototipo debe ser útil desde la primera iteración, con calidad visual creciente.

| Paquete | Responsable propuesto | Entregable |
|---|---|---|
| **S11-I01** Contratos/datos | ChatGPT | Diseños, perfiles y validaciones estáticas de S11; **cubierto documentalmente en esta entrega** |
| **S11-I02** Proyección de solo lectura | Codex — HOST/Core | Adaptador autorizado por contexto, jerarquía L1–L4, permisos, hechos y revisión de conocimiento; sin segunda base de datos |
| **S11-I03** Holograma 3D vertical slice | Codex — Unreal + ChatGPT diseño | Cámara 360°, galaxia agregada, sector Sol/Vulcano, selección, ID persistente, LOD |
| **S11-I04** Sistema/planeta y Ciencia | Codex — Unreal/Science | Órbitas, globo, ficha, comparación Tierra–Vulcano y etiquetas de escala |
| **S11-I05** Consola/voz/PADD | Codex + ChatGPT UX | LCARS, pantalla completa, PADD ligero, comando determinista sin servicio IA, accesibilidad |
| **S11-I06** Navegación/Universo Vivo | Codex en fronteras de dominio | Handoff rutas, capas políticas temporales, cambios legítimamente conocidos, proyecciones |
| **S11-I07** Sala premium y coherencia de interiores | ChatGPT diseño + Blender/Codex UE5 | Ubicación/puertas/estructura cuando S12 lo permita; materiales Galaxy Refit A2, animación refinada |
| **S11-I08** Certificación real | ChatGPT auditoría + Codex + autor | AST-01…AST-20 en UE5, FPS, latencia, VRAM, guardado, seguridad y demostración MSI |

**Vertical slice recomendado:** Sol y Vulcano como primeros ejemplos, región y cartas próximas, Tierra y Vulcano comparables, rutas visibles, cámara orbital libre y presentación LCARS. Se pueden usar geometrías de prueba inicialmente; la falta de sala final no bloquea validar interacción y datos.

## Dependencias y reglas

- Sensores DEC-0021 proporcionan lecturas ordinarias precisas/inmediatas dentro de alcance, cuando el refit esté operativo.
- Navegación mantiene cálculos y autoridad de maniobras; Ciencia mantiene análisis; Core conserva verdad y descubrimientos.
- HOST **orquesta servicios** y no reimplementa reglas F10, F11 ni los dominios especializados.
- Diseño de cubiertas/entrada/paredes se hace en S12/Valhalla, sin inventar ahora geometría.
- Fase de arte 2D/UI, especificaciones y guiones de voz pueden adelantarse sin cuota Codex; la ejecución nativa y Unreal requieren implementación, pruebas y validación.

## Cierre

**Aprobación de diseño no equivale a implementación.** Declarar sistema jugable únicamente tras pasar pruebas runtime y aceptación del autor en su máquina objetivo.
