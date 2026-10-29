# LORE-04E07 — Invariantes, regresiones y pruebas adversariales

**Estado:** AUDITORÍA DOCUMENTAL EN PR DRAFT — sin merge, sin certificación runtime ni decisiones creativas añadidas.

## 1. Ejecución reproducible

`desarrollo/tools/validation/validate_lore04_phase.py` y `test_lore04_phase.py` comprueban cada fase B/C/D/E y sus fixtures contra su rama. `validate_lore04_e_crossphase.py` y `test_lore04_e_crossphase.py` añaden integridad interdependiente. Las Actions incluyen las regresiones A/LORE-03/01/02, sin modificar sus archivos. Los tests no necesitan conectarse a la red ni a una escena ejecutable.

## 2. Fallos que deben detectarse

Casos de ensayo: fuente no registrada convertida en canon, `WorldState` propiedad de IA, escenario marcado runtime, salario/moneda universal declarado, ciudad que se genera en el instante de llegada, pasajero duplicado, capacidad aumentada por prioridad, competencias civiles de Flota inventadas, miembro de Tal Shiar inferido por etnia, ley penal inexistente, cambio de identidad en LOD, canon posterior impuesto al jugador.

## 3. Matiz de resultados

La validación de formato/propiedad/referencias es **documental** y se puede marcar PASS cuando realmente se ejecuta. Las simulaciones de mercado, cola física, policía o NPC autónomo solo pueden declararse PASS si las ejecuta CoreRPG/UE5 y hay evidencia de mundo cargado y persistido. No se inflarán conteos declarando tests no ejecutados.

## 4. Criterio

E07 se considera listo para auditoría de PR cuando las Actions de último HEAD y sus variantes adversariales pasan y no existen conflictos o fallos CI. Un pull request apilado requiere revisar también los commits de B/C/D y sus comparaciones con las bases, no solo la última ejecución E.

**Control:** CoreRPG es dueño del WorldState; fuentes de verdad LORE-01/02/03 y F00–F15 no se duplican. El dictamen final depende de CI, revisión de autor y fusiones posteriores expresas.
