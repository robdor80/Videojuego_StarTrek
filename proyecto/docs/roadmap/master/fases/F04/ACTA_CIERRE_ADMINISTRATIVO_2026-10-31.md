# Acta de cierre administrativo F04 — 31-10-2026

**Proyecto:** Videojuego Star Trek RPG · **Fase:** F04 — Naves, dotación y autoridad.
**Resolución:** CERRADA en el **corte operativo probado**, al objetivo organizativo **REFERENCIA_PROBADA** del Plan Maestro. Siguiente fase principal: F05 EN_CURSO, primer incremento F05-P01. Esta acta reconcilia el estado; no modifica código ni invalida la historia de los informes anteriores.

## Evidencias y fuentes verificadas

- GitHub `Videojuego_StarTrek/main`: merge [PR #76](https://github.com/robdor80/Videojuego_StarTrek/pull/76) en `142f852e5a1abfa373413002be928fd4f437b3bc`, con base previa que incorpora las implementaciones y ampliaciones F04.
- GitHub `CoreRPG/main`: merge [PR #13](https://github.com/robdor80/CoreRPG/pull/13) en `76a7b7b485616d8c4994f384a90f123bf333591d`, fuente histórica `89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98`.
- [CI principal de Star Trek tras merge de PR #76](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41217034878) en verde; [cuatro workflows del HEAD final de la rama F04](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/41214818632) y los workflows de contratos/gobierno/operación en verde; [CI de CoreRPG main](https://github.com/robdor80/CoreRPG/actions/runs/41212329569) en verde.
- Cinco perfiles organizativos F04: Miranda (130), Intrepid (160), Sovereign (700), Odyssey (1.600), Valhalla (1.800 Flota + 400 civiles). Plantillas y agendas reales; sin confundir civiles, dotación naval Defiant y Marines.
- Persistencia histórica y recuperación autoritativa en CoreRPG; seis campañas auditadas: cinco de **365 días** y una de **730 días** para Valhalla, con resultados PASS en la evidencia de PR #76. Repetibilidad, IDs estables, turnos, límites y comparación de futuro documentados en [informe de historial](F04-PERSISTENCIA-03_CAMPANAS_LARGAS.md) y artefactos de CI.

## Alcance exacto y exclusiones

- Cierre de la **base organizativa y de autoridad validada** que F05 debe reutilizar; no afirmación de `UE5_JUGABLE`, del puente acabado ni de una partida completa.
- `NullRHI` acredita lógica/representación Unreal sin certificar gráficos, recorrido o interfaz final.
- Se preservan como deuda explícita, **no capacidades demostradas por este acta**, las operaciones completas con platillo y cuerpo separados bajo mandos autónomos independientes, todas las transiciones acoplada/desacoplada de Defiant, el despliegue de Marines en misión, combate/camuflaje y la integración de órdenes inteligentes. No extrapolar pruebas de censo/adscripción a estos flujos. El plan operativo [F04-INTEGRACION-04](PLAN_CIERRE_F04_2026-10-31.md) conserva su valor de especificación de los escenarios amplios **aún no certificados**; se deberá asignar explícitamente su futura entrega antes de anunciar esas capacidades.
- Permanecen históricos y **no se reescriben** los resultados y avisos `EN_CURSO` de documentos elaborados durante la ejecución.

## Gobierno y siguiente paso

Se reconcilian `ESTADO_GLOBAL.json`, `PLAN_MAESTRO.md` y el índice F04. F05 pasa a EN_CURSO **solo como apertura administrativa** y P01 EN_CURSO; P02–P04 siguen sin implementación certificada, y P05 conserva únicamente sus pruebas de referencia previas. F05 **no** es `CORE_INTEGRADO` ni `CERRADA` hasta pruebas de runtime y auditoría independientes.

**Control de cambios:** documentación y ajuste mínimo del validador de gobierno del roadmap para reconocer el estado actualizado, en PR separada. La fusión queda sujeta a revisión, CI y autorización del director técnico. No se modifican activos 3D, Blender, CoreRPG, UE5, scripts de producción ni resultados de laboratorio.
