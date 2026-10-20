# Technology

## Purpose

This directory stores technology knowledge needed by lore, gameplay validation and procedural generation.

Technology is not only descriptive reference. It constrains what a generated ship, facility, civilization or character can plausibly possess in a given era.

## Core dimensions

Technology data should distinguish where relevant:

- technology identity;
- function;
- era/date validity;
- faction/civilization validity;
- maturity/availability;
- compatible platform/class;
- normal operating constraints;
- resource/power requirements;
- detectable signatures;
- known failure modes;
- interaction with other systems;
- whether access is restricted;
- provenance.

## Availability is not installation

A technology being available in an era does not mean every ship has it.

```text
ERA AVAILABILITY
      +
FACTION / CIVILIZATION
      +
SHIP / FACILITY DESIGN
      +
REFIT / CAMPAIGN HISTORY
      ↓
ACTUAL INSTALLED CAPABILITY
```

## Procedural-generation use

Procedural generators may use this data to determine:

- valid propulsion;
- power systems;
- sensors;
- weapons;
- shields;
- computers;
- communications;
- transporters;
- medical/science capability;
- civilian/industrial systems.

Generators must not use technology that is invalid for the date, culture or platform merely because it exists somewhere in the catalogue.

## Existing areas

- communications;
- computers;
- energy;
- era baseline;
- experimental;
- holography;
- medical;
- propulsion;
- replicators;
- sensors;
- shields;
- transporters;
- tricorders;
- weapons.

Coverage remains progressive and should be driven by gameplay and procedural-universe needs.

## LORE-02 A — tecnología de naves y estaciones (en investigación)

- [Plan maestro A–E](../../docs/roadmap/lore_02_master_plan_v0.1.md).
- [Notas de investigación 02-A](../../docs/roadmap/lore_02_a_research_notes_v0.1.md).
- [Dossier de las ocho lagunas A-G01–A-G08](../../docs/roadmap/lore_02_a_eight_gaps_dossier_v0.2.md): referencias externas consultadas, reglas cautelares, casos negativos y cuestiones todavía abiertas.
- [Catálogo cualitativo inicial (14 sistemas)](ship_station_catalogue_v0.1.json): fuentes, disponibilidades derivadas de matriz, dependencias, fallos y restricciones, sin cifras inventadas.
- [14 casos negativos](ship_station_cases_v0.1.json): cambios de época, sistema no instalado, observación parcial, acciones no autorizadas y DLC Delta reservado.
- Validación: `python tools/validation/validate_lore02_a.py`; regresiones: `python tools/validation/test_lore02_a.py`.

**Estado:** `IN_PROGRESS`; el conjunto es un primer corte de investigación para PR Draft. No altera contratos de gameplay, categorías CoreRPG ni equipos UE5. Faltan impulso/energía/comunicaciones/soporte vital y tecnología específica de estaciones y otras civilizaciones; no declarar fase A `COMPLETE` hasta resolver las lagunas.

### Clase Valhalla — decisiones de diseño aprobadas

- [Perfil conceptual VAL-TEC-01 a VAL-TEC-16](valhalla_tech_profile_v0.1.md): 8 elecciones B expresas y 8 opciones B adoptadas por delegación creativa; restricciones y salvaguardas, incluido triple escudo + ablativo.
- [Registro de aprobación y procedencia por decisión](valhalla_tech_decisions_v0.1.json): metadatos de diseño, **no** contrato de capacidades ni estado instalado.
- Valhalla es **clase nueva inspirada en Galaxy**, no un refit oficial Galaxy. IDEA-0010 sustituye a IDEA-0004; no hay yate activo ni autorización automática de camuflaje, fechas, prestaciones o equipamiento de la nave auxiliar.
- Este perfil **avanza A-G07 conceptualmente**, pero no declara cerradas las ocho lagunas ni sustituye la investigación y contraste del canon.
