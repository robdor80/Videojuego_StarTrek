# A04 — Criterios de aceptación y cierre de LORE-05A

**Estado a fecha de creación:** candidata documental; las comprobaciones deben ejecutarse, no presumirse.

## Invariantes

1. `Proyecto Valhalla` es programa, no clase ni nuevo nombre de la nave.
2. `uss_enterprise_ncc_1701_d` conserva `NCC-1701-D` y `class_id=galaxy` ya presentes en catálogo.
3. Fecha Academia **2383**; Odyssey operativa; la Enterprise-D está en reconstrucción, no lanzada por defecto.
4. 2387 es objetivo **condicional**, no garantía universal de disponibilidad, destino o capitanía.
5. 2401 es hecho audiovisual posterior documentado y **no** un evento que deba imponerse en la partida.
6. El casco Syracuse no es automáticamente el donante de 2387, ni se instala flujo cuántico por defecto.
7. No se eliminan ni renombran los datos históricos de clase `valhalla`, las 16 decisiones tecnológicas o la dotación F04.
8. El gobierno de autoría conserva `SCREEN_CANON`, `OFFICIAL_REFERENCE`, `GAME_ADDITION` y `UNKNOWN` separados.
9. No cambia CoreRPG, motor de partida, juego 3D, activos, datos de guardado ni `CONTENT_STATUS.md`.
10. Se mantienen intactos los cierres documentales de LORE-01–04.

## Verificación reproducible

- `python3 desarrollo/tools/validation/validate_lore05_a.py`
- `python3 -m unittest discover -s desarrollo/tools/validation -p 'test_lore05_a.py' -v`
- GitHub Actions `LORE-05A — Reconciliación documental`.
- Examinar PR contra `main` y comprobar que ningún archivo histórico de clase o CoreRPG ha sido reescrito.
- Verificar CI del **último SHA** y, tras aprobación de fusión, volver a comprobar CI y archivos de `main`.

**Solo después de la fusión efectiva** podrá registrarse `LORE-05A COMPLETE_DOCUMENTARY` en el estado administrativo. LORE-05 global continuará abierta para B–F.
