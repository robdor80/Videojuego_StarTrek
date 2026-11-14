# H06-P06-A6 · Factibilidad del validador de antecedentes iniciales

**Fecha** 14-11-2026. **Base** `b6ab80c1f4489dc70b36f4871427bedde5276ac4`. **Dominio** F10.

## Fuentes y alcance

| Revisión | Reutilización |
|---|---|
| [#152](https://github.com/robdor80/Videojuego_StarTrek/pull/152) | Validador nativo, borrador canónico, dos puertas y recibo privado. |
| [#153](https://github.com/robdor80/Videojuego_StarTrek/pull/153) y [#154](https://github.com/robdor80/Videojuego_StarTrek/pull/154) | Contrato y verificación de especie, edad, restricciones de Delta y fecha de campaña. |
| [#155](https://github.com/robdor80/Videojuego_StarTrek/pull/155) y [#156](https://github.com/robdor80/Videojuego_StarTrek/pull/156) | Frontera semántica y autoridad de evidencias con registro de procedencia, alcance y vigencia. |
| [#157](https://github.com/robdor80/Videojuego_StarTrek/pull/157) | [Política de antecedentes iniciales](../../../../sistemas/gameplay/character_creation/f10_initial_background_policy_v0.1.json) y referencia offline. La atestación prevista respalda la plausibilidad de un antecedente antes de crear PERSON. |

## IMPLEMENTADO

La comprobación de cronología de F10 ya obtiene la información necesaria para acotar una actividad personal estructurada. Su resultado se reutiliza para producir una atestación de alcance limitado que resuelve el registro existente. La referencia offline de la PR #157 conserva su función de triaje.

## PROBADO

La base coincide con el merge de la PR #157. La composición HOST exige un checkout CoreRPG limpio en `76a7b7b485616d8c4994f384a90f123bf333591d`. La matriz existente permite verificar el alcance nativo y el ABI de producto en Windows y Linux, además de ASan/UBSan.

## BLOQUEADO

La procedencia institucional, la madurez individual y la revisión semántica requieren reglas o proveedores aprobados. El contrato de antecedentes personales permite avanzar antes de esas decisiones.

## PENDIENTE

Auditoría independiente, reglas específicas de especie, fecha completa de campaña y fuentes para afirmaciones que dependen de hechos del mundo.
