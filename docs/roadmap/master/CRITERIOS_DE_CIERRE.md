# Criterios comunes de aceptación y cierre

## Dos dimensiones independientes

**Estado de planificación** (por paso/fase): `PLANIFICADA`, `EN_CURSO`, `EN_REVISION`, `BLOQUEADA`, `CERRADA`, `DESCARTADA_CON_MOTIVO`.

**Madurez/evidencia del entregable**: `IDEA`, `DISENO_VALIDADO`, `CONTRATO_VALIDADO`, `REFERENCIA_PROBADA`, `CORE_INTEGRADO`, `UE5_JUGABLE`, `ACEPTACION_SUPERADA`. Esta es una escala orientativa, no confundir con un mismo artefacto que deba pasar linealmente por todas. La web y assets tienen evidencia adicional de publicación/importación.

Ejemplo: un sistema puede estar `CERRADO` en **contrato v0.1** y seguir `BLOQUEADO` para **integración UE5**. El plan mantiene ambos hechos sin sobrescribirlos.

## Puerta obligatoria de cada paso

1. **Reutilización:** comprobar en `gameplay/`, `lore/`, `universe/`, `ai/`, `docs/`, `tools/` y `validation/` si existe. Referenciar rutas precisas y SHA/PR si aplica.
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
- Ideas nuevas siempre en `ideas/BUZON.md`; estado `PLANIFICADA` solo después de ubicar y aceptar su fase/paso.
- Escenarios donde se requiere autor: clase protagonista de Imperator, cambio de canon/épocas, dimensiones del primer MVP, reglas de consentimiento/privacidad o límites de la simulación.
- La **F00 se cierra por evidencias documentales y de navegación**; no significa que F01–F15 estén cerradas ni que se haya desarrollado un ejecutable 3D.
