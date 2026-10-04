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
