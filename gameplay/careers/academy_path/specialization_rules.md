# Reglas de especialización

## Modelo autoritativo

La Academia utiliza **exactamente siete ramas jugables de nivel superior**:

1. **Mando** (`command`)
2. **Vuelo / Navegación** (`flight_navigation`)
3. **Operaciones** (`operations`)
4. **Ingeniería** (`engineering`)
5. **Seguridad / Táctica** (`security_tactical`)
6. **Ciencia / Sensores** (`science_sensors`)
7. **Medicina** (`medical`)

Estos identificadores son canónicos para juego, currículo y web de la Academia.

Los identificadores históricos se normalizan mediante `specializations.json > legacy_id_map`. En particular, `flight_control_navigation` pasa a `flight_navigation`, mientras que `science`, `astrophysics_cartography` y `exosciences` se integran en `science_sensors`.

## Momento de elección

El cadete puede entrar:
- con una preferencia clara,
- con una división provisional,
- sin decidir.

La especialización definitiva no tiene por qué elegirse en la pantalla inicial del personaje.

## Cambio de rumbo

Cambiar de especialización puede exigir:
- tutoría,
- recuperar asignaturas,
- superar una evaluación,
- alargar un semestre o curso en casos extremos.

No borra automáticamente conocimientos ya adquiridos.

## Formación secundaria y subespecializaciones

El sistema admite:
- optativas,
- cursos cruzados,
- cualificaciones complementarias,
- doble foco académico cuando sea razonable,
- subespecializaciones dentro de una de las siete ramas.

Esto permite perfiles tipo:
- Mando + ingeniería,
- Ciencia / Sensores + vuelo,
- Medicina + ingeniería básica,
- Seguridad / Táctica + diplomacia.

**Astrofísica / cartografía**, **Exociencias** y otros focos científicos son subespecializaciones de **Ciencia / Sensores**, no ramas principales adicionales.

## Relación con el currículo

Las asignaturas troncales de especialización de 2.ª y 1.ª clase usan la rama canónica del cadete para resolver el contenido profesional correspondiente.

La biblioteca de rama desarrolla:
- tramos **201–203** durante 2.ª clase;
- tramos **101–102** durante 1.ª clase.

El resultado académico debe conservar el `specialization_id` canónico y las cualificaciones obtenidas. Un contenido de subespecialidad no cambia por sí solo la rama principal.

## Ciencia / Sensores y la consola de Sensores

**Ciencia / Sensores** es una rama académica amplia. Dentro de ella pueden existir cualificaciones diferenciadas, entre ellas:
- análisis científico;
- operaciones de sensores.

El **Manual de Operador de Sensores** no constituye una octava rama. Es material operativo ligado a la cualificación de Sensores y a la consola funcional real.

Reglas:
- el manual debe enseñar las mismas operaciones que existen en `gameplay/ship_operations/consoles/sensors/`;
- las prácticas de Academia deben reutilizar el backend real de Sensores cuando esté disponible;
- **Sensores mide y observa; Ciencia interpreta**;
- una ampliación de la consola que cambie procedimientos debe reflejarse también en el manual operativo;
- la web puede presentar ese manual dentro de la rama **Ciencia / Sensores**, sin mezclarlo con el currículo profesional de rama.

## Efecto en juego

La especialización influye en:
- horario,
- clases disponibles,
- instructores,
- simulaciones,
- prácticas,
- NPC compañeros,
- evaluaciones,
- cualificaciones,
- candidatos a primer destino.

No determina automáticamente el destino final.

Los puestos concretos de una nave son **empleos o cualificaciones**, no nuevas ramas académicas. Por ejemplo, un operador de Sensores puede proceder de Ciencia / Sensores y acreditar la cualificación operativa correspondiente.

## Compatibilidad de partidas y datos antiguos

Al cargar datos históricos:
1. si el identificador ya es uno de los siete canónicos, se conserva;
2. si aparece un identificador de `legacy_id_map`, se normaliza al canónico;
3. la procedencia histórica puede conservarse como metadato, pero no vuelve a crear una rama de nivel superior;
4. ninguna migración debe borrar cualificaciones o progreso previamente obtenido.

## IA

Los instructores y compañeros deben conocer la especialización visible del cadete, sus resultados y su reputación.

La IA no puede conceder una cualificación o cambiar de especialidad sin pasar por la regla autoritativa correspondiente.
