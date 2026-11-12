# Planes y dirección del proyecto

**Plan general vigente:** [`master/README.md`](master/README.md) · [Plan Maestro F00–F15](master/PLAN_MAESTRO.md) · [Estado global](master/ESTADO_GLOBAL.json).

Este directorio conserva los roadmaps especializados **sin trasladar ni renumerar sus entregables**. El plan maestro determina prioridades y pruebas de aceptación del **videojuego completo**; los siguientes documentos mantienen su propia autoridad sobre el detalle de sus dominios.

## Subplanes en uso o preservados

- [Preparación del diseño — ocho pilares](game_design_readiness_v0_2.md): base de Academia, carrera, vida social, bienestar, lore, IA, universo y Ordenador.
- [Vertical slice de Sensores](ship_console_vertical_slice_v0_0_1.md): árboles funcionales, resultado observable, historial y aceptación previstos; integración en UE5/Core pendiente.
- [Plan procedural de 120 capas](procedural_layers_master_plan_v0.1.md): alcance **documental/contratos**, capa 119 parcial y 120 bloqueada por runtime.
- [Universo dinámico — 10 bloques](procedural_dynamic_universe_10_block_plan_v0.1.md): **1–10 cerrados únicamente como contrato/referencia offline**, pendiente runtime CoreRPG/HOST/UE5. [B04 economía viva](procedural_living_economy_plan_v0.1.md) · [B05 historia](procedural_history_major_events_plan_v0.1.md) · [B06 ciencia/tecnología](procedural_science_technology_discovery_plan_v0.1.md) · [B07 fenómenos y arqueología](procedural_phenomena_archaeology_plan_v0.1.md) · [B08 crisis sistémicas](procedural_systemic_crises_plan_v0.1.md) · [B09 misiones emergentes](procedural_emergent_missions_plan_v0.1.md) · [B10 evolución offscreen](procedural_background_galactic_evolution_plan_v0.1.md). Sin runtime CoreRPG/HOST/UE5.
- [Vida en Academia — cierre 20/20](academy_life_final_closure_v1.0.md): contratos y simuladores de referencia; no equivale a la Academia 3D.
- [Vida a bordo y generación de nave 15/15](shipboard_life_and_procedural_starship_generation_plan_v0.1.md): contrato/referencia, integración posterior.
- [Manual de Sensores](sensors_operator_manual_plan.md) y [preparación de lore jugable](gameplay_lore_readiness.md).

- [LORE-01–04 — Estado documental definitivo](../../../CONTENT_STATUS.md): todas las fases A–E correspondientes cerradas documentalmente; no equivale a runtime.
- [LORE-05A — Reconciliación Enterprise-D / Proyecto Valhalla](lore_05_a/README.md): **candidata documental, pendiente CI y fusión**; [DEC-0020](../decisions/enterprise_d_proyecto_valhalla_2380_2387_2026-11-13.md) prevalece en la identidad del buque. B–F no iniciadas.
- [LORE-03 — Historia, conflictos y continuidad](lore_03_master_plan_v0.1.md): cerrada documentalmente desde octubre, con anotaciones históricas preservadas; sin runtime.

## Regla de gestión

La ejecución de una tarea se cierra **solo contra su criterio de entrega**, con pruebas/commit/enlaces. No marcar una función de runtime completa solo por existir su diseño. Al cambiar un subplan se actualizan su estado y el plan maestro cuando cambien prioridades o alcance; `CONTENT_STATUS.md` se modifica únicamente si cambió el contenido/estado editorial que representa.
