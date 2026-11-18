# S12 — Plan propuesto de construcción de interiores y desplazamientos

> **ACTUALIZACIÓN AUTORAL 18-11-2026 — PROTOTIPO S12 NO APROBADO:** la identidad/autenticación/permisos de puertas privadas **pertenecen ahora al Sistema 18 (DEC-0024, fusionada en main)**, no a S12. S12 se concentra en puertas mecánicas/automáticas, pulsadores, turboascensores que llegan a la **parada real más próxima**, navegación de NPC y geolocalización/mapas LCARS. **No es un sistema de decoración, texturas ni construcción de recorridos Blender.** Véase S12_FUNCIONAL_PRIORIDADES_ADENDA_2026-11-18.md.

**18-11-2026 — propuesta para revisión, NO implementación.** S12 = Sistema 12 del catálogo de 17, no fase de proyecto F12 (Vida a bordo).

## Meta

Crear la experiencia de recorrer la USS Enterprise-D modernizada sin destruir recursos Blender locales ni requerir casco y cubiertas físicamente unidos en Unreal. Topología Core persistente, sectores UE5 caminables, transiciones válidas de turboascensor, NPC con agendas F12, puertas y emergencias reales.

| Paso | Responsable | Entregable |
|---|---|---|
| **S12-I01** Inventario de escenarios y auditoría | ChatGPT contratos + Blender / Codex cuando proceda | Asignación de ID a cubiertas, lugares y conectores; distinguir geometría verificada de inventario histórico; sin alterar .blend |
| **S12-I02** Grafo funcional y seguridad | Codex (Core/HOST) con ChatGPT revisión | Reutilizar `interior_navigation_graph_v0.1`, autorización, daños, tiempo, mapas de acceso; sin doble simulador |
| **S12-I03** Vertical slice D→E | Blender + UE5/Codex | Camarote D → corredor realmente transitado → puerta/turbolift → escena E → destino; colisiones y streaming |
| **S12-I04** Puertas, ascensores, Jefferies | Codex/UE5 + ChatGPT diseño | Contratos de estados; puerta sin hueco falso; viaje que consume tiempo y persiste; mantenimiento solo donde exista |
| **S12-I05** Tripulación que se desplaza | Core/HOST/Codex en coordinación con F12 | Un oficial en guardia, otro libre; LOD visual sin duplicidad ni desaparición |
| **S12-I06** Salas emblemáticas | Diseño conjunto + Blender/UE5 | Puente A, Astrometría S11 (ubicación posterior), Ten Forward E, Ingeniería, supercomputadora, Enfermería y Holocubierta en escenas reales |
| **S12-I07** Emergencias y sección de batalla | Core/UE5/Codex | Compartimentación, accesos, crisis y puente de batalla externo con transición condicionada |
| **S12-I08** Auditoría MSI y fusión futura | ChatGPT + Codex + autor | Pruebas de recorridos, seguridad, save/load, tiempo, NPC, VRAM/FPS, estilo y aceptación en equipo real |

**Primer slice visual viable:** recorrer el camarote y su puerta D, pasillo curvo D y turbolift, cargar una zona E funcional. No intentar toda la Enterprise de golpe. Conservar el proyecto Blender, la biblioteca de elementos y el estilo Galaxy Refit A2.

## Dependencias y restricciones

- DEC-0020 nave Enterprise-D clase Galaxy; Proyecto Valhalla **programa**, no clase.
- S11 Astrometría queda funcionalmente diseñada, con sala sin posición exacta aún.
- F12 del roadmap sigue siendo vida a bordo/relaciones (no cambiar sus hitos P01–P05).
- MAP-01 validador existente requiere enlaces `verified=true`; ningún acceso no auditado pasa automáticamente a juego.
- Las cubiertas pueden representarse con mapas distintos; pasillos dentro de cada sector sí deben ser realmente caminables.
- No exportar binarios 3D al Git ignorando su política, no borrar ni modificar un .blend sin autorización y copia de trabajo.
- Turbolift puede cargar mapa virtual, **no traslada físicamente UE5 a través de un casco completo**.
- La topología Core mantiene tiempo y restricciones incluso si UE5 presenta una transición breve.
- Un NPC no se duplica, no aparece sin causa, no construye relaciones por proximidad.

## Criterio de promoción

`PROPOSAL_REVIEW_REQUIRED` → revisión/decisión autoral → contrato aprobado → vertical slice en MSI con pruebas → expansión / certificación. **Ningún check documental sustituye un test real UE5.**
