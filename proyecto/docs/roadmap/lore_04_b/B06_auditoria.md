# LORE-04B06 — Auditoría económica, reservas y cierre documental

**Estado:** DOCUMENTACIÓN CANDIDATA — pendiente de revisión y fusión expresa; no implementación. **Fecha:** 2026-10-29.

## 1. Verificaciones

El plan y los contratos no introducen nueva moneda ni tabla global de valores; no confunden réplica con riqueza ilimitada, no cambian derechos de vivienda, no dan salario por especie, no duplican economía viva. Todos los ejemplos separan verdad económica, observación de NPC y transición de CoreRPG. La historia de Ferenginar se contextualiza temporalmente; la futura campaña permanece abierta.

## 2. Fuente y alcance

Anclas audiovisuales: TNG *Family*; DS9 *Family Business*, *Profit and Lace*, *The Dogs of War*, situaciones de Quark. Referencias oficiales de StarTrek.com: artículo sobre economía, ficha Latinum, Ishka; su valor es editorial/corroborador y **no** crea reglas de moneda universales ni números. Lo no confirmado queda `UNKNOWN`.

## 3. Paquetes de prueba

`lore04b_cases_v0.1.json` recoge casos con precondición y resultados prohibidos, validados documentalmente por la herramienta de `desarrollo/tools/validation/validate_lore04_phase.py`. Se excluyen simulación real, prueba de mundo CoreRPG y validación UE5. La PR debe permanecer Draft hasta revisión del autor.

## 4. Dictamen y reservas

B01–B06 son **candidatos a cierre documental**, no cierre administrativo. Autor decide cualquier economía jugable que exija moneda unificada, valoración de bienes o remuneraciones sin respaldo canónico. LORE-04C podrá usar las necesidades de carga como referencias, no como tráfico ya simulado. LORE-04E verificará el cruce B–D. **Ningún merge o borrado de rama está autorizado**.

---
**Referencias transversales:** `proyecto/docs/roadmap/lore_04_master_plan_v0.1.md`, `mundo/sources/canon_policy.md`, `mundo/sources/provenance_policy.md`, `desarrollo/validation/consistency/movement_logistics_economy_diplomacy_invariants_v0.1.json`. **Autoridad:** CoreRPG WorldState. **No se valida simulación runtime**.
