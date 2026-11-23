# F11 — Plan autoral actualizado (11-11-2026)

**Alcance:** decisión de diseño de la carrera profesional; NO acredita integración CoreRPG, Host ni Unreal Engine.
**Estado:** F11-P01 iniciada, documentación/contrato en desarrollo; F11 global no cerrada.
**Autoridad:** decisiones creativas aprobadas por el propietario en conversación el 11-11-2026.
**Destino aspiracional:** USS Enterprise NCC-1701-D modernizada (Galaxy refit), denominada internamente «Valhalla» durante el trabajo anterior. No confundir con la **nueva clase Valhalla** de documentos históricos: para la nueva campaña, la nave objetivo del jugador es la **Enterprise-D**. Reconciliar más adelante las referencias históricas/planes de clases; no reescribir artefactos anteriores silenciosamente.

## Propósito y contrato de producto

El jugador debe poder disfrutar etapas sustantivas como teniente, teniente comandante con jefatura, comandante con jefatura, primer oficial, capitán de otra nave y finalmente **capitán de la Enterprise-D**, conservando libertad de aceptar, rechazar o posponer ofertas.

**Garantía de diseño:** si el jugador sigue voluntariamente la ruta de mando, cumple hitos y permite avanzar el tiempo ficticio, el sistema DEBE crear oportunidades válidas y creíbles hasta alcanzar el objetivo. No depender exclusivamente del azar o de vacantes casuales; tampoco regalar rangos automáticamente cada X días. Sucesiones de NPC, promociones y traslados se preparan con antelación y se registran con causa. La garantía se refiere a la progresión a lo largo de la campaña, NO a saltarse comprobaciones de autoridad.

**Ninguna plaza ocupada se libera artificialmente al ejecutar una promoción:** un NPC puede recibir oferta de ascenso y destino alternativo, pero conserva su puesto hasta formalizar el relevo. No forzar fallecimientos, ceses arbitrarios, desapariciones ni expulsiones para favorecer al protagonista. Nunca fabricar cualificaciones, órdenes, recursos o vacantes ya efectivas.

No se implementa por ahora un temporizador fijo de años; la duración se decidirá/ajustará más adelante para que cada etapa resulte disfrutable, en tiempo ficticio acelerado, con temporadas, servicio y posibles elipsis. El juego no debe reservar la capitanía solo para el epílogo.

## Distribución de subfases aprobada

| Paso | Nuevo alcance autoral | Evidencia deseada |
|---|---|---|
| **F11-P01** | Escalafón; rango, división, departamento, puesto, destino y estación; autoridad contextual, mando, sustitución y delegación | Reglamento + contrato verificable + casos positivos/negativos; referencia no mutadora |
| **F11-P02** | Destinos, vacantes ordinarias, departamentos, perfiles de puesto, ofertas y solicitudes de traslado | Catálogo y reglas de asignación |
| **F11-P03** | Evaluación, méritos, promociones, sanciones y planificador de oportunidades garantizadas | Máquina de estados de progreso; plan de preparación de vacantes con horizontes flexibles |
| **F11-P04** | Trayectorias, mando de departamento, primer oficial, capitán de otra nave y sucesión eventual de la Enterprise-D | Director de sucesiones de NPC, casos de reubicación causal, aceptación/rechazo del jugador |
| **F11-P05** | Expediente persistente, continuidad de NPC y validación transversal de la carrera | Esquemas de eventos; migraciones; pruebas Core/Host/UE5 y guardado/carga cuando se integre |

La documentación F11 del 14-10-2026 («rutas y clases», prototipo Python, escenarios) se conserva como **referencia histórica reutilizable**, sin atribuirle autoridad runtime ni compatibilidad automática con la nueva decisión creativa. La numeración anterior de pasos se interpreta como organización histórica; este documento prevalece para el alcance nuevo aprobado, pendiente de reconciliar el Plan Maestro tras revisar las dependencias.

## Responsabilidades y viabilidad de implementación

- **Star Trek (este repositorio):** escalafón, cargos, política de autorización, causas narrativas de ofertas, tipos de vacantes, criterios de elegibilidad y semántica de la Enterprise-D.
- **CoreRPG:** entidades, tiempo, identidad y revisiones fiables, eventos causales, expedientes, estados de NPC, autorización final y persistencia; añadir capacidades genéricas solo si faltan, sin clonar Core en este repositorio.
- **Host/UE5:** emitir solicitudes y representar órdenes, ceremonias, comunicaciones y puestos, siempre mostrando estados confirmados por Core.
- **Narrativa/IA:** preparar explicaciones, diálogos y variaciones; **nunca** conceder rangos o vacantes directamente.

Plan técnico futuro del director de carrera: (1) evaluar un hito del jugador con datos autoritativos; (2) programar anticipadamente una cadena causal de oportunidades profesionales NPC; (3) comprobar vacantes y méritos; (4) emitir oferta; (5) registrar aceptación/rechazo; (6) aplicar eventos confirmados y continuidad social. Si un plan narrativo falla, regenerar otro sin mutar autoridad ni expulsar al NPC.

**Viabilidad:** la arquitectura es realizable con máquinas de estados/eventos y planificador acotado. No se afirma que esas capacidades estén implementadas ya. La garantía de progresión será una propiedad que deberá probarse con campañas simuladas y partidas reales, incluyendo decisiones adversas y ausencia de vacantes.

## Gate de F11-P01

1. Separación estricta de grado, puesto, destino, cualificación, guardia y autoridad.
2. Cadena de sucesión sin cambio automático de rango ni plaza.
3. Delegación acotada por ámbito, fuente, duración y revocación.
4. Límites médicos y de normas aplicados por competencia, no por comparar galones.
5. Pruebas negativas: no usurpación por rango, vacante, recomendación, IA ni pertenecer a la nave; fail-closed ante falta de datos fiables.
6. No modificar los estados maestros ni cerrar F11 hasta satisfacer su puerta real; distinguir DOCUMENTACIÓN / CONTRATO / CORE / UE5.

## Reutilización explícita

- `proyecto/docs/decisions/personnel_model.md`, `universal_rank_insignia.md`, `character_growth_without_xp.md`.
- `proyecto/docs/roadmap/master/fases/F04/MANDO_NOMBRAMIENTOS_P03.md` y `LIMITES_MEDICOS_NORMATIVOS_P04.md`.
- `sistemas/gameplay/chain_of_command/` y `mundo/lore/federation/starfleet/command_structure/succession_rules.json`.
- `sistemas/gameplay/careers/` y `desarrollo/tools/validation/f11_career_reference.py`.
- `proyecto/docs/roadmap/master/CRITERIOS_DE_CIERRE.md`.

**Nota:** el antiguo `README.md` de F11, `PLAN_MAESTRO.md` y `ESTADO_GLOBAL.json` contienen referencias previas a la nueva clase Valhalla y al objetivo UE5. Se conservan sin alteración en esta rama de diseño P01; requieren una futura reconciliación explícita, sin falsificar el estado del desarrollo.
