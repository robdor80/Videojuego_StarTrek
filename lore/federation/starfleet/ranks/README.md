# Starfleet Ranks

## Commissioned officer ladder

The normal commissioned-officer progression used by the game is:

1. **Ensign — Alférez**
2. **Lieutenant junior grade — Teniente júnior**
3. **Lieutenant — Teniente**
4. **Lieutenant commander — Teniente comandante**
5. **Commander — Comandante**
6. **Captain — Capitán**

## Flag ranks

The project recognizes these Starfleet flag grades:

- **Commodore — Comodoro**
- **Rear admiral — Contraalmirante**
- **Vice admiral — Vicealmirante**
- **Admiral — Almirante**
- **Fleet admiral — Almirante de Flota**

### Important historical nuance

Commodore is directly established in the TOS period as a flag rank above Captain.

In the TNG boxed-pip system, the clean canon/reference mapping is:
- 2 boxed pips → Rear Admiral
- 3 boxed pips → Vice Admiral
- 4 boxed pips → Admiral
- 5 boxed pips → Fleet Admiral reference pattern

A **one-boxed-pip** insignia exists in reference material as a one-star admiral grade, but the retained TNG/DS9/Voyager screen scope does not cleanly name it `Commodore`.

The game still maps Commodore to one boxed pip for universal readability, explicitly as a `GAME_ADDITION`.

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

Star Trek establishes `fleet captain` as a rare command distinction/title associated with authority over more than one unit or facility. It is **not** treated as a normal rung in the player's promotion ladder.

### Cadets

Cadet grades belong to Starfleet Academy and are not commissioned-officer ranks.

### Enlisted and NCO personnel

Crewmen and petty/chief petty officers are a separate personnel track. They must not be collapsed into the commissioned ladder.

### Provisional/Maquis personnel

Voyager-era provisional rank devices are a separate visual/personnel system. They will be documented when the Maquis/Starfleet integration rules are researched.
