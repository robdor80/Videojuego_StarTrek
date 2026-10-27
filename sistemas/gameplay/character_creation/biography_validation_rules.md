# Validación de biografía inicial

Status: **LOCKED BASELINE**

## Principio

> **Una ficha de personaje no entra en el mundo hasta ser validada.**

La ficha inicial describe el pasado del personaje. Después de comenzar la campaña, sus capacidades evolucionan mediante acontecimientos reales y no mediante edición libre.

## Doble puerta obligatoria

La validación combina dos capas:

1. **Reglas autoritativas**  
   Comprueban restricciones objetivas: era, especie, edad, adultez equivalente, cronología, ciudadanía, disponibilidad tecnológica, certificaciones conocidas y otras incompatibilidades deterministas.

2. **Revisión semántica de coherencia asistida por IA**  
   Examina si el conjunto biográfico es plausible aunque cada dato aislado pueda ser válido.

Ambas deben superar la validación.

La IA no puede anular una prohibición objetiva del motor. Las reglas tampoco pueden detectar por sí solas todos los excesos narrativos.

## Qué se valida

### Cronología
- edad compatible con estudios y actividades;
- años de práctica posibles;
- ausencia de solapamientos imposibles;
- experiencia posterior a que la tecnología/institución exista.

### Especie y etapa vital
- adulto equivalente;
- desarrollo biológico compatible;
- capacidades innatas no inventadas fuera del perfil de especie.

### Origen y acceso
- procedencia compatible con fecha/campaña;
- ciudadanía o estatus correctamente modelado;
- acceso plausible a la formación declarada.

### Educación y certificaciones
Una certificación formal requiere una ruta plausible para obtenerla.

Declarar años de afición no equivale automáticamente a una certificación.

### Tiempo disponible
No existe un presupuesto de puntos visible, pero sí una vida finita.

Un humano de 20 años puede haber entrenado una disciplina desde la infancia a alto nivel. No puede haber acumulado simultáneamente varias carreras profesionales largas, doctorados, mandos operativos y maestrías incompatibles con su cronología.

### Experiencias
La revisión distingue:
- afición;
- exposición;
- práctica regular;
- competición;
- estudio formal;
- trabajo supervisado;
- experiencia profesional;
- experiencia operativa real.

## Resultado

```text
VALID
→ ficha aceptada y bloqueada como estado inicial

CHANGES_REQUIRED
→ se enumeran contradicciones o excesos
→ el jugador corrige
→ se vuelve a validar
```

No se “arregla” silenciosamente la biografía en nombre del jugador.

## Ejemplos

**Plausible**  
Humano, 20 años, karate desde los 8, cinturón negro 1.º Dan, gimnasio regular.

**Requiere corrección**  
Humano, 20 años, médico especialista, comandante durante seis años, experto en cuatro artes marciales y doctorado en ingeniería warp.

La objeción no usa puntos: usa cronología, acceso, duración y coherencia.
