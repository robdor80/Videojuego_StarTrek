# LORE-03B / B08 — Auditoría y puerta de aceptación

**Fecha de integración:** 27-10-2026 · **Base:** `main@9cc9c240` · **Rama:** `lore/03-b-conflicts-crises` · **PR:** [#41](https://github.com/robdor80/Videojuego_StarTrek/pull/41), Draft.

**Dictamen histórico previo a la fusión: `NEEDS_REVIEW` — documentación y CI de la rama correctos; entonces pendiente revisión y autorización humana para fusionar.** ST-ORG-01 quedó expresamente desbloqueada por el autor el 27-10-2026. Este expediente no certifica reorganización local del MSI ni validación audiovisual integral.

## Entregado

- [x] Ocho subfases B01–B08 incorporadas a la rama.
- [x] 22 dossiers históricos en JSON y Markdown con IDs y enlaces a acontecimientos heredados.
- [x] 12 escenarios emergentes hipotéticos, con salida diplomática y sin mutación de WorldState.
- [x] Sin segunda simulación estratégica: los contratos `sistemas/gameplay/conflict/` permanecen intactos.
- [x] Verificados por el validador los 40 IDs LORE-01D, 26 anclas LORE-03A, fuentes y facciones.
- [x] Un solo `dominion_war`; la resistencia cardassiana es subconflicto relacionado.
- [x] Falso golpe tzenkethi preservado como información falsa y no como guerra real.
- [x] Sin fecha exacta inventada para 2383; Rómulo continúa intacto en el punto inicial.
- [x] Sin cambios en CoreRPG, UE5, assets ni sistemas de ejecución.
- [x] CI propio B y regresiones documentales LORE-01D, LORE-02E y LORE-03A: correctas en rama/PR.

## Reservas abiertas

1. **Fechas históricas imprecisas:** la ofensiva Borg de LORE-01D está fechada aproximadamente en 2366 mientras Wolf 359 en LORE-03A aparece en 2367. No se generan dos invasiones distintas.
2. **Bajor:** el comienzo de la ocupación (~2319/~2328) depende de la definición de presencia y control. No se asigna un comienzo único.
3. **Dominio:** los registros `dominion_cardassian_war_bajor` y `dominion_war_begins` pueden solaparse; no crear dos guerras.
4. **Canon frente a interpretación:** los dossiers contienen síntesis editoriales, con fuentes identificadas pero sin revisión de cada escena del corpus audiovisual. No declarar precisión histórica que no se ha contrastado.
5. **Grupos no estatales:** Sección 31, Maquis, hirogen y especie 8472 no equivalen a Estados; algunos actores solo aparecen en texto cuando no hay ID oficial de facción del proyecto.
6. **CI externo a B:** el workflow heredado LORE-02E sobre `main@a5f76737` falló por una prueba F07 que exige nueve `NO_EJECUTADO`; cuatro evidencias ya figuraban como «reportadas, pendientes de cotejo». Este error es anterior y ajeno a B; no falsear el registro.
7. **Runtime:** pruebas documentales verdes NO acreditan implementación en CoreRPG ni Unreal Engine.

## Pendiente para cierre formal

- [x] Revisión y aceptación del alcance documental mediante fusión autorizada de PR #41; reservas históricas continúan documentadas.
- [x] Fusión autorizada de PR #41 en `main` el 27-10-2026 (`2b1447d4`).
- [x] Verificación tras fusión: LORE-03B y LORE-03A en GitHub Actions `success`; rama original eliminada por el autor. Acta administrativa preparada en PR independiente.

**Principio:** el canon establece antecedentes anteriores al inicio de campaña; después el estado del universo evoluciona exclusivamente bajo CoreRPG. Paz, negociación y soluciones parciales tienen plena legitimidad; no hay guerras por conveniencia del jugador.

## Acta de cierre administrativo — 27-10-2026

- **Estado:** `COMPLETE_DOCUMENTARY` tras la fusión de la PR [#41](https://github.com/robdor80/Videojuego_StarTrek/pull/41).
- **Commit de fusión:** `2b1447d4469fb8f52c98486342be61c9a069b90a`; **fecha:** 2026-10-27T11:23:39Z (UTC).
- **Rama de desarrollo:** `lore/03-b-conflicts-crises`, eliminada tras fusión.
- **Pruebas posteriores al merge:** LORE-03B [40495811165](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40495811165) = `success`; regresión LORE-03A [40495811218](https://github.com/robdor80/Videojuego_StarTrek/actions/runs/40495811218) = `success`.
- **Alcance:** cierre documental B01–B08 y 22 dossiers + 12 escenarios; no hay runtime de CoreRPG ni UE5 activado.
- **Reservas:** se preservan sin inventar canon, fechas de batalla o resultados futuros.
- **Siguiente fase:** LORE-03C podrá iniciarse tras integrar esta regularización, sin iniciar desarrollo automáticamente.
