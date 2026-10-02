# Universal Rank Insignia

Status: **APPROVED GAME DESIGN**

## Decision

All playable eras use the **TNG-style pip language** for fast rank recognition, even when the historical uniform of that era originally used sleeve braid, pins or another insignia system.

This is an intentional `GAME_ADDITION`.

The underlying Starfleet rank is canon-based; only the cross-era visual standardisation is project-created.

## Standard commissioned-officer pips

Legend:
- `●` = solid gold pip
- `○` = black pip with gold rim (shown here as hollow for readability)

| Rank | Spanish | Project pip display |
|---|---|---|
| Ensign | Alférez | ● |
| Lieutenant junior grade | Teniente júnior | ●○ |
| Lieutenant | Teniente | ●● |
| Lieutenant commander | Teniente comandante | ●●○ |
| Commander | Comandante | ●●● |
| Captain | Capitán | ●●●● |

The black pip is **not** a half-painted pip. It represents the intermediate step in the TNG-era visual system.

## Flag officers — canon vs project normalisation

TNG-era flag officers use **boxed/framed gold pips**.

The retained canon/reference mapping is strongest from two pips upward:

| Display | Canon/reference interpretation |
|---|---|
| [●] | one-star admiral; exact retained-era title is ambiguous |
| [●●] | Rear Admiral / two-star admiral |
| [●●●] | Vice Admiral / three-star admiral |
| [●●●●] | Admiral / four-star admiral |
| [●●●●●] | Fleet Admiral / five-star admiral reference pattern |

### Project treatment of Commodore

`Commodore` is a real Starfleet flag rank historically shown in the TOS period, one grade above Captain.

However, **TNG does not cleanly establish that one boxed pip means Commodore** within the retained screen scope.

Therefore the game uses:

| Rank | Spanish | Project display | Status |
|---|---|---|---|
| Commodore | Comodoro | [●] | GAME_ADDITION visual mapping |
| Rear admiral | Contraalmirante | [●●] | canon-aligned |
| Vice admiral | Vicealmirante | [●●●] | canon-aligned |
| Admiral | Almirante | [●●●●] | canon-aligned |
| Fleet admiral | Almirante de Flota | [●●●●●] | reference-aligned |

This gives the player one clean progression while keeping the provenance distinction explicit.

## Scope

Applied in:
- Pike / Strange New Worlds
- Kirk / TOS + films
- TNG + DS9 + Voyager

Historical uniform styling remains era-specific. Only the **rank-reading language** is unified.

## Special cases

- Cadet is a training status, not part of the commissioned-officer ladder above. Cadet academic class uses the separate universal silver-pip system defined in `docs/decisions/universal_cadet_insignia.md`.
- Enlisted / NCO ranks are separate and will receive their own insignia model.
- Fleet captain is not part of the normal promotion ladder; it is retained as a rare/special historical grade/title for separate treatment.
- Provisional/Maquis rank bars are a separate system and will be modeled when Voyager-era personnel rules are researched.

## Design reason

The player should be able to look at an NPC and read rank instantly in every era without learning three unrelated insignia systems.
