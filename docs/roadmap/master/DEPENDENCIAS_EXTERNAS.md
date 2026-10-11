# Dependencias externas a Videojuego_StarTrek

**Propósito:** evitar que documentación/activos de otros repositorios aparezcan falsamente como entregables integrados aquí.

| Sistema | Localización/identidad conocida | Responsabilidad y fases | Evidencia y puerta pendiente |
|---|---|---|---|
| **Academia web** | [`robdor80/academiaflota`](https://github.com/robdor80/academiaflota); [web](https://robdor80.github.io/academiaflota/) | Material educativo, selección de perfil y experiencia web (F10) | Auditar `main` y sincronización; **no** implica cadete UE5 ni guardados Core |
| **Core RPG** | Repositorio/versión exactos se comprobarán en F02 | Estado genérico, reglas, persistencia, eventos, IA context builder (F02–F15) | No suponer 4.10 entregada ni interfaces inventadas; ver `DEPENDENCIAS_CORE_RPG.md` |
| **Unreal Engine 5** | Entorno/proyecto jugable aún no presente en árbol de este repo auditado | Puentes, movimiento, render 3D, consolas, VFX, empaquetado (F07–F15) | Registrar repositorio o proyecto real, versión de UE, build, rendimiento, pruebas de interacción |
| **Blender / Rob3D** | Herramienta y proyectos externos; ruta/repo definitivo por verificar | Limpieza, importación, mallas, materiales, licencias (F07, F14) | Nunca modificar fuentes 3D originales; outputs derivados trazables; revisar ejes/escala/PBR |
| **NAP 2.0** | Proyecto/pipeline visual externo; `art_direction/nap/` y `nap/` contienen reglas Trek | Archivo maestro, derivados de producción, metadatos, identidad visual (F07, F14) | Revisar estado real de NAP 2.0; nunca dar por distribuido un recurso por existir una biblia |
| **IA por API remota** | Proveedor intercambiable según rutas lógicas | Decisiones candidatas, diálogo, asesoría contextual (F05, F09, F12–F13) | No accede a World Truth completo ni ejecuta mutaciones, latencia/fallo no bloquean rutina |
| **MSI de destino** | Windows 11, RTX 4070 de 8 GB, 32 GB RAM | Restricción de diseño/rendimiento (F01, F07, F08, F15) | Medir en hardware real, no inferir FPS por capturas |

## Contratos de interfaz que habrá que decidir en fase, nunca a ciegas

- **Star Trek ↔ Core:** IDs, autoridad, eventos, consulta conocimiento, reglas, guardado/carga.
- **Core ↔ UE5:** lectura de estado, inputs/acciones, sincronización de NPC 3D, replicación visual local, escenas, telemetría.
- **Academia web ↔ partida:** identidad de jugador, progreso educativo vs progreso diegético, autenticación/sincronización segura; sin acoplar el estado canónico del juego a un sitio web.
- **NAP ↔ Star Trek ↔ UE5:** metadata de procedencia/versión/uso comercial, asset maestro y derivado, escala y materiales, trazabilidad.
- **IA ↔ motor:** contexto filtrado, candidato estructurado, validación en recepción, fallback determinista y observabilidad de fallos.

## Reglas sobre elección de naves 3D

La decisión de la Dama base **Galaxy / Sovereign / Odyssey** no consta aprobada: va a F01. El **puente piloto** de F07 puede elegirse por conveniencia técnica si no prejuzga la Dama protagonista. La carrera incluye naves menores/intermedias y la **Imperator** como posible aspiración máxima, nunca como final forzoso. Para modelado, licencias y assets hay que comprobar formato real, texturas y posibilidad legal de uso.
