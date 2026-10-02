# Content Research Workflow

Standard operating procedure for adding Star Trek knowledge to the repository.

## 1. Select one bounded block

Work on one coherent subject at a time.

Examples:
- Starfleet ranks,
- Academy admissions,
- Constitution-class,
- Vulcan culture.

Do not open unrelated lore fronts during the same pass unless a dependency requires it.

## 2. Define the questions

Before browsing, identify what the game needs to know and which claims are chronology-sensitive.

## 3. Research in project order

1. Series and films.
2. Licensed novels and comics.
3. Internet research:
   - official Star Trek / Paramount references,
   - specialist reliable secondary sources,
   - broader web only as needed.

## 4. Capture provenance

Register every source that materially supports retained information.

Do not retain an unattributed fact just because several websites repeat it.

## 5. Resolve or expose conflicts

Apply `sources/canon_policy.md`.

Unresolved contradictions go to `sources/unresolved_conflicts/`; they are not silently averaged together.

## 6. Separate fact from interpretation

Classify material as:
- canon/reference fact,
- licensed expansion,
- inference,
- game addition.

## 7. Write human-readable lore first

Use Markdown for explanation, nuance, sources and unresolved questions.

Create JSON only when structured data adds real value or a schema is sufficiently understood. Do not prematurely freeze runtime schemas.

## 8. Validate temporal consistency

For chronology-sensitive material, check:
- era availability,
- character age/status,
- assignments,
- ship service dates,
- technology availability,
- political state.

## 9. Escalate only true design decisions

Use `NEEDS_ROBERTO` only when research cannot decide the matter and a project choice affects the game.

Routine research choices are handled without escalation.

## 10. Update CONTENT_STATUS.md

A block reaches `COMPLETE` only when:
- current research scope is satisfied,
- provenance is recorded,
- known contradictions are resolved or explicitly logged,
- structure is coherent,
- relevant validation has passed.

## 11. Commit coherently

Prefer one commit per completed research block or tightly related set of foundation changes.

Commit messages should describe the domain, not the browsing process.
