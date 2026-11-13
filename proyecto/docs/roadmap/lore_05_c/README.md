# LORE-05C — Mundos, colonias y localizaciones

**Fecha:** 13/11/2026 · **Estado:** cierre documental candidato; runtime NO implementado.

El contenido añade dieciséis identidades narrativas sin duplicar los perfiles físicos ni la lógica de la Planificación 2. Trece están ancladas en el atlas anterior, Marte se refiere al contexto Sol pero no tiene anclaje planetario autónomo, y Dorvan V y Nueva Bajor quedan en consulta histórica (sin nuevos nodos de navegación).

## Entregables
- [Guía narrativa 2383](../../../../mundo/lore/astrography/worlds/lore05c_guia_localizaciones_2026-11-13.md).
- [Catálogo de 16 fichas](../../../../mundo/lore/astrography/worlds/lore05c_priority_locations_v0.1.json).
- [Matriz de 12 escenarios de seguridad narrativa](../../../../mundo/lore/astrography/worlds/lore05c_validation_cases_v0.1.json).
- Validador: `desarrollo/tools/validation/validate_lore05_c.py`.
- Pruebas adversariales: `desarrollo/tools/validation/test_lore05_c.py`.
- Workflow independiente: `.github/workflows/lore05-c-documentary.yml`.

## Entrega editorial y límites
1. Los anclajes y las instalaciones preexistentes NO cambian. Ninguna coordenada, ruta o frontera se crea.
2. Bajor y DS9 mantienen autoridades separadas; no confundir especie con ciudadanía, organización o autoridad.
3. Nueva Bajor NO existe como colonia activa en 2383. Dorvan V no recibe una supervivencia inventada. Marte no se convierte en astillero de Valhalla por defecto.
4. 2383 es fecha inicial. El alta de Enterprise-D en 2387 es objetivo condicionado; no se trasplanta el futuro de la serie Picard.
5. No se amplía elenco LORE-05B (12 NPC cerrados); no se ejecuta DLC Delta.
6. Narración y mapa obedecen a CoreRPG, F11/HOST, permisos y conocimiento. Es material documental.

**Criterio de cierre:** validar contenido referenciado contra anclajes, registro de fuentes y catálogos físicos; 12 escenarios documentales y mutaciones negativas; CI del HEAD de PR en verde; fusionar por PR si está autorizado. El éxito NO certifica UE5, HOST ni WorldState.
