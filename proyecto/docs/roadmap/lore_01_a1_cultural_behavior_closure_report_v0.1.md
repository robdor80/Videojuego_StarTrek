# Informe de entrega LORE-01 A.1 — Personalidad individual frente a cultura

**Fecha:** 17-10-2026. **Repositorio:** `robdor80/Videojuego_StarTrek`. **Rama:** `lore/01-a1-npc-cultural-behavior`.

**Punto de partida real:** PR #25 de LORE-01 A aprobada y fusionada en `main` (`abcc4c77af37d0aaf8d5eb09b65b480c34c4042b`).

## Alcance entregado

- 25 guías culturales contextuales JSON; 20 principales y cinco exclusivamente futuro DLC Delta.
- Cada guía incluye comunicación, emoción, conflicto, autoridad, vínculos, educación/cultura de procedencia, variaciones, advertencias contra estereotipos, referencia al corpus y **dos resultados contrastados** de personajes de la misma especie.
- `behavior_context_contract_v0.1.json`: prioridades de estado persistente, cultura, personalidad, situación, IA y autoridad CoreRPG; prohibición de rasgos estadísticos raciales.
- `species_behavior_index_v0.1.json`: índice, disponibilidad 20/5 y reserva DLC.
- `npc_dialogue_context_examples_v0.1.json`: nueve escenas editoriales de contraste con resultados permitidos y prohibidos.
- Validador y pruebas de regresión con GitHub Actions propia.

## Criterios editoriales

- **Una especie no recibe personalidad prefijada** y un NPC puede tener varias culturas por crianza; la especie es índice para consultar investigación, NO selector de probabilidades.
- Los valores de una comunidad pueden explicar cortesía, lenguaje o reacción sin obligar a cada miembro. Las personalidad y memoria individual tienen prioridad.
- En aenar, breen y pakled el estilo social colectivo queda **desconocido** hasta donde permiten las series retenidas. No se inventan tendencias para cumplir una tabla.
- Borg sigue siendo condición de persona, nunca una especie con carácter propio. El-aurianos en Alfa y el Borg canónico de TNG continúan permitidos; Delta está protegido.
- Fuente: anclajes de la PR #25 por episodio/fuente; no hay inspección escena por escena ni auditoría psicológica del reparto completo.

## Límites técnicos

Ningún algoritmo de creación de NPC, proveedor LLM, consulta de bases de conocimiento, UE5, CoreRPG o generador del mundo ha sido modificado. Los archivos proponen contratos e información para **futura integración**, no hablan por NPC actualmente. No se incorporan diálogos canónicos literales ni decisiones inalterables de campaña.

## Procedimiento de cierre

1. CI A.1 verde y regresiones A verdes; PR creada y sin conflictos.
2. Revisión y fusión por propietario. **No fusionar automáticamente**.
3. Comprobar material y CI en `main`, borrar rama cuando se autorice.
4. LORE-01 B (civilizaciones y potencias) permanece sin iniciar por regla secuencial.
