# LORE-01 E — Información operativa transversal

**Ámbito:** TNG, DS9 y Voyager, con antecedentes TOS/películas cuando son necesarios. **Fecha:** 2026-10-19.
**Estado:** investigación/documentación para revisión, NO runtime, NO importación. CoreRPG conserva toda autoridad sobre el estado de cada campaña.

## Propósito y lectura
Este bloque **no reescribe** especies, naciones, mapas, tratados ni manuales tecnológicos. Traduce ejemplos canónicos a preguntas operativas, con límites expresos; no crea permisos, fronteras, instituciones, aranceles, instalaciones, porcentajes de rendimiento ni nuevas mecánicas.

1. [Investigación por ocho ámbitos](INTERPRETACIONES_A_H.md): A sistemas y territorios; B circulación/acceso; C comercio; D ley/jurisdicción; E comunicaciones; F tecnología; G primer contacto; H operaciones civiles/científicas/humanitarias.
2. [32 fichas de evidencia operacional](operational_evidence_v0.1.json), con `record_id` estable, fuente registrada, entidades, lugares, relaciones y posibles hitos temporales.
3. [12 preguntas jugador/NPC](query_scenarios_v0.1.json): solicitudes, contexto mínimo, límites de acceso y respuestas que **no** autorizan acciones.
4. [Cruce A–E y dependencias](cross_layer_reference_v0.1.json): rutas a fuentes de verdad de autoría sin duplicarlas.
5. [18 incertidumbres](uncertainty_ledger_v0.1.json): desconocidos explícitos, mejoras y cautelas legales.
6. [Modelo de consulta y casos de decisión](MODELO_DE_CONSULTA.md).
7. [Auditoría global A–E](../../docs/roadmap/lore_01_e_global_audit_v0.1.md).
8. Validación documental: `python tools/validation/validate_lore01_e.py`; pruebas: `python tools/validation/test_lore01_e.py`.

## Cadena de consulta
**Identidad física C** → **clasificación/poder B** → **contexto de especie/cultura A** → **comportamiento individual A.1** → **relación histórica D** → **lectura operativa E** → **proyección real de conocimiento y permisos del actor** → **decisión/evolución exclusiva de CoreRPG**.

El orden no es un motor: la identidad, fecha, continuidad, autoridad y observador se consultarán en los sistemas que se integren más adelante. E ni siquiera ofrece una «autorización recomendada» vinculante.

## Interpretación de cada ficha
- `documented_observation`: hecho o situación audiovisual de referencia, **no** un estado actual de partida.
- `operational_interpretation`: inferencia editorial aplicada a preguntas de operación; no es un protocolo canónico de uso universal.
- `prohibited_inference`: deducción que deliberadamente no puede hacerse.
- `provenance_class` y `confidence`: procedencia y cautela. Las referencias al episodio no son auditoría escena a escena de todos los matices.
- `temporal.not_before_event_id`: ayuda a evitar anacronismos. **No** dispara el evento automáticamente y **no** implica disponibilidad para todos los personajes posteriores.
- `entities`, `locations`, `relations`: referencias a índices B, C y D. No afirman soberanía fija, jurisdicción o localización de un NPC en runtime.
- `knowledge` y `runtime`: límites conservadores, no contratos ejecutables.

## Ocho ámbitos
| Código | Pregunta que resuelve | Lo que deliberadamente no hace |
|---|---|---|
| A | ¿Qué significado tiene este sistema en esta época? | Crear censos, polígonos, bases o posesión permanente |
| B | ¿Qué debemos consultar antes de cruzar/atracar? | Inventar pasaportes o fronteras universales |
| C | ¿Qué comercio está realmente documentado? | Crear economía, tipos de cambio o inventarios |
| D | ¿Quién puede actuar y bajo qué jurisdicción? | Otorgar competencia legal a rango, especie o IA |
| E | ¿Quién recibió qué información y cuándo? | Confundir verdad, mensaje, rumor y acceso autorizado |
| F | ¿Qué tecnología puede conocerse/utilizarse? | Atribuir prestaciones u homogeneidad industrial |
| G | ¿Cómo negociar o contactar con respeto? | Convertir cultura en personalidad automática |
| H | ¿Qué asistencia o expedición resulta plausible? | Crear automáticamente misiones y recursos |

## Hitos, campañas y DLC
El canon determina historia preinicial y sólo hechos previamente ocurridos **y efectivamente conocidos** pueden condicionar el informe. No se ejecutan años 2373/2375 como cron automático; un año puede contener varios episodios. Las diferencias posteriores dependen del estado persistente de la campaña.

Los cinco pueblos reservados del DLC Delta permanecen documentalmente referenciables pero no generables; IDEA-0011 sigue inactiva. El encuentro Borg en Alfa de TNG no equivale a conexión transwarp Alfa–Delta.

**Prohibiciones:** no sincronizar estos JSON a `gameplay/`, `universe/generation/`, UE5 ni CoreRPG; no alterar códigos de autoridad, modelos de naves o acceso a la computadora; no declarar mundo simulado probado.
