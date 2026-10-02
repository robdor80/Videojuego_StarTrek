# Starfleet Academy as a Playable Hub

Status: **APPROVED GAME DESIGN**

## Core decision

Starfleet Academy is **playable terrain**, not background lore.

The Academy must function as a living hub where the player can move between locations, attend scheduled activities, interact with NPCs, make choices, build a record and progress toward graduation.

## Presentation model

The Academy follows the global presentation rule:

```text
LOCATION != SCENE != POV
```

Example:

```text
Location: Patio de instrucción
Scene: Formación de mañana
POV: Cadete jugador
```

A location can host many scenes.

The project does **not** require unrestricted 3D free-roaming. The host may present the Academy through first-person illustrated scenes, navigable location choices, transitions and contextual interaction.

## What a playable Academy location must provide

Each location should be able to define:

- player-visible Spanish name,
- era availability,
- connected locations,
- allowed time windows,
- NPC pools,
- activities,
- scheduled events,
- random/event hooks,
- scene-state variants,
- access restrictions,
- gameplay effects.

## Academy loop

```text
Despertar / planificación
        ↓
clases / entrenamiento / guardias / estudio
        ↓
relaciones / actividades / decisiones
        ↓
evaluaciones / consecuencias
        ↓
expediente del cadete
        ↓
progresión académica
```

Free time is meaningful: the player may study, train, socialize, explore approved areas, meet instructors, participate in clubs or ignore obligations and accept the consequences.

## Canon rule

Canon determines:
- institution,
- era,
- known geography,
- known schools/facilities,
- terminology,
- historical context.

The game may add connective or functional spaces when needed, but they must be marked `GAME_ADDITION` and must not contradict retained canon.

## Completion rule

No Academy subject is complete until it has a gameplay consequence or explicit reason for remaining lore-only.
