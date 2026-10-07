# Procedural starship fixture — Oberth science ship, 2372

This fixture locks one deterministic reference outcome for the Star Trek ship generator.

## Input

- seed: `shipboard_fixture_001`
- era: `tng_ds9_voyager`
- date: `2372-01-01`
- operator: `starfleet`
- role: `science`

## Expected result

The reference generator selects an **Oberth-class** science ship with:

- stable ship ID `gen:starship:de67f663aaf6de92`;
- temporary generated designation `STARFLEET-6D0EDF`;
- target duty crew: **80**;
- three-watch rotation anchored at **04:00 ship time** for this individual vessel;
- Alpha **28**, Beta **24**, Gamma **24**, relief/float **4**.

The class does **not** canonically require that exact timetable. It is a deterministic game schedule derived from class/crew/watch rules.

## Schedule example

`sample_individual_schedule.json` demonstrates that an Alpha-watch crewmember can also have handoff, training, meals, leisure and protected sleep. Off watch therefore does not mean “free and available”.

## Runtime boundary

This fixture validates content/rules/reference generation. CoreRPG 4.5+ remains the future authoritative owner of live World State, catch-up simulation and persistence.
