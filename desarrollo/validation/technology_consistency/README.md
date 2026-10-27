# Validación de consistencia tecnológica

## Objetivo

Impedir que una nave, escena o evento reciba tecnología que no corresponde a su fecha/configuración.

## Validación

Para una instalación tecnológica:

```text
fecha de campaña
      ↓
perfil tecnológico de era
      ↓
clase de nave
      ↓
refit/configuración
      ↓
estado individual
```

## Reglas mínimas

1. Una tecnología `unavailable` no puede aparecer salvo excepción explícita con procedencia.
2. `experimental` necesita una definición/entidad concreta que justifique su presencia.
3. `class_specific` exige una clase/configuración compatible.
4. `available` no significa instalación automática.
5. Un refit no puede existir antes de su fecha.
6. La campaña puede destruir/perder una tecnología, pero no inventar una nueva capacidad sin proceso/causa.
7. Un NPC no conoce automáticamente una tecnología clasificada o aún no divulgada.

## Ejemplos

- Replicador completo tipo TNG en 2267 → rechazo.
- Food synthesizer en TOS → válido.
- Gel bioneural en USS Voyager en 2371 → válido.
- Gel bioneural en toda nave Starfleet de 2371 → rechazo.
- Quantum torpedoes en unidad compatible desde 2371 → posible, no automático.
