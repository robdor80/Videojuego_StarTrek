# Ruta jugable de la Academia

Starfleet Academy is the first full playable career hub.

## Player journey

```text
VALIDATED CHARACTER
  ↓
ACCESS / ADMISSION
  ↓
CADET DE 4.ª CLASE
  ↓
CADET DE 3.ª CLASE
  ↓
SPECIALIZATION CHOICE
  ↓
CADET DE 2.ª CLASE
  ↓
CADET DE 1.ª CLASE
  ↓
GRADUATION
  ↓
ALFÉREZ
  ↓
DESARROLLO PROFESIONAL EN SERVICIO
```

Each Academy year is divided into **three trimesters**.

## Access v1.0

The definitive access scope is under `access/`.

Five compact blocks:
- ACC-01 Federación y Flota Estelar
- ACC-02 Cómo se organiza Starfleet
- ACC-03 Vida a bordo de una nave
- ACC-04 Tecnología básica de Starfleet
- ACC-05 Principios del servicio en Starfleet

Access is general orientation. Professional depth belongs to Academy.

## Core gameplay pillars

- **Tiempo** — classes, appointments, training and free time compete for the cadet's day.
- **Competencia** — courses, simulations and practical work build real game capabilities.
- **Expediente** — evaluations, commendations, reprimands and qualifications persist.
- **Relaciones** — cadets and instructors remember the player.
- **Elecciones** — specialization is chosen by the player at the end of Third Class.
- **Consecuencias** — failure may mean remediation, retakes, delayed progression, discipline or altered opportunities rather than automatic game over.
- **Vida** — study, practice, rest, social life, hobbies and relationships share the same calendar.
- **Era** — the same Academy architecture is presented/configured differently for Pike, Kirk and TNG/DS9/Voyager.

## Learning loop

```text
THEORY
→ INSTRUCTOR CLASS
→ REAL-SYSTEM PRACTICE
→ CONTINUOUS EVALUATION
```

Academy may require player knowledge that was explicitly taught. It does not use untaught trivia as a gate.

## Character continuity

The cadet enters with a validated biography, existing hobbies/experience and long-term objectives.

Academy life can therefore develop both professional and non-professional capabilities. A cadet may improve fitness, martial arts, music, languages, medicine or any other plausible domain through sustained activity even when it is not their chosen specialization.

## Career continuity

Graduation is not the end of learning.

The post-Academy path continues through supervised Ensign service, ship/class familiarization, qualifications, mentorship and increasingly autonomous responsibility.

See:
- `academy_career_v0_2.md`
- `academic_year_trimester_model.json`
- `access/`
- `../post_academy/README.md`

## Academy Life & Social Simulation

The living-Academy layer is tracked in `life/` and `docs/roadmap/academy_life_social_simulation_plan_v0.1.md`.

Current status: **Step 1/20 — Academy population COMPLETE.** The Academy population now has explicit cohort/group accounting, Tier A/B/C conservation, player-slot accounting and membership/presence separation. Procedural individual cadet generation is deliberately reserved for Step 2.
