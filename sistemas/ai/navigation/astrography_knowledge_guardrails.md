# Astrography and navigation AI guardrails

AI may explain routes, hazards and political context only from information available to the ship/character.

## Required behavior

- Distinguish World Truth from charted knowledge.
- Never reveal an uncharted system, hidden fleet, minefield, cloaked force or secret border order just because it exists in global data.
- Present uncertain distances and map-derived placements as uncertain.
- Use current campaign political state, not a future canon map.
- Do not silently convert a licensed-reference placement into SCREEN_CANON.
- Do not invent a precise ETA when propulsion state, route geometry or local subspace conditions do not justify it.
- Do not infer political ownership from a species name or historical association.

## Route explanations

AI may explain:
- candidate routes;
- known border crossings;
- known hazards;
- known support facilities;
- why one route is safer/faster;
- what permissions may be required.

Core resolves:
- actual ship motion;
- travel time;
- encounters;
- border responses;
- sensor discoveries;
- navigation failures;
- persistent exploration state.

## Knowledge layers

The narration must respect:
1. world truth;
2. sensor/chart evidence;
3. database access;
4. character knowledge;
5. player report.

Only layer 5 is automatically player-visible.
