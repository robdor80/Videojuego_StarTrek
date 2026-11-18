# Ciencia

Familia funcional `science`. Pendiente de definición detallada.

## Dependencia ya fijada desde Sensores

Ciencia puede recibir **tareas de análisis estructuradas** procedentes de Sensores.

Flujo mínimo aprobado:

```text
Sensores detecta/mide
→ operador envía datos a Ciencia
→ se crea una tarea de análisis
→ personal de Ciencia interpreta los datos
→ Ciencia puede pedir más lecturas a Sensores
→ los hallazgos vuelven a la ficha persistente del contacto
```

Ciencia añade interpretación científica con su propia procedencia y confianza. No recibe ni puede revelar automáticamente propiedades del mundo que no hayan sido observadas.

Contrato provisional de entrada:
`incoming_analysis_task_contract.json`.

La consola de Ciencia completa se diseñará en su fase correspondiente; este contrato existe ahora para que Sensores pueda entregar datos de forma correcta sin anticipar toda su UX.

## Dependencia de Astrometría 360° — DEC-0023 (18-11-2026)

Astrometría puede mostrar comparaciones científicas y solicitar un **estudio real a Ciencia** mediante un handoff con objeto, datos disponibles, fuente, observación y permisos; Ciencia sigue teniendo autoridad sobre la interpretación y cualquier resultado se registra con procedencia. El estudio no introduce automáticamente hipótesis como verdad ni inventa información científica ausente. Contrato: sistemas/gameplay/ship_operations/interconsole/s11_astrometrics_to_science_study_v0.1.json. Diseño: sistemas/gameplay/astrometrics/S11_ASTROMETRIA_360_DISENO_v1.md.

**Diseño únicamente; sin ejecución verificada.**
