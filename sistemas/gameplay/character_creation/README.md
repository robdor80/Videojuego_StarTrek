# Creación de personaje

Status: **v1.0 baseline locked**

La creación inicial define **quién era el personaje antes de comenzar la campaña**. No es un creador de builds ni un reparto de atributos.

## Orden de inicio

```text
ERA / FECHA
→ PERFIL DE JUGADOR / NICKNAME
→ BORRADOR DE PERSONAJE
→ VALIDACIÓN DE COHERENCIA
→ FICHA INICIAL BLOQUEADA
→ ACCESO A STARFLEET ACADEMY
```

## Principios

- No hay reparto manual de puntos.
- No hay nivel global.
- La especie aporta biología y contexto, no una personalidad prefijada.
- El jugador declara historia, educación, aficiones, experiencia y certificaciones.
- Las capacidades iniciales se **derivan** de esa biografía.
- El protagonista debe ser adulto-equivalente para su especie/contexto.
- La ficha inicial debe superar validación objetiva y revisión semántica de coherencia.
- Tras comenzar, la evolución ocurre mediante vida, práctica, estudio, trabajo y experiencia.

## Archivos

- `player_profile_contract.json` — separa nickname/perfil del personaje diegético.
- `character_creation_contract_v1_0.json` — flujo y campos de creación.
- `character_sheet_model_v1_0.json` — estructura de ficha.
- `prior_activity_model.json` — aficiones, deportes, artes, estudios y experiencia previa.
- `biography_validation_rules.md` — puerta obligatoria de validación.

## Ficha vs expediente

La ficha del personaje contiene el estado amplio que el juego necesita.

El expediente de Starfleet contiene solo aquello que Starfleet registra oficialmente.

```text
FICHA DE PERSONAJE
≠ EXPEDIENTE DE ACADEMIA
≠ EXPEDIENTE DE SERVICIO
≠ BITÁCORA PERSONAL
```

## Desarrollo posterior

El sistema general está en `../characters/development/`.

Los objetivos y trayectoria están en `../characters/objectives/`.
