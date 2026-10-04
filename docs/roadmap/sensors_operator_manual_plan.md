# Sensors operator manual — delivery plan

Status: **COMPLETE v0.1**

The Sensors console must ship with two synchronized study/reference formats:

1. **In-game Starfleet study manual**
   - Diegetic PADD/LCARS-style presentation.
   - Accessible from Starfleet Academy study material and later from ship Computer/Database help.
   - Uses the real Sensors v0.1 functional tree and procedures.
   - Includes explanations, examples, worked orders, mistakes, exercises and quick-reference pages.
   - Must teach operational use, not Star Trek trivia.

2. **External PDF operator manual**
   - High-quality visual document suitable for reading outside the game.
   - Starfleet/Federation visual treatment, not a plain office-style PDF.
   - Cover, section dividers, LCARS-inspired callouts, diagrams, example console flows and quick-reference sheets.
   - May use user-supplied Starfleet/Federation emblems as decorative/reference assets where appropriate.
   - Content must remain synchronized with the in-game manual.

## Planned structure

- Cover / Starfleet Academy + Starfleet Command identity
- Purpose and operating philosophy
- Console overview
- Status panel
- Scans
- Search / localization
- Contacts
- Tracking
- Sensor readout
- Interference / compensation
- Configuration
- Results
- Diagnostics
- Standard operating procedures
- Worked bridge orders
- Common operator errors
- Practice exercises
- Quick-reference appendix

## Production rule

Sensors v0.1 is approved. The in-game study manual and external designed PDF v0.1 have now been produced from the closed functional specification. Future changes must version both together.


## Delivered

- Canonical in-game text: `gameplay/careers/academy_path/study_materials/sensors/SENSORS_OPERATOR_MANUAL_v0.1.md`
- In-game UX specification: `ui/academy/sensors_manual_experience.md`
- Manifest: `gameplay/careers/academy_path/study_materials/sensors/manual_manifest.json`
- External PDF: generated artifact `Manual_Operador_Sensores_Flota_Estelar_v0.1.pdf` with Starfleet/Federation visual treatment and user-supplied emblems.
