# Decision — Authoritative observable universe

Status: **FIXED**
Version: **0.1**

## Principle

The game engine owns reality.

A scan, tricorder reading, scientific analysis or NPC report does **not** create the object being observed. The object, phenomenon or event must already exist in authoritative world state, either because it is canonical, authored, procedurally generated or produced by a previous campaign event.

The player discovers reality; the UI and AI do not invent it at observation time.

## Mandatory rules

1. **Ground truth precedes observation.**
   - Objects and phenomena have an authoritative state before the player scans them.
   - A sensor action queries that state.

2. **Procedural generation is deterministic and persistent.**
   - Generated content is derived from an explicit seed and context.
   - Once materialized into a campaign, the generated entity persists unless world events change or destroy it.

3. **Canon reserves space.**
   - Procedural generation may enrich unreserved space but may not overwrite canonical locations, events, factions, technology availability or temporal anchors.

4. **Knowledge is observer-specific.**
   - The engine may know the complete truth while the player, a ship, an NPC or a faction knows only a subset.
   - Discovering a fact changes knowledge, not the underlying truth.

5. **Detection is constrained.**
   - Range, sensor quality, power, resolution, filters, interference, damage, masking and the target's signatures determine what can be observed.
   - Partial, uncertain or absent readings are valid outcomes.

6. **AI has no authority over ground truth.**
   - AI may verbalize, summarize or role-play an interpretation of structured data supplied by the engine.
   - AI may not silently add entities, properties or discoveries that the authoritative state did not provide.

7. **Actions are logged.**
   - Operational actions such as scans are recorded with operator, parameters, target area, result summary and relevant confidence/error information.

## Consequence for consoles

A console is an interface to an authoritative system. It assembles a structured operation, submits it to the engine and presents the returned structured result.

The same operation may be exposed through different UX layouts in Starfleet Academy, a Galaxy-class ship, an older vessel or a non-Starfleet vessel.
