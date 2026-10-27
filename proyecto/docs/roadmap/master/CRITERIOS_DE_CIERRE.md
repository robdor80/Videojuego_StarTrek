# Criterios comunes de aceptación y cierre

## Dos dimensiones independientes

**Estado de planificación** (por paso/fase): `PLANIFICADA`, `EN_CURSO`, `EN_REVISION`, `BLOQUEADA`, `CERRADA`, `DESCARTADA_CON_MOTIVO`.

**Madurez/evidencia del entregable**: `IDEA`, `DISENO_VALIDADO`, `CONTRATO_VALIDADO`, `REFERENCIA_PROBADA`, `CORE_INTEGRADO`, `UE5_JUGABLE`, `ACEPTACION_SUPERADA`. Esta es una escala orientativa, no confundir con un mismo artefacto que deba pasar linealmente por todas. La web y assets tienen evidencia adicional de publicación/importación.

Ejemplo: un sistema puede tener un paso `CERRADA` en **contrato v0.1** y permanecer con la **fase global `EN_REVISION`** por integración UE5. El plan mantiene ambos hechos sin sobrescribirlos.

En `ESTADO_GLOBAL.json`, `status` indica **estado de planificación**, `target_maturity` la **puerta de fase**, `achieved_maturity` la **evidencia alcanzada en algún alcance comprobable** y `step_evidence_maturity` el **nivel exacto de cada entregable cerrado o documentado**. No atribuir a toda la fase la madurez parcial más elevada. Para cerrar una fase, además de alcanzar su objetivo documental o de runtime, deberán cumplirse **todas las puertas propias de su README**, incluidas negativas, dependencias y artefactos externos pertinentes. 

**Caso 13-10-2026:** F01 `CERRADA` solamente en `DISENO_VALIDADO`; F04/F06 `EN_REVISION` aun con QA `REFERENCIA_PROBADA` porque falta validación operativa de su alcance, y F02 es la única fase principal `EN_CURSO`. Véase [acta de reconciliación](ACTA_RECONCILIACION_F00_F06_2026-10-13.md).

## Puerta obligatoria de cada paso

1. **Reutilización:** comprobar en `sistemas/gameplay/`, `mundo/lore/`, `sistemas/universe/`, `sistemas/ai/`, `proyecto/docs/`, `desarrollo/tools/` y `desarrollo/validation/` si existe. Referenciar rutas precisas y SHA/PR si aplica.
2. **Propiedad:** Core RPG genérico / Star Trek universo / UE5 3D / academiaflota web / NAP assets / proveedor IA. No mezclar responsabilidades.
3. **Alcance:** especificar resultado y exclusiones, dependencias y decisiones de autor.
4. **Entregable inspeccionable:** documento, esquema, simulador, suite, demostración, build o despliegue con URL/commit verificable.
5. **Prueba correspondiente al objetivo:** JSON válido no prueba ejecución; script definido no prueba que haya pasado; CI verde no prueba UE5; captura de puente no prueba consolas operativas.
6. **Evidencia fechada:** comando o workflow, entorno, resultado y enlace; si no se ejecutó, declarar `NO_EJECUTADO`.
7. **Trazabilidad:** enlazar tarea, decisión/idea, documentación original, validación, cambios y cierre. Los cambios de estado no pueden ocultar bloqueos.
8. **No regresión:** el trabajo nuevo no altera contratos aprobados sin migración, ni rompe la lógica ni la web Academia. Actualizar registros solo donde proceda.

## Cierres por nivel

| Nivel | Evidencia mínima |
|---|---|
| `DISENO_VALIDADO` | Decisión documentada, fuentes, alternativas, límites y autoría cuando proceda |
| `CONTRATO_VALIDADO` | Campos/estados, invariantes, interfaces, ejemplos y referencias existentes comprobadas |
| `REFERENCIA_PROBADA` | Script o motor de prueba **ejecutado**, fixture y resultado observables; no solo tests enumerados |
| `CORE_INTEGRADO` | Versión/ref concreta de Core RPG, integración ejecutada, mutación/autorización/persistencia validadas |
| `UE5_JUGABLE` | Build/proyecto UE5 realmente ejecutado, escena y controles funcionales, rendimiento básico registrado |
| `ACEPTACION_SUPERADA` | Suite E2E, casos positivos/negativos, guardado/carga, ausencia de bloqueantes y acta |

## Prioridad, control y bloqueos

- Priorizar **camino crítico** F01→F08. Antes de ejecutar trabajo específico buscar evidencias ya disponibles en su roadmap fuente.
- Dependencia externa pendiente: `BLOQUEADA` **solo la tarea dependiente**, no reetiquetar todo el proyecto; documentar versión/comportamiento esperado sin diseñar APIs definitivas sin contraparte.
- Ideas nuevas siempre en `proyecto/ideas/BUZON.md`; estado `PLANIFICADA` solo después de ubicar y aceptar su fase/paso.
- Escenarios donde se requiere autor: **nuevas** decisiones creativas sobre la **Clase Valhalla** (elección de inspiración Galaxy y nombre ya resueltos), alteraciones de canon/épocas no aprobadas, dimensiones sustantivas de nuevos MVP, reglas de consentimiento/privacidad o límites de la simulación.
- La **F00 se cierra por evidencias documentales y de navegación**; no significa que F01–F15 estén cerradas ni que se haya desarrollado un ejecutable 3D.
