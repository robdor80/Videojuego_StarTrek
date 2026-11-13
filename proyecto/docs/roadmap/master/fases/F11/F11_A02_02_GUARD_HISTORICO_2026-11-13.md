# F11 A02-02 — Alcance temporal del guard histórico

Fecha: 2026-11-13. Estado: AJUSTE DE CI PROPUESTO EN PR (NO FUSIONADO).

## Diagnóstico

La certificación A02-02 de la PR #107 verificó que, desde el árbol auditado
`d54457f20712849902b3815cc20a68ac813bcc4d`, solo cambiaron los
cuatro archivos autorizados de aquella certificación. Su guard
`desarrollo/tools/validation/f11_p05_a02_02_certify.py` continúa con
una allowlist de cuatro archivos que, deliberadamente, no admite fases
posteriores del proyecto. Es apropiada para una auditoría temporal de A02-02,
pero no es una comprobación genérica de integridad de la rama `main`
actual ni de las PR posteriores del HOST.

En PR #135 (H04), la ejecución automática producía FAIL por archivos
legítimos añadidos en H01–H04, LORE y otras fases, no porque fallase
una prueba nativa de ascensos. La evidencia está en el run
https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43453369288.

## Decisión y alcance

- La CI `.github/workflows/f11-a02-02-certification.yml` pasa a ser
  **reproducción manual de una certificación histórica** (`workflow_dispatch`).
- Todos sus checkouts del código Star Trek quedan fijados al merge certificado
  de A02-02: `d222ed98f63127737aa45f955116a3fc60691a48` (PR #107).
  Esto evita confundir la historia certificada con el estado actual.
- **No se modifica el script del guard**, sus expectativas, los oráculos,
  la fuente de CoreRPG ni los pins. Tampoco se relaja la allowlist.
- **No se presenta esta reproducción manual como comprobación de las PR
  posteriores**. Los checks actuales son `f11-native-promotions.yml`
  (13 casos F11 Linux/Windows), `f11-a02-03-native-host-reader.yml`
  (17 casos aislados), `f11-career-reference.yml` y las CI independientes
  de F04/F05/HOST. Cada una mantiene sus propios disparadores y contratos.
- Se retira únicamente la activación automática del *certificado congelado*,
  no las pruebas funcionales vigentes.

## Evidencia y límites

- PR de certificación: https://github.com/robdor80/Videojuego_StarTrek/pull/107
- Merge histórico: `d222ed98f63127737aa45f955116a3fc60691a48`.
- Regresiones H04 CI corregida: https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43453368894 (5/5 jobs PASS).
- Las seis campañas históricas de F04 han pasado con fuentes y oráculos
  inalterados: https://github.com/robdor80/Videojuego_StarTrek/actions/runs/43433024139.
- Este cambio es **de selección de ejecución de CI**, no de código de juego.
- Repetición manual del workflow archivado tras este ajuste: **NOT_RUN**
  hasta disponer de una ejecución real; no se inventa un PASS.
- Mientras la PR de ajuste esté sin fusionar, las ejecuciones automáticas
  del workflow original pueden continuar fallando en ramas no históricas.

Conclusión: conservar la auditoría antigua exactamente como fue certificada
sin utilizar su allowlist temporal para bloquear el desarrollo legítimo
posterior del repositorio.
