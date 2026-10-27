# Federación Unida de Planetas — base de gobierno

## Alcance

Este bloque fija únicamente la estructura política mínima necesaria para que la Federación exista como una entidad viva y jugable. No intenta completar una constitución imaginaria ni inventar instituciones que la pantalla no define con claridad.

## Hechos retenidos

- La Federación Unida de Planetas fue fundada en **2161**.
- La ceremonia fundacional se sitúa en **San Francisco, Tierra**.
- El núcleo fundador retenido para el proyecto está formado por **Tierra, Vulcano, Andoria y Tellar Prime**.
- La Federación es una unión política interestelar de mundos miembros.
- Su gobierno dispone de un **Presidente de la Federación** y un **Consejo de la Federación**.
- Los mundos miembros participan en la gobernanza federal.
- Starfleet está subordinada a la autoridad civil de la Federación; **Federación != Starfleet**.
- En el siglo XXIV tardío la Federación ha crecido hasta superar los 150 mundos miembros y extenderse aproximadamente 8.000 años luz. Este dato no se extrapola hacia atrás a Pike o Kirk.

## Límites deliberados

No fijamos todavía:
- sistema electoral detallado;
- duración de mandatos;
- reparto exacto de escaños;
- competencias constitucionales exhaustivas;
- fiscalidad;
- moneda o ausencia universal de moneda;
- procedimiento completo de adhesión;
- relación jurídica exacta entre cada gobierno planetario y el gobierno federal.

Esos datos se incorporarán solo cuando exista evidencia suficiente o cuando el gameplay requiera una **GAME_ADDITION** explícita.

## Regla temporal

La Federación no es una ficha estática.

Cada campaña carga su situación política hasta la fecha inicial:
- miembros conocidos;
- tratados;
- guerras;
- crisis;
- fronteras;
- relaciones exteriores;
- autoridades conocidas.

Desde el inicio de campaña, el **World State** es autoritativo. Un tratado puede romperse, una guerra puede evitarse o un mundo puede cambiar de situación si la campaña lo produce.

## Regla de modelado

```text
ESPECIE != MUNDO != GOBIERNO != FEDERACIÓN != STARFLEET
```

Ejemplo:

```text
Vulcanos -> especie/cultura
Vulcano  -> mundo miembro
Federación -> entidad política federal
Starfleet -> servicio federal
```

Esto evita que el juego trate automáticamente a todos los individuos de una especie como representantes de su gobierno.

## Procedencia

Fuentes principales:
- `ENT_4X22_THESE_ARE_THE_VOYAGES`
- `TNG_5X17_THE_OUTCAST`
- `ST8_FIRST_CONTACT`
- `ST_OFFICIAL_GET_TO_KNOW_FEDERATION`
- `ST_OFFICIAL_GALACTIC_POLITICS_FEDERATION_DOMINION`

La estructura runtime que convierte estos hechos en estados mutables es una adaptación de juego y no se presenta como burocracia canónica literal.
