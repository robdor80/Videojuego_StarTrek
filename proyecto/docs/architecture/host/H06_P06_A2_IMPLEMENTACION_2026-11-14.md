# H06-P06-A2 · Implementación de la madurez jugable nativa

**Fecha** 14-11-2026. **Base** `bcc6f77e8491677f573ebbde6a1964a19f9e5d1d`. **Rama** `codex/h06-p06-a2-species-maturity`.

## IMPLEMENTADO

| Punto | Comportamiento |
|---|---|
| Generación CMake | El JSON de madurez es una dependencia directa. El generador valida la identidad y versión del contrato, escenario, era, año, unidad y alcance. Comprueba el catálogo completo, las referencias a perfiles, las formas de los mínimos, la ausencia de máximos y la concordancia con la disponibilidad Delta. Excluye los perfiles transformativos. Ante datos incompatibles falla la compilación. |
| Edad numérica | Los 22 mínimos proceden del JSON. Una edad inferior produce `CHANGES_REQUIRED` con `BELOW_PLAYABLE_AGE`. Una edad suficiente permite continuar con la evidencia de madurez y el resto de controles. Se conserva la revisión cronológica de edades fuera del calendario representable. |
| Fecha de nacimiento | El formato previo `AAAA-MM-DD` sigue validando fechas de calendario. Si el mínimo se cumple después de 2383, devuelve `BELOW_PLAYABLE_AGE`. Si se cumple durante 2383, devuelve `PLAYABLE_AGE_UNDECIDED` y mantiene la revisión incluso ante un proveedor dispuesto a resolver evidencia. Si se cumple antes de 2383, el umbral de edad queda satisfecho. Se aplica la regla de año límite a todo 2383, incluidos los nacimientos cuyo aniversario cae el 1 de enero. |
| Excepciones y DLC | `changeling`, `jem_hadar` y `vorta` quedan en `REVIEW_REQUIRED` con `SPECIAL_MATURITY_RULE_REQUIRED`. Solo una regla específica versionada podría habilitar su futura evaluación. Los cinco perfiles Delta devuelven `DLC_DELTA_UNAVAILABLE` como rechazo objetivo. Para edades insuficientes del DLC se comunican ambos rechazos. |
| Autoridad | `MATURITY_EVIDENCE_REQUIRED` exige evidencia individual incluso con `adult_equivalent_status=true`. Conserva la verificación de perfil, origen, ciudadanía, formación y cronología, además de la revisión semántica obligatoria. La evaluación solo devuelve diagnóstico y, tras las dos puertas con controles de ensayo, un recibo interno. Los únicos datos que usa de Core son los necesarios para el cálculo puro de SHA-256. |
| Versión y procedencia | La identidad tiene forma `f10-biography/2:<contrato>/<versión>:<sha256>`. La huella cubre el contenido canónico del JSON completo junto con las demás fuentes. `evaluate` exige la identidad en la evidencia semántica y `eligible` la vuelve a exigir para el recibo, junto con emisor, política, borrador y contexto vigentes. |

## PROBADO

Los casos nativos nuevos recorren el catálogo compilado, aplican el mínimo y la edad inmediatamente inferior a todas las especies numéricas, y prueban los cinco rechazos de DLC y las tres excepciones frente a una autoridad de ensayo que resuelve evidencias. Verifican los cumpleaños límite aun con esa autoridad. La suite de generación modifica una copia del contrato para comprobar que el contenido nuevo cambia la huella y que referencias inválidas, duplicados, máximos, alcances y versiones incompatibles fallan. Los tests de procedencia rechazan evidencia anterior y un recibo con huella distinta bajo el mismo emisor de ensayo.

## BLOQUEADO

La configuración de producto sigue devolviendo `REVIEW_UNAVAILABLE` para un borrador pendiente sin proveedores aprobados. El corte no publica una sesión, crea un `PERSON`, concede una plaza, rango o permiso, ni abre el DLC Delta.

## PENDIENTE

Auditoría independiente de esta entrega y revisión de la fecha de campaña por el autor. H06-P06-A, HU-08 y M1 siguen sin certificación.
