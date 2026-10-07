# Contrato IA — interpretación de órdenes de nave

Status: **FOUNDATION v0.2**

## Regla principal

**AI interprets. Core executes.**

La IA transforma lenguaje natural (texto o voz) en un `CommandPlan` estructurado. Nunca muta directamente el estado autoritativo.

Esquema canónico:

`schemas/starship_computer_command_plan.schema.json`

Arquitectura general:

`ai/command_interpretation/starship_computer_system.md`

Paridad completa de Sensores:

`ai/command_interpretation/sensors_manual_ai_parity.md`

## La IA puede

- interpretar lenguaje natural, incluso coloquial o imperfecto;
- extraer intención y parámetros;
- resolver referencias contextuales cuando el perfil de computadora lo permite;
- descomponer una orden en varias acciones candidatas;
- pedir una aclaración;
- generar una consulta estructurada;
- preparar una secuencia procedimental;
- resumir un resultado autoritativo;
- proponer opciones técnicamente válidas.

## La IA no puede

- elevar escudos por sí misma sin una acción validada;
- quitar energía de un sistema;
- causar daño;
- disparar un arma;
- cambiar rumbo;
- declarar una reparación terminada;
- inventar permisos;
- saltarse la cadena de mando;
- inventar información de sensores;
- inventar respuestas de otros departamentos;
- decidir qué recurso/contacto/vida sacrificar cuando corresponde al oficial;
- declarar que una operación tuvo éxito antes de que Core la resuelva.

## Flujo

```
UTTERANCE
   ↓
INTERPRETER (Gemini / fallback)
   ↓
COMMAND PLAN
   ↓
SCHEMA VALIDATION
   ↓
AUTHORITY / CONTEXT / RESOURCE VALIDATION
   ↓
DETERMINISTIC EXECUTION
   ↓
AUTHORITATIVE RESULT
   ↓
COMPUTER PRESENTATION
```

## Ejemplos

```text
«Rumbo 173 marca 4, warp 6»
→ candidate: navigate(course=173/4, speed=warp_6)

«Saquen toda la potencia que puedan y denla a los escudos»
→ candidate: transfer_power(destination=shields, amount=max_safe_available)

«Mantén C-43 bajo seguimiento prioritario y avísame si cambia de rumbo»
→ actions:
   track_start(contactId=C-43, priority=priority)
   watch(contactId=C-43, condition=course_change)
```

En todos los casos el resultado final depende de reglas, permisos y estado real.

## Clarification contract

Si la orden no puede transformarse de forma segura:

```json
{
  "version": "1.0",
  "intentSummary": "Objetivo ambiguo",
  "needsClarification": true,
  "clarificationQuestion": "¿Qué contacto desea mantener en seguimiento?",
  "actions": []
}
```

No debe rellenarse un dato importante al azar para evitar hacer una pregunta.

## Trazabilidad

Toda acción relevante debe permitir reconstruir:

- texto/transcripción de entrada;
- proveedor/modelo de interpretación;
- perfil de computadora;
- contexto autoritativo suministrado;
- `CommandPlan` producido;
- validación;
- acciones realmente ejecutadas;
- IDs/resultados autoritativos;
- aclaraciones o bloqueos.

No registrar más información privada o bruta de la necesaria para diagnóstico.
