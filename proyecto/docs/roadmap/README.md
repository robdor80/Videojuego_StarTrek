# Planes y dirección del proyecto

**Plan general vigente:** [`master/README.md`](master/README.md) · [Plan Maestro F00–F15](master/PLAN_MAESTRO.md) · [Estado global](master/ESTADO_GLOBAL.json).

Este directorio conserva los roadmaps especializados **sin trasladar ni renumerar sus entregables**. El plan maestro determina prioridades y pruebas de aceptación del **videojuego completo**; los siguientes documentos mantienen su propia autoridad sobre el detalle de sus dominios.

## Subplanes en uso o preservados

- [Preparación del diseño — ocho pilares](game_design_readiness_v0_2.md): base de Academia, carrera, vida social, bienestar, lore, IA, universo y Ordenador.
- [Vertical slice de Sensores](ship_console_vertical_slice_v0_0_1.md): árboles funcionales, resultado observable, historial y aceptación previstos; integración en UE5/Core pendiente.
- [Plan procedural de 120 capas](procedural_layers_master_plan_v0.1.md): alcance **documental/contratos**, capa 119 parcial y 120 bloqueada por runtime.
- [Universo dinámico — 10 bloques](procedural_dynamic_universe_10_block_plan_v0.1.md): 1–8 completos a nivel de contrato/referencia; **9 siguiente tras CI y fusión B08** (misiones emergentes). [B04 economía viva](procedural_living_economy_plan_v0.1.md) · [B05 historia](procedural_history_major_events_plan_v0.1.md) · [B06 ciencia/tecnología](procedural_science_technology_discovery_plan_v0.1.md) · [B07 fenómenos y arqueología](procedural_phenomena_archaeology_plan_v0.1.md) · [B08 crisis sistémicas](procedural_systemic_crises_plan_v0.1.md). Sin runtime CoreRPG/HOST/UE5.
- [Vida en Academia — cierre 20/20](academy_life_final_closure_v1.0.md): contratos y simuladores de referencia; no equivale a la Academia 3D.
- [Vida a bordo y generación de nave 15/15](shipboard_life_and_procedural_starship_generation_plan_v0.1.md): contrato/referencia, integración posterior.
- [Manual de Sensores](sensors_operator_manual_plan.md) y [preparación de lore jugable](gameplay_lore_readiness.md).

- [LORE-03 — Historia, conflictos y continuidad](lore_03_master_plan_v0.1.md): marco TNG/DS9/Voyager exclusivo; fase A iniciada documentalmente, B–E pendientes; sin runtime.

## Regla de gestión

La ejecución de una tarea se cierra **solo contra su criterio de entrega**, con pruebas/commit/enlaces. No marcar una función de runtime completa solo por existir su diseño. Al cambiar un subplan se actualizan su estado y el plan maestro cuando cambien prioridades o alcance; `CONTENT_STATUS.md` se modifica únicamente si cambió el contenido/estado editorial que representa.
