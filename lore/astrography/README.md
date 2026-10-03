# Astrography — gameplay-first model

Astrography exists to answer player-facing operational questions:

- Where is the destination?
- How far away is it?
- Which route is plausible from the current ship position?
- Which political borders or jurisdictions are crossed?
- What is known, uncertain, restricted or unexplored at the campaign date?
- Which hazards, stations, safe ports and strategic locations matter?
- What can the current crew actually know from sensors, charts and databases?

It is not an atlas for its own sake.

## Layer separation

```text
PHYSICAL SPACE
  systems / objects / coordinates / distances
        +
REFERENCE SECTOR SCHEME
        +
TEMPORAL POLITICAL LAYER
  borders / jurisdiction / treaties / conflicts
        +
KNOWLEDGE LAYER
  explored / charted / classified / uncertain
        =
NAVIGATION GAMEPLAY
```

Political ownership and borders are never baked permanently into physical locations.

## Source hierarchy

Screen canon remains authoritative when it directly establishes a location, distance, route or border fact.

Licensed/official references such as *Star Trek: Star Charts* are used to create coherent working geometry where screen canon is incomplete.

Reliable secondary sources such as Star Trek Dimension are useful for:
- gathering distance statements;
- identifying source episodes/manuals;
- exposing contradictions;
- preserving uncertainty.

Derived coordinates and travel distances must retain their provenance and confidence.

## Campaign rule

Canon initializes geography and political state only through campaign start.

After campaign start:
- borders may change;
- access may change;
- stations may be destroyed or built;
- routes may become unsafe;
- unexplored locations may become charted;
- wars may open or close corridors.

Live World State owns the future.
