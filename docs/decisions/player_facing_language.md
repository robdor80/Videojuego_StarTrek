# Player-Facing Language

Status: **APPROVED GAME DESIGN**

## Rule

The internal authoring and runtime model may use stable English technical identifiers.

The **player-facing game language is Spanish (Spain)**.

Examples:

```text
internal id: lieutenant_commander
display es-ES: Teniente comandante

internal id: chief_engineering_officer
display es-ES: Jefe de Ingeniería

internal id: first_officer
display es-ES: Primer Oficial
```

## Scope

Spanish must be used in:
- HUD
- menus
- character sheets
- rank labels
- department and position labels
- mission/system messages
- codex entries
- tutorial text
- player-facing AI/system output

English identifiers are implementation details and must never leak into the normal interface.

## Future localization

The architecture remains localization-ready. English or other languages may be added later, but `es-ES` is the authoritative launch/display locale for the current project.
