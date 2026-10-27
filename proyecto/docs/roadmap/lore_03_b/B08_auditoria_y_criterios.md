# LORE-03B / B08 — Auditoría y puerta de aceptación

**Fecha de integración:** 27-10-2026 · **Base:** `main@9cc9c240` · **Rama:** `lore/03-b-conflicts-crises` · **PR:** [#41](https://github.com/robdor80/Videojuego_StarTrek/pull/41), Draft.

**Dictamen vigente: `NEEDS_REVIEW` — documentación y CI de la rama correctos; pendiente revisión y autorización humana para fusionar.** ST-ORG-01 quedó expresamente desbloqueada por el autor el 27-10-2026. Este expediente no certifica reorganización local del MSI ni validación audiovisual integral.

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

- [ ] Revisión humana del contenido y reservas históricas, sin necesidad de reabrir LORE-03A.
- [ ] Fusión autorizada expresamente de la PR #41 en `main`.
- [ ] Verificación posterior al merge y acta administrativa de cierre `COMPLETE`, sin borrado de rama salvo autorización.

**Principio:** el canon establece antecedentes anteriores al inicio de campaña; después el estado del universo evoluciona exclusivamente bajo CoreRPG. Paz, negociación y soluciones parciales tienen plena legitimidad; no hay guerras por conveniencia del jugador.
