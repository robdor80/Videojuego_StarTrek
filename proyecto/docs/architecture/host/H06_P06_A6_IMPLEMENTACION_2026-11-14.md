# H06-P06-A6 · Validador nativo de antecedentes iniciales F10

**Fecha** 14-11-2026. **Base** `b6ab80c1f4489dc70b36f4871427bedde5276ac4`. **Rama** `codex/h06-p06-a6-initial-background`.

## IMPLEMENTADO

- El generador comprueba versión, escenario, era, año, fecha pendiente y pin de campaña del contrato A5. Comprueba también el alcance de la atestación, las clases personales admitidas y la obligatoriedad de la revisión semántica. El contrato completo participa en la huella de reglas y su ID y versión identifican la fuente interna F10.
- El evaluador reutiliza los resultados cronológicos del validador existente. Puede respaldar `ACTIVITY_BUDGET_REVIEW` para el campo de actividades y aficiones cuando todas las entradas estructuradas tienen nombre y un periodo comparable. Acepta edades o fechas completas con nacimiento fechado, y un fin explícito o `current`. Las entradas sin fechas comparables, los periodos solapados y el texto sin estructura quedan pendientes. Este alcance evita deducir horarios o acceso a instituciones. Una contradicción cronológica demostrada conserva el rechazo existente.
- La puerta objetiva separa la cronología de aficiones de los requisitos de origen y hechos del mundo, estudios, certificaciones, experiencia profesional y legalidad. Los antecedentes que declaran recursos tecnológicos o incluyen afirmaciones adicionales sobre formación, acreditación o acceso siguen en revisión. El texto de espacios narrativos como nombre, interés u objetivo no se traduce en conclusiones sobre capacidades, instituciones o permisos. Los campos de autoridad forjados se rechazan.
- Cuando el contexto permite una evaluación, `BiographyValidator` presenta la atestación de alcance único a `RegisteredBiographyAuthority`. El registro comprueba el código y campo, la fuente, versión, emisor, origen y vinculación exacta al borrador canónico, campaña, perfil y generación. Una contradicción o revocación aplicable prevalece. Solo el evaluador nativo puede aportar un resultado favorable bajo su propio ID. La composición por defecto registra esta fuente y una composición explícita debe registrarla para habilitarla.
- `MATURITY_EVIDENCE_REQUIRED` sigue pendiente. Las edades ambiguas, los casos de especie especial y el calendario indeterminado bloquean la atestación nativa. Los cinco perfiles Delta se rechazan antes de consultar evidencias. La segunda puerta sigue obligatoria. El producto devuelve `REVIEW_UNAVAILABLE` para borradores pendientes.

## PROBADO

Los casos nativos comprueban karate desde los ocho años, astronomía, periodos consecutivos y fechas completas. Cubren también cronologías incompatibles, datos incompletos, periodos solapados, certificados, declaraciones institucionales, permisos falsos, cambios de borrador y generación, versión anterior, revocación y ausencia de proveedores. La generación de reglas prueba la invalidez de una política que suprima la puerta semántica y el cambio de huella ante cambios del contrato.

## BLOQUEADO Y PENDIENTE

Madurez individual, fuentes institucionales o del mundo, proveedor semántico, reglas de las tres especies especiales y fecha completa de campaña. Los resultados de este módulo son diagnósticos privados de plausibilidad. La publicación de PERSON, admisión, permisos y rangos queda fuera de esta operación.
