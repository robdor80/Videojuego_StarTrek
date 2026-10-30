# PLAN DE CIERRE F04 — cinco subfases ordenadas

**Fecha:** 31-10-2026. **Estado:** plan de ejecución **no equivale a fase cerrada**. Parte del merge PR #72 y de las clases Miranda, Intrepid, Sovereign y Odyssey ya integradas. Responsable implementación: Codex local MSI; responsable auditoría, fusiones y aceptación: ChatGPT. **Una rama y PR Draft por subfase** desde `origin/main` limpio y actualizado; no fusionar sin auditoría.

## F04-VALHALLA-01 — Quinta clase y comunidad

Implementar [plantilla exacta de Valhalla](F04-VALHALLA-01_PLANTILLA_1800_Y_CIVILES_400.md): siete departamentos, 90 secciones, 1.800 personas de Flota, 400 residentes civiles (2.200 personas distintas), día de referencia 550 Alpha / 380 Beta / 255 Gamma / 615 fuera; 40 operadores navales Defiant + 60 Marines Hijos de Odín ya contados entre los 1.800, **funciones totalmente diferenciadas**. Guardias de 1, 7, 14 y 28 días reutilizando sistema 3×8 de Sovereign/Odyssey, máx. 5 turnos en 7 días móviles, mín. 12 h entre turnos, bajas/relevos, ocho funciones críticas en Valhalla. Distinguir personal naval, Marines y civiles sin convertir a civiles en oficiales de Flota. Camuflaje y combate de Defiant **NO ejecutables aquí**. Validar manifest, cobertura, latencias, memoria y límite de 65.536 entidades/64 MiB; si falla horizonte prolongado, declarar bloqueo técnico explícito y continuar a paquete de persistencia sin fabricar resultados.

## F04-GUARDIAS-02 — Miranda e Intrepid Beta/Gamma

Completar turnos reales de Miranda (130/32) e Intrepid (160/34), manteniendo sus secciones e IDs, adaptando SCHEMA 3→4 de forma versionada. Reusar el mismo planificador y contratos; no copiar demanda gigante de Sovereign ni alterar manualmente plazas para cuadrar. Determinar cuadros diarios físicamente factibles, rotaciones 1/7/14/28 días, autoridades sustitutas, descanso, cobertura crítica y déficits documentados. Probar la carga de partidas antiguas y regresiones de las cinco clases.

## F04-PERSISTENCIA-03 — Historial largo

Corregir límite actual de historial CoreRPG: en Odyssey, tras acumular 56 días se rechaza nuevo bloque por cota de 65.536 entidades/64 MiB. Diseñar retención/archivo/compactación **dentro de la autoridad CoreRPG** sin borrar hitos causales, bajas, decisiones, auditoría exigible, estado ni reproducibilidad; sin crear almacén independiente con otra fuente de verdad. Ejecutar pruebas de transacciones, fallos a mitad de guardado, recuperación y migraciones. Demostrar campañas de al menos un año y un ensayo multianual, con progreso y límites medidos para Odyssey y Valhalla. **Si requiere alterar CoreRPG** y no existe API compatible, preparar propuesta aislada y pedir autorización explícita antes de modificar el repositorio genérico.

## F04-INTEGRACION-04 — Secciones, tripulaciones y responsabilidades

Ejercitar estados CoreRPG de platillo y cuerpo de Valhalla separados (mando y cobertura por sección), Defiant acoplada/desacoplada, 40 tripulantes navales dedicados, Marines embarcados/desembarcados como pasajeros de misión, 400 civiles con residencia/unicidad. Sin doble ubicación, plaza, guardia o acceso remoto por turboascensor. Probar ausencias, bajas, mando sustituto, rescate, retorno, operaciones fuera de cámara y guardados/recargas. Defiant es una nave única persistente y el destacamento no la pilota. **No exigir geometría física continua o combate F09/14, ni IA F05**, pero sí invariantes lógicos certificables y pruebas Unreal NullRHI de la proyección.

## F04-CIERRE-05 — Auditoría, acta y reconciliación

Con todas las PR anteriores integradas en `main`, verificar cinco clases, esquema ABI/guardados, CoreRPG fijado, Unreal 5.8.2 NullRHI, CI en verde, identidad, civiles, turnos, mando, seguridad, persistencia de campañas largas, negativos y ausencia de modificaciones artísticas. Comparar cualquier incidencia del validador global con la base y corregir nuevas/bloqueantes. Emitir acta con todas las evidencias y límites; solo después de auditoría y fusión actualizar `proyecto/docs/roadmap/master/ESTADO_GLOBAL.json`, README y Plan Maestro, preservando el grado real de madurez alcanzado. `NullRHI` **no certifica** UE5 jugable 3D.

## Dependencias y reglas comunes

**Orden de ejecución nominal:** Valhalla → Guardias → Persistencia → Integración → Cierre. Si capacidad bloquea Valhalla a 28 días, no deshacer dotaciones: documentar y resolver en Persistencia, después repetir pruebas integrales. Dejar cada rama en PR Draft; ChatGPT audita y fusiona, el autor hace Fetch/Pull en GitHub Desktop sobre `main` antes del siguiente encargo. Nunca declarar que `F04-CERRADA` por tener solo documentos o CI verde si faltan pruebas de Core/UE5 del alcance.

**Reservado a fases posteriores:** modelado de puentes y salas 3D; IA social plena y órdenes universales; ingeniería física del blindaje; mecánica real de combate/camuflaje/torpedos; motor de flujo cuántico; misiones de infiltración; economía social y profesiones civiles completas. Es legítimo tener datos y agendas iniciales de 400 civiles en F04 sin implementar toda la experiencia de vida a bordo.

**Protección:** no modificar modelos Blender, GLB/FBX, UV, PBR, geometría Valhalla/Enterprise-D, separación experimental previa ni copias TABULA RASA. No cambios genéricos de CoreRPG sin autorización. No inventar rangos ni contar dos veces una persona destinada a Defiant y presente en Valhalla.
