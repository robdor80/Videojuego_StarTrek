# Starfleet Ranks

## Commissioned officer ladder

The normal commissioned-officer progression used by the game is:

1. **Ensign — Alférez**
2. **Lieutenant junior grade — Teniente júnior**
3. **Lieutenant — Teniente**
4. **Lieutenant commander — Teniente comandante**
5. **Commander — Comandante**
6. **Captain — Capitán**
7. **Commodore — Comodoro**
8. **Rear admiral — Contraalmirante**
9. **Vice admiral — Vicealmirante**
10. **Admiral — Almirante**
11. **Fleet admiral — Almirante de Flota**

Ranks from commodore upward are flag-officer ranks.

## Important distinctions

**Rank is not position.**

Examples:
- A captain by rank may command a starship.
- A commander may be a first officer.
- A lieutenant commander may be chief engineer.
- A captain may hold a staff assignment and command no ship at all.

The words `Captain`, `Commander`, etc. must therefore never be used as a substitute for a character's job/position field.

## Game visual standard

See:
- `docs/decisions/universal_rank_insignia.md`
- `rank_insignia_standard.json`

The project deliberately uses TNG-style pips in every playable era for readability.

## Special / non-standard grades

### Fleet captain

Star Trek has used `fleet captain`, but it is not treated as a normal rung in the player's promotion ladder because its exact status and historical use are exceptional and inconsistent.

It will be modeled separately if a story or NPC requires it.

### Cadets

Cadet grades belong to Starfleet Academy and are not commissioned-officer ranks.

### Enlisted and NCO personnel

Crewmen and petty/chief petty officers are a separate personnel track. They must not be collapsed into the commissioned ladder.
